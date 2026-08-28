#!/usr/bin/env python3
"""Round295-A: close the complete Round291 physical-incidence frontier.

This is an append-only identity closure.  The 276 positive-t retained
children at the Round291 t=0 frontier are not new occurrences: each is the
punctured positive-t continuation of the unique resolved index-1 child of
the same Round174 origin.  Round295-A records exactly 276 representation
aliases to those already-issued Round294 occurrence IDs.

The promotion is atomic across three complete tables:

* 276 retained-volume representation aliases;
* all 113,452 Round291 physical-witness incidence bindings; and
* all 28,016 Round291 absence witnesses, which remain unbound.

No occurrence ID, component/DSU edge, seam edge, maximality, fibre,
disposition, Jx/Jy, Gate5, D02, or CM2 credit is issued here.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import gc
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, Callable, Iterable


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure"
)
DEFAULT_ALIASES = HERE / f"{PREFIX}_representation_alias_ledger.json.gz"
DEFAULT_INCIDENCE = (
    HERE / f"{PREFIX}_physical_witness_incidence_binding_ledger.json.gz"
)
DEFAULT_ABSENCE = HERE / f"{PREFIX}_absence_no_binding_ledger.json.gz"
DEFAULT_RESULT = HERE / f"{PREFIX}_result.json"

SCHEMA = "cm2.round295a.r291-positive-t-retained-continuation-closure.v1"
ALIAS_SCHEMA = (
    "cm2.round295a.r291-positive-t-retained-continuation-alias-ledger.v1"
)
INCIDENCE_SCHEMA = (
    "cm2.round295a.r291-complete-physical-witness-incidence-ledger.v1"
)
ABSENCE_SCHEMA = "cm2.round295a.r291-complete-absence-no-binding-ledger.v1"

R174 = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_"
    "rows.json"
)
R179 = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R204 = (
    "cm2_round204_source_g_wall_return_signature_local_replacement_"
    "certificate.json"
)
R208 = (
    "cm2_round208_source_g_outgoing_direct_signature_materialization_"
    "certificate.json"
)
R288 = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_"
    "atom_dispositions.json.gz"
)
R292_OVERLAP = (
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger."
    "json.gz"
)
R291 = (
    "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_"
    "ledger.json.gz"
)
R293_LEDGER = (
    "cm2_round293_source_g_r289_r291_witness_binding_canonical_closure_"
    "ledger.json.gz"
)
R293_RESULT = (
    "cm2_round293_source_g_r289_r291_witness_binding_canonical_closure_"
    "result.json"
)
R293_VERIFICATION = (
    "cm2_round293_source_g_r289_r291_witness_binding_canonical_closure_"
    "verification.json"
)
R293_MANIFEST = (
    "cm2_round293_source_g_r289_r291_witness_binding_canonical_closure_"
    "manifest.sha256"
)
R294_PRODUCER = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion.py"
)
R294_REGISTRY = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)
R294_BINDINGS = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "representation_binding_ledger.json.gz"
)
R294_RESULT = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_result.json"
)
R294_VERIFIER = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_verifier.py"
)
R294_VERIFICATION = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "verification.json"
)
R294_ATTACKS = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "attack_suite.json"
)
R294_MANIFEST = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "manifest.sha256"
)

# The Round294 entries are replaced only after its dual-seed package is
# completely sealed.  Keeping one explicit pin table makes accidental use of
# a moving candidate fail closed.
BYTE_PINS = {
    R174: "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    R179: "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R204: "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    R208: "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    R288: "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a",
    R292_OVERLAP:
        "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    R291: "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab",
    R293_LEDGER:
        "0e7395a69844734cc51563882f471987cc566db28a55ccae6e6d15d045f9e53c",
    R293_RESULT:
        "36459f330fdd577031f35d8d8f7e93cf3ebc96bef049a4f687b22c9e39e91613",
    R293_VERIFICATION:
        "7eed8a1edf0f725a09239e5e440109954aeb26cdd57d6ea5eeee4a2e8809c9ec",
    R293_MANIFEST:
        "14fef7e62be76cefaa2c331d7c6f72e50f732c7b5df17596759afe1a49406987",
    # ROUND294_FINAL_PINS_BEGIN
    R294_PRODUCER:
        "6e0ab06cf6ab7dfb7868b2fe7a4699a914e6a3b0f8b18e4181d138bc2d887a9b",
    R294_REGISTRY:
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    R294_BINDINGS:
        "f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833",
    R294_RESULT:
        "dc93ef564ce1aec4aabbc7ff717ac76749b92899e210179a00dba63f2d32d626",
    R294_VERIFIER:
        "154158d7910b1ffa1f71475c4e0505c6ab72ca3ab856a2fa4c27d7e376533aaa",
    R294_VERIFICATION:
        "13dcb461f269a8e346c220b85cad0e87a0392b5e2682b7dd70132fd8bd7a1245",
    R294_ATTACKS:
        "aefb50be4969676d752cf8c8cb06f355db508007be4c1ee95f07c305e19a8adb",
    R294_MANIFEST:
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    # ROUND294_FINAL_PINS_END
}

ZERO_FIELDS = (
    "formal_new_expanded_occurrence_credit",
    "formal_component_union_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_seam_edge_credit",
    "formal_Jx_Jy_same_point_glue_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)


class Round295AError(RuntimeError):
    """Fail-closed Round295-A contract violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Round295AError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def chunks(value: Any) -> Iterable[bytes]:
    for piece in ENCODER.iterencode(value):
        yield piece.encode("utf-8")


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


def guarded_path(name: str, maximum: int = 2_000_000_000) -> Path:
    path = HERE / name
    need(
        path.parent == HERE and path.parent.resolve() == HERE.resolve(),
        f"path parent:{name}",
    )
    need(path.exists() and not path.is_symlink(), f"path exists:{name}")
    info = path.stat()
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        f"path regular/link/size:{name}",
    )
    return path


def strict_decode(raw: bytes, label: str) -> dict[str, Any]:
    need(
        raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"strict bytes:{label}",
    )

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            need(key not in value, f"duplicate JSON key:{label}:{key}")
            value[key] = item
        return value

    def reject(token: str) -> None:
        raise ValueError(token)

    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )
    need(type(value) is dict, f"strict top object:{label}")
    return value


