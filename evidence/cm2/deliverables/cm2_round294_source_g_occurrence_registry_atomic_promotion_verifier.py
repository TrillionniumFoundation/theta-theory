#!/usr/bin/env python3
"""Independent cacheless verifier for the Round294 Stage-A registry.

The verifier never imports or executes either the Round294 producer or the
Round292 candidate builder.  It opens the frozen R266/R287/R288/R290 inputs,
the sealed Round292 overlap quartet, and the two Round294 ledgers directly.
It independently checks source-to-row exhaustiveness, content IDs, all closed
commitments, the exact promotion-credit partition, and targeted fully
reclosed forgeries.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import gzip
import hashlib
import io
import json
import mmap
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, Callable, Iterable
import zlib


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round294_source_g_occurrence_registry_atomic_promotion"
PRODUCER = HERE / f"{PREFIX}.py"
REGISTRY = HERE / f"{PREFIX}_registry_ledger.json.gz"
BINDINGS = HERE / f"{PREFIX}_representation_binding_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"
ATTACKS = HERE / f"{PREFIX}_attack_suite.json"
VERIFICATION = HERE / f"{PREFIX}_verification.json"

SCHEMA = "cm2.round294.source-g-occurrence-registry-atomic-promotion.v1"
REGISTRY_SCHEMA = "cm2.round294.source-g-occurrence-registry-ledger.v1"
BINDING_SCHEMA = (
    "cm2.round294.source-g-occurrence-representation-binding-ledger.v1"
)
PROMOTED = "FORMALLY_PROMOTED_ROUND294_ATOMIC_OCCURRENCE_REGISTRY"
MAX_FILE_BYTES = 1_100_000_000
MAX_GZIP_UNCOMPRESSED_BYTES = 2_000_000_000

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
OVERLAP_RESULT = (
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_result.json"
)
OVERLAP_LEDGER = (
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz"
)
OVERLAP_VERIFICATION = (
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_"
    "verification.json"
)
OVERLAP_MANIFEST = (
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_"
    "manifest.sha256"
)

INPUT_PINS = {
    PRODUCER.name:
        "6e0ab06cf6ab7dfb7868b2fe7a4699a914e6a3b0f8b18e4181d138bc2d887a9b",
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
    OVERLAP_RESULT:
        "f3887e75f4ef62459b75d8c77eee4781ec14f57651b4feb09b8d7ca8e372c508",
    OVERLAP_LEDGER:
        "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    OVERLAP_VERIFICATION:
        "7088e4f0927100e3c2b36f164e4f64e7b7aa0db5f81b4201c3967f16ba07ddfd",
    OVERLAP_MANIFEST:
        "4ea92e4112cae18aa0c13a6d2308816bafc19e4129c09d8b6be914268cfc4870",
}

MANIFEST_BINDINGS = {
    R266_MANIFEST: (R266_CERTIFICATE, R266_VERIFICATION),
    R287_MANIFEST: (R287_RESULT, R287_LEDGER, R287_VERIFICATION),
    R288_MANIFEST: (
        R288_RESULT, R288_ATOMS, R288_OVERLAPS, R288_VERIFICATION,
    ),
    R290_MANIFEST: (R290_RESULT, R290_LEDGER, R290_VERIFICATION),
    OVERLAP_MANIFEST: (
        OVERLAP_RESULT, OVERLAP_LEDGER, OVERLAP_VERIFICATION,
    ),
}

ZERO_UNPROMOTED_FIELDS = (
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
R287_ALIAS = (
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


class VerificationError(RuntimeError):
    """Fail-closed verification error."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


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
    for piece in chunks(value):
        state.update(piece)
    return state.hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1024 * 1024), b""):
            state.update(piece)
    return state.hexdigest()


def require_safe_regular(path: Path, max_bytes: int = MAX_FILE_BYTES) -> None:
    need(
        path.parent.resolve() == HERE.resolve(),
        f"HERE-only path:{path}",
    )
    try:
        metadata = path.lstat()
    except FileNotFoundError as error:
        raise VerificationError(f"missing file:{path}") from error
    need(
        stat.S_ISREG(metadata.st_mode)
        and not path.is_symlink()
        and metadata.st_nlink == 1
        and 0 < metadata.st_size <= max_bytes,
        f"safe regular single-link bounded file:{path}",
    )


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        need(key not in value, f"duplicate JSON key:{key}")
        value[key] = item
    return value


def strict_integer(text: str) -> int:
    need(
        re.fullmatch(r"-?(?:0|[1-9][0-9]*)", text) is not None
        and len(text.lstrip("-")) <= 128,
        "strict bounded JSON integer",
    )
    return int(text)


def reject_float(text: str) -> Any:
    raise VerificationError(f"non-integral JSON number rejected:{text}")


def reject_constant(text: str) -> Any:
    raise VerificationError(f"nonfinite JSON number rejected:{text}")


def strict_json_load(stream: Any) -> Any:
    return json.load(
        stream,
        object_pairs_hook=unique_object,
        parse_int=strict_integer,
        parse_float=reject_float,
        parse_constant=reject_constant,
    )


def strict_json_bytes(payload: bytes) -> Any:
    return json.loads(
        payload,
        object_pairs_hook=unique_object,
        parse_int=strict_integer,
        parse_float=reject_float,
        parse_constant=reject_constant,
    )


def scan_single_member_gzip(
    path: Path,
    max_uncompressed: int = MAX_GZIP_UNCOMPRESSED_BYTES,
) -> int:
    require_safe_regular(path)
    decoder = zlib.decompressobj(wbits=31)
    total = 0
    with path.open("rb") as stream:
        while True:
            piece = stream.read(1024 * 1024)
            if not piece:
                break
            need(not decoder.eof, f"trailing or multi-member gzip:{path}")
            output = decoder.decompress(piece)
            total += len(output)
            need(
                total <= max_uncompressed,
                f"gzip uncompressed size cap:{path}",
            )
            need(
                not decoder.unused_data,
                f"trailing or multi-member gzip:{path}",
            )
    total += len(decoder.flush())
    need(
        decoder.eof
        and not decoder.unused_data
        and total <= max_uncompressed,
        f"strict single-member gzip:{path}",
    )
    return total


def scan_single_member_gzip_bytes(
    payload: bytes,
    max_uncompressed: int,
) -> int:
    decoder = zlib.decompressobj(wbits=31)
    output = decoder.decompress(payload)
    total = len(output)
    need(
        decoder.eof
        and not decoder.unused_data
        and total <= max_uncompressed,
        "strict bounded single-member gzip bytes",
    )
    return total


