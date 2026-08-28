#!/usr/bin/env python3
"""Independent cacheless verifier for Round295-A.

The Round295-A producer is treated as inert bytes and is never imported or
executed.  Before any candidate output is opened, this verifier:

1. byte-pins the sealed Round293 and Round294 packages;
2. independently reconstructs all 276 Round174/Round179 same-origin
   continuation identities with exact rational and 256-bit Arb arithmetic;
3. exhausts positive-volume overlap against all three tranches of the
   431,208-row Round294 registry;
4. reconstructs the complete 113,452 physical-incidence and 28,016 absence
   tables; and
5. builds the exact expected deterministic gzip bytes and result object.

Only then are the candidate files read.  Re-signed semantic mutations and
malformed/path attacks are also required to fail closed.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from fractions import Fraction as Q
import gc
import gzip
import hashlib
import importlib
import io
import json
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any, Callable, Iterable

from flint import arb, ctx, __version__ as FLINT_VERSION


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure"
)
PRODUCER = HERE / f"{PREFIX}.py"
CANDIDATE_ALIASES = HERE / f"{PREFIX}_representation_alias_ledger.json.gz"
CANDIDATE_INCIDENCE = (
    HERE / f"{PREFIX}_physical_witness_incidence_binding_ledger.json.gz"
)
CANDIDATE_ABSENCE = HERE / f"{PREFIX}_absence_no_binding_ledger.json.gz"
CANDIDATE_RESULT = HERE / f"{PREFIX}_result.json"
DEFAULT_OUTPUT = HERE / f"{PREFIX}_verification.json"
DEFAULT_ATTACK_OUTPUT = HERE / f"{PREFIX}_attack_suite.json"

SCHEMA = "cm2.round295a.r291-positive-t-retained-continuation-closure.v1"
VERIFICATION_SCHEMA = SCHEMA + ".verification.v1"
ATTACK_SCHEMA = SCHEMA + ".attack-suite.v1"
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
R174_VERIFIER = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_"
    "verifier.py"
)
R179 = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R179_VERIFIER = "cm2_round179_source_g_residual_tube_arrangement_verifier.py"
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
G5M = "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"

INPUT_PINS = {
    R174: "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    R174_VERIFIER:
        "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
    R179: "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R179_VERIFIER:
        "292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679",
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
    G5M: "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
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


def guard_path(
    path: Path,
    maximum: int = 2_000_000_000,
    allowed_parent: Path = HERE,
) -> bytes:
    need(
        path.parent == allowed_parent
        and path.parent.resolve() == allowed_parent.resolve(),
        f"path parent:{path}",
    )
    need(path.exists() and not path.is_symlink(), f"path exists:{path}")
    info = path.stat()
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        f"path regular/link/size:{path.name}",
    )
    return path.read_bytes()


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


def read_json(name: str) -> dict[str, Any]:
    return strict_decode(guard_path(HERE / name), name)


def read_gzip_json(name: str) -> dict[str, Any]:
    path = HERE / name
    guard_path(path)
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
    for line in guard_path(HERE / name, 100_000).decode("utf-8").splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, f"manifest syntax:{name}")
        sha256, filename = match.groups()
        need(filename not in rows, f"manifest duplicate:{filename}")
        rows[filename] = sha256
    return rows


class ListCommitment:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        for piece in chunks(value):
            self.state.update(piece)
        self.count += 1

    def finish(self) -> str:
        result = self.state.copy()
        result.update(b"]")
        return result.hexdigest()


def scan_large_gzip_ledger(
    name: str, visit: Callable[[dict[str, Any]], None]
) -> dict[str, Any]:
    path = HERE / name
    guard_path(path)
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
        count = 0
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
                    need(bool(piece), f"truncated rows:{name}:{count}")
                    buffer += piece
            need(type(row) is dict, f"row object:{name}:{count}")
            visit(row)
            count += 1
            buffer = buffer[end:]
        suffix = buffer + stream.read()
    metadata = strict_decode(
        (before + '"rows":[]' + suffix).encode("utf-8"),
        f"{name}:metadata",
    )
    need(metadata["rows"] == [], f"metadata rows:{name}")
    metadata["streamed_row_count"] = count
    return metadata


def validate_row_hash(row: dict[str, Any], label: str) -> None:
    expected = row.get("row_sha256")
    payload = dict(row)
    payload.pop("row_sha256", None)
    need(
        isinstance(expected, str) and digest(payload) == expected,
        f"row hash:{label}",
    )


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


def validate_frozen_packages() -> tuple[dict[str, Any], str]:
    need(FLINT_VERSION == "0.9.0", "python-flint version")
    producer_sha256 = file_sha256(PRODUCER)
    # The current producer is pinned as inert evidence only after expected
    # reconstruction; its hash is needed in the expected provenance.
    for name, expected in INPUT_PINS.items():
        need(
            re.fullmatch(r"[0-9a-f]{64}", expected) is not None,
            f"unsealed input pin:{name}",
        )
        need(
            file_sha256(HERE / name) == expected,
            f"frozen input byte pin:{name}",
        )
    manifest293 = parse_manifest(R293_MANIFEST)
    for name in (R293_LEDGER, R293_RESULT, R293_VERIFICATION):
        need(manifest293.get(name) == INPUT_PINS[name], f"R293 manifest:{name}")
    manifest294 = parse_manifest(R294_MANIFEST)
    for name in (
        R294_PRODUCER, R294_REGISTRY, R294_BINDINGS, R294_RESULT,
        R294_VERIFIER, R294_VERIFICATION, R294_ATTACKS,
    ):
        need(manifest294.get(name) == INPUT_PINS[name], f"R294 manifest:{name}")
    result294 = read_json(R294_RESULT)
    verification294 = read_json(R294_VERIFICATION)
    verify_self_digest(result294, "result_sha256", "Round294 result")
    verify_self_digest(
        verification294, "verification_sha256", "Round294 verification"
    )
    need(
        result294.get("status", "").startswith(
            "PASS_ROUND294_ATOMIC_STAGE_A_OCCURRENCE_REGISTRY_PROMOTION"
        )
        and result294.get("census", {}).get(
            "formal_occurrence_registry_row_count"
        ) == 431_208
        and result294["census"].get(
            "formal_representation_binding_count"
        ) == 46_288
        and result294.get("scope_contract", {}).get(
            "final_exhaustive_all_stratum_registry_claimed"
        ) is False
        and result294.get("nonpromotion_freeze", {}).get(
            "post_Round294_quotient_component_count"
        ) is None
        and result294["nonpromotion_freeze"].get(
            "post_Round294_expanded_registry_component_DSU_status"
        ) == "NOT_REBUILT"
        and verification294.get("status", "").startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND294"
        ),
        "sealed Round294 semantics",
    )
    return result294, producer_sha256


def load_frontier_before_candidate() -> tuple[
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
    dispositions: dict[str, dict[str, Any]] = {}
    for row in r291["rows"]:
        validate_row_hash(row, "Round291 disposition")
        row_id = row["complete_lower_stratum_local_disposition_row_id"]
        need(row_id not in dispositions, "unique Round291 disposition ID")
        dispositions[row_id] = row
    need(len(dispositions) == 55_428, "complete Round291 dispositions")
    r179 = read_json(R179)["result"]
    origins = {
        row["origin_row_id"]: row
        for row in unpack(r179, "origin_tube_rows")
    }
    need(len(origins) == 62_012, "complete Round179 origins")
    return r291, r293, r179, dispositions, origins


def reconstruct_owner_universe(
    r293: dict[str, Any],
    dispositions: dict[str, dict[str, Any]],
    r179: dict[str, Any],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, list[dict[str, Any]]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    unresolved = [
        row for row in r293["Round291_physical_witness_binding_rows"]
        if row["binding_classification"]
        == "UNRESOLVED_POSITIVE_T_OWNER_RETAINED_VOLUME__"
        "NO_ISSUED_REGISTRY_OCCURRENCE"
    ]
    need(len(unresolved) == 576, "576 unresolved source rows")
    witnesses_by_retained: dict[str, list[dict[str, Any]]] = defaultdict(list)
    witness_cells: dict[str, dict[str, Any]] = {}
    for binding in unresolved:
        disposition = dispositions[binding["Round291_local_disposition_row_id"]]
        index = binding["physical_witness_cell_index"]
        need(
            0 <= index < disposition["physical_witness_cell_count"],
            "physical witness source index",
        )
        cell = disposition["physical_witness_cells"][index]
        need(
            cell["witness_kind"]
            in {
                "ROUND179_POSITIVE_T0_RETAINED_OWNER",
                "ROUND179_NEGATIVE_T0_SHADOW_PATCH",
            }
            and cell["owner_policy"]
            == "OUTCOME_BLIND_POSITIVE_T_SIDE_OWNS__"
            "NEGATIVE_T_SIDE_IS_SHADOW",
            "unresolved owner/shadow witness contract",
        )
        retained_id = cell["positive_owner_retained_child_row_id"]
        witnesses_by_retained[retained_id].append(binding)
        witness_cells[
            binding["Round292_R291_physical_witness_binding_row_id"]
        ] = cell
    retained_rows = {
        row["row_id"]: row
        for row in unpack(r179, "retained_3d_child_rows")
        if row["row_id"] in witnesses_by_retained
    }
    owner_origin_ids = {
        row["origin_row_id"] for row in retained_rows.values()
    }
    owner_origins = {
        row["origin_row_id"]: row
        for row in unpack(r179, "origin_tube_rows")
        if row["origin_row_id"] in owner_origin_ids
    }
    sibling_candidates: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in unpack(r179, "resolved_3d_child_rows"):
        if row["origin_row_id"] in owner_origin_ids:
            sibling_candidates[row["origin_row_id"]].append(row)
    siblings: dict[str, dict[str, Any]] = {}
    for retained_id, retained in retained_rows.items():
        rows = sibling_candidates[retained["origin_row_id"]]
        need(
            len(rows) == 1
            and retained["child_index"] == 0
            and rows[0]["child_index"] == 1,
            f"unique resolved index1 sibling:{retained_id}",
        )
        siblings[retained_id] = rows[0]
    need(
        len(retained_rows) == len(owner_origins) == len(siblings) == 276
        and Counter(len(rows) for rows in witnesses_by_retained.values())
        == {1: 60, 2: 176, 3: 24, 5: 8, 6: 4, 7: 4}
        and Counter(
            retained["chart"] for retained in retained_rows.values()
        ) == {"G:E": 69, "G:N": 69, "G:S": 69, "G:W": 69},
        "complete owner grouping census",
    )
    return retained_rows, witnesses_by_retained, siblings, witness_cells


def scan_round294_before_candidate(
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
    occurrence_commitment = ListCommitment()
    row_id_commitment = ListCommitment()
    hash_commitment = ListCommitment()
    rows_commitment = ListCommitment()

    def visit(row: dict[str, Any]) -> None:
        validate_row_hash(row, "Round294 registry")
        occurrence_id = row["registry_occurrence_id"]
        need(occurrence_id not in registry_ids, "unique Round294 occurrence")
        registry_ids.add(occurrence_id)
        occurrence_commitment.add(occurrence_id)
        row_id_commitment.add(row["Round294_occurrence_registry_row_id"])
        hash_commitment.add(row["row_sha256"])
        rows_commitment.add(row)
        entry_kind = row["registry_entry_kind"]
        tranche_ids[entry_kind].add(
            row["source_row_id"]
            if entry_kind
            == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
            else occurrence_id
        )
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
        and occurrence_commitment.finish()
        == summary["occurrence_ids_sha256"]
        and row_id_commitment.finish() == summary["row_ids_sha256"]
        and hash_commitment.finish() == summary["row_hashes_sha256"]
        and rows_commitment.finish() == summary["rows_sha256"]
        and len(registry_ids) == 431_208
        and set(targets) == target_ids,
        "Round294 registry complete stream reconstruction",
    )

    ids = ListCommitment()
    hashes = ListCommitment()
    rows = ListCommitment()

    def visit_binding(row: dict[str, Any]) -> None:
        validate_row_hash(row, "Round294 representation binding")
        ids.add(row["Round294_occurrence_representation_binding_row_id"])
        hashes.add(row["row_sha256"])
        rows.add(row)

    binding_meta = scan_large_gzip_ledger(R294_BINDINGS, visit_binding)
    binding_summary = result294["representation_binding_ledger"]
    need(
        binding_meta["streamed_row_count"]
        == binding_meta["row_count"] == 46_288
        and ids.finish() == binding_summary["row_ids_sha256"]
        and hashes.finish() == binding_summary["row_hashes_sha256"]
        and rows.finish() == binding_summary["rows_sha256"],
        "Round294 binding complete stream reconstruction",
    )
    return (
        registry_ids,
        targets,
        tranche_ids,
        {kind: len(ids) for kind, ids in tranche_ids.items()},
    )


def independently_reconstruct_continuation_math(
    retained_rows: dict[str, dict[str, Any]],
    siblings: dict[str, dict[str, Any]],
    origins: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    """Rebuild every origin split and punctured dynamic signature."""

    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    # Both older verifier sources were byte-pinned before import.  Neither
    # Round295-A producer nor any Round295-A candidate is importable here.
    math174 = importlib.import_module(
        "cm2_round174_source_g_unique_first_dynamic_occurrence_"
        "materialization_verifier"
    )
    math179 = importlib.import_module(
        "cm2_round179_source_g_residual_tube_arrangement_verifier"
    )
    ctx.prec = 256
    gate5 = strict_decode(
        guard_path(HERE / G5M, 5_000_000), G5M
    )
    registry = math174.rebuild_registry(gate5)

    # Independently bind each Round179 origin summary back to the exact
    # Round174 residual row and parent target.
    r174 = read_json(R174)["result"]
    owner_origin_ids = {
        retained["origin_row_id"] for retained in retained_rows.values()
    }
    residual_by_id = {
        row["row_id"]: row
        for row in unpack(r174, "residual_3d_tube_rows")
        if row["row_id"] in owner_origin_ids
    }
    parent_by_id = {
        row["parent_id"]: row
        for row in unpack(r174, "parent_rows")
        if row["parent_id"]
        in {origins[origin_id]["parent_id"] for origin_id in owner_origin_ids}
    }
    del r174
    gc.collect()
    need(
        len(residual_by_id) == len(owner_origin_ids) == 276,
        "complete owner Round174 residual recovery",
    )

    continuation: dict[str, dict[str, Any]] = {}
    target_proof_histogram: Counter[str] = Counter()
    event_length_histogram: Counter[int] = Counter()
    source_axis_histogram: Counter[str] = Counter()
    special_count = 0
    origin_reason_histogram: Counter[tuple[str, ...]] = Counter()

    for retained_id in sorted(retained_rows):
        retained = retained_rows[retained_id]
        sibling = siblings[retained_id]
        origin = origins[retained["origin_row_id"]]
        residual = residual_by_id[origin["origin_row_id"]]
        parent = parent_by_id[origin["parent_id"]]
        origin_reason_histogram[tuple(origin["original_reason_labels"])] += 1
        need(
            residual["row_id"] == origin["origin_row_id"]
            and residual["parent_id"] == origin["parent_id"]
            and residual["chart"] == origin["chart"]
            and residual["refinement_path"]
            == origin["original_refinement_path"]
            and residual["box"] == origin["original_box"]
            and residual["coordinate_volume"]
            == origin["original_coordinate_volume"]
            and residual["reason_labels"]
            == origin["original_reason_labels"]
            and parent["owner_target"] == origin["owner_target"],
            f"Round174/Round179 origin reconstruction:{retained_id}",
        )
        residual_identity_payload = [
            residual["chart"], residual["parent_id"],
            residual["refinement_path"], residual["box"],
            residual["reason_labels"],
        ]
        if residual["transport_source_row_id"] is not None:
            need(
                residual["provenance"]
                == "ROUND173_EXACT_ISOMETRIC_TRANSPORT"
                and residual["transport_generator"] is not None,
                f"transported Round174 residual provenance:{retained_id}",
            )
            residual_identity_payload.append(
                residual["transport_source_row_id"]
            )
        else:
            need(
                residual["provenance"]
                == "DIRECT_BOUNDED_DEPTH_UNRESOLVED_TUBE"
                and residual["transport_generator"] is None,
                f"direct Round174 residual provenance:{retained_id}",
            )
        expected_origin_id = (
            "round174-residual-3d-tube:"
            + digest(residual_identity_payload)
        )
        need(
            expected_origin_id == origin["origin_row_id"],
            f"Round174 residual content ID:{retained_id}",
        )

        origin_box = math174.atlas.AtlasBox(
            *map(Q, origin["original_box"]),
            len(origin["original_refinement_path"]),
            origin["origin_row_id"],
        )
        child0, child1 = math174.bisect(origin_box, 0)
        kind0, data0 = math174.classify_child(
            origin["chart"], child0, origin["owner_target"], registry
        )
        kind1, data1 = math174.classify_child(
            origin["chart"], child1, origin["owner_target"], registry
        )
        need(
            kind0 == "residual"
            and kind1 == "resolved"
            and data0 == retained["reason_labels"]
            and isinstance(data1, dict),
            f"independent t split classification:{retained_id}",
        )
        child0_box = math174.box_values(child0)
        child1_box = math174.box_values(child1)
        expected_retained_id = "round179-retained-child:" + digest([
            origin["origin_row_id"], 0,
            [*origin["original_refinement_path"], "t0"],
            child0_box, sorted(set(data0)),
        ])
        expected_sibling_id = "round179-resolved-child:" + digest([
            origin["origin_row_id"], 1,
            [*origin["original_refinement_path"], "t1"],
            child1_box, data1["key"]["identifier"], data1["outgoing"],
        ])
        need(
            expected_retained_id == retained_id
            and expected_sibling_id == sibling["row_id"]
            and child0_box == retained["box"]
            and child1_box == sibling["box"]
            and math174.qstr(math174.volume(child0))
            == retained["coordinate_volume"]
            and math174.qstr(math174.volume(child1))
            == sibling["coordinate_volume"]
            and data1["target"] == sibling["owner_target"]
            and data1["events"] == sibling["ordered_integer_wall_events"]
            and list(data1["pattern"]) == sibling["signed_wall_word"]
            and data1["roof"] == sibling["roof"]
            and data1["outgoing"] == sibling["outgoing_cell"]
            and data1["target_chart"] == sibling["target_chart"]
            and data1["key"]["row"] == sibling["official_key_row"]
            and data1["key"]["ordinal"] == sibling["official_key_ordinal"]
            and data1["key"]["identifier"] == sibling["official_key_id"],
            f"independent child row reconstruction:{retained_id}",
        )

        # The complete origin must fail the old closed-box classifier only at
        # the frozen endpoint-zero reason (and the four dependency-overwrap
        # wall-one reasons).  No grazing, owner, return-time, outgoing, count,
        # range, or corner-order reason is permitted.
        origin_signature, origin_reasons = math174.certify_signature(
            origin["chart"], origin_box, origin["owner_target"], registry
        )
        need(
            origin_signature is None
            and origin_reasons == origin["original_reason_labels"],
            f"complete origin reason exhaustion:{retained_id}",
        )

        cell = origin["chart"].split(":")[1]
        endpoint_axis = "X" if cell in {"N", "S"} else "Y"
        endpoint_name = (
            "source_x" if endpoint_axis == "X" else "source_y"
        )
        target_name = "hit_x" if endpoint_axis == "X" else "hit_y"
        source_axis_histogram[endpoint_axis] += 1
        math_origin = {
            "row_id": origin["origin_row_id"],
            "parent_id": origin["parent_id"],
            "chart": origin["chart"],
            "box": origin["original_box"],
            "refinement_path": origin["original_refinement_path"],
            "reason_labels": origin["original_reason_labels"],
        }
        geometry = math179.independent_geometry(
            origin["chart"], origin["owner_target"], origin_box
        )
        source_dual = geometry[endpoint_name]
        zero_face = math179.face_box(origin_box, "t", False)
        zero_geometry = math179.independent_geometry(
            origin["chart"], origin["owner_target"], zero_face
        )
        source_zero = zero_geometry[endpoint_name][0]
        # The pinned Round179 evaluator constructs the source normal
        # chartwise as (sqrt(1-t^2),t), (-sqrt(1-t^2),t),
        # (t,sqrt(1-t^2)), or (t,-sqrt(1-t^2)).  The selected endpoint
        # coordinate therefore has exact symbolic t coefficient 1 in every
        # chart, before exact rational source-radius scaling by 9/25.  Arb
        # encloses that rational with a tiny radius, so use structural
        # rational equality plus interval containment rather than comparing
        # two nonzero-radius Arb balls for object equality.
        endpoint_basis_t_coefficient = Q(1)
        endpoint_exact_t_coefficient = (
            endpoint_basis_t_coefficient * Q(9, 25)
        )
        need(
            source_zero.is_zero()
            and endpoint_exact_t_coefficient == Q(9, 25)
            and source_dual[1][0].contains(arb(9) / 25)
            and bool(source_dual[1][0] > 0)
            and origin_box.t0 == 0
            and origin_box.t1 > 0,
            f"exact source endpoint (9/25)t:{retained_id}",
        )

        endpoint_reason = (
            f"wall_endpoint_or_count_transition:{endpoint_axis}:0"
        )
        need(
            endpoint_reason in origin["original_reason_labels"],
            f"endpoint reason:{retained_id}",
        )
        wall0 = math179.expected_wall(
            math_origin, origin["owner_target"], geometry, endpoint_reason
        )
        need(
            wall0["source_factor_classification"] == "REGULAR_GRAPH"
            and wall0["source_gradient_axis"] == "t"
            and wall0["source_gradient_sign"] == "STRICT_POSITIVE"
            and wall0["target_face_classification"]
            == "STRICT_ZERO_ABSENT",
            f"wall0 factorization:{retained_id}",
        )
        if wall0["target_factor_classification"] == "STRICT_NONZERO":
            target_proof = "DIRECT_STRICT_INTERVAL"
        else:
            need(
                wall0["target_factor_classification"] == "REGULAR_GRAPH"
                and wall0["target_lower_face_sign"]
                == wall0["target_upper_face_sign"]
                in {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
                f"wall0 monotone face proof:{retained_id}",
            )
            target_proof = "STRICT_MONOTONE_EQUAL_FACE_SIGNS"
        target_proof_histogram[target_proof] += 1

        special_reasons = [
            reason for reason in origin["original_reason_labels"]
            if reason.startswith("wall_crossing_time_not_strict:")
        ]
        if special_reasons:
            need(
                special_reasons
                == [f"wall_crossing_time_not_strict:{endpoint_axis}:1"],
                f"special wall-one reason identity:{retained_id}",
            )
            special_wall = math179.expected_wall(
                math_origin, origin["owner_target"], geometry,
                special_reasons[0],
            )
            need(
                special_wall["source_factor_classification"]
                == special_wall["target_factor_classification"]
                == "STRICT_NONZERO"
                and special_wall[
                    "crossing_time_dependency_overwrap_discharged"
                ] is True,
                f"special wall-one dependency discharge:{retained_id}",
            )
            special_count += 1

        # Rebuild the punctured-origin event set from strict endpoint signs.
        # At wall zero, the exact identity q=(9/25)t supplies q>0 on 0<t<T.
        computed_events: dict[tuple[str, int], tuple[str, Any]] = {}
        event_alpha: dict[tuple[str, int], Any] = {}
        for axis in ("X", "Y"):
            qdual = geometry["source_x" if axis == "X" else "source_y"]
            hdual = geometry["hit_x" if axis == "X" else "hit_y"]
            qvalue, hvalue = qdual[0], hdual[0]
            need(
                bool(qvalue > -7) and bool(qvalue < 7)
                and bool(hvalue > -7) and bool(hvalue < 7),
                f"wall audit range:{retained_id}:{axis}",
            )
            for wall in range(-6, 7):
                qsign = math179.arb_sign(qvalue - arb(wall))
                hsign = math179.arb_sign(hvalue - arb(wall))
                if axis == endpoint_axis and wall == 0:
                    qsign = "STRICT_POSITIVE"
                    if hsign == "OVERWRAP":
                        hsign = wall0["target_lower_face_sign"]
                need(
                    qsign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
                    and hsign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
                    f"strict punctured endpoint profile:"
                    f"{retained_id}:{axis}:{wall}",
                )
                if qsign == hsign:
                    continue
                token = axis + ("+" if qsign == "STRICT_NEGATIVE" else "-")
                computed_events[(axis, wall)] = (token, wall)
                event_alpha[(axis, wall)] = (
                    arb(wall) - qvalue
                ) / (hvalue - qvalue)
        sibling_events = [
            (token, wall)
            for token, wall in sibling["ordered_integer_wall_events"]
        ]
        need(
            set(computed_events.values()) == set(sibling_events),
            f"complete punctured event set:{retained_id}",
        )
        alphas = [
            event_alpha[(token[0], wall)]
            for token, wall in sibling_events
        ]
        need(
            all(
                bool(alphas[index] < alphas[index + 1])
                for index in range(len(alphas) - 1)
            ),
            f"strict complete-origin event order:{retained_id}",
        )
        event_length_histogram[len(sibling_events)] += 1

        # Independently re-evaluate root, time and outgoing chart over the
        # complete origin.  The only removed obstruction is the artificial
        # endpoint sheet at t=0.
        qx, qy, ux, uy, s_coord, _source_cosine = math174.atlas.geometry(
            origin["chart"], origin_box
        )
        record = math174.atlas.root_record(
            origin["chart"], origin_box, origin["owner_target"]
        )
        need(
            record.classification == "strict_future_root"
            and record.near is not None
            and bool(record.discriminant > 0)
            and bool(record.near < math174.first_hit.arbq(Q(3))),
            f"root/time invariants:{retained_id}",
        )
        radical = record.discriminant.sqrt()
        radius = math174.first_hit.arbq(
            math174.first_hit.RADIUS[origin["owner_target"][0]]
        )
        normal_x = (-radical * ux + record.transverse * uy) / radius
        normal_y = (-radical * uy - record.transverse * ux) / radius
        outgoing, outgoing_reasons = math174.outgoing_cell(
            normal_x, normal_y
        )
        need(
            not outgoing_reasons
            and outgoing == sibling["outgoing_cell"],
            f"whole-origin outgoing invariant:{retained_id}",
        )
        expected_key = math174.exact_key(
            origin["chart"], origin["owner_target"],
            tuple(token for token, _wall in sibling_events), registry,
        )
        need(
            expected_key["identifier"] == sibling["official_key_id"]
            and expected_key["ordinal"] == sibling["official_key_ordinal"]
            and expected_key["row"] == sibling["official_key_row"],
            f"whole-origin exact key invariant:{retained_id}",
        )

        owner_box = qbox(retained["box"])
        sibling_box = qbox(sibling["box"])
        origin_exact_box = qbox(origin["original_box"])
        need(
            owner_box[0] == 0
            and owner_box[1] == sibling_box[0]
            and sibling_box[1] == origin_exact_box[1]
            and owner_box[2:] == sibling_box[2:] == origin_exact_box[2:]
            and volume(owner_box) + volume(sibling_box)
            == volume(origin_exact_box),
            f"exact artificial face and volume:{retained_id}",
        )
        continuation[retained_id] = {
            "artificial_split_axis": "t",
            "artificial_split_face": [
                sibling["box"][0], sibling["box"][0], *sibling["box"][2:]
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
            "wall_crossing_time_not_strict_wall1_reason_count":
                len(special_reasons),
        }

    need(
        target_proof_histogram
        == {
            "DIRECT_STRICT_INTERVAL": 268,
            "STRICT_MONOTONE_EQUAL_FACE_SIGNS": 8,
        }
        and special_count == 4
        and source_axis_histogram == {"X": 138, "Y": 138},
        "complete continuation mathematical census",
    )
    return continuation, {
        "owner_count": 276,
        "Round174_residual_IDs_rebuilt": 276,
        "Round179_retained_child_IDs_rebuilt": 276,
        "Round179_resolved_sibling_IDs_rebuilt": 276,
        "source_endpoint_axis_histogram":
            dict(sorted(source_axis_histogram.items())),
        "target_wall0_strict_nonzero_proof_histogram":
            dict(sorted(target_proof_histogram.items())),
        "resolved_sibling_event_length_histogram":
            dict(sorted(event_length_histogram.items())),
        "special_wall1_dependency_discharge_count": special_count,
        "origin_reason_histogram": {
            "|".join(reasons): count
            for reasons, count in sorted(origin_reason_histogram.items())
        },
        "all_root_owner_discriminant_time_outgoing_event_order_and_key_"
        "invariants_rebuilt": True,
        "source_endpoint_exactly_9_over_25_t_with_unique_zero_t0": True,
        "identity_basis_never_signature_box_or_symmetry": True,
    }


def independently_exhaust_registry_overlap(
    retained_rows: dict[str, dict[str, Any]],
    tranche_ids: dict[str, set[str]],
) -> tuple[dict[str, Any], dict[str, int]]:
    owners: dict[str, list[tuple[str, tuple[Q, Q, Q, Q, Q, Q]]]] = (
        defaultdict(list)
    )
    per_owner = {retained_id: 0 for retained_id in retained_rows}
    for retained_id, retained in retained_rows.items():
        owners[retained["chart"]].append((retained_id, qbox(retained["box"])))
    owner_pair_overlap = 0
    for rows in owners.values():
        for index, (_first_id, first) in enumerate(rows):
            for _second_id, second in rows[index + 1:]:
                owner_pair_overlap += int(positive_overlap(first, second))
    need(owner_pair_overlap == 0, "pairwise owner positive disjointness")

    overlap_pairs = 0

    def audit(chart: str, values: list[str]) -> None:
        nonlocal overlap_pairs
        support = qbox(values)
        for retained_id, owner in owners[chart]:
            if positive_overlap(owner, support):
                per_owner[retained_id] += 1
                overlap_pairs += 1

    preserved_ids: set[str] = set()
    r174 = read_json(R174)["result"]
    for row in unpack(r174, "resolved_3d_occurrence_rows"):
        need(row["row_id"] not in preserved_ids, "unique R174 occurrence")
        preserved_ids.add(row["row_id"])
        audit(row["chart"], row["box"])
    del r174
    gc.collect()

    r179 = read_json(R179)["result"]
    for row in unpack(r179, "resolved_3d_child_rows"):
        need(row["row_id"] not in preserved_ids, "unique R179 occurrence")
        preserved_ids.add(row["row_id"])
        audit(row["chart"], row["box"])
    del r179
    gc.collect()

    r204 = read_json(R204)["result"]
    for row in r204["formal_local_open_3D_region_ledger"]["rows"]:
        need(row["region_row_id"] not in preserved_ids, "unique R204 region")
        preserved_ids.add(row["region_row_id"])
        audit(row["chart"], row["leaf_exact_box"])
    del r204
    gc.collect()

    r208 = read_json(R208)["result"]
    for row in r208["formal_local_open_3D_signature_ledger"]["rows"]:
        need(row["region_row_id"] not in preserved_ids, "unique R208 region")
        preserved_ids.add(row["region_row_id"])
        audit(
            row["local_return_signature"]["source_chart"],
            row["Round182_leaf_box"],
        )
    del r208
    gc.collect()
    preserved_kind = "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
    need(
        len(preserved_ids) == 126_468
        and preserved_ids == tranche_ids[preserved_kind],
        "preserved tranche exact support exhaustion",
    )

    r288 = read_gzip_json(R288)
    r288_ids: set[str] = set()
    r288_envelopes = 0
    for row in r288["rows"]:
        if not row["occurrence_identity_disposition"].startswith("NEW_"):
            continue
        occurrence_id = row["reserved_candidate_occurrence_id__not_issued"]
        need(occurrence_id not in r288_ids, "unique R288 ID")
        r288_ids.add(occurrence_id)
        envelopes = row["frozen_positive_rational_support_envelopes"]
        need(bool(envelopes), f"R288 nonempty support:{occurrence_id}")
        r288_envelopes += len(envelopes)
        for support in envelopes:
            audit(row["source_chart"], support)
    del r288
    gc.collect()
    r288_kind = "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
    need(
        len(r288_ids) == 295_336
        and r288_ids == tranche_ids[r288_kind],
        "Round288 tranche exact envelope exhaustion",
    )

    squared: dict[
        str, list[tuple[str, tuple[Q, Q, Q, Q, Q, Q]]]
    ] = defaultdict(list)
    for chart, rows in owners.items():
        for retained_id, box in rows:
            squared[chart].append((
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
        support = qbox(row["exact_transformed_open_cell"])
        for retained_id, owner in squared[row["source_chart"]]:
            if positive_overlap(owner, support):
                per_owner[retained_id] += 1
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
        "Round292 refined tranche exact cell exhaustion",
    )
    need(
        overlap_pairs == 0 and set(per_owner.values()) == {0},
        "zero complete-registry positive-volume overlap",
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
    }, per_owner


def exact_alias_row(
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


def exact_incidence_row(
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


def exact_absence_row(source: dict[str, Any]) -> dict[str, Any]:
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


def exact_ledger(
    rows: list[dict[str, Any]],
    schema: str,
    status: str,
    id_field: str,
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    need(len(ids) == len(set(ids)), f"expected unique IDs:{schema}")
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


def deterministic_gzip(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=buffer, mtime=0, compresslevel=9
    ) as stream:
        for piece in chunks(value):
            stream.write(piece)
    return buffer.getvalue()


def independently_build_expected() -> dict[str, Any]:
    result294, producer_sha256 = validate_frozen_packages()
    _r291, r293, r179, dispositions, origins = (
        load_frontier_before_candidate()
    )
    (
        retained_rows,
        witnesses_by_retained,
        siblings,
        _witness_cells,
    ) = reconstruct_owner_universe(r293, dispositions, r179)
    continuation, math_audit = independently_reconstruct_continuation_math(
        retained_rows, siblings, origins
    )
    target_ids = {
        target
        for row in r293["Round291_physical_witness_binding_rows"]
        for target in row["terminal_registry_target_references"]
    } | {sibling["row_id"] for sibling in siblings.values()}
    (
        registry_ids,
        registry_targets,
        tranche_ids,
        tranche_counts,
    ) = scan_round294_before_candidate(result294, target_ids)
    overlap, per_owner_overlap = independently_exhaust_registry_overlap(
        retained_rows, tranche_ids
    )

    alias_rows: list[dict[str, Any]] = []
    alias_id_by_retained: dict[str, str] = {}
    for retained_id in sorted(retained_rows):
        retained = retained_rows[retained_id]
        sibling = siblings[retained_id]
        origin = origins[retained["origin_row_id"]]
        target = registry_targets[sibling["row_id"]]
        need(
            target["registry_entry_kind"]
            == "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
            and target["source_occurrence_class"] == "ROUND179_RESOLVED"
            and target["physical_support_chart"] == retained["chart"]
            and target["official_key_id"] == sibling["official_key_id"],
            f"independent Round294 sibling binding:{retained_id}",
        )
        row = exact_alias_row(
            retained,
            origin,
            sibling,
            target,
            len(witnesses_by_retained[retained_id]),
            continuation[retained_id],
            per_owner_overlap[retained_id],
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

    unresolved_target: dict[str, tuple[str, str]] = {}
    for retained_id, sources in witnesses_by_retained.items():
        for source in sources:
            unresolved_target[
                source["Round292_R291_physical_witness_binding_row_id"]
            ] = (
                siblings[retained_id]["row_id"],
                alias_id_by_retained[retained_id],
            )

    incidence_rows: list[dict[str, Any]] = []
    for source in r293["Round291_physical_witness_binding_rows"]:
        source_id = source["Round292_R291_physical_witness_binding_row_id"]
        if source_id in unresolved_target:
            target_id, alias_id = unresolved_target[source_id]
            row_target_ids = [target_id]
        else:
            alias_id = None
            row_target_ids = source["terminal_registry_target_references"]
        need(
            bool(row_target_ids)
            and all(target in registry_ids for target in row_target_ids),
            f"independent issued incidence targets:{source_id}",
        )
        incidence_rows.append(exact_incidence_row(
            source,
            [registry_targets[target] for target in row_target_ids],
            alias_id,
        ))
    incidence_rows.sort(
        key=lambda row: row[
            "Round295A_R291_physical_incidence_binding_row_id"
        ]
    )
    absence_rows = [
        exact_absence_row(source)
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
        "independent atomic expected census",
    )

    alias_ledger = exact_ledger(
        alias_rows,
        ALIAS_SCHEMA,
        "FORMAL_276_SAME_ORIGIN_POSITIVE_T_CONTINUATION_ALIASES__"
        "ZERO_NEW_OCCURRENCE_IDS",
        "Round295A_retained_continuation_alias_row_id",
    )
    incidence_ledger = exact_ledger(
        incidence_rows,
        INCIDENCE_SCHEMA,
        "FORMAL_COMPLETE_113452_ROUND291_PHYSICAL_WITNESS_INCIDENCE_"
        "BINDINGS__1600_UNIQUE__111852_MULTI__ZERO_UNRESOLVED",
        "Round295A_R291_physical_incidence_binding_row_id",
    )
    absence_ledger = exact_ledger(
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
        "input_file_pins": dict(sorted({
            name: sha256
            for name, sha256 in INPUT_PINS.items()
            if name not in {R174_VERIFIER, R179_VERIFIER, G5M}
        }.items())),
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
            "special_wall_crossing_time_not_strict_wall1_origin_count": 4,
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
            alias_ledger, CANDIDATE_ALIASES.name
        ),
        "physical_witness_incidence_binding_ledger": ledger_summary(
            incidence_ledger, CANDIDATE_INCIDENCE.name
        ),
        "absence_no_binding_ledger": ledger_summary(
            absence_ledger, CANDIDATE_ABSENCE.name
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
    alias_bytes = deterministic_gzip(alias_ledger)
    incidence_bytes = deterministic_gzip(incidence_ledger)
    absence_bytes = deterministic_gzip(absence_ledger)
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
    # JSON object member names are strings.  In-memory Counters above use
    # integer multiplicities, which the canonical encoder correctly emits as
    # JSON string member names.  Normalize the expected comparison object
    # through the already constructed strict canonical bytes so Python's
    # pre-encoding integer keys cannot create a false object-only mismatch.
    result_object = strict_decode(
        result_bytes, "independently reconstructed Round295A result"
    )
    return {
        "aliases": alias_ledger,
        "incidence": incidence_ledger,
        "absence": absence_ledger,
        "result": result_object,
        "alias_bytes": alias_bytes,
        "incidence_bytes": incidence_bytes,
        "absence_bytes": absence_bytes,
        "result_bytes": result_bytes,
        "math_audit": math_audit,
    }


def resign_row(
    row: dict[str, Any],
    id_field: str,
    prefix: str,
    domain: str,
) -> dict[str, Any]:
    payload = {
        key: value
        for key, value in row.items()
        if key not in {id_field, "row_sha256"}
    }
    rebuilt = {
        id_field: prefix + digest([domain, payload]),
        **payload,
    }
    rebuilt["row_sha256"] = digest(rebuilt)
    return rebuilt


def validate_alias_semantics(
    row: dict[str, Any], expected: dict[str, Any]
) -> None:
    validate_row_hash(row, "attack alias")
    need(row == expected, "alias must equal independent mathematical row")
    need(
        row["identity_basis"]
        == "SAME_ROUND174_ORIGIN__UNIQUE_RESOLVED_INDEX1_SIBLING__"
        "ARTIFICIAL_T_SPLIT_FACE__NO_EVENT_CONTINUATION"
        and row["source_endpoint_exact_formula"] == "(9/25)*t"
        and row["source_endpoint_unique_zero"] == "t=0"
        and row["formal_occurrence_alias_credit"] == 1
        and row["formal_occurrence_ID_issued"] is False
        and row["undesignated_positive_volume_overlap_count"] == 0
        and all(row[field] == 0 for field in ZERO_FIELDS),
        "alias semantic contract",
    )


def validate_incidence_semantics(
    row: dict[str, Any], expected: dict[str, Any]
) -> None:
    validate_row_hash(row, "attack incidence")
    need(row == expected, "incidence must equal independent full binding row")
    need(
        row["target_Round294_registry_reference_count"] in {1, 2}
        and len(row["target_Round294_registry_occurrence_ids"])
        == row["target_Round294_registry_reference_count"]
        and row["formal_physical_witness_incidence_binding_credit"] == 1
        and row["formal_target_reference_credit"]
        == row["target_Round294_registry_reference_count"]
        and row["formal_occurrence_alias_credit"] == 0
        and row["formal_occurrence_ID_issued"] is False
        and all(row[field] == 0 for field in ZERO_FIELDS),
        "incidence semantic contract",
    )


def validate_absence_semantics(
    row: dict[str, Any], expected: dict[str, Any]
) -> None:
    validate_row_hash(row, "attack absence")
    need(row == expected, "absence must equal independent no-binding row")
    need(
        row["target_Round294_registry_occurrence_ids"] == []
        and row["target_Round294_registry_reference_count"] == 0
        and row["formal_physical_witness_incidence_binding_credit"] == 0
        and row["formal_target_reference_credit"] == 0
        and row["formal_occurrence_alias_credit"] == 0
        and all(row[field] == 0 for field in ZERO_FIELDS),
        "absence semantic contract",
    )


def validate_result_semantics(
    result: dict[str, Any], expected: dict[str, Any]
) -> None:
    verify_self_digest(result, "result_sha256", "attack result")
    need(result == expected, "result exact independent reconstruction")
    need(
        result["formal_credit_transition"][
            "formal_expanded_occurrence_count"
        ] == 431_208
        and result["formal_credit_transition"][
            "formal_new_expanded_occurrence_credit"
        ] == 0
        and result["formal_credit_transition"][
            "formal_representation_binding_count_after"
        ] == 46_564
        and result["atomic_R291_binding_census"][
            "formal_unresolved_physical_witness_count"
        ] == 0
        and result["post_Round295A_nonpromotion_freeze"][
            "post_Round295A_quotient_component_count"
        ] is None
        and result["post_Round295A_nonpromotion_freeze"][
            "post_Round294_component_DSU_status"
        ] == "NOT_REBUILT",
        "result semantic contract",
    )


def run_targeted_attacks(expected: dict[str, Any]) -> dict[str, Any]:
    labels: list[str] = []

    def reject(label: str, action: Callable[[], None]) -> None:
        try:
            action()
        except Exception:
            labels.append(label)
            return
        raise VerificationError(f"attack accepted:{label}")

    alias_expected = expected["aliases"]["rows"][0]
    alias_id = "Round295A_retained_continuation_alias_row_id"
    alias_attacks = (
        (
            "forge_alias_registry_target",
            "target_Round294_registry_occurrence_id",
            "round179-resolved-child:" + "0" * 64,
        ),
        (
            "replace_identity_basis_with_signature",
            "identity_basis",
            "SIGNATURE_EQUALITY",
        ),
        (
            "claim_signature_identity_shortcut",
            "signature_or_box_equality_used_as_identity_basis",
            True,
        ),
        (
            "forge_source_endpoint_formula",
            "source_endpoint_exact_formula",
            "(9/25)*t+1",
        ),
        (
            "erase_unique_t0_zero",
            "source_endpoint_unique_zero",
            "NONE",
        ),
        (
            "forge_artificial_split_face",
            "artificial_split_face",
            ["0", "0", "0", "1", "0", "1"],
        ),
        (
            "claim_undesignated_overlap",
            "undesignated_positive_volume_overlap_count",
            1,
        ),
        (
            "issue_new_occurrence_from_alias",
            "formal_occurrence_ID_issued",
            True,
        ),
        (
            "grant_alias_component_credit",
            "formal_component_union_credit",
            1,
        ),
        (
            "grant_alias_identity_collapse",
            "formal_identity_collapse_credit",
            1,
        ),
    )
    for label, field, value in alias_attacks:
        def action(
            field: str = field,
            value: Any = value,
        ) -> None:
            row = copy.deepcopy(alias_expected)
            row[field] = value
            row = resign_row(
                row, alias_id,
                "round295a-retained-continuation-alias:",
                "ROUND295A_RETAINED_CONTINUATION_ALIAS_V1",
            )
            validate_alias_semantics(row, alias_expected)
        reject(label, action)

    incidence_expected = expected["incidence"]["rows"][0]
    incidence_id = "Round295A_R291_physical_incidence_binding_row_id"
    incidence_attacks = (
        (
            "erase_incidence_target",
            "target_Round294_registry_occurrence_ids",
            [],
        ),
        (
            "forge_incidence_target_count",
            "target_Round294_registry_reference_count",
            0,
        ),
        (
            "mark_incidence_unresolved",
            "Round295A_binding_classification",
            "UNRESOLVED",
        ),
        (
            "grant_incidence_alias_credit",
            "formal_occurrence_alias_credit",
            1,
        ),
        (
            "issue_occurrence_from_incidence",
            "formal_occurrence_ID_issued",
            True,
        ),
        (
            "grant_incidence_component_credit",
            "formal_component_union_credit",
            1,
        ),
        (
            "grant_incidence_seam_credit",
            "formal_seam_edge_credit",
            1,
        ),
        (
            "grant_partitioned_whole_parent",
            "partitioned_parent_whole_binding_credit",
            1,
        ),
    )
    for label, field, value in incidence_attacks:
        def action(
            field: str = field,
            value: Any = value,
        ) -> None:
            row = copy.deepcopy(incidence_expected)
            row[field] = value
            row = resign_row(
                row, incidence_id,
                "round295a-r291-physical-incidence:",
                "ROUND295A_COMPLETE_R291_PHYSICAL_INCIDENCE_V1",
            )
            validate_incidence_semantics(row, incidence_expected)
        reject(label, action)

    absence_expected = expected["absence"]["rows"][0]
    absence_id = "Round295A_R291_absence_no_binding_row_id"
    absence_attacks = (
        (
            "bind_absence_to_registry",
            "target_Round294_registry_occurrence_ids",
            ["round179-resolved-child:" + "0" * 64],
        ),
        (
            "grant_absence_target_credit",
            "formal_target_reference_credit",
            1,
        ),
        (
            "grant_absence_incidence_credit",
            "formal_physical_witness_incidence_binding_credit",
            1,
        ),
    )
    for label, field, value in absence_attacks:
        def action(
            field: str = field,
            value: Any = value,
        ) -> None:
            row = copy.deepcopy(absence_expected)
            row[field] = value
            row = resign_row(
                row, absence_id,
                "round295a-r291-absence-no-binding:",
                "ROUND295A_COMPLETE_R291_ABSENCE_NO_BINDING_V1",
            )
            validate_absence_semantics(row, absence_expected)
        reject(label, action)

    result_expected = expected["result"]
    result_attacks: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
        (
            "increment_registry_count",
            lambda row: row["formal_credit_transition"].__setitem__(
                "formal_expanded_occurrence_count", 431_209
            ),
        ),
        (
            "grant_new_occurrence_credit",
            lambda row: row["formal_credit_transition"].__setitem__(
                "formal_new_expanded_occurrence_credit", 1
            ),
        ),
        (
            "forge_alias_total",
            lambda row: row["formal_credit_transition"].__setitem__(
                "formal_representation_binding_count_after", 46_565
            ),
        ),
        (
            "restore_R291_unresolved",
            lambda row: row["atomic_R291_binding_census"].__setitem__(
                "formal_unresolved_physical_witness_count", 1
            ),
        ),
        (
            "reuse_legacy_quotient_as_current",
            lambda row: row["post_Round295A_nonpromotion_freeze"].__setitem__(
                "post_Round295A_quotient_component_count", 63_224
            ),
        ),
        (
            "grant_DSU_status",
            lambda row: row["post_Round295A_nonpromotion_freeze"].__setitem__(
                "post_Round294_component_DSU_status", "REBUILT"
            ),
        ),
        (
            "claim_final_CM2",
            lambda row: row["post_Round295A_nonpromotion_freeze"].__setitem__(
                "CM2", "CERTIFIED"
            ),
        ),
        (
            "seed_affects_output",
            lambda row: row.__setitem__("seed_affects_output", True),
        ),
    )
    for label, mutate in result_attacks:
        def action(mutate: Callable[[dict[str, Any]], None] = mutate) -> None:
            value = copy.deepcopy(result_expected)
            value.pop("result_sha256")
            mutate(value)
            value["result_sha256"] = digest(value)
            validate_result_semantics(value, result_expected)
        reject(label, action)

    # Malformed and filesystem attacks use isolated temporary paths and never
    # alter a candidate or frozen input.
    reject(
        "duplicate_json_key",
        lambda: strict_decode(b'{"a":1,"a":1}', "duplicate-attack"),
    )
    reject(
        "nonfinite_json_constant",
        lambda: strict_decode(b'{"a":NaN}', "nan-attack"),
    )
    reject(
        "nul_json",
        lambda: strict_decode(b'{"a":"\\u0000"}\x00', "nul-attack"),
    )
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        regular = root / "regular"
        regular.write_bytes(b"x")
        symlink = root / "symlink"
        symlink.symlink_to(regular)
        hardlink = root / "hardlink"
        hardlink.hardlink_to(regular)
        reject(
            "symlink_input",
            lambda: guard_path(symlink, allowed_parent=root),
        )
        reject(
            "hardlink_input",
            lambda: guard_path(hardlink, allowed_parent=root),
        )
        reject(
            "path_traversal_input",
            lambda: guard_path(HERE / ".." / HERE.name / R291),
        )
        malformed = root / "bad.json.gz"
        malformed.write_bytes(b"not-gzip")

        def malformed_action() -> None:
            with gzip.open(malformed, "rb") as stream:
                stream.read()
        reject("malformed_gzip", malformed_action)

    return {
        "attack_count": len(labels),
        "rejected_count": len(labels),
        "attack_labels": labels,
        "all_targeted_resigned_and_malformed_attacks_rejected": True,
        "resigned_semantic_attack_count": (
            len(alias_attacks)
            + len(incidence_attacks)
            + len(absence_attacks)
            + len(result_attacks)
        ),
        "malformed_or_path_attack_count": 7,
    }


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
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--attack-output", type=Path, default=DEFAULT_ATTACK_OUTPUT
    )
    parser.add_argument("--seed", default="295171")
    arguments = parser.parse_args()

    # This entire call completes before any candidate output is opened.
    expected = independently_build_expected()
    expected_reconstruction_completed_before_candidate_open = True

    alias_raw = guard_path(CANDIDATE_ALIASES)
    incidence_raw = guard_path(CANDIDATE_INCIDENCE)
    absence_raw = guard_path(CANDIDATE_ABSENCE)
    result_raw = guard_path(CANDIDATE_RESULT)
    need(
        alias_raw == expected["alias_bytes"]
        and incidence_raw == expected["incidence_bytes"]
        and absence_raw == expected["absence_bytes"]
        and result_raw == expected["result_bytes"],
        "candidate deterministic bytes exact independent expectation",
    )
    candidate_aliases = strict_decode(
        gzip.decompress(alias_raw), CANDIDATE_ALIASES.name
    )
    candidate_incidence = strict_decode(
        gzip.decompress(incidence_raw), CANDIDATE_INCIDENCE.name
    )
    candidate_absence = strict_decode(
        gzip.decompress(absence_raw), CANDIDATE_ABSENCE.name
    )
    candidate_result = strict_decode(result_raw, CANDIDATE_RESULT.name)
    need(
        candidate_aliases == expected["aliases"]
        and candidate_incidence == expected["incidence"]
        and candidate_absence == expected["absence"]
        and candidate_result == expected["result"],
        "candidate object exact independent expectation",
    )
    validate_result_semantics(candidate_result, expected["result"])
    attacks = run_targeted_attacks(expected)
    need(
        attacks["attack_count"] == attacks["rejected_count"] == 36,
        "complete attack rejection census",
    )
    attack_suite = {
        "schema": ATTACK_SCHEMA,
        "status":
            "PASS_ROUND295A_36_OF_36_RECLOSED_SEMANTIC_MALFORMED_"
            "AND_PATH_ATTACKS_REJECTED",
        "candidate_basis": {
            "representation_alias_ledger_file_sha256":
                hashlib.sha256(alias_raw).hexdigest(),
            "physical_incidence_ledger_file_sha256":
                hashlib.sha256(incidence_raw).hexdigest(),
            "absence_ledger_file_sha256":
                hashlib.sha256(absence_raw).hexdigest(),
            "result_file_sha256": hashlib.sha256(result_raw).hexdigest(),
            "candidate_result_sha256": candidate_result["result_sha256"],
            "all_candidate_files_first_matched_independently_"
            "reconstructed_exact_bytes": True,
        },
        "attacks": attacks,
        "seed_affects_output": False,
    }
    attack_suite["attack_suite_sha256"] = digest(attack_suite)
    attack_payload = canonical(attack_suite)

    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status":
            "PASS_INDEPENDENT_CACHELESS_ROUND295A_R291_CONTINUATION_"
            "CLOSURE__276_ALIASES__113452_COMPLETE_PHYSICAL_INCIDENCE_"
            "BINDINGS__28016_ABSENCE_NO_BINDINGS__576_TO_ZERO_"
            "UNRESOLVED__ZERO_NEW_OCCURRENCES",
        "seed_affects_output": False,
        "independence_contract": {
            "Round295A_producer_imported_or_executed": False,
            "Round295A_candidate_opened_before_expected_reconstruction":
                False,
            "expected_reconstruction_completed_before_candidate_open":
                expected_reconstruction_completed_before_candidate_open,
            "Round293_or_Round294_producer_imported_or_executed": False,
            "Round174_and_Round179_independent_verifiers_used_as_pinned_"
            "lower_level_math_evaluators": True,
            "cache_pickle_or_pyc_input_used": False,
            "complete_431208_registry_streamed_and_recommitted": True,
            "complete_46288_prior_binding_table_streamed_and_recommitted":
                True,
            "complete_R291_physical_and_absence_frontiers_reconstructed":
                True,
        },
        "mathematical_reconstruction": expected["math_audit"],
        "overlap_reconstruction":
            expected["result"]["complete_registry_overlap_exhaustion"],
        "candidate_file_audit": {
            "producer_file_sha256": file_sha256(PRODUCER),
            "representation_alias_ledger_file_sha256":
                hashlib.sha256(alias_raw).hexdigest(),
            "physical_incidence_ledger_file_sha256":
                hashlib.sha256(incidence_raw).hexdigest(),
            "absence_ledger_file_sha256":
                hashlib.sha256(absence_raw).hexdigest(),
            "result_file_sha256": hashlib.sha256(result_raw).hexdigest(),
            "candidate_result_sha256": candidate_result["result_sha256"],
            "all_four_candidate_files_exact_expected_bytes": True,
            "all_four_candidate_objects_exact_expected_values": True,
            "all_three_gzip_streams_decompress_strictly": True,
            "all_rows_closed_by_content_SHA256": True,
        },
        "atomic_promotion_audit": {
            "representation_alias_row_count": 276,
            "physical_witness_incidence_binding_row_count": 113_452,
            "absence_no_binding_row_count": 28_016,
            "unique_target_witness_count": 1_600,
            "multi_target_witness_count": 111_852,
            "target_registry_reference_count": 225_304,
            "unresolved_witness_count": 0,
            "representation_binding_count_before": 46_288,
            "representation_binding_count_after": 46_564,
            "expanded_occurrence_count": 431_208,
            "new_occurrence_count": 0,
            "incidence_rows_are_identity_aliases": False,
            "partitioned_parent_count": 8,
            "partitioned_parent_whole_binding_credit": 0,
        },
        "targeted_reclosed_attacks": attacks,
        "attack_suite_audit": {
            "filename": DEFAULT_ATTACK_OUTPUT.name,
            "file_sha256": hashlib.sha256(attack_payload).hexdigest(),
            "attack_suite_sha256":
                attack_suite["attack_suite_sha256"],
            "attack_count": attacks["attack_count"],
            "rejected_count": attacks["rejected_count"],
        },
        "strict_nonpromotion": {
            "post_Round294_component_DSU_status": "NOT_REBUILT",
            "post_Round295A_quotient_component_count": None,
            "legacy_pre_Round294_63224_used_as_current": False,
            "component_union_credit": 0,
            "DSU_rank_reduction_credit": 0,
            "seam_edge_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "maximality_credit": 0,
            "fibre_credit": 0,
            "global_disposition_credit": 0,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    verification["verification_sha256"] = digest(verification)
    payload = canonical(verification)
    safe_write(arguments.attack_output, attack_payload)
    safe_write(arguments.output, payload)
    print(json.dumps({
        "status": verification["status"],
        "seed": arguments.seed,
        "seed_affects_output": False,
        "verification_file_sha256": hashlib.sha256(payload).hexdigest(),
        "verification_sha256": verification["verification_sha256"],
        "attack_suite_file_sha256":
            hashlib.sha256(attack_payload).hexdigest(),
        "attack_suite_sha256": attack_suite["attack_suite_sha256"],
        "attack_count": attacks["attack_count"],
        "mathematical_reconstruction":
            verification["mathematical_reconstruction"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