def read_json(name: str, maximum: int = 2_000_000_000) -> dict[str, Any]:
    return strict_decode(guarded_path(name, maximum).read_bytes(), name)


def read_gzip_json(name: str) -> dict[str, Any]:
    path = guarded_path(name)
    with gzip.open(path, "rb") as stream:
        raw = stream.read()
    return strict_decode(raw, name)


def verify_self_digest(
    value: dict[str, Any], field: str, label: str
) -> None:
    expected = value.get(field)
    payload = dict(value)
    payload.pop(field, None)
    need(
        isinstance(expected, str)
        and re.fullmatch(r"[0-9a-f]{64}", expected) is not None
        and digest(payload) == expected,
        f"self digest:{label}",
    )


def parse_manifest(name: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in guarded_path(name, 100_000).read_text(
        encoding="utf-8"
    ).splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, f"manifest syntax:{name}")
        sha256, filename = match.groups()
        need(filename not in rows, f"manifest duplicate:{filename}")
        rows[filename] = sha256
    return rows


class ListCommitment:
    """Incremental canonical-JSON commitment to a finite list."""

    def __init__(self) -> None:
        self.state = hashlib.sha256()
        self.state.update(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        for piece in chunks(value):
            self.state.update(piece)
        self.count += 1

    def finish(self) -> str:
        final = self.state.copy()
        final.update(b"]")
        return final.hexdigest()


def scan_large_gzip_ledger(
    name: str,
    visit: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    """Stream the canonical `rows` array and return metadata without rows."""

    path = guarded_path(name)
    decoder = json.JSONDecoder(
        object_pairs_hook=lambda pairs: dict(pairs),
        parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    marker = '"rows":['
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        prefix = ""
        while marker not in prefix:
            piece = stream.read(1 << 20)
            need(bool(piece), f"rows marker:{name}")
            prefix += piece
        before, buffer = prefix.split(marker, 1)
        row_count = 0
        while True:
            buffer = buffer.lstrip()
            if buffer.startswith(","):
                buffer = buffer[1:].lstrip()
            if buffer.startswith("]"):
                buffer = buffer[1:]
                break
            while True:
                try:
                    row, end = decoder.raw_decode(buffer)
                    break
                except json.JSONDecodeError:
                    piece = stream.read(1 << 20)
                    need(bool(piece), f"truncated rows:{name}:{row_count}")
                    buffer += piece
            need(type(row) is dict, f"row object:{name}:{row_count}")
            visit(row)
            row_count += 1
            buffer = buffer[end:]
        suffix = buffer + stream.read()
    metadata_raw = (before + '"rows":[]' + suffix).encode("utf-8")
    metadata = strict_decode(metadata_raw, f"{name}:metadata")
    need(metadata.get("rows") == [], f"metadata rows empty:{name}")
    metadata["streamed_row_count"] = row_count
    return metadata


def validate_row_hash(row: dict[str, Any], label: str) -> None:
    expected = row.get("row_sha256")
    payload = dict(row)
    payload.pop("row_sha256", None)
    need(
        isinstance(expected, str) and digest(payload) == expected,
        f"row hash:{label}",
    )


def validate_round294_package() -> dict[str, Any]:
    for name, expected in BYTE_PINS.items():
        need(
            re.fullmatch(r"[0-9a-f]{64}", expected) is not None,
            f"unsealed pin placeholder:{name}",
        )
        need(file_sha256(guarded_path(name)) == expected, f"byte pin:{name}")
    manifest = parse_manifest(R294_MANIFEST)
    for name in (
        R294_PRODUCER, R294_REGISTRY, R294_BINDINGS, R294_RESULT,
        R294_VERIFIER, R294_VERIFICATION, R294_ATTACKS,
    ):
        need(manifest.get(name) == BYTE_PINS[name], f"R294 manifest:{name}")
    result = read_json(R294_RESULT)
    verify_self_digest(result, "result_sha256", "Round294 result")
    verification = read_json(R294_VERIFICATION)
    verify_self_digest(
        verification, "verification_sha256", "Round294 verification"
    )
    need(
        result.get("status", "").startswith(
            "PASS_ROUND294_ATOMIC_STAGE_A_OCCURRENCE_REGISTRY_PROMOTION"
        )
        and result.get("census", {}).get(
            "formal_occurrence_registry_row_count"
        ) == 431_208
        and result["census"].get(
            "formal_representation_binding_count"
        ) == 46_288
        and result.get("scope_contract", {}).get(
            "final_exhaustive_all_stratum_registry_claimed"
        ) is False
        and result.get("nonpromotion_freeze", {}).get(
            "post_Round294_quotient_component_count"
        ) is None
        and result["nonpromotion_freeze"].get(
            "post_Round294_expanded_registry_component_DSU_status"
        ) == "NOT_REBUILT"
        and verification.get("status", "").startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND294"
        ),
        "sealed Round294 semantic package",
    )
    return result


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = result["row_column_schemas"][table]
    return [
        dict(zip(columns, row, strict=True))
        for row in result[table]
    ]


def qbox(values: list[str]) -> tuple[Q, Q, Q, Q, Q, Q]:
    box = tuple(map(Q, values))
    need(
        len(box) == 6
        and box[0] < box[1]
        and box[2] < box[3]
        and box[4] < box[5],
        "positive rational box",
    )
    return box  # type: ignore[return-value]


def volume(box: tuple[Q, Q, Q, Q, Q, Q]) -> Q:
    return (
        (box[1] - box[0])
        * (box[3] - box[2])
        * (box[5] - box[4])
    )


def positive_overlap(
    first: tuple[Q, Q, Q, Q, Q, Q],
    second: tuple[Q, Q, Q, Q, Q, Q],
) -> bool:
    return all(
        max(first[index], second[index])
        < min(first[index + 1], second[index + 1])
        for index in (0, 2, 4)
    )


def validate_ledger_commitments(
    rows: list[dict[str, Any]],
    ledger: dict[str, Any],
    id_field: str,
    label: str,
) -> None:
    need(ledger.get("row_count") == len(rows), f"row count:{label}")
    ids: list[str] = []
    hashes: list[str] = []
    for index, row in enumerate(rows):
        validate_row_hash(row, f"{label}:{index}")
        ids.append(row[id_field])
        hashes.append(row["row_sha256"])
    need(
        len(ids) == len(set(ids))
        and digest(ids) == ledger.get("row_ids_sha256")
        and digest(hashes) == ledger.get("row_hashes_sha256")
        and digest(rows) == ledger.get("rows_sha256"),
        f"ledger commitments:{label}",
    )


def load_frontier() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    r291 = read_gzip_json(R291)
    r293 = read_gzip_json(R293_LEDGER)
    result293 = read_json(R293_RESULT)
    verification293 = read_json(R293_VERIFICATION)
    verify_self_digest(result293, "result_sha256", "Round293 result")
    verify_self_digest(
        verification293, "verification_sha256", "Round293 verification"
    )
    manifest293 = parse_manifest(R293_MANIFEST)
    for name in (R293_LEDGER, R293_RESULT, R293_VERIFICATION):
        need(manifest293.get(name) == BYTE_PINS[name], f"R293 manifest:{name}")
    need(
        r291.get("row_count") == 55_428
        and len(r291.get("rows", [])) == 55_428
        and len(r293.get("Round291_physical_witness_binding_rows", []))
        == 113_452
        and len(r293.get("Round291_absence_no_binding_rows", [])) == 28_016
        and result293.get("Round291", {}).get(
            "physical_witness_unresolved_count"
        ) == 576
        and verification293.get("status", "").startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND293"
        ),
        "sealed R291/R293 frontier",
    )
    dispositions = {
        row["complete_lower_stratum_local_disposition_row_id"]: row
        for row in r291["rows"]
    }
    need(len(dispositions) == 55_428, "unique Round291 dispositions")
    r179 = read_json(R179)["result"]
    origins = {
        row["origin_row_id"]: row
        for row in unpack(r179, "origin_tube_rows")
    }
    return r291, r293, r179, dispositions, origins


def resolve_owner_groups(
    r293: dict[str, Any],
    dispositions: dict[str, dict[str, Any]],
    r179: dict[str, Any],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, list[dict[str, Any]]],
    dict[str, dict[str, Any]],
]:
    unresolved = [
        row for row in r293["Round291_physical_witness_binding_rows"]
        if row["binding_classification"]
        == "UNRESOLVED_POSITIVE_T_OWNER_RETAINED_VOLUME__"
        "NO_ISSUED_REGISTRY_OCCURRENCE"
    ]
    need(len(unresolved) == 576, "Round293 unresolved witness count")
    witnesses_by_retained: dict[str, list[dict[str, Any]]] = defaultdict(list)
    witness_cells: dict[str, dict[str, Any]] = {}
    for binding in unresolved:
        disposition = dispositions[binding["Round291_local_disposition_row_id"]]
        index = binding["physical_witness_cell_index"]
        need(
            0 <= index < len(disposition["physical_witness_cells"]),
            "physical witness index",
        )
        cell = disposition["physical_witness_cells"][index]
        retained_id = cell["positive_owner_retained_child_row_id"]
        witnesses_by_retained[retained_id].append(binding)
        witness_cells[binding["Round292_R291_physical_witness_binding_row_id"]] = (
            cell
        )
    retained_rows = {
        row["row_id"]: row
        for row in unpack(r179, "retained_3d_child_rows")
        if row["row_id"] in witnesses_by_retained
    }
    owner_origins = {
        row["origin_row_id"]: row
        for row in unpack(r179, "origin_tube_rows")
        if row["origin_row_id"]
        in {retained["origin_row_id"] for retained in retained_rows.values()}
    }
    siblings_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in unpack(r179, "resolved_3d_child_rows"):
        if row["origin_row_id"] in owner_origins:
            siblings_by_origin[row["origin_row_id"]].append(row)
    siblings: dict[str, dict[str, Any]] = {}
    for retained_id, retained in retained_rows.items():
        origin = owner_origins[retained["origin_row_id"]]
        candidates = siblings_by_origin[origin["origin_row_id"]]
        need(
            len(candidates) == 1
            and retained["child_index"] == 0
            and candidates[0]["child_index"] == 1,
            f"unique index-1 sibling:{retained_id}",
        )
        siblings[retained_id] = candidates[0]
    need(
        len(retained_rows) == len(owner_origins) == len(siblings) == 276,
        "276 owner-origin-sibling triples",
    )
    return retained_rows, witnesses_by_retained, siblings


