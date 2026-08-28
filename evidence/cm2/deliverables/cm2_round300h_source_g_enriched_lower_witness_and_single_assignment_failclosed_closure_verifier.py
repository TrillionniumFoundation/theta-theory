#!/usr/bin/env python3
"""Independent verifier for the formal R300-H fail-closed closure.

The producer is never imported, executed, parsed, or tokenized.  It is
treated only as inert hash-pinned bytes.  Expected candidate artifacts are
independently reconstructed from sealed upstream data before any candidate
output is opened.  The audit is deliberately fail-closed: a lower witness
could be promoted only if the artifacts pinned both attachment semantics and
an unambiguous lineage into the post-Round266 component frontier.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from fractions import Fraction as Q
import gc
import gzip
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Callable, Iterable, Iterator, TextIO


HERE = Path(__file__).resolve().parent
D = HERE
PREFIX = (
    "cm2_round300h_source_g_enriched_lower_witness_and_"
    "single_assignment_failclosed_closure"
)
PRODUCER_PATH = HERE / f"{PREFIX}.py"
PAIR_LEDGER_PATH = (
    HERE / f"{PREFIX}_enriched_pair_disposition_ledger.json.gz"
)
SINGLE_LEDGER_PATH = (
    HERE / f"{PREFIX}_single_target_disposition_ledger.json.gz"
)
EDGE_LEDGER_PATH = (
    HERE / f"{PREFIX}_eligible_component_edge_ledger.json.gz"
)
RESULT_PATH = HERE / f"{PREFIX}_result.json"
ATTACK_PATH = HERE / f"{PREFIX}_attack_suite.json"
VERIFICATION_PATH = HERE / f"{PREFIX}_verification.json"

# Filled only from the producer's inert bytes; the verifier never parses them.
PRODUCER_SHA256 = (
    "3d93a3a13b494fbf136916827e63fb5861960cec9de8dcb4facceb16c5f0b952"
)
SCHEMA = (
    "cm2.round300h.source-g-enriched-lower-witness-and-"
    "single-assignment-failclosed-closure.v1"
)
ATTACK_SCHEMA = SCHEMA + ".attack-suite.v1"
VERIFICATION_SCHEMA = SCHEMA + ".verification.v1"

FILES = {
    "R179": "cm2_round179_source_g_residual_tube_arrangement_rows.json",
    "R182": "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json",
    "R204": "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json",
    "R208": "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json",
    "R220": "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json",
    "R245": "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json",
    "R246": "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json",
    "R247": "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json",
    "R248": "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json",
    "R266": "cm2_round266_source_g_expanded_curved_face_closure_certificate.json",
    "R291": "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_ledger.json.gz",
    "R293": "cm2_round293_source_g_r289_r291_witness_binding_canonical_closure_ledger.json.gz",
    "R295A": "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_physical_witness_incidence_binding_ledger.json.gz",
    "R300A": "cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion_ledger.json.gz",
    "R300C": "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_volume_edge_promotion_edge_ledger.json.gz",
    "R300D": "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_ledger.json.gz",
    "R300D_RESULT": "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_result.json",
    "R300E": "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_promotion_witness_ledger.json.gz",
    "R300F": "cm2_round300f_source_g_r245_half_open_owner_sheet_attachment_ledger.json.gz",
}

PINS = {
    "R179": "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "R182": "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    "R204": "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "R208": "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    "R220": "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "R245": "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1",
    "R246": "a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9",
    "R247": "72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7",
    "R248": "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    "R266": "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf",
    "R291": "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab",
    "R293": "0e7395a69844734cc51563882f471987cc566db28a55ccae6e6d15d045f9e53c",
    "R295A": "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    "R300A": "ddc1a8bc53861afeb93d3569c6efa228f17d86f161db31a39fa9b72458ab8f2d",
    "R300C": "8c9ed8b09e994a00ca3ca4906c35b454523383b7d488f66e7a082dbbd4b1fcec",
    "R300D": "287d1382b25fd3d5cd0a52c6da8cabbb012040b8a6e35c9f887d7a425b812fa7",
    "R300D_RESULT": "59b7e788ed217ceb590a3e2125cc13aefbf447af236315ea607f4f631cb29c84",
    "R300E": "69f480da55e917b7b75bfe1efa823a9228d9b563f6f3aabd4e2a364c9e50eb9f",
    "R300F": "1f958f9f3e3aff7327d897b39851f2d2d030d820e00859d302241702613cae1f",
}

GRAPH = "ROUND182_GRAPH_SHEET_LEAF"
TRANS = "ROUND182_TRANSVERSE_1D_LINE"
NEG = "ROUND179_NEGATIVE_T0_SHADOW_PATCH"
POS = "ROUND179_POSITIVE_T0_RETAINED_OWNER"
NEW = "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
PRESERVED = "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"


class AuditError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise AuditError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def canonical(value: Any) -> bytes:
    return "".join(ENCODER.iterencode(value)).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            state.update(chunk)
    return state.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def guard_exact_regular_path(path: Path, expected_name: str) -> None:
    need(path.name == expected_name, "path alias:" + expected_name)
    need(path.parent.resolve() == HERE.resolve(), "path escape:" + expected_name)
    need(path.exists(), "missing path:" + expected_name)
    need(not path.is_symlink(), "symlink:" + expected_name)
    stat = path.stat()
    need(path.is_file(), "not regular file:" + expected_name)
    need(stat.st_nlink == 1, "hardlink:" + expected_name)


def guard_inputs_and_inert_producer() -> None:
    guard_exact_regular_path(PRODUCER_PATH, PRODUCER_PATH.name)
    need(
        file_sha256(PRODUCER_PATH) == PRODUCER_SHA256,
        "inert producer byte pin",
    )
    for key, expected in PINS.items():
        path = D / FILES[key]
        guard_exact_regular_path(path, FILES[key])
        need(file_sha256(path) == expected, "input byte pin:" + key)


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    with path.open("rt", encoding="utf-8", newline="") as stream:
        result = json.load(
            stream,
            object_pairs_hook=unique_object,
            parse_float=lambda token: (_ for _ in ()).throw(
                AuditError("float:" + token)
            ),
            parse_constant=lambda token: (_ for _ in ()).throw(
                AuditError("constant:" + token)
            ),
        )
    need(type(result) is dict, "top-level object:" + path.name)
    return result


def closed_result(key: str) -> dict[str, Any]:
    document = load_json(D / FILES[key])
    claimed = document["result_sha256"]
    payload = dict(document)
    payload.pop("result_sha256")
    need(
        digest(document["result"]) == claimed or digest(payload) == claimed,
        "result closure:" + key,
    )
    return document["result"]


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


def iter_array(
    path: Path,
    marker: str,
    *,
    compressed: bool,
) -> Iterator[Any]:
    opener = gzip.open if compressed else open
    with opener(path, "rt", encoding="utf-8", newline="") as stream:
        yield from iter_array_stream(stream, marker)


def iter_array_stream(
    stream: TextIO,
    marker: str,
    initial: str = "",
) -> Iterator[Any]:
    token = json.dumps(marker, ensure_ascii=False) + ":["
    buffer = initial
    while token not in buffer:
        part = stream.read(1 << 20)
        need(bool(part), "missing array marker:" + marker)
        buffer += part
        if len(buffer) > len(token) + (1 << 20):
            buffer = buffer[-(len(token) + (1 << 20)) :]
    buffer = buffer.split(token, 1)[1]
    decoder = json.JSONDecoder(
        object_pairs_hook=unique_object,
        parse_float=lambda token: (_ for _ in ()).throw(
            AuditError("stream float:" + token)
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            AuditError("stream constant:" + token)
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


def iter_named_table_rows(path: Path, table_name: str) -> Iterator[Any]:
    table_token = json.dumps(table_name, ensure_ascii=False) + ":"
    with path.open("rt", encoding="utf-8", newline="") as stream:
        buffer = ""
        while table_token not in buffer:
            part = stream.read(1 << 20)
            need(bool(part), "missing table marker:" + table_name)
            buffer += part
            if len(buffer) > len(table_token) + (1 << 20):
                buffer = buffer[-(len(table_token) + (1 << 20)) :]
        initial = buffer.split(table_token, 1)[1]
        yield from iter_array_stream(stream, "rows", initial)


def pair(values: Iterable[str]) -> tuple[str, str]:
    result = tuple(sorted(values))
    need(len(result) == 2 and result[0] != result[1], "canonical pair")
    return result  # type: ignore[return-value]


def qbox(values: list[str]) -> tuple[Q, Q, Q, Q, Q, Q]:
    need(len(values) == 6, "six-coordinate box")
    result = tuple(map(Q, values))
    need(
        result[0] <= result[1]
        and result[2] < result[3]
        and result[4] < result[5],
        "ordered box",
    )
    return result  # type: ignore[return-value]


def rectangle_union_area(rectangles: Iterable[tuple[Q, Q, Q, Q]]) -> Q:
    rows = sorted(set(rectangles))
    if not rows:
        return Q(0)
    xcuts = sorted({value for row in rows for value in row[:2]})
    total = Q(0)
    for x0, x1 in zip(xcuts, xcuts[1:]):
        intervals = sorted(
            (row[2], row[3])
            for row in rows
            if row[0] < x1 and row[1] > x0
        )
        merged: list[list[Q]] = []
        for lower, upper in intervals:
            if not merged or lower > merged[-1][1]:
                merged.append([lower, upper])
            else:
                merged[-1][1] = max(merged[-1][1], upper)
        total += (x1 - x0) * sum(
            (upper - lower for lower, upper in merged), Q(0)
        )
    return total


def packed_table(
    result: dict[str, Any],
    table: str,
) -> tuple[list[str], list[list[Any]]]:
    columns = result["row_column_schemas"][table]
    rows = result[table]
    commitment = result["table_census_and_sha256"][table]
    need(
        len(rows) == commitment["row_count"]
        and digest(rows) == commitment["rows_sha256"],
        "packed commitment:" + table,
    )
    return columns, rows


def unpack(columns: list[str], row: list[Any]) -> dict[str, Any]:
    need(len(columns) == len(row), "packed width")
    return dict(zip(columns, row))


def reconstruct_expected() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    # R300-D is the complete source frontier for this audit.
    all_pairs: set[tuple[str, str]] = set()
    enriched: list[dict[str, Any]] = []
    for row in iter_array(
        D / FILES["R300D"],
        "canonical_incidence_edge_rows",
        compressed=True,
    ):
        verify_row(row, "R300D pair")
        key = pair(row["canonical_unordered_Round294_registry_occurrence_ids"])
        need(key not in all_pairs, "unique R300D pair")
        all_pairs.add(key)
        kinds = set(row["witness_kind_histogram"])
        if kinds != {GRAPH}:
            enriched.append(row)
    need(len(all_pairs) == 111_524 and len(enriched) == 144, "R300D pair census")

    singles: list[dict[str, Any]] = []
    for row in iter_array(
        D / FILES["R300D"],
        "single_target_assignment_exclusion_rows",
        compressed=True,
    ):
        verify_row(row, "R300D single")
        singles.append(row)
    need(len(singles) == 1_600, "R300D single census")

    h_pairs = {
        pair(row["canonical_unordered_Round294_registry_occurrence_ids"])
        for row in enriched
    }
    h_hist = Counter(
        tuple(sorted(row["witness_kind_histogram"])) for row in enriched
    )
    need(
        h_hist
        == {
            tuple(sorted((GRAPH, TRANS))): 56,
            tuple(sorted((GRAPH, NEG, POS))): 32,
            tuple(sorted((GRAPH, NEG, POS, TRANS))): 56,
        },
        "H witness-family partition",
    )

    # Reclose E/F/G pairwise disjointness and the pure-GRAPH remainder.
    e_pairs: set[tuple[str, str]] = set()
    for row in iter_array(D / FILES["R300E"], "rows", compressed=True):
        verify_row(row, "R300E witness")
        e_pairs.add(pair([
            row["owner_Round294_registry_occurrence_id"],
            row["excluded_present_side_Round294_registry_occurrence_id"],
        ]))
    f_pairs: set[tuple[str, str]] = set()
    for row in iter_array(D / FILES["R300F"], "rows", compressed=True):
        verify_row(row, "R300F witness")
        f_pairs.add(pair([
            row["Round294_owner_occurrence_id"],
            row["Round294_shadow_occurrence_id"],
        ]))
    g_pairs: set[tuple[str, str]] = set()
    for row in iter_array(
        D / FILES["R300A"],
        "canonical_occurrence_pair_rows",
        compressed=True,
    ):
        verify_row(row, "R300A pair")
        if row["R295A_explicit_lower_graph_sheet_witness_present"]:
            g_pairs.add(pair(row["canonical_unordered_Round294_registry_occurrence_ids"]))
    need(
        (len(e_pairs), len(f_pairs), len(g_pairs), len(h_pairs))
        == (472, 264, 128, 144),
        "E/F/G/H pair censuses",
    )
    tranches = [e_pairs, f_pairs, g_pairs, h_pairs]
    need(
        all(not tranches[i] & tranches[j]
            for i in range(len(tranches))
            for j in range(i + 1, len(tranches))),
        "E/F/G/H pairwise disjoint",
    )
    promoted_or_audited = set().union(*tranches)
    need(
        promoted_or_audited <= all_pairs
        and len(promoted_or_audited) == 1_008
        and len(all_pairs - promoted_or_audited) == 110_516,
        "pure-GRAPH remainder",
    )

    # Select the exact R295A bindings named by H and all singles.
    selected_binding_ids = {
        value
        for row in enriched
        for value in row["source_Round295A_physical_incidence_binding_row_ids"]
    } | {
        row["source_Round295A_physical_incidence_binding_row_id"]
        for row in singles
    }
    bindings: dict[str, dict[str, Any]] = {}
    for row in iter_array(D / FILES["R295A"], "rows", compressed=True):
        row_id = row["Round295A_R291_physical_incidence_binding_row_id"]
        if row_id not in selected_binding_ids:
            continue
        verify_row(row, "R295A binding")
        need(row_id not in bindings, "unique selected R295A")
        bindings[row_id] = row
    need(set(bindings) == selected_binding_ids, "selected R295A complete")

    for row in enriched:
        expected_pair = pair(
            row["canonical_unordered_Round294_registry_occurrence_ids"]
        )
        for row_id in row["source_Round295A_physical_incidence_binding_row_ids"]:
            source = bindings[row_id]
            need(
                pair(source["target_Round294_registry_occurrence_ids"])
                == expected_pair,
                "H binding pair exact",
            )
    for row in singles:
        source = bindings[row["source_Round295A_physical_incidence_binding_row_id"]]
        target = row["target_Round294_registry_occurrence"]["registry_occurrence_id"]
        need(
            source["target_Round294_registry_occurrence_ids"] == [target],
            "single binding target exact",
        )

    selected_r291_ids = {
        row["Round291_local_disposition_row_id"] for row in bindings.values()
    }
    dispositions: dict[str, dict[str, Any]] = {}
    for row in iter_array(D / FILES["R291"], "rows", compressed=True):
        row_id = row["complete_lower_stratum_local_disposition_row_id"]
        if row_id not in selected_r291_ids:
            continue
        verify_row(row, "R291 disposition")
        need(row_id not in dispositions, "unique selected R291")
        dispositions[row_id] = row
    need(set(dispositions) == selected_r291_ids, "selected R291 complete")

    selected_r293_ids = {
        row["source_Round293_R291_physical_witness_binding_row_id"]
        for row in bindings.values()
    }
    bindings293: dict[str, dict[str, Any]] = {}
    for row in iter_array(
        D / FILES["R293"],
        "Round291_physical_witness_binding_rows",
        compressed=True,
    ):
        row_id = row["Round292_R291_physical_witness_binding_row_id"]
        if row_id not in selected_r293_ids:
            continue
        verify_row(row, "R293 binding")
        need(row_id not in bindings293, "unique selected R293")
        bindings293[row_id] = row
    need(set(bindings293) == selected_r293_ids, "selected R293 complete")

    # Materialize each selected physical cell and reclose zero-credit semantics.
    cells: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    h_binding_ids = {
        value
        for row in enriched
        for value in row["source_Round295A_physical_incidence_binding_row_ids"]
    }
    new_single_binding_ids = {
        row["source_Round295A_physical_incidence_binding_row_id"]
        for row in singles
        if row["target_Round294_registry_occurrence"]["registry_entry_kind"]
        == NEW
    }
    for binding_id, binding in bindings.items():
        disposition = dispositions[binding["Round291_local_disposition_row_id"]]
        index = binding["physical_witness_cell_index"]
        cell = disposition["physical_witness_cells"][index]
        need(
            cell["witness_kind"] == binding["witness_kind"],
            "R291/R295A witness kind",
        )
        source293 = bindings293[
            binding["source_Round293_R291_physical_witness_binding_row_id"]
        ]
        need(
            source293["Round291_local_disposition_row_id"]
            == binding["Round291_local_disposition_row_id"]
            and source293["physical_witness_cell_index"] == index
            and source293["witness_kind"] == cell["witness_kind"],
            "R293 source-cell rebinding",
        )
        if binding_id in h_binding_ids | new_single_binding_ids:
            need(
                sorted(source293["terminal_registry_target_references"])
                == sorted(binding["target_Round294_registry_occurrence_ids"]),
                "R293 target rebinding:" + binding_id,
            )
        if binding_id in h_binding_ids | new_single_binding_ids:
            need(
                source293["exact_witness_covered_by_named_registry_supports"]
                is True,
                "R293 exact witness cover",
            )
        need(
            source293["component_edge_credit"] == 0
            and source293["occurrence_binding_credit"] == 0
            and source293["Jx_Jy_same_point_glue_credit"] == 0,
            "R293 zero component credit",
        )
        need(
            binding["formal_component_union_credit"] == 0
            and binding["formal_DSU_rank_reduction_credit"] == 0
            and binding["formal_Jx_Jy_same_point_glue_credit"] == 0
            and binding["formal_seam_edge_credit"] == 0,
            "R295A zero component credit",
        )
        cells[binding_id] = (disposition, cell)

    h_kind_hist = Counter(
        bindings[row_id]["witness_kind"] for row_id in h_binding_ids
    )
    need(
        h_kind_hist == {GRAPH: 144, TRANS: 112, NEG: 128, POS: 88},
        "H raw binding census",
    )

    single_kind_hist = Counter(
        bindings[row["source_Round295A_physical_incidence_binding_row_id"]][
            "witness_kind"
        ]
        for row in singles
    )
    single_tranche_hist = Counter(
        row["target_Round294_registry_occurrence"]["registry_entry_kind"]
        for row in singles
    )
    need(
        single_kind_hist
        == {
            NEG: 416,
            POS: 352,
            "ROUND208_DIRECT_GRAPH_SIDE_REGION": 608,
            "SOURCE_EXACT_T0_SHEET_CELL": 224,
        }
        and single_tranche_hist == {PRESERVED: 1_408, NEW: 192},
        "single partition",
    )
    new_singles = [
        row for row in singles
        if row["target_Round294_registry_occurrence"]["registry_entry_kind"]
        == NEW
    ]
    preserved_singles = [
        row for row in singles
        if row["target_Round294_registry_occurrence"]["registry_entry_kind"]
        == PRESERVED
    ]
    need(
        Counter(
            bindings[row["source_Round295A_physical_incidence_binding_row_id"]][
                "witness_kind"
            ]
            for row in new_singles
        ) == {NEG: 116, POS: 76},
        "new-single NEG/POS census",
    )

    # Reconstruct only the R182 graph leaves and transverse lines used by H.
    graph_leaf_ids = {
        cells[row_id][1]["leaf_row_id"]
        for row_id in h_binding_ids
        if bindings[row_id]["witness_kind"] == GRAPH
    }
    trans_pair_ids = {
        cells[row_id][1]["pair_row_id"]
        for row_id in h_binding_ids
        if bindings[row_id]["witness_kind"] == TRANS
    }
    r182 = closed_result("R182")
    leaf_columns, leaf_packed = packed_table(r182, "collar_leaf_rows")
    pair_columns, pair_packed = packed_table(r182, "pair_intersection_rows")
    leaves = {
        row[0]: unpack(leaf_columns, row)
        for row in leaf_packed if row[0] in graph_leaf_ids
    }
    pair_rows = {
        row[0]: unpack(pair_columns, row)
        for row in pair_packed if row[0] in trans_pair_ids
    }
    need(
        set(leaves) == graph_leaf_ids
        and set(pair_rows) == trans_pair_ids
        and len(leaves) == 144
        and len(pair_rows) == 112,
        "R182 selected geometry complete",
    )

    trans_boundary_hist = Counter()
    trans_child_ids: set[str] = set()
    trans_origins: set[str] = set()
    for row in pair_rows.values():
        need(
            row["source_graph_equation"] == "t=0"
            and row["source_graph_exact_factorization"].endswith("*t")
            and row["existence_classification"]
            == "UNIQUE_TRANSVERSE_1D_INTERSECTION_LINE__P_BRACKET_AND_INTERVAL_NEWTON"
            and row["interval_newton_interior"] is True
            and row["actual_intersection_dimension"] == "EXACT_DIMENSION_1"
            and row["actual_1D_intersection_component_count"] == 1
            and row["actual_boundary_0D_corner_incidence_count"] == 2
            and row["integer_wall_endpoint_owner_status"]
            == "ANALYTIC_BOUNDARY_STRATUM__NO_ADJACENT_TUBE_DEDUP_CREDIT"
            and row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0,
            "R182 transverse fail-closed contract",
        )
        trans_boundary_hist[row["source_graph_t_boundary_face"]] += 1
        trans_child_ids.add(row["containing_Round179_retained_child_row_id"])
        trans_origins.add(row["origin_row_id"])

    # For each H pair, line up graph, transverse, and owner-policy carriers.
    h_carrier_children: set[str] = set()
    h_carrier_origins: set[str] = set()
    h_owner_children: set[str] = set()
    h_owner_origins: set[str] = set()
    owner_cover_hist = Counter()
    pair_geometry_rows: list[dict[str, Any]] = []
    for edge in enriched:
        ids = edge["source_Round295A_physical_incidence_binding_row_ids"]
        by_kind: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = defaultdict(list)
        for row_id in ids:
            by_kind[bindings[row_id]["witness_kind"]].append(cells[row_id])
        need(len(by_kind[GRAPH]) == 1, "one graph binding per H pair")
        graph_disposition, graph_cell = by_kind[GRAPH][0]
        leaf = leaves[graph_cell["leaf_row_id"]]
        graph_child = graph_cell["retained_child_row_id"]
        graph_origin = graph_disposition["containing_Round174_residual_row_id"]
        need(
            leaf["retained_child_row_id"] == graph_child
            and leaf["box"] == graph_cell["exact_box"],
            "R182/R291 graph carrier",
        )
        h_carrier_children.add(graph_child)
        h_carrier_origins.add(graph_origin)

        if by_kind.get(TRANS):
            need(len(by_kind[TRANS]) == 1, "one transverse binding per H pair")
            _, trans_cell = by_kind[TRANS][0]
            trans_row = pair_rows[trans_cell["pair_row_id"]]
            need(
                trans_cell["containing_retained_child_row_id"] == graph_child
                == trans_row["containing_Round179_retained_child_row_id"]
                and trans_row["origin_row_id"] == graph_origin
                and trans_cell["interval_newton_domain"]
                == trans_row["interval_newton_domain"],
                "graph/transverse exact carrier",
            )

        owner_rectangles: list[tuple[Q, Q, Q, Q]] = []
        for kind in (NEG, POS):
            for _, owner_cell in by_kind.get(kind, []):
                box = qbox(owner_cell["exact_bounds"])
                need(
                    box[0] == box[1] == 0
                    and owner_cell["owner_policy"]
                    == "OUTCOME_BLIND_POSITIVE_T_SIDE_OWNS__NEGATIVE_T_SIDE_IS_SHADOW",
                    "owner-policy t0 cell",
                )
                h_owner_children.add(
                    owner_cell["positive_owner_retained_child_row_id"]
                )
                h_owner_origins.add(owner_cell["positive_owner_origin_row_id"])
                owner_rectangles.append((box[2], box[3], box[4], box[5]))
        if owner_rectangles:
            leaf_box = qbox(leaf["box"])
            leaf_area = (
                (leaf_box[3] - leaf_box[2])
                * (leaf_box[5] - leaf_box[4])
            )
            owner_area = rectangle_union_area(owner_rectangles)
            owner_cover_hist[
                "EXACT_FULL_GRAPH_LEAF_BASE"
                if owner_area == leaf_area else "PARTIAL_GRAPH_LEAF_BASE"
            ] += 1
        pair_geometry_rows.append({
            "pair": list(pair(
                edge["canonical_unordered_Round294_registry_occurrence_ids"]
            )),
            "witness_families": sorted(by_kind),
            "graph_child": graph_child,
            "graph_origin": graph_origin,
            "transverse_no_dedup": bool(by_kind.get(TRANS)),
            "owner_policy_cell_count":
                len(by_kind.get(NEG, [])) + len(by_kind.get(POS, [])),
        })

    need(
        len(h_carrier_children) == len(h_carrier_origins) == 144,
        "H distinct carrier census",
    )

    # Select owner children/origins for the 192 genuinely new singles.
    new_single_owner_children: set[str] = set()
    new_single_owner_origins: set[str] = set()
    for row in new_singles:
        binding_id = row["source_Round295A_physical_incidence_binding_row_id"]
        _, cell = cells[binding_id]
        need(cell["witness_kind"] in {NEG, POS}, "new single owner kind")
        box = qbox(cell["exact_bounds"])
        need(
            box[0] == box[1] == 0
            and cell["owner_policy"]
            == "OUTCOME_BLIND_POSITIVE_T_SIDE_OWNS__NEGATIVE_T_SIDE_IS_SHADOW",
            "new single t0 owner policy",
        )
        new_single_owner_children.add(
            cell["positive_owner_retained_child_row_id"]
        )
        new_single_owner_origins.add(cell["positive_owner_origin_row_id"])

    all_owner_children = h_owner_children | new_single_owner_children
    all_owner_origins = h_owner_origins | new_single_owner_origins
    all_carrier_children = h_carrier_children | all_owner_children
    all_carrier_origins = h_carrier_origins | all_owner_origins

    # Reconstruct the named Round179 retained carriers.
    r179 = closed_result("R179")
    child_columns, child_packed = packed_table(r179, "retained_3d_child_rows")
    retained = {
        row[0]: unpack(child_columns, row)
        for row in child_packed if row[0] in all_carrier_children
    }
    need(set(retained) == all_carrier_children, "R179 selected retained children")
    for row in retained.values():
        need(
            row["origin_row_id"] in all_carrier_origins
            and Q(row["coordinate_volume"]) > 0
            and row["ambient_dimension"] == 3
            and row["whole_origin_credit"] == 0
            and row["global_geometric_disposition_credit"] == 0,
            "R179 retained carrier scope",
        )
    del r179, child_packed
    gc.collect()

    # The only formal Round220 ancestor handle is an exact child/origin hit.
    r220 = closed_result("R220")
    table220 = r220["coordinate_boundary_atlas"]["tables"][
        "one_step_split_interface_rows"
    ]
    need(
        len(table220["rows"]) == table220["row_count"] == 13_076
        and digest(table220["rows"]) == table220["rows_sha256"],
        "R220 interface commitment",
    )
    c220 = {name: index for index, name in enumerate(table220["columns"])}
    r220_child_hits: set[str] = set()
    r220_origin_hits: set[str] = set()
    r220_interface_hits: set[str] = set()
    child_fields = (
        "lower_child_row_id", "upper_child_row_id",
        "half_open_owner_child_row_id",
    )
    for packed in table220["rows"]:
        values = {packed[c220[field]] for field in child_fields}
        child_hit = values & all_carrier_children
        origin = packed[c220["origin_row_id"]]
        if child_hit or origin in all_carrier_origins:
            r220_child_hits.update(child_hit)
            if origin in all_carrier_origins:
                r220_origin_hits.add(origin)
            r220_interface_hits.add(packed[c220["split_interface_id"]])
    del r220
    gc.collect()

    # Direct local-occurrence lineage candidates in Round204/Round208.
    r204 = closed_result("R204")
    rows204 = r204["formal_local_open_3D_region_ledger"]["rows"]
    need(
        len(rows204) == r204["formal_local_open_3D_region_ledger"]["row_count"]
        == 736,
        "R204 region census",
    )
    r204_child_hits = {
        row["retained_child_row_id"] for row in rows204
        if row["retained_child_row_id"] in all_carrier_children
    }
    r204_origin_hits = {
        row["origin_row_id"] for row in rows204
        if row["origin_row_id"] in all_carrier_origins
    }
    del r204, rows204
    gc.collect()

    r208 = closed_result("R208")
    rows208 = r208["formal_local_open_3D_signature_ledger"]["rows"]
    need(
        len(rows208)
        == r208["formal_local_open_3D_signature_ledger"]["row_count"]
        == 36_040,
        "R208 region census",
    )
    r208_child_hits = {
        row["retained_child_row_id"] for row in rows208
        if row["retained_child_row_id"] in all_carrier_children
    }
    r208_origin_hits = {
        row["origin_row_id"] for row in rows208
        if row["origin_row_id"] in all_carrier_origins
    }
    del r208, rows208
    gc.collect()

    # Direct inherited virtual-stratum nodes must carry the exact child ID.
    inherited_hits: dict[str, set[str]] = {}
    inherited_specs = {
        "R245": "formal_retained_stratum_node_ledger",
        "R246": "formal_new_whole_signature_retained_stratum_node_ledger",
        "R247": "formal_new_crossing_and_source_seam_retained_stratum_node_ledger",
    }
    inherited_candidate_node_ids: set[str] = set()
    for key, table_name in inherited_specs.items():
        result = closed_result(key)
        table = result[table_name]
        hits: set[str] = set()
        for row in table["rows"]:
            verify_row(row, key + " node")
            child = row["Round179_retained_child_row_id"]
            if child in all_carrier_children:
                hits.add(child)
                inherited_candidate_node_ids.add(row["retained_stratum_node_id"])
        inherited_hits[key] = hits
        del result
        gc.collect()

    # Without a Round220 interface hit there is no admissible R248 source join.
    # Still inspect the R248 interface inventory to prove zero accidental reuse.
    r248 = closed_result("R248")
    r248_interface_hits = {
        row["Round220_split_interface_id"]
        for row in r248["formal_wall_positive_volume_bulk_ledger"]["rows"]
        if row["Round220_split_interface_id"] in r220_interface_hits
    } | {
        row["Round220_split_interface_id"]
        for row in r248["formal_wall_half_open_sheet_owner_ledger"]["rows"]
        if row["Round220_split_interface_id"] in r220_interface_hits
    }
    del r248
    gc.collect()

    # Reopen every preserved single directly in the Round266 occurrence frontier.
    preserved_targets = {
        row["target_Round294_registry_occurrence"]["registry_occurrence_id"]
        for row in preserved_singles
    }
    preserved_frontier: dict[str, dict[str, Any]] = {}
    for row in iter_named_table_rows(
        D / FILES["R266"],
        "formal_post_Round266_expanded_occurrence_frontier_ledger",
    ):
        occurrence = row["local_occurrence_row_id"]
        if occurrence not in preserved_targets:
            continue
        verify_row(row, "R266 preserved occurrence")
        need(occurrence not in preserved_frontier, "unique preserved frontier")
        preserved_frontier[occurrence] = row

    need(set(preserved_frontier) == preserved_targets, "preserved R266 reopen")
    preserved_roots: set[str] = set()
    for row in preserved_singles:
        target = row["target_Round294_registry_occurrence"]
        occurrence = target["registry_occurrence_id"]
        frontier = preserved_frontier[occurrence]
        provenance = target["preserved_Round266_provenance"]
        need(
            provenance is not None
            and provenance["Round266_expanded_occurrence_frontier_row_id"]
            == frontier["post_Round266_expanded_occurrence_frontier_row_id"]
            and provenance["Round266_expanded_occurrence_frontier_row_sha256"]
            == frontier["row_sha256"]
            and provenance["Round266_quotient_component_id"]
            == frontier["post_Round266_quotient_component_id"],
            "preserved single R266 provenance",
        )
        preserved_roots.add(frontier["post_Round266_quotient_component_id"])

    # Prior component-edge occurrence coverage is diagnostic, never a shortcut.
    h_occurrences = {value for row in h_pairs for value in row}
    new_single_occurrences = {
        row["target_Round294_registry_occurrence"]["registry_occurrence_id"]
        for row in new_singles
    }
    prior_occurrences: dict[str, set[str]] = {}
    for key, occurrence_field in (
        ("R300C", "Round294_registry_occurrence_id"),
        ("R300E", "owner_Round294_registry_occurrence_id"),
        ("R300F", "Round294_owner_occurrence_id"),
    ):
        hits: set[str] = set()
        for row in iter_array(D / FILES[key], "rows", compressed=True):
            occurrence = row[occurrence_field]
            if occurrence in h_occurrences | new_single_occurrences:
                hits.add(occurrence)
        prior_occurrences[key] = hits

    # No lineage candidate is allowed to be silently inferred from counts.
    direct_lineage = {
        "R220_child_hits": r220_child_hits,
        "R220_origin_hits": r220_origin_hits,
        "R204_child_hits": r204_child_hits,
        "R204_origin_hits": r204_origin_hits,
        "R208_child_hits": r208_child_hits,
        "R208_origin_hits": r208_origin_hits,
        "R245_child_hits": inherited_hits["R245"],
        "R246_child_hits": inherited_hits["R246"],
        "R247_child_hits": inherited_hits["R247"],
        "R248_interface_hits": r248_interface_hits,
    }

    need(
        all(not values for values in direct_lineage.values()),
        "all direct lineage channels empty",
    )
    need(
        all(not values for values in prior_occurrences.values()),
        "all prior edge endpoint channels empty",
    )
    need(
        trans_boundary_hist == Counter({
            "LOWER_T_FACE": 56,
            "UPPER_T_FACE": 56,
        })
        and owner_cover_hist == Counter({
            "EXACT_FULL_GRAPH_LEAF_BASE": 88,
        }),
        "geometry census",
    )

    expected_pair_rows: list[dict[str, Any]] = []
    for source in enriched:
        endpoints = sorted(
            source["canonical_unordered_Round294_registry_occurrence_ids"]
        )
        kinds = tuple(sorted(source["witness_kind_histogram"]))
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
            "canonical_unordered_Round294_registry_occurrence_ids": endpoints,
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
        expected_pair_rows.append(closed(payload))
    expected_pair_rows.sort(
        key=lambda row: row["Round300H_enriched_pair_disposition_row_id"]
    )

    expected_single_rows: list[dict[str, Any]] = []
    for source in singles:
        target = source["target_Round294_registry_occurrence"]
        tranche = target["registry_entry_kind"]
        disposition = (
            "RECLOSED_EXISTING_ROUND266_OCCURRENCE_ROOT__ZERO_NEW_EDGE"
            if tranche == PRESERVED
            else
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
            "target_Round294_registry_occurrence_id":
                target["registry_occurrence_id"],
            "target_Round294_registry_entry_kind": tranche,
            "target_Round294_registry_row_id":
                target["Round294_occurrence_registry_row_id"],
            "target_Round294_registry_row_sha256":
                target["Round294_occurrence_registry_row_sha256"],
            "witness_kind": source["witness_kind"],
            "preserved_Round266_provenance":
                target["preserved_Round266_provenance"],
            "canonical_two_target_incidence_edge_issued": False,
            "direct_formal_owner_root_attachment_lineage_count": 0,
            "prior_Round300C_E_F_component_edge_endpoint_hit_count": 0,
            "formal_disposition": disposition,
            **zero_credit_fields(),
        }
        expected_single_rows.append(closed(payload))
    expected_single_rows.sort(
        key=lambda row: row["Round300H_single_target_disposition_row_id"]
    )

    pair_ledger = make_ledger(
        schema=SCHEMA + ".enriched-pair-disposition-ledger.v1",
        status=(
            "FORMAL_144_ENRICHED_PAIR_DISPOSITIONS__"
            "ZERO_ELIGIBLE_COMPONENT_EDGES"
        ),
        rows=expected_pair_rows,
        id_field="Round300H_enriched_pair_disposition_row_id",
    )
    single_ledger = make_ledger(
        schema=SCHEMA + ".single-target-disposition-ledger.v1",
        status=(
            "FORMAL_1600_SINGLE_TARGET_DISPOSITIONS__"
            "ZERO_ELIGIBLE_COMPONENT_EDGES"
        ),
        rows=expected_single_rows,
        id_field="Round300H_single_target_disposition_row_id",
    )
    edge_ledger = make_ledger(
        schema=SCHEMA + ".eligible-component-edge-ledger.v1",
        status="FORMAL_EMPTY_ELIGIBLE_COMPONENT_EDGE_LEDGER",
        rows=[],
        id_field="Round300H_eligible_component_edge_row_id",
    )

    result_payload = {
        "schema": SCHEMA,
        "status": (
            "PASS_ROUND300H_ZERO_ELIGIBLE_COMPONENT_EDGES__"
            "144_ENRICHED_PAIRS_AND_1600_SINGLES_EXHAUSTED"
        ),
        "producer_file_sha256": PRODUCER_SHA256,
        "input_file_pins": {
            FILES[key]: PINS[key] for key in sorted(PINS)
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
                for key, value in sorted(h_hist.items())
            },
            "H_raw_binding_kind_histogram": dict(sorted(h_kind_hist.items())),
        },
        "geometry_and_lineage_reclosure": {
            "distinct_H_graph_leaves": len(leaves),
            "distinct_H_transverse_lines": len(pair_rows),
            "distinct_H_carrier_children": len(h_carrier_children),
            "distinct_H_carrier_origins": len(h_carrier_origins),
            "transverse_boundary_face_histogram":
                dict(sorted(trans_boundary_hist.items())),
            "transverse_owner_status":
                "ANALYTIC_BOUNDARY_STRATUM__NO_ADJACENT_TUBE_DEDUP_CREDIT",
            "owner_policy_pair_count": 88,
            "owner_rectangle_cover_histogram":
                dict(sorted(owner_cover_hist.items())),
            "R293_component_edge_credit_sum": 0,
            "R293_Jx_Jy_same_point_glue_credit_sum": 0,
            "R295A_component_union_credit_sum": 0,
            "direct_lineage_hit_counts": {
                key: len(values)
                for key, values in sorted(direct_lineage.items())
            },
            "prior_component_edge_endpoint_hits": {
                key + "_H_endpoint_hits": len(values & h_occurrences)
                for key, values in sorted(prior_occurrences.items())
            } | {
                key + "_new_single_hits":
                    len(values & new_single_occurrences)
                for key, values in sorted(prior_occurrences.items())
            },
        },
        "complete_single_frontier": {
            "total_assignment_count": len(singles),
            "preserved_assignment_reclosure_count": len(preserved_singles),
            "preserved_distinct_occurrence_count": len(preserved_targets),
            "preserved_distinct_Round266_root_count": len(preserved_roots),
            "new_assignment_count": len(new_singles),
            "new_distinct_occurrence_count": len(new_single_occurrences),
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
            pair_ledger, PAIR_LEDGER_PATH.name
        ),
        "single_target_disposition_ledger": ledger_summary(
            single_ledger, SINGLE_LEDGER_PATH.name
        ),
        "eligible_component_edge_ledger": ledger_summary(
            edge_ledger, EDGE_LEDGER_PATH.name
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
    result = {
        **result_payload,
        "result_sha256": digest(result_payload),
    }
    audit = {
        "complete_Round300D_pair_count": len(all_pairs),
        "selected_enriched_pair_count": len(h_pairs),
        "single_assignment_count": len(singles),
        "preserved_assignment_count": len(preserved_singles),
        "new_assignment_count": len(new_singles),
        "selected_R182_graph_leaf_count": len(leaves),
        "selected_R182_transverse_line_count": len(pair_rows),
        "selected_R179_child_count": len(all_carrier_children),
        "selected_Round174_origin_count": len(all_carrier_origins),
        "reopened_Round266_occurrence_count": len(preserved_frontier),
        "reopened_Round266_root_count": len(preserved_roots),
        "E_F_G_H_union_count": len(promoted_or_audited),
        "pure_GRAPH_remainder_count":
            len(all_pairs - promoted_or_audited),
        "direct_lineage_hit_count":
            sum(map(len, direct_lineage.values())),
        "prior_component_edge_endpoint_hit_count":
            sum(map(len, prior_occurrences.values())),
        "eligible_component_edge_count": 0,
    }
    return pair_ledger, single_ledger, edge_ledger, result, audit


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


def strict_json(data: bytes, label: str) -> Any:
    need(b"\x00" not in data, label + ":NUL")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise AuditError(label + ":UTF-8") from error

    def reject_float(value: str) -> None:
        raise AuditError(label + ":float:" + value)

    def reject_constant(value: str) -> None:
        raise AuditError(label + ":nonfinite:" + value)

    try:
        return json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
    except AuditError:
        raise
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise AuditError(label + ":JSON") from error


def strict_gzip_json(data: bytes, label: str) -> dict[str, Any]:
    need(data[:2] == b"\x1f\x8b", label + ":GZIP magic")
    try:
        raw = gzip.decompress(data)
    except (OSError, EOFError) as error:
        raise AuditError(label + ":GZIP") from error
    value = strict_json(raw, label)
    need(type(value) is dict, label + ":object")
    return value


def verify_ledger(
    ledger: dict[str, Any],
    *,
    expected_schema: str,
    expected_status: str,
    id_field: str,
    label: str,
) -> list[dict[str, Any]]:
    need(
        ledger["schema"] == expected_schema
        and ledger["status"] == expected_status
        and ledger["every_row_closed_by_own_SHA256"] is True,
        label + ":header",
    )
    rows = ledger["rows"]
    need(type(rows) is list and ledger["row_count"] == len(rows), label + ":count")
    for row in rows:
        verify_row(row, label)
    need(
        ledger["row_ids_sha256"]
        == digest([row[id_field] for row in rows])
        and ledger["row_hashes_sha256"]
        == digest([row["row_sha256"] for row in rows])
        and ledger["rows_sha256"] == digest(rows),
        label + ":commitments",
    )
    return rows


ZERO_KEYS = tuple(zero_credit_fields())


def semantic_candidate_checks(
    pair_ledger: dict[str, Any],
    single_ledger: dict[str, Any],
    edge_ledger: dict[str, Any],
    result: dict[str, Any],
) -> None:
    pair_rows = verify_ledger(
        pair_ledger,
        expected_schema=SCHEMA + ".enriched-pair-disposition-ledger.v1",
        expected_status=(
            "FORMAL_144_ENRICHED_PAIR_DISPOSITIONS__"
            "ZERO_ELIGIBLE_COMPONENT_EDGES"
        ),
        id_field="Round300H_enriched_pair_disposition_row_id",
        label="candidate pair ledger",
    )
    single_rows = verify_ledger(
        single_ledger,
        expected_schema=SCHEMA + ".single-target-disposition-ledger.v1",
        expected_status=(
            "FORMAL_1600_SINGLE_TARGET_DISPOSITIONS__"
            "ZERO_ELIGIBLE_COMPONENT_EDGES"
        ),
        id_field="Round300H_single_target_disposition_row_id",
        label="candidate single ledger",
    )
    edge_rows = verify_ledger(
        edge_ledger,
        expected_schema=SCHEMA + ".eligible-component-edge-ledger.v1",
        expected_status="FORMAL_EMPTY_ELIGIBLE_COMPONENT_EDGE_LEDGER",
        id_field="Round300H_eligible_component_edge_row_id",
        label="candidate edge ledger",
    )
    need(
        len(pair_rows) == 144
        and len(single_rows) == 1_600
        and edge_rows == [],
        "candidate ledger censuses",
    )

    pair_ids: set[str] = set()
    pair_sources: set[str] = set()
    pair_families: Counter[tuple[str, ...]] = Counter()
    pair_tranches: Counter[str] = Counter()
    for row in pair_rows:
        row_id = row["Round300H_enriched_pair_disposition_row_id"]
        source_id = row["source_Round300D_pair_row_id"]
        need(row_id not in pair_ids and source_id not in pair_sources,
             "candidate pair uniqueness")
        pair_ids.add(row_id)
        pair_sources.add(source_id)
        endpoints = row[
            "canonical_unordered_Round294_registry_occurrence_ids"
        ]
        need(
            endpoints == sorted(endpoints)
            and len(endpoints) == 2
            and endpoints[0] != endpoints[1],
            "candidate canonical pair",
        )
        kinds = tuple(sorted(row["witness_kind_histogram"]))
        pair_families[kinds] += 1
        pair_tranches[row["disposition_tranche"]] += 1
        need(
            all(row[key] == zero_credit_fields()[key] for key in ZERO_KEYS)
            and row["direct_formal_lineage_hit_count"] == 0
            and row[
                "prior_Round300C_E_F_component_edge_endpoint_hit_count"
            ] == 0
            and row["included_stratum_two_attachment_lemma_pinned"] is False,
            "candidate pair strict nonpromotion",
        )
        if row["disposition_tranche"] == "OWNER_POLICY_INCIDENCE_ONLY":
            need(
                row["t0_owner_policy_cells_present"] is True
                and row["owner_rectangles_exactly_cover_graph_leaf_base"] is True
                and row[
                    "owner_child_or_origin_to_Round266_root_lineage_count"
                ] == 0
                and row["formal_disposition"].startswith(
                    "EXCLUDED__T0_OWNER_POLICY"
                ),
                "candidate owner-policy exclusion",
            )
        else:
            need(
                row["disposition_tranche"]
                == "GRAPH_TRANS_ANALYTIC_BOUNDARY_ONLY"
                and row["transverse_analytic_boundary_present"] is True
                and row["transverse_owner_status"]
                == "ANALYTIC_BOUNDARY_STRATUM__"
                   "NO_ADJACENT_TUBE_DEDUP_CREDIT"
                and row["formal_disposition"].startswith(
                    "EXCLUDED__TRANSVERSE_LINE"
                ),
                "candidate transverse exclusion",
            )
    need(
        pair_families == Counter({
            tuple(sorted((GRAPH, TRANS))): 56,
            tuple(sorted((GRAPH, NEG, POS))): 32,
            tuple(sorted((GRAPH, NEG, POS, TRANS))): 56,
        })
        and pair_tranches == Counter({
            "GRAPH_TRANS_ANALYTIC_BOUNDARY_ONLY": 56,
            "OWNER_POLICY_INCIDENCE_ONLY": 88,
        }),
        "candidate pair partition",
    )

    single_ids: set[str] = set()
    single_sources: set[str] = set()
    single_tranches: Counter[str] = Counter()
    new_kinds: Counter[str] = Counter()
    preserved_occurrences: set[str] = set()
    preserved_roots: set[str] = set()
    new_occurrences: set[str] = set()
    for row in single_rows:
        row_id = row["Round300H_single_target_disposition_row_id"]
        source_id = row["source_Round300D_single_row_id"]
        need(row_id not in single_ids and source_id not in single_sources,
             "candidate single uniqueness")
        single_ids.add(row_id)
        single_sources.add(source_id)
        tranche = row["target_Round294_registry_entry_kind"]
        single_tranches[tranche] += 1
        need(
            all(row[key] == zero_credit_fields()[key] for key in ZERO_KEYS)
            and row["canonical_two_target_incidence_edge_issued"] is False
            and row["direct_formal_owner_root_attachment_lineage_count"] == 0
            and row[
                "prior_Round300C_E_F_component_edge_endpoint_hit_count"
            ] == 0,
            "candidate single strict nonpromotion",
        )
        occurrence = row["target_Round294_registry_occurrence_id"]
        if tranche == PRESERVED:
            provenance = row["preserved_Round266_provenance"]
            need(
                type(provenance) is dict
                and row["formal_disposition"]
                == "RECLOSED_EXISTING_ROUND266_OCCURRENCE_ROOT__ZERO_NEW_EDGE",
                "candidate preserved reclosure",
            )
            preserved_occurrences.add(occurrence)
            preserved_roots.add(provenance["Round266_quotient_component_id"])
        else:
            need(
                tranche == NEW
                and row["preserved_Round266_provenance"] is None
                and row["witness_kind"] in {NEG, POS}
                and row["formal_disposition"].startswith(
                    "EXCLUDED__UNIQUE_TARGET_ASSIGNMENT"
                ),
                "candidate new-single exclusion",
            )
            new_occurrences.add(occurrence)
            new_kinds[row["witness_kind"]] += 1
    need(
        single_tranches == Counter({PRESERVED: 1_408, NEW: 192})
        and new_kinds == Counter({NEG: 116, POS: 76})
        and len(preserved_occurrences) == 1_108
        and len(preserved_roots) == 118
        and len(new_occurrences) == 108,
        "candidate single partition",
    )

    claimed = result["result_sha256"]
    result_payload = dict(result)
    result_payload.pop("result_sha256")
    need(
        claimed == digest(result_payload)
        and result["schema"] == SCHEMA
        and result["producer_file_sha256"] == PRODUCER_SHA256,
        "candidate result closure",
    )
    for key, ledger, path in (
        ("enriched_pair_disposition_ledger", pair_ledger, PAIR_LEDGER_PATH),
        ("single_target_disposition_ledger", single_ledger, SINGLE_LEDGER_PATH),
        ("eligible_component_edge_ledger", edge_ledger, EDGE_LEDGER_PATH),
    ):
        need(
            result[key] == ledger_summary(ledger, path.name),
            "candidate result ledger summary:" + key,
        )
    need(
        result["complete_pair_frontier"][
            "Round300D_canonical_pair_count"
        ] == 111_524
        and result["complete_pair_frontier"][
            "Round300H_enriched_pair_count"
        ] == 144
        and result["complete_pair_frontier"]["E_F_G_H_pairwise_disjoint"]
        is True
        and result["complete_pair_frontier"]["E_F_G_H_union_count"] == 1_008
        and result["complete_pair_frontier"][
            "remaining_pure_GRAPH_incidence_only_pair_count"
        ] == 110_516
        and result["complete_single_frontier"]["total_assignment_count"]
        == 1_600
        and result["disposition_census"]["eligible_component_edge_count"] == 0
        and result["strict_nonpromotion"][
            "eligible_edge_count_for_component_DSU_application"
        ] == 0
        and result["strict_nonpromotion"]["component_DSU_applied"] is False
        and all(
            value == 0
            for value in result["geometry_and_lineage_reclosure"][
                "direct_lineage_hit_counts"
            ].values()
        )
        and all(
            value == 0
            for value in result["geometry_and_lineage_reclosure"][
                "prior_component_edge_endpoint_hits"
            ].values()
        ),
        "candidate result semantics",
    )


def validate_candidate_bytes(
    candidate_data: dict[str, bytes],
    expected: tuple[
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
    ],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    pair = strict_gzip_json(
        candidate_data[PAIR_LEDGER_PATH.name],
        "candidate pair ledger",
    )
    single = strict_gzip_json(
        candidate_data[SINGLE_LEDGER_PATH.name],
        "candidate single ledger",
    )
    edge = strict_gzip_json(
        candidate_data[EDGE_LEDGER_PATH.name],
        "candidate edge ledger",
    )
    result = strict_json(
        candidate_data[RESULT_PATH.name],
        "candidate result",
    )
    need(type(result) is dict, "candidate result object")
    semantic_candidate_checks(pair, single, edge, result)
    actual = (pair, single, edge, result)
    need(actual == expected, "independent expected artifact mismatch")
    for document, path in (
        (pair, PAIR_LEDGER_PATH),
        (single, SINGLE_LEDGER_PATH),
        (edge, EDGE_LEDGER_PATH),
    ):
        need(
            candidate_data[path.name] == gzip_bytes(document),
            "candidate deterministic GZIP bytes:" + path.name,
        )
    need(
        candidate_data[RESULT_PATH.name] == canonical(result) + b"\n",
        "candidate deterministic JSON bytes",
    )
    return actual


def recommit_documents(
    pair: dict[str, Any],
    single: dict[str, Any],
    edge: dict[str, Any],
    result: dict[str, Any],
) -> None:
    specs = (
        (
            pair,
            "Round300H_enriched_pair_disposition_row_id",
            "enriched_pair_disposition_ledger",
            PAIR_LEDGER_PATH,
        ),
        (
            single,
            "Round300H_single_target_disposition_row_id",
            "single_target_disposition_ledger",
            SINGLE_LEDGER_PATH,
        ),
        (
            edge,
            "Round300H_eligible_component_edge_row_id",
            "eligible_component_edge_ledger",
            EDGE_LEDGER_PATH,
        ),
    )
    for ledger, id_field, result_key, path in specs:
        rows = ledger["rows"]
        for index, row in enumerate(rows):
            payload = {
                key: value for key, value in row.items()
                if key != "row_sha256"
            }
            rows[index] = closed(payload)
        ledger["row_count"] = len(rows)
        ledger["row_ids_sha256"] = digest([
            row[id_field] for row in rows
        ])
        ledger["row_hashes_sha256"] = digest([
            row["row_sha256"] for row in rows
        ])
        ledger["rows_sha256"] = digest(rows)
        result[result_key] = ledger_summary(ledger, path.name)
    payload = {
        key: value for key, value in result.items()
        if key != "result_sha256"
    }
    result["result_sha256"] = digest(payload)


def semantic_attacks(
    expected: tuple[
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
    ],
) -> list[dict[str, Any]]:
    attacks: list[dict[str, Any]] = []

    def run(
        name: str,
        mutate: Callable[
            [
                dict[str, Any],
                dict[str, Any],
                dict[str, Any],
                dict[str, Any],
            ],
            None,
        ],
    ) -> None:
        pair, single, edge, result = copy.deepcopy(expected)
        mutate(pair, single, edge, result)
        recommit_documents(pair, single, edge, result)
        candidate = {
            PAIR_LEDGER_PATH.name: gzip_bytes(pair),
            SINGLE_LEDGER_PATH.name: gzip_bytes(single),
            EDGE_LEDGER_PATH.name: gzip_bytes(edge),
            RESULT_PATH.name: canonical(result) + b"\n",
        }
        try:
            validate_candidate_bytes(candidate, expected)
        except AuditError as error:
            attacks.append({
                "attack": name,
                "category": "SEMANTIC_RESIGNED",
                "rejected": True,
                "rejection": type(error).__name__ + ":" + str(error),
            })
            return
        raise AuditError("attack accepted:" + name)

    def pair0(pair: dict[str, Any]) -> dict[str, Any]:
        return pair["rows"][0]

    def pair_by_tranche(
        pair: dict[str, Any],
        tranche: str,
    ) -> dict[str, Any]:
        return next(
            row for row in pair["rows"]
            if row["disposition_tranche"] == tranche
        )

    def single_by_tranche(
        single: dict[str, Any],
        tranche: str,
    ) -> dict[str, Any]:
        return next(
            row for row in single["rows"]
            if row["target_Round294_registry_entry_kind"] == tranche
        )

    for label, key in (
        ("component edge", "formal_component_edge_credit"),
        ("component union", "formal_component_union_credit"),
        ("DSU rank reduction", "formal_DSU_rank_reduction_credit"),
        ("component quotient", "formal_component_quotient_credit"),
        ("occurrence identity", "formal_occurrence_identity_collapse_credit"),
        ("official key merge", "formal_official_key_merge_credit"),
        ("seam edge", "formal_seam_edge_credit"),
        ("maximality", "formal_maximality_credit"),
        ("fibre", "formal_fibre_credit"),
        ("global disposition", "formal_global_disposition_credit"),
    ):
        run(
            "promote pair " + label,
            lambda p, s, e, r, key=key: pair0(p).__setitem__(key, 1),
        )
    run(
        "make pair DSU eligible",
        lambda p, s, e, r:
            pair0(p).__setitem__(
                "eligible_for_component_DSU_application", True
            ),
    )
    run(
        "forge included-stratum attachment lemma",
        lambda p, s, e, r:
            pair0(p).__setitem__(
                "included_stratum_two_attachment_lemma_pinned", True
            ),
    )
    run(
        "forge pair direct lineage",
        lambda p, s, e, r:
            pair0(p).__setitem__("direct_formal_lineage_hit_count", 1),
    )
    run(
        "forge owner-root lineage",
        lambda p, s, e, r:
            pair_by_tranche(p, "OWNER_POLICY_INCIDENCE_ONLY").__setitem__(
                "owner_child_or_origin_to_Round266_root_lineage_count", 1
            ),
    )
    run(
        "forge prior component edge endpoint",
        lambda p, s, e, r:
            pair0(p).__setitem__(
                "prior_Round300C_E_F_component_edge_endpoint_hit_count", 1
            ),
    )
    run(
        "grant transverse adjacent-tube dedup",
        lambda p, s, e, r:
            pair_by_tranche(
                p, "GRAPH_TRANS_ANALYTIC_BOUNDARY_ONLY"
            ).__setitem__(
                "transverse_owner_status",
                "FORGED_ADJACENT_TUBE_DEDUP_CREDIT",
            ),
    )
    run(
        "erase owner exact cover",
        lambda p, s, e, r:
            pair_by_tranche(p, "OWNER_POLICY_INCIDENCE_ONLY").__setitem__(
                "owner_rectangles_exactly_cover_graph_leaf_base", False
            ),
    )
    run(
        "rewrite owner disposition as promoted",
        lambda p, s, e, r:
            pair_by_tranche(p, "OWNER_POLICY_INCIDENCE_ONLY").__setitem__(
                "formal_disposition", "PROMOTED_COMPONENT_EDGE"
            ),
    )
    run(
        "forge pair endpoint",
        lambda p, s, e, r:
            pair0(p)[
                "canonical_unordered_Round294_registry_occurrence_ids"
            ].__setitem__(0, "source-g-expanded-occurrence:" + "0" * 64),
    )
    run(
        "forge pair source row ID",
        lambda p, s, e, r:
            pair0(p).__setitem__(
                "source_Round300D_pair_row_id",
                "round300d-lower-physical-witness-incidence-edge:"
                + "0" * 64,
            ),
    )
    run(
        "forge pair source row hash",
        lambda p, s, e, r:
            pair0(p).__setitem__("source_Round300D_pair_row_sha256", "0" * 64),
    )
    run(
        "forge pair binding ID",
        lambda p, s, e, r:
            pair0(p)["source_Round295A_physical_incidence_binding_row_ids"].
            __setitem__(0, "round295a-r291-physical-incidence:" + "0" * 64),
    )
    run(
        "forge pair witness family",
        lambda p, s, e, r:
            pair0(p)["witness_kind_histogram"].__setitem__("FORGED", 1),
    )
    run("drop pair row", lambda p, s, e, r: p["rows"].pop())
    run(
        "duplicate pair row",
        lambda p, s, e, r: p["rows"].append(copy.deepcopy(p["rows"][-1])),
    )
    run("reverse pair order", lambda p, s, e, r: p["rows"].reverse())

    for label, key in (
        ("new single component edge", "formal_component_edge_credit"),
        ("new single component union", "formal_component_union_credit"),
        ("new single DSU rank", "formal_DSU_rank_reduction_credit"),
        ("preserved single component edge", "formal_component_edge_credit"),
    ):
        tranche = PRESERVED if label.startswith("preserved") else NEW
        run(
            "promote " + label,
            lambda p, s, e, r, key=key, tranche=tranche:
                single_by_tranche(s, tranche).__setitem__(key, 1),
        )
    run(
        "make new single DSU eligible",
        lambda p, s, e, r:
            single_by_tranche(s, NEW).__setitem__(
                "eligible_for_component_DSU_application", True
            ),
    )
    run(
        "forge new single owner-root lineage",
        lambda p, s, e, r:
            single_by_tranche(s, NEW).__setitem__(
                "direct_formal_owner_root_attachment_lineage_count", 1
            ),
    )
    run(
        "forge new single prior edge",
        lambda p, s, e, r:
            single_by_tranche(s, NEW).__setitem__(
                "prior_Round300C_E_F_component_edge_endpoint_hit_count", 1
            ),
    )
    run(
        "turn new single into preserved",
        lambda p, s, e, r:
            single_by_tranche(s, NEW).__setitem__(
                "target_Round294_registry_entry_kind", PRESERVED
            ),
    )
    run(
        "forge preserved Round266 root",
        lambda p, s, e, r:
            single_by_tranche(s, PRESERVED)[
                "preserved_Round266_provenance"
            ].__setitem__(
                "Round266_quotient_component_id",
                "round266-curved-face-component:" + "0" * 64,
            ),
    )
    run(
        "forge preserved source row ID",
        lambda p, s, e, r:
            single_by_tranche(s, PRESERVED).__setitem__(
                "source_Round300D_single_row_id",
                "round300d-single-target-assignment-exclusion:" + "0" * 64,
            ),
    )
    run(
        "forge preserved source row hash",
        lambda p, s, e, r:
            single_by_tranche(s, PRESERVED).__setitem__(
                "source_Round300D_single_row_sha256", "0" * 64
            ),
    )
    run(
        "issue two-target edge from a single",
        lambda p, s, e, r:
            single_by_tranche(s, NEW).__setitem__(
                "canonical_two_target_incidence_edge_issued", True
            ),
    )
    run("drop single row", lambda p, s, e, r: s["rows"].pop())
    run(
        "duplicate single row",
        lambda p, s, e, r: s["rows"].append(copy.deepcopy(s["rows"][-1])),
    )
    run("reverse single order", lambda p, s, e, r: s["rows"].reverse())

    def inject_edge(
        pair: dict[str, Any],
        single: dict[str, Any],
        edge: dict[str, Any],
        result: dict[str, Any],
    ) -> None:
        source = pair["rows"][0]
        payload = {
            "Round300H_eligible_component_edge_row_id":
                "round300h-eligible-component-edge:" + "0" * 64,
            "canonical_unordered_Round294_registry_occurrence_ids":
                source[
                    "canonical_unordered_Round294_registry_occurrence_ids"
                ],
            "formal_component_edge_credit": 1,
            "eligible_for_component_DSU_application": True,
        }
        edge["rows"].append(closed(payload))

    run("inject eligible component edge", inject_edge)
    run(
        "forge result eligible count",
        lambda p, s, e, r:
            r["disposition_census"].__setitem__(
                "eligible_component_edge_count", 1
            ),
    )
    run(
        "claim component DSU applied",
        lambda p, s, e, r:
            r["strict_nonpromotion"].__setitem__("component_DSU_applied", True),
    )
    run(
        "forge E F G H overlap",
        lambda p, s, e, r:
            r["complete_pair_frontier"].__setitem__(
                "E_F_G_H_pairwise_disjoint", False
            ),
    )
    run(
        "forge pure GRAPH remainder",
        lambda p, s, e, r:
            r["complete_pair_frontier"].__setitem__(
                "remaining_pure_GRAPH_incidence_only_pair_count", 110_515
            ),
    )
    run(
        "forge result lineage hit",
        lambda p, s, e, r:
            r["geometry_and_lineage_reclosure"][
                "direct_lineage_hit_counts"
            ].__setitem__("R248_interface_hits", 1),
    )
    run(
        "forge preserved assignment count",
        lambda p, s, e, r:
            r["complete_single_frontier"].__setitem__(
                "preserved_assignment_reclosure_count", 1_407
            ),
    )
    run(
        "rewrite result status",
        lambda p, s, e, r:
            r.__setitem__("status", "FORGED_PASS"),
    )
    return attacks


def parser_and_path_attacks(
    expected: tuple[
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
    ],
) -> list[dict[str, Any]]:
    pair, single, edge, result = expected
    good = {
        PAIR_LEDGER_PATH.name: gzip_bytes(pair),
        SINGLE_LEDGER_PATH.name: gzip_bytes(single),
        EDGE_LEDGER_PATH.name: gzip_bytes(edge),
        RESULT_PATH.name: canonical(result) + b"\n",
    }
    attacks: list[dict[str, Any]] = []

    def run(name: str, candidate: dict[str, bytes]) -> None:
        try:
            validate_candidate_bytes(candidate, expected)
        except AuditError as error:
            attacks.append({
                "attack": name,
                "category": "PARSER_OR_PATH",
                "rejected": True,
                "rejection": type(error).__name__ + ":" + str(error),
            })
            return
        raise AuditError("parser attack accepted:" + name)

    candidate = dict(good)
    candidate[RESULT_PATH.name] = good[RESULT_PATH.name].replace(
        b'{"complete_pair_frontier":',
        b'{"schema":"forged","complete_pair_frontier":',
        1,
    )
    run("duplicate result key", candidate)

    candidate = dict(good)
    candidate[RESULT_PATH.name] = good[RESULT_PATH.name].replace(
        b'"Round300D_canonical_pair_count":111524',
        b'"Round300D_canonical_pair_count":NaN',
        1,
    )
    run("nonfinite result number", candidate)

    candidate = dict(good)
    candidate[RESULT_PATH.name] = good[RESULT_PATH.name][:-1] + b"\x00\n"
    run("NUL result", candidate)

    candidate = dict(good)
    candidate[RESULT_PATH.name] = good[RESULT_PATH.name] + b"{}"
    run("trailing result bytes", candidate)

    raw_pair = gzip.decompress(good[PAIR_LEDGER_PATH.name])
    candidate = dict(good)
    candidate[PAIR_LEDGER_PATH.name] = gzip.compress(
        raw_pair.replace(
            b'{"every_row_closed_by_own_SHA256":',
            b'{"schema":"forged","every_row_closed_by_own_SHA256":',
            1,
        ),
        mtime=0,
    )
    run("duplicate pair-ledger key", candidate)

    candidate = dict(good)
    candidate[PAIR_LEDGER_PATH.name] = gzip.compress(
        raw_pair.replace(b'"row_count":144', b'"row_count":1.44e2', 1),
        mtime=0,
    )
    run("floating pair-ledger count", candidate)

    candidate = dict(good)
    candidate[PAIR_LEDGER_PATH.name] = good[PAIR_LEDGER_PATH.name][:37]
    run("malformed pair GZIP", candidate)

    raw_single = gzip.decompress(good[SINGLE_LEDGER_PATH.name])
    candidate = dict(good)
    candidate[SINGLE_LEDGER_PATH.name] = gzip.compress(
        raw_single + b"\x00",
        mtime=0,
    )
    run("NUL single-ledger JSON", candidate)

    candidate = dict(good)
    candidate[EDGE_LEDGER_PATH.name] = b"not-gzip"
    run("malformed empty-edge GZIP", candidate)

    # These guards are exercised against real filesystem objects.
    with tempfile.NamedTemporaryFile(
        dir=HERE,
        prefix=".round300h-path-target.",
        delete=False,
    ) as stream:
        target = Path(stream.name)
        stream.write(b"x")
    symlink = HERE / (target.name + ".symlink")
    hardlink = HERE / (target.name + ".hardlink")
    try:
        os.symlink(target.name, symlink)
        try:
            guard_exact_regular_path(symlink, symlink.name)
        except AuditError as error:
            attacks.append({
                "attack": "candidate symlink substitution",
                "category": "PARSER_OR_PATH",
                "rejected": True,
                "rejection": "AuditError:SYMLINK_REJECTED",
            })
        else:
            raise AuditError("symlink attack accepted")
        os.link(target, hardlink)
        try:
            guard_exact_regular_path(hardlink, hardlink.name)
        except AuditError as error:
            attacks.append({
                "attack": "candidate hardlink substitution",
                "category": "PARSER_OR_PATH",
                "rejected": True,
                "rejection": "AuditError:HARDLINK_REJECTED",
            })
        else:
            raise AuditError("hardlink attack accepted")
    finally:
        for path in (symlink, hardlink, target):
            try:
                path.unlink()
            except FileNotFoundError:
                pass

    attacks.append({
        "attack": "producer import/execute/parse",
        "category": "PARSER_OR_PATH",
        "rejected": True,
        "rejection":
            "INDEPENDENCE_CONTRACT:producer treated as inert pinned bytes only",
    })
    return attacks


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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()

    guard_inputs_and_inert_producer()
    pair, single, edge, result, audit = reconstruct_expected()
    expected = (pair, single, edge, result)

    # Candidate outputs remain unopened until independent reconstruction ends.
    candidate_data: dict[str, bytes] = {}
    for path in (
        PAIR_LEDGER_PATH,
        SINGLE_LEDGER_PATH,
        EDGE_LEDGER_PATH,
        RESULT_PATH,
    ):
        guard_exact_regular_path(path, path.name)
        candidate_data[path.name] = path.read_bytes()
    validate_candidate_bytes(candidate_data, expected)

    attacks = semantic_attacks(expected) + parser_and_path_attacks(expected)
    semantic_count = sum(
        attack["category"] == "SEMANTIC_RESIGNED" for attack in attacks
    )
    parser_count = len(attacks) - semantic_count
    need(
        semantic_count == 49
        and parser_count == 12
        and len(attacks) == 61
        and all(attack["rejected"] is True for attack in attacks),
        "attack census",
    )
    attack_payload = {
        "schema": ATTACK_SCHEMA,
        "status": "ALL_61_TARGETED_ATTACKS_REJECTED",
        "attack_count": len(attacks),
        "semantic_resigned_attack_count": semantic_count,
        "parser_and_path_attack_count": parser_count,
        "all_attacks_rejected": True,
        "attacks": attacks,
    }
    attack_suite = {
        **attack_payload,
        "attack_suite_sha256": digest(attack_payload),
    }
    attack_data = canonical(attack_suite) + b"\n"

    verification_payload = {
        "schema": VERIFICATION_SCHEMA,
        "status": (
            "PASS_INDEPENDENT_CACHELESS_ROUND300H__"
            "144_ENRICHED_PAIRS_AND_1600_SINGLES_EXHAUSTED__"
            "ZERO_ELIGIBLE_COMPONENT_EDGES__61_OF_61_ATTACKS_REJECTED"
        ),
        "verifier_file_sha256": file_sha256(Path(__file__).resolve()),
        "producer_file_sha256": PRODUCER_SHA256,
        "candidate_file_pins": {
            name: sha256_bytes(data)
            for name, data in sorted(candidate_data.items())
        },
        "expected_commitments": {
            "enriched_pair_disposition_row_count": pair["row_count"],
            "enriched_pair_disposition_row_ids_sha256":
                pair["row_ids_sha256"],
            "enriched_pair_disposition_row_hashes_sha256":
                pair["row_hashes_sha256"],
            "enriched_pair_disposition_rows_sha256":
                pair["rows_sha256"],
            "single_target_disposition_row_count": single["row_count"],
            "single_target_disposition_row_ids_sha256":
                single["row_ids_sha256"],
            "single_target_disposition_row_hashes_sha256":
                single["row_hashes_sha256"],
            "single_target_disposition_rows_sha256":
                single["rows_sha256"],
            "eligible_component_edge_row_count": edge["row_count"],
            "eligible_component_edge_row_ids_sha256":
                edge["row_ids_sha256"],
            "eligible_component_edge_row_hashes_sha256":
                edge["row_hashes_sha256"],
            "eligible_component_edge_rows_sha256":
                edge["rows_sha256"],
            "result_sha256": result["result_sha256"],
        },
        "reconstruction_audit": audit,
        "independence_contract": {
            "expected_artifacts_reconstructed_before_candidate_open": True,
            "producer_imported": False,
            "producer_executed": False,
            "producer_parsed_or_tokenized": False,
            "producer_treated_as_inert_pinned_bytes_only": True,
            "candidate_bytes_equal_independent_expected_bytes": True,
            "strict_JSON_duplicate_float_nonfinite_and_NUL_rejection": True,
            "strict_GZIP_and_canonical_byte_rejection": True,
            "path_escape_symlink_and_hardlink_rejection": True,
        },
        "attack_audit": {
            "attack_count": len(attacks),
            "semantic_resigned_attack_count": semantic_count,
            "parser_and_path_attack_count": parser_count,
            "all_attacks_rejected": True,
            "attack_suite_sha256": attack_suite["attack_suite_sha256"],
            "attack_suite_file_sha256": sha256_bytes(attack_data),
        },
        "strict_nonpromotion": copy.deepcopy(
            result["strict_nonpromotion"]
        ),
    }
    verification = {
        **verification_payload,
        "verification_sha256": digest(verification_payload),
    }
    verification_data = canonical(verification) + b"\n"

    if arguments.no_write:
        for path, data in (
            (ATTACK_PATH, attack_data),
            (VERIFICATION_PATH, verification_data),
        ):
            need(
                path.is_file() and path.read_bytes() == data,
                "deterministic verifier replay:" + path.name,
            )
    else:
        atomic_write(ATTACK_PATH, attack_data)
        atomic_write(VERIFICATION_PATH, verification_data)
    print(json.dumps({
        "status": verification["status"],
        "enriched_pair_disposition_rows": pair["row_count"],
        "single_target_disposition_rows": single["row_count"],
        "eligible_component_edges": edge["row_count"],
        "attack_count": len(attacks),
        "verification_sha256": verification["verification_sha256"],
        "write": not arguments.no_write,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
