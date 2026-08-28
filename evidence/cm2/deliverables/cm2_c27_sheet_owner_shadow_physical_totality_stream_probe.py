#!/usr/bin/env python3
"""Independent physical-totality reconstruction for SHEET_OWNER/SHADOW.

The candidate universe is generated from primitive half-open geometry, not
from Round306C27, its FAMILIES table, or an edge ledger:

* R204 candidates are regenerated from the complete open-region ledger.  The
  positive/negative target-factor sides determine the unique pair, and the
  source half-open convention assigns the equality sheet to the positive
  side.
* R211 candidates are regenerated from the complete R208 leaf/region ledger.
  Factor signs determine the unique E/W side and N/S side, while the pinned
  R173 convention assigns the sheet to E/W and excludes it from N/S.

The C21/C26 rows are consumed only after candidate generation, as theorem and
downstream binding checks.  In particular C26 has no shadow node; this probe
materializes a separate, explicit shadow-companion ledger from the primitive
geometry.  It issues local zero credit only.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import random
import sys
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent
R173 = "cm2_round173_source_g_exact_return_signature_transport_certificate.json"
R204 = "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
R208 = "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C20 = "cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz"
C21A = "cm2_round306c21a_source_g_1008_r204_A1_A2_direct_feature_kernel_ledger.jsonl.gz"
C21B = "cm2_round306c21b_source_g_17716_r211_self_contained_sheet_theorem_materialization_ledger.jsonl.gz"
C21C = "cm2_round306c21c_source_g_79084_r211_A1_A2_incidence_closure_ledger.jsonl.gz"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C26 = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz"
PINS = {
    R173: "5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a",
    R204: "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    R208: "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    C20: "bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922",
    C21A: "1c60f2ef752b1b3ab363740cec7505cbddacfbc7509922dab63bbf011e3659f1",
    C21B: "1500052cf49cfa7a22388567173a912be6b79d2ba647ad5d1906f9e170dc26bb",
    C21C: "add22270845ef504427475e91696451f2d53c41b4b2cb9af2784a9507ce60c09",
    C25: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    C26: "fc6d1a31e9e7c476bde73336c18d7ad4fb92deed71c3f7b7c58638c0ffc8e88e",
}
STRICT = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
OPPOSITE = {
    "STRICT_NEGATIVE": "STRICT_POSITIVE",
    "STRICT_POSITIVE": "STRICT_NEGATIVE",
}
CELL_SIGNS = {
    "E": ("STRICT_POSITIVE", "STRICT_POSITIVE"),
    "N": ("STRICT_POSITIVE", "STRICT_NEGATIVE"),
    "W": ("STRICT_NEGATIVE", "STRICT_NEGATIVE"),
    "S": ("STRICT_NEGATIVE", "STRICT_POSITIVE"),
}
SIGN_CELL = {value: key for key, value in CELL_SIGNS.items()}
NONPROMOTION_21 = {
    "B1A": 0, "B2": 0, "CM2": 0, "DSU_edge": 0,
    "DSU_union": 0, "maximality": 0,
}
NONPROMOTION_26 = {
    "B2": 0, "CM2": 0, "DSU_edge": 0, "maximality": 0,
    "member_identity": 0, "pair_routing": 0, "transition_theorem": 0,
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def closed(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label)


def checked_rows(name: str) -> Iterator[dict[str, Any]]:
    with gzip.open(ROOT / name, "rb") as stream:
        for ordinal, raw in enumerate(stream):
            need(raw.endswith(b"\n"), f"newline:{name}:{ordinal}")
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) + b"\n" == raw,
                 f"canonical:{name}:{ordinal}")
            closed(row, f"row closure:{name}:{ordinal}")
            yield row


def envelope(name: str) -> dict[str, Any]:
    raw = (ROOT / name).read_bytes()
    value = json.loads(raw)
    need(
        type(value) is dict
        and set(value) == {"schema", "result", "result_sha256"}
        and value["result_sha256"] == digest(value["result"]),
        "sealed envelope:" + name,
    )
    return value["result"]


def signature_core(value: dict[str, Any]) -> dict[str, Any]:
    return {
        key: item for key, item in value.items()
        if key not in {"outgoing_cell", "target_chart"}
    }


def shadow_cell(active_factor: str, inactive_sign: str) -> str:
    active_sign = OPPOSITE[inactive_sign]
    signs = (
        (active_sign, inactive_sign)
        if active_factor == "HPLUS"
        else (inactive_sign, active_sign)
    )
    need(signs in SIGN_CELL, "shadow cell sign pair")
    return SIGN_CELL[signs]


def probe_sheet_r211(
    leaf: dict[str, Any], owner: dict[str, Any], shadow: dict[str, Any],
) -> tuple[dict[str, Any], str, str]:
    inactive = owner["inactive_factor"]
    need(inactive == shadow["inactive_factor"] and inactive in {"HPLUS", "HMINUS"},
         "R211 common inactive factor")
    active = "HMINUS" if inactive == "HPLUS" else "HPLUS"
    need(owner["whole_box_factor_C0"] == shadow["whole_box_factor_C0"],
         "R211 C0 equality")
    c0 = owner["whole_box_factor_C0"][inactive]
    inactive_sign = c0["selected_sign"]
    need(inactive_sign in STRICT, "R211 strict inactive sign")
    if c0["direct_sign"] == inactive_sign:
        c0_proof = "DIRECT_WHOLE_BOX_C0"
    else:
        need(c0["centered_sign"] == inactive_sign, "R211 centered C0")
        c0_proof = "CENTERED_WHOLE_BOX_C0"
    owner_cell = "E" if inactive_sign == "STRICT_POSITIVE" else "W"
    excluded_cell = shadow_cell(active, inactive_sign)
    need(
        owner["outgoing_cell"] == owner_cell
        and shadow["outgoing_cell"] == excluded_cell
        and (owner["HPLUS_sign"], owner["HMINUS_sign"])
        == CELL_SIGNS[owner_cell]
        and (shadow["HPLUS_sign"], shadow["HMINUS_sign"])
        == CELL_SIGNS[excluded_cell],
        "R211 factor-derived cells",
    )
    owner_active = owner[active + "_sign"]
    owner_inactive = owner[inactive + "_sign"]
    shadow_active = shadow[active + "_sign"]
    shadow_inactive = shadow[inactive + "_sign"]
    need(
        owner_active == owner_inactive == inactive_sign
        and shadow_inactive == inactive_sign
        and shadow_active == OPPOSITE[inactive_sign],
        "R211 factor side derivation",
    )
    owner_signature = owner["local_return_signature"]
    shadow_signature = shadow["local_return_signature"]
    owner_prefix = owner_signature["target_lift"].split("[", 1)[0]
    shadow_prefix = shadow_signature["target_lift"].split("[", 1)[0]
    core = signature_core(owner_signature)
    need(
        core == signature_core(shadow_signature)
        and owner_signature["target_chart"] == f"{owner_prefix}:{owner_cell}"
        and shadow_signature["target_chart"] == f"{shadow_prefix}:{excluded_cell}",
        "R211 signature pair",
    )
    core_hash = digest(core)
    relation = (
        "HMINUS=2*Nx_ON_HPLUS_ZERO_SHEET"
        if active == "HPLUS"
        else "HPLUS=2*Nx_ON_HMINUS_ZERO_SHEET"
    )
    identity = {
        "leaf_row_id": leaf["leaf_row_id"],
        "owner_region_row_id": owner["region_row_id"],
        "shadow_region_row_id": shadow["region_row_id"],
        "rule": "E_OR_W_OWNS__N_OR_S_SHADOWS",
    }
    probe_id = "round209-half-open-sheet:" + digest(identity)
    body = {
        "sheet_row_id": probe_id,
        "leaf_row_id": leaf["leaf_row_id"],
        "origin_row_id": leaf["origin_row_id"],
        "occurrence_row_id": leaf["occurrence_row_id"],
        "retained_child_row_id": leaf["retained_child_row_id"],
        "leaf_classification": leaf["final_graph_classification"],
        "active_factor": active,
        "inactive_factor": inactive,
        "inactive_factor_whole_box_C0_proof": c0_proof,
        "inactive_factor_whole_box_strict_sign": inactive_sign,
        "factor_identity_on_sheet": relation,
        "Nx_sign_on_sheet": inactive_sign,
        "owner_region_row_id": owner["region_row_id"],
        "shadow_region_row_id": shadow["region_row_id"],
        "owner_outgoing_cell": owner_cell,
        "shadow_outgoing_cell": excluded_cell,
        "owner_signature_core_sha256": core_hash,
        "shadow_signature_core_sha256": core_hash,
        "signature_difference_field_allowlist": ["outgoing_cell", "target_chart"],
        "Round173_half_open_rule": "E or W owns; N or S excludes",
        "deterministic_unique_owner_lineage": True,
        "incidence_is_not_a_global_component": True,
        "formal_half_open_owner_credit": 0,
        "whole_original_tube_credit": 0,
        "global_exact_key_disposition_credit": 0,
    }
    probe = {**body, "row_sha256": digest(body)}
    formal_id = "round211-half-open-sheet-owner:" + digest({
        "probe_id": probe_id, "probe_row_sha256": probe["row_sha256"],
    })
    return probe, formal_id, relation


def load_theorem_bindings() -> tuple[
    dict[str, dict[str, Any]], dict[str, dict[str, Any]],
    dict[str, dict[str, Any]], dict[str, dict[str, Any]],
]:
    c21a: dict[str, dict[str, Any]] = {}
    kinds_a: Counter[str] = Counter()
    for row in checked_rows(C21A):
        kinds_a[row["obligation_kind"]] += 1
        if row["obligation_kind"] == "A1_R204_TARGET_SHEET":
            need(row["feature_row_id"] not in c21a, "unique C21A A1")
            c21a[row["feature_row_id"]] = row
    need(kinds_a == {
        "A1_R204_TARGET_SHEET": 224,
        "A2_R204_SOURCE_TARGET_CURVE": 504,
        "A2_R204_SOURCE_TARGET_ENDPOINT": 280,
    }, "C21A census")

    c21b: dict[str, dict[str, Any]] = {}
    for row in checked_rows(C21B):
        need(row["R211_sheet_row_id"] not in c21b, "unique C21B sheet")
        c21b[row["R211_sheet_row_id"]] = row
    need(len(c21b) == 17_716, "C21B census")

    c21c: dict[str, dict[str, Any]] = {}
    kinds_c: Counter[str] = Counter()
    for row in checked_rows(C21C):
        kinds_c[row["obligation_kind"]] += 1
        if row["obligation_kind"] == "A1_R211_OWNER_SHEET":
            need(row["feature_row_id"] not in c21c, "unique C21C A1")
            c21c[row["feature_row_id"]] = row
    need(kinds_c == {
        "A1_R211_OWNER_SHEET": 17_716,
        "A2_R211_OWNER_CURVE": 20_456,
        "A2_R211_OWNER_ENDPOINT": 40_912,
    }, "C21C census")

    c26: dict[str, dict[str, Any]] = {}
    node_census: Counter[str] = Counter()
    for ordinal, row in enumerate(checked_rows(C26)):
        need(row["feature_ordinal"] == ordinal, "C26 ordinal")
        node_census[row["node_id"]] += 1
        if row["node_id"] == "A1":
            need(row["feature_id"] not in c26, "unique C26 A1")
            c26[row["feature_id"]] = row
    need(node_census == {
        "A1": 17_940, "A2": 62_152, "G1": 5_264,
        "G2A": 5_264, "G2B": 10_128, "R1": 295_340,
        "R2": 295_336,
    }, "C26 census")
    return c21a, c21b, c21c, c26


def derive_r204(
    result: dict[str, Any], c21a: dict[str, dict[str, Any]],
    c26: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    source_regions = result["formal_local_open_3D_region_ledger"]["rows"]
    source_sheets = result["formal_2D_sheet_lineage"]["target_sheet_rows"]
    need(len(source_regions) == 736 and len(source_sheets) == 224,
         "R204 primitive census")
    for row in source_regions:
        closed(row, "R204 region closure")
    sheet_index: dict[str, dict[str, Any]] = {}
    for row in source_sheets:
        closed(row, "R204 sheet closure")
        need(row["sheet_row_id"] not in sheet_index, "unique R204 sheet")
        sheet_index[row["sheet_row_id"]] = row
    by_leaf: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in source_regions:
        if row["target_graph_sheet_incident"]:
            by_leaf[row["leaf_row_id"]].append(row)
        else:
            need(row["target_sheet_row_id"] is None, "R204 nonincident null sheet")
    need(len(by_leaf) == 224 and sum(map(len, by_leaf.values())) == 448,
         "R204 independently generated candidate universe")

    output: list[dict[str, Any]] = []
    for leaf_id, joined in by_leaf.items():
        need(len(joined) == 2, "R204 two sides per sheet")
        signs = {row["target_factor_sign"]: row for row in joined}
        need(set(signs) == {"NEGATIVE", "POSITIVE"}, "R204 opposite sides")
        positive = signs["POSITIVE"]
        negative = signs["NEGATIVE"]
        common = (
            "chart", "owner_target", "wall_axis", "integer_wall",
            "leaf_exact_box", "origin_row_id", "parent_id",
        )
        need(all(positive[key] == negative[key] for key in common),
             "R204 common primitive geometry")
        identity = [
            leaf_id, positive["chart"], positive["owner_target"],
            positive["wall_axis"], positive["integer_wall"],
            positive["leaf_exact_box"][2:],
        ]
        sheet_id = "round204-target-graph-sheet-cell:" + digest(identity)
        need(
            positive["target_sheet_row_id"] == sheet_id
            and negative["target_sheet_row_id"] == sheet_id
            and sheet_id in sheet_index,
            "R204 independently reconstructed sheet id",
        )
        source = sheet_index[sheet_id]
        need(
            source["leaf_row_id"] == leaf_id
            and source["chart"] == positive["chart"]
            and source["owner_target"] == positive["owner_target"]
            and source["base_p_s_exact_bounds"] == positive["leaf_exact_box"][2:]
            and source["leaf_t_exact_bounds"] == positive["leaf_exact_box"][:2]
            and source["target_factor_graph_axis"] == "t"
            and source["target_t_derivative_sign"] == "STRICT_POSITIVE"
            and source["half_open_owner_policy"]
            == "TARGET_FACTOR_POSITIVE_SIDE_OWNS__NEGATIVE_SIDE_IS_SHADOW",
            "R204 physical sheet theorem and convention",
        )
        # Role fields are checked only after the sign-based derivation.
        need(
            source["positive_side_region_row_id"] == positive["region_row_id"]
            and source["negative_side_region_row_id"] == negative["region_row_id"]
            and source["half_open_owner_region_row_id"] == positive["region_row_id"]
            and source["half_open_shadow_region_row_id"] == negative["region_row_id"],
            "R204 derived roles agree with source declaration",
        )
        theorem = c21a.get(sheet_id)
        need(theorem is not None, "R204 C21A theorem exists")
        need(
            theorem["owner_member_id"] == positive["region_row_id"]
            and theorem["shadow_member_id"] == negative["region_row_id"]
            and theorem["source_row_sha256"] == source["row_sha256"]
            and theorem["feature_theorem_ast"]["kind"]
            == "A1_UNIQUE_TARGET_REGULAR_GRAPH_SHEET"
            and theorem["feature_theorem_ast"]["strict_t_derivative_sign"]
            == "STRICT_POSITIVE"
            and theorem["formal_credit"] == {"A1": 1, "A2": 0},
            "R204 C21A regularity binding",
        )
        feature = c26.get(sheet_id)
        need(feature is not None, "R204 C26 A1 binding")
        need(
            feature["obligation_kind"] == "A1_R204_TARGET_SHEET"
            and feature["obligation_role"] == "INDEPENDENT_DEFINITION_ROOT"
            and feature["depends_on_node_ids"] == []
            and feature["owner_member_id"] == positive["region_row_id"]
            and feature["definition_or_dependency_theorem_ast_sha256"]
            == theorem["feature_theorem_ast_sha256"]
            and feature["source_bindings"]["source_kernel"] == "C21A"
            and feature["source_bindings"]["source_row_sha256"]
            == theorem["row_sha256"],
            "R204 C26 exact owner root",
        )
        output.append({
            "physical_sheet_id": sheet_id,
            "source_class": "R204",
            "mechanism": "R204_TARGET_REGULAR_GRAPH_SHEET",
            "coordinate_chart": source["chart"],
            "exact_ambient_box": positive["leaf_exact_box"],
            "equation_kind": "TARGET_FACTOR_MINUS_INTEGER_WALL_EQUALS_ZERO",
            "equation_parameter": {
                "target": source["owner_target"],
                "wall_axis": source["wall_axis"],
                "integer_wall": source["integer_wall"],
            },
            "owner_member_id": positive["region_row_id"],
            "shadow_member_id": negative["region_row_id"],
            "owner_open_side": "TARGET_FACTOR_STRICT_POSITIVE",
            "shadow_open_side": "TARGET_FACTOR_STRICT_NEGATIVE",
            "sheet_inclusion_rule": "POSITIVE_OPEN_SIDE_PLUS_EQUALITY_SHEET_OWNS",
            "primitive_sheet_row_sha256": source["row_sha256"],
            "primitive_owner_region_row_sha256": positive["row_sha256"],
            "primitive_shadow_region_row_sha256": negative["row_sha256"],
            "A1_theorem_row_sha256": theorem["row_sha256"],
            "A1_theorem_ast_sha256": theorem["feature_theorem_ast_sha256"],
            "C26_owner_root_row_sha256": feature["row_sha256"],
        })
    need(set(sheet_index) == {row["physical_sheet_id"] for row in output},
         "R204 no orphan primitive sheet")
    return output


def derive_r211(
    result: dict[str, Any], c21b: dict[str, dict[str, Any]],
    c21c: dict[str, dict[str, Any]], c26: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    leaves = result["formal_leaf_geometry_ledger"]["rows"]
    regions = result["formal_local_open_3D_signature_ledger"]["rows"]
    need(len(leaves) == 18_324 and len(regions) == 36_040,
         "R208 primitive census")
    leaf_index: dict[str, dict[str, Any]] = {}
    for row in leaves:
        closed(row, "R208 leaf closure")
        need(row["leaf_row_id"] not in leaf_index, "unique R208 leaf")
        leaf_index[row["leaf_row_id"]] = row
    by_leaf: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in regions:
        closed(row, "R208 region closure")
        by_leaf[row["leaf_row_id"]].append(row)
    need(set(by_leaf) == set(leaf_index), "R208 complete leaf-region join")

    output: list[dict[str, Any]] = []
    empty_count = 0
    for leaf_id, leaf in leaf_index.items():
        joined = by_leaf[leaf_id]
        classification = leaf["final_graph_classification"]
        if classification == "EMPTY":
            empty_count += 1
            need(
                len(joined) == 1
                and leaf["two_dimensional_graph_sheet_count"] == 0
                and leaf["side_specific_signature_candidate_region_count"] == 1,
                "R208 empty leaf exclusion",
            )
            continue
        need(
            classification in {"CLIPPED_2D_BOUNDARY_1D", "FULL_2D"}
            and len(joined) == 2
            and leaf["two_dimensional_graph_sheet_count"] == 1
            and leaf["side_specific_signature_candidate_region_count"] == 2
            and leaf["candidate_region_signs"]
            == ["STRICT_NEGATIVE", "STRICT_POSITIVE"],
            "R208 nonempty sheet candidate",
        )
        owner_rows = [row for row in joined if row["outgoing_cell"] in {"E", "W"}]
        shadow_rows = [row for row in joined if row["outgoing_cell"] in {"N", "S"}]
        need(len(owner_rows) == len(shadow_rows) == 1,
             "R208 unique owner/shadow sides")
        owner, shadow = owner_rows[0], shadow_rows[0]
        need(owner["F_sign"] == "STRICT_POSITIVE"
             and shadow["F_sign"] == "STRICT_NEGATIVE", "R208 F side signs")
        probe, sheet_id, relation = probe_sheet_r211(leaf, owner, shadow)
        theorem = c21b.get(sheet_id)
        discharge = c21c.get(sheet_id)
        feature = c26.get(sheet_id)
        need(theorem is not None and discharge is not None and feature is not None,
             "R211 theorem/discharge/C26 chain exists")
        need(
            theorem["owner_member_id"] == owner["region_row_id"]
            and theorem["shadow_member_id"] == shadow["region_row_id"]
            and theorem["theorem_ast"]["kind"]
            == "SELF_CONTAINED_REGULAR_R211_ACTIVE_FACTOR_ZERO_SHEET"
            and theorem["theorem_ast"]["exact_identity_on_active_sheet"] == relation
            and theorem["formal_credit"] == {
                "A1_obligation_discharge": 0,
                "A2_obligation_discharge": 0,
                "self_contained_sheet_theorem_materialization": 1,
            },
            "R211 independent regularity theorem",
        )
        need(
            discharge["owner_member_id"] == owner["region_row_id"]
            and discharge["source_bindings"]["C21b_sheet_theorem_row_sha256"]
            == theorem["row_sha256"]
            and discharge["theorem_ast"]["kind"]
            == "A1_R211_REGULAR_ACTIVE_FACTOR_ZERO_SHEET_DISCHARGE"
            and discharge["formal_credit"] == {"A1": 1, "A2": 0},
            "R211 A1 discharge binding",
        )
        need(
            feature["obligation_kind"] == "A1_R211_OWNER_SHEET"
            and feature["obligation_role"] == "INDEPENDENT_DEFINITION_ROOT"
            and feature["depends_on_node_ids"] == []
            and feature["owner_member_id"] == owner["region_row_id"]
            and feature["definition_or_dependency_theorem_ast_sha256"]
            == discharge["theorem_ast_sha256"]
            and feature["source_bindings"]["source_kernel"] == "C21C"
            and feature["source_bindings"]["source_row_sha256"]
            == discharge["row_sha256"],
            "R211 C26 exact owner root",
        )
        output.append({
            "physical_sheet_id": sheet_id,
            "source_class": "R211",
            "mechanism": "R211_ACTIVE_FACTOR_ZERO_SHEET",
            "coordinate_chart": owner["local_return_signature"]["source_chart"],
            "exact_ambient_box": leaf["box"],
            "equation_kind": "ACTIVE_FACTOR_EQUALS_ZERO",
            "equation_parameter": {
                "active_factor": probe["active_factor"],
                "inactive_factor": probe["inactive_factor"],
                "inactive_factor_strict_sign": probe["inactive_factor_whole_box_strict_sign"],
                "factor_identity_on_sheet": relation,
            },
            "owner_member_id": owner["region_row_id"],
            "shadow_member_id": shadow["region_row_id"],
            "owner_open_side": "OUTGOING_CELL_IN_E_OR_W",
            "shadow_open_side": "OUTGOING_CELL_IN_N_OR_S",
            "sheet_inclusion_rule": "E_OR_W_OPEN_SIDE_PLUS_EQUALITY_SHEET_OWNS",
            "primitive_sheet_row_sha256": probe["row_sha256"],
            "primitive_owner_region_row_sha256": owner["row_sha256"],
            "primitive_shadow_region_row_sha256": shadow["row_sha256"],
            "A1_theorem_row_sha256": discharge["row_sha256"],
            "A1_theorem_ast_sha256": discharge["theorem_ast_sha256"],
            "C21B_regular_sheet_row_sha256": theorem["row_sha256"],
            "C26_owner_root_row_sha256": feature["row_sha256"],
        })
    need(empty_count == 608 and len(output) == 17_716,
         "R211 independently generated candidate universe")
    need(set(c21b) == set(c21c) == {row["physical_sheet_id"] for row in output},
         "R211 no missing/orphan theorem sheet")
    return output


def bind_current_supports(sheets: list[dict[str, Any]]) -> None:
    role_ids = {
        value for sheet in sheets
        for value in (sheet["owner_member_id"], sheet["shadow_member_id"])
    }
    need(len(role_ids) == 35_880, "distinct primitive sheet-side member universe")
    expected_region_sha = {
        sheet["owner_member_id"]: sheet["primitive_owner_region_row_sha256"]
        for sheet in sheets
    }
    expected_region_sha.update({
        sheet["shadow_member_id"]: sheet["primitive_shadow_region_row_sha256"]
        for sheet in sheets
    })
    expected_geometry = {}
    for sheet in sheets:
        for member in (sheet["owner_member_id"], sheet["shadow_member_id"]):
            expected_geometry[member] = (
                sheet["coordinate_chart"], sheet["exact_ambient_box"],
                "ROUND204_REGION" if sheet["source_class"] == "R204"
                else "ROUND208_REGION",
            )

    c15: dict[str, dict[str, Any]] = {}
    for ordinal, row in enumerate(checked_rows(C15)):
        need(row["member_ordinal"] == ordinal, "C15 ordinal")
        member = row["registry_member_id"]
        if member in role_ids:
            c15[member] = row
    need(len(c15) == len(role_ids), "all role members in current C15")

    c20: dict[str, dict[str, Any]] = {}
    for row in checked_rows(C20):
        member = row["member_id"]
        if member not in role_ids:
            continue
        chart, bounds, family = expected_geometry[member]
        need(
            row["fine_family"] == family
            and row["construction_certificate"]["source_row_sha256"]
            == expected_region_sha[member]
            and row["support_ast"] == {
                "bounds": bounds,
                "coordinate_chart": chart,
                "coordinates": ["t", "p", "s"],
                "exact_volume": row["support_ast"]["exact_volume"],
                "kind": "OPEN_RATIONAL_BOX",
            }
            and row["fresh_component_id"] == c15[member]["fresh_component_id"],
            "primitive region to C20 exact open support",
        )
        need(member not in c20, "unique C20 role member")
        c20[member] = row
    need(len(c20) == len(role_ids), "all role members in C20")

    c25: dict[str, dict[str, Any]] = {}
    for row in checked_rows(C25):
        member = row["member_id"]
        if member not in role_ids:
            continue
        need(
            row["support_semantic_kind"] == "EXACT_MEMBER_SUPPORT_EQUALITY"
            and row["normalized_support_ast_sha256"] == c20[member]["support_ast_sha256"]
            and row["fresh_component_id"] == c15[member]["fresh_component_id"]
            and row["source_bindings"]["C15_member_row_sha256"] == c15[member]["row_sha256"]
            and row["source_bindings"]["support_kernel"] == "C20A"
            and row["source_bindings"]["support_kernel_row_sha256"]
            == c20[member]["row_sha256"],
            "C25 exact current support semantics",
        )
        need(member not in c25, "unique C25 role member")
        c25[member] = row
    need(len(c25) == len(role_ids), "all role members in C25")

    for sheet in sheets:
        owner = sheet["owner_member_id"]
        shadow = sheet["shadow_member_id"]
        need(owner != shadow, "owner/shadow disjoint members")
        need(c15[owner]["fresh_component_id"] == c15[shadow]["fresh_component_id"],
             "current C15 component handoff")
        sheet["fresh_component_id"] = c15[owner]["fresh_component_id"]
        sheet["owner_C15_row_sha256"] = c15[owner]["row_sha256"]
        sheet["shadow_C15_row_sha256"] = c15[shadow]["row_sha256"]
        sheet["owner_C25_row_sha256"] = c25[owner]["row_sha256"]
        sheet["shadow_C25_row_sha256"] = c25[shadow]["row_sha256"]
        sheet["owner_support_ast_sha256"] = c20[owner]["support_ast_sha256"]
        sheet["shadow_support_ast_sha256"] = c20[shadow]["support_ast_sha256"]


def materialize(sheets: Iterable[dict[str, Any]]) -> tuple[
    list[dict[str, Any]], list[dict[str, Any]],
]:
    roles: list[dict[str, Any]] = []
    shadows: list[dict[str, Any]] = []
    for sheet in sheets:
        shadow_body = {
            "schema": "cm2.c27.independent-sheet-shadow-companion.v1.row.v1",
            "physical_sheet_id": sheet["physical_sheet_id"],
            "source_class": sheet["source_class"],
            "mechanism": sheet["mechanism"],
            "shadow_member_id": sheet["shadow_member_id"],
            "owner_member_id": sheet["owner_member_id"],
            "fresh_component_id": sheet["fresh_component_id"],
            "shadow_open_side": sheet["shadow_open_side"],
            "equality_sheet_included": False,
            "exclusion_reason": "HALF_OPEN_EQUALITY_SHEET_ASSIGNED_TO_UNIQUE_OWNER_SIDE",
            "primitive_sheet_row_sha256": sheet["primitive_sheet_row_sha256"],
            "primitive_shadow_region_row_sha256": sheet["primitive_shadow_region_row_sha256"],
            "shadow_C15_row_sha256": sheet["shadow_C15_row_sha256"],
            "shadow_C25_row_sha256": sheet["shadow_C25_row_sha256"],
            "C26_owner_root_row_sha256": sheet["C26_owner_root_row_sha256"],
            "C26_shadow_node_was_absent_and_not_used_as_authority": True,
            "formal_credit": 0,
        }
        shadow_id = "cm2-c27-independent-shadow-companion:" + digest(shadow_body)
        shadow_row = {
            **shadow_body, "materialized_shadow_node_id": shadow_id,
        }
        shadow_row["row_sha256"] = digest(shadow_row)
        shadows.append(shadow_row)

        common = {
            "schema": "cm2.c27.sheet-owner-shadow-physical-totality.v1.row.v1",
            "physical_sheet_id": sheet["physical_sheet_id"],
            "source_class": sheet["source_class"],
            "mechanism": sheet["mechanism"],
            "coordinate_chart": sheet["coordinate_chart"],
            "exact_ambient_box": sheet["exact_ambient_box"],
            "equation_kind": sheet["equation_kind"],
            "equation_parameter": sheet["equation_parameter"],
            "sheet_inclusion_rule": sheet["sheet_inclusion_rule"],
            "owner_member_id": sheet["owner_member_id"],
            "shadow_member_id": sheet["shadow_member_id"],
            "fresh_component_id": sheet["fresh_component_id"],
            "primitive_sheet_row_sha256": sheet["primitive_sheet_row_sha256"],
            "A1_theorem_row_sha256": sheet["A1_theorem_row_sha256"],
            "A1_theorem_ast_sha256": sheet["A1_theorem_ast_sha256"],
            "C26_owner_root_row_sha256": sheet["C26_owner_root_row_sha256"],
            "owner_C15_row_sha256": sheet["owner_C15_row_sha256"],
            "shadow_C15_row_sha256": sheet["shadow_C15_row_sha256"],
            "owner_C25_row_sha256": sheet["owner_C25_row_sha256"],
            "shadow_C25_row_sha256": sheet["shadow_C25_row_sha256"],
            "materialized_shadow_node_id": shadow_id,
            "materialized_shadow_node_row_sha256": shadow_row["row_sha256"],
            "formal_credit": 0,
        }
        for role in ("OWNER", "SHADOW"):
            owner = role == "OWNER"
            body = {
                **common,
                "terminal": "SHEET_OWNER" if owner else "SHEET_SHADOW",
                "role": role,
                "assigned_member_id": (
                    sheet["owner_member_id"] if owner else sheet["shadow_member_id"]
                ),
                "open_side_predicate": (
                    sheet["owner_open_side"] if owner else sheet["shadow_open_side"]
                ),
                "equality_sheet_included": owner,
                "terminal_disposition": (
                    "UNIQUE_HALF_OPEN_SHEET_OWNER"
                    if owner else "UNIQUE_ADJACENT_SHADOW_EXCLUDED_FROM_EQUALITY_SHEET"
                ),
            }
            body["row_sha256"] = digest(body)
            roles.append(body)
    roles.sort(key=lambda row: (row["physical_sheet_id"].encode(), row["role"].encode()))
    shadows.sort(key=lambda row: row["physical_sheet_id"].encode())
    roles = [
        {**{key: value for key, value in row.items() if key != "row_sha256"},
         "ordinal": ordinal}
        for ordinal, row in enumerate(roles)
    ]
    roles = [{**row, "row_sha256": digest(row)} for row in roles]
    shadows = [
        {**{key: value for key, value in row.items() if key != "row_sha256"},
         "ordinal": ordinal}
        for ordinal, row in enumerate(shadows)
    ]
    shadows = [{**row, "row_sha256": digest(row)} for row in shadows]
    return roles, shadows


def write_gzip_rows(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    raw = b"".join(canonical(row) + b"\n" for row in rows)
    with path.open("wb") as output:
        with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as zipped:
            zipped.write(raw)
    return {
        "filename": path.name,
        "row_count": len(rows),
        "sha256": file_hash(path),
        "uncompressed_sha256": hashlib.sha256(raw).hexdigest(),
        "ordered_row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=30627401)
    parser.add_argument("--output-dir", required=True)
    arguments = parser.parse_args()
    need(arguments.seed >= 0, "nonnegative declared seed")
    output_dir = Path(arguments.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    observed = {name: file_hash(ROOT / name) for name in sorted(PINS)}
    need(observed == {name: PINS[name] for name in sorted(PINS)},
         "exact primitive input pins")
    r173 = envelope(R173)
    rule = r173["outgoing_chart_contract"]
    need(
        rule["diagonal_seam_rule"] == "E or W owns; N or S excludes"
        and rule["owner_set"] == ["E", "W"]
        and rule["strict_chart_transport_is_total_on_E_W_N_S"] is True,
        "R173 half-open physical convention",
    )
    c21a, c21b, c21c, c26 = load_theorem_bindings()
    sheets = derive_r204(envelope(R204), c21a, c26)
    sheets.extend(derive_r211(envelope(R208), c21b, c21c, c26))
    need(len(sheets) == 17_940
         and len({row["physical_sheet_id"] for row in sheets}) == 17_940,
         "combined primitive sheet universe")
    rng = random.Random(arguments.seed)
    rng.shuffle(sheets)
    bind_current_supports(sheets)
    roles, shadows = materialize(sheets)
    need(len(roles) == 35_880 and len(shadows) == 17_940,
         "materialized role and shadow universes")

    per_sheet: Counter[str] = Counter(row["physical_sheet_id"] for row in roles)
    per_terminal: Counter[str] = Counter(row["terminal"] for row in roles)
    source_census: Counter[str] = Counter(row["source_class"] for row in shadows)
    include_census: Counter[bool] = Counter(row["equality_sheet_included"] for row in roles)
    need(set(per_sheet.values()) == {2}, "exactly two terminal roles per sheet")
    need(per_terminal == {"SHEET_OWNER": 17_940, "SHEET_SHADOW": 17_940},
         "terminal census")
    need(source_census == {"R204": 224, "R211": 17_716}, "source census")
    need(include_census == {True: 17_940, False: 17_940},
         "unique inclusion/exclusion census")

    role_desc = write_gzip_rows(
        output_dir / "sheet_owner_shadow_terminal_ledger.jsonl.gz", roles,
    )
    shadow_desc = write_gzip_rows(
        output_dir / "materialized_shadow_companion_ledger.jsonl.gz", shadows,
    )
    candidate_projection = [
        {
            "physical_sheet_id": row["physical_sheet_id"],
            "terminal": row["terminal"],
            "assigned_member_id": row["assigned_member_id"],
            "fresh_component_id": row["fresh_component_id"],
            "equality_sheet_included": row["equality_sheet_included"],
            "materialized_shadow_node_id": row["materialized_shadow_node_id"],
        }
        for row in roles
    ]
    semantic_projection = {
        "schema": "cm2.c27.sheet-owner-shadow-physical-totality.zero-credit.v1",
        "status": "PASS_LOCAL_ZERO_CREDIT__SHEET_OWNER_AND_SHEET_SHADOW_PHYSICAL_TOTALITY_FROM_PRIMITIVE_HALF_OPEN_GEOMETRY",
        "implementation": "STREAMED_PRIMITIVE_GEOMETRY_RECONSTRUCTION",
        "C27_source_or_FAMILIES_imported_or_read": False,
        "edge_ledger_used_as_candidate_universe": False,
        "primitive_candidate_generation": {
            "R204_target_factor_sign_partition": 224,
            "R211_factor_sign_and_outgoing_chart_partition": 17_716,
            "total_physical_sheets": 17_940,
        },
        "terminal_census": dict(sorted(per_terminal.items())),
        "candidate_role_row_count": len(roles),
        "candidate_projection_sha256": digest(candidate_projection),
        "role_ledger": role_desc,
        "C26_explicit_shadow_node_present": False,
        "independent_materialized_shadow_companion_count": len(shadows),
        "shadow_companion_ledger": shadow_desc,
        "owner_shadow_mutually_exclusive_per_sheet": True,
        "unique_owner_and_unique_shadow_per_sheet": True,
        "all_primitive_sheets_covered": True,
        "unresolved": 0,
        "orphan_or_duplicate": 0,
        "legal_cross_component_witness": 0,
        "current_C15_same_component_handoff_count": 17_940,
        "half_open_side_inclusion_independently_derived": True,
        "terminal_physical_totality": "PASS_LOCAL_ZERO_CREDIT",
        "input_sha256": observed,
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_PENDING_ALL_20_TERMINAL_GATE",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = {
        **semantic_projection,
        "declared_seed": arguments.seed,
        "declared_seed_semantically_used_before_canonical_sort": True,
        "invocation": {
            "command_argv": [
                sys.executable, "-I", "-B", str(Path(__file__).resolve()),
                "--seed", str(arguments.seed),
                "--output-dir", str(output_dir),
            ],
            "isolated_runtime": True,
            "dont_write_bytecode": True,
        },
        "semantic_projection_sha256": digest(semantic_projection),
    }
    result_with_hash = {**result, "result_sha256": digest(result)}
    result_path = output_dir / "result.json"
    result_path.write_bytes(canonical(result_with_hash) + b"\n")
    print(canonical(result_with_hash).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        Failure, OSError, KeyError, TypeError, ValueError,
        json.JSONDecodeError,
    ) as error:
        print("REJECT_SHEET_OWNER_SHADOW_PHYSICAL_TOTALITY:" + str(error),
              file=sys.stderr)
        raise SystemExit(2)