def read_json(
    path: Path, *, require_canonical_bytes: bool = False
) -> dict[str, Any]:
    require_safe_regular(path)
    with path.open("rt", encoding="utf-8", newline="") as stream:
        value = strict_json_load(stream)
    need(isinstance(value, dict), f"JSON object:{path.name}")
    if require_canonical_bytes:
        need(
            path.read_bytes() == canonical(value),
            f"canonical single-document JSON bytes:{path.name}",
        )
    return value


def read_gzip(path: Path) -> dict[str, Any]:
    scan_single_member_gzip(path)
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        value = strict_json_load(stream)
    need(isinstance(value, dict), f"gzip JSON object:{path.name}")
    return value


def closed(row: dict[str, Any], label: str) -> None:
    payload = dict(row)
    expected = payload.pop("row_sha256", None)
    need(expected == digest(payload), f"closed row:{label}")


def self_digest(
    document: dict[str, Any], field: str, label: str
) -> None:
    payload = dict(document)
    expected = payload.pop(field, None)
    need(expected == digest(payload), f"self digest:{label}")


def parse_manifest(name: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in (HERE / name).read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, f"manifest syntax:{name}")
        sha256, filename = match.groups()
        need(filename not in entries, f"manifest duplicate:{name}:{filename}")
        entries[filename] = sha256
    return entries


def validate_input_package() -> None:
    for name in sorted(INPUT_PINS):
        require_safe_regular(HERE / name)
    actual = {
        name: file_sha256(HERE / name)
        for name in sorted(INPUT_PINS)
    }
    need(actual == dict(sorted(INPUT_PINS.items())), "complete input pins")
    for manifest, filenames in MANIFEST_BINDINGS.items():
        entries = parse_manifest(manifest)
        for filename in filenames:
            need(
                entries.get(filename) == INPUT_PINS[filename],
                f"manifest binding:{manifest}:{filename}",
            )
    status_specs = (
        (
            R266_VERIFICATION,
            "PASS_INDEPENDENT_ROUND266",
        ),
        (
            R287_VERIFICATION,
            "PASS_INDEPENDENT_ROUND287_TERMINAL_OCCURRENCE_DISPOSITION",
        ),
        (
            R288_VERIFICATION,
            "PASS_INDEPENDENT_CACHELESS_ROUND288",
        ),
        (
            R290_VERIFICATION,
            "PASS_INDEPENDENT_CACHELESS_ROUND290",
        ),
        (
            OVERLAP_VERIFICATION,
            "PASS_INDEPENDENT_CACHELESS_ROUND292_R287_REGISTRY_OVERLAP",
        ),
    )
    for filename, prefix in status_specs:
        value = read_json(HERE / filename)
        need(
            value.get("status", "").startswith(prefix),
            f"verification freeze:{filename}",
        )
    overlap = read_json(HERE / OVERLAP_VERIFICATION)
    self_digest(overlap, "verification_sha256", "Round292 overlap")
    need(
        overlap["independent_reconstruction"][
            "refined_new_support_component_count"
        ] == 9_404
        and overlap["independent_reconstruction"][
            "occupied_unique_target_refinement_cell_count"
        ] == 1_600
        and overlap["independent_reconstruction"][
            "pairwise_unresolved_positive_overlap_count"
        ] == 0
        and overlap["targeted_reclosed_attacks"][
            "all_targeted_resigned_attacks_rejected"
        ] is True,
        "sealed Round292 overlap verification semantics",
    )


def validate_ledger(
    value: dict[str, Any],
    *,
    schema: str,
    count: int,
    id_field: str,
) -> list[dict[str, Any]]:
    rows = value.get("rows")
    need(
        value.get("schema") == schema
        and value.get("row_count") == count
        and isinstance(rows, list)
        and len(rows) == count
        and value.get("every_row_closed_by_own_SHA256") is True,
        f"ledger envelope:{schema}",
    )
    ids = [row[id_field] for row in rows]
    need(
        len(set(ids)) == count
        and value.get("row_ids_sha256") == digest(ids)
        and value.get("row_hashes_sha256")
        == digest([row["row_sha256"] for row in rows])
        and value.get("rows_sha256") == digest(rows),
        f"ledger commitments:{schema}",
    )
    for row in rows:
        closed(row, row[id_field])
    return rows


def verify_promoted_registry_row(row: dict[str, Any]) -> None:
    closed(row, row["Round294_occurrence_registry_row_id"])
    payload = dict(row)
    payload.pop("row_sha256")
    row_id = payload.pop("Round294_occurrence_registry_row_id")
    need(
        row_id == "round294-occurrence-registry:" + digest([
            "ROUND294_ATOMIC_OCCURRENCE_REGISTRY_ROW_V1", payload
        ]),
        f"Round294 registry content ID:{row_id}",
    )
    old_id = payload.pop("source_Round292_registry_candidate_row_id")
    old_hash = payload.pop("source_Round292_registry_candidate_row_sha256")
    is_new = (
        row["registry_identity_status"]
        == "FORMALLY_ISSUED_ROUND294_ATOMIC_OCCURRENCE_ID"
    )
    need(
        row["registry_promotion_status"] == PROMOTED
        and row["formal_new_expanded_occurrence_credit"] == int(is_new)
        and row["formal_occurrence_alias_credit"] == 0
        and all(row[field] == 0 for field in ZERO_UNPROMOTED_FIELDS),
        f"registry promotion credit:{row_id}",
    )
    payload.update({
        "registry_identity_status": (
            "CANDIDATE_NEW_ID__NOT_FORMALLY_ISSUED"
            if is_new else
            "PRESERVED_EXISTING_ID__NO_ROUND292_PROMOTION"
        ),
        "registry_promotion_status": "WAITING_OVERLAP_AUDIT",
        "formal_new_expanded_occurrence_credit": 0,
        "formal_occurrence_alias_credit": 0,
    })
    expected_old_id = "round292-registry-candidate:" + digest([
        "ROUND292_OCCURRENCE_REGISTRY_CANDIDATE_ROW_V2", payload
    ])
    old_row = {
        "Round292_registry_candidate_row_id": expected_old_id,
        **payload,
    }
    need(
        old_id == expected_old_id and old_hash == digest(old_row),
        f"independent Round292 candidate reverse closure:{row_id}",
    )


