#!/usr/bin/env python3
"""Construct the revised Source-G occurrence-registry candidate.

This is a deterministic, fail-closed registry *candidate* builder.  It
preserves the 126,468 Round266 occurrence IDs, carries forward the 295,336
Round288 reserved canonical-atom IDs, and gives new conditional IDs only to
the 9,404 exact (t^2,p,s)-refined Round287 support components that survive the
Round292 existing-registry overlap probe.

The naive 10,020 Round287-union issuance is deliberately rejected: 920 source
unions have positive-volume overlap with the preserved Round174/Round179
frontier.  Exact refinement leaves 9,404 connected uncovered supports and
1,600 occupied representation-subcover cells.  Those 1,600 cells are alias
bindings, not occurrences.

No full promotion is performed here.  Every new ID, alias, component, DSU,
seam, Jx/Jy, maximality, fibre, and disposition credit remains zero.  The
output is WAITING_OVERLAP_AUDIT because the consumed overlap probe is not yet
an independently frozen promoting artifact and this producer is not its
independent verifier.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gc
import gzip
import hashlib
import io
import json
import mmap
from pathlib import Path
import re
import tempfile
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round292_source_g_occurrence_registry_candidate_construction"
DEFAULT_REGISTRY_LEDGER = HERE / f"{PREFIX}_registry_ledger.json.gz"
DEFAULT_ALIAS_LEDGER = HERE / f"{PREFIX}_alias_ledger.json.gz"
DEFAULT_RESULT = HERE / f"{PREFIX}_result.json"

SCHEMA = "cm2.round292.source-g-occurrence-registry-candidate-construction.v2"
REGISTRY_LEDGER_SCHEMA = (
    "cm2.round292.source-g-occurrence-registry-candidate-ledger.v2"
)
ALIAS_LEDGER_SCHEMA = (
    "cm2.round292.source-g-occurrence-alias-binding-candidate-ledger.v2"
)

WAITING = "WAITING_OVERLAP_AUDIT"

R266_CERTIFICATE = (
    "cm2_round266_source_g_expanded_curved_face_closure_certificate.json"
)
R266_VERIFICATION = (
    "cm2_round266_source_g_expanded_curved_face_closure_verification.json"
)
R266_MANIFEST = (
    "cm2_round266_source_g_expanded_curved_face_closure_manifest.sha256"
)

R287_RESULT = (
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_"
    "result.json"
)
R287_LEDGER = (
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_"
    "ledger.json.gz"
)
R287_VERIFICATION = (
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_"
    "verification.json"
)
R287_MANIFEST = (
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_"
    "manifest.sha256"
)

R288_RESULT = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_"
    "result.json"
)
R288_ATOMS = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_"
    "atom_dispositions.json.gz"
)
R288_OVERLAPS = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_"
    "existing_overlap_relations.json.gz"
)
R288_VERIFICATION = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_"
    "verification.json"
)
R288_MANIFEST = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_"
    "manifest.sha256"
)

R290_RESULT = (
    "cm2_round290_source_g_isolated_atom_inner_support_closure_result.json"
)
R290_LEDGER = (
    "cm2_round290_source_g_isolated_atom_inner_support_closure_"
    "inner_support_ledger.json.gz"
)
R290_VERIFICATION = (
    "cm2_round290_source_g_isolated_atom_inner_support_closure_"
    "verification.json"
)
R290_MANIFEST = (
    "cm2_round290_source_g_isolated_atom_inner_support_closure_"
    "manifest.sha256"
)

OVERLAP_PROBE_RESULT = (
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_result.json"
)
OVERLAP_PROBE_LEDGER = (
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz"
)


INPUT_SHA256 = {
    R266_CERTIFICATE:
        "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf",
    R266_VERIFICATION:
        "a6436c716cbbe74f0195e2d87f4084a28ca2a2e27b9fe5eeb98b6835df92b75b",
    R266_MANIFEST:
        "63fb5b25d52ca5de579256499629d04d15f6a313e0a73f7e80fcb463385cbe09",
    R287_RESULT:
        "1265475e5d27f99eda35b16f13ba342e0d270ca1bc064df215a018d3ffae89f9",
    R287_LEDGER:
        "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a",
    R287_VERIFICATION:
        "c0ad4d3e229a1e21cb5b4f4144575df7f5eaf88d7fc8a6960967ab4c1db515a3",
    R287_MANIFEST:
        "85a9d4fcf9d9931a0e352eeef7582347b12325b92ffc78f2ee40c77c58093751",
    R288_RESULT:
        "9b5875777f3937efe05a4d871a8c8b76c92ca69d0f636eb014542f59dfe49569",
    R288_ATOMS:
        "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a",
    R288_OVERLAPS:
        "d76d27c436735511dc34056d9237a2772decd30129e3019b74c5a02a118ab24e",
    R288_VERIFICATION:
        "f08749d2f90ea63a696c482a342489c12e2c86436734a59c6a2e2b79d9cf9b23",
    R288_MANIFEST:
        "c15e4657051318f1a4e6aadcf80fa679840969c7f2c776e65460ac05cc2eb1eb",
    R290_RESULT:
        "1c2412da9fd28f6838eab1abb3b3e70773a4ca4f0ea28fafcda8c8342e881d59",
    R290_LEDGER:
        "9c2a596f3b981d24baa039e02c72e5270889d145dc146963532f3dedebc94025",
    R290_VERIFICATION:
        "94a8b1a3a0274bfb14d6f9e9b00d896673792548220e309b0211f2f2e3367b51",
    R290_MANIFEST:
        "e4e4b0614d810bb0516902e173ea7c816f1cecdea162d202ff058200b3d83189",
    OVERLAP_PROBE_RESULT:
        "f3887e75f4ef62459b75d8c77eee4781ec14f57651b4feb09b8d7ca8e372c508",
    OVERLAP_PROBE_LEDGER:
        "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
}


MANIFEST_SELECTIONS = {
    R266_MANIFEST: (R266_CERTIFICATE, R266_VERIFICATION),
    R287_MANIFEST: (R287_RESULT, R287_LEDGER, R287_VERIFICATION),
    R288_MANIFEST: (
        R288_RESULT,
        R288_ATOMS,
        R288_OVERLAPS,
        R288_VERIFICATION,
    ),
    R290_MANIFEST: (R290_RESULT, R290_LEDGER, R290_VERIFICATION),
}


ZERO_FIELDS = (
    "formal_new_expanded_occurrence_credit",
    "formal_occurrence_alias_credit",
    "formal_component_union_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_seam_edge_credit",
    "formal_Jx_Jy_same_point_glue_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)

R288_EXISTING_STATES = {
    "EXISTING_ROUND208_OCCURRENCE_ID_PRESERVED",
    "EXACT_ALIAS_OF_EXISTING_ROUND204_OCCURRENCE",
}
R288_READY_STATE = (
    "NEW_DISJOINT_PROMOTION_READY_CANDIDATE__"
    "ROUND279_STRICT_INWARD_CORRIDOR_INNER_SUPPORT__"
    "PENDING_INDEPENDENT_ROUND288_VERIFIER"
)
R288_ISOLATED_STATE = (
    "NEW_DISJOINT_CANDIDATE__"
    "POSITIVE_VOLUME_RATIONAL_INNER_SUPPORT_NOT_MATERIALIZED"
)
R288_NEW_STATES = {R288_READY_STATE, R288_ISOLATED_STATE}

R287_ALIAS_DISPOSITION = (
    "EXACT_INCLUSION_ALIAS_REPRESENTATION_SUBCOVER__"
    "CONDITIONAL_ON_CONTAINING_ATOM_IDENTITY"
)
PROBE_OCCUPIED = (
    "EXACT_EXISTING_OCCURRENCE_REPRESENTATION_SUBCOVER__"
    "NO_NEW_OCCURRENCE_ID"
)
PROBE_UNCOVERED = (
    "EXACT_UNCOVERED_POSITIVE_OPEN_SLICE__"
    "MEMBER_OF_REFINED_PARENT_LOCAL_NEW_SUPPORT"
)


class Round292RegistryError(RuntimeError):
    """Fail-closed contract violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Round292RegistryError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value):
        yield chunk.encode("utf-8")


def canonical(value: Any) -> bytes:
    return b"".join(chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in chunks(value):
        state.update(chunk)
    return state.hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1024 * 1024), b""):
            state.update(piece)
    return state.hexdigest()


def read_json(name: str) -> dict[str, Any]:
    with (HERE / name).open("rb") as stream:
        value = json.load(stream)
    need(isinstance(value, dict), f"JSON object:{name}")
    return value


def read_gzip_json(name: str) -> dict[str, Any]:
    with gzip.open(HERE / name, "rb") as stream:
        value = json.load(stream)
    need(isinstance(value, dict), f"gzip JSON object:{name}")
    return value


def verify_input_bytes() -> None:
    actual = {
        name: file_sha256(HERE / name)
        for name in sorted(INPUT_SHA256)
    }
    need(actual == dict(sorted(INPUT_SHA256.items())), "complete input byte pins")


