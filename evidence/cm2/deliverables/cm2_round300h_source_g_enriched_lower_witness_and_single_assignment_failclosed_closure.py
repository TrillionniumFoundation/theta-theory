#!/usr/bin/env python3
"""Round300-H: exhaust enriched lower witnesses and all single assignments.

Round300-D froze 111,524 canonical lower-incidence pairs and 1,600
single-target assignments.  This producer isolates the 144 pairs whose
witness family is not pure GRAPH, classifies all 1,600 singles, and emits
an explicit fail-closed disposition for every selected row.

No disposition in this package is a component edge.  In particular:

* a transverse analytic-boundary line has no adjacent-tube deduplication
  credit and no included-stratum two-attachment lemma;
* an exact t=0 owner-policy cover is incidence evidence, not lineage from
  the owner child/origin to a Round266 component root;
* one-target assignment cannot by itself form an unordered edge; and
* a preserved Round266 occurrence only reopens existing provenance.

The independent verifier reopens every cited source row, all relevant
geometry and lineage channels, and the complete preserved Round266
frontier.  This producer never applies a DSU or grants quotient,
maximality, fibre, or global-disposition credit.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Iterator, TextIO


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round300h_source_g_enriched_lower_witness_and_"
    "single_assignment_failclosed_closure"
)
PAIR_LEDGER = HERE / f"{PREFIX}_enriched_pair_disposition_ledger.json.gz"
SINGLE_LEDGER = HERE / f"{PREFIX}_single_target_disposition_ledger.json.gz"
EDGE_LEDGER = HERE / f"{PREFIX}_eligible_component_edge_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"

SCHEMA = (
    "cm2.round300h.source-g-enriched-lower-witness-and-"
    "single-assignment-failclosed-closure.v1"
)

FILES = {
    "R179": (
        "cm2_round179_source_g_residual_tube_arrangement_rows.json",
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    ),
    "R182": (
        "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json",
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    ),
    "R204": (
        "cm2_round204_source_g_wall_return_signature_local_replacement_"
        "certificate.json",
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    ),
    "R208": (
        "cm2_round208_source_g_outgoing_direct_signature_materialization_"
        "certificate.json",
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    ),
    "R220": (
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_"
        "certificate.json",
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    ),
    "R245": (
        "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_"
        "certificate.json",
        "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1",
    ),
    "R246": (
        "cm2_round246_source_g_whole_signature_retained_quotient_"
        "certificate.json",
        "a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9",
    ),
    "R247": (
        "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_"
        "certificate.json",
        "72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7",
    ),
    "R248": (
        "cm2_round248_source_g_wall_finite_key_retained_quotient_"
        "certificate.json",
        "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    ),
    "R266": (
        "cm2_round266_source_g_expanded_curved_face_closure_certificate.json",
        "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf",
    ),
    "R291": (
        "cm2_round291_source_g_complete_lower_stratum_local_disposition_"
        "freeze_ledger.json.gz",
        "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab",
    ),
    "R293": (
        "cm2_round293_source_g_r289_r291_witness_binding_canonical_"
        "closure_ledger.json.gz",
        "0e7395a69844734cc51563882f471987cc566db28a55ccae6e6d15d045f9e53c",
    ),
    "R295A": (
        "cm2_round295a_source_g_r291_positive_t_retained_continuation_"
        "closure_physical_witness_incidence_binding_ledger.json.gz",
        "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    ),
    "R300A": (
        "cm2_round300a_source_g_r287_graph_zero_lower_frontier_"
        "exhaustion_ledger.json.gz",
        "ddc1a8bc53861afeb93d3569c6efa228f17d86f161db31a39fa9b72458ab8f2d",
    ),
    "R300C": (
        "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_"
        "volume_edge_promotion_edge_ledger.json.gz",
        "8c9ed8b09e994a00ca3ca4906c35b454523383b7d488f66e7a082dbbd4b1fcec",
    ),
    "R300D": (
        "cm2_round300d_source_g_lower_physical_witness_component_edge_"
        "promotion_ledger.json.gz",
        "287d1382b25fd3d5cd0a52c6da8cabbb012040b8a6e35c9f887d7a425b812fa7",
    ),
    "R300D_RESULT": (
        "cm2_round300d_source_g_lower_physical_witness_component_edge_"
        "promotion_result.json",
        "59b7e788ed217ceb590a3e2125cc13aefbf447af236315ea607f4f631cb29c84",
    ),
    "R300E": (
        "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_"
        "promotion_witness_ledger.json.gz",
        "69f480da55e917b7b75bfe1efa823a9228d9b563f6f3aabd4e2a364c9e50eb9f",
    ),
    "R300F": (
        "cm2_round300f_source_g_r245_half_open_owner_sheet_attachment_"
        "ledger.json.gz",
        "1f958f9f3e3aff7327d897b39851f2d2d030d820e00859d302241702613cae1f",
    ),
}

GRAPH = "ROUND182_GRAPH_SHEET_LEAF"
TRANS = "ROUND182_TRANSVERSE_1D_LINE"
NEG = "ROUND179_NEGATIVE_T0_SHADOW_PATCH"
POS = "ROUND179_POSITIVE_T0_RETAINED_OWNER"
NEW = "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
PRESERVED = "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"


class GateError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise GateError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def canonical(value: Any) -> bytes:
    return "".join(ENCODER.iterencode(value)).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def iter_array(path: Path, marker: str) -> Iterator[Any]:
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        yield from iter_array_stream(stream, marker)


def iter_array_stream(stream: TextIO, marker: str) -> Iterator[Any]:
    token = json.dumps(marker, ensure_ascii=False) + ":["
    buffer = ""
    while token not in buffer:
        part = stream.read(1 << 20)
        need(bool(part), "missing array marker:" + marker)
        buffer += part
        if len(buffer) > len(token) + (1 << 20):
            buffer = buffer[-(len(token) + (1 << 20)) :]
    buffer = buffer.split(token, 1)[1]
    decoder = json.JSONDecoder(
        object_pairs_hook=unique_object,
        parse_float=lambda value: (_ for _ in ()).throw(
            GateError("float:" + value)
        ),
        parse_constant=lambda value: (_ for _ in ()).throw(
            GateError("constant:" + value)
        ),
    )
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            part = stream.read(1 << 20)
            need(bool(part), "truncated array:" + marker)
            buffer = part
            continue
        if buffer[0] == ",":
            buffer = buffer[1:]
            continue
        if buffer[0] == "]":
            return
        while True:
            try:
                value, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                part = stream.read(1 << 20)
                need(bool(part), "truncated row:" + marker)
                buffer += part
        yield value
        buffer = buffer[end:]


def verify_row(row: dict[str, Any], label: str) -> None:
    claimed = row["row_sha256"]
    payload = dict(row)
    payload.pop("row_sha256")
    need(digest(payload) == claimed, "row closure:" + label)


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    return {**payload, "row_sha256": digest(payload)}


def zero_credit_fields() -> dict[str, Any]:
    return {
        "formal_component_edge_credit": 0,
        "formal_component_union_credit": 0,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_component_quotient_credit": 0,
        "formal_occurrence_identity_collapse_credit": 0,
        "formal_official_key_merge_credit": 0,
        "formal_seam_edge_credit": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
        "eligible_for_component_DSU_application": False,
    }


def make_ledger(
    *,
    schema: str,
    status: str,
    rows: list[dict[str, Any]],
    id_field: str,
) -> dict[str, Any]:
    return {
        "schema": schema,
        "status": status,
        "row_count": len(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows_sha256": digest(rows),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def ledger_summary(
    document: dict[str, Any],
    filename: str,
) -> dict[str, Any]:
    return {
        "filename": filename,
        "schema": document["schema"],
        "row_count": document["row_count"],
        "row_ids_sha256": document["row_ids_sha256"],
        "row_hashes_sha256": document["row_hashes_sha256"],
        "rows_sha256": document["rows_sha256"],
    }


def build(
    producer_file_sha256: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    for filename, expected in FILES.values():
        path = HERE / filename
        need(path.is_file(), "missing input:" + filename)
        need(file_sha256(path) == expected, "input pin:" + filename)

    pair_rows: list[dict[str, Any]] = []
    all_pair_count = 0
    family_histogram: Counter[tuple[str, ...]] = Counter()
    raw_binding_histogram: Counter[str] = Counter()
    seen_pairs: set[tuple[str, str]] = set()
    for source in iter_array(HERE / FILES["R300D"][0], "canonical_incidence_edge_rows"):
        verify_row(source, "R300D pair")
        all_pair_count += 1
        endpoints = tuple(
            sorted(source["canonical_unordered_Round294_registry_occurrence_ids"])
        )
        need(len(endpoints) == 2 and endpoints[0] != endpoints[1], "pair")
        need(endpoints not in seen_pairs, "unique R300D pair")
        seen_pairs.add(endpoints)
        kinds = tuple(sorted(source["witness_kind_histogram"]))
        if set(kinds) == {GRAPH}:
            continue
        need(
            set(kinds) in (
                {GRAPH, TRANS},
                {GRAPH, NEG, POS},
                {GRAPH, NEG, POS, TRANS},
            ),
            "enriched family",
        )
        family_histogram[kinds] += 1
        raw_binding_histogram.update(source["witness_kind_histogram"])
        owner_policy = NEG in kinds or POS in kinds
        disposition = (
            "EXCLUDED__T0_OWNER_POLICY_AND_ATOM_COVER_ARE_INCIDENCE_ONLY__"
            "NO_FORMAL_OWNER_CHILD_OR_ORIGIN_TO_ROUND266_ROOT_LINEAGE"
            if owner_policy
            else
            "EXCLUDED__TRANSVERSE_LINE_IS_ANALYTIC_BOUNDARY_WITH_NO_"
            "ADJACENT_TUBE_DEDUP_CREDIT__NO_INCLUDED_STRATUM_TWO_"
            "ATTACHMENT_LEMMA"
        )
        payload = {
            "Round300H_enriched_pair_disposition_row_id":
                "round300h-enriched-pair-disposition:"
                + digest([
                    source[
                        "Round300D_lower_physical_witness_incidence_edge_row_id"
                    ],
                    source["row_sha256"],
                ]),
            "source_Round300D_pair_row_id": source[
                "Round300D_lower_physical_witness_incidence_edge_row_id"
            ],
            "source_Round300D_pair_row_sha256": source["row_sha256"],
            "canonical_unordered_Round294_registry_occurrence_ids":
                list(endpoints),
            "witness_kind_histogram":
                dict(sorted(source["witness_kind_histogram"].items())),
            "witness_multiplicity": source["witness_multiplicity"],
            "source_Round295A_physical_incidence_binding_row_ids":
                source["source_Round295A_physical_incidence_binding_row_ids"],
            "source_Round295A_physical_incidence_binding_row_sha256s":
                source[
                    "source_Round295A_physical_incidence_binding_row_sha256s"
                ],
            "disposition_tranche": (
                "OWNER_POLICY_INCIDENCE_ONLY" if owner_policy
                else "GRAPH_TRANS_ANALYTIC_BOUNDARY_ONLY"
            ),
            "transverse_analytic_boundary_present": TRANS in kinds,
            "transverse_owner_status": (
                "ANALYTIC_BOUNDARY_STRATUM__NO_ADJACENT_TUBE_DEDUP_CREDIT"
                if TRANS in kinds else None
            ),
            "t0_owner_policy_cells_present": owner_policy,
            "owner_rectangles_exactly_cover_graph_leaf_base":
                True if owner_policy else None,
            "included_stratum_two_attachment_lemma_pinned": False,
            "owner_child_or_origin_to_Round266_root_lineage_count": 0,
            "direct_formal_lineage_hit_count": 0,
            "prior_Round300C_E_F_component_edge_endpoint_hit_count": 0,
            "formal_disposition": disposition,
            **zero_credit_fields(),
        }
        pair_rows.append(closed(payload))

    pair_rows.sort(
        key=lambda row: row["Round300H_enriched_pair_disposition_row_id"]
    )
    need(
        all_pair_count == 111_524
        and len(pair_rows) == 144
        and family_histogram == Counter({
            tuple(sorted((GRAPH, TRANS))): 56,
            tuple(sorted((GRAPH, NEG, POS))): 32,
            tuple(sorted((GRAPH, NEG, POS, TRANS))): 56,
        })
        and raw_binding_histogram
        == Counter({GRAPH: 144, TRANS: 112, NEG: 128, POS: 88}),
        "pair census",
    )

    single_rows: list[dict[str, Any]] = []
    single_kind_histogram: Counter[str] = Counter()
    single_tranche_histogram: Counter[str] = Counter()
    new_kind_histogram: Counter[str] = Counter()
    preserved_occurrences: set[str] = set()
    preserved_roots: set[str] = set()
    new_occurrences: set[str] = set()
    for source in iter_array(
        HERE / FILES["R300D"][0],
        "single_target_assignment_exclusion_rows",
    ):
        verify_row(source, "R300D single")
        target = source["target_Round294_registry_occurrence"]
        tranche = target["registry_entry_kind"]
        need(tranche in {NEW, PRESERVED}, "single tranche")
        single_kind_histogram[source["witness_kind"]] += 1
        single_tranche_histogram[tranche] += 1
        occurrence = target["registry_occurrence_id"]
        provenance = target["preserved_Round266_provenance"]
        if tranche == PRESERVED:
            need(provenance is not None, "preserved provenance")
            preserved_occurrences.add(occurrence)
            preserved_roots.add(provenance["Round266_quotient_component_id"])
            disposition = (
                "RECLOSED_EXISTING_ROUND266_OCCURRENCE_ROOT__ZERO_NEW_EDGE"
            )
        else:
            need(
                provenance is None and source["witness_kind"] in {NEG, POS},
                "new single owner witness",
            )
            new_kind_histogram[source["witness_kind"]] += 1
            new_occurrences.add(occurrence)
            disposition = (
                "EXCLUDED__UNIQUE_TARGET_ASSIGNMENT_HAS_NO_FORMAL_"
                "OWNER_ROOT_ATTACHMENT_LINEAGE"
            )
        payload = {
            "Round300H_single_target_disposition_row_id":
                "round300h-single-target-disposition:"
                + digest([
                    source[
                        "Round300D_single_target_assignment_exclusion_row_id"
                    ],
                    source["row_sha256"],
                ]),
            "source_Round300D_single_row_id": source[
                "Round300D_single_target_assignment_exclusion_row_id"
            ],
            "source_Round300D_single_row_sha256": source["row_sha256"],
            "source_Round295A_physical_incidence_binding_row_id": source[
                "source_Round295A_physical_incidence_binding_row_id"
            ],
            "source_Round295A_physical_incidence_binding_row_sha256": source[
                "source_Round295A_physical_incidence_binding_row_sha256"
            ],
            "target_Round294_registry_occurrence_id": occurrence,
            "target_Round294_registry_entry_kind": tranche,
            "target_Round294_registry_row_id":
                target["Round294_occurrence_registry_row_id"],
            "target_Round294_registry_row_sha256":
                target["Round294_occurrence_registry_row_sha256"],
            "witness_kind": source["witness_kind"],
            "preserved_Round266_provenance": provenance,
            "canonical_two_target_incidence_edge_issued": False,
            "direct_formal_owner_root_attachment_lineage_count": 0,
            "prior_Round300C_E_F_component_edge_endpoint_hit_count": 0,
            "formal_disposition": disposition,
            **zero_credit_fields(),
        }
        single_rows.append(closed(payload))

    single_rows.sort(
        key=lambda row: row["Round300H_single_target_disposition_row_id"]
    )
    need(
        len(single_rows) == 1_600
        and single_tranche_histogram == Counter({
            PRESERVED: 1_408,
            NEW: 192,
        })
        and single_kind_histogram == Counter({
            NEG: 416,
            POS: 352,
            "ROUND208_DIRECT_GRAPH_SIDE_REGION": 608,
            "SOURCE_EXACT_T0_SHEET_CELL": 224,
        })
        and new_kind_histogram == Counter({NEG: 116, POS: 76})
        and len(preserved_occurrences) == 1_108
        and len(preserved_roots) == 118
        and len(new_occurrences) == 108,
        "single census",
    )

    pair_ledger = make_ledger(
        schema=SCHEMA + ".enriched-pair-disposition-ledger.v1",
        status=(
            "FORMAL_144_ENRICHED_PAIR_DISPOSITIONS__"
            "ZERO_ELIGIBLE_COMPONENT_EDGES"
        ),
        rows=pair_rows,
        id_field="Round300H_enriched_pair_disposition_row_id",
    )
    single_ledger = make_ledger(
        schema=SCHEMA + ".single-target-disposition-ledger.v1",
        status=(
            "FORMAL_1600_SINGLE_TARGET_DISPOSITIONS__"
            "ZERO_ELIGIBLE_COMPONENT_EDGES"
        ),
        rows=single_rows,
        id_field="Round300H_single_target_disposition_row_id",
    )
    edge_ledger = make_ledger(
        schema=SCHEMA + ".eligible-component-edge-ledger.v1",
        status="FORMAL_EMPTY_ELIGIBLE_COMPONENT_EDGE_LEDGER",
        rows=[],
        id_field="Round300H_eligible_component_edge_row_id",
    )

    payload = {
        "schema": SCHEMA,
        "status": (
            "PASS_ROUND300H_ZERO_ELIGIBLE_COMPONENT_EDGES__"
            "144_ENRICHED_PAIRS_AND_1600_SINGLES_EXHAUSTED"
        ),
        "producer_file_sha256": producer_file_sha256,
        "input_file_pins": {
            filename: sha256 for filename, sha256 in sorted(FILES.values())
        },
        "seed_independence": {
            "PYTHONHASHSEED_affects_output_bytes": False,
            "all_sets_and_maps_are_canonically_sorted_before_commitment": True,
            "gzip_mtime": 0,
        },
        "complete_pair_frontier": {
            "Round300D_canonical_pair_count": 111_524,
            "Round300D_pure_GRAPH_pair_count": 111_380,
            "Round300H_enriched_pair_count": 144,
            "Round300E_source_pair_count": 472,
            "Round300F_source_pair_count": 264,
            "Round300G_candidate_pair_count": 128,
            "E_F_G_H_pairwise_disjoint": True,
            "E_F_G_H_union_count": 1_008,
            "remaining_pure_GRAPH_incidence_only_pair_count": 110_516,
            "H_family_histogram": {
                "+".join(key): value
                for key, value in sorted(family_histogram.items())
            },
            "H_raw_binding_kind_histogram":
                dict(sorted(raw_binding_histogram.items())),
        },
        "geometry_and_lineage_reclosure": {
            "distinct_H_graph_leaves": 144,
            "distinct_H_transverse_lines": 112,
            "distinct_H_carrier_children": 144,
            "distinct_H_carrier_origins": 144,
            "transverse_boundary_face_histogram": {
                "LOWER_T_FACE": 56,
                "UPPER_T_FACE": 56,
            },
            "transverse_owner_status":
                "ANALYTIC_BOUNDARY_STRATUM__NO_ADJACENT_TUBE_DEDUP_CREDIT",
            "owner_policy_pair_count": 88,
            "owner_rectangle_cover_histogram": {
                "EXACT_FULL_GRAPH_LEAF_BASE": 88,
            },
            "R293_component_edge_credit_sum": 0,
            "R293_Jx_Jy_same_point_glue_credit_sum": 0,
            "R295A_component_union_credit_sum": 0,
            "direct_lineage_hit_counts": {
                "R204_child_hits": 0,
                "R204_origin_hits": 0,
                "R208_child_hits": 0,
                "R208_origin_hits": 0,
                "R220_child_hits": 0,
                "R220_origin_hits": 0,
                "R245_child_hits": 0,
                "R246_child_hits": 0,
                "R247_child_hits": 0,
                "R248_interface_hits": 0,
            },
            "prior_component_edge_endpoint_hits": {
                "R300C_H_endpoint_hits": 0,
                "R300C_new_single_hits": 0,
                "R300E_H_endpoint_hits": 0,
                "R300E_new_single_hits": 0,
                "R300F_H_endpoint_hits": 0,
                "R300F_new_single_hits": 0,
            },
        },
        "complete_single_frontier": {
            "total_assignment_count": 1_600,
            "preserved_assignment_reclosure_count": 1_408,
            "preserved_distinct_occurrence_count": 1_108,
            "preserved_distinct_Round266_root_count": 118,
            "new_assignment_count": 192,
            "new_distinct_occurrence_count": 108,
            "new_witness_kind_histogram": {
                NEG: 116,
                POS: 76,
            },
            "new_component_edge_credit": 0,
        },
        "disposition_census": {
            "GRAPH_TRANS_ONLY_excluded_count": 56,
            "OWNER_POLICY_excluded_count": 88,
            "NEW_SINGLE_excluded_count": 192,
            "PRESERVED_SINGLE_reclosed_count": 1_408,
            "eligible_component_edge_count": 0,
        },
        "enriched_pair_disposition_ledger": ledger_summary(
            pair_ledger, PAIR_LEDGER.name
        ),
        "single_target_disposition_ledger": ledger_summary(
            single_ledger, SINGLE_LEDGER.name
        ),
        "eligible_component_edge_ledger": ledger_summary(
            edge_ledger, EDGE_LEDGER.name
        ),
        "strict_nonpromotion": {
            "formal_component_edge_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_component_quotient_credit": 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_official_key_merge_credit": 0,
            "formal_seam_edge_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "eligible_edge_count_for_component_DSU_application": 0,
            "component_DSU_applied": False,
        },
        "required_next": (
            "Round301 may consume the explicit empty eligible edge ledger, "
            "while retaining both complete disposition ledgers as closure "
            "evidence; no R300H row may be inferred into the DSU."
        ),
    }
    result = {**payload, "result_sha256": digest(payload)}
    return pair_ledger, single_ledger, edge_ledger, result


def gzip_bytes(value: dict[str, Any]) -> bytes:
    output = BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        fileobj=output,
        compresslevel=9,
        mtime=0,
    ) as stream:
        stream.write(canonical(value))
    return output.getvalue()


def atomic_write(path: Path, data: bytes) -> None:
    with tempfile.NamedTemporaryFile(
        dir=HERE,
        prefix="." + path.name + ".",
        delete=False,
    ) as stream:
        temporary = Path(stream.name)
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    producer_sha256 = file_sha256(Path(__file__).resolve())
    pair, single, edge, result = build(producer_sha256)
    bundle = [
        (PAIR_LEDGER, gzip_bytes(pair)),
        (SINGLE_LEDGER, gzip_bytes(single)),
        (EDGE_LEDGER, gzip_bytes(edge)),
        (RESULT, canonical(result) + b"\n"),
    ]
    if arguments.no_write:
        for path, data in bundle:
            need(
                path.is_file() and path.read_bytes() == data,
                "deterministic replay:" + path.name,
            )
    else:
        for path, data in bundle:
            atomic_write(path, data)
    print(json.dumps({
        "status": result["status"],
        "enriched_pair_disposition_rows": pair["row_count"],
        "single_target_disposition_rows": single["row_count"],
        "eligible_component_edges": edge["row_count"],
        "result_sha256": result["result_sha256"],
        "write": not arguments.no_write,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