def verify_promoted_binding_row(row: dict[str, Any]) -> None:
    closed(
        row, row["Round294_occurrence_representation_binding_row_id"]
    )
    payload = dict(row)
    payload.pop("row_sha256")
    row_id = payload.pop(
        "Round294_occurrence_representation_binding_row_id"
    )
    need(
        row_id
        == "round294-occurrence-representation-binding:" + digest([
            "ROUND294_ATOMIC_OCCURRENCE_REPRESENTATION_BINDING_ROW_V1",
            payload,
        ]),
        f"Round294 binding content ID:{row_id}",
    )
    old_id = payload.pop(
        "source_Round292_alias_binding_candidate_row_id"
    )
    old_hash = payload.pop(
        "source_Round292_alias_binding_candidate_row_sha256"
    )
    need(
        row["alias_binding_status"]
        == "FORMALLY_RECORDED_ROUND294_REPRESENTATION_BINDING"
        and row["formal_new_expanded_occurrence_credit"] == 0
        and row["formal_occurrence_alias_credit"] == 1
        and row["does_not_issue_new_occurrence_id"] is True
        and row["does_not_collapse_distinct_occurrence_ids"] is True
        and all(row[field] == 0 for field in ZERO_UNPROMOTED_FIELDS),
        f"binding promotion credit:{row_id}",
    )
    payload.update({
        "alias_binding_status": "WAITING_OVERLAP_AUDIT",
        "formal_new_expanded_occurrence_credit": 0,
        "formal_occurrence_alias_credit": 0,
    })
    expected_old_id = "round292-alias-binding-candidate:" + digest([
        "ROUND292_OCCURRENCE_ALIAS_BINDING_CANDIDATE_ROW_V2", payload
    ])
    old_row = {
        "Round292_alias_binding_candidate_row_id": expected_old_id,
        **payload,
    }
    need(
        old_id == expected_old_id and old_hash == digest(old_row),
        f"independent Round292 binding reverse closure:{row_id}",
    )


def load_r266_rows() -> list[dict[str, Any]]:
    marker = b'"formal_post_Round266_expanded_occurrence_frontier_ledger":'
    end_marker = b',"formal_post_Round266_key_frontier_ledger":'
    with (HERE / R266_CERTIFICATE).open("rb") as stream, mmap.mmap(
        stream.fileno(), 0, access=mmap.ACCESS_READ
    ) as mapped:
        start = mapped.find(marker)
        need(start >= 0, "Round266 ledger marker")
        start += len(marker)
        end = mapped.find(end_marker, start)
        need(end > start, "Round266 ledger terminator")
        table = strict_json_bytes(mapped[start:end])
    rows = table["rows"]
    need(
        table["row_count"] == len(rows) == 126_468
        and table["rows_sha256"]
        == "441cde017675dc279a55d52f47c24c31721309ad1cb03e1ea831e6984569f351"
        == digest(rows),
        "Round266 occurrence table commitment",
    )
    for row in rows:
        closed(
            row, row["post_Round266_expanded_occurrence_frontier_row_id"]
        )
    return rows


def validate_standard_source(
    value: dict[str, Any],
    *,
    schema: str,
    count: int,
    id_field: str,
) -> list[dict[str, Any]]:
    return validate_ledger(
        value, schema=schema, count=count, id_field=id_field
    )


