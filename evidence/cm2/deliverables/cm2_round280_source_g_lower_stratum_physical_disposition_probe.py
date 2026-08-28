#!/usr/bin/env python3
"""Fail-closed physical-disposition audit of the 55,428 Round267 nominal supports.

This is a ZERO-CREDIT probe.  It classifies the already frozen local
existence/absence evidence without creating an expanded occurrence,
component edge, maximality assignment, exact-key-fibre disposition, or
Jx/Jy same-point identification.

The four output states are intentionally distinct:

* ``CERTIFIED_PHYSICAL_SUPPORT_EXISTS``: an upstream frozen artifact contains
  an explicit graph sheet or transverse intersection witness;
* ``CERTIFIED_SUPPORT_ABSENT``: an upstream frozen artifact exhausts the
  relevant local collar/pair domain by strict emptiness;
* ``FORMAL_PROVENANCE_ONLY__NO_PHYSICAL_DECISION``: Round179 completely
  replaced the positive-volume origin before Round182 built a collar, so the
  frozen lineage is real but absence is not inferred from a missing collar;
* ``UNRESOLVED__SOURCE_T0_HALF_OPEN_OWNER_NOT_MATERIALIZED``: the source
  factor is the exact t=0 boundary graph, but no frozen half-open physical
  owner ledger exists for that boundary support.

The Round268 seam patches, Round275 reverse-rechart guards, and Round279
collar atoms are audited as non-dispositive side inputs.  In particular,
Round279 candidate atoms are not promoted to lower-stratum existence.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gc
import gzip
import hashlib
import io
import json
from pathlib import Path
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round280_source_g_lower_stratum_physical_disposition_probe"
DEFAULT_LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
DEFAULT_RESULT = HERE / f"{PREFIX}_result.json"
SCHEMA = "cm2.round280.source-g-lower-stratum-physical-disposition-probe.v1"
LEDGER_SCHEMA = "cm2.round280.source-g-lower-stratum-physical-disposition-ledger.v1"

INPUT_SHA256 = {
    "cm2_round267_source_g_lower_stratum_terminal_lineage_certificate.json":
        "66879215e0250a4a462fea9837c24bccf49a936ce3c5e66da2707e1a66fafc8f",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json":
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json":
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json":
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_certificate.json":
        "10d5e42f4353e981e7e8d5aacc002bed119453ee14a13398c524d5cb4ac2f7b9",
    "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json":
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_certificate.json":
        "ef60a40cc05d47b3d899b73169017bee8e246583ce51a5b543f1b1a1047f064e",
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz":
        "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
}

PHYSICAL = "CERTIFIED_PHYSICAL_SUPPORT_EXISTS"
ABSENT = "CERTIFIED_SUPPORT_ABSENT"
PROVENANCE = "FORMAL_PROVENANCE_ONLY__NO_PHYSICAL_DECISION"
UNRESOLVED = "UNRESOLVED__SOURCE_T0_HALF_OPEN_OWNER_NOT_MATERIALIZED"


class ProbeError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ProbeError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            state.update(chunk)
    return state.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        value = json.load(stream)
    need(isinstance(value, dict), f"object input:{path.name}")
    return value


def closed(row: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in row, "row already closed")
    output = dict(row)
    output["row_sha256"] = digest(output)
    return output


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = result["row_column_schemas"][table]
    rows = result[table]
    need(all(len(row) == len(columns) for row in rows), f"packed width:{table}")
    return [dict(zip(columns, row)) for row in rows]


def write_atomic(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="wb", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
    temporary.replace(path)


def gzip_payload(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, mtime=0) as stream:
        stream.write(canonical(value))
    return buffer.getvalue()


def make_row_id(lineage_row_id: str, support_row_id: str) -> str:
    return "round280-lower-support-disposition:" + hashlib.sha256(
        canonical([lineage_row_id, support_row_id])
    ).hexdigest()


def zero_credit() -> dict[str, int]:
    return {
        "expanded_occurrence_credit": 0,
        "component_edge_credit": 0,
        "maximality_credit": 0,
        "exact_key_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
        "Jx_Jy_same_point_glue_credit": 0,
    }


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    for filename, expected in INPUT_SHA256.items():
        need(file_sha256(HERE / filename) == expected, f"pinned input:{filename}")

    round267 = read_json(
        HERE / "cm2_round267_source_g_lower_stratum_terminal_lineage_certificate.json"
    )
    lineage_rows = round267["result"][
        "formal_Round174_lower_stratum_terminal_lineage_ledger"
    ]["rows"]
    nominal = [row for row in lineage_rows if row["nominal_support_only"]]
    need(len(nominal) == 55_428, "Round267 nominal count")
    need(
        len({row["lower_stratum_terminal_lineage_row_id"] for row in nominal})
        == len(nominal),
        "unique Round267 lineage ids",
    )
    nominal_by_support = {
        row["canonical_support_or_absence_row_id"]: row for row in nominal
    }
    need(len(nominal_by_support) == len(nominal), "unique nominal support ids")
    del round267, lineage_rows
    gc.collect()

    round179 = read_json(
        HERE / "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )["result"]
    wall_by_id = {
        row["row_id"]: row for row in unpack(round179, "wall_normal_form_rows")
    }
    origin_by_id = {
        row["origin_row_id"]: row for row in unpack(round179, "origin_tube_rows")
    }
    del round179
    gc.collect()

    round182 = read_json(
        HERE / "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
    )["result"]
    collars = unpack(round182, "collar_occurrence_rows")
    pairs = unpack(round182, "pair_intersection_rows")
    del round182
    gc.collect()

    decisions: dict[str, dict[str, Any]] = {}
    provisional_outgoing: set[str] = set()
    provisional_wall: set[str] = set()

    for collar in collars:
        support_id = collar["Round179_occurrence_row_id"]
        if support_id not in nominal_by_support:
            continue
        lineage = nominal_by_support[support_id]
        if collar["Round179_origin_already_fully_replaced"]:
            state = PROVENANCE
            basis = "ROUND179_FULL_REPLACEMENT__ROUND182_HAS_NO_RETAINED_COLLAR"
        elif collar["two_dimensional_graph_sheet_count"] > 0:
            state = PHYSICAL
            basis = "ROUND182_EXPLICIT_FULL_OR_CLIPPED_2D_GRAPH_SHEET"
        elif collar["residual_leaf_count"] > 0:
            if collar["kind"] == "OUTGOING":
                provisional_outgoing.add(support_id)
            else:
                need(collar["kind"] == "WALL", "known collar kind")
                provisional_wall.add(support_id)
            continue
        else:
            need(collar["closed_leaf_count"] > 0, "nonempty closed collar")
            need(
                collar["absent_graph_leaf_count"] == collar["closed_leaf_count"],
                "exhaustive empty collar",
            )
            state = ABSENT
            basis = "ROUND182_EXHAUSTIVE_CLOSED_COLLAR_ALL_GRAPH_LEAVES_EMPTY"
        decisions[support_id] = {
            "physical_disposition": state,
            "evidence_basis": basis,
            "evidence_row_ids": [collar["row_id"]],
            "evidence_census": {
                "closed_leaf_count": collar["closed_leaf_count"],
                "residual_leaf_count": collar["residual_leaf_count"],
                "two_dimensional_graph_sheet_count":
                    collar["two_dimensional_graph_sheet_count"],
                "absent_graph_leaf_count": collar["absent_graph_leaf_count"],
            },
        }

    need(len(provisional_outgoing) == 56, "Round182 outgoing no-graph residual")
    need(len(provisional_wall) == 32, "Round182 wall no-graph residual")

    nominal_pair_count = 0
    for pair in pairs:
        support_id = pair["Round179_pair_row_id"]
        if support_id not in nominal_by_support:
            continue
        nominal_pair_count += 1
        classification = pair["existence_classification"]
        if classification == (
            "UNIQUE_TRANSVERSE_1D_INTERSECTION_LINE__"
            "P_BRACKET_AND_INTERVAL_NEWTON"
        ):
            state = PHYSICAL
            basis = "ROUND182_STRICT_INTERIOR_INTERVAL_NEWTON_TRANSVERSE_1D_LINE"
        else:
            need(
                classification == "EMPTY__STRICT_SAME_SIGN_P_FACES",
                "nominal pair has supported empty taxonomy",
            )
            state = ABSENT
            basis = "ROUND182_PAIR_STRICT_SAME_SIGN_P_FACES"
        decisions[support_id] = {
            "physical_disposition": state,
            "evidence_basis": basis,
            "evidence_row_ids": [pair["row_id"]],
            "evidence_census": {
                "existence_classification": classification,
                "actual_1D_intersection_component_count":
                    pair["actual_1D_intersection_component_count"],
            },
        }
    need(nominal_pair_count == 328, "nominal pair join count")
    del collars, pairs
    gc.collect()

    round208 = read_json(
        HERE / "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
    )["result"]
    signature_rows = round208["formal_local_open_3D_signature_ledger"]["rows"]
    by_occurrence: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in signature_rows:
        if row["occurrence_row_id"] in provisional_outgoing:
            by_occurrence[row["occurrence_row_id"]].append(row)
    need(set(by_occurrence) == provisional_outgoing, "Round208 residual join")
    for support_id in sorted(provisional_outgoing):
        evidence = by_occurrence[support_id]
        physical_rows = [
            row for row in evidence if row["leaf_classification"] != "EMPTY"
        ]
        if physical_rows:
            state = PHYSICAL
            basis = "ROUND208_EXPLICIT_RESIDUAL_OUTGOING_GRAPH_SHEET_AND_SIDES"
            selected = physical_rows
        else:
            state = ABSENT
            basis = "ROUND208_EXHAUSTIVE_RESIDUAL_OUTGOING_ROWS_ALL_EMPTY"
            selected = evidence
        decisions[support_id] = {
            "physical_disposition": state,
            "evidence_basis": basis,
            "evidence_row_ids": [row["region_row_id"] for row in selected],
            "evidence_census": {
                "formal_signature_region_count": len(evidence),
                "nonempty_graph_region_count": len(physical_rows),
                "all_signature_regions_direct": all(
                    row["formal_local_open_3D_signature_credit"] == 1
                    for row in evidence
                ),
            },
        }
    del round208, signature_rows, by_occurrence
    gc.collect()

    round204 = read_json(
        HERE / "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
    )["result"]
    completion_by_origin = {
        row["origin_row_id"]: row
        for row in round204["origin_local_completion_ledger"]["rows"]
    }
    for support_id in sorted(provisional_wall):
        lineage = nominal_by_support[support_id]
        origin_id = lineage["containing_Round174_residual_row_id"]
        need(origin_id in completion_by_origin, "Round204 wall residual origin join")
        evidence = completion_by_origin[origin_id]
        need(
            evidence["source_t0_2D_sheet_cell_count"]
            + evidence["target_graph_2D_sheet_cell_count"] > 0,
            "Round204 explicit incident sheet",
        )
        decisions[support_id] = {
            "physical_disposition": PHYSICAL,
            "evidence_basis":
                "ROUND204_EXPLICIT_SOURCE_OR_TARGET_2D_SHEET_WITH_HALF_OPEN_LINEAGE",
            "evidence_row_ids": evidence["incident_2D_sheet_row_ids"],
            "evidence_census": {
                "source_t0_2D_sheet_cell_count":
                    evidence["source_t0_2D_sheet_cell_count"],
                "target_graph_2D_sheet_cell_count":
                    evidence["target_graph_2D_sheet_cell_count"],
                "Round204_fully_locally_signature_replaced":
                    evidence["Round204_fully_locally_signature_replaced"],
            },
        }
    del round204, completion_by_origin
    gc.collect()

    collar_or_pair_ids = set(decisions)
    unresolved_rows = [
        row for support_id, row in nominal_by_support.items()
        if support_id not in collar_or_pair_ids
    ]
    need(len(unresolved_rows) == 880, "source t0 unresolved count")

    unresolved_geometry: dict[
        tuple[str, str, int, tuple[str, ...]], list[tuple[str, str]]
    ] = defaultdict(list)
    for lineage in unresolved_rows:
        support_id = lineage["canonical_support_or_absence_row_id"]
        wall = wall_by_id[support_id]
        origin = origin_by_id[wall["origin_row_id"]]
        box = origin["original_box"]
        need(
            lineage["canonical_support_kind"]
            == "NOMINAL_REGULAR_FACTOR_UNION_IF_PRESENT",
            "unresolved nominal kind",
        )
        need(wall["source_factor_classification"] == "REGULAR_GRAPH",
             "unresolved source regular graph")
        need(wall["source_gradient_axis"] == "t", "source t derivative")
        need(wall["integer_wall"] == 0, "source graph only at wall zero")
        need(
            wall["target_face_classification"] == "STRICT_ZERO_ABSENT",
            "unresolved target factor absent",
        )
        need((box[0] == "0") ^ (box[1] == "0"), "one t=0 boundary face")
        side = "POSITIVE_T_SIDE" if box[0] == "0" else "NEGATIVE_T_SIDE"
        key = (wall["chart"], wall["axis"], wall["integer_wall"], tuple(box[2:]))
        unresolved_geometry[key].append((side, support_id))

    partner_by_support: dict[str, str] = {}
    for group in unresolved_geometry.values():
        sides = Counter(side for side, _ in group)
        if len(group) == 2 and sides == {
            "NEGATIVE_T_SIDE": 1,
            "POSITIVE_T_SIDE": 1,
        }:
            first, second = group
            partner_by_support[first[1]] = second[1]
            partner_by_support[second[1]] = first[1]
        else:
            need(len(group) == 1, "unresolved geometry group size")
    need(len(partner_by_support) == 176, "paired unresolved rows")

    for lineage in unresolved_rows:
        support_id = lineage["canonical_support_or_absence_row_id"]
        wall = wall_by_id[support_id]
        origin = origin_by_id[wall["origin_row_id"]]
        partner = partner_by_support.get(support_id)
        decisions[support_id] = {
            "physical_disposition": UNRESOLVED,
            "evidence_basis": (
                "ROUND179_EXACT_SOURCE_T0_BOUNDARY_GRAPH__"
                + (
                    "SAME_CHART_OPPOSITE_T_PARTNER_BUT_NO_FROZEN_OWNER"
                    if partner
                    else "ONE_SIDED_BOUNDARY_WITH_NO_FROZEN_OWNER"
                )
            ),
            "evidence_row_ids": [support_id] + ([partner] if partner else []),
            "evidence_census": {
                "original_box": origin["original_box"],
                "source_factor_classification":
                    wall["source_factor_classification"],
                "target_face_classification":
                    wall["target_face_classification"],
                "same_chart_opposite_t_partner_count": 1 if partner else 0,
            },
        }

    need(set(decisions) == set(nominal_by_support), "all nominal supports decided")

    # Non-dispositive audit of the specifically requested later pins.
    round268 = read_json(
        HERE / "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_certificate.json"
    )["result"]
    seam_rows = round268["formal_true_source_seam_positive_patch_ledger"]["rows"]
    nominal_support_ids = set(nominal_by_support)
    seam_references = set()
    for row in seam_rows:
        seam_references.add(row["left_Round182_source_seam_row_id"])
        seam_references.add(row["right_Round182_source_seam_row_id"])
        need(row["component_edge_credit"] == 0, "Round268 zero edge credit")
        need(row["Jx_Jy_same_point_glue_credit"] == 0, "Round268 zero Jx/Jy")
    need(not (seam_references & nominal_support_ids), "Round268 nominal support join")
    round268_audit = {
        "positive_patch_count": len(seam_rows),
        "direct_nominal_support_row_id_overlap_count": 0,
        "disposition_effect": "NONE__SOURCE_SEAM_PATCHES_ARE_NOT_NOMINAL_SUPPORT_ROWS",
    }
    del round268, seam_rows
    gc.collect()

    round275 = read_json(
        HERE / "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json"
    )["result"]
    guard_rows = round275["guard_closure_ledger"]["rows"]
    nominal_parents = {row["parent_id"] for row in nominal}
    guard_parent_overlap = {
        row["parent_id"] for row in guard_rows if row["parent_id"] in nominal_parents
    }
    need(all(row["occurrence_credit"] == 0 for row in guard_rows),
         "Round275 zero occurrence credit")
    need(all(row["component_credit"] == 0 for row in guard_rows),
         "Round275 zero component credit")
    round275_audit = {
        "guard_count": len(guard_rows),
        "nominal_parent_overlap_count": len(guard_parent_overlap),
        "guard_rows_on_overlapping_parents": sum(
            row["parent_id"] in nominal_parents for row in guard_rows
        ),
        "direct_nominal_support_row_id_join_count": 0,
        "disposition_effect":
            "NONE__PARENT_LEVEL_RECHART_IS_NOT_SUPPORT_EXISTENCE",
    }
    del round275, guard_rows
    gc.collect()

    with gzip.open(
        HERE / "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz",
        "rt",
        encoding="utf-8",
    ) as stream:
        round279_atoms = json.load(stream)
    atoms = round279_atoms["rows"]
    nominal_atoms = [
        row for row in atoms
        if row["Round182_occurrence_row_id"] in nominal_support_ids
    ]
    nominal_atom_occurrences = {
        row["Round182_occurrence_row_id"] for row in nominal_atoms
    }
    need(len(nominal_atoms) == 332_016, "Round279 nominal atom count")
    need(len(nominal_atom_occurrences) == 53_824,
         "Round279 nominal occurrence join")
    need(all(row["expanded_occurrence_credit"] == 0 for row in nominal_atoms),
         "Round279 zero atom occurrence credit")
    round279_audit = {
        "candidate_atom_count_joined_to_nominal_support_occurrences":
            len(nominal_atoms),
        "nominal_support_occurrence_count_touched":
            len(nominal_atom_occurrences),
        "existing_Round208_occurrence_backed_atom_count": sum(
            bool(row["existing_Round208_occurrence_row_ids"])
            for row in nominal_atoms
        ),
        "new_occurrence_region_atom_candidate_count": sum(
            row["new_occurrence_region_atom_candidate"] for row in nominal_atoms
        ),
        "disposition_effect":
            "NONE__CANDIDATE_ATOMS_DO_NOT_IMPLY_LOWER_STRATUM_EXISTENCE",
    }
    del round279_atoms, atoms, nominal_atoms
    gc.collect()

    output_rows: list[dict[str, Any]] = []
    for support_id in sorted(nominal_by_support):
        lineage = nominal_by_support[support_id]
        decision = decisions[support_id]
        row = {
            "lower_stratum_physical_disposition_row_id": make_row_id(
                lineage["lower_stratum_terminal_lineage_row_id"], support_id
            ),
            "Round267_lower_stratum_terminal_lineage_row_id":
                lineage["lower_stratum_terminal_lineage_row_id"],
            "Round174_stratum_id": lineage["Round174_stratum_id"],
            "canonical_support_row_id": support_id,
            "canonical_support_kind": lineage["canonical_support_kind"],
            "containing_Round174_residual_row_id":
                lineage["containing_Round174_residual_row_id"],
            "parent_id": lineage["parent_id"],
            "source_chart": lineage["source_chart"],
            "predicate_label": lineage["predicate_label"],
            "predicate_equation": lineage["predicate_equation"],
            "physical_disposition": decision["physical_disposition"],
            "evidence_basis": decision["evidence_basis"],
            "evidence_row_ids": decision["evidence_row_ids"],
            "evidence_census": decision["evidence_census"],
            "nominal_lineage_promoted_to_occurrence": False,
            "requires_final_DSU_to_decide_local_physical_support": False,
            **zero_credit(),
        }
        output_rows.append(closed(row))

    need(
        len({row["lower_stratum_physical_disposition_row_id"] for row in output_rows})
        == len(output_rows),
        "unique Round280 row ids",
    )
    disposition_histogram = Counter(
        row["physical_disposition"] for row in output_rows
    )
    need(
        disposition_histogram == {
            PHYSICAL: 38_440,
            ABSENT: 15_712,
            PROVENANCE: 396,
            UNRESOLVED: 880,
        },
        "four-way disposition census",
    )
    basis_histogram = Counter(row["evidence_basis"] for row in output_rows)
    support_kind_by_disposition: dict[str, Counter[str]] = defaultdict(Counter)
    for row in output_rows:
        support_kind_by_disposition[row["canonical_support_kind"]][
            row["physical_disposition"]
        ] += 1

    ledger = {
        "schema": LEDGER_SCHEMA,
        "status": "ROUND280_LOWER_STRATUM_PHYSICAL_DISPOSITION_PROBE__ZERO_CREDIT",
        "row_count": len(output_rows),
        "row_ids_sha256": digest(
            [row["lower_stratum_physical_disposition_row_id"] for row in output_rows]
        ),
        "row_hashes_sha256": digest([row["row_sha256"] for row in output_rows]),
        "rows_sha256": digest(output_rows),
        "rows": output_rows,
    }
    result = {
        "schema": SCHEMA,
        "status": "PASS_ROUND280_LOWER_STRATUM_PHYSICAL_DISPOSITION_PROBE__ZERO_CREDIT",
        "pins": INPUT_SHA256,
        "census": {
            "Round267_nominal_support_count": 55_428,
            "physical_disposition_histogram": dict(sorted(disposition_histogram.items())),
            "evidence_basis_histogram": dict(sorted(basis_histogram.items())),
            "support_kind_by_disposition": {
                kind: dict(sorted(counter.items()))
                for kind, counter in sorted(support_kind_by_disposition.items())
            },
            "same_chart_exact_opposite_t_boundary_pair_count": 88,
            "unresolved_rows_with_exact_opposite_t_partner_count": 176,
            "unresolved_one_sided_t0_boundary_row_count": 704,
            "local_physical_support_rows_requiring_final_DSU_count": 0,
            "nonterminal_local_physical_decision_count": 1_276,
        },
        "non_dispositive_later_pin_audit": {
            "Round268": round268_audit,
            "Round275": round275_audit,
            "Round279": round279_audit,
        },
        "ledger_attachment": {
            "filename": DEFAULT_LEDGER.name,
            "schema": LEDGER_SCHEMA,
            "row_count": ledger["row_count"],
            "row_ids_sha256": ledger["row_ids_sha256"],
            "row_hashes_sha256": ledger["row_hashes_sha256"],
            "rows_sha256": ledger["rows_sha256"],
        },
        "minimum_remaining_local_dependencies": {
            "396_formal_provenance_rows":
                "replay exact predicate signs over the exhaustive Round179 "
                "fully-replaced child cover; missing Round182 collars are not absence",
            "880_source_t0_boundary_rows":
                "materialize an explicit same-point half-open source-sheet owner/"
                "absence ledger; 176 rows already form 88 exact same-chart opposing "
                "boundary pairs and 704 rows remain one-sided",
            "final_DSU_dependency":
                "NONE for local physical support; DSU remains downstream and cannot "
                "decide existence",
        },
        "strict_nonpromotion": {
            **zero_credit(),
            "physical_support_classification_is_not_expanded_occurrence": True,
            "Round279_candidate_atom_is_not_support_existence": True,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    return ledger, result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--result", type=Path, default=DEFAULT_RESULT)
    parser.add_argument("--seed", default="280071")
    args = parser.parse_args()
    ledger, result = build()
    ledger_bytes = gzip_payload(ledger)
    result["ledger_attachment"]["file_sha256"] = hashlib.sha256(
        ledger_bytes
    ).hexdigest()
    result["result_sha256"] = digest(result)
    write_atomic(args.ledger, ledger_bytes)
    write_atomic(args.result, canonical(result))
    print(json.dumps({
        "status": result["status"],
        "ledger": str(args.ledger),
        "ledger_sha256": result["ledger_attachment"]["file_sha256"],
        "result": str(args.result),
        "result_sha256": result["result_sha256"],
        "census": result["census"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
