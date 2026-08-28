#!/usr/bin/env python3
"""Atomically promote the sealed Source-G Stage-A occurrence registry.

Round294 promotes exactly the already constructed, overlap-exhausted Stage-A
identity frontier:

* 126,468 pre-existing Round266 occurrence IDs are preserved;
* 295,336 Round288 canonical-atom IDs are issued;
* 9,404 overlap-refined Round287 support-component IDs are issued; and
* 46,288 representation bindings are recorded without collapsing identities.

This program deliberately delegates no geometry, overlap, component, DSU,
seam, maximality, fibre, or disposition decision to Round294.  The complete
Round292 overlap result, ledger, independent verification, and manifest are
byte-pinned before the inert Round292 candidate constructor is loaded.  The
constructor is used only to reconstruct its deterministic candidate tables;
Round294 then performs a closed, census-preserving status/credit transition.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gc
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import tempfile
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round294_source_g_occurrence_registry_atomic_promotion"
DEFAULT_REGISTRY = HERE / f"{PREFIX}_registry_ledger.json.gz"
DEFAULT_BINDINGS = HERE / f"{PREFIX}_representation_binding_ledger.json.gz"
DEFAULT_RESULT = HERE / f"{PREFIX}_result.json"

SCHEMA = "cm2.round294.source-g-occurrence-registry-atomic-promotion.v1"
REGISTRY_SCHEMA = "cm2.round294.source-g-occurrence-registry-ledger.v1"
BINDING_SCHEMA = (
    "cm2.round294.source-g-occurrence-representation-binding-ledger.v1"
)
PROMOTED = "FORMALLY_PROMOTED_ROUND294_ATOMIC_OCCURRENCE_REGISTRY"
OLD_PRODUCER = (
    "cm2_round292_source_g_occurrence_registry_candidate_construction.py"
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

BYTE_PINS = {
    OLD_PRODUCER:
        "2c0b7e864839880f47cca2989b3f8d48fcec0399c0644c92f8aabab225402004",
    OVERLAP_RESULT:
        "f3887e75f4ef62459b75d8c77eee4781ec14f57651b4feb09b8d7ca8e372c508",
    OVERLAP_LEDGER:
        "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    OVERLAP_VERIFICATION:
        "7088e4f0927100e3c2b36f164e4f64e7b7aa0db5f81b4201c3967f16ba07ddfd",
    OVERLAP_MANIFEST:
        "4ea92e4112cae18aa0c13a6d2308816bafc19e4129c09d8b6be914268cfc4870",
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


class Round294Error(RuntimeError):
    """Fail-closed Round294 contract violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Round294Error(label)


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


def verify_self_digest(document: dict[str, Any], field: str, label: str) -> None:
    expected = document.get(field)
    payload = dict(document)
    payload.pop(field, None)
    need(
        isinstance(expected, str)
        and re.fullmatch(r"[0-9a-f]{64}", expected) is not None
        and digest(payload) == expected,
        f"{label} self digest",
    )


def parse_manifest(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, f"manifest syntax:{line!r}")
        sha256, filename = match.groups()
        need(filename not in rows, f"manifest duplicate:{filename}")
        rows[filename] = sha256
    return rows


def validate_sealed_overlap_package() -> dict[str, Any]:
    actual = {
        name: file_sha256(HERE / name)
        for name in sorted(BYTE_PINS)
    }
    need(actual == dict(sorted(BYTE_PINS.items())), "Round294 byte pins")
    manifest = parse_manifest(HERE / OVERLAP_MANIFEST)
    for name in (OVERLAP_RESULT, OVERLAP_LEDGER, OVERLAP_VERIFICATION):
        need(
            manifest.get(name) == BYTE_PINS[name],
            f"sealed overlap manifest binding:{name}",
        )
    with (HERE / OVERLAP_VERIFICATION).open("rb") as stream:
        verification = json.load(stream)
    verify_self_digest(
        verification, "verification_sha256", "Round292 overlap verification"
    )
    reconstruction = verification.get("independent_reconstruction", {})
    attacks = verification.get("targeted_reclosed_attacks", {})
    audit = verification.get("candidate_result_audit", {})
    ledger_audit = verification.get("ledger_commitment_audit", {})
    need(
        verification.get("schema")
        == "cm2.round292.r287-registry-overlap-exhaustion-probe.v1."
        "verification.v1"
        and verification.get("status", "").startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND292_R287_REGISTRY_OVERLAP"
        )
        and audit.get("candidate_file_sha256") == BYTE_PINS[OVERLAP_RESULT]
        and ledger_audit.get("deterministic_gzip_file_sha256")
        == BYTE_PINS[OVERLAP_LEDGER]
        and reconstruction.get("refined_new_support_component_count") == 9_404
        and reconstruction.get("occupied_unique_target_refinement_cell_count")
        == 1_600
        and reconstruction.get("pairwise_unresolved_positive_overlap_count")
        == 0
        and attacks.get("all_targeted_resigned_attacks_rejected") is True
        and attacks.get("attack_count") == 31,
        "sealed independent Round292 overlap package",
    )
    return verification


