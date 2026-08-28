#!/usr/bin/env python3
"""Independent verifier for the Round133 owner-map realizability audit.

This verifier never imports or executes the Round133 producer.  It pins the
frozen owner contracts and the Round132 source certificate, independently
rebuilds all 64 owner-candidate requests, five ordered blockers and the
17-field replacement contract, and keeps actual owner membership unknown.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
import tempfile
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = HERE / "cm2_round133_round132_owner_map_realizability_audit.py"
CERTIFICATE = (
    HERE
    / "cm2-round133-round132-owner-map-realizability-audit-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round133-round132-owner-map-realizability-audit-verification-2026-07-24.json"
)

CERTIFICATE_SCHEMA = "cm2.round133.round132-owner-map-realizability-audit.v1"
VERIFICATION_SCHEMA = (
    "cm2.round133.round132-owner-map-realizability-audit-verification.v1"
)
PRODUCER_SHA256 = (
    "3607bf2a3b2498c13d4bab27113dd151577e050cb83e68535ee32aaadbd79722"
)
CERTIFICATE_SHA256 = (
    "a020ce376c1398384e5f304aff320aa214721f5f8d8bcc1e35bfa31eadd54c91"
)
CERTIFICATE_RESULT_SHA256 = (
    "0e8e446fc81b1432dac31a9e7fc407b74bd6948dbd72451c67ffc43034f05ed2"
)

R50P = "cm2_gate5_round50_owner_boundary_zb_f17_frontier_cert.py"
R50 = "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json"
R54P = "cm2_gate5_round54_collar_pairing_directional_bv_frontier_cert.py"
R54 = "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json"
R58P = "cm2_gate5_round58_owner_ledger_positive_transport_frontier_cert.py"
R58 = "cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.json"
R60P = "cm2_gate5_round60_owner_trace_suffix_positive_anchor_frontier_cert.py"
R60 = "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.json"
R61P = "cm2_gate5_round61_complement_rn_borel_orlicz_frontier_cert.py"
R61 = "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.json"
R67P = "cm2_round67_fixed_j_occurrence_owner_root_time_potential_frontier_cert.py"
R67 = "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.json"
R132P = "cm2_round132_round28_occurrence_record_materialization.py"
R132 = "cm2-round132-round28-occurrence-record-materialization-2026-07-24.json"

INPUT_NAMES = (
    R50P,
    R50,
    R54P,
    R54,
    R58P,
    R58,
    R60P,
    R60,
    R61P,
    R61,
    R67P,
    R67,
    R132P,
    R132,
)

BYTE_PINS = {
    R50P: "54238b6cae1d42a7cd0e58fe1e4fd21cbe92adf7dc8431d4c3f372c03a6dff77",
    R50: "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46",
    R54P: "137054d3f255e3a6292ce6eec4223d5111448f5538980915710dda59ce558048",
    R54: "87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5",
    R58P: "9d898bd753ecf61662ded5c75ffdb4387b7a4c582dc138d81b9fcf5cd4fd9a6e",
    R58: "27c5d2e9a6ac9ed8eeb3d42dc96aa1c0a8faa8e50e006811efea22b45c86b859",
    R60P: "b0e35d7d7a0d82fe655d772ecc3e0478070a987128d7f22d74158b0861c70efe",
    R60: "d519ad15a870fe7820839828347140e4bae3b5752a95fab4c18263c67e2ab778",
    R61P: "c3b3a3abdb61019d01b86aca0dbec34a94991bf8b174cd634aa5d90fbb039c31",
    R61: "59bce010748cccc1ffb829a9c232cab77185e6467433b3fed34988913649ae75",
    R67P: "cfb501aff4f321742e3fead9895c596e9105b2a89d064d917646b70c6f91ee8f",
    R67: "97cb410b9e960d8331a37ef9203b040c9b1d86c3ed3d1ba6ba66a28c4e4ff400",
    R132P: "88a12779148a49f111380c0560b0cb490a4e87f00d7ba7671878eec858f87d53",
    R132: "b5d09c7398dae4b77a6f011430286f88539e0f13ca449e50eb84fc3712d67d31",
}

SCHEMA_PINS = {
    R50: "cm2.gate5.round50-owner-boundary-zb-f17-frontier.v1.manifest.v1",
    R54: "cm2.gate5.round54-collar-pairing-directional-bv-frontier.v1.manifest.v1",
    R58: "cm2.gate5.round58-owner-ledger-positive-transport-frontier.v1.manifest.v1",
    R60: "cm2.gate5.round60-owner-trace-suffix-positive-anchor-frontier.v1.manifest.v1",
    R61: "cm2.gate5.round61-complement-rn-borel-orlicz-frontier.v1.manifest.v1",
    R67: "cm2.round67.fixed-j-occurrence-owner-root-time-potential.v1.manifest.v1",
    R132: "cm2.round132.round28-occurrence-record-materialization.v1",
}

RESULT_PINS = {
    R50: "939c047f04cbd91d4a468729c4abe932a6827487c4836a88a4021a7cd13b9831",
    R54: "0473dc4cec003b4038863eb42b57f515d8ddd9d6df9ebfb62aa18446919c1dc5",
    R58: "8900629d59bb7a36ec5bc80589900cdd5760569fc87ccd84130638ae9edfa992",
    R60: "a20f984e81141a8539b41707a5d742be9ff303297c0cca74fa29dfb85e0a631e",
    R61: "d621a93bce41bc26105f635a5c04bf5efbddfa5b297ea0863c043c259bad8a0f",
    R67: "c1fd3e486d671b83c6ae6a0c6da8c4d50bd2796842cfe1c8d8d5985001e5a57f",
    R132: "3a5b4450d838ac39e0e7f596344589b520a8060bb0131bd88fb8f2c77af4d624",
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
    pass


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


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise VerificationError(f"non-finite JSON constant:{token}")


def strict_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    require(len(raw) <= 2_000_000, f"oversized JSON:{label}")
    require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM:{label}")
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=strict_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise VerificationError(f"strict JSON:{label}") from exc
    require(isinstance(value, dict), f"top-level object:{label}")
    return value


def strict_json_path(path: Path) -> dict[str, Any]:
    return strict_json_bytes(path.read_bytes(), path.name)


def closed_row(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "row already closed")
    return {**row, "row_sha256": digest(row)}


def load_inputs(check_files: bool = True) -> dict[str, dict[str, Any]]:
    documents: dict[str, dict[str, Any]] = {}
    for name in INPUT_NAMES:
        path = HERE / name
        if check_files:
            require(path.is_file(), f"missing input:{name}")
            require(not path.is_symlink(), f"symlink input:{name}")
            metadata = path.lstat()
            require(stat.S_ISREG(metadata.st_mode), f"regular input:{name}")
            require(metadata.st_nlink == 1, f"hardlinked input:{name}")
            require(sha256_path(path) == BYTE_PINS[name], f"byte pin:{name}")
        if name.endswith(".json"):
            document = strict_json_path(path)
            require(document.get("schema") == SCHEMA_PINS[name], f"schema:{name}")
            result = document.get("result")
            require(isinstance(result, dict), f"result object:{name}")
            require(digest(result) == RESULT_PINS[name], f"result pin:{name}")
            if name == R132:
                require(
                    document.get("result_sha256") == RESULT_PINS[name],
                    "Round132 outer result digest",
                )
            documents[name] = document
    return documents


def validate_contracts(documents: dict[str, dict[str, Any]]) -> None:
    r50 = documents[R50]["result"]["global_owner_aware_boundary_ZB_kernel"]
    require(
        r50["candidate_representation_token"]
        == "(restriction-id,time-j,physical-event-signature,primitive-key,connected-rank-0,side-label)",
        "Round50 candidate token",
    )
    require(
        r50["physical_event_signature"]
        == "(restriction-id,time-j,physical-face-kind,exact geometric event labels,side-label)",
        "Round50 primitive-free event signature",
    )
    require(
        r50["owner_rule"]
        == "within one physical-event signature, retain the lexicographically least active primitive key; E_i^owner=E_i minus union_(h<i)E_h",
        "Round50 owner selector",
    )
    require(
        r50["active_regular_root_section"]
        == "the Borel graph of the unique transverse rank-0 root on the parent W",
        "Round50 active root",
    )
    require(
        r50["nonempty_component_coordinates_enumerated"] is False,
        "Round50 coordinates absent",
    )

    r54 = documents[R54]["result"]["recordwise_owner_collar_E_Tr"]
    require(
        r54["same_ID_label"]
        == "(restriction-id,time-j,physical-event-signature,primitive-key,connected-rank-0,side-label,word-cell)",
        "Round54 token",
    )
    require(
        "measurable integer minima" in r54["canonical_Borel_selection"],
        "Round54 collar selector",
    )
    require(
        r54["all_physical_owner_records_stagewise_E_Tr_installed"] is False,
        "Round54 record frontier",
    )
    require(
        r54["nu_mass_of_A_col_positive_or_full"] == "NOT_CERTIFIED",
        "Round54 coverage frontier",
    )

    r58 = documents[R58]["result"]
    require(
        "owner/root registry, A_col predicate, clearance d, dyadic K"
        in r58["frozen_chain_field_audit"]["positive_findings"],
        "Round58 abstract ledger",
    )
    require(
        r58["physical_same_owner_extended_clearance_ledger"][
            "coverage_not_certified"
        ]
        == "nu(A_col^c)=0 is NOT_CERTIFIED",
        "Round58 coverage",
    )
    require(
        r58["root_density_kernelised_pullback_frontier"][
            "why_recordwise_Da_is_not_frozen"
        ],
        "Round58 recordwise density",
    )

    r60 = documents[R60]["result"]["owner_root_crosswalk_and_coverage_frontier"]
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
        "Round60 projection formula",
    )

    r61 = documents[R61]["result"]["actual_owner_complement_RN_anchor"]
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
        "Round61 retained keys",
    )

    r67 = documents[R67]["result"]
    fixed = r67["actual_fixed_j_subroot"]
    require(fixed["owner_view"] == "deterministic Borel q_j", "Round67 q_j")
    require(
        fixed["root"]
        == "Omega_j={(a,x):x in E_(j,a)^owner intersect R_(j,a)^reg}",
        "Round67 q_j domain",
    )
    require(
        r67["minimal_spanning_registry"]["open_edges"][0]
        == "OWNER_TO_EXACT_RETURN_GRAPH_PATH_COMPONENT",
        "Round67 first open edge",
    )

    r132 = documents[R132]["result"]
    require(
        r132["count_ledger"]["Round28_rebuilt_occurrence_face_count"] == 64,
        "Round132 source count",
    )
    require(
        r132["count_ledger"]["Round67_owned_Omega_j_record_count"] == 0,
        "Round132 materialized owner count",
    )
    require(r132["count_ledger"]["owner_key_count"] == 0, "Round132 owner keys")


def build_candidate_rows(r132: dict[str, Any]) -> list[dict[str, Any]]:
    source_rows = r132["occurrence_face_record_rows"]
    require(isinstance(source_rows, list) and len(source_rows) == 64, "64 sources")
    require(
        r132["occurrence_face_record_rows_sha256"] == digest(source_rows),
        "Round132 source digest",
    )
    rows: list[dict[str, Any]] = []
    source_ids: set[str] = set()
    primitive_keys: set[str] = set()
    event_ids: set[str] = set()
    for source in source_rows:
        source_copy = dict(source)
        recorded = source_copy.pop("row_sha256", None)
        require(recorded == digest(source_copy), "Round132 row closure")
        fields = source["canonical_Round67_source_field_values"]
        maximal = source["maximal_occurrence_source_row"]
        primitive = fields["primitive_key"]
        record_id = source["occurrence_record_id"]
        require(
            primitive == source["immutable_global_occurrence_face_seed_id"],
            "source primitive",
        )
        require(fields["owner_key"] is None, "source owner null")
        require(source["Round67_owner_map_q_j_materialized"] is False, "q_j absent")
        require(source["Round67_owned_Omega_j_record"] is False, "owner absent")
        require(fields["rank_zero_component"] is None, "rank absent")
        require(
            source["source_side_missing_fields"]
            == ["return_component", "owner_key", "rank_zero_component"],
            "source missing fields",
        )
        require(
            fields["insertion_time"] == fields["collision_index"] == 1,
            "fixed time",
        )
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
        require(fields["event_signature"] == expected_event, "event closure")
        rebuilt = source["Round28_rebuilt_face_row"]
        require(
            rebuilt["physical_carrier_type"]
            == source["physical_carrier_type"]
            == "moving_first_event_grazing_occurrence_face",
            "carrier type",
        )
        require(
            rebuilt["selected_all_scale_germ_exhausts_whole_maximal_row"] is False,
            "local germ only",
        )
        payload = {
            "source_round132_occurrence_record_id": record_id,
            "source_round132_occurrence_row_sha256": recorded,
            "source_primitive_key": primitive,
            "source_occurrence_id": source["occurrence_id"],
        }
        rows.append(
            closed_row(
                {
                    "owner_candidate_request_id":
                        "round133-owner-candidate-request:"
                        + digest(["round133-owner-candidate-request-v1", payload]),
                    **payload,
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
                        "parameter_coarea_polarity": maximal[
                            "parameter_coarea_polarity"
                        ],
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
                    "actual_Round67_owned_membership": "UNKNOWN_NOT_CERTIFIED",
                    "selector_application_status":
                        "UNRESOLVED_BEFORE_OWNER_MINIMIZATION",
                    "why_no_singleton_subset_promotion":
                        "uniqueness inside the 64 source rows does not prove completeness of the Round50 active-representation fibre",
                    "source_selected_germ_exhausts_whole_maximal_row": False,
                }
            )
        )
        require(record_id not in source_ids, "unique source ID")
        require(primitive not in primitive_keys, "unique primitive")
        require(fields["event_signature"] not in event_ids, "unique event")
        source_ids.add(record_id)
        primitive_keys.add(primitive)
        event_ids.add(fields["event_signature"])
    rows.sort(key=lambda row: row["source_round132_occurrence_record_id"])
    require(
        len(rows) == len(source_ids) == len(primitive_keys) == len(event_ids) == 64,
        "64 unique requests",
    )
    return rows


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
            ["Round54 word-cell on the same owner fibre", "oriented side reconciliation"],
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
        closed_row(
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


def build_contract_rows() -> list[dict[str, Any]]:
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
        closed_row(
            {
                "field_index": index,
                "required_field": field,
                "currently_available": available,
                "source_or_requirement": source,
            }
        )
        for index, (field, available, source) in enumerate(specifications, start=1)
    ]


def build_expected(check_files: bool = True) -> dict[str, Any]:
    if check_files:
        require(sha256_path(PRODUCER) == PRODUCER_SHA256, "producer pin")
    documents = load_inputs(check_files)
    validate_contracts(documents)
    candidates = build_candidate_rows(documents[R132]["result"])
    blockers = build_blocker_rows()
    contract = build_contract_rows()
    row_hashes = [
        *(row["row_sha256"] for row in candidates),
        *(row["row_sha256"] for row in blockers),
        *(row["row_sha256"] for row in contract),
    ]
    require(len(row_hashes) == len(set(row_hashes)) == 86, "86 unique rows")
    return {
        "status":
            "CERTIFIED_OWNER_MAP_REALIZABILITY_AUDIT__0_MATERIALIZED_OWNED_RECORDS__FIRST_BLOCKER_ACTIVE_REPRESENTATION_CROSSWALK",
        "provenance": {
            "producer_sha256": PRODUCER_SHA256,
            "input_byte_pins": {name: BYTE_PINS[name] for name in sorted(BYTE_PINS)},
            "input_schema_pins": {
                name: SCHEMA_PINS[name] for name in sorted(SCHEMA_PINS)
            },
            "input_result_pins": {
                name: RESULT_PINS[name] for name in sorted(RESULT_PINS)
            },
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
            "actual_nonempty_owned_subset_existence": "UNKNOWN_NOT_CERTIFIED",
            "reason":
                "no Round132 row is crosswalked into the complete active regular Round50 representation fibre on a parent W",
        },
        "first_missing_object": {
            "object": "Round132-to-Round50 active-representation domain crosswalk",
            "must_precede":
                "lexicographic owner minimization and recordwise q_j evaluation",
            "why_first":
                "q_j has domain m_j^own; without E_i^owner intersect R_i^reg membership, assigning an owner output is ill-typed",
            "observed_64_rows_may_be_treated_as_complete_candidate_fibres": False,
            "observed_unique_Round132_event_ids_may_prove_unique_owner": False,
            "structural_reason":
                "the Round132 event hash contains primitive-key, so it separates rather than groups alternative primitive representations",
        },
        "owner_candidate_request_rows": candidates,
        "owner_candidate_request_rows_sha256": digest(candidates),
        "ordered_blocker_rows": blockers,
        "ordered_blocker_rows_sha256": digest(blockers),
        "minimum_replacement_contract_rows": contract,
        "minimum_replacement_contract_rows_sha256": digest(contract),
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
            "actual_Round67_owned_Omega_j_record_count": "UNKNOWN_NOT_CERTIFIED",
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


def validate_row_closures(result: dict[str, Any]) -> None:
    groups = [
        ("owner_candidate_request_rows", 64),
        ("ordered_blocker_rows", 5),
        ("minimum_replacement_contract_rows", 17),
    ]
    row_hashes: list[str] = []
    for group, count in groups:
        rows = result.get(group)
        require(isinstance(rows, list) and len(rows) == count, f"group count:{group}")
        require(result.get(group + "_sha256") == digest(rows), f"group digest:{group}")
        for row in rows:
            require(isinstance(row, dict), f"row object:{group}")
            copy_row = dict(row)
            recorded = copy_row.pop("row_sha256", None)
            require(recorded == digest(copy_row), f"row closure:{group}")
            row_hashes.append(recorded)
    require(len(row_hashes) == len(set(row_hashes)) == 86, "86 row hashes")
    ledger = result["count_ledger"]
    require(ledger["finite_Round133_row_count"] == 86, "finite row count")
    require(ledger["owner_candidate_request_row_count"] == 64, "request count")
    require(ledger["ordered_blocker_row_count"] == 5, "blocker count")
    require(ledger["minimum_replacement_contract_field_count"] == 17, "contract count")
    require(
        ledger["certified_or_materialized_Round67_owned_Omega_j_record_count"]
        == 0,
        "materialized owner count",
    )
    require(
        ledger["actual_Round67_owned_Omega_j_record_count"]
        == "UNKNOWN_NOT_CERTIFIED",
        "actual owner unknown",
    )


def evaluate_document(document: dict[str, Any], expected: dict[str, Any]) -> None:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "closed certificate envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(isinstance(result, dict), "result object")
    require(document["result_sha256"] == digest(result), "outer result digest")
    validate_row_closures(result)
    require(result == expected, "independent expected result equality")
    require(
        document["result_sha256"] == CERTIFICATE_RESULT_SHA256,
        "frozen result digest",
    )


def resign(document: dict[str, Any]) -> None:
    document["result_sha256"] = digest(document["result"])


def reclose_row(result: dict[str, Any], group: str, index: int) -> None:
    row = result[group][index]
    row.pop("row_sha256", None)
    row["row_sha256"] = digest(row)
    result[group + "_sha256"] = digest(result[group])


def semantic_mutations(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    def simple(path: tuple[str, ...], value: Any) -> Callable[[dict[str, Any]], None]:
        def mutate(document: dict[str, Any]) -> None:
            target: Any = document
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            resign(document)
        return mutate

    def mutate_row(
        group: str,
        index: int,
        operation: Callable[[dict[str, Any]], None],
    ) -> Callable[[dict[str, Any]], None]:
        def mutate(document: dict[str, Any]) -> None:
            operation(document["result"][group][index])
            reclose_row(document["result"], group, index)
            resign(document)
        return mutate

    def trim_candidate(document: dict[str, Any]) -> None:
        result = document["result"]
        result["owner_candidate_request_rows"].pop()
        result["owner_candidate_request_rows_sha256"] = digest(
            result["owner_candidate_request_rows"]
        )
        result["count_ledger"]["owner_candidate_request_row_count"] = 63
        result["count_ledger"]["finite_Round133_row_count"] = 85
        result["minimum_constructible_substitute"]["materialized_row_count"] = 63
        resign(document)

    def delete_blocker(document: dict[str, Any]) -> None:
        result = document["result"]
        result["ordered_blocker_rows"].pop(0)
        result["ordered_blocker_rows_sha256"] = digest(result["ordered_blocker_rows"])
        result["count_ledger"]["ordered_blocker_row_count"] = 4
        result["count_ledger"]["finite_Round133_row_count"] = 85
        resign(document)

    def delete_contract_field(document: dict[str, Any]) -> None:
        result = document["result"]
        result["minimum_replacement_contract_rows"].pop()
        result["minimum_replacement_contract_rows_sha256"] = digest(
            result["minimum_replacement_contract_rows"]
        )
        result["count_ledger"]["minimum_replacement_contract_field_count"] = 16
        result["count_ledger"]["finite_Round133_row_count"] = 85
        resign(document)

    def fake_owner(kind: str) -> Callable[[dict[str, Any]], None]:
        def mutate(document: dict[str, Any]) -> None:
            result = document["result"]
            row = result["owner_candidate_request_rows"][0]
            if kind == "tangent":
                surrogate = row["exact_source_event_labels"]["tangent_target"]
            elif kind == "occurrence":
                surrogate = row["source_occurrence_id"]
            else:
                surrogate = "source-core:" + "0" * 64
            row["owner_key"] = surrogate
            row["q_j_recordwise_output_formula_or_serialized_value"] = surrogate
            row["certified_or_materialized_as_Round67_owned_Omega_j_record"] = True
            row["actual_Round67_owned_membership"] = "CERTIFIED_OWNED"
            row["selector_application_status"] = "SELECTED_WITHOUT_COMPLETE_FIBRE"
            reclose_row(result, "owner_candidate_request_rows", 0)
            result["count_ledger"]["owner_key_count"] = 1
            result["count_ledger"]["q_j_recordwise_output_count"] = 1
            result["count_ledger"][
                "certified_or_materialized_Round67_owned_Omega_j_record_count"
            ] = 1
            result["global_safety"]["materialized_Round67_owned_record_count"] = 1
            resign(document)
        return mutate

    mutations.extend(
        [
            (
                "certificate schema altered",
                lambda d: (d.__setitem__("schema", "bad"), resign(d)),
            ),
            (
                "producer pin altered",
                simple(("result", "provenance", "producer_sha256"), "0" * 64),
            ),
            (
                "Round132 pin altered",
                simple(("result", "provenance", "input_byte_pins", R132), "0" * 64),
            ),
            (
                "candidate row removed and counts re-signed",
                trim_candidate,
            ),
            (
                "first blocker removed and counts re-signed",
                delete_blocker,
            ),
            (
                "contract field removed and counts re-signed",
                delete_contract_field,
            ),
            (
                "actual subset changed from unknown to empty",
                simple(
                    (
                        "result",
                        "frozen_owner_selector_audit",
                        "actual_nonempty_owned_subset_existence",
                    ),
                    "CERTIFIED_EMPTY",
                ),
            ),
            (
                "actual owned count changed from unknown to zero",
                simple(
                    (
                        "result",
                        "count_ledger",
                        "actual_Round67_owned_Omega_j_record_count",
                    ),
                    0,
                ),
            ),
            (
                "global actual owner count changed from unknown to zero",
                simple(
                    (
                        "result",
                        "global_safety",
                        "actual_Round67_owned_record_count",
                    ),
                    0,
                ),
            ),
            (
                "tangent target spliced as owner",
                fake_owner("tangent"),
            ),
            (
                "source core spliced as owner",
                fake_owner("core"),
            ),
            (
                "occurrence ID spliced as owner",
                fake_owner("occurrence"),
            ),
            (
                "Round132 event renamed primitive-free signature",
                mutate_row(
                    "owner_candidate_request_rows",
                    0,
                    lambda row: row.__setitem__(
                        "round132_event_signature_is_a_Round50_deduplication_signature",
                        True,
                    ),
                ),
            ),
            (
                "hit side renamed plus side",
                mutate_row(
                    "owner_candidate_request_rows",
                    0,
                    lambda row: row.__setitem__("Round50_minus_plus_side_label", "plus"),
                ),
            ),
            (
                "occurrence word cell renamed Round54 word cell",
                mutate_row(
                    "owner_candidate_request_rows",
                    0,
                    lambda row: row.__setitem__(
                        "Round54_word_cell_crosswalk",
                        "round132-occurrence-word-cell:" + "0" * 64,
                    ),
                ),
            ),
            (
                "q_j formula fabricated",
                mutate_row(
                    "owner_candidate_request_rows",
                    0,
                    lambda row: row.__setitem__(
                        "q_j_recordwise_output_formula_or_serialized_value",
                        ["t54", "endpoint", "root"],
                    ),
                ),
            ),
            (
                "global match invented",
                simple(
                    (
                        "result",
                        "global_safety",
                        "Round67_to_path_typed_incidence_match_count",
                    ),
                    1,
                ),
            ),
            (
                "Round72 numeric fields promoted",
                simple(
                    (
                        "result",
                        "global_safety",
                        "Round72_numeric_fields_promoted_to_Round67_root",
                    ),
                    True,
                ),
            ),
            (
                "global complete block invented",
                simple(
                    (
                        "result",
                        "global_safety",
                        "global_complete_18_field_block_count",
                    ),
                    1,
                ),
            ),
            (
                "complete block invented",
                simple(
                    ("result", "global_safety", "complete_18_field_block_count"),
                    1,
                ),
            ),
            (
                "Gate5 block invented",
                simple(("result", "global_safety", "gate5_block_count"), 1),
            ),
            (
                "Gate5 maturity promoted",
                simple(("result", "global_safety", "gate5_global_maturity"), "18/18"),
            ),
            (
                "Gate5 promoted",
                simple(("result", "global_safety", "gate5_status"), "CERTIFIED"),
            ),
            (
                "CM2 promoted",
                simple(("result", "global_safety", "CM2"), "GO_FOR_CLAIM"),
            ),
            (
                "strict nonclaim removed",
                lambda d: (d["result"]["strict_nonclaims"].pop(), resign(d)),
            ),
            (
                "unknown result key added",
                lambda d: (d["result"].__setitem__("unknown", True), resign(d)),
            ),
        ]
    )

    for index in range(64):
        mutations.append(
            (
                f"candidate {index:02d} falsely selected as lexicographic minimum of observed 64",
                mutate_row(
                    "owner_candidate_request_rows",
                    index,
                    lambda row: (
                        row.__setitem__(
                            "selector_application_status",
                            "SELECTED_AS_MINIMUM_OF_OBSERVED_64",
                        ),
                        row.__setitem__(
                            "actual_Round67_owned_membership",
                            "CERTIFIED_OWNED",
                        ),
                    ),
                ),
            )
        )

    rejected: list[str] = []
    for label, mutation in mutations:
        candidate = copy.deepcopy(certificate)
        mutation(candidate)
        try:
            evaluate_document(candidate, expected)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected.append(label)
        else:
            raise VerificationError(f"semantic mutation accepted:{label}")
    return rejected


def strict_json_attacks(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    raw = canonical(certificate).encode("utf-8")
    status = (
        b'"status":"CERTIFIED_OWNER_MAP_REALIZABILITY_AUDIT__0_'
        b'MATERIALIZED_OWNED_RECORDS__FIRST_BLOCKER_ACTIVE_REPRESENTATION_CROSSWALK"'
    )
    attacks: list[tuple[str, bytes]] = [
        (
            "duplicate top-level schema key",
            raw.replace(b'{"result":', b'{"schema":"duplicate","result":', 1),
        ),
        (
            "duplicate nested status key",
            raw.replace(status, b'"status":"duplicate",' + status, 1),
        ),
        (
            "duplicate candidate owner key",
            raw.replace(
                b'"owner_key":null',
                b'"owner_key":"fake","owner_key":null',
                1,
            ),
        ),
        (
            "floating-point row count",
            raw.replace(
                b'"finite_Round133_row_count":86',
                b'"finite_Round133_row_count":86.0',
                1,
            ),
        ),
        (
            "NaN constant",
            raw.replace(
                b'"finite_Round133_row_count":86',
                b'"finite_Round133_row_count":NaN',
                1,
            ),
        ),
        (
            "positive Infinity",
            raw.replace(
                b'"finite_Round133_row_count":86',
                b'"finite_Round133_row_count":Infinity',
                1,
            ),
        ),
        (
            "negative Infinity",
            raw.replace(
                b'"finite_Round133_row_count":86',
                b'"finite_Round133_row_count":-Infinity',
                1,
            ),
        ),
        ("UTF-8 BOM", b"\xef\xbb\xbf" + raw),
        ("invalid UTF-8", raw[:-1] + b"\xff}"),
        ("top-level array", b"[]"),
        ("top-level null", b"null"),
        ("trailing second document", raw + b"{}"),
        (
            "leading-zero integer",
            raw.replace(
                b'"finite_Round133_row_count":86',
                b'"finite_Round133_row_count":086',
                1,
            ),
        ),
        (
            "negative zero",
            raw.replace(
                b'"finite_Round133_row_count":86',
                b'"finite_Round133_row_count":-0',
                1,
            ),
        ),
        (
            "unpaired surrogate",
            raw.replace(
                (
                    b'"schema":"cm2.round133.round132-owner-map-realizability-'
                    b'audit.v1"'
                ),
                b'"schema":"\\ud800"',
                1,
            ),
        ),
        ("oversized JSON", b'{"padding":"' + b"x" * 2_000_001 + b'"}'),
    ]
    extra_top = copy.deepcopy(certificate)
    extra_top["unknown"] = True
    attacks.append(("closed envelope extra key", canonical(extra_top).encode()))
    extra_result = copy.deepcopy(certificate)
    extra_result["result"]["unknown"] = True
    resign(extra_result)
    attacks.append(("closed result extra key", canonical(extra_result).encode()))
    stale = copy.deepcopy(certificate)
    stale["result"]["status"] = "tampered"
    attacks.append(("stale outer result digest", canonical(stale).encode()))

    rejected: list[str] = []
    for label, attack in attacks:
        try:
            document = strict_json_bytes(attack, label)
            evaluate_document(document, expected)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected.append(label)
        else:
            raise VerificationError(f"strict JSON attack accepted:{label}")
    return rejected


def build_verification(
    certificate: dict[str, Any],
    expected: dict[str, Any],
    mutations: list[str],
    attacks: list[str],
) -> dict[str, Any]:
    require(certificate["result"] == expected, "valid certificate equality")
    result = {
        "status": "PASS",
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
        "certificate_schema": CERTIFICATE_SCHEMA,
        "verifier_sha256": sha256_path(VERIFIER),
        "independence_contract": {
            "Round133_producer_imported": False,
            "Round133_producer_executed": False,
            "Round50_Round54_Round58_Round60_Round61_Round67_contracts_independently_checked": True,
            "Round132_event_hashes_independently_rebuilt": True,
            "all_86_Round133_rows_independently_reconstructed": True,
        },
        "replay_audit": {
            "Round132_occurrence_source_row_count": 64,
            "Round132_event_signatures_containing_primitive_key": 64,
            "owner_candidate_request_row_count": 64,
            "ordered_blocker_row_count": 5,
            "minimum_replacement_contract_field_count": 17,
            "finite_row_count": 86,
            "row_group_counts": [64, 5, 17],
            "all_row_and_aggregate_hashes_rebuilt": True,
            "certified_or_materialized_owned_record_count": 0,
            "actual_owned_subset_existence": "UNKNOWN_NOT_CERTIFIED",
            "q_j_recordwise_output_count": 0,
        },
        "semantic_mutation_test_count": len(mutations),
        "semantic_mutation_rejection_labels": mutations,
        "strict_json_attack_count": len(attacks),
        "strict_json_attack_rejection_labels": attacks,
        "determinism_contract": {
            "canonical_JSON_sort_keys": True,
            "no_hash_iteration_controls_output": True,
            "verification_replay_is_PYTHONHASHSEED_independent": True,
        },
        "safety": {
            "materialized_Round67_owned_record_count": 0,
            "actual_Round67_owned_record_count": "UNKNOWN_NOT_CERTIFIED",
            "Round67_to_path_typed_incidence_match_count": 0,
            "global_complete_18_field_block_count": 0,
            "complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "gate5_global_maturity": "10/18",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def safe_input_path(path: Path) -> Path:
    expanded = path.expanduser()
    require(expanded.exists(), "certificate missing")
    require(not expanded.is_symlink(), "certificate must not be a symlink")
    metadata = expanded.lstat()
    require(stat.S_ISREG(metadata.st_mode), "certificate must be regular")
    require(metadata.st_nlink == 1, "certificate must not have hardlinks")
    return expanded.resolve()


def safe_output_path(path: Path, certificate_path: Path) -> Path:
    expanded = path.expanduser()
    protected = {
        VERIFIER,
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        certificate_path.resolve(),
        *((HERE / name).resolve() for name in INPUT_NAMES),
    }
    require(not expanded.is_symlink(), "output must not be a symlink")
    if expanded.exists():
        metadata = expanded.lstat()
        require(stat.S_ISREG(metadata.st_mode), "existing output must be regular")
        require(metadata.st_nlink == 1, "existing output must not have hardlinks")
        for item in protected:
            try:
                require(
                    not os.path.samefile(expanded, item),
                    "output aliases protected input",
                )
            except FileNotFoundError:
                pass
    resolved = expanded.resolve()
    require(resolved not in protected, "output overwrites protected input")
    require(resolved.parent.is_dir(), "output parent directory")
    return resolved


def write_document(path: Path, document: dict[str, Any]) -> None:
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
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        certificate_path = safe_input_path(args.certificate)
        raw = certificate_path.read_bytes()
        require(sha256_bytes(raw) == CERTIFICATE_SHA256, "certificate byte pin")
        certificate = strict_json_bytes(raw, certificate_path.name)
        expected = build_expected(check_files=True)
        evaluate_document(certificate, expected)
        mutations = semantic_mutations(certificate, expected)
        attacks = strict_json_attacks(certificate, expected)
        verification = build_verification(certificate, expected, mutations, attacks)
        output = safe_output_path(args.output, certificate_path)
        write_document(output, verification)
        print(
            canonical(
                {
                    "output": str(output),
                    "semantic_mutations": len(mutations),
                    "status": "PASS",
                    "strict_json_attacks": len(attacks),
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