def parse_manifest(name: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    with (HERE / name).open("rt", encoding="utf-8") as stream:
        for line in stream:
            text = line.rstrip("\n")
            if not text:
                continue
            match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", text)
            need(match is not None, f"manifest syntax:{name}")
            sha256, filename = match.groups()
            need(filename not in rows, f"manifest duplicate:{name}:{filename}")
            rows[filename] = sha256
    need(rows, f"nonempty manifest:{name}")
    return rows


def verify_selected_manifest_bindings() -> None:
    for manifest, selections in MANIFEST_SELECTIONS.items():
        entries = parse_manifest(manifest)
        for filename in selections:
            need(
                entries.get(filename) == INPUT_SHA256[filename],
                f"manifest selected binding:{manifest}:{filename}",
            )


def verify_result_digest(document: dict[str, Any], label: str) -> None:
    expected = document.get("result_sha256")
    payload = dict(document)
    payload.pop("result_sha256", None)
    need(
        isinstance(expected, str)
        and re.fullmatch(r"[0-9a-f]{64}", expected) is not None
        and digest(payload) == expected,
        f"result self digest:{label}",
    )


def verify_closed_row(row: dict[str, Any], label: str) -> None:
    payload = dict(row)
    row_hash = payload.pop("row_sha256", None)
    need(row_hash == digest(payload), f"closed row:{label}")


def validate_standard_ledger(
    table: dict[str, Any],
    *,
    schema: str,
    id_field: str,
    expected_count: int,
    label: str,
) -> list[dict[str, Any]]:
    rows = table.get("rows")
    need(
        table.get("schema") == schema
        and table.get("row_count") == expected_count
        and isinstance(rows, list)
        and len(rows) == expected_count
        and table.get("every_row_closed_by_own_SHA256") is True,
        f"standard ledger envelope:{label}",
    )
    ids = [row[id_field] for row in rows]
    hashes = [row["row_sha256"] for row in rows]
    need(
        len(set(ids)) == expected_count
        and table.get("row_ids_sha256") == digest(ids)
        and table.get("row_hashes_sha256") == digest(hashes)
        and table.get("rows_sha256") == digest(rows),
        f"standard ledger commitments:{label}",
    )
    for row in rows:
        verify_closed_row(row, f"{label}:{row[id_field]}")
    return rows


def load_round266_occurrence_rows() -> list[dict[str, Any]]:
    """Read only the 126,468-row occurrence table from the 892 MiB envelope."""

    path = HERE / R266_CERTIFICATE
    marker = (
        b'"formal_post_Round266_expanded_occurrence_frontier_ledger":'
    )
    end_marker = b',"formal_post_Round266_key_frontier_ledger":'
    with path.open("rb") as stream, mmap.mmap(
        stream.fileno(), 0, access=mmap.ACCESS_READ
    ) as mapped:
        start = mapped.find(marker)
        need(start >= 0, "Round266 occurrence ledger marker")
        need(mapped.find(marker, start + 1) < 0, "unique Round266 ledger marker")
        start += len(marker)
        end = mapped.find(end_marker, start)
        need(end > start, "Round266 occurrence ledger terminator")
        table = json.loads(mapped[start:end])
    need(
        table.get("row_count") == 126_468
        and table.get("every_row_closed_by_own_SHA256") is True,
        "Round266 occurrence ledger envelope",
    )
    rows = table["rows"]
    ids = [
        row["post_Round266_expanded_occurrence_frontier_row_id"]
        for row in rows
    ]
    hashes = [row["row_sha256"] for row in rows]
    need(
        len(rows) == 126_468
        and len(set(ids)) == 126_468
        and table["rows_sha256"]
        == "441cde017675dc279a55d52f47c24c31721309ad1cb03e1ea831e6984569f351"
        == digest(rows)
        and table["row_ids_sha256"]
        == "db01addd10a5112d56109695684d64994b927ce009e71b5e39dc95de2846acce"
        == digest(ids)
        and table["row_hashes_sha256"]
        == "08fa74d62a0673cb02339bae0df05007e7f4cb9d452d69feef79a958ceaa5ad9"
        == digest(hashes),
        "Round266 occurrence ledger commitments",
    )
    for row in rows:
        verify_closed_row(
            row, row["post_Round266_expanded_occurrence_frontier_row_id"]
        )
    return rows


def validate_r287_ledger(
    table: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    need(
        table.get("schema")
        == "cm2.round287.source-g-rechart-terminal-occurrence-disposition."
        "ledger.v1",
        "Round287 ledger schema",
    )
    specs = {
        "mutually_exclusive_outer_overlap_pair_rows": (
            3_488,
            "Round287_mutually_exclusive_outer_overlap_pair_row_id",
        ),
        "potential_new_support_union_rows": (
            10_020,
            "Round287_potential_new_support_union_id",
        ),
        "refinement_cell_rows": (
            7_616,
            "Round287_refinement_cell_disposition_row_id",
        ),
        "region_rows": (
            13_788,
            "Round287_region_disposition_row_id",
        ),
        "valid_internal_physical_face_rows": (
            648,
            "Round287_internal_physical_face_row_id",
        ),
    }
    output: dict[str, list[dict[str, Any]]] = {}
    for key, (count, id_field) in specs.items():
        rows = table.get(key)
        count_key = key.removesuffix("s") + "_count"
        digest_key = key + "_sha256"
        need(
            isinstance(rows, list)
            and len(rows) == count
            and table.get(count_key) == count
            and table.get(digest_key) == digest(rows)
            and len({row[id_field] for row in rows}) == count,
            f"Round287 table envelope:{key}",
        )
        for row in rows:
            verify_closed_row(row, f"{key}:{row[id_field]}")
        output[key] = rows
    return output


PROBE_ROW_ID_FIELDS = (
    "Round292_registry_overlap_row_id",
    "Round292_R287_existing_overlap_refinement_cell_id",
    "Round292_refined_new_support_component_id",
)


def probe_row_id(row: dict[str, Any]) -> str:
    if "Round292_registry_overlap_row_id" in row:
        return row["Round292_registry_overlap_row_id"]
    if "Round292_R287_existing_overlap_refinement_cell_id" in row:
        return row["Round292_R287_existing_overlap_refinement_cell_id"]
    if "Round292_refined_new_support_component_id" in row:
        return row["Round292_refined_new_support_component_id"]
    raise Round292RegistryError("missing overlap-probe row ID")


def validate_probe_ledger(
    table: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    rows = table.get("rows")
    need(
        table.get("schema")
        == "cm2.round292.r287-registry-overlap-exhaustion-probe.v1."
        "ledger.v1"
        and table.get("row_count") == 22_820
        and isinstance(rows, list)
        and len(rows) == 22_820
        and table.get("rows_sha256")
        == "556bd0ed95709fe43ff7837522d8729582ce0e7c9679879a57365f864f6ba055"
        == digest(rows),
        "Round292 overlap-probe ledger envelope",
    )
    ids = [probe_row_id(row) for row in rows]
    need(len(set(ids)) == 22_820, "unique overlap-probe row IDs")
    overlaps: list[dict[str, Any]] = []
    refinement: list[dict[str, Any]] = []
    components: list[dict[str, Any]] = []
    pair_rows: list[dict[str, Any]] = []
    for row in rows:
        row_id = probe_row_id(row)
        verify_closed_row(row, f"overlap probe:{row_id}")
        if "Round292_registry_overlap_row_id" in row:
            expected = "round292-registry-overlap:" + digest([
                row["Round287_potential_new_support_union_id"],
                row["Round287_support_cell_id"],
                row["registry_occurrence_id"],
                row["registry_exact_rational_support_box"],
            ])
            need(row_id == expected, f"probe overlap content ID:{row_id}")
            overlaps.append(row)
        elif "Round292_R287_existing_overlap_refinement_cell_id" in row:
            expected = "round292-r287-existing-refinement-cell:" + digest([
                row["Round287_potential_new_support_union_id"],
                row["source_Round287_support_cell_id"],
                row["exact_transformed_open_cell"],
            ])
            need(row_id == expected, f"probe refinement content ID:{row_id}")
            refinement.append(row)
        elif "member_refinement_cell_ids" in row:
            expected = "round292-r287-refined-new-support:" + digest([
                "ROUND287_EXISTING_OVERLAP_REFINED_NEW_SUPPORT_V1",
                row["source_Round287_potential_new_support_union_id"],
                row["member_refinement_cell_ids"],
            ])
            need(row_id == expected, f"probe component content ID:{row_id}")
            components.append(row)
        else:
            pair_rows.append(row)
    need(
        len(overlaps) == 1_564
        and len(refinement) == 11_852
        and len(components) == 9_404
        and not pair_rows,
        "overlap-probe row-kind census",
    )
    return overlaps, refinement, components, pair_rows


def zero_credit() -> dict[str, int]:
    return {field: 0 for field in ZERO_FIELDS}


def registry_row(payload: dict[str, Any]) -> dict[str, Any]:
    need(
        not (set(payload) & {"Round292_registry_candidate_row_id", "row_sha256"}),
        "fresh registry payload",
    )
    row_id = "round292-registry-candidate:" + digest([
        "ROUND292_OCCURRENCE_REGISTRY_CANDIDATE_ROW_V2",
        payload,
    ])
    row = {
        "Round292_registry_candidate_row_id": row_id,
        **payload,
    }
    row["row_sha256"] = digest(row)
    return row


def alias_row(payload: dict[str, Any]) -> dict[str, Any]:
    need(
        not (set(payload) & {"Round292_alias_binding_candidate_row_id", "row_sha256"}),
        "fresh alias payload",
    )
    row_id = "round292-alias-binding-candidate:" + digest([
        "ROUND292_OCCURRENCE_ALIAS_BINDING_CANDIDATE_ROW_V2",
        payload,
    ])
    row = {
        "Round292_alias_binding_candidate_row_id": row_id,
        **payload,
    }
    row["row_sha256"] = digest(row)
    return row


def verify_registry_row_content_id(row: dict[str, Any]) -> None:
    payload = dict(row)
    row_hash = payload.pop("row_sha256")
    row_id = payload.pop("Round292_registry_candidate_row_id")
    expected = "round292-registry-candidate:" + digest([
        "ROUND292_OCCURRENCE_REGISTRY_CANDIDATE_ROW_V2",
        payload,
    ])
    need(row_id == expected, f"registry row content ID:{row_id}")
    payload = {"Round292_registry_candidate_row_id": row_id, **payload}
    need(row_hash == digest(payload), f"registry row closure:{row_id}")


def verify_alias_row_content_id(row: dict[str, Any]) -> None:
    payload = dict(row)
    row_hash = payload.pop("row_sha256")
    row_id = payload.pop("Round292_alias_binding_candidate_row_id")
    expected = "round292-alias-binding-candidate:" + digest([
        "ROUND292_OCCURRENCE_ALIAS_BINDING_CANDIDATE_ROW_V2",
        payload,
    ])
    need(row_id == expected, f"alias row content ID:{row_id}")
    payload = {"Round292_alias_binding_candidate_row_id": row_id, **payload}
    need(row_hash == digest(payload), f"alias row closure:{row_id}")


def finite_content_address_insert(
    mapping: dict[str, bytes],
    occurrence_id: str,
    descriptor: Any,
    label: str,
) -> None:
    encoded = canonical(descriptor)
    previous = mapping.get(occurrence_id)
    need(previous is None, f"duplicate occurrence ID:{label}:{occurrence_id}")
    mapping[occurrence_id] = encoded


def valid_preserved_occurrence_id(source: str, occurrence_id: str) -> bool:
    patterns = {
        "ROUND174_RESOLVED": r"round174-resolved-3d:[0-9a-f]{64}",
        "ROUND179_RESOLVED": r"round179-resolved-child:[0-9a-f]{64}",
        "ROUND204_REGION": r"round204-wall-open-region:[0-9a-f]{64}",
        "ROUND208_REGION":
            r"round182-collar-leaf:[0-9a-f]{64}:STRICT_(?:NEGATIVE|POSITIVE)",
    }
    pattern = patterns.get(source)
    return pattern is not None and re.fullmatch(pattern, occurrence_id) is not None


def positive_box(box: list[str], label: str) -> None:
    need(len(box) == 6, f"box width:{label}")
    values = list(map(Fraction, box))
    need(
        all(values[2 * axis] < values[2 * axis + 1] for axis in range(3)),
        f"positive rational box:{label}",
    )


def ledger_attachment(
    rows: list[dict[str, Any]],
    id_field: str,
    schema: str,
    status: str,
    occurrence_field: str | None = None,
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    need(len(ids) == len(set(ids)), f"unique output ledger IDs:{id_field}")
    output = {
        "schema": schema,
        "status": status,
        "row_count": len(rows),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows_sha256": digest(rows),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }
    if occurrence_field is not None:
        occurrence_ids = [row[occurrence_field] for row in rows]
        output["occurrence_ids_sha256"] = digest(occurrence_ids)
    return output


def attachment_summary(
    ledger: dict[str, Any],
    filename: str,
) -> dict[str, Any]:
    keys = (
        "schema",
        "row_count",
        "row_ids_sha256",
        "row_hashes_sha256",
        "rows_sha256",
    )
    output = {"filename": filename}
    output.update({key: ledger[key] for key in keys})
    if "occurrence_ids_sha256" in ledger:
        output["occurrence_ids_sha256"] = ledger["occurrence_ids_sha256"]
    return output


def build(
    producer_sha256: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    verify_input_bytes()
    verify_selected_manifest_bindings()

    r266_verification = read_json(R266_VERIFICATION)
    need(
        r266_verification.get("schema")
        == "cm2.round266.source-g-expanded-curved-face-closure-verification.v1"
        and r266_verification.get("status") == "PASS_INDEPENDENT_ROUND266"
        and r266_verification.get("candidate_sha256")
        == INPUT_SHA256[R266_CERTIFICATE]
        and r266_verification.get("verified_census", {}).get(
            "complete_occurrence_frontier_count"
        ) == 126_468,
        "Round266 independent freeze",
    )

    r287_result = read_json(R287_RESULT)
    verify_result_digest(r287_result, "Round287")
    r287_verification = read_json(R287_VERIFICATION)
    need(
        r287_result.get("schema")
        == "cm2.round287.source-g-rechart-terminal-occurrence-disposition-probe.v1"
        and r287_result.get("census", {}).get(
            "total_conditional_new_Round275_support_count"
        ) == 10_020
        and r287_verification.get("status", "").startswith(
            "PASS_INDEPENDENT_ROUND287_TERMINAL_OCCURRENCE_DISPOSITION"
        ),
        "Round287 frozen input",
    )
    r287_tables = validate_r287_ledger(read_gzip_json(R287_LEDGER))

    r288_result = read_json(R288_RESULT)
    verify_result_digest(r288_result, "Round288")
    r288_verification = read_json(R288_VERIFICATION)
    need(
        r288_result.get("schema")
        == "cm2.round288.source-g-canonical-atom-occurrence-identity-gate-audit.v1"
        and r288_result.get("census", {}).get(
            "conditionally_distinct_new_atom_candidate_count"
        ) == 295_336
        and r288_result.get("census", {}).get(
            "existing_overlap_relation_count"
        ) == 36_680
        and r288_verification.get("status", "").startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND288"
        ),
        "Round288 frozen input",
    )
    r288_atom_rows = validate_standard_ledger(
        read_gzip_json(R288_ATOMS),
        schema="cm2.round288.canonical-atom-occurrence-disposition-ledger.v1",
        id_field="Round288_atom_disposition_row_id",
        expected_count=332_016,
        label="Round288 atom dispositions",
    )
    r288_overlap_rows = validate_standard_ledger(
        read_gzip_json(R288_OVERLAPS),
        schema="cm2.round288.existing-occurrence-overlap-relation-ledger.v1",
        id_field="Round288_existing_overlap_relation_row_id",
        expected_count=36_680,
        label="Round288 existing overlaps",
    )

    r290_result = read_json(R290_RESULT)
    verify_result_digest(r290_result, "Round290")
    r290_verification = read_json(R290_VERIFICATION)
    need(
        r290_result.get("schema")
        == "cm2.round290.source-g-isolated-atom-inner-support-closure.v1"
        and r290_result.get("census", {}).get(
            "strict_positive_volume_inner_support_count"
        ) == 21_160
        and r290_verification.get("status", "").startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND290"
        ),
        "Round290 frozen input",
    )
    r290_rows = validate_standard_ledger(
        read_gzip_json(R290_LEDGER),
        schema="cm2.round290.isolated-atom-inner-support-ledger.v1",
        id_field="Round290_inner_support_row_id",
        expected_count=21_160,
        label="Round290 inner supports",
    )

    probe_result = read_json(OVERLAP_PROBE_RESULT)
    verify_result_digest(probe_result, "Round292 overlap probe")
    need(
        probe_result.get("schema")
        == "cm2.round292.r287-registry-overlap-exhaustion-probe.v1"
        and probe_result.get("status")
        == "PASS_ZERO_CREDIT__R287_FULL_REGISTRY_OVERLAP_EXHAUSTED"
        and probe_result.get("census", {}).get(
            "refined_strictly_new_support_component_count"
        ) == 9_404
        and probe_result.get("census", {}).get(
            "occupied_representation_subcover_cell_count"
        ) == 1_600
        and probe_result.get("strict_nonpromotion", {}).get(
            "formal_new_occurrence_credit"
        ) == 0,
        "Round292 overlap-probe candidate result",
    )
    (
        probe_overlap_rows,
        probe_refinement_rows,
        probe_component_rows,
        probe_pair_rows,
    ) = validate_probe_ledger(read_gzip_json(OVERLAP_PROBE_LEDGER))
    need(not probe_pair_rows, "no unresolved overlap-probe pair rows")

    r266_rows = load_round266_occurrence_rows()
    occurrence_descriptors_by_id: dict[str, bytes] = {}
    registry_rows: list[dict[str, Any]] = []
    source_identity_keys: set[str] = set()

    # Preserve the complete Round266 occurrence identity frontier byte for
    # byte.  R266 does not carry enough upstream preimage data to recompute
    # all four historical ID formulas, so the content-address contract is
    # explicitly the pinned upstream contract rather than a false local
    # reconstruction claim.
    r266_source_histogram = Counter(
        row["occurrence_source"] for row in r266_rows
    )
    need(
        r266_source_histogram
        == {
            "ROUND174_RESOLVED": 72_500,
            "ROUND179_RESOLVED": 17_192,
            "ROUND204_REGION": 736,
            "ROUND208_REGION": 36_040,
        },
        "Round266 occurrence source census",
    )
    r208_sign_histogram: Counter[str] = Counter()
    preserved_by_id: dict[str, dict[str, Any]] = {}
    for source in sorted(
        r266_rows, key=lambda row: row["local_occurrence_row_id"]
    ):
        occurrence_id = source["local_occurrence_row_id"]
        occurrence_source = source["occurrence_source"]
        need(
            valid_preserved_occurrence_id(occurrence_source, occurrence_id)
            and occurrence_id == source["source_geometry_row_id"]
            and source["post_Round266_expanded_occurrence_frontier_row_id"]
            == "round266-expanded-occurrence:" + digest([occurrence_id]),
            f"Round266 preserved ID contract:{occurrence_id}",
        )
        if occurrence_source == "ROUND208_REGION":
            r208_sign_histogram[occurrence_id.rsplit(":", 1)[1]] += 1
        source_identity = f"ROUND266_LOCAL_OCCURRENCE::{occurrence_id}"
        need(
            source_identity not in source_identity_keys,
            f"unique source identity:{source_identity}",
        )
        source_identity_keys.add(source_identity)
        finite_content_address_insert(
            occurrence_descriptors_by_id,
            occurrence_id,
            [
                "UPSTREAM_PINNED_ROUND266_CONTENT_ADDRESS",
                occurrence_source,
                occurrence_id,
                source["source_geometry_row_sha256"],
                source["row_sha256"],
            ],
            "Round266",
        )
        row = registry_row({
            "registry_occurrence_id": occurrence_id,
            "registry_source_identity": source_identity,
            "registry_entry_kind":
                "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE",
            "registry_identity_status":
                "PRESERVED_EXISTING_ID__NO_ROUND292_PROMOTION",
            "registry_promotion_status": WAITING,
            "occurrence_id_content_addressing_contract":
                "UPSTREAM_PINNED_CONTENT_ADDRESS__PREIMAGE_NOT_REOPENED_HERE",
            "occurrence_id_content_preimage_sha256": None,
            "source_occurrence_round": 266,
            "source_occurrence_class": occurrence_source,
            "source_ledger_filename": R266_CERTIFICATE,
            "source_ledger_file_sha256": INPUT_SHA256[R266_CERTIFICATE],
            "source_ledger_table":
                "formal_post_Round266_expanded_occurrence_frontier_ledger",
            "source_row_id":
                source["post_Round266_expanded_occurrence_frontier_row_id"],
            "source_row_sha256": source["row_sha256"],
            "source_geometry_row_id": source["source_geometry_row_id"],
            "source_geometry_row_sha256":
                source["source_geometry_row_sha256"],
            "physical_support_chart": source["source_chart"],
            "owner_target": None,
            "official_key_id": source["official_key_id"],
            "official_key_ordinal": source["official_key_ordinal"],
            "complete_10_field_return_signature_sha256":
                source["complete_10_field_return_signature_sha256"],
            "support_representation_kind":
                "PINNED_ROUND266_EXISTING_OCCURRENCE_GEOMETRY",
            "positive_volume_rational_inner_support_box": None,
            "support_box_sha256": source["exact_box_sha256"],
            "support_geometry_status":
                "RECONSTRUCT_FROM_PINNED_SOURCE_GEOMETRY_ROW",
            "outer_envelope_used_as_inner_support": False,
            **zero_credit(),
        })
        registry_rows.append(row)
        preserved_by_id[occurrence_id] = row
    need(
        len(preserved_by_id) == 126_468
        and r208_sign_histogram
        == {"STRICT_NEGATIVE": 18_024, "STRICT_POSITIVE": 18_016},
        "Round266 preserved frontier injectivity",
    )

    # Join the 21,160 Round290 supports to the isolated Round288 atoms.  The
    # identity remains the Round288 reserved ID: support implementation never
    # rewrites occurrence identity.
    r290_by_atom = {
        row["canonical_atom_id"]: row
        for row in r290_rows
    }
    need(len(r290_by_atom) == 21_160, "unique Round290 atom join")
    atom_by_id = {
        row["canonical_atom_id"]: row
        for row in r288_atom_rows
    }
    need(len(atom_by_id) == 332_016, "unique Round288 canonical atoms")
    atom_to_occurrence_id: dict[str, str] = {}
    atom_state_histogram: Counter[str] = Counter()
    r288_new_count = 0
    for atom in sorted(
        r288_atom_rows, key=lambda row: row["canonical_atom_id"]
    ):
        atom_id = atom["canonical_atom_id"]
        state = atom["occurrence_identity_disposition"]
        atom_state_histogram[state] += 1
        need(
            atom["Round288_atom_disposition_row_id"]
            == "round288-atom-disposition:" + digest(atom_id),
            f"Round288 disposition content ID:{atom_id}",
        )
        if state in R288_EXISTING_STATES:
            occurrence_id = atom["existing_local_occurrence_row_id"]
            need(
                occurrence_id in preserved_by_id
                and atom["reserved_candidate_occurrence_id__not_issued"] is None,
                f"Round288 existing atom binding:{atom_id}",
            )
            atom_to_occurrence_id[atom_id] = occurrence_id
            continue
        need(state in R288_NEW_STATES, f"Round288 known state:{atom_id}")
        occurrence_id = atom["reserved_candidate_occurrence_id__not_issued"]
        need(
            isinstance(occurrence_id, str)
            and re.fullmatch(
                r"source-g-expanded-occurrence:[0-9a-f]{64}",
                occurrence_id,
            ) is not None,
            f"Round288 reserved content ID format:{atom_id}",
        )
        atom_to_occurrence_id[atom_id] = occurrence_id
        source_identity = f"ROUND288_CANONICAL_ATOM::{atom_id}"
        need(
            source_identity not in source_identity_keys,
            f"unique source identity:{source_identity}",
        )
        source_identity_keys.add(source_identity)
        finite_content_address_insert(
            occurrence_descriptors_by_id,
            occurrence_id,
            [
                "UPSTREAM_PINNED_ROUND288_RESERVED_CONTENT_ADDRESS",
                atom_id,
                atom["Round288_atom_disposition_row_id"],
                atom["row_sha256"],
            ],
            "Round288",
        )

        round290 = r290_by_atom.get(atom_id)
        if state == R288_READY_STATE:
            selected = atom["selected_Round279_strict_inner_corridor"]
            need(
                isinstance(selected, dict)
                and round290 is None,
                f"Round288 corridor support partition:{atom_id}",
            )
            support_kind = (
                "ROUND279_DYNAMIC_STRICT_INWARD_CORRIDOR_INNER_SUPPORT"
            )
            support_box = selected[
                "exact_positive_volume_rational_inner_support_box"
            ]
            support_volume = selected["exact_inner_support_volume"]
            support_source_row_id = selected[
                "formal_face_edge_witness_row_id"
            ]
            support_source_row_sha256 = None
            source_round279_face = support_source_row_id
            source_round290_row = None
            source_round290_hash = None
            support_verification = (
                "PASS_PINNED_INDEPENDENT_ROUND288_DYNAMIC_CORRIDOR_VERIFIER"
            )
        else:
            need(
                round290 is not None
                and atom["selected_Round279_strict_inner_corridor"] is None
                and round290["Round288_atom_disposition_row_id"]
                == atom["Round288_atom_disposition_row_id"]
                and round290["Round182_leaf_row_id"]
                == atom["Round182_leaf_row_id"]
                and round290["complete_10_field_return_signature_sha256"]
                == atom["complete_10_field_return_signature_sha256"]
                and round290["official_key_id"] == atom["official_key_id"]
                and round290["official_key_ordinal"]
                == atom["official_key_ordinal"],
                f"Round290 isolated support join:{atom_id}",
            )
            support_kind = "ROUND290_ISOLATED_ATOM_RATIONAL_INNER_SUPPORT"
            support_box = round290[
                "exact_positive_volume_rational_inner_support_box"
            ]
            support_volume = round290["exact_inner_support_volume"]
            support_source_row_id = round290["Round290_inner_support_row_id"]
            support_source_row_sha256 = round290["row_sha256"]
            source_round279_face = None
            source_round290_row = support_source_row_id
            source_round290_hash = support_source_row_sha256
            support_verification = (
                "PASS_PINNED_INDEPENDENT_ROUND290_WHOLE_BOX_VERIFIER"
            )
        positive_box(support_box, f"Round288/290 support:{atom_id}")
        need(
            Fraction(support_volume) > 0
            and support_box
            not in atom["frozen_positive_rational_support_envelopes"],
            f"inner support is not outer envelope:{atom_id}",
        )
        row = registry_row({
            "registry_occurrence_id": occurrence_id,
            "registry_source_identity": source_identity,
            "registry_entry_kind":
                "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM",
            "registry_identity_status":
                "CANDIDATE_NEW_ID__NOT_FORMALLY_ISSUED",
            "registry_promotion_status": WAITING,
            "occurrence_id_content_addressing_contract":
                "PINNED_ROUND288_RESERVED_CONTENT_ADDRESS__"
                "INDEPENDENT_R288_VERIFIER_REBUILT_PREIMAGE",
            "occurrence_id_content_preimage_sha256":
                occurrence_id.rsplit(":", 1)[1],
            "source_occurrence_round": 288,
            "source_occurrence_class": state,
            "source_ledger_filename": R288_ATOMS,
            "source_ledger_file_sha256": INPUT_SHA256[R288_ATOMS],
            "source_ledger_table": "rows",
            "source_row_id": atom["Round288_atom_disposition_row_id"],
            "source_row_sha256": atom["row_sha256"],
            "canonical_atom_id": atom_id,
            "Round182_leaf_row_id": atom["Round182_leaf_row_id"],
            "source_signature_row_ids": atom["source_signature_row_ids"],
            "source_proof_classes": atom["source_proof_classes"],
            "physical_support_chart": atom["source_chart"],
            "owner_target": atom["owner_target"],
            "official_key_id": atom["official_key_id"],
            "official_key_ordinal": atom["official_key_ordinal"],
            "complete_10_field_return_signature_sha256":
                atom["complete_10_field_return_signature_sha256"],
            "support_representation_kind": support_kind,
            "support_source_row_id": support_source_row_id,
            "support_source_row_sha256": support_source_row_sha256,
            "source_Round279_formal_face_edge_witness_row_id":
                source_round279_face,
            "source_Round290_inner_support_row_id": source_round290_row,
            "source_Round290_inner_support_row_sha256":
                source_round290_hash,
            "positive_volume_rational_inner_support_box": support_box,
            "exact_inner_support_volume": support_volume,
            "outer_support_envelopes_sha256": digest(
                atom["frozen_positive_rational_support_envelopes"]
            ),
            "support_geometry_status": support_verification,
            "outer_envelope_used_as_inner_support": False,
            **zero_credit(),
        })
        registry_rows.append(row)
        r288_new_count += 1
    need(
        atom_state_histogram
        == {
            R288_READY_STATE: 274_176,
            R288_ISOLATED_STATE: 21_160,
            "EXISTING_ROUND208_OCCURRENCE_ID_PRESERVED": 36_040,
            "EXACT_ALIAS_OF_EXISTING_ROUND204_OCCURRENCE": 640,
        }
        and r288_new_count == 295_336
        and set(r290_by_atom)
        == {
            row["canonical_atom_id"]
            for row in r288_atom_rows
            if row["occurrence_identity_disposition"] == R288_ISOLATED_STATE
        },
        "Round288/Round290 complete identity-support partition",
    )

    union_rows = r287_tables["potential_new_support_union_rows"]
    union_by_id = {
        row["Round287_potential_new_support_union_id"]: row
        for row in union_rows
    }
    region_rows = r287_tables["region_rows"]
    region_by_id = {
        row["Round275_region_id"]: row
        for row in region_rows
    }
    need(
        len(union_by_id) == 10_020 and len(region_by_id) == 13_788,
        "Round287 provenance maps",
    )
    refinement_by_id = {
        row["Round292_R287_existing_overlap_refinement_cell_id"]: row
        for row in probe_refinement_rows
    }
    component_by_id = {
        row["Round292_refined_new_support_component_id"]: row
        for row in probe_component_rows
    }
    need(
        len(refinement_by_id) == 11_852
        and len(component_by_id) == 9_404,
        "Round292 probe maps",
    )

    occupied_probe_rows = [
        row for row in probe_refinement_rows
        if row["disposition"] == PROBE_OCCUPIED
    ]
    uncovered_probe_rows = [
        row for row in probe_refinement_rows
        if row["disposition"] == PROBE_UNCOVERED
    ]
    need(
        len(occupied_probe_rows) == 1_600
        and len(uncovered_probe_rows) == 10_252
        and all(
            row["existing_occurrence_occupancy_count"] == 1
            and len(row["existing_occurrence_ids"]) == 1
            and row["Round292_refined_new_support_component_id"] is None
            for row in occupied_probe_rows
        )
        and all(
            row["existing_occurrence_occupancy_count"] == 0
            and not row["existing_occurrence_ids"]
            and isinstance(
                row["Round292_refined_new_support_component_id"], str
            )
            for row in uncovered_probe_rows
        ),
        "Round292 refined occupied/uncovered partition",
    )
    for row in probe_refinement_rows:
        positive_box(
            row["exact_transformed_open_cell"],
            row["Round292_R287_existing_overlap_refinement_cell_id"],
        )
        need(
            Fraction(row["exact_transformed_cell_volume"]) > 0
            and row["exact_transformed_coordinate_system"] == "(t^2,p,s)"
            and all(row.get(field, 0) == 0 for field in (
                "formal_new_occurrence_credit",
                "formal_representation_alias_binding_credit",
                "formal_component_credit",
                "formal_DSU_rank_reduction_credit",
            )),
            "exact probe refinement cell contract",
        )

    component_source_unions: set[str] = set()
    component_member_ids: set[str] = set()
    for component in sorted(
        probe_component_rows,
        key=lambda row: row["Round292_refined_new_support_component_id"],
    ):
        component_id = component["Round292_refined_new_support_component_id"]
        union_id = component[
            "source_Round287_potential_new_support_union_id"
        ]
        source_union = union_by_id.get(union_id)
        need(source_union is not None, f"component Round287 union:{component_id}")
        member_ids = component["member_refinement_cell_ids"]
        members = [refinement_by_id[member_id] for member_id in member_ids]
        need(
            member_ids == sorted(member_ids)
            and len(member_ids) == component["member_refinement_cell_count"]
            and all(
                member["disposition"] == PROBE_UNCOVERED
                and member["Round292_refined_new_support_component_id"]
                == component_id
                and member["Round287_potential_new_support_union_id"]
                == union_id
                for member in members
            )
            and component["one_connected_positive_open_support"] is True
            and component[
                "strictly_disjoint_from_complete_conditional_base_atom_registry"
            ] is True,
            f"component exact member binding:{component_id}",
        )
        need(
            not (component_member_ids & set(member_ids)),
            f"component member injectivity:{component_id}",
        )
        component_member_ids.update(member_ids)
        component_source_unions.add(union_id)
        charts = {member["source_chart"] for member in members}
        signatures = {
            member["complete_10_field_return_signature_sha256"]
            for member in members
        }
        regions = {member["Round275_region_id"] for member in members}
        need(
            len(charts) == len(signatures) == len(regions) == 1
            and regions == {source_union["Round275_region_id"]}
            and charts == {source_union["adjacent_chart"]}
            and signatures
            == {source_union["complete_10_field_return_signature_sha256"]},
            f"component physical provenance:{component_id}",
        )
        physical_chart = next(iter(charts))
        signature_sha = next(iter(signatures))
        region_id = next(iter(regions))
        source_region = region_by_id[region_id]
        need(
            source_region["adjacent_chart"] == physical_chart
            and source_region["source_chart"] == source_union["source_chart"]
            and source_region["owner_target"] == source_union["owner_target"],
            f"component region provenance:{component_id}",
        )

        occurrence_preimage = [
            "ROUND292_R287_EXISTING_OVERLAP_REFINED_NEW_SUPPORT_"
            "LOCAL_OCCURRENCE_V1",
            component_id,
            component["row_sha256"],
        ]
        occurrence_suffix = digest(occurrence_preimage)
        occurrence_id = "source-g-expanded-occurrence:" + occurrence_suffix
        source_identity = f"ROUND292_R287_REFINED_COMPONENT::{component_id}"
        need(
            source_identity not in source_identity_keys,
            f"unique source identity:{source_identity}",
        )
        source_identity_keys.add(source_identity)
        finite_content_address_insert(
            occurrence_descriptors_by_id,
            occurrence_id,
            occurrence_preimage,
            "Round292 refined R287 component",
        )
        member_payloads = [
            {
                "Round292_refinement_cell_id":
                    member["Round292_R287_existing_overlap_refinement_cell_id"],
                "source_row_sha256": member["row_sha256"],
                "source_Round287_support_cell_id":
                    member["source_Round287_support_cell_id"],
                "exact_transformed_coordinate_system":
                    member["exact_transformed_coordinate_system"],
                "exact_transformed_open_cell":
                    member["exact_transformed_open_cell"],
                "exact_transformed_cell_volume":
                    member["exact_transformed_cell_volume"],
                "Round275_region_id": member["Round275_region_id"],
                "physical_support_chart": member["source_chart"],
                "complete_10_field_return_signature_sha256":
                    member["complete_10_field_return_signature_sha256"],
            }
            for member in members
        ]
        row = registry_row({
            "registry_occurrence_id": occurrence_id,
            "registry_source_identity": source_identity,
            "registry_entry_kind":
                "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT",
            "registry_identity_status":
                "CANDIDATE_NEW_ID__NOT_FORMALLY_ISSUED",
            "registry_promotion_status": WAITING,
            "occurrence_id_content_addressing_contract":
                "ROUND292_CANONICAL_JSON_SHA256_DOMAIN_SEPARATED_V1",
            "occurrence_id_content_preimage_sha256": occurrence_suffix,
            "source_occurrence_round": 292,
            "source_occurrence_class":
                "R287_EXISTING_OVERLAP_REFINED_NEW_SUPPORT_COMPONENT",
            "source_ledger_filename": OVERLAP_PROBE_LEDGER,
            "source_ledger_file_sha256":
                INPUT_SHA256[OVERLAP_PROBE_LEDGER],
            "source_ledger_table": "rows",
            "source_row_id": component_id,
            "source_row_sha256": component["row_sha256"],
            "source_Round287_union_id": union_id,
            "source_Round287_union_row_sha256": source_union["row_sha256"],
            "source_Round287_union_kind": source_union["source_kind"],
            "source_Round287_reverse_rechart_chart":
                source_union["source_chart"],
            "source_Round287_original_member_cell_ids":
                source_union["nonempty_uncovered_member_cell_ids"],
            "source_Round287_internal_physical_face_ids":
                source_union["valid_internal_physical_face_ids"],
            "Round275_region_id": region_id,
            "source_Round287_region_disposition_row_id":
                source_region["Round287_region_disposition_row_id"],
            "source_Round287_region_disposition_row_sha256":
                source_region["row_sha256"],
            "physical_support_chart": physical_chart,
            "owner_target": source_union["owner_target"],
            "official_key_id": None,
            "official_key_ordinal": None,
            "official_key_binding_status":
                "NOT_MATERIALIZED_IN_R287_FROZEN_LEDGER__"
                "COMPLETE_SIGNATURE_HASH_PINNED",
            "complete_10_field_return_signature_sha256": signature_sha,
            "support_representation_kind":
                "EXACT_T2_P_S_CONNECTED_UNCOVERED_REFINEMENT_CELL_UNION",
            "positive_volume_rational_inner_support_box": None,
            "exact_transformed_coordinate_system": "(t^2,p,s)",
            "member_refinement_cell_count": len(member_payloads),
            "member_refinement_cells": member_payloads,
            "one_connected_positive_open_support": True,
            "strictly_disjoint_from_complete_conditional_base_atom_registry":
                True,
            "support_geometry_status":
                "PINNED_EXACT_TRANSFORMED_CELL_UNION__"
                "NOT_RELABELED_AS_ONE_OUTER_OR_INNER_BOX",
            "outer_envelope_used_as_inner_support": False,
            **zero_credit(),
        })
        registry_rows.append(row)
    need(
        len(component_source_unions) == 9_404
        and component_member_ids
        == {
            row["Round292_R287_existing_overlap_refinement_cell_id"]
            for row in uncovered_probe_rows
        },
        "complete refined-component support partition",
    )

    registry_rows.sort(key=lambda row: row["registry_occurrence_id"])
    registry_occurrence_ids = [
        row["registry_occurrence_id"] for row in registry_rows
    ]
    registry_row_ids = [
        row["Round292_registry_candidate_row_id"]
        for row in registry_rows
    ]
    need(
        len(registry_rows) == 431_208
        and len(set(registry_occurrence_ids)) == 431_208
        and len(set(registry_row_ids)) == 431_208
        and len(occurrence_descriptors_by_id) == 431_208
        and len(set(occurrence_descriptors_by_id.values())) == 431_208
        and len(source_identity_keys) == 431_208,
        "finite registry occurrence-ID injectivity and collision freedom",
    )
    for row in registry_rows:
        verify_registry_row_content_id(row)
        need(
            all(row[field] == 0 for field in ZERO_FIELDS)
            and row["outer_envelope_used_as_inner_support"] is False,
            f"registry zero-credit:{row['registry_occurrence_id']}",
        )
    registry_by_occurrence = {
        row["registry_occurrence_id"]: row for row in registry_rows
    }

    alias_rows: list[dict[str, Any]] = []

    # Round288 exact-equality aliases to preserved Round266 IDs.
    for relation in sorted(
        r288_overlap_rows,
        key=lambda row: row["Round288_existing_overlap_relation_row_id"],
    ):
        atom_id = relation["canonical_atom_id"]
        atom = atom_by_id[atom_id]
        target_id = relation["existing_local_occurrence_row_id"]
        need(
            atom["occurrence_identity_disposition"] in R288_EXISTING_STATES
            and atom["existing_local_occurrence_row_id"] == target_id
            and atom_to_occurrence_id[atom_id] == target_id
            and target_id in preserved_by_id
            and relation["relation"] == "EXACT_EQUAL_SUPPORT_ENVELOPE"
            and relation["Round288_existing_overlap_relation_row_id"]
            == "round288-existing-overlap:" + digest([
                atom_id,
                target_id,
                relation["atom_support_box_index"],
            ]),
            f"Round288 exact alias relation:{atom_id}",
        )
        target = registry_by_occurrence[target_id]
        alias_rows.append(alias_row({
            "alias_source_identity":
                f"ROUND288_CANONICAL_ATOM_REPRESENTATION::{atom_id}",
            "alias_source_kind":
                "ROUND288_EXACT_EQUAL_EXISTING_SUPPORT_ENVELOPE",
            "source_representation_id": atom_id,
            "target_registry_occurrence_id": target_id,
            "target_registry_candidate_row_id":
                target["Round292_registry_candidate_row_id"],
            "target_registry_entry_kind": target["registry_entry_kind"],
            "target_registry_identity_status":
                target["registry_identity_status"],
            "alias_binding_status": WAITING,
            "does_not_issue_new_occurrence_id": True,
            "does_not_collapse_distinct_occurrence_ids": True,
            "source_ledger_filename": R288_OVERLAPS,
            "source_ledger_file_sha256": INPUT_SHA256[R288_OVERLAPS],
            "source_row_id":
                relation["Round288_existing_overlap_relation_row_id"],
            "source_row_sha256": relation["row_sha256"],
            "source_Round288_atom_disposition_row_id":
                atom["Round288_atom_disposition_row_id"],
            "source_Round288_atom_disposition_row_sha256":
                atom["row_sha256"],
            "physical_support_chart": relation["source_chart"],
            "owner_target": atom["owner_target"],
            "complete_10_field_return_signature_sha256":
                relation["complete_10_field_return_signature_sha256"],
            "support_representation_kind":
                "EXACT_EQUAL_SUPPORT_ENVELOPE_ALIAS_EVIDENCE",
            "exact_support_representation_box": relation["exact_box"],
            "outer_envelope_used_as_inner_support": False,
            **zero_credit(),
        }))

    # The original Round287 representation subcovers map to their containing
    # Round279 atom identity.  They never receive an occurrence ID.
    r287_region_aliases = [
        row for row in region_rows
        if row["exact_inclusion_alias_lemma_satisfied"] is True
    ]
    r287_cell_rows = r287_tables["refinement_cell_rows"]
    r287_cell_aliases = [
        row for row in r287_cell_rows
        if row["exact_inclusion_alias_lemma_satisfied"] is True
    ]
    need(
        len(r287_region_aliases) == 2_476
        and len(r287_cell_aliases) == 5_532,
        "Round287 atom-subcover alias census",
    )
    for source_kind, aliases in (
        ("ROUND287_R275_REGION_INCLUSION_SUBCOVER", r287_region_aliases),
        ("ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER", r287_cell_aliases),
    ):
        for source in sorted(
            aliases,
            key=lambda row: (
                row.get("Round287_region_disposition_row_id")
                or row["Round287_refinement_cell_disposition_row_id"]
            ),
        ):
            is_region = "Round287_region_disposition_row_id" in source
            if is_region:
                need(
                    source["disposition"] == R287_ALIAS_DISPOSITION
                    and source["containing_atom_id"] is not None
                    and source["Round287_potential_new_support_union_id"] is None
                    and source["Round286_refinement_cell_count"] == 0,
                    "Round287 region alias exact filter",
                )
                source_row_id = source[
                    "Round287_region_disposition_row_id"
                ]
                representation_id = source["Round275_region_id"]
                representation_box = None
                signed_state = None
            else:
                need(
                    source["disposition"] == R287_ALIAS_DISPOSITION
                    and source["containing_atom_id"] is not None
                    and source["Round286_coordinate_occupancy_count"] == 1
                    and source["signed_region_cell_state"]
                    != "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL",
                    "Round287 cell alias exact filter",
                )
                source_row_id = source[
                    "Round287_refinement_cell_disposition_row_id"
                ]
                representation_id = source["Round286_refinement_cell_id"]
                representation_box = source["coordinate_box"]
                signed_state = source["signed_region_cell_state"]
            atom_id = source["containing_atom_id"]
            atom = atom_by_id[atom_id]
            target_id = atom_to_occurrence_id[atom_id]
            target = registry_by_occurrence[target_id]
            alias_rows.append(alias_row({
                "alias_source_identity":
                    f"{source_kind}::{representation_id}",
                "alias_source_kind": source_kind,
                "source_representation_id": representation_id,
                "target_registry_occurrence_id": target_id,
                "target_registry_candidate_row_id":
                    target["Round292_registry_candidate_row_id"],
                "target_registry_entry_kind": target["registry_entry_kind"],
                "target_registry_identity_status":
                    target["registry_identity_status"],
                "alias_binding_status": WAITING,
                "does_not_issue_new_occurrence_id": True,
                "does_not_collapse_distinct_occurrence_ids": True,
                "source_ledger_filename": R287_LEDGER,
                "source_ledger_file_sha256": INPUT_SHA256[R287_LEDGER],
                "source_row_id": source_row_id,
                "source_row_sha256": source["row_sha256"],
                "source_Round287_reverse_rechart_chart":
                    source["source_chart"],
                "Round275_region_id": source["Round275_region_id"],
                "source_Round288_containing_atom_id": atom_id,
                "source_Round288_atom_disposition_row_id":
                    atom["Round288_atom_disposition_row_id"],
                "source_Round288_atom_disposition_row_sha256":
                    atom["row_sha256"],
                "physical_support_chart": source["adjacent_chart"],
                "owner_target": source["owner_target"],
                "complete_10_field_return_signature_sha256":
                    source["complete_10_field_return_signature_sha256"],
                "support_representation_kind":
                    "EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER",
                "exact_support_representation_box": representation_box,
                "physical_t_sign": source["physical_t_sign"],
                "physical_t_square_open_interval":
                    source["physical_t_square_open_interval"],
                "signed_region_cell_state": signed_state,
                "outer_envelope_used_as_inner_support": False,
                **zero_credit(),
            }))

    # The exact overlap refinement contributes 1,600 additional bindings to
    # preserved Round174/Round179 occurrences.  Occupied cells are never new
    # occurrences and are never merged by a DSU here.
    refined_alias_source_histogram: Counter[str] = Counter()
    for source in sorted(
        occupied_probe_rows,
        key=lambda row: row[
            "Round292_R287_existing_overlap_refinement_cell_id"
        ],
    ):
        target_id = source["existing_occurrence_ids"][0]
        target = registry_by_occurrence.get(target_id)
        need(
            target is not None
            and target["registry_entry_kind"]
            == "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
            and target["source_occurrence_class"]
            in {"ROUND174_RESOLVED", "ROUND179_RESOLVED"},
            f"refined occupied cell target:{target_id}",
        )
        refined_alias_source_histogram[
            target["source_occurrence_class"]
        ] += 1
        union_id = source["Round287_potential_new_support_union_id"]
        source_union = union_by_id[union_id]
        need(
            source["source_chart"] == source_union["adjacent_chart"]
            and source["Round275_region_id"]
            == source_union["Round275_region_id"],
            "refined occupied-cell physical provenance",
        )
        alias_rows.append(alias_row({
            "alias_source_identity":
                "ROUND292_R287_REFINED_EXISTING_SUBCOVER::"
                + source[
                    "Round292_R287_existing_overlap_refinement_cell_id"
                ],
            "alias_source_kind":
                "ROUND292_R287_EXACT_REFINED_EXISTING_SUBCOVER_CELL",
            "source_representation_id":
                source["Round292_R287_existing_overlap_refinement_cell_id"],
            "target_registry_occurrence_id": target_id,
            "target_registry_candidate_row_id":
                target["Round292_registry_candidate_row_id"],
            "target_registry_entry_kind": target["registry_entry_kind"],
            "target_registry_identity_status":
                target["registry_identity_status"],
            "alias_binding_status": WAITING,
            "does_not_issue_new_occurrence_id": True,
            "does_not_collapse_distinct_occurrence_ids": True,
            "source_ledger_filename": OVERLAP_PROBE_LEDGER,
            "source_ledger_file_sha256":
                INPUT_SHA256[OVERLAP_PROBE_LEDGER],
            "source_row_id":
                source["Round292_R287_existing_overlap_refinement_cell_id"],
            "source_row_sha256": source["row_sha256"],
            "source_Round287_union_id": union_id,
            "source_Round287_union_row_sha256": source_union["row_sha256"],
            "source_Round287_union_kind": source_union["source_kind"],
            "source_Round287_support_cell_id":
                source["source_Round287_support_cell_id"],
            "Round275_region_id": source["Round275_region_id"],
            "physical_support_chart": source["source_chart"],
            "owner_target": source_union["owner_target"],
            "complete_10_field_return_signature_sha256":
                source["complete_10_field_return_signature_sha256"],
            "support_representation_kind":
                "EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL",
            "exact_transformed_coordinate_system":
                source["exact_transformed_coordinate_system"],
            "exact_transformed_open_cell":
                source["exact_transformed_open_cell"],
            "exact_transformed_cell_volume":
                source["exact_transformed_cell_volume"],
            "outer_envelope_used_as_inner_support": False,
            **zero_credit(),
        }))
    need(
        sum(refined_alias_source_histogram.values()) == 1_600,
        "refined alias target source census",
    )

    alias_rows.sort(
        key=lambda row: row["Round292_alias_binding_candidate_row_id"]
    )
    alias_ids = [
        row["Round292_alias_binding_candidate_row_id"] for row in alias_rows
    ]
    alias_sources = [row["alias_source_identity"] for row in alias_rows]
    need(
        len(alias_rows) == 46_288
        and len(set(alias_ids)) == 46_288
        and len(set(alias_sources)) == 46_288,
        "alias candidate injectivity",
    )
    for row in alias_rows:
        verify_alias_row_content_id(row)
        need(
            row["target_registry_occurrence_id"] in registry_by_occurrence
            and row["does_not_issue_new_occurrence_id"] is True
            and row["does_not_collapse_distinct_occurrence_ids"] is True
            and row["outer_envelope_used_as_inner_support"] is False
            and all(row[field] == 0 for field in ZERO_FIELDS),
            f"alias zero-credit target binding:{row['alias_source_identity']}",
        )

    registry_kind_histogram = Counter(
        row["registry_entry_kind"] for row in registry_rows
    )
    alias_kind_histogram = Counter(
        row["alias_source_kind"] for row in alias_rows
    )
    alias_target_kind_histogram = Counter(
        row["target_registry_entry_kind"] for row in alias_rows
    )
    candidate_new_ids = {
        row["registry_occurrence_id"]
        for row in registry_rows
        if row["registry_identity_status"]
        == "CANDIDATE_NEW_ID__NOT_FORMALLY_ISSUED"
    }
    preserved_ids = set(preserved_by_id)
    need(
        registry_kind_histogram
        == {
            "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE": 126_468,
            "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM": 295_336,
            "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT": 9_404,
        }
        and alias_kind_histogram
        == {
            "ROUND288_EXACT_EQUAL_EXISTING_SUPPORT_ENVELOPE": 36_680,
            "ROUND287_R275_REGION_INCLUSION_SUBCOVER": 2_476,
            "ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER": 5_532,
            "ROUND292_R287_EXACT_REFINED_EXISTING_SUBCOVER_CELL": 1_600,
        }
        and len(candidate_new_ids) == 304_740
        and candidate_new_ids.isdisjoint(preserved_ids),
        "revised registry and alias census",
    )

    registry_ledger = ledger_attachment(
        registry_rows,
        "Round292_registry_candidate_row_id",
        REGISTRY_LEDGER_SCHEMA,
        (
            "431208_CONDITIONAL_REGISTRY_ROWS__126468_PRESERVED__"
            "304740_CANDIDATE_NEW__WAITING_OVERLAP_AUDIT__ZERO_CREDIT"
        ),
        occurrence_field="registry_occurrence_id",
    )
    alias_ledger = ledger_attachment(
        alias_rows,
        "Round292_alias_binding_candidate_row_id",
        ALIAS_LEDGER_SCHEMA,
        (
            "46288_ALIAS_BINDING_CANDIDATES__36680_R288_EXISTING__"
            "8008_R287_ATOM_SUBCOVERS__1600_REFINED_EXISTING_SUBCOVERS__"
            "WAITING_OVERLAP_AUDIT__ZERO_CREDIT"
        ),
    )

    result = {
        "schema": SCHEMA,
        "status": (
            "ROUND292_REVISED_OCCURRENCE_REGISTRY_CANDIDATE_CONSTRUCTED__"
            "431208_REGISTRY_ROWS__46288_ALIAS_BINDINGS__"
            "304740_CANDIDATE_NEW__WAITING_OVERLAP_AUDIT__ZERO_CREDIT"
        ),
        "input_file_pins": dict(sorted(INPUT_SHA256.items())),
        "input_package_contract": {
            "all_selected_input_bytes_match_frozen_SHA256": True,
            "selected_R266_R287_R288_R290_manifest_bindings_match": True,
            "Round266_independent_verification_status":
                r266_verification["status"],
            "Round287_independent_verification_status":
                r287_verification["status"],
            "Round288_independent_verification_status":
                r288_verification["status"],
            "Round290_independent_verification_status":
                r290_verification["status"],
            "Round292_overlap_probe_candidate_status":
                probe_result["status"],
            "Round292_overlap_probe_independent_verifier_pinned": False,
            "Round292_overlap_probe_manifest_pinned": False,
            "reason_for_waiting":
                "the overlap probe candidate has not yet been frozen by an "
                "independent verifier/manifest in this input contract",
        },
        "superseded_naive_census": {
            "naive_Round287_union_direct_ID_count": 10_020,
            "naive_registry_candidate_count": 431_824,
            "naive_alias_row_count": 44_688,
            "direct_Round287_union_ID_issuance_valid": False,
            "Round287_union_with_existing_positive_volume_overlap_count": 920,
            "positive_volume_overlap_relation_count": 1_564,
            "fully_existing_covered_source_union_count": 616,
            "partially_existing_covered_source_union_count": 304,
            "occupied_existing_subcover_refinement_cell_count": 1_600,
            "uncovered_refinement_cell_count": 10_252,
            "refined_connected_new_support_count": 9_404,
            "supersession_rule":
                "only exact uncovered connected (t^2,p,s) refinement "
                "components may receive conditional candidate IDs",
        },
        "census": {
            "preserved_Round266_occurrence_ID_count": 126_468,
            "Round288_existing_alias_count": 36_680,
            "Round288_reserved_atom_candidate_new_count": 295_336,
            "Round287_atom_subcover_alias_count": 8_008,
            "Round292_refined_existing_subcover_alias_count": 1_600,
            "Round292_refined_R287_candidate_new_support_count": 9_404,
            "candidate_new_occurrence_count": 304_740,
            "conditional_registry_candidate_count": 431_208,
            "alias_binding_candidate_count": 46_288,
            "formal_registry_promotion_count": 0,
            "formal_new_occurrence_count": 0,
            "registry_entry_kind_histogram":
                dict(sorted(registry_kind_histogram.items())),
            "alias_source_kind_histogram":
                dict(sorted(alias_kind_histogram.items())),
            "alias_target_registry_kind_histogram":
                dict(sorted(alias_target_kind_histogram.items())),
            "Round266_source_histogram":
                dict(sorted(r266_source_histogram.items())),
            "Round266_R208_sign_histogram":
                dict(sorted(r208_sign_histogram.items())),
            "Round288_atom_state_histogram":
                dict(sorted(atom_state_histogram.items())),
            "refined_alias_target_source_histogram":
                dict(sorted(refined_alias_source_histogram.items())),
            "finite_registry_source_descriptor_count":
                len(occurrence_descriptors_by_id),
            "finite_registry_occurrence_ID_count":
                len(registry_occurrence_ids),
            "finite_registry_ID_collision_count": 0,
            "finite_registry_source_descriptor_collision_count": 0,
        },
        "identity_contract": {
            "Round266_local_occurrence_IDs_preserved_byte_for_byte": True,
            "Round288_reserved_atom_IDs_preserved_byte_for_byte": True,
            "Round290_support_rows_never_rewrite_Round288_atom_identity": True,
            "Round287_naive_union_IDs_never_used_as_occurrence_IDs": True,
            "Round292_refined_component_ID_rule":
                "source-g-expanded-occurrence:SHA256(canonical_json(["
                "'ROUND292_R287_EXISTING_OVERLAP_REFINED_NEW_SUPPORT_"
                "LOCAL_OCCURRENCE_V1',component_id,component_row_sha256]))",
            "finite_frozen_universe_source_to_ID_injective": True,
            "finite_frozen_universe_ID_to_source_collision_count": 0,
            "registry_row_IDs_content_addressed": True,
            "alias_row_IDs_content_addressed": True,
            "aliases_issue_no_occurrence_ID": True,
            "ordinary_face_never_collapses_occurrence_identity": True,
            "true_seam_never_collapses_occurrence_identity": True,
            "Jx_Jy_never_collapses_occurrence_identity": True,
        },
        "support_representation_contract": {
            "Round288_corridor_candidates_use_exact_Round279_inner_supports":
                True,
            "Round288_isolated_candidates_use_exact_Round290_inner_supports":
                True,
            "Round292_refined_R287_candidates_preserve_exact_transformed_cells":
                True,
            "Round292_refined_R287_cell_union_never_relabelled_as_one_box":
                True,
            "outer_envelope_ever_used_as_inner_support": False,
            "all_9404_refined_components_have_member_cell_provenance": True,
            "all_1600_occupied_cells_are_alias_bindings_only": True,
        },
        "overlap_scope": {
            "overlap_computation_performed_by_this_builder": False,
            "consumed_Round292_probe_positive_overlap_relation_count": 1_564,
            "consumed_Round292_probe_remaining_unresolved_overlap_count": 0,
            "consumed_Round292_probe_refined_component_count": 9_404,
            "consumed_Round292_probe_independent_verification_frozen": False,
            "registry_promotion_status": WAITING,
        },
        "registry_ledger": attachment_summary(
            registry_ledger, DEFAULT_REGISTRY_LEDGER.name
        ),
        "alias_ledger": attachment_summary(
            alias_ledger, DEFAULT_ALIAS_LEDGER.name
        ),
        "provenance": {
            "producer_sha256": producer_sha256,
            "seed_affects_output": False,
            "upstream_producer_imported_or_executed": False,
            "DSU_or_component_union_algorithm_executed": False,
            "seam_or_Jx_Jy_glue_algorithm_executed": False,
        },
        "strict_nonpromotion": {
            **zero_credit(),
            "formal_registry_promotion_count": 0,
            "formal_alias_binding_promotion_count": 0,
            "formal_expanded_occurrences": 126_468,
            "conditional_registry_candidate_count": 431_208,
            "conditional_candidate_new_count": 304_740,
            "registry_promotion_status": WAITING,
            "quotient_components": 63_224,
            "maximality": "0/63224",
            "exact_key_fibres": "0/116",
            "global_dispositions": "0/224580",
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": [
            "Independently verify and freeze the Round292 R287-registry "
            "overlap-exhaustion probe.",
            "Independently reconstruct this 431,208-row registry candidate "
            "and both content-address maps without importing this producer.",
            "Reject every attempt to restore the naive 10,020 direct-union "
            "issuance or the superseded 431,824 census.",
            "Only a later explicit promoting round may change any occurrence, "
            "alias, DSU, component, seam, Jx/Jy, maximality, fibre, or global "
            "disposition credit.",
        ],
    }
    return registry_ledger, alias_ledger, result


def deterministic_gzip(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        fileobj=buffer,
        mtime=0,
        compresslevel=9,
    ) as stream:
        for piece in chunks(value):
            stream.write(piece)
    return buffer.getvalue()


def safe_write(path: Path, payload: bytes) -> None:
    need(path.parent.resolve() == HERE.resolve(), f"output parent:{path}")
    with tempfile.NamedTemporaryFile(
        mode="wb",
        dir=HERE,
        prefix=f".{path.name}.",
        delete=False,
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--registry-ledger", type=Path, default=DEFAULT_REGISTRY_LEDGER
    )
    parser.add_argument(
        "--alias-ledger", type=Path, default=DEFAULT_ALIAS_LEDGER
    )
    parser.add_argument("--result", type=Path, default=DEFAULT_RESULT)
    parser.add_argument("--seed", default="292071")
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()

    producer_sha256 = file_sha256(Path(__file__).resolve())
    registry_ledger, alias_ledger, result = build(producer_sha256)
    registry_bytes = deterministic_gzip(registry_ledger)
    alias_bytes = deterministic_gzip(alias_ledger)
    result["registry_ledger"]["file_sha256"] = hashlib.sha256(
        registry_bytes
    ).hexdigest()
    result["alias_ledger"]["file_sha256"] = hashlib.sha256(
        alias_bytes
    ).hexdigest()
    result["seed_affects_output"] = False
    result["result_sha256"] = digest(result)
    result_bytes = canonical(result)
    if not arguments.no_write:
        safe_write(arguments.registry_ledger, registry_bytes)
        safe_write(arguments.alias_ledger, alias_bytes)
        safe_write(arguments.result, result_bytes)
    print(json.dumps({
        "status": result["status"],
        "seed": arguments.seed,
        "seed_affects_output": False,
        "registry_ledger_file_sha256":
            result["registry_ledger"]["file_sha256"],
        "alias_ledger_file_sha256":
            result["alias_ledger"]["file_sha256"],
        "result_file_sha256": hashlib.sha256(result_bytes).hexdigest(),
        "result_sha256": result["result_sha256"],
        "census": result["census"],
    }, sort_keys=True))
    del registry_ledger, alias_ledger, registry_bytes, alias_bytes
    gc.collect()


if __name__ == "__main__":
    main()