def exact_continuation_contract(
    retained: dict[str, Any],
    origin: dict[str, Any],
    sibling: dict[str, Any],
) -> dict[str, Any]:
    owner_box = qbox(retained["box"])
    origin_box = qbox(origin["original_box"])
    sibling_box = qbox(sibling["box"])
    chart_cell = origin["chart"].split(":")[1]
    endpoint_axis = "X" if chart_cell in {"N", "S"} else "Y"
    special = [
        reason for reason in origin["original_reason_labels"]
        if reason.startswith("wall_crossing_time_not_strict:")
    ]
    need(
        origin["chosen_split_axis"] == "t"
        and origin["resolved_child_count"] == 1
        and origin["retained_child_count"] == 1
        and origin["guard_child_count"] == 0
        and retained["origin_row_id"] == sibling["origin_row_id"]
        == origin["origin_row_id"]
        and retained["parent_id"] == sibling["parent_id"]
        == origin["parent_id"]
        and retained["chart"] == sibling["chart"] == origin["chart"]
        and sibling["owner_target"] == origin["owner_target"]
        and retained["reason_labels"]
        == [f"wall_endpoint_or_count_transition:{endpoint_axis}:0"]
        and origin_box[0] == owner_box[0] == 0
        and owner_box[1] == sibling_box[0]
        and sibling_box[1] == origin_box[1]
        and owner_box[2:] == sibling_box[2:] == origin_box[2:]
        and volume(owner_box) == Q(retained["coordinate_volume"])
        and volume(sibling_box) == Q(sibling["coordinate_volume"])
        and volume(origin_box) == Q(origin["original_coordinate_volume"])
        and volume(owner_box) + volume(sibling_box) == volume(origin_box)
        and retained["refinement_path"]
        == [*origin["original_refinement_path"], "t0"]
        and sibling["refinement_path"]
        == [*origin["original_refinement_path"], "t1"]
        and sibling["ambient_dimension"] == 3
        and sibling["credit_kind"] == "LOCAL_POSITIVE_3D_OCCURRENCE_ONLY"
        and sibling["global_geometric_disposition_credit"] == 0,
        f"exact same-origin continuation:{retained['row_id']}",
    )
    need(
        not special
        or (
            len(special) == 1
            and special[0]
            == f"wall_crossing_time_not_strict:{endpoint_axis}:1"
        ),
        f"special wall-one reason:{retained['row_id']}",
    )
    return {
        "artificial_split_axis": "t",
        "artificial_split_face": [
            sibling["box"][0],
            sibling["box"][0],
            *sibling["box"][2:],
        ],
        "source_endpoint_axis": endpoint_axis,
        "source_endpoint_exact_formula": "(9/25)*t",
        "source_endpoint_unique_zero": "t=0",
        "punctured_owner_domain": "0<t<T",
        "same_origin_unique_index1_sibling": True,
        "exact_full_face_shared": True,
        "exact_volume_conserved": True,
        "identity_basis":
            "SAME_ROUND174_ORIGIN__UNIQUE_RESOLVED_INDEX1_SIBLING__"
            "ARTIFICIAL_T_SPLIT_FACE__NO_EVENT_CONTINUATION",
        "signature_or_box_equality_used_as_identity_basis": False,
        "symmetry_used_as_identity_basis": False,
        "wall_crossing_time_not_strict_wall1_reason_count": len(special),
    }