def validate_r287(value: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    need(
        value.get("schema")
        == "cm2.round287.source-g-rechart-terminal-occurrence-disposition."
        "ledger.v1",
        "Round287 schema",
    )
    specs = {
        "potential_new_support_union_rows": (
            10_020, "Round287_potential_new_support_union_id",
        ),
        "refinement_cell_rows": (
            7_616, "Round287_refinement_cell_disposition_row_id",
        ),
        "region_rows": (
            13_788, "Round287_region_disposition_row_id",
        ),
    }
    tables: dict[str, list[dict[str, Any]]] = {}
    for key, (count, id_field) in specs.items():
        rows = value.get(key)
        need(
            isinstance(rows, list)
            and len(rows) == count
            and value.get(key.removesuffix("s") + "_count") == count
            and value.get(key + "_sha256") == digest(rows),
            f"Round287 table:{key}",
        )
        for row in rows:
            closed(row, row[id_field])
        tables[key] = rows
    return tables


def probe_row_id(row: dict[str, Any]) -> str:
    for field in (
        "Round292_registry_overlap_row_id",
        "Round292_R287_existing_overlap_refinement_cell_id",
        "Round292_refined_new_support_component_id",
    ):
        if field in row:
            return row[field]
    raise VerificationError("unknown Round292 overlap row")


def positive_box(box: list[str], label: str) -> None:
    values = list(map(Fraction, box))
    need(
        len(values) == 6
        and all(values[2 * axis] < values[2 * axis + 1] for axis in range(3)),
        f"positive box:{label}",
    )


def audit_result(value: dict[str, Any]) -> None:
    self_digest(value, "result_sha256", "Round294 result")
    census = value.get("census", {})
    credits = value.get("formal_credit_transition", {})
    scope = value.get("scope_contract", {})
    freeze = value.get("nonpromotion_freeze", {})
    superseded = value.get("superseded_census_rejection", {})
    need(
        value.get("schema") == SCHEMA
        and value.get("status", "").startswith(
            "PASS_ROUND294_ATOMIC_STAGE_A_OCCURRENCE_REGISTRY_PROMOTION"
        )
        and census.get("formal_occurrence_registry_row_count") == 431_208
        and census.get("preserved_Round266_occurrence_count") == 126_468
        and census.get("formal_new_Round288_atom_occurrence_count") == 295_336
        and census.get("formal_new_refined_Round287_occurrence_count") == 9_404
        and census.get("formal_new_occurrence_count") == 304_740
        and census.get("formal_expanded_occurrence_count") == 431_208
        and census.get("formal_representation_binding_count") == 46_288
        and credits == {
            "formal_new_expanded_occurrence_credit": 304_740,
            "formal_occurrence_alias_credit": 46_288,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_seam_edge_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        }
        and superseded.get("superseded_registry_row_count") == 431_824
        and superseded.get("superseded_direct_Round287_union_issuance_count")
        == 10_020
        and superseded.get("superseded_registry_row_count_accepted") is False
        and superseded.get("direct_Round287_union_issuance_accepted") is False
        and scope.get("registry_scope")
        == "CURRENT_FORMAL_STAGE_A_OPEN_3D_PLUS_R287_REFINED_FRONTIER"
        and scope.get("final_exhaustive_all_stratum_registry_claimed") is False
        and scope.get("final_registry_count") is None
        and scope.get("known_lower_stratum_gap_frontier_R291") == 576
        and scope.get("known_R289_incidence_refinement_frontier") == 396
        and freeze.get(
            "legacy_pre_Round294_preserved_registry_quotient_components"
        ) == 63_224
        and freeze.get(
            "post_Round294_expanded_registry_component_DSU_status"
        ) == "NOT_REBUILT"
        and freeze.get("post_Round294_quotient_component_count") is None
        and freeze.get("post_Round294_maximality_status")
        == "WAITING_EXPANDED_REGISTRY_DSU"
        and freeze.get("post_Round294_exact_key_fibre_status")
        == "WAITING_EXPANDED_REGISTRY_DSU"
        and freeze.get("post_Round294_global_disposition_status")
        == "WAITING_EXPANDED_REGISTRY_DSU"
        and freeze.get("Gate5") == "10/18"
        and freeze.get("D02") == "BLOCKED"
        and freeze.get("CM2") == "NO-GO_FOR_CLAIM",
        "exact Round294 result semantics",
    )


def reclose_result(value: dict[str, Any]) -> None:
    value.pop("result_sha256", None)
    value["result_sha256"] = digest(value)


def expect_rejected(
    attack_id: str,
    callback: Callable[[], None],
    *,
    fully_reclosed: bool = True,
) -> dict[str, Any]:
    try:
        callback()
    except (VerificationError, KeyError, TypeError, ValueError) as error:
        payload = {
            "attack_id": attack_id,
            "attack_fully_reclosed": fully_reclosed,
            "rejected": True,
            "rejection_class": type(error).__name__,
        }
    else:
        raise VerificationError(f"attack accepted:{attack_id}")
    payload["row_sha256"] = digest(payload)
    return payload


def reclose_registry_row(row: dict[str, Any]) -> None:
    row.pop("row_sha256", None)
    payload = dict(row)
    payload.pop("Round294_occurrence_registry_row_id", None)
    row["Round294_occurrence_registry_row_id"] = (
        "round294-occurrence-registry:" + digest([
            "ROUND294_ATOMIC_OCCURRENCE_REGISTRY_ROW_V1", payload
        ])
    )
    # ID is first under canonical JSON regardless of insertion order.
    row["row_sha256"] = digest({
        "Round294_occurrence_registry_row_id":
            row["Round294_occurrence_registry_row_id"],
        **{
            key: value for key, value in row.items()
            if key not in {
                "Round294_occurrence_registry_row_id", "row_sha256"
            }
        },
    })


def reclose_binding_row(row: dict[str, Any]) -> None:
    row.pop("row_sha256", None)
    payload = dict(row)
    payload.pop(
        "Round294_occurrence_representation_binding_row_id", None
    )
    row_id = "round294-occurrence-representation-binding:" + digest([
        "ROUND294_ATOMIC_OCCURRENCE_REPRESENTATION_BINDING_ROW_V1",
        payload,
    ])
    row["Round294_occurrence_representation_binding_row_id"] = row_id
    row["row_sha256"] = digest({
        "Round294_occurrence_representation_binding_row_id": row_id,
        **{
            key: value for key, value in row.items()
            if key not in {
                "Round294_occurrence_representation_binding_row_id",
                "row_sha256",
            }
        },
    })


def attacks(
    result: dict[str, Any],
    sample_registry: dict[str, Any],
    sample_binding: dict[str, Any],
    artifact_paths: dict[str, Path],
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []

    def result_attack(
        attack_id: str, mutator: Callable[[dict[str, Any]], None]
    ) -> None:
        forged = deepcopy(result)
        mutator(forged)
        reclose_result(forged)
        rows.append(expect_rejected(attack_id, lambda: audit_result(forged)))

    result_attack(
        "RECLOSED_SUPERSEDED_REGISTRY_CENSUS_431824",
        lambda value: value["census"].update({
            "formal_occurrence_registry_row_count": 431_824,
            "formal_expanded_occurrence_count": 431_824,
        }),
    )
    result_attack(
        "RECLOSED_DIRECT_R287_UNION_ISSUANCE_10020",
        lambda value: value["census"].update({
            "formal_new_refined_Round287_occurrence_count": 10_020,
            "formal_new_occurrence_count": 305_356,
        }),
    )
    result_attack(
        "RECLOSED_LEGACY_63224_FORGED_AS_CURRENT_QUOTIENT",
        lambda value: value["nonpromotion_freeze"].update({
            "post_Round294_quotient_component_count": 63_224,
        }),
    )
    result_attack(
        "RECLOSED_FINAL_ALL_STRATUM_REGISTRY_FORGE",
        lambda value: value["scope_contract"].update({
            "final_exhaustive_all_stratum_registry_claimed": True,
            "final_registry_count": 431_208,
        }),
    )
    result_attack(
        "RECLOSED_COMPONENT_DSU_CREDIT_FORGE",
        lambda value: value["formal_credit_transition"].update({
            "formal_component_union_credit": 1,
        }),
    )
    result_attack(
        "RECLOSED_GATE5_PROMOTION_FORGE",
        lambda value: value["nonpromotion_freeze"].update({
            "Gate5": "11/18",
        }),
    )
    result_attack(
        "RECLOSED_CM2_GO_FORGE",
        lambda value: value["nonpromotion_freeze"].update({
            "CM2": "GO",
        }),
    )

    forged_registry = deepcopy(sample_registry)
    forged_registry["formal_DSU_rank_reduction_credit"] = 1
    reclose_registry_row(forged_registry)
    rows.append(expect_rejected(
        "RECLOSED_REGISTRY_ROW_DSU_CREDIT",
        lambda: verify_promoted_registry_row(forged_registry),
    ))

    forged_registry = deepcopy(sample_registry)
    forged_registry["registry_entry_kind"] = (
        "CANDIDATE_NEW_ROUND287_DIRECT_UNION_FORBIDDEN"
    )
    forged_registry["registry_occurrence_id"] = (
        "source-g-expanded-occurrence:" + "0" * 64
    )
    reclose_registry_row(forged_registry)
    rows.append(expect_rejected(
        "RECLOSED_DIRECT_R287_UNION_REGISTRY_ROW",
        lambda: verify_promoted_registry_row(forged_registry),
    ))

    forged_binding = deepcopy(sample_binding)
    forged_binding["does_not_issue_new_occurrence_id"] = False
    reclose_binding_row(forged_binding)
    rows.append(expect_rejected(
        "RECLOSED_BINDING_ISSUES_OCCURRENCE_ID",
        lambda: verify_promoted_binding_row(forged_binding),
    ))

    forged_binding = deepcopy(sample_binding)
    forged_binding["does_not_collapse_distinct_occurrence_ids"] = False
    reclose_binding_row(forged_binding)
    rows.append(expect_rejected(
        "RECLOSED_BINDING_COLLAPSES_IDENTITIES",
        lambda: verify_promoted_binding_row(forged_binding),
    ))

    parser_cases: tuple[tuple[str, bytes], ...] = (
        ("JSON_DUPLICATE_KEY", b'{"x":1,"x":2}'),
        ("JSON_NAN_NONFINITE", b'{"x":NaN}'),
        ("JSON_INFINITY_NONFINITE", b'{"x":Infinity}'),
        ("JSON_FLOAT_NUMBER", b'{"x":1.5}'),
        ("JSON_OVERSIZED_INTEGER", b'{"x":' + b"9" * 129 + b"}"),
        ("JSON_TRAILING_DOCUMENT", b'{"x":1}{"y":2}'),
    )
    for attack_id, payload in parser_cases:
        rows.append(expect_rejected(
            attack_id,
            lambda payload=payload: strict_json_bytes(payload),
            fully_reclosed=False,
        ))

    first = gzip.compress(b'{"x":1}', mtime=0)
    second = gzip.compress(b'{"y":2}', mtime=0)
    gzip_cases: tuple[tuple[str, bytes, int], ...] = (
        ("GZIP_MULTI_MEMBER", first + second, 1024),
        ("GZIP_TRAILING_BYTES", first + b"TRAILING", 1024),
        ("GZIP_UNCOMPRESSED_SIZE_CAP", gzip.compress(b"x" * 11, mtime=0), 10),
    )
    for attack_id, payload, cap in gzip_cases:
        rows.append(expect_rejected(
            attack_id,
            lambda payload=payload, cap=cap:
                scan_single_member_gzip_bytes(payload, cap),
            fully_reclosed=False,
        ))

    def fresh_path(label: str) -> Path:
        with tempfile.NamedTemporaryFile(
            dir=HERE,
            prefix=f".round294_{label}_",
            delete=True,
        ) as stream:
            return Path(stream.name)

    def clean(path: Path) -> None:
        if path.is_symlink() or path.exists():
            if path.is_dir() and not path.is_symlink():
                path.rmdir()
            else:
                path.unlink()

    path_attack_types = (
        "SYMLINK", "HARDLINK", "FIFO", "DIRECTORY", "MISSING",
        "ESCAPE", "OVERSIZE",
    )
    for artifact_kind, actual in artifact_paths.items():
        for attack_type in path_attack_types:
            if attack_type == "ESCAPE":
                candidate = HERE.parent / (
                    f".round294_escape_{artifact_kind.lower()}"
                )
                rows.append(expect_rejected(
                    f"{artifact_kind}_PATH_ESCAPE",
                    lambda candidate=candidate:
                        require_safe_regular(candidate),
                    fully_reclosed=False,
                ))
                continue
            candidate = fresh_path(
                f"{artifact_kind.lower()}_{attack_type.lower()}"
            )
            try:
                if attack_type == "SYMLINK":
                    os.symlink(actual.resolve(), candidate)
                elif attack_type == "HARDLINK":
                    os.link(actual, candidate)
                elif attack_type == "FIFO":
                    os.mkfifo(candidate)
                elif attack_type == "DIRECTORY":
                    candidate.mkdir()
                elif attack_type == "OVERSIZE":
                    with candidate.open("wb") as stream:
                        stream.truncate(MAX_FILE_BYTES + 1)
                elif attack_type != "MISSING":
                    raise AssertionError(attack_type)
                rows.append(expect_rejected(
                    f"{artifact_kind}_PATH_{attack_type}",
                    lambda candidate=candidate:
                        require_safe_regular(candidate),
                    fully_reclosed=False,
                ))
            finally:
                clean(candidate)

    semantic_attack_count = sum(
        row["attack_fully_reclosed"] for row in rows
    )
    parser_and_path_attack_count = len(rows) - semantic_attack_count
    value = {
        "schema":
            "cm2.round294.source-g-occurrence-registry-atomic-promotion."
            "attack-suite.v1",
        "status":
            "PASS_ALL_ROUND294_RECLOSED_SEMANTIC_AND_STRUCTURAL_"
            "ATTACKS_REJECTED",
        "attack_count": len(rows),
        "rejected_attack_count": len(rows),
        "fully_reclosed_semantic_attack_count": semantic_attack_count,
        "parser_gzip_path_attack_count": parser_and_path_attack_count,
        "all_semantic_attacks_fully_reclosed": True,
        "all_attacks_rejected": True,
        "strict_single_document_JSON_enforced": True,
        "duplicate_key_nonfinite_float_huge_integer_trailing_JSON_rejected":
            True,
        "strict_single_member_bounded_GZIP_enforced": True,
        "multi_member_trailing_and_uncompressed_size_cap_GZIP_rejected": True,
        "HERE_only_regular_non_symlink_non_hardlink_bounded_files_enforced":
            True,
        "symlink_hardlink_FIFO_directory_missing_escape_oversize_rejected":
            True,
        "explicit_superseded_431824_rejection": True,
        "explicit_direct_R287_10020_issuance_rejection": True,
        "explicit_legacy_63224_current_quotient_rejection": True,
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows_sha256": digest(rows),
        "rows": rows,
    }
    value["attack_suite_sha256"] = digest(value)
    return value


def safe_write(path: Path, payload: bytes) -> None:
    need(path.parent.resolve() == HERE.resolve(), f"output parent:{path}")
    with tempfile.NamedTemporaryFile(
        mode="wb", dir=HERE, prefix=f".{path.name}.", delete=False
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry-ledger", type=Path, default=REGISTRY)
    parser.add_argument(
        "--representation-binding-ledger", type=Path, default=BINDINGS
    )
    parser.add_argument("--result", type=Path, default=RESULT)
    parser.add_argument("--attack-output", type=Path, default=ATTACKS)
    parser.add_argument("--verification", type=Path, default=VERIFICATION)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()

    require_safe_regular(Path(__file__).resolve())
    validate_input_package()
    result = read_json(arguments.result, require_canonical_bytes=True)
    audit_result(result)
    registry_value = read_gzip(arguments.registry_ledger)
    binding_value = read_gzip(arguments.representation_binding_ledger)
    registry_rows = validate_ledger(
        registry_value,
        schema=REGISTRY_SCHEMA,
        count=431_208,
        id_field="Round294_occurrence_registry_row_id",
    )
    binding_rows = validate_ledger(
        binding_value,
        schema=BINDING_SCHEMA,
        count=46_288,
        id_field="Round294_occurrence_representation_binding_row_id",
    )
    need(
        result["registry_ledger"]["file_sha256"]
        == file_sha256(arguments.registry_ledger)
        and result["representation_binding_ledger"]["file_sha256"]
        == file_sha256(arguments.representation_binding_ledger),
        "result output byte bindings",
    )

    for row in registry_rows:
        verify_promoted_registry_row(row)
    for row in binding_rows:
        verify_promoted_binding_row(row)
    registry_by_occurrence = {
        row["registry_occurrence_id"]: row for row in registry_rows
    }
    binding_by_source = {
        row["alias_source_identity"]: row for row in binding_rows
    }
    need(
        len(registry_by_occurrence) == 431_208
        and len(binding_by_source) == 46_288,
        "output identity injectivity",
    )

    expected_registry_sources: set[str] = set()
    expected_binding_sources: set[str] = set()
    r266_source_histogram: Counter[str] = Counter()
    for source in load_r266_rows():
        occurrence_id = source["local_occurrence_row_id"]
        output = registry_by_occurrence.get(occurrence_id)
        need(
            output is not None
            and output["registry_source_identity"]
            == f"ROUND266_LOCAL_OCCURRENCE::{occurrence_id}"
            and output["registry_entry_kind"]
            == "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
            and output["source_row_id"]
            == source["post_Round266_expanded_occurrence_frontier_row_id"]
            and output["source_row_sha256"] == source["row_sha256"]
            and output["source_occurrence_class"]
            == source["occurrence_source"]
            and output["formal_new_expanded_occurrence_credit"] == 0,
            f"Round266 preserved registry reconstruction:{occurrence_id}",
        )
        expected_registry_sources.add(output["registry_source_identity"])
        r266_source_histogram[source["occurrence_source"]] += 1
    need(
        r266_source_histogram == {
            "ROUND174_RESOLVED": 72_500,
            "ROUND179_RESOLVED": 17_192,
            "ROUND204_REGION": 736,
            "ROUND208_REGION": 36_040,
        },
        "Round266 source histogram",
    )

    atom_rows = validate_standard_source(
        read_gzip(HERE / R288_ATOMS),
        schema="cm2.round288.canonical-atom-occurrence-disposition-ledger.v1",
        count=332_016,
        id_field="Round288_atom_disposition_row_id",
    )
    atom_info: dict[str, tuple[str, str, str]] = {}
    isolated_atoms: set[str] = set()
    atom_states: Counter[str] = Counter()
    for atom in atom_rows:
        atom_id = atom["canonical_atom_id"]
        state = atom["occurrence_identity_disposition"]
        atom_states[state] += 1
        occurrence_id = (
            atom["existing_local_occurrence_row_id"]
            if state in R288_EXISTING_STATES else
            atom["reserved_candidate_occurrence_id__not_issued"]
        )
        need(
            isinstance(occurrence_id, str)
            and atom["Round288_atom_disposition_row_id"]
            == "round288-atom-disposition:" + digest(atom_id),
            f"Round288 atom identity:{atom_id}",
        )
        atom_info[atom_id] = (
            occurrence_id,
            atom["Round288_atom_disposition_row_id"],
            atom["row_sha256"],
        )
        if state in R288_EXISTING_STATES:
            need(
                occurrence_id in registry_by_occurrence,
                f"Round288 existing target:{atom_id}",
            )
            continue
        output = registry_by_occurrence.get(occurrence_id)
        need(
            output is not None
            and output["registry_source_identity"]
            == f"ROUND288_CANONICAL_ATOM::{atom_id}"
            and output["registry_entry_kind"]
            == "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
            and output["source_row_id"]
            == atom["Round288_atom_disposition_row_id"]
            and output["source_row_sha256"] == atom["row_sha256"]
            and output["formal_new_expanded_occurrence_credit"] == 1
            and output["canonical_atom_id"] == atom_id,
            f"Round288 new registry reconstruction:{atom_id}",
        )
        if state == R288_READY_STATE:
            selected = atom["selected_Round279_strict_inner_corridor"]
            need(
                output["support_representation_kind"]
                == "ROUND279_DYNAMIC_STRICT_INWARD_CORRIDOR_INNER_SUPPORT"
                and output["positive_volume_rational_inner_support_box"]
                == selected[
                    "exact_positive_volume_rational_inner_support_box"
                ]
                and output["exact_inner_support_volume"]
                == selected["exact_inner_support_volume"],
                f"Round288 corridor support:{atom_id}",
            )
        else:
            need(state == R288_ISOLATED_STATE, f"known atom state:{atom_id}")
            isolated_atoms.add(atom_id)
        expected_registry_sources.add(output["registry_source_identity"])
    need(
        atom_states[R288_READY_STATE] == 274_176
        and atom_states[R288_ISOLATED_STATE] == 21_160
        and sum(atom_states[state] for state in R288_EXISTING_STATES) == 36_680,
        "Round288 state census",
    )

    r290_rows = validate_standard_source(
        read_gzip(HERE / R290_LEDGER),
        schema="cm2.round290.isolated-atom-inner-support-ledger.v1",
        count=21_160,
        id_field="Round290_inner_support_row_id",
    )
    seen_r290: set[str] = set()
    for source in r290_rows:
        atom_id = source["canonical_atom_id"]
        occurrence_id = atom_info[atom_id][0]
        output = registry_by_occurrence[occurrence_id]
        positive_box(
            source["exact_positive_volume_rational_inner_support_box"],
            atom_id,
        )
        need(
            atom_id in isolated_atoms
            and output["support_representation_kind"]
            == "ROUND290_ISOLATED_ATOM_RATIONAL_INNER_SUPPORT"
            and output["source_Round290_inner_support_row_id"]
            == source["Round290_inner_support_row_id"]
            and output["source_Round290_inner_support_row_sha256"]
            == source["row_sha256"]
            and output["positive_volume_rational_inner_support_box"]
            == source["exact_positive_volume_rational_inner_support_box"]
            and output["exact_inner_support_volume"]
            == source["exact_inner_support_volume"],
            f"Round290 support reconstruction:{atom_id}",
        )
        seen_r290.add(atom_id)
    need(seen_r290 == isolated_atoms, "complete Round290 support join")

    overlap_relations = validate_standard_source(
        read_gzip(HERE / R288_OVERLAPS),
        schema="cm2.round288.existing-occurrence-overlap-relation-ledger.v1",
        count=36_680,
        id_field="Round288_existing_overlap_relation_row_id",
    )
    for source in overlap_relations:
        atom_id = source["canonical_atom_id"]
        identity = f"ROUND288_CANONICAL_ATOM_REPRESENTATION::{atom_id}"
        output = binding_by_source.get(identity)
        need(
            output is not None
            and output["alias_source_kind"]
            == "ROUND288_EXACT_EQUAL_EXISTING_SUPPORT_ENVELOPE"
            and output["source_row_id"]
            == source["Round288_existing_overlap_relation_row_id"]
            and output["source_row_sha256"] == source["row_sha256"]
            and output["target_registry_occurrence_id"]
            == source["existing_local_occurrence_row_id"]
            == atom_info[atom_id][0],
            f"Round288 binding reconstruction:{atom_id}",
        )
        expected_binding_sources.add(identity)

    r287 = validate_r287(read_gzip(HERE / R287_LEDGER))
    union_by_id = {
        row["Round287_potential_new_support_union_id"]: row
        for row in r287["potential_new_support_union_rows"]
    }
    for kind, rows, source_kind, id_field in (
        (
            "region",
            r287["region_rows"],
            "ROUND287_R275_REGION_INCLUSION_SUBCOVER",
            "Round287_region_disposition_row_id",
        ),
        (
            "cell",
            r287["refinement_cell_rows"],
            "ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER",
            "Round287_refinement_cell_disposition_row_id",
        ),
    ):
        aliases = [
            row for row in rows
            if row["exact_inclusion_alias_lemma_satisfied"] is True
        ]
        need(
            len(aliases) == (2_476 if kind == "region" else 5_532),
            f"Round287 {kind} alias census",
        )
        for source in aliases:
            need(
                source["disposition"] == R287_ALIAS
                and source["containing_atom_id"] in atom_info,
                f"Round287 exact alias filter:{source[id_field]}",
            )
            representation_id = (
                source["Round275_region_id"]
                if kind == "region" else
                source["Round286_refinement_cell_id"]
            )
            identity = f"{source_kind}::{representation_id}"
            output = binding_by_source.get(identity)
            atom_id = source["containing_atom_id"]
            need(
                output is not None
                and output["alias_source_kind"] == source_kind
                and output["source_row_id"] == source[id_field]
                and output["source_row_sha256"] == source["row_sha256"]
                and output["source_Round288_containing_atom_id"] == atom_id
                and output["target_registry_occurrence_id"]
                == atom_info[atom_id][0],
                f"Round287 binding reconstruction:{identity}",
            )
            expected_binding_sources.add(identity)

    probe = read_gzip(HERE / OVERLAP_LEDGER)
    probe_rows = probe.get("rows")
    need(
        probe.get("schema")
        == "cm2.round292.r287-registry-overlap-exhaustion-probe.v1."
        "ledger.v1"
        and probe.get("row_count") == 22_820
        and isinstance(probe_rows, list)
        and len(probe_rows) == 22_820
        and probe.get("rows_sha256")
        == "556bd0ed95709fe43ff7837522d8729582ce0e7c9679879a57365f864f6ba055"
        == digest(probe_rows),
        "Round292 overlap ledger commitment",
    )
    refinement_by_id: dict[str, dict[str, Any]] = {}
    components: list[dict[str, Any]] = []
    occupied: list[dict[str, Any]] = []
    overlap_count = 0
    for source in probe_rows:
        closed(source, probe_row_id(source))
        if "Round292_registry_overlap_row_id" in source:
            overlap_count += 1
        elif "member_refinement_cell_ids" in source:
            components.append(source)
        elif (
            "Round292_R287_existing_overlap_refinement_cell_id" in source
        ):
            refinement_by_id[
                source["Round292_R287_existing_overlap_refinement_cell_id"]
            ] = source
            if source["disposition"] == PROBE_OCCUPIED:
                occupied.append(source)
    need(
        overlap_count == 1_564
        and len(refinement_by_id) == 11_852
        and len(components) == 9_404
        and len(occupied) == 1_600,
        "Round292 overlap/refinement/component census",
    )
    component_member_ids: set[str] = set()
    for component in components:
        component_id = component["Round292_refined_new_support_component_id"]
        member_ids = component["member_refinement_cell_ids"]
        members = [refinement_by_id[member_id] for member_id in member_ids]
        occurrence_id = "source-g-expanded-occurrence:" + digest([
            "ROUND292_R287_EXISTING_OVERLAP_REFINED_NEW_SUPPORT_"
            "LOCAL_OCCURRENCE_V1",
            component_id,
            component["row_sha256"],
        ])
        output = registry_by_occurrence.get(occurrence_id)
        need(
            output is not None
            and output["registry_source_identity"]
            == f"ROUND292_R287_REFINED_COMPONENT::{component_id}"
            and output["registry_entry_kind"]
            == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
            and output["source_row_id"] == component_id
            and output["source_row_sha256"] == component["row_sha256"]
            and output["source_Round287_union_id"]
            == component["source_Round287_potential_new_support_union_id"]
            and output["member_refinement_cell_count"] == len(member_ids)
            and [
                item["Round292_refinement_cell_id"]
                for item in output["member_refinement_cells"]
            ] == member_ids
            and output["formal_new_expanded_occurrence_credit"] == 1
            and all(
                member["disposition"] == PROBE_UNCOVERED
                and member["Round292_refined_new_support_component_id"]
                == component_id
                for member in members
            ),
            f"Round292 refined registry reconstruction:{component_id}",
        )
        expected_registry_sources.add(output["registry_source_identity"])
        need(
            not (component_member_ids & set(member_ids)),
            f"component member injectivity:{component_id}",
        )
        component_member_ids.update(member_ids)
    need(
        len(component_member_ids) == 10_252,
        "complete uncovered refinement-cell partition",
    )

    for source in occupied:
        source_id = source[
            "Round292_R287_existing_overlap_refinement_cell_id"
        ]
        identity = f"ROUND292_R287_REFINED_EXISTING_SUBCOVER::{source_id}"
        output = binding_by_source.get(identity)
        target = source["existing_occurrence_ids"]
        need(
            output is not None
            and len(target) == source["existing_occurrence_occupancy_count"] == 1
            and output["alias_source_kind"]
            == "ROUND292_R287_EXACT_REFINED_EXISTING_SUBCOVER_CELL"
            and output["source_row_id"] == source_id
            and output["source_row_sha256"] == source["row_sha256"]
            and output["target_registry_occurrence_id"] == target[0]
            and output["source_Round287_union_id"]
            in union_by_id,
            f"Round292 refined existing binding:{source_id}",
        )
        expected_binding_sources.add(identity)

    need(
        expected_registry_sources
        == {row["registry_source_identity"] for row in registry_rows}
        and expected_binding_sources == set(binding_by_source),
        "source reconstruction exhausts both Round294 ledgers",
    )
    registry_histogram = Counter(
        row["registry_entry_kind"] for row in registry_rows
    )
    binding_histogram = Counter(
        row["alias_source_kind"] for row in binding_rows
    )
    need(
        registry_histogram == {
            "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE": 126_468,
            "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM": 295_336,
            "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT": 9_404,
        }
        and binding_histogram == {
            "ROUND288_EXACT_EQUAL_EXISTING_SUPPORT_ENVELOPE": 36_680,
            "ROUND287_R275_REGION_INCLUSION_SUBCOVER": 2_476,
            "ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER": 5_532,
            "ROUND292_R287_EXACT_REFINED_EXISTING_SUBCOVER_CELL": 1_600,
        }
        and sum(
            row["formal_new_expanded_occurrence_credit"]
            for row in registry_rows
        ) == 304_740
        and sum(
            row["formal_occurrence_alias_credit"] for row in binding_rows
        ) == 46_288,
        "final independent promotion census",
    )

    attack_value = attacks(
        result,
        registry_rows[-1],
        binding_rows[-1],
        {
            "RESULT": arguments.result,
            "REGISTRY": arguments.registry_ledger,
            "BINDING": arguments.representation_binding_ledger,
        },
    )
    attack_bytes = canonical(attack_value)
    verification = {
        "schema":
            "cm2.round294.source-g-occurrence-registry-atomic-promotion."
            "verification.v1",
        "status":
            "PASS_INDEPENDENT_CACHELESS_ROUND294_STAGE_A_REGISTRY__"
            "431208_ROWS__126468_PRESERVED__304740_FORMAL_NEW__"
            "46288_REPRESENTATION_BINDINGS__POST_REGISTRY_DSU_NOT_REBUILT",
        "artifact_pins": {
            **dict(sorted(INPUT_PINS.items())),
            arguments.result.name: file_sha256(arguments.result),
            arguments.registry_ledger.name:
                file_sha256(arguments.registry_ledger),
            arguments.representation_binding_ledger.name:
                file_sha256(arguments.representation_binding_ledger),
            arguments.attack_output.name: hashlib.sha256(
                attack_bytes
            ).hexdigest(),
        },
        "independence_contract": {
            "Round294_producer_imported_or_executed": False,
            "Round292_candidate_builder_imported_or_executed": False,
            "candidate_output_used_as_expected_row_oracle": False,
            "cache_or_pickle_input_used": False,
            "all_source_ledgers_opened_directly": True,
            "source_to_promoted_row_mapping_reconstructed_independently": True,
            "Round292_candidate_closure_reversed_independently": True,
        },
        "verified_census": {
            "formal_occurrence_registry_row_count": 431_208,
            "preserved_Round266_occurrence_count": 126_468,
            "formal_new_Round288_atom_occurrence_count": 295_336,
            "formal_new_refined_Round287_occurrence_count": 9_404,
            "formal_new_occurrence_count": 304_740,
            "formal_expanded_occurrence_count": 431_208,
            "formal_representation_binding_count": 46_288,
            "superseded_registry_row_count_rejected": 431_824,
            "direct_Round287_union_issuance_count_rejected": 10_020,
        },
        "scope_audit": {
            "registry_scope":
                "CURRENT_FORMAL_STAGE_A_OPEN_3D_PLUS_R287_REFINED_FRONTIER",
            "final_exhaustive_all_stratum_registry": False,
            "final_registry_count": None,
            "known_R291_gap_frontier": 576,
            "known_R289_incidence_refinement_frontier": 396,
        },
        "post_registry_nonpromotion": {
            "legacy_pre_Round294_preserved_registry_quotient_components":
                63_224,
            "post_Round294_quotient_component_count": None,
            "post_Round294_component_DSU_status": "NOT_REBUILT",
            "maximality_fibres_dispositions":
                "WAITING_EXPANDED_REGISTRY_DSU",
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "attack_audit": {
            "attack_suite_file_sha256":
                hashlib.sha256(attack_bytes).hexdigest(),
            "attack_suite_sha256": attack_value["attack_suite_sha256"],
            "attack_count": attack_value["attack_count"],
            "rejected_attack_count": attack_value["rejected_attack_count"],
            "fully_reclosed_semantic_attack_count":
                attack_value["fully_reclosed_semantic_attack_count"],
            "parser_gzip_path_attack_count":
                attack_value["parser_gzip_path_attack_count"],
            "all_semantic_reclosed_and_structural_attacks_rejected": True,
            "superseded_431824_explicitly_rejected": True,
            "direct_R287_10020_issuance_explicitly_rejected": True,
            "legacy_63224_as_current_quotient_explicitly_rejected": True,
        },
        "strict_document_and_file_object_contract": {
            "single_document_duplicate_free_integral_finite_JSON": True,
            "canonical_result_JSON_bytes": True,
            "single_member_trailing_free_bounded_GZIP": True,
            "gzip_uncompressed_size_cap_bytes":
                MAX_GZIP_UNCOMPRESSED_BYTES,
            "HERE_only_regular_non_symlink_non_hardlink_bounded_files": True,
            "file_size_cap_bytes": MAX_FILE_BYTES,
            "symlink_hardlink_FIFO_directory_missing_escape_oversize_attacks":
                "ALL_REJECTED",
        },
        "replay_contract": {
            "seed_argument_affects_output": False,
            "external_PYTHONHASHSEED_dual_cold_replay_required": True,
        },
    }
    verification["verification_sha256"] = digest(verification)
    verification_bytes = canonical(verification)
    if not arguments.no_write:
        safe_write(arguments.attack_output, attack_bytes)
        safe_write(arguments.verification, verification_bytes)
    print(json.dumps({
        "status": verification["status"],
        "verification_file_sha256":
            hashlib.sha256(verification_bytes).hexdigest(),
        "verification_sha256": verification["verification_sha256"],
        "attack_suite_file_sha256":
            hashlib.sha256(attack_bytes).hexdigest(),
        "attack_suite_sha256": attack_value["attack_suite_sha256"],
        "verified_census": verification["verified_census"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
