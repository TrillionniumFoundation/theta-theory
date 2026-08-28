#!/usr/bin/env python3
"""Round133: fail-closed audit of the Round132-to-Round67 owner map.

The frozen chain contains a mathematical owner selector: within one
Round50 physical-event signature, retain the lexicographically least active
primitive representation.  It also declares a deterministic Borel map q_j
from an already-owned fixed-time record to the Round54 owner/root carrier.

Those statements do not by themselves assign any of the 64 materialized
Round132 occurrence source rows to the owned law.  This producer checks the
frozen Round50/54/58/60/61/67 contracts, audits every Round132 row, and emits
the smallest useful substitute: 64 canonical owner-candidate request rows.
They are explicitly not owner keys and not Omega_j records.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import tempfile
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PRODUCER = Path(__file__).resolve()
OUTPUT = (
    HERE
    / "cm2-round133-round132-owner-map-realizability-audit-2026-07-24.json"
)
SCHEMA = "cm2.round133.round132-owner-map-realizability-audit.v1"

R50P = HERE / "cm2_gate5_round50_owner_boundary_zb_f17_frontier_cert.py"
R50 = (
    HERE
    / "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json"
)
R54P = HERE / "cm2_gate5_round54_collar_pairing_directional_bv_frontier_cert.py"
R54 = (
    HERE
    / "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json"
)
R58P = HERE / "cm2_gate5_round58_owner_ledger_positive_transport_frontier_cert.py"
R58 = (
    HERE
    / "cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.json"
)
R60P = HERE / "cm2_gate5_round60_owner_trace_suffix_positive_anchor_frontier_cert.py"
R60 = (
    HERE
    / "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.json"
)
R61P = HERE / "cm2_gate5_round61_complement_rn_borel_orlicz_frontier_cert.py"
R61 = (
    HERE
    / "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.json"
)
R67P = (
    HERE
    / "cm2_round67_fixed_j_occurrence_owner_root_time_potential_frontier_cert.py"
)
R67 = (
    HERE
    / "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.json"
)
R132P = HERE / "cm2_round132_round28_occurrence_record_materialization.py"
R132 = (
    HERE
    / "cm2-round132-round28-occurrence-record-materialization-2026-07-24.json"
)

INPUTS = (R50P, R50, R54P, R54, R58P, R58, R60P, R60, R61P, R61, R67P, R67, R132P, R132)

BYTE_PINS = {
    R50P.name: "54238b6cae1d42a7cd0e58fe1e4fd21cbe92adf7dc8431d4c3f372c03a6dff77",
    R50.name: "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46",
    R54P.name: "137054d3f255e3a6292ce6eec4223d5111448f5538980915710dda59ce558048",
    R54.name: "87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5",
    R58P.name: "9d898bd753ecf61662ded5c75ffdb4387b7a4c582dc138d81b9fcf5cd4fd9a6e",
    R58.name: "27c5d2e9a6ac9ed8eeb3d42dc96aa1c0a8faa8e50e006811efea22b45c86b859",
    R60P.name: "b0e35d7d7a0d82fe655d772ecc3e0478070a987128d7f22d74158b0861c70efe",
    R60.name: "d519ad15a870fe7820839828347140e4bae3b5752a95fab4c18263c67e2ab778",
    R61P.name: "c3b3a3abdb61019d01b86aca0dbec34a94991bf8b174cd634aa5d90fbb039c31",
    R61.name: "59bce010748cccc1ffb829a9c232cab77185e6467433b3fed34988913649ae75",
    R67P.name: "cfb501aff4f321742e3fead9895c596e9105b2a89d064d917646b70c6f91ee8f",
    R67.name: "97cb410b9e960d8331a37ef9203b040c9b1d86c3ed3d1ba6ba66a28c4e4ff400",
    R132P.name: "88a12779148a49f111380c0560b0cb490a4e87f00d7ba7671878eec858f87d53",
    R132.name: "b5d09c7398dae4b77a6f011430286f88539e0f13ca449e50eb84fc3712d67d31",
}

SCHEMA_PINS = {
    R50.name: "cm2.gate5.round50-owner-boundary-zb-f17-frontier.v1.manifest.v1",
    R54.name: "cm2.gate5.round54-collar-pairing-directional-bv-frontier.v1.manifest.v1",
    R58.name: "cm2.gate5.round58-owner-ledger-positive-transport-frontier.v1.manifest.v1",
    R60.name: "cm2.gate5.round60-owner-trace-suffix-positive-anchor-frontier.v1.manifest.v1",
    R61.name: "cm2.gate5.round61-complement-rn-borel-orlicz-frontier.v1.manifest.v1",
    R67.name: "cm2.round67.fixed-j-occurrence-owner-root-time-potential.v1.manifest.v1",
    R132.name: "cm2.round132.round28-occurrence-record-materialization.v1",
}

RESULT_PINS = {
    R50.name: "939c047f04cbd91d4a468729c4abe932a6827487c4836a88a4021a7cd13b9831",
    R54.name: "0473dc4cec003b4038863eb42b57f515d8ddd9d6df9ebfb62aa18446919c1dc5",
    R58.name: "8900629d59bb7a36ec5bc80589900cdd5760569fc87ccd84130638ae9edfa992",
    R60.name: "a20f984e81141a8539b41707a5d742be9ff303297c0cca74fa29dfb85e0a631e",
    R61.name: "d621a93bce41bc26105f635a5c04bf5efbddfa5b297ea0863c043c259bad8a0f",
    R67.name: "c1fd3e486d671b83c6ae6a0c6da8c4d50bd2796842cfe1c8d8d5985001e5a57f",
    R132.name: "3a5b4450d838ac39e0e7f596344589b520a8060bb0131bd88fb8f2c77af4d624",
}

ROUND50_TOKEN_FIELDS = [
    "restriction-id",
    "time-j",
    "physical-event-signature",
    "primitive-key",
    "connected-rank-0",
    "side-label",
]


class VerificationError(RuntimeError):
    """Fail-closed input, semantic, reconstruction, or output error."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, child in pairs:
        require(key not in value, f"duplicate JSON key:{key}")
        value[key] = child
    return value