def scan_round294(
    result294: dict[str, Any],
    target_ids: set[str],
) -> tuple[
    set[str],
    dict[str, dict[str, Any]],
    dict[str, set[str]],
    dict[str, int],
]:
    registry_ids: set[str] = set()
    targets: dict[str, dict[str, Any]] = {}
    tranche_ids: dict[str, set[str]] = defaultdict(set)
    ids_commitment = ListCommitment()
    row_ids_commitment = ListCommitment()
    hashes_commitment = ListCommitment()
    rows_commitment = ListCommitment()

    def visit(row: dict[str, Any]) -> None:
        validate_row_hash(row, "Round294 registry")
        occurrence_id = row["registry_occurrence_id"]
        need(occurrence_id not in registry_ids, "Round294 unique occurrence ID")
        registry_ids.add(occurrence_id)
        ids_commitment.add(occurrence_id)
        row_ids_commitment.add(row["Round294_occurrence_registry_row_id"])
        hashes_commitment.add(row["row_sha256"])
        rows_commitment.add(row)
        entry_kind = row["registry_entry_kind"]
        tranche_identity = (
            row["source_row_id"]
            if entry_kind
            == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
            else occurrence_id
        )
        tranche_ids[entry_kind].add(tranche_identity)
        if occurrence_id in target_ids:
            targets[occurrence_id] = {
                "registry_occurrence_id": occurrence_id,
                "Round294_occurrence_registry_row_id":
                    row["Round294_occurrence_registry_row_id"],
                "Round294_occurrence_registry_row_sha256":
                    row["row_sha256"],
                "registry_entry_kind": row["registry_entry_kind"],
                "source_occurrence_class": row["source_occurrence_class"],
                "physical_support_chart": row["physical_support_chart"],
                "official_key_id": row["official_key_id"],
                "official_key_ordinal": row["official_key_ordinal"],
                "complete_10_field_return_signature_sha256":
                    row["complete_10_field_return_signature_sha256"],
            }

    metadata = scan_large_gzip_ledger(R294_REGISTRY, visit)
    summary = result294["registry_ledger"]
    need(
        metadata["streamed_row_count"] == metadata["row_count"] == 431_208
        and ids_commitment.finish() == summary["occurrence_ids_sha256"]
        and row_ids_commitment.finish() == summary["row_ids_sha256"]
        and hashes_commitment.finish() == summary["row_hashes_sha256"]
        and rows_commitment.finish() == summary["rows_sha256"]
        and len(registry_ids) == 431_208
        and set(targets) == target_ids,
        "complete Round294 registry streaming commitments",
    )

    binding_ids = ListCommitment()
    binding_hashes = ListCommitment()
    binding_rows = ListCommitment()
    alias_count = 0

    def visit_binding(row: dict[str, Any]) -> None:
        nonlocal alias_count
        validate_row_hash(row, "Round294 representation binding")
        alias_count += 1
        binding_ids.add(
            row["Round294_occurrence_representation_binding_row_id"]
        )
        binding_hashes.add(row["row_sha256"])
        binding_rows.add(row)

    binding_metadata = scan_large_gzip_ledger(R294_BINDINGS, visit_binding)
    binding_summary = result294["representation_binding_ledger"]
    need(
        binding_metadata["streamed_row_count"]
        == binding_metadata["row_count"]
        == alias_count == 46_288
        and binding_ids.finish() == binding_summary["row_ids_sha256"]
        and binding_hashes.finish() == binding_summary["row_hashes_sha256"]
        and binding_rows.finish() == binding_summary["rows_sha256"],
        "complete Round294 binding streaming commitments",
    )
    tranche_counts = {
        kind: len(rows) for kind, rows in tranche_ids.items()
    }
    return registry_ids, targets, tranche_ids, tranche_counts


