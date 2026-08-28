#!/usr/bin/env python3
"""Round144: append-only Round137-v1 superseding migration schema.

This certificate freezes a new, explicitly versioned identifier domain rooted
in ``round137-dyadic-basis-enumeration-v1``.  It does not rewrite or alias the
unnamed Round27 enumeration and it does not mint any component, restriction,
owner, token, or output whose prerequisites are absent.

The result is deliberately fail-closed.  It records which R1648 fields can be
copied mechanically from frozen Round139/140/142 evidence, defines the exact
dependency DAG for the new identifier family, and leaves all downstream
identifiers null until their guards are independently certified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2-round144-round137-v1-superseding-migration-schema-2026-07-24.json"
)
SCHEMA = "cm2.round144.round137-v1-superseding-migration-schema.v1"


def dependency(name: str) -> Path:
    return HERE / name


ROUND27 = dependency(
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
)
ROUND35 = dependency(
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
)
ROUND137 = dependency(
    "cm2-round137-seed-independent-dyadic-basis-rank-contract-2026-07-24.json"
)
ROUND137_V = dependency(
    "cm2-round137-seed-independent-dyadic-basis-rank-contract-verification-2026-07-24.json"
)
ROUND140 = dependency(
    "cm2-round140-fixed-s-adaptive-component-identity-bridge-2026-07-24.json"
)
ROUND140_V = dependency(
    "cm2-round140-fixed-s-adaptive-component-identity-bridge-verification-2026-07-24.json"
)
ROUND140_W = dependency(
    "cm2-round140-round35-parent-w-r1648-materialization-audit-2026-07-24.json"
)
ROUND140_W_V = dependency(
    "cm2-round140-round35-parent-w-r1648-materialization-audit-verification-2026-07-24.json"
)
ROUND142 = dependency(
    "cm2-round142-historical-component-crosswalk-outer-atlas-frontier-2026-07-24.json"
)
ROUND142_V = dependency(
    "cm2-round142-historical-component-crosswalk-outer-atlas-frontier-verification-2026-07-24.json"
)
ROUND133 = dependency(
    "cm2-round133-round132-owner-map-realizability-audit-2026-07-24.json"
)
ROUND133_V = dependency(
    "cm2-round133-round132-owner-map-realizability-audit-verification-2026-07-24.json"
)
ROUND50 = dependency(
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json"
)
ROUND54 = dependency(
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json"
)
ROUND67 = dependency(
    "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.json"
)

PINS = {
    ROUND27.name: "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916",
    ROUND35.name: "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c",
    ROUND137.name: "06918b7bbfdeed9bda41a1220a25b630df6eaaa5f06024757f25a8c9fe7b88bf",
    ROUND137_V.name: "53369532c293d9cb2830a362facef7e4c4040f826f5ddea70519fde9034a1a5c",
    ROUND140.name: "e3f08525e770829c3ce71fed872a18dbfdc3139f514c3f865d12f6abc114a353",
    ROUND140_V.name: "75500f473e1932151bc643109187e99e88033c3b9457b584ecb1df4c0860b611",
    ROUND140_W.name: "bb6283e2fccba194b47f9aa174e85594560ba88062ed57d06651003744755a79",
    ROUND140_W_V.name: "b38306fb85e4a8a27d0339d95ff9e7ee3eabea044239972c719c926e0891782d",
    ROUND142.name: "816284789cc1249efd0ae9b9880e7d0434e8f74499c2616c6b64331997143ba0",
    ROUND142_V.name: "3e7abbe91af042cea229b998fba9c3829fe94120227102f98ecea620005db170",
    ROUND133.name: "a020ce376c1398384e5f304aff320aa214721f5f8d8bcc1e35bfa31eadd54c91",
    ROUND133_V.name: "f41a45baf3cffab63a3429b66c2f3c9473394024a4ae4c9a234df13e3410794f",
    ROUND50.name: "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46",
    ROUND54.name: "87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5",
    ROUND67.name: "97cb410b9e960d8331a37ef9203b040c9b1d86c3ed3d1ba6ba66a28c4e4ff400",
}

ENVELOPES = {
    ROUND137.name: (
        "cm2.round137.seed-independent-dyadic-basis-rank-contract.v1",
        "CERTIFIED_PROSPECTIVE_SEED_INDEPENDENT_DYADIC_BASIS_RANK_CONTRACT",
    ),
    ROUND137_V.name: (
        "cm2.round137.seed-independent-dyadic-basis-rank-contract-verification.v1",
        "PASS",
    ),
    ROUND140.name: (
        "cm2.round140.fixed-s-adaptive-component-identity-bridge.v1",
        "CERTIFIED_FIXED_S_ADAPTIVE_IDENTITY_STRICT_NONSUBSTITUTION",
    ),
    ROUND140_V.name: (
        "cm2.round140.fixed-s-adaptive-component-identity-bridge-verification.v1",
        "PASS",
    ),
    ROUND140_W.name: (
        "cm2.round140.round35-parent-w-r1648-materialization-audit.v1",
        "CERTIFIED_MAXIMAL_LEGAL_ROUND35_PARENT_W_DATA_FROM_R1648",
    ),
    ROUND140_W_V.name: (
        "cm2.round140.round35-parent-w-r1648-materialization-audit-verification.v1",
        "PASS",
    ),
    ROUND142.name: (
        "cm2.round142.historical-component-crosswalk-outer-atlas-frontier.v1",
        "CERTIFIED_HISTORICAL_ENUMERATION_UNDERDETERMINATION_AND_OUTER_ATLAS_FRONTIER",
    ),
    ROUND142_V.name: (
        "cm2.round142.historical-component-crosswalk-outer-atlas-frontier-verification.v1",
        "PASS",
    ),
    ROUND133.name: (
        "cm2.round133.round132-owner-map-realizability-audit.v1",
        "CERTIFIED_OWNER_MAP_REALIZABILITY_AUDIT__0_MATERIALIZED_OWNED_RECORDS__FIRST_BLOCKER_ACTIVE_REPRESENTATION_CROSSWALK",
    ),
    ROUND133_V.name: (
        "cm2.round133.round132-owner-map-realizability-audit-verification.v1",
        "PASS",
    ),
}

HISTORICAL_SCHEMAS = {
    ROUND27.name: "cm2.gate34.round27-arbitrary-n-path-schema.manifest.v1",
    ROUND35.name: "cm2.gate45.round35-arbitrary-rn-common-carrier.v1.manifest.v1",
    ROUND50.name: "cm2.gate5.round50-owner-boundary-zb-f17-frontier.v1.manifest.v1",
    ROUND54.name: "cm2.gate5.round54-collar-pairing-directional-bv-frontier.v1.manifest.v1",
    ROUND67.name: "cm2.round67.fixed-j-occurrence-owner-root-time-potential.v1.manifest.v1",
}

ENUMERATION_ID = "round137-dyadic-basis-enumeration-v1"
SOURCE_CORE_ID = (
    "core:90398e9ab632e57b027266bc7c34461a0a6a6d308c35fbeacc41432a3d7f48f7"
)
PATH_SHA256 = "5cec1061ec331e8f37929dfb1b2b2a78757309ba60198d571abd9e8cf6c70ed9"
ADAPTIVE_ID = (
    "round140-fixed-s0-adaptive-path-cell:"
    "a4a3be3cf7115abec08f372382ca7a863838e963a7d03af400d6a6ca58812b6a"
)
COMPONENT_LOCATOR = (
    "round140-unique-containing-maximal-component-locator:"
    "028dd77208582e33185707e1ea1ca31988e3cf4f698674fb8a0f791981dce90b"
)


class CertificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise CertificationError(label)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_constant(token: str) -> None:
    raise CertificationError(f"non-finite JSON token:{token}")


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def strict_json(path: Path) -> dict[str, Any]:
    metadata = path.lstat()
    require(
        stat.S_ISREG(metadata.st_mode)
        and metadata.st_nlink == 1
        and not path.is_symlink(),
        f"unsafe dependency:{path.name}",
    )
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=reject_constant,
    )
    require(isinstance(value, dict), f"object dependency:{path.name}")
    return value


def with_hash(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["row_sha256"] = digest(row)
    return result


def load_dependencies() -> dict[str, dict[str, Any]]:
    values: dict[str, dict[str, Any]] = {}
    for name, expected in sorted(PINS.items()):
        path = HERE / name
        require(path.exists(), f"missing dependency:{name}")
        require(sha256(path) == expected, f"dependency pin:{name}")
        values[name] = strict_json(path)
    for name, (schema, status) in ENVELOPES.items():
        value = values[name]
        require(set(value) == {"schema", "result", "result_sha256"}, f"envelope keys:{name}")
        require(value["schema"] == schema, f"schema:{name}")
        require(value["result_sha256"] == digest(value["result"]), f"result digest:{name}")
        require(value["result"]["status"] == status, f"status:{name}")
    for name, schema in HISTORICAL_SCHEMAS.items():
        require(values[name]["schema"] == schema, f"historical schema:{name}")
    return values


def namespace_rows() -> list[dict[str, Any]]:
    specifications = [
        {
            "object_type": "component",
            "prefix": "c24v1-component",
            "ordered_payload_fields": [
                "source_core_id",
                "return_depth_n",
                "path_tuple_sha256",
                "basis_enumeration_id",
                "least_2d_basis_rank_decimal",
            ],
            "direct_prerequisites": [
                "complete_2D_maximal_component_outer_atlas",
                "exhausted_physical_event_frontier",
                "positive_contained_basis_witness",
                "least_rank_negative_oracle_for_all_earlier_v1_rows",
            ],
        },
        {
            "object_type": "parent_W",
            "prefix": "rn-v1-parent-W",
            "ordered_payload_fields": [
                "component_v1_id",
                "fixed_s",
                "exact_b_descriptor",
                "source_interval_v1_rank",
                "incidence_rank_path_sha256",
                "short_cell_k",
            ],
            "direct_prerequisites": [
                "component_v1_id",
                "certified_full_leaf_interval",
                "least_1d_source_interval_v1_rank",
                "natural_short_cell_index",
            ],
        },
        {
            "object_type": "restriction",
            "prefix": "rn-v1-restriction",
            "ordered_payload_fields": [
                "component_v1_id",
                "parent_W_v1_id",
                "image_recut_v1_rank",
            ],
            "direct_prerequisites": [
                "component_v1_id",
                "parent_W_v1_id",
                "certified_image_recut_v1_rank",
            ],
        },
        {
            "object_type": "owner",
            "prefix": "round50-v1-owner",
            "ordered_payload_fields": [
                "restriction_v1_id",
                "time_j",
                "physical_event_signature_excluding_primitive",
                "primitive_key",
                "connected_rank_zero_component_id",
                "side_label",
                "complete_same_event_candidate_fibre_digest",
            ],
            "direct_prerequisites": [
                "restriction_v1_id",
                "Round132_to_Round50_active_representation_domain_crosswalk",
                "complete_active_regular_same_event_fibre",
                "lexicographically_least_active_primitive_proof",
            ],
        },
        {
            "object_type": "token",
            "prefix": "round54-v1-t54",
            "ordered_payload_fields": [
                "owner_v1_id",
                "round54_word_cell",
                "minus_plus_side_label",
                "owned_endpoint_root_coordinates_sha256",
                "collar_length_selector_payload_sha256",
            ],
            "direct_prerequisites": [
                "owner_v1_id",
                "same_root_Round54_word_and_side_crosswalk",
                "owned_endpoint_root_coordinates",
                "recordwise_t54_serialization",
            ],
        },
        {
            "object_type": "output",
            "prefix": "round67-v1-qj",
            "ordered_payload_fields": [
                "token_v1_id",
                "time_j",
                "owner_key_sha256",
                "q_j_record_payload_sha256",
            ],
            "direct_prerequisites": [
                "token_v1_id",
                "typed_Omega_j_owner_root_record",
                "recordwise_q_j_formula_and_serialized_output",
            ],
        },
    ]
    rows = []
    for index, spec in enumerate(specifications, start=1):
        row = {
            "namespace_index": index,
            "namespace_version": "round144-round137-v1",
            "identifier_serialization": (
                "prefix + ':' + sha256(canonical_JSON_array(["
                "namespace_version,ordered_payload_values]))"
            ),
            "null_propagation": (
                "if any direct prerequisite or ordered payload field is absent, "
                "the identifier is null and MUST NOT be minted"
            ),
            **spec,
        }
        rows.append(with_hash(row))
    return rows


def dag_rows() -> list[dict[str, Any]]:
    raw = [
        ("D00", "adopt_round137_v1_enumeration", [], "READY", None),
        ("D01", "pin_R1648_seed_path_payload", ["D00"], "READY", None),
        (
            "D02",
            "complete_2D_centered_jet_outer_atlas",
            ["D01"],
            "BLOCKED",
            "complete validated two-generator centered-jet outer atlas with exhausted event frontier",
        ),
        (
            "D03",
            "prove_least_2d_v1_rank_negative_oracle",
            ["D02"],
            "BLOCKED",
            "exclude every earlier Round137-v1 basis row from closure containment in the maximal component",
        ),
        ("D04", "mint_component_v1_id", ["D03"], "BLOCKED", "D02 then D03"),
        (
            "D05",
            "certify_full_leaf_endpoint_interval",
            ["D01"],
            "AWAITING_FUTURE_CERTIFICATE",
            "an accepted Round141/143-class exact leaf endpoint certificate",
        ),
        (
            "D06",
            "prove_least_1d_source_interval_v1_rank_and_short_cell",
            ["D05"],
            "BLOCKED",
            "full leaf interval plus exact Round137-v1 1D leastness and natural short-cell rule",
        ),
        ("D07", "mint_parent_W_v1_id", ["D04", "D06"], "BLOCKED", "D04 and D06"),
        (
            "D08",
            "certify_image_recut_v1_rank",
            ["D05"],
            "AWAITING_FUTURE_CERTIFICATE",
            "exact image interval, coordinate normalization, endpoint ownership and v1 leastness",
        ),
        ("D09", "mint_restriction_v1_id", ["D04", "D07", "D08"], "BLOCKED", "D04, D07 and D08"),
        (
            "D10",
            "materialize_Round132_to_Round50_active_representation_crosswalk",
            ["D09"],
            "BLOCKED",
            "the 17-field replacement contract and complete active regular representation fibres",
        ),
        ("D11", "mint_owner_v1_id", ["D10"], "BLOCKED", "D10"),
        (
            "D12",
            "mint_t54_v1_token",
            ["D11"],
            "BLOCKED",
            "D11 plus same-root Round54 word/side/endpoint crosswalk",
        ),
        (
            "D13",
            "mint_qj_v1_output",
            ["D12"],
            "BLOCKED",
            "D12 plus typed Omega_j record and recordwise q_j serialization",
        ),
    ]
    return [
        with_hash(
            {
                "node_id": node,
                "operation": operation,
                "depends_on": deps,
                "status": status,
                "first_local_blocker": blocker,
            }
        )
        for node, operation, deps, status, blocker in raw
    ]


def build() -> dict[str, Any]:
    values = load_dependencies()
    r27 = values[ROUND27.name]["result"]
    r35 = values[ROUND35.name]["result"]
    r137 = values[ROUND137.name]["result"]
    r140 = values[ROUND140.name]["result"]
    r140w = values[ROUND140_W.name]["result"]
    r142 = values[ROUND142.name]["result"]
    r133 = values[ROUND133.name]["result"]

    enumeration = r137["dyadic_basis_enumeration_v1"]
    require(enumeration["contract_id"] == ENUMERATION_ID, "enumeration id")
    require(enumeration["index_origin"] == "zero_based", "enumeration origin")
    require(
        r27["canonical_regular_connected_component_schema"]["canonical_component_id"]
        == "c24-component:(source_core_id,n,path_key,least_dyadic_basis_index)",
        "Round27 component schema",
    )
    require(
        r35["arbitrary_Rn_parent_W_Borel_registry"]["component_id_schema"]
        == "c24-component:(source-core-id,n,path-key,least-dyadic-basis-index)",
        "Round35 component schema",
    )
    adaptive = r140["fixed_s_adaptive_path_cell"]
    bridge = r140["unique_containing_maximal_component_bridge"]
    path = r140w["materialized_source_core_path_tuple"]
    leaf = r140w["fixed_parameter_and_exact_implicit_leaf"]
    incidence = r140w["incidence_rank_and_density_mesh"]
    rank2 = r140w["Round137_v1_contained_2d_basis_rank"]
    rank1 = r140w["Round137_v1_contained_1d_leaf_rank"]
    atlas = r142["centered_jet_outer_atlas_frontier"]
    ambiguity = r142["two_enumeration_model_underdetermination_proof"]

    require(path["source_core_id"] == SOURCE_CORE_ID, "source core")
    require(path["return_depth"] == 1648, "return depth")
    require(path["payload_sha256"] == PATH_SHA256, "path tuple")
    require(adaptive["adaptive_path_cell_id"] == ADAPTIVE_ID, "adaptive id")
    require(adaptive["Round27_path_tuple_sha256"] == PATH_SHA256, "adaptive path")
    require(
        bridge["unique_containing_component_locator_id"] == COMPONENT_LOCATOR,
        "component locator",
    )
    require(atlas["target_component_locator"] == COMPONENT_LOCATOR, "atlas target")
    require(atlas["complete_2D_centered_jet_cell_count"] == 0, "atlas empty")
    require(not atlas["maximal_component_U_boundary_exhausted"], "frontier open")
    require(not ambiguity["historical_numeric_rank_identified_by_frozen_artifacts"], "historical rank absent")
    require(not ambiguity["historical_c24_component_ID_identified_by_frozen_artifacts"], "historical id absent")
    require(r133["first_missing_object"]["object"] == "Round132-to-Round50 active-representation domain crosswalk", "owner blocker")
    replacement = r133["minimum_replacement_contract_rows"]
    require(len(replacement) == 17, "replacement field count")

    namespaces = namespace_rows()
    dag = dag_rows()
    namespace_prefixes = [row["prefix"] for row in namespaces]
    require(len(namespace_prefixes) == len(set(namespace_prefixes)), "namespace disjointness")
    require("c24-component" not in namespace_prefixes, "historical prefix collision")
    require("rn-restriction" not in namespace_prefixes, "historical restriction collision")

    mechanically_migratable = [
        with_hash({"field": "basis_enumeration_id", "value": ENUMERATION_ID, "source": ROUND137.name}),
        with_hash({"field": "basis_index_origin", "value": "zero_based", "source": ROUND137.name}),
        with_hash({"field": "source_core_id", "value": SOURCE_CORE_ID, "source": ROUND140_W.name}),
        with_hash({"field": "return_depth_n", "value": 1648, "source": ROUND140_W.name}),
        with_hash({"field": "path_tuple_sha256", "value": PATH_SHA256, "source": ROUND140_W.name}),
        with_hash({"field": "official_word_count", "value": path["official_word_key_occurrence_count"], "source": ROUND140_W.name}),
        with_hash({"field": "official_word_sequence_sha256", "value": path["official_word_key_sequence_sha256"], "source": ROUND140_W.name}),
        with_hash({"field": "unique_official_word_count", "value": path["unique_official_word_key_count"], "source": ROUND140_W.name}),
        with_hash({"field": "fixed_s", "value": leaf["s"], "source": ROUND140_W.name}),
        with_hash({"field": "exact_b_descriptor", "value": leaf["exact_b_star_descriptor"], "source": ROUND140_W.name}),
        with_hash({"field": "incidence_rank_path_sha256", "value": incidence["incidence_rank_path_sha256"], "source": ROUND140_W.name}),
        with_hash({"field": "incidence_rank_path_RLE", "value": incidence["incidence_rank_path_run_length_encoding"], "source": ROUND140_W.name}),
        with_hash({"field": "delta_14", "value": incidence["delta_14"], "source": ROUND140_W.name}),
        with_hash({"field": "adaptive_seed_cell_id", "value": ADAPTIVE_ID, "source": ROUND140.name}),
        with_hash({"field": "set_theoretic_component_locator", "value": COMPONENT_LOCATOR, "source": ROUND140.name}),
        with_hash({
            "field": "contained_2d_basis_upper_bound",
            "value": {
                "level": rank2["contained_primitive_basis_row"][0],
                "row_sha256": digest(rank2["contained_primitive_basis_row"]),
                "rank_bit_length": rank2["contained_primitive_basis_rank"]["bit_length"],
                "rank_decimal_digit_count": rank2["contained_primitive_basis_rank"]["decimal_digit_count"],
                "rank_decimal_sha256": rank2["contained_primitive_basis_rank"]["sha256_of_decimal"],
                "is_least_component_rank": False,
            },
            "source": ROUND140_W.name,
        }),
        with_hash({
            "field": "contained_1d_leaf_basis_upper_bound",
            "value": {
                "level": rank1["contained_primitive_basis_row"][0],
                "row_sha256": digest(rank1["contained_primitive_basis_row"]),
                "rank_bit_length": rank1["contained_primitive_basis_rank"]["bit_length"],
                "rank_decimal_digit_count": rank1["contained_primitive_basis_rank"]["decimal_digit_count"],
                "rank_decimal_sha256": rank1["contained_primitive_basis_rank"]["sha256_of_decimal"],
                "is_full_leaf_interval_rank": False,
            },
            "source": ROUND140_W.name,
        }),
        with_hash({
            "field": "historical_enumeration_underdetermination_proof_id",
            "value": ambiguity["ambiguity_proof_id"],
            "source": ROUND142.name,
        }),
    ]

    unavailable = [
        ("least_2d_basis_rank_of_maximal_component", "D02,D03"),
        ("component_v1_id", "D04"),
        ("least_1d_source_interval_v1_rank", "D05,D06"),
        ("natural_short_cell_k", "D05,D06"),
        ("parent_W_v1_id", "D07"),
        ("image_recut_v1_rank", "D08"),
        ("restriction_v1_id", "D09"),
        ("Round50_active_representation_crosswalk", "D10"),
        ("owner_v1_id", "D11"),
        ("t54_v1_token", "D12"),
        ("Omega_j_record", "D13"),
        ("q_j_v1_output", "D13"),
    ]
    unavailable_rows = [
        with_hash({"field": field, "value": None, "blocked_by": blocker})
        for field, blocker in unavailable
    ]

    future_acceptance = with_hash({
        "allowed_future_sources": [
            "a formally pinned centered-affine collar certificate",
            "a formally pinned exact leaf-endpoint/image-recut certificate",
            "a formally pinned complete two-generator outer-atlas certificate",
        ],
        "acceptance_guards": [
            "the source and independent verification bytes are SHA256-pinned",
            "the certificate envelope is canonical and its verification status is PASS",
            "the source explicitly targets the same source_core_id, R1648 path tuple and component locator",
            "the source uses round137-dyadic-basis-enumeration-v1 prospectively",
            "the source does not alias any v1 identifier to a Round27/35/50/54/67 historical identifier",
            "only DAG nodes whose complete direct prerequisites are certified may change from null",
        ],
        "centered_collar_alone_closes_D02": False,
        "leaf_endpoint_certificate_alone_closes_D04": False,
        "leaf_endpoint_certificate_may_fill_after_verification": [
            "D05",
            "D06",
            "D08",
        ],
        "outer_atlas_and_negative_oracle_may_fill_after_verification": [
            "D02",
            "D03",
            "D04",
        ],
    })

    registry_payload = [
        "round144-round137-v1-superseding-migration-schema",
        ENUMERATION_ID,
        [row["row_sha256"] for row in namespaces],
        [row["row_sha256"] for row in dag],
        digest(mechanically_migratable),
        digest(unavailable_rows),
    ]
    result = {
        "status": "CERTIFIED_VERSIONED_SUPERSEDING_MIGRATION_SCHEMA__NO_CORRECTED_COMPONENT_MINTED",
        "provenance": {
            "dependency_sha256": dict(sorted(PINS.items())),
            "append_only": True,
            "old_round_files_modified": False,
            "historical_identifier_rewrite_or_alias_count": 0,
        },
        "adoption_contract": with_hash({
            "adopted_enumeration_id": ENUMERATION_ID,
            "adoption_scope": "prospective superseding namespace only",
            "index_origin": enumeration["index_origin"],
            "two_dimensional_row_schema": enumeration["two_dimensional"]["row_schema"],
            "one_dimensional_row_schema": enumeration["one_dimensional"]["row_schema"],
            "historical_Round27_enumeration_recovered": False,
            "historical_Round27_bytes_reinterpreted": False,
            "migration_semantics": "new identifiers coexist with and never impersonate historical identifiers",
            "fail_closed": True,
        }),
        "identifier_namespace_rows": namespaces,
        "identifier_namespace_rows_sha256": digest(namespaces),
        "migration_DAG_rows": dag,
        "migration_DAG_rows_sha256": digest(dag),
        "mechanically_migratable_field_rows": mechanically_migratable,
        "mechanically_migratable_field_rows_sha256": digest(mechanically_migratable),
        "currently_unavailable_field_rows": unavailable_rows,
        "currently_unavailable_field_rows_sha256": digest(unavailable_rows),
        "future_certificate_acceptance_contract": future_acceptance,
        "first_exact_blocker": with_hash({
            "node_id": "D02",
            "object": atlas["first_missing_geometric_oracle_after_prospective_v1_adoption"],
            "why_first": (
                "the known adaptive cell and contained basis row give only a positive upper bound; "
                "without a maximal-component outer atlas no complete earlier-rank exclusion query is valid"
            ),
            "next_after_D02": "D03 least-rank negative oracle",
            "corrected_component_id": None,
        }),
        "owner_chain_contract": with_hash({
            "Round133_first_missing_object": r133["first_missing_object"]["object"],
            "replacement_field_count": len(replacement),
            "replacement_required_fields": [row["required_field"] for row in replacement],
            "replacement_rows_sha256": r133["minimum_replacement_contract_rows_sha256"],
            "owner_selector_formula": r133["frozen_owner_selector_audit"]["formula"],
            "may_select_owner_from_observed_64_rows": False,
            "component_and_restriction_v1_ids_must_precede_owner_crosswalk": True,
        }),
        "current_identifier_values": {
            "component_v1_id": None,
            "parent_W_v1_id": None,
            "restriction_v1_id": None,
            "owner_v1_id": None,
            "t54_v1_token": None,
            "Omega_j_v1_record": None,
            "q_j_v1_output": None,
        },
        "migration_registry_id": (
            "round144-round137-v1-migration-registry:" + digest(registry_payload)
        ),
        "strict_nonpromotion": {
            "new_historical_Round27_component_rank_count": 0,
            "new_historical_Round27_c24_component_ID_count": 0,
            "new_versioned_component_ID_count": 0,
            "new_versioned_parent_W_ID_count": 0,
            "new_versioned_restriction_ID_count": 0,
            "new_versioned_owner_ID_count": 0,
            "new_versioned_t54_token_count": 0,
            "new_versioned_Omega_j_record_count": 0,
            "new_versioned_q_j_output_count": 0,
            "global_complete_18_field_block_count": 0,
            "global_gate5_maturity": "10/18",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict_nonclaims": [
            "Round137-v1 is not the unnamed historical Round27 enumeration",
            "the versioned namespace does not rewrite Round27/35/50/54/67 identifiers",
            "the adaptive seed cell is not the maximal regular component",
            "a contained basis row is not the least component rank",
            "a centered collar is not a complete two-dimensional outer atlas",
            "no corrected component identifier is minted before D02 and D03",
            "no parent-W or restriction is minted from partial leaf data",
            "no owner is selected from an incomplete observed candidate fibre",
            "no t54, Omega_j or q_j output is materialized",
            "no Gate5 field, block, or CM2 theorem is promoted",
        ],
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def protected_paths() -> set[Path]:
    return {Path(__file__).resolve(), *((HERE / name).resolve() for name in PINS)}


def validate_output_target(path: Path) -> Path:
    absolute = path.absolute()
    parent = absolute.parent
    require(
        parent.exists()
        and parent.is_dir()
        and not parent.is_symlink()
        and parent.resolve() == parent,
        "safe output parent",
    )
    require(not absolute.is_symlink(), "output symlink")
    resolved = absolute.resolve(strict=False)
    protected = protected_paths()
    require(resolved not in protected, "output aliases protected path")
    if absolute.exists():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
            "safe existing output",
        )
        for item in protected:
            if item.exists():
                require(not os.path.samefile(absolute, item), "output hardlink aliases protected input")
    return resolved


def write_atomic(path: Path, value: dict[str, Any]) -> None:
    resolved = validate_output_target(path)
    payload = json.dumps(
        value,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{resolved.name}.", suffix=".tmp", dir=resolved.parent
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, resolved)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    envelope = build()
    write_atomic(args.output, envelope)
    print("STATUS:", envelope["result"]["status"])
    print("REGISTRY_ID:", envelope["result"]["migration_registry_id"])
    print("CORRECTED_COMPONENT_ID:", envelope["result"]["current_identifier_values"]["component_v1_id"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CertificationError, KeyError, TypeError, ValueError, OSError) as exc:
        print(f"CertificationError: {exc}", file=sys.stderr)
        raise SystemExit(1)