def load_inert_round292_builder() -> Any:
    path = HERE / OLD_PRODUCER
    spec = importlib.util.spec_from_file_location(
        "_round294_inert_round292_candidate_builder", path
    )
    need(spec is not None and spec.loader is not None, "Round292 load spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def promoted_registry_row(old: dict[str, Any]) -> dict[str, Any]:
    payload = dict(old)
    old_hash = payload.pop("row_sha256")
    old_row_id = payload.pop("Round292_registry_candidate_row_id")
    is_new = (
        payload["registry_identity_status"]
        == "CANDIDATE_NEW_ID__NOT_FORMALLY_ISSUED"
    )
    payload.update({
        "source_Round292_registry_candidate_row_id": old_row_id,
        "source_Round292_registry_candidate_row_sha256": old_hash,
        "registry_identity_status": (
            "FORMALLY_ISSUED_ROUND294_ATOMIC_OCCURRENCE_ID"
            if is_new else
            "PRESERVED_EXISTING_ID_IN_ROUND294_FORMAL_REGISTRY"
        ),
        "registry_promotion_status": PROMOTED,
        "formal_new_expanded_occurrence_credit": int(is_new),
        "formal_occurrence_alias_credit": 0,
    })
    for field in ZERO_UNPROMOTED_FIELDS:
        payload[field] = 0
    row_id = "round294-occurrence-registry:" + digest([
        "ROUND294_ATOMIC_OCCURRENCE_REGISTRY_ROW_V1", payload
    ])
    row = {"Round294_occurrence_registry_row_id": row_id, **payload}
    row["row_sha256"] = digest(row)
    return row


def promoted_binding_row(old: dict[str, Any]) -> dict[str, Any]:
    payload = dict(old)
    old_hash = payload.pop("row_sha256")
    old_row_id = payload.pop("Round292_alias_binding_candidate_row_id")
    payload.update({
        "source_Round292_alias_binding_candidate_row_id": old_row_id,
        "source_Round292_alias_binding_candidate_row_sha256": old_hash,
        "alias_binding_status":
            "FORMALLY_RECORDED_ROUND294_REPRESENTATION_BINDING",
        "formal_new_expanded_occurrence_credit": 0,
        "formal_occurrence_alias_credit": 1,
    })
    for field in ZERO_UNPROMOTED_FIELDS:
        payload[field] = 0
    row_id = "round294-occurrence-representation-binding:" + digest([
        "ROUND294_ATOMIC_OCCURRENCE_REPRESENTATION_BINDING_ROW_V1", payload
    ])
    row = {
        "Round294_occurrence_representation_binding_row_id": row_id,
        **payload,
    }
    row["row_sha256"] = digest(row)
    return row


def ledger(
    *,
    rows: list[dict[str, Any]],
    schema: str,
    status: str,
    id_field: str,
    occurrence_field: str | None = None,
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    need(len(ids) == len(set(ids)), f"unique output IDs:{id_field}")
    value = {
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
        value["occurrence_ids_sha256"] = digest(occurrence_ids)
    return value


def summary(value: dict[str, Any], filename: str) -> dict[str, Any]:
    keys = (
        "schema", "row_count", "row_ids_sha256", "row_hashes_sha256",
        "rows_sha256",
    )
    result = {"filename": filename}
    result.update({key: value[key] for key in keys})
    if "occurrence_ids_sha256" in value:
        result["occurrence_ids_sha256"] = value["occurrence_ids_sha256"]
    return result


def build(
    producer_sha256: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    overlap_verification = validate_sealed_overlap_package()
    old = load_inert_round292_builder()
    candidate_registry, candidate_aliases, candidate_result = old.build(
        BYTE_PINS[OLD_PRODUCER]
    )
    need(
        candidate_registry.get("row_count") == 431_208
        and candidate_aliases.get("row_count") == 46_288
        and candidate_result.get("census", {}).get(
            "candidate_new_occurrence_count"
        ) == 304_740
        and candidate_result.get("superseded_naive_census", {}).get(
            "naive_registry_candidate_count"
        ) == 431_824
        and candidate_result["superseded_naive_census"].get(
            "direct_Round287_union_ID_issuance_valid"
        ) is False,
        "Round292 candidate reconstruction census",
    )

    registry_rows = [
        promoted_registry_row(row) for row in candidate_registry["rows"]
    ]
    binding_rows = [
        promoted_binding_row(row) for row in candidate_aliases["rows"]
    ]
    registry_rows.sort(key=lambda row: row["registry_occurrence_id"])
    binding_rows.sort(
        key=lambda row: row[
            "Round294_occurrence_representation_binding_row_id"
        ]
    )

    registry_histogram = Counter(
        row["registry_entry_kind"] for row in registry_rows
    )
    binding_histogram = Counter(
        row["alias_source_kind"] for row in binding_rows
    )
    occurrence_ids = [row["registry_occurrence_id"] for row in registry_rows]
    need(
        len(registry_rows) == len(set(occurrence_ids)) == 431_208
        and sum(
            row["formal_new_expanded_occurrence_credit"]
            for row in registry_rows
        ) == 304_740
        and sum(
            row["formal_occurrence_alias_credit"] for row in registry_rows
        ) == 0
        and len(binding_rows) == 46_288
        and sum(
            row["formal_occurrence_alias_credit"] for row in binding_rows
        ) == 46_288
        and all(
            row[field] == 0
            for row in registry_rows + binding_rows
            for field in ZERO_UNPROMOTED_FIELDS
        ),
        "strict Round294 promotion census and credit partition",
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
        },
        "strict Round294 kind histograms",
    )

    registry_ledger = ledger(
        rows=registry_rows,
        schema=REGISTRY_SCHEMA,
        status=(
            "FORMAL_STAGE_A_431208_ROW_OCCURRENCE_REGISTRY_FRONTIER__"
            "126468_PRESERVED__"
            "295336_ROUND288_NEW__9404_REFINED_R287_NEW__"
            "304740_FORMAL_NEW_OCCURRENCES"
        ),
        id_field="Round294_occurrence_registry_row_id",
        occurrence_field="registry_occurrence_id",
    )
    binding_ledger = ledger(
        rows=binding_rows,
        schema=BINDING_SCHEMA,
        status=(
            "FORMAL_46288_REPRESENTATION_BINDINGS__NO_OCCURRENCE_ID_ISSUED__"
            "NO_IDENTITY_COLLAPSE"
        ),
        id_field="Round294_occurrence_representation_binding_row_id",
    )

    result = {
        "schema": SCHEMA,
        "status": (
            "PASS_ROUND294_ATOMIC_STAGE_A_OCCURRENCE_REGISTRY_PROMOTION__"
            "431208_REGISTRY_ROWS__46288_REPRESENTATION_BINDINGS__"
            "304740_FORMAL_NEW_OCCURRENCES"
        ),
        "input_file_pins": dict(sorted(BYTE_PINS.items())),
        "sealed_overlap_contract": {
            "Round292_result_ledger_verification_manifest_all_byte_pinned":
                True,
            "Round292_manifest_binds_result_ledger_verification": True,
            "Round292_independent_verifier_status":
                overlap_verification["status"],
            "Round292_overlap_relation_count": 1_564,
            "Round292_refined_new_support_component_count": 9_404,
            "Round292_occupied_representation_subcover_count": 1_600,
            "Round292_remaining_unresolved_overlap_count": 0,
        },
        "consumed_frozen_inputs": {
            "Round266_complete_preserved_registry": True,
            "Round287_terminal_disposition": True,
            "Round288_canonical_atom_identity_gate": True,
            "Round290_isolated_atom_inner_support": True,
            "transitive_exact_byte_pins_enforced_by_inert_Round292_builder":
                True,
            "Round292_builder_imported_only_after_byte_pin_validation": True,
        },
        "census": {
            "formal_occurrence_registry_row_count": 431_208,
            "preserved_Round266_occurrence_count": 126_468,
            "formal_new_Round288_atom_occurrence_count": 295_336,
            "formal_new_refined_Round287_occurrence_count": 9_404,
            "formal_new_occurrence_count": 304_740,
            "formal_expanded_occurrence_count": 431_208,
            "formal_representation_binding_count": 46_288,
            "formal_occurrence_ID_issued_by_binding_rows": 0,
            "registry_entry_kind_histogram":
                dict(sorted(registry_histogram.items())),
            "representation_binding_kind_histogram":
                dict(sorted(binding_histogram.items())),
        },
        "scope_contract": {
            "registry_scope":
                "CURRENT_FORMAL_STAGE_A_OPEN_3D_PLUS_R287_REFINED_FRONTIER",
            "final_exhaustive_all_stratum_registry_claimed": False,
            "final_registry_count": None,
            "append_only_future_occurrence_extension_permitted": True,
            "known_lower_stratum_gap_frontier_R291": 576,
            "known_R289_incidence_refinement_frontier": 396,
            "scope_warning":
                "431,208 is not a final all-stratum census; unresolved "
                "lower-stratum work may append IDs but may not rewrite this "
                "closed Stage-A identity frontier",
        },
        "superseded_census_rejection": {
            "superseded_registry_row_count": 431_824,
            "superseded_direct_Round287_union_issuance_count": 10_020,
            "superseded_registry_row_count_accepted": False,
            "direct_Round287_union_issuance_accepted": False,
            "reason":
                "920 unions meet existing positive-volume occurrence support; "
                "only 9,404 exact uncovered connected refinements are issued",
        },
        "atomicity_contract": {
            "promotion_unit":
                "complete closed registry plus complete closed binding table",
            "partial_registry_promotion_permitted": False,
            "partial_binding_promotion_permitted": False,
            "preserved_IDs_rewritten": False,
            "Round288_reserved_IDs_rewritten": False,
            "Round292_refined_component_IDs_rewritten": False,
            "aliases_issue_new_IDs": False,
            "aliases_collapse_distinct_IDs": False,
        },
        "registry_ledger": summary(
            registry_ledger, DEFAULT_REGISTRY.name
        ),
        "representation_binding_ledger": summary(
            binding_ledger, DEFAULT_BINDINGS.name
        ),
        "formal_credit_transition": {
            "formal_new_expanded_occurrence_credit": 304_740,
            "formal_occurrence_alias_credit": 46_288,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_seam_edge_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "nonpromotion_freeze": {
            "legacy_pre_Round294_preserved_registry_quotient_components":
                63_224,
            "post_Round294_expanded_registry_component_DSU_status":
                "NOT_REBUILT",
            "post_Round294_quotient_component_count": None,
            "component_or_DSU_promotion": False,
            "seam_or_Jx_Jy_promotion": False,
            "post_Round294_maximality_status":
                "WAITING_EXPANDED_REGISTRY_DSU",
            "post_Round294_exact_key_fibre_status":
                "WAITING_EXPANDED_REGISTRY_DSU",
            "post_Round294_global_disposition_status":
                "WAITING_EXPANDED_REGISTRY_DSU",
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "provenance": {
            "producer_sha256": producer_sha256,
            "seed_affects_output": False,
            "old_candidate_artifacts_consumed": False,
            "old_candidate_producer_loaded_as_pinned_inert_reconstructor": True,
            "geometry_or_overlap_decision_reopened_by_Round294": False,
        },
        "required_next": [
            "Independently verify the complete Round294 ledgers cachelessly.",
            "Resolve the 576-entry Round291 lower-stratum gap frontier and "
            "the 396-entry Round289 incidence-refinement frontier; append "
            "occurrences only when independently proved.",
            "Rebuild component/DSU state over the expanded 431,208-row "
            "Stage-A registry before stating any post-Round294 quotient "
            "component count.",
            "Keep component/DSU/seam/maximality/fibre/disposition/Gate5/CM2 "
            "credits frozen until their own explicit promoting gates.",
        ],
    }
    return registry_ledger, binding_ledger, result


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
    parser.add_argument("--registry-ledger", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument(
        "--representation-binding-ledger",
        type=Path,
        default=DEFAULT_BINDINGS,
    )
    parser.add_argument("--result", type=Path, default=DEFAULT_RESULT)
    parser.add_argument("--seed", default="294071")
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()

    producer_sha256 = file_sha256(Path(__file__).resolve())
    registry, bindings, result = build(producer_sha256)
    registry_bytes = deterministic_gzip(registry)
    binding_bytes = deterministic_gzip(bindings)
    result["registry_ledger"]["file_sha256"] = hashlib.sha256(
        registry_bytes
    ).hexdigest()
    result["representation_binding_ledger"]["file_sha256"] = hashlib.sha256(
        binding_bytes
    ).hexdigest()
    result["seed_affects_output"] = False
    result["result_sha256"] = digest(result)
    result_bytes = canonical(result)
    if not arguments.no_write:
        safe_write(arguments.registry_ledger, registry_bytes)
        safe_write(arguments.representation_binding_ledger, binding_bytes)
        safe_write(arguments.result, result_bytes)
    print(json.dumps({
        "status": result["status"],
        "seed": arguments.seed,
        "seed_affects_output": False,
        "registry_ledger_file_sha256":
            result["registry_ledger"]["file_sha256"],
        "representation_binding_ledger_file_sha256":
            result["representation_binding_ledger"]["file_sha256"],
        "result_file_sha256": hashlib.sha256(result_bytes).hexdigest(),
        "result_sha256": result["result_sha256"],
        "census": result["census"],
    }, sort_keys=True))
    del registry, bindings, registry_bytes, binding_bytes
    gc.collect()


if __name__ == "__main__":
    main()