def complete_overlap_exhaustion(
    retained_rows: dict[str, dict[str, Any]],
    tranche_ids: dict[str, set[str]],
) -> tuple[dict[str, Any], dict[str, int]]:
    owners: dict[str, list[tuple[str, tuple[Q, Q, Q, Q, Q, Q]]]] = (
        defaultdict(list)
    )
    per_owner_overlap = {retained_id: 0 for retained_id in retained_rows}
    for retained_id, retained in retained_rows.items():
        owners[retained["chart"]].append((retained_id, qbox(retained["box"])))
    owner_pair_overlap = 0
    for chart_rows in owners.values():
        for index, (_first_id, first) in enumerate(chart_rows):
            for _second_id, second in chart_rows[index + 1:]:
                owner_pair_overlap += int(positive_overlap(first, second))
    need(owner_pair_overlap == 0, "owner aliases pairwise positive disjoint")

    overlap_pairs = 0

    def audit_support(chart: str, box_values: list[str]) -> None:
        nonlocal overlap_pairs
        support = qbox(box_values)
        for retained_id, owner in owners[chart]:
            if positive_overlap(owner, support):
                per_owner_overlap[retained_id] += 1
                overlap_pairs += 1

    # Complete preserved Round266 tranche: independently recover all exact
    # source geometry IDs and full rational support boxes.
    preserved_ids: set[str] = set()
    r174 = read_json(R174)["result"]
    for row in unpack(r174, "resolved_3d_occurrence_rows"):
        need(row["row_id"] not in preserved_ids, "unique R174 support")
        preserved_ids.add(row["row_id"])
        audit_support(row["chart"], row["box"])
    del r174
    gc.collect()

    r179 = read_json(R179)["result"]
    for row in unpack(r179, "resolved_3d_child_rows"):
        need(row["row_id"] not in preserved_ids, "unique R179 support")
        preserved_ids.add(row["row_id"])
        audit_support(row["chart"], row["box"])
    del r179
    gc.collect()

    r204 = read_json(R204)["result"]
    for row in r204["formal_local_open_3D_region_ledger"]["rows"]:
        need(row["region_row_id"] not in preserved_ids, "unique R204 support")
        preserved_ids.add(row["region_row_id"])
        audit_support(row["chart"], row["leaf_exact_box"])
    del r204
    gc.collect()

    r208 = read_json(R208)["result"]
    for row in r208["formal_local_open_3D_signature_ledger"]["rows"]:
        need(row["region_row_id"] not in preserved_ids, "unique R208 support")
        preserved_ids.add(row["region_row_id"])
        audit_support(
            row["local_return_signature"]["source_chart"],
            row["Round182_leaf_box"],
        )
    del r208
    gc.collect()

    preserved_kind = "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
    need(
        len(preserved_ids) == 126_468
        and preserved_ids == tranche_ids[preserved_kind],
        "complete preserved registry support recovery",
    )

    # Complete Round288 new-atom tranche.  Frozen envelopes, not the smaller
    # inner witnesses, are used for the disjointness test.
    r288 = read_gzip_json(R288)
    r288_ids: set[str] = set()
    r288_envelopes = 0
    for row in r288["rows"]:
        if not row["occurrence_identity_disposition"].startswith("NEW_"):
            continue
        occurrence_id = row["reserved_candidate_occurrence_id__not_issued"]
        need(occurrence_id not in r288_ids, "unique R288 occurrence ID")
        r288_ids.add(occurrence_id)
        envelopes = row["frozen_positive_rational_support_envelopes"]
        need(envelopes, f"R288 nonempty envelopes:{occurrence_id}")
        r288_envelopes += len(envelopes)
        for support in envelopes:
            audit_support(row["source_chart"], support)
    del r288
    gc.collect()
    r288_kind = "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
    need(
        len(r288_ids) == 295_336
        and r288_ids
        == {
            occurrence_id
            for occurrence_id in tranche_ids[r288_kind]
        },
        "complete Round288 registry support recovery",
    )

    # Complete Round292 refined-R287 tranche in exact (t^2,p,s)
    # coordinates.  All owner boxes lie at t>=0, so squaring preserves order.
    owner_squared: dict[
        str, list[tuple[str, tuple[Q, Q, Q, Q, Q, Q]]]
    ] = defaultdict(list)
    for chart, rows in owners.items():
        for retained_id, box in rows:
            owner_squared[chart].append((
                retained_id,
                (
                    box[0] * box[0], box[1] * box[1],
                    box[2], box[3], box[4], box[5],
                ),
            ))
    probe = read_gzip_json(R292_OVERLAP)
    component_ids: set[str] = set()
    refined_cells = 0
    for row in probe["rows"]:
        if row.get("disposition") != (
            "EXACT_UNCOVERED_POSITIVE_OPEN_SLICE__"
            "MEMBER_OF_REFINED_PARENT_LOCAL_NEW_SUPPORT"
        ):
            continue
        refined_cells += 1
        component_ids.add(row["Round292_refined_new_support_component_id"])
        cell = qbox(row["exact_transformed_open_cell"])
        for retained_id, owner in owner_squared[row["source_chart"]]:
            if positive_overlap(owner, cell):
                per_owner_overlap[retained_id] += 1
                overlap_pairs += 1
    del probe
    gc.collect()
    refined_kind = (
        "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
    )
    need(
        len(component_ids) == 9_404
        and component_ids == tranche_ids[refined_kind]
        and refined_cells == 10_252,
        "complete Round292 refined registry support recovery",
    )
    need(
        overlap_pairs == 0
        and set(per_owner_overlap.values()) == {0},
        "zero positive-volume registry overlap",
    )
    return {
        "registry_row_count_exhausted": 431_208,
        "preserved_Round266_registry_rows_exhausted": 126_468,
        "new_Round288_registry_rows_exhausted": 295_336,
        "new_Round288_frozen_support_envelopes_exhausted": r288_envelopes,
        "refined_Round292_registry_rows_exhausted": 9_404,
        "refined_Round292_exact_transformed_cells_exhausted": 10_252,
        "retained_owner_alias_count": 276,
        "retained_owner_pairwise_positive_overlap_count":
            owner_pair_overlap,
        "registry_positive_volume_overlap_pair_count": overlap_pairs,
        "undesignated_positive_volume_overlap_count": overlap_pairs,
        "all_registry_tranches_exhausted": True,
        "all_undesignated_overlaps_rejected": True,
    }, per_owner_overlap