def reject_constant(token: str) -> None:
    raise VerificationError(f"non-finite JSON token:{token}")


def strict_json(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(len(raw) <= 16_000_000, f"oversized JSON:{path.name}")
    require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM:{path.name}")
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=strict_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise VerificationError(f"strict JSON:{path.name}") from exc
    require(isinstance(value, dict), f"top-level object:{path.name}")
    return value


def with_hash(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "row already closed")
    return {**row, "row_sha256": digest(row)}


def load_inputs() -> dict[str, dict[str, Any]]:
    documents: dict[str, dict[str, Any]] = {}
    for path in INPUTS:
        require(path.is_file(), f"missing input:{path.name}")
        require(not path.is_symlink(), f"symlink input:{path.name}")
        require(path.resolve().parent == HERE, f"input parent:{path.name}")
        require(sha256_path(path) == BYTE_PINS[path.name], f"byte pin:{path.name}")
        if path.suffix == ".json":
            document = strict_json(path)
            require(document.get("schema") == SCHEMA_PINS[path.name], f"schema:{path.name}")
            result = document.get("result")
            require(isinstance(result, dict), f"result object:{path.name}")
            require(digest(result) == RESULT_PINS[path.name], f"result pin:{path.name}")
            if path == R132:
                require(
                    document.get("result_sha256") == RESULT_PINS[path.name],
                    "Round132 outer result digest",
                )
            documents[path.name] = document
    return documents


def validate_frozen_contracts(documents: dict[str, dict[str, Any]]) -> None:
    r50 = documents[R50.name]["result"]["global_owner_aware_boundary_ZB_kernel"]
    require(
        r50["candidate_representation_token"]
        == "(restriction-id,time-j,physical-event-signature,primitive-key,connected-rank-0,side-label)",
        "Round50 candidate token",
    )
    require(
        r50["physical_event_signature"]
        == "(restriction-id,time-j,physical-face-kind,exact geometric event labels,side-label)",
        "Round50 physical-event signature",
    )
    require(
        r50["owner_rule"]
        == "within one physical-event signature, retain the lexicographically least active primitive key; E_i^owner=E_i minus union_(h<i)E_h",
        "Round50 owner selector",
    )
    require(
        r50["active_regular_root_section"]
        == "the Borel graph of the unique transverse rank-0 root on the parent W",
        "Round50 active root section",
    )
    require(r50["nonempty_component_coordinates_enumerated"] is False, "Round50 no coordinates")

    r54 = documents[R54.name]["result"]["recordwise_owner_collar_E_Tr"]
    require(
        r54["same_ID_label"]
        == "(restriction-id,time-j,physical-event-signature,primitive-key,connected-rank-0,side-label,word-cell)",
        "Round54 t54 token",
    )
    require(
        "measurable integer minima" in r54["canonical_Borel_selection"],
        "Round54 collar selector",
    )
    require(
        r54["all_physical_owner_records_stagewise_E_Tr_installed"] is False,
        "Round54 not all records",
    )
    require(
        r54["nu_mass_of_A_col_positive_or_full"] == "NOT_CERTIFIED",
        "Round54 coverage boundary",
    )

    r58 = documents[R58.name]["result"]
    require(
        "owner/root registry, A_col predicate, clearance d, dyadic K"
        in r58["frozen_chain_field_audit"]["positive_findings"],
        "Round58 abstract owner ledger",
    )
    require(
        r58["physical_same_owner_extended_clearance_ledger"]["coverage_not_certified"]
        == "nu(A_col^c)=0 is NOT_CERTIFIED",
        "Round58 coverage",
    )
    require(
        r58["root_density_kernelised_pullback_frontier"]["why_recordwise_Da_is_not_frozen"],
        "Round58 missing recordwise density",
    )

    r60 = documents[R60.name]["result"]["owner_root_crosswalk_and_coverage_frontier"]
    require(
        r60["Round50_to_Round54_same_ID_crosswalk"]
        == "CERTIFIED_EXACT_BOREL_PROJECTION",
        "Round60 token projection",
    )
    require(
        r60["Round25_to_Round50_exact_root_ID_crosswalk"] == "NOT_MATERIALIZED",
        "Round60 root-ID frontier",
    )
    require(
        r60["exact_projection"]
        == "pi_50(t54) drops only word-cell and equals t50; within a fixed word-cell the lift t50->t54 is injective",
        "Round60 exact projection",
    )

    r61 = documents[R61.name]["result"]["actual_owner_complement_RN_anchor"]
    require(
        r61["fixed_insertion_scope"].startswith(
            "fix j; take the disjoint marked source law m_j^own="
        ),
        "Round61 already-owned domain",
    )
    require(
        "apply the Borel root/collar map q_j retaining the full t54 token"
        in r61["actual_owner_law_construction"],
        "Round61 q_j declaration",
    )
    require(
        "q_j retains restriction/time/event/primitive/rank/side/word-cell"
        in r61["token_guard"],
        "Round61 retained fields",
    )

    r67 = documents[R67.name]["result"]
    fixed = r67["actual_fixed_j_subroot"]
    require(fixed["owner_view"] == "deterministic Borel q_j", "Round67 q_j")
    require(
        fixed["root"]
        == "Omega_j={(a,x):x in E_(j,a)^owner intersect R_(j,a)^reg}",
        "Round67 owner domain",
    )
    require(
        r67["minimal_spanning_registry"]["open_edges"][0]
        == "OWNER_TO_EXACT_RETURN_GRAPH_PATH_COMPONENT",
        "Round67 first open edge",
    )

    r132 = documents[R132.name]["result"]
    require(
        r132["count_ledger"]["Round28_rebuilt_occurrence_face_count"] == 64,
        "Round132 face count",
    )
    require(
        r132["count_ledger"]["Round67_owned_Omega_j_record_count"] == 0,
        "Round132 owner count",
    )
    require(r132["count_ledger"]["owner_key_count"] == 0, "Round132 owner keys")


def build_candidate_rows(r132: dict[str, Any]) -> list[dict[str, Any]]:
    source_rows = r132["occurrence_face_record_rows"]
    require(isinstance(source_rows, list) and len(source_rows) == 64, "64 source rows")
    require(
        r132["occurrence_face_record_rows_sha256"] == digest(source_rows),
        "Round132 source aggregate digest",
    )

    candidate_rows: list[dict[str, Any]] = []
    source_ids: set[str] = set()
    primitive_keys: set[str] = set()
    event_ids: set[str] = set()
    for source in source_rows:
        row_copy = dict(source)
        recorded = row_copy.pop("row_sha256", None)
        require(recorded == digest(row_copy), "Round132 source row closure")

        record_id = source["occurrence_record_id"]
        fields = source["canonical_Round67_source_field_values"]
        primitive = fields["primitive_key"]
        require(primitive == source["immutable_global_occurrence_face_seed_id"], "primitive join")
        require(fields["owner_key"] is None, "source owner null")
        require(source["Round67_owner_map_q_j_materialized"] is False, "q_j absent")
        require(source["Round67_owned_Omega_j_record"] is False, "not owned")
        require(fields["rank_zero_component"] is None, "rank component absent")
        require(source["source_side_missing_fields"] == ["return_component", "owner_key", "rank_zero_component"], "missing fields")
        require(fields["insertion_time"] == fields["collision_index"] == 1, "fixed time one")

        rebuilt = source["Round28_rebuilt_face_row"]
        maximal = source["maximal_occurrence_source_row"]
        expected_event = (
            "round132-occurrence-event-signature:"
            + digest(
                [
                    "round132-occurrence-event-signature-v1",
                    primitive,
                    maximal["global_physical_label"],
                    maximal["left_boundary"],
                    maximal["right_boundary"],
                    maximal["parameter_coarea_polarity"],
                ]
            )
        )
        require(fields["event_signature"] == expected_event, "Round132 event closure")
        require(
            rebuilt["physical_carrier_type"]
            == source["physical_carrier_type"]
            == "moving_first_event_grazing_occurrence_face",
            "moving occurrence carrier",
        )
        require(rebuilt["selected_all_scale_germ_exhausts_whole_maximal_row"] is False, "local germ only")

        request_payload = {
            "source_round132_occurrence_record_id": record_id,
            "source_round132_occurrence_row_sha256": recorded,
            "source_primitive_key": primitive,
            "source_occurrence_id": source["occurrence_id"],
        }
        candidate_rows.append(
            with_hash(
                {
                    "owner_candidate_request_id":
                        "round133-owner-candidate-request:"
                        + digest(["round133-owner-candidate-request-v1", request_payload]),
                    **request_payload,
                    "source_restriction_id": fields["restriction_id"],
                    "source_time_j": fields["insertion_time"],
                    "physical_face_kind": "moving_occurrence_face",
                    "source_round132_event_signature": fields["event_signature"],
                    "round132_event_signature_payload_contains_primitive_key": True,
                    "round132_event_signature_is_a_Round50_deduplication_signature": False,
                    "exact_source_event_labels": {
                        "global_physical_label": source["global_physical_label"],
                        "source": source["source"],
                        "tangent_target": source["tangent_target"],
                        "epsilon": source["epsilon"],
                        "miss_target": source["miss_target"],
                        "left_boundary": maximal["left_boundary"],
                        "right_boundary": maximal["right_boundary"],
                        "parameter_coarea_polarity": maximal["parameter_coarea_polarity"],
                    },
                    "source_oriented_hit_miss_side": fields["plaque_side"],
                    "Round50_minus_plus_side_label": None,
                    "Round50_restriction_id_crosswalk": None,
                    "Round50_physical_event_signature_excluding_primitive": None,
                    "Round50_parent_W_id": None,
                    "Round50_arbitrary_Rn_path_key": None,
                    "Round50_canonical_component_id": None,
                    "Round50_active_representation_E_i_membership": None,
                    "Round50_complete_same_event_candidate_fibre_digest": None,
                    "Round50_connected_rank_zero_component_id": None,
                    "Round50_unique_transverse_root_witness": None,
                    "Round54_word_cell_crosswalk": None,
                    "q_j_recordwise_output_formula_or_serialized_value": None,
                    "owner_key": None,
                    "certified_or_materialized_as_Round67_owned_Omega_j_record": False,
                    "actual_Round67_owned_membership":
                        "UNKNOWN_NOT_CERTIFIED",
                    "selector_application_status":
                        "UNRESOLVED_BEFORE_OWNER_MINIMIZATION",
                    "why_no_singleton_subset_promotion":
                        "uniqueness inside the 64 source rows does not prove completeness of the Round50 active-representation fibre",
                    "source_selected_germ_exhausts_whole_maximal_row": False,
                }
            )
        )
        require(record_id not in source_ids, "unique source record")
        require(primitive not in primitive_keys, "unique primitive")
        require(fields["event_signature"] not in event_ids, "unique Round132 event")
        source_ids.add(record_id)
        primitive_keys.add(primitive)
        event_ids.add(fields["event_signature"])

    candidate_rows.sort(key=lambda row: row["source_round132_occurrence_record_id"])
    require(
        len(candidate_rows) == len(source_ids) == len(primitive_keys) == len(event_ids) == 64,
        "64 unique candidate requests",
    )
    return candidate_rows


def build_blocker_rows() -> list[dict[str, Any]]:
    specifications = [
        (
            1,
            "ROUND132_TO_ROUND50_ACTIVE_REPRESENTATION_DOMAIN_CROSSWALK_ABSENT",
            "first missing data",
            [
                "parent-W id",
                "arbitrary-R_n path key",
                "canonical component id",
                "Round50 restriction-id crosswalk",
                "membership in E_i and R_i^reg",
            ],
            "without domain membership, q_j is not defined on a Round132 row",
        ),
        (
            2,
            "ROUND50_EVENT_FIBRE_AND_SIDE_NOT_MATERIALIZED",
            "selector input incomplete",
            [
                "physical-event signature excluding primitive-key",
                "Round50 minus/plus side-label",
                "complete active primitive fibre",
            ],
            "lexicographic minimum over the observed 64 rows is not the certified owner rule",
        ),
        (
            3,
            "CONNECTED_RANK_ZERO_ROOT_RECORD_ABSENT",
            "active root witness absent",
            [
                "connected rank-zero component id",
                "unique transverse root on the parent W",
                "regular-root witness",
            ],
            "a moving occurrence face seed is not automatically an active owner root",
        ),
        (
            4,
            "ROUND54_WORD_CELL_AND_SIDE_CROSSWALK_ABSENT",
            "t50-to-t54 lift incomplete",
            [
                "Round54 word-cell on the same owner fibre",
                "oriented side reconciliation",
            ],
            "Round132 occurrence word cells and hit/miss traces are not the frozen t54 fields",
        ),
        (
            5,
            "Q_J_RECORDWISE_SERIALIZATION_ABSENT",
            "owner-map output not materialized",
            [
                "canonical q_j output tuple",
                "canonical owner_key encoding",
                "endpoint/root value on the owned root",
            ],
            "the statement deterministic Borel q_j is not a row-generating formula",
        ),
    ]
    return [
        with_hash(
            {
                "blocker_order": order,
                "blocker_id": blocker_id,
                "classification": classification,
                "missing_values": values,
                "effect": effect,
            }
        )
        for order, blocker_id, classification, values, effect in specifications
    ]


def build_substitute_contract_rows() -> list[dict[str, Any]]:
    specifications = [
        ("source_round132_occurrence_record_id", True, "Round132"),
        ("source_round132_occurrence_row_sha256", True, "Round132"),
        ("Round50_restriction_id", False, "new exact crosswalk"),
        ("time_j", True, "Round132; value 1"),
        ("parent_W_id", False, "new active-root atlas"),
        ("arbitrary_Rn_path_key", False, "new active-root atlas"),
        ("canonical_component_id", False, "new active-root atlas"),
        ("physical_face_kind", True, "moving_occurrence_face"),
        ("physical_event_signature_excluding_primitive", False, "new owner fibre"),
        ("primitive_key", True, "Round132 face seed"),
        ("connected_rank_zero_component_id", False, "new root materialization"),
        ("Round50_minus_plus_side_label", False, "new side reconciliation"),
        ("active_E_i_and_regular_R_i_witness", False, "new predicate witness"),
        ("complete_same_event_candidate_fibre_digest", False, "new completeness proof"),
        ("Round54_word_cell", False, "new same-root word crosswalk"),
        ("owned_endpoint_root_coordinates", False, "new same-root coordinate record"),
        ("canonical_q_j_output", False, "new recordwise map encoding"),
    ]
    return [
        with_hash(
            {
                "field_index": index,
                "required_field": field,
                "currently_available": available,
                "source_or_requirement": source,
            }
        )
        for index, (field, available, source) in enumerate(specifications, start=1)
    ]


def build() -> dict[str, Any]:
    documents = load_inputs()
    validate_frozen_contracts(documents)
    r132 = documents[R132.name]["result"]

    candidate_rows = build_candidate_rows(r132)
    blocker_rows = build_blocker_rows()
    contract_rows = build_substitute_contract_rows()
    all_row_hashes = [
        *(row["row_sha256"] for row in candidate_rows),
        *(row["row_sha256"] for row in blocker_rows),
        *(row["row_sha256"] for row in contract_rows),
    ]
    require(len(all_row_hashes) == len(set(all_row_hashes)) == 86, "86 unique rows")

    return {
        "status":
            "CERTIFIED_OWNER_MAP_REALIZABILITY_AUDIT__0_MATERIALIZED_OWNED_RECORDS__FIRST_BLOCKER_ACTIVE_REPRESENTATION_CROSSWALK",
        "provenance": {
            "producer_sha256": sha256_path(PRODUCER),
            "input_byte_pins": {name: BYTE_PINS[name] for name in sorted(BYTE_PINS)},
            "input_schema_pins": {name: SCHEMA_PINS[name] for name in sorted(SCHEMA_PINS)},
            "input_result_pins": {name: RESULT_PINS[name] for name in sorted(RESULT_PINS)},
            "append_only": True,
        },
        "frozen_owner_selector_audit": {
            "Round50_owner_selector_formula_reconstructible": True,
            "formula":
                "within a complete physical-event fibre, retain the lexicographically least active primitive key; E_i^owner=E_i\\union_(h<i)E_h",
            "Round50_candidate_token_fields": list(ROUND50_TOKEN_FIELDS),
            "Round54_collar_length_selector_reconstructible_only_after_owned_root": True,
            "Round60_t50_to_t54_projection_reconstructible": True,
            "Round61_Round67_q_j_declared_deterministic_Borel": True,
            "q_j_recordwise_formula_or_serialized_output_present": False,
            "certified_applicable_to_any_Round132_row": False,
            "certified_applicable_nonempty_Round132_measurable_subset_exists": False,
            "actual_nonempty_owned_subset_existence":
                "UNKNOWN_NOT_CERTIFIED",
            "reason":
                "no Round132 row is crosswalked into the complete active regular Round50 representation fibre on a parent W",
        },
        "first_missing_object": {
            "object":
                "Round132-to-Round50 active-representation domain crosswalk",
            "must_precede":
                "lexicographic owner minimization and recordwise q_j evaluation",
            "why_first":
                "q_j has domain m_j^own; without E_i^owner intersect R_i^reg membership, assigning an owner output is ill-typed",
            "observed_64_rows_may_be_treated_as_complete_candidate_fibres": False,
            "observed_unique_Round132_event_ids_may_prove_unique_owner": False,
            "structural_reason":
                "the Round132 event hash contains primitive-key, so it separates rather than groups alternative primitive representations",
        },
        "owner_candidate_request_rows": candidate_rows,
        "owner_candidate_request_rows_sha256": digest(candidate_rows),
        "ordered_blocker_rows": blocker_rows,
        "ordered_blocker_rows_sha256": digest(blocker_rows),
        "minimum_replacement_contract_rows": contract_rows,
        "minimum_replacement_contract_rows_sha256": digest(contract_rows),
        "minimum_constructible_substitute": {
            "object":
                "64 closed owner-candidate request rows with exact Round132 provenance and null owner fields",
            "materialized_row_count": 64,
            "is_an_owner_registry": False,
            "is_a_q_j_graph": False,
            "may_be_used_as_owned_Omega_j_records": False,
            "next_legal_construction":
                "materialize the 17-field replacement contract, group by the primitive-free Round50 event signature, prove fibre completeness and E_i/R_i regular activity, select the least primitive, then encode q_j on the selected t54 root",
        },
        "count_ledger": {
            "Round132_occurrence_source_row_count": 64,
            "Round132_event_signatures_containing_primitive_key": 64,
            "owner_candidate_request_row_count": 64,
            "ordered_blocker_row_count": 5,
            "minimum_replacement_contract_field_count": 17,
            "finite_Round133_row_count": 86,
            "Round50_complete_candidate_fibre_count": 0,
            "Round50_active_regular_representation_crosswalk_count": 0,
            "Round50_connected_rank_zero_root_record_count": 0,
            "Round54_same_root_word_side_crosswalk_count": 0,
            "q_j_recordwise_output_count": 0,
            "owner_key_count": 0,
            "certified_or_materialized_Round67_owned_Omega_j_record_count": 0,
            "actual_Round67_owned_Omega_j_record_count":
                "UNKNOWN_NOT_CERTIFIED",
        },
        "global_safety": {
            "materialized_Round67_owned_record_count": 0,
            "actual_Round67_owned_record_count": "UNKNOWN_NOT_CERTIFIED",
            "Round67_to_path_typed_incidence_match_count": 0,
            "Round72_numeric_fields_promoted_to_Round67_root": False,
            "global_complete_18_field_block_count": 0,
            "complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "gate5_global_maturity": "10/18",
            "gate5_status": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict_nonclaims": [
            "no Round132 source row is asserted to lie in E_i^owner intersect R_i^reg",
            "no source record, occurrence ID or face label is paired to an owner by name",
            "the 64 observed primitives are not asserted to exhaust any Round50 event fibre",
            "a lexicographic minimum over the 64 observed source rows is forbidden",
            "Round132 hit/miss sides are not renamed Round50 minus/plus sides",
            "Round132 occurrence word cells are not renamed Round54 owner word cells",
            "no q_j owner key or Omega_j record is materialized",
            "no owner-to-return path, F10/F14/F15/F17/F18 block, Gate5 or CM2 upgrade",
        ],
    }


def safe_output_path(path: Path) -> Path:
    expanded = path.expanduser()
    protected = {PRODUCER, *(item.resolve() for item in INPUTS)}
    require(not expanded.is_symlink(), "output path must not be a symlink")
    if expanded.exists():
        metadata = expanded.lstat()
        require(stat.S_ISREG(metadata.st_mode), "existing output must be regular")
        require(metadata.st_nlink == 1, "existing output must not have hardlinks")
        for protected_path in protected:
            try:
                require(
                    not os.path.samefile(expanded, protected_path),
                    "output aliases protected input",
                )
            except FileNotFoundError:
                pass
    resolved = expanded.resolve()
    require(resolved not in protected, "output overwrites protected input")
    require(resolved.parent.is_dir(), "output parent directory")
    return resolved


def write_certificate(path: Path, result: dict[str, Any]) -> None:
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    payload = (
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.tmp-",
        dir=path.parent,
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        output = safe_output_path(args.output)
        result = build()
        write_certificate(output, result)
        print(
            canonical(
                {
                    "output": str(output),
                    "result_sha256": digest(result),
                    "status": result["status"],
                }
            )
        )
        return 0
    except (
        VerificationError,
        OSError,
        ValueError,
        KeyError,
        IndexError,
        TypeError,
        ArithmeticError,
    ) as exc:
        print(f"VerificationError: {exc}", file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