def alias_row(
    retained: dict[str, Any],
    origin: dict[str, Any],
    sibling: dict[str, Any],
    target: dict[str, Any],
    witness_count: int,
    continuation: dict[str, Any],
    overlap_count: int,
) -> dict[str, Any]:
    payload = {
        "source_Round179_retained_child_row_id": retained["row_id"],
        "source_Round174_origin_row_id": origin["origin_row_id"],
        "source_parent_id": origin["parent_id"],
        "source_chart": origin["chart"],
        "owner_target": origin["owner_target"],
        "retained_child_index": retained["child_index"],
        "resolved_sibling_index": sibling["child_index"],
        "retained_positive_t_open_box": retained["box"],
        "resolved_sibling_open_box": sibling["box"],
        "retained_exact_coordinate_volume": retained["coordinate_volume"],
        "resolved_sibling_exact_coordinate_volume":
            sibling["coordinate_volume"],
        "resolved_sibling_row_id": sibling["row_id"],
        "resolved_sibling_official_key_id": sibling["official_key_id"],
        "resolved_sibling_official_key_ordinal":
            sibling["official_key_ordinal"],
        "resolved_sibling_signed_wall_word": sibling["signed_wall_word"],
        "resolved_sibling_ordered_integer_wall_events":
            sibling["ordered_integer_wall_events"],
        "resolved_sibling_outgoing_cell": sibling["outgoing_cell"],
        "resolved_sibling_target_chart": sibling["target_chart"],
        "target_Round294_registry_occurrence_id":
            target["registry_occurrence_id"],
        "target_Round294_occurrence_registry_row_id":
            target["Round294_occurrence_registry_row_id"],
        "target_Round294_occurrence_registry_row_sha256":
            target["Round294_occurrence_registry_row_sha256"],
        "target_Round294_registry_entry_kind":
            target["registry_entry_kind"],
        "target_Round294_source_occurrence_class":
            target["source_occurrence_class"],
        "Round291_witness_binding_count": witness_count,
        **continuation,
        "target_factor_wall0_whole_box_strict_nonzero":
            "PROVED_DIRECT_STRICT_INTERVAL_OR_STRICT_MONOTONE_FACE_SIGNS",
        "all_other_dynamic_event_signature_invariants_strict":
            "PROVED_ON_COMPLETE_ORIGIN_BY_256_BIT_INTERVAL_EVENT_REPLAY",
        "complete_Round294_registry_positive_volume_overlap_count":
            overlap_count,
        "undesignated_positive_volume_overlap_count": overlap_count,
        "alias_binding_status":
            "FORMALLY_RECORDED_ROUND295A_SAME_ORIGIN_POSITIVE_T_"
            "CONTINUATION_ALIAS",
        "formal_occurrence_alias_credit": 1,
        "formal_physical_witness_incidence_binding_credit": 0,
        "formal_target_reference_credit": 0,
        "formal_occurrence_ID_issued": False,
        "formal_identity_collapse_credit": 0,
        "partitioned_parent_whole_binding_credit": 0,
        **{field: 0 for field in ZERO_FIELDS},
    }
    row_id = "round295a-retained-continuation-alias:" + digest([
        "ROUND295A_RETAINED_CONTINUATION_ALIAS_V1", payload
    ])
    row = {
        "Round295A_retained_continuation_alias_row_id": row_id,
        **payload,
    }
    row["row_sha256"] = digest(row)
    return row


def incidence_row(
    source: dict[str, Any],
    targets: list[dict[str, Any]],
    continuation_alias_id: str | None,
) -> dict[str, Any]:
    target_ids = [target["registry_occurrence_id"] for target in targets]
    source_unresolved = source["terminal_registry_target_reference_count"] == 0
    payload = {
        "source_Round293_R291_physical_witness_binding_row_id":
            source["Round292_R291_physical_witness_binding_row_id"],
        "source_Round293_R291_physical_witness_binding_row_sha256":
            source["row_sha256"],
        "Round291_local_disposition_row_id":
            source["Round291_local_disposition_row_id"],
        "physical_witness_cell_index": source["physical_witness_cell_index"],
        "source_chart": source["source_chart"],
        "canonical_support_kind": source["canonical_support_kind"],
        "local_disposition": source["local_disposition"],
        "witness_kind": source["witness_kind"],
        "source_Round293_binding_classification":
            source["binding_classification"],
        "Round295A_binding_classification": (
            "EXACT_SAME_ORIGIN_ARTIFICIAL_T_SPLIT_NO_EVENT_CONTINUATION_"
            "TO_EXISTING_ROUND294_RESOLVED_SIBLING"
            if source_unresolved else
            "FORMAL_ROUND294_REGISTRY_REBIND__"
            + source["binding_classification"]
        ),
        "target_Round294_registry_occurrence_ids": target_ids,
        "target_Round294_registry_reference_count": len(targets),
        "target_Round294_registry_rows": targets,
        "Round295A_retained_continuation_alias_row_id":
            continuation_alias_id,
        "exact_witness_covered_by_named_registry_supports": True,
        "formal_physical_witness_incidence_binding_credit": 1,
        "formal_target_reference_credit": len(targets),
        "formal_occurrence_alias_credit": 0,
        "formal_occurrence_ID_issued": False,
        "partitioned_parent_whole_binding_credit": 0,
        **{field: 0 for field in ZERO_FIELDS},
    }
    row_id = "round295a-r291-physical-incidence:" + digest([
        "ROUND295A_COMPLETE_R291_PHYSICAL_INCIDENCE_V1", payload
    ])
    row = {
        "Round295A_R291_physical_incidence_binding_row_id": row_id,
        **payload,
    }
    row["row_sha256"] = digest(row)
    return row


def absence_row(source: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "source_Round293_R291_absence_no_binding_row_id":
            source["Round292_R291_absence_no_binding_row_id"],
        "source_Round293_R291_absence_no_binding_row_sha256":
            source["row_sha256"],
        "Round291_local_disposition_row_id":
            source["Round291_local_disposition_row_id"],
        "absence_witness_cell_index": source["absence_witness_cell_index"],
        "witness_kind": source["witness_kind"],
        "binding_classification":
            "FORMAL_PROVEN_LOCAL_ABSENCE__NO_ROUND294_REGISTRY_INCIDENCE",
        "target_Round294_registry_occurrence_ids": [],
        "target_Round294_registry_reference_count": 0,
        "formal_physical_witness_incidence_binding_credit": 0,
        "formal_target_reference_credit": 0,
        "formal_occurrence_alias_credit": 0,
        "formal_occurrence_ID_issued": False,
        **{field: 0 for field in ZERO_FIELDS},
    }
    row_id = "round295a-r291-absence-no-binding:" + digest([
        "ROUND295A_COMPLETE_R291_ABSENCE_NO_BINDING_V1", payload
    ])
    row = {
        "Round295A_R291_absence_no_binding_row_id": row_id,
        **payload,
    }
    row["row_sha256"] = digest(row)
    return row


def make_ledger(
    rows: list[dict[str, Any]],
    schema: str,
    status: str,
    id_field: str,
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    need(len(ids) == len(set(ids)), f"unique ledger IDs:{schema}")
    return {
        "schema": schema,
        "status": status,
        "row_count": len(rows),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows_sha256": digest(rows),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def ledger_summary(
    ledger: dict[str, Any], filename: str
) -> dict[str, Any]:
    return {
        "filename": filename,
        **{
            key: ledger[key]
            for key in (
                "schema", "row_count", "row_ids_sha256",
                "row_hashes_sha256", "rows_sha256",
            )
        },
    }


def build(
    producer_sha256: str,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    result294 = validate_round294_package()
    _r291, r293, r179, dispositions, origins = load_frontier()
    retained_rows, witnesses_by_retained, siblings = resolve_owner_groups(
        r293, dispositions, r179
    )
    target_ids = {
        source_target
        for row in r293["Round291_physical_witness_binding_rows"]
        for source_target in row["terminal_registry_target_references"]
    } | {sibling["row_id"] for sibling in siblings.values()}
    registry_ids, registry_targets, tranche_ids, tranche_counts = (
        scan_round294(result294, target_ids)
    )
    overlap, per_owner_overlap = complete_overlap_exhaustion(
        retained_rows, tranche_ids
    )

    alias_rows: list[dict[str, Any]] = []
    alias_id_by_retained: dict[str, str] = {}
    special_count = 0
    for retained_id in sorted(retained_rows):
        retained = retained_rows[retained_id]
        origin = origins[retained["origin_row_id"]]
        sibling = siblings[retained_id]
        continuation = exact_continuation_contract(
            retained, origin, sibling
        )
        special_count += continuation[
            "wall_crossing_time_not_strict_wall1_reason_count"
        ]
        target = registry_targets[sibling["row_id"]]
        need(
            target["registry_entry_kind"]
            == "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
            and target["source_occurrence_class"] == "ROUND179_RESOLVED"
            and target["physical_support_chart"] == retained["chart"]
            and target["official_key_id"] == sibling["official_key_id"],
            f"Round294 resolved sibling target:{retained_id}",
        )
        row = alias_row(
            retained, origin, sibling, target,
            len(witnesses_by_retained[retained_id]),
            continuation, per_owner_overlap[retained_id],
        )
        alias_rows.append(row)
        alias_id_by_retained[retained_id] = (
            row["Round295A_retained_continuation_alias_row_id"]
        )
    alias_rows.sort(
        key=lambda row: row[
            "Round295A_retained_continuation_alias_row_id"
        ]
    )
    need(special_count == 4, "four special wall-one origins")

    # Map each formerly unresolved witness to its owner alias and sibling.
    unresolved_target: dict[str, tuple[str, str]] = {}
    for retained_id, source_rows in witnesses_by_retained.items():
        sibling_id = siblings[retained_id]["row_id"]
        for source in source_rows:
            unresolved_target[
                source["Round292_R291_physical_witness_binding_row_id"]
            ] = (sibling_id, alias_id_by_retained[retained_id])

    incidence_rows: list[dict[str, Any]] = []
    for source in r293["Round291_physical_witness_binding_rows"]:
        source_id = source["Round292_R291_physical_witness_binding_row_id"]
        if source_id in unresolved_target:
            target_id, alias_id = unresolved_target[source_id]
            target_ids_for_row = [target_id]
        else:
            alias_id = None
            target_ids_for_row = source["terminal_registry_target_references"]
        need(
            target_ids_for_row
            and all(target in registry_ids for target in target_ids_for_row),
            f"issued Round294 incidence targets:{source_id}",
        )
        incidence_rows.append(incidence_row(
            source,
            [registry_targets[target] for target in target_ids_for_row],
            alias_id,
        ))
    incidence_rows.sort(
        key=lambda row: row[
            "Round295A_R291_physical_incidence_binding_row_id"
        ]
    )

    absence_rows = [
        absence_row(source)
        for source in r293["Round291_absence_no_binding_rows"]
    ]
    absence_rows.sort(
        key=lambda row: row["Round295A_R291_absence_no_binding_row_id"]
    )

    target_histogram = Counter(
        row["target_Round294_registry_reference_count"]
        for row in incidence_rows
    )
    witness_kind_histogram = Counter(
        row["witness_kind"] for row in incidence_rows
    )
    need(
        len(alias_rows) == 276
        and len(incidence_rows) == 113_452
        and len(absence_rows) == 28_016
        and target_histogram == {1: 1_600, 2: 111_852}
        and sum(
            row["formal_target_reference_credit"]
            for row in incidence_rows
        ) == 225_304
        and sum(
            row["formal_physical_witness_incidence_binding_credit"]
            for row in incidence_rows
        ) == 113_452
        and sum(
            row["formal_occurrence_alias_credit"] for row in alias_rows
        ) == 276
        and all(
            row["formal_occurrence_ID_issued"] is False
            for row in alias_rows + incidence_rows + absence_rows
        )
        and all(
            row[field] == 0
            for row in alias_rows + incidence_rows + absence_rows
            for field in ZERO_FIELDS
        ),
        "atomic Round295-A promotion census",
    )

    alias_ledger = make_ledger(
        alias_rows,
        ALIAS_SCHEMA,
        "FORMAL_276_SAME_ORIGIN_POSITIVE_T_CONTINUATION_ALIASES__"
        "ZERO_NEW_OCCURRENCE_IDS",
        "Round295A_retained_continuation_alias_row_id",
    )
    incidence_ledger = make_ledger(
        incidence_rows,
        INCIDENCE_SCHEMA,
        "FORMAL_COMPLETE_113452_ROUND291_PHYSICAL_WITNESS_INCIDENCE_"
        "BINDINGS__1600_UNIQUE__111852_MULTI__ZERO_UNRESOLVED",
        "Round295A_R291_physical_incidence_binding_row_id",
    )
    absence_ledger = make_ledger(
        absence_rows,
        ABSENCE_SCHEMA,
        "FORMAL_COMPLETE_28016_ROUND291_ABSENCE_WITNESSES__"
        "ZERO_REGISTRY_BINDINGS",
        "Round295A_R291_absence_no_binding_row_id",
    )

    result = {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND295A_ATOMIC_R291_POSITIVE_T_CONTINUATION_CLOSURE__"
            "276_REPRESENTATION_ALIASES__113452_FORMAL_PHYSICAL_"
            "INCIDENCE_BINDINGS__28016_ABSENCE_NO_BINDINGS__"
            "ZERO_NEW_OCCURRENCE_IDS__AWAITING_INDEPENDENT_VERIFIER",
        "input_file_pins": dict(sorted(BYTE_PINS.items())),
        "Round294_consumption": {
            "sealed_result_verification_manifest_byte_pinned": True,
            "formal_stage_A_registry_row_count": 431_208,
            "formal_pre_Round295A_representation_binding_count": 46_288,
            "registry_tranche_counts": dict(sorted(tranche_counts.items())),
            "complete_registry_ledger_streamed_and_recommitted": True,
            "complete_representation_binding_ledger_streamed_and_recommitted":
                True,
        },
        "continuation_census": {
            "unresolved_Round293_witness_count_before": 576,
            "distinct_positive_t_retained_owner_count": 276,
            "distinct_same_origin_unique_resolved_sibling_count": 276,
            "source_chart_owner_count": {
                chart: sum(
                    retained["chart"] == chart
                    for retained in retained_rows.values()
                )
                for chart in ("G:E", "G:N", "G:S", "G:W")
            },
            "owner_witness_multiplicity_histogram": dict(sorted(Counter(
                len(rows) for rows in witnesses_by_retained.values()
            ).items())),
            "special_wall_crossing_time_not_strict_wall1_origin_count":
                special_count,
            "source_endpoint_formula": "(9/25)*t",
            "source_endpoint_unique_zero": "t=0",
            "identity_basis":
                "SAME_ORIGIN_UNIQUE_RESOLVED_SIBLING_PLUS_ARTIFICIAL_T_"
                "FACE_PLUS_NO_EVENT_CONTINUATION",
            "signature_box_or_symmetry_identity_shortcut_used": False,
            "automatic_new_ID_fallback_permitted": False,
        },
        "complete_registry_overlap_exhaustion": overlap,
        "atomic_R291_binding_census": {
            "formal_physical_witness_incidence_binding_row_count": 113_452,
            "formal_unique_target_physical_witness_count": 1_600,
            "formal_multi_target_physical_witness_count": 111_852,
            "formal_unresolved_physical_witness_count": 0,
            "formal_target_registry_reference_count": 225_304,
            "physical_witness_kind_histogram":
                dict(sorted(witness_kind_histogram.items())),
            "formal_absence_no_binding_row_count": 28_016,
            "partitioned_parent_count": 8,
            "partitioned_parent_whole_binding_credit": 0,
            "incidence_bindings_are_occurrence_identity_aliases": False,
        },
        "formal_credit_transition": {
            "formal_expanded_occurrence_count": 431_208,
            "formal_new_expanded_occurrence_credit": 0,
            "formal_representation_binding_count_before": 46_288,
            "formal_representation_alias_credit_delta": 276,
            "formal_representation_binding_count_after": 46_564,
            "formal_physical_witness_incidence_binding_credit": 113_452,
            "formal_target_reference_credit": 225_304,
            "formal_absence_binding_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_seam_edge_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "representation_alias_ledger": ledger_summary(
            alias_ledger, DEFAULT_ALIASES.name
        ),
        "physical_witness_incidence_binding_ledger": ledger_summary(
            incidence_ledger, DEFAULT_INCIDENCE.name
        ),
        "absence_no_binding_ledger": ledger_summary(
            absence_ledger, DEFAULT_ABSENCE.name
        ),
        "post_Round295A_nonpromotion_freeze": {
            "legacy_pre_Round294_quotient_component_count": 63_224,
            "legacy_count_is_current_post_Round294_quotient": False,
            "post_Round294_component_DSU_status": "NOT_REBUILT",
            "post_Round295A_quotient_component_count": None,
            "maximality_status": "WAITING_EXPANDED_REGISTRY_DSU",
            "exact_key_fibre_status": "WAITING_EXPANDED_REGISTRY_DSU",
            "global_disposition_status": "WAITING_EXPANDED_REGISTRY_DSU",
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": [
            "Independently reconstruct every continuation identity and all "
            "three complete promoted tables before accepting this candidate.",
            "Re-audit and close the 396 Round289 physical incidence gaps "
            "against the now complete Round291 continuation bindings.",
            "Bind and pair all 152 true seam patches before building the "
            "expanded component/DSU edge ledger.",
        ],
        "provenance": {
            "producer_sha256": producer_sha256,
            "seed_affects_output": False,
            "Round294_or_Round293_producer_imported_or_executed": False,
            "automatic_new_occurrence_ID_fallback_used": False,
        },
    }
    return alias_ledger, incidence_ledger, absence_ledger, result


def deterministic_gzip(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=buffer, mtime=0, compresslevel=9
    ) as stream:
        for piece in chunks(value):
            stream.write(piece)
    return buffer.getvalue()


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
    parser.add_argument("--representation-alias-ledger", type=Path,
                        default=DEFAULT_ALIASES)
    parser.add_argument("--physical-incidence-ledger", type=Path,
                        default=DEFAULT_INCIDENCE)
    parser.add_argument("--absence-ledger", type=Path, default=DEFAULT_ABSENCE)
    parser.add_argument("--result", type=Path, default=DEFAULT_RESULT)
    parser.add_argument("--seed", default="295101")
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()

    producer_sha256 = file_sha256(Path(__file__).resolve())
    aliases, incidence, absence, result = build(producer_sha256)
    alias_bytes = deterministic_gzip(aliases)
    incidence_bytes = deterministic_gzip(incidence)
    absence_bytes = deterministic_gzip(absence)
    result["representation_alias_ledger"]["file_sha256"] = hashlib.sha256(
        alias_bytes
    ).hexdigest()
    result["physical_witness_incidence_binding_ledger"][
        "file_sha256"
    ] = hashlib.sha256(incidence_bytes).hexdigest()
    result["absence_no_binding_ledger"]["file_sha256"] = hashlib.sha256(
        absence_bytes
    ).hexdigest()
    result["seed_affects_output"] = False
    result["result_sha256"] = digest(result)
    result_bytes = canonical(result)
    if not arguments.no_write:
        safe_write(arguments.representation_alias_ledger, alias_bytes)
        safe_write(arguments.physical_incidence_ledger, incidence_bytes)
        safe_write(arguments.absence_ledger, absence_bytes)
        safe_write(arguments.result, result_bytes)
    print(json.dumps({
        "status": result["status"],
        "seed": arguments.seed,
        "seed_affects_output": False,
        "representation_alias_ledger_file_sha256":
            result["representation_alias_ledger"]["file_sha256"],
        "physical_incidence_ledger_file_sha256":
            result["physical_witness_incidence_binding_ledger"][
                "file_sha256"
            ],
        "absence_ledger_file_sha256":
            result["absence_no_binding_ledger"]["file_sha256"],
        "result_file_sha256": hashlib.sha256(result_bytes).hexdigest(),
        "result_sha256": result["result_sha256"],
        "census": result["atomic_R291_binding_census"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
