#!/usr/bin/env python3
"""Round306B1AF4P1 preserved/non-graph exact-join preflight.

This is a read-only, zero-theorem-credit replay.  It pins and replays the
identity/authority joins needed before a formal normalized-support producer
can exist for the 126,468 preserved and 17,828 non-graph Source-G members.
It does not construct a B1A candidate and does not turn an upstream witness,
outer envelope, promotion summary, or wire-shaped kernel certificate into a
full-support theorem.

Normal contract printing and self-test are filesystem-inert.  Only the
explicit ``--full-replay`` mode opens the 28 pinned inputs.  Candidate and
production entry points refuse before any path, input, temporary-file, or
output operation.
"""

from __future__ import annotations

import argparse
import builtins
from collections import Counter, defaultdict
import copy
import gzip
import hashlib
import heapq
import io
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any, Callable, Final, Iterable, Iterator
from unittest import mock


class PreflightBlocked(RuntimeError):
    """Fail-closed contract, pin, join, or mode violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise PreflightBlocked(label)


SCHEMA: Final = (
    "cm2.round306b1af4p1.source-g-preserved-non-graph-"
    "exact-join-preflight.v1"
)
STATUS: Final = (
    "PASS_ZERO_CREDIT_EXACT_JOIN_PREFLIGHT_CONTRACT__"
    "FORMAL_NORMALIZED_SUPPORT_AND_B1A_STILL_BLOCKED"
)
REPLAY_STATUS: Final = (
    "PASS_EXACT_144296_MEMBER_IDENTITY_AUTHORITY_PREFLIGHT__"
    "NO_NORMALIZED_FULL_SUPPORT_THEOREM_CREDIT"
)
CANDIDATE_BLOCK_REASON: Final = (
    "AF4P1 is a read-only zero-credit replay/preflight; candidate and "
    "production modes are blocked before path/open/temp/write"
)
INPUT_DIRECTORY: Final = Path(__file__).parent
SORT_BUFFER_LIMIT: Final = 16 * 1024 * 1024
DECODED_CANONICAL_ROW_CAP: Final = 8_388_608
PARSER_CHUNK_BYTES: Final = 1_048_576
PARSER_BUFFER_CAP: Final = 9_437_184


# Exact byte pins.  These are data, not import targets.  Full replay only
# decodes the listed ledgers; it never imports or executes any upstream file.
INPUT_PINS: Final = (
    ("AF2_CONTRACT", "cm2_round306b1af2_source_g_primitive_support_source_partition_freeze_contract.py", 52_538, "a91578a8bef1c4a72f940f7ebc71aea4c0ebc1ddac08ddbb3889a2da6cdd00f5"),
    ("AF2_PRIMARY_RESULT", "cm2_round306b1af2_source_g_primitive_support_source_partition_primary_result.json", 2_540, "7238c245e79124e5bf3aa14c463fcc639efcde7431b03ac3a1cd035a4d1f7ebb"),
    ("AF2_INDEPENDENT_RESULT", "cm2_round306b1af2_source_g_primitive_support_source_partition_independent_result.json", 2_540, "7238c245e79124e5bf3aa14c463fcc639efcde7431b03ac3a1cd035a4d1f7ebb"),
    ("AF3D1_CONTRACT", "cm2_round306b1af3d1_source_g_support_representation_authority_delta_contract.py", 57_389, "d61fbdc7e6d917c9c451cf63a7640285e900fd08dff76800119ca60ae5e55138"),
    ("AF4_KERNEL", "cm2_round306b1af4_source_g_normalized_support_symbolic_kernel.py", 87_237, "c8bb9cf85aace782639859c33625732bf866a7fad34ff31cce58ab84af9f6a6f"),
    ("AF4_SCHEMA", "cm2_round306b1af4_source_g_normalized_support_representation_typed_schema_contract.py", 80_436, "ee095fe5db22c6a4dd0804eca0fb553a132546367dcb37fcd75733050aa52cf9"),
    ("AF4D1_SEMANTIC_DELTA", "cm2_round306b1af4d1_source_g_semantic_wire_delta_contract.py", 84_392, "5082df54ea4c514de906f4a923856adb20c6240c9be33401e784b2513a85f09f"),
    ("B0", "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz", 162_499_140, "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af"),
    ("R294_REGISTRY", "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz", 262_951_902, "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb"),
    ("R294_ALIAS", "cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz", 26_672_326, "f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833"),
    ("R295A_ALIAS", "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_representation_alias_ledger.json.gz", 118_612, "5c826ef03dd6f8662528e565c36089422e590d1ebf9fc8bade99f1665c68ad2f"),
    ("R266", "cm2_round266_source_g_expanded_curved_face_closure_certificate.json", 934_776_249, "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf"),
    ("R174", "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json", 113_656_620, "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54"),
    ("R179", "cm2_round179_source_g_residual_tube_arrangement_rows.json", 131_273_924, "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42"),
    ("R204", "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json", 7_157_575, "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818"),
    ("R208", "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json", 193_161_618, "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938"),
    ("R211", "cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json", 140_690_802, "bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f"),
    ("R220", "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json", 294_422_681, "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"),
    ("R232", "cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json", 3_596_500, "a33d14fd7fd0ca0bb8e64efefd97be0839a5a8107b759f2219c14580ef3aa8c0"),
    ("R234", "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json", 50_766_450, "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"),
    ("R236", "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json", 2_061_199, "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"),
    ("R237", "cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json", 346_302, "5fa46f8c6d8074770ebbf8cbdb2f0590dbdf5710254d05c6a0a3aca0953359f3"),
    ("R238", "cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json", 399_196, "8200ba9c35ba32c938eb66beb7a4040908db9b81fc449881a55b09e67b517446"),
    ("R242", "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json", 13_734_655, "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e"),
    ("R245", "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json", 20_683_081, "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1"),
    ("R246", "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json", 18_283_721, "a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9"),
    ("R247", "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json", 13_400_149, "72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7"),
    ("R248", "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json", 205_148_977, "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"),
)

PRESERVED_COUNTS: Final = (
    ("ROUND174_RESOLVED", 72_500),
    ("ROUND179_RESOLVED", 17_192),
    ("ROUND204_REGION", 736),
    ("ROUND208_REGION", 36_040),
)
NON_GRAPH_COUNTS: Final = (
    ("R245_WHOLE_ROOT_ZERO_ABSENCE_BULK", 2_872),
    ("R246_WHOLE_ORIGIN_SINGLE_SIGNATURE_RETAINED_BULK", 2_220),
    ("R247_CROSSING_TIME_WHOLE_SIGNATURE_RETAINED_BULK", 240),
    ("R247_SOURCE_CHART_SEAM_WHOLE_SIGNATURE_RETAINED_BULK", 264),
    ("R248_ROUND234_RESOLVED_DESCENDANT", 12_200),
    ("R248_ROUND236_CROSSING_DISCHARGE_BULK", 32),
)
ALIAS_SOURCE_CLASS_COUNTS: Final = (
    ("ROUND174_RESOLVED", 752),
    ("ROUND179_RESOLVED", 848),
    ("ROUND204_REGION", 640),
    ("ROUND208_REGION", 36_760),
)
ALIAS_REPRESENTATION_COUNTS: Final = (
    ("TPS_EXACT_EQUAL", 36_680),
    ("TPS_INCLUSION_SUBCOVER", 720),
    ("T2PS_REFINED_SUBCOVER", 1_600),
)
A1_A2_COUNTS: Final = (
    ("A1_R204_TARGET_SHEET", 224),
    ("A1_R211_OWNER_SHEET", 17_716),
    ("A2_R204_SOURCE_TARGET_CURVE", 504),
    ("A2_R204_SOURCE_TARGET_ENDPOINT", 280),
    ("A2_R211_OWNER_CURVE", 20_456),
    ("A2_R211_OWNER_ENDPOINT", 40_912),
)

# Exact JSON property paths for every selected replay table.  Array indices are
# never elided into these paths: the structural validator inserts the literal
# ``[]`` while descending array elements, so a lookalike key inside a row
# cannot satisfy a top-level/result-table path.
SELECTED_TABLE_PATHS: Final = {
    "B0": (("member_support_source_rows",),),
    "R294_REGISTRY": (("rows",),),
    "R294_ALIAS": (("rows",),),
    "R295A_ALIAS": (("rows",),),
    "R266": (
        ("result", "formal_post_Round266_expanded_occurrence_frontier_ledger", "rows"),
        ("result", "formal_post_Round266_valid_virtual_node_frontier_ledger", "rows"),
        ("result", "formal_post_Round266_component_member_frontier_ledger", "rows"),
    ),
    "R174": (("result", "resolved_3d_occurrence_rows"),),
    "R179": (
        ("result", "resolved_3d_child_rows"),
        ("result", "retained_3d_child_rows"),
    ),
    "R204": (
        ("result", "formal_local_open_3D_region_ledger", "rows"),
        ("result", "formal_2D_sheet_lineage", "target_sheet_rows"),
        ("result", "formal_1D_boundary_and_intersection_lineage", "rows"),
        ("result", "formal_0D_endpoint_and_corner_lineage", "rows"),
    ),
    "R208": (("result", "formal_local_open_3D_signature_ledger", "rows"),),
    "R211": (
        ("result", "formal_2D_sheet_owner_ledger", "rows"),
        ("result", "formal_1D_curve_incidence_owner_ledger", "rows"),
        ("result", "formal_0D_endpoint_incidence_owner_ledger", "rows"),
    ),
    "R220": (("result", "coordinate_boundary_atlas", "tables", "one_step_split_interface_rows", "rows"),),
    "R232": (("result", "whole_origin_promotion_rows"),),
    "R234": (("result", "resolved_descendant_rows"),),
    "R236": (("result", "crossing_dependency_discharge_rows"),),
    "R237": (("result", "whole_origin_promotion_rows"),),
    "R238": (("result", "whole_origin_promotion_rows"),),
    "R242": (("result", "formal_zero_absence_base_partition_ledger", "rows"),),
    "R245": (("result", "formal_retained_stratum_node_ledger", "rows"),),
    "R246": (("result", "formal_new_whole_signature_retained_stratum_node_ledger", "rows"),),
    "R247": (("result", "formal_new_crossing_and_source_seam_retained_stratum_node_ledger", "rows"),),
    "R248": (("result", "formal_wall_positive_volume_bulk_ledger", "rows"),),
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def _reject_nonstandard_constant(token: str) -> Any:
    raise PreflightBlocked("nonstandard JSON constant:" + token)


def canonical_replay_row_bytes(value: Any) -> bytes:
    raw = canonical_bytes(value)
    need(len(raw) <= DECODED_CANONICAL_ROW_CAP, "canonical replay row cap")
    return raw


def replay_row_digest(value: Any) -> str:
    return hashlib.sha256(canonical_replay_row_bytes(value)).hexdigest()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def row_digest(row: dict[str, Any]) -> str:
    body = dict(row)
    expected = body.pop("row_sha256", None)
    need(isinstance(expected, str) and len(expected) == 64, "row SHA field")
    actual = replay_row_digest(body)
    need(actual == expected, "row SHA mismatch")
    return actual


AST_BLUEPRINTS: Final = (
    {
        "source": "R174_RESOLVED",
        "support_ast": "OPEN_RATIONAL_BOX(t0<t<t1 AND p0<p<p1 AND s0<s<s1)",
        "authority": "R174.resolved_3d_occurrence_rows.box",
    },
    {
        "source": "R179_RESOLVED",
        "support_ast": "OPEN_RATIONAL_BOX(t0<t<t1 AND p0<p<p1 AND s0<s<s1)",
        "authority": "R179.resolved_3d_child_rows.box",
    },
    {
        "source": "R204_REGION",
        "support_ast": "OPEN_RATIONAL_BOX AND STRICT_SIGN((9/25)*t) AND STRICT_SIGN(hit_X_or_Y_wall_factor)",
        "authority": "R204.formal_local_open_3D_region_ledger",
    },
    {
        "source": "R208_REGION",
        "support_ast": "OPEN_RATIONAL_BOX AND STRICT_SIGN(F) AND STRICT_SIGN(HPLUS) AND STRICT_SIGN(HMINUS)",
        "identities": ["HPLUS=vx+vy", "HMINUS=vx-vy", "F=HPLUS*HMINUS=vx^2-vy^2"],
        "authority": "R208.formal_local_open_3D_signature_ledger",
    },
    {
        "source": "R204_A1_A2",
        "support_ast": "TARGET_FACTOR=0_GRAPH_IN_t; CURVE=t=0_AND_TARGET_FACTOR=0; ENDPOINT=CURVE_AND_FIXED_s",
        "authority": "R204 formal 2D/1D/0D lineages",
    },
    {
        "source": "R211_A1_A2",
        "support_ast": "HPLUS_or_HMINUS=0_IN_LEAF; BOUNDARY_RESTRICTION; ENDPOINT_RESTRICTION",
        "authority": "R211 formal owner sheet/curve/endpoint ledgers",
    },
    {
        "source": "R245_NON_GRAPH",
        "support_ast": "FULL_RETAINED_OPEN_BOX",
        "authority": "R179 retained child plus R242 zero-absence partition",
        "forbidden_substitute": "strict_positive_3D_witness_box",
    },
    {
        "source": "R246_NON_GRAPH",
        "support_ast": "FULL_RETAINED_CHILD_OPEN_BOX",
        "authority": "R179 retained child plus R232 finite-descendant cover",
        "forbidden_substitute": "resolved_plus_retained_union_summary",
    },
    {
        "source": "R247_CROSSING",
        "support_ast": "FULL_RETAINED_CHILD_OPEN_BOX",
        "authority": "R179 retained child plus R237 crossing promotion",
    },
    {
        "source": "R247_SOURCE_SEAM",
        "support_ast": "FULL_RETAINED_CHILD_OPEN_BOX AND (2*t^2-1<0)",
        "authority": "R179 retained child plus R238 seam promotion",
        "forbidden_substitute": "dyadic_inside_corridor_witness",
    },
    {
        "source": "R248_NON_GRAPH",
        "support_ast": "EXACT_R234_OR_R236_POSITIVE_OPEN_BOX",
        "authority": "R248 exact_positive_3D_box with direct R234/R236 lineage",
    },
    {
        "source": "T2PS_PULLBACK",
        "support_ast": "FORWARD(t=sigma*sqrt(u)); INVERSE(u=t^2)",
        "authority": "fixed-sign T2PS pullback only",
        "limitation": "does not discharge alias subset-equality",
    },
)

BLOCKERS: Final = (
    {
        "id": "B01_WIRE_SHAPE_KERNEL_ZERO_THEOREM_CREDIT",
        "reason": "the sealed 13-kernel bundle is mostly wire-shape validation; equivalence, graph existence, incidence, backbinding, sheet/boundary ownership, and source exhaustion remain unproved",
    },
    {
        "id": "B02_NO_INDEPENDENT_SYMBOLIC_DIFFERENTIATION",
        "reason": "no pinned independent symbolic differentiation and derivative-identity primitive exists",
    },
    {
        "id": "B03_R211_NOT_SELF_CONTAINED",
        "reason": "R211 rows omit a self-contained chart/target/box/equation/derivative AST and require multi-hop R208/probe reconstruction plus independent interval proof",
    },
    {
        "id": "B04_ALIAS_SET_EQUALITY_NOT_DISCHARGED",
        "reason": "720 TPS inclusion rows, 1600 T2PS subcover rows, and 276 R295A adjacent continuation boxes cannot claim per-row complete-support set equality",
    },
    {
        "id": "B05_TPS_INTERCHART_THEOREM_MISSING",
        "reason": "canonical TPS inter-chart forward/inverse AST and theorem are absent; generic CHART_PULLBACK and fixed-sign T2PS are insufficient",
    },
    {
        "id": "B06_DIRECT_THEOREM_EVIDENCE_FRONTIER_INCOMPLETE",
        "reason": "independent theorem replay still needs direct row-level R231/R233/R230/R235/Gate5/R209 evidence; promotion summaries do not suffice",
    },
)


def _pin_documents() -> list[dict[str, Any]]:
    return [
        {
            "label": label,
            "filename": filename,
            "exact_size": size,
            "sha256": sha,
            "role": (
                "SEALED_GOVERNANCE_BYTES_ONLY"
                if label.startswith("AF")
                else "READ_ONLY_REPLAY_INPUT"
            ),
        }
        for label, filename, size, sha in INPUT_PINS
    ]


def contract_document() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "sealed": True,
        "artifact_kind": "ZERO_CREDIT_READ_ONLY_FULL_REPLAY_PREFLIGHT__NOT_FORMAL_CONSTRUCTOR",
        "scope": {
            "preserved_member_count": 126_468,
            "non_graph_member_count": 17_828,
            "exact_scope_member_count": 144_296,
            "preserved_source_counts": [
                {"source": key, "count": count} for key, count in PRESERVED_COUNTS
            ],
            "non_graph_source_counts": [
                {"source": key, "count": count} for key, count in NON_GRAPH_COUNTS
            ],
            "outside_scope": ["R2", "R292", "G2A", "G2B"],
        },
        "exact_input_pins": {
            "count": len(INPUT_PINS),
            "total_bytes": sum(row[2] for row in INPUT_PINS),
            "pin_set_sha256": digest(_pin_documents()),
            "files": _pin_documents(),
            "upstream_python_imported_or_executed": False,
        },
        "input_security": {
            "held_directory_descriptor": True,
            "O_NOFOLLOW": True,
            "regular_file_required": True,
            "nlink_must_equal": 1,
            "two_full_sha256_passes_per_held_fd": True,
            "path_fd_identity_checked_before_and_after": True,
            "symlink_hardlink_TOCTOU_path_replacement": "FAIL_CLOSED",
            "whole_JSON_document_structure_replayed_to_EOF": True,
            "duplicate_object_keys_rejected_at_every_depth": True,
            "selected_table_exact_property_path_required_once": True,
            "selected_table_offsets_derived_from_exact_structural_paths": True,
            "raw_marker_search_used": False,
        },
        "authority_frontier": {
            "identity_authorities": ["B0", "R294_REGISTRY", "R266"],
            "representation_authorities": ["R294_ALIAS", "R295A_ALIAS"],
            "construction_authorities": ["R174", "R179", "R204", "R208", "R211", "R220", "R232", "R234", "R236", "R237", "R238", "R242", "R245", "R246", "R247", "R248"],
            "priority": "EXACT_CONSTRUCTION_ROW > DIRECT_LINEAGE_ROW > IDENTITY_BINDING > PROMOTION_SUMMARY > WITNESS_OR_OUTER_ENVELOPE",
            "identity_binding_may_supply_geometry": False,
            "witness_or_outer_envelope_may_equal_full_support": False,
        },
        "required_join_replay": {
            "preserved": [
                "B0.R294 primary <-> R294 preserved registry",
                "R294.source_row <-> R266 expanded occurrence",
                "R266.source_geometry <-> exact R174/R179/R204/R208 row",
            ],
            "non_graph": [
                "B0.R266 primary <-> R266 valid-virtual component member",
                "R266 component <-> R266 valid virtual frontier",
                "R266 member <-> exact selected R245/R246/R247/R248 row",
                "selected source lineage <-> R179/R220/R232/R234/R236/R237/R238/R242",
            ],
            "every_link_requires": [
                "full_identity_join",
                "forward_antijoin_zero",
                "reverse_antijoin_zero",
                "duplicate_identity_zero",
                "available_row_hash_backbinding_or_pinned_content_address",
            ],
            "row_hash_scope": {
                "object_row_with_row_sha256": "RECOMPUTE_CANONICAL_ROW_WITHOUT_row_sha256_AND_REQUIRE_EQUALITY",
                "packed_or_content_addressed_row_without_row_sha256": "DO_NOT_INVENT_ROW_HASH__REQUIRE_WHOLE_FILE_PIN_UNIQUE_ROW_ID_AND_ALL_AVAILABLE_FIELD_BACKBINDINGS",
                "blanket_every_row_has_own_hash_claimed": False,
            },
        },
        "representation_alias_dispatch": {
            "R294_total": 46_288,
            "R294_preserved_target": 39_000,
            "R294_R288_residual_outside_scope": 7_288,
            "R295A_preserved_target": 276,
            "preserved_source_class_counts": [
                {"source": key, "count": count}
                for key, count in ALIAS_SOURCE_CLASS_COUNTS
            ],
            "preserved_representation_semantics": [
                {"kind": key, "count": count}
                for key, count in ALIAS_REPRESENTATION_COUNTS
            ],
            "R294_unique_preserved_target_occurrence_ids": 37_388,
            "R294_source_owner_keys_unique": 46_288,
            "R295A_source_owner_keys_unique": 276,
            "namespaced_global_owner_keys_unique": 46_564,
            "R294_R295A_target_occurrence_intersection": 0,
            "T2PS_1600_classification": "PRESERVED_ALIAS_SUBCOVER__NOT_R288_RESIDUAL",
        },
        "ast_blueprints": {
            "rows": list(AST_BLUEPRINTS),
            "source_by_source_blueprint_sha256": digest(AST_BLUEPRINTS),
            "typed_AST_rows_are_constructed_by_this_preflight": False,
        },
        "A1_A2_obligation_census": {
            "rows": [{"kind": key, "count": count} for key, count in A1_A2_COUNTS],
            "A1": 17_940,
            "A2": 62_152,
            "total": 80_092,
            "counts_are_obligations_not_proved_features": True,
        },
        "resource_contract": {
            "incremental_JSON_and_gzip_decode": True,
            "strict_selected_array_single_comma_grammar": True,
            "missing_double_and_trailing_commas_rejected": True,
            "trailing_document_garbage_rejected": True,
            "nonstandard_NaN_Infinity_constants_rejected": True,
            "decoded_and_canonical_row_cap_bytes": DECODED_CANONICAL_ROW_CAP,
            "parser_buffer_cap_bytes": PARSER_BUFFER_CAP,
            "parser_chunk_bytes": PARSER_CHUNK_BYTES,
            "parser_buffer_cap_equation": "9437184=8388608+1048576",
            "bounded_external_sort": True,
            "sort_buffer_limit_bytes": SORT_BUFFER_LIMIT,
            "deterministic_bytewise_canonical_JSON_order": True,
            "temporary_files_outside_deliverables": True,
            "OS_temp_root_realpath_outside_deliverables_required": True,
            "OS_temp_root_non_symlink_held_identity_required": True,
            "created_temp_directory_realpath_outside_deliverables_required": True,
            "created_temp_directory_non_symlink_required": True,
            "measured_RSS_bytes": None,
            "RSS_claimed": False,
        },
        "remaining_blockers": list(BLOCKERS),
        "remaining_blocker_count": 6,
        "candidate_and_production_modes": {
            "enabled": False,
            "block_reason": CANDIDATE_BLOCK_REASON,
            "block_before_path": True,
            "block_before_open": True,
            "block_before_temp": True,
            "block_before_write": True,
        },
        "full_replay_success_means": "IDENTITY_AUTHORITY_AND_BLUEPRINT_PREFLIGHT_ONLY",
        "full_replay_success_does_not_mean": [
            "NORMALIZED_FULL_SUPPORT_PROVED",
            "REPRESENTATION_SET_EQUALITY_PROVED",
            "FORMAL_B1A_MINTED",
            "B2_AUTHORIZED",
            "D02_UNBLOCKED",
            "CM2_GO",
        ],
        "formal_credit": {
            "normalized_member_support": 0,
            "representation_cover": 0,
            "A1_A2": 0,
            "B1A": 0,
            "transition": 0,
            "pair_routing": 0,
            "maximality": 0,
            "CM2": 0,
        },
        "downstream_state": {
            "B1A": "BLOCKED_BY_EXACT_SIX_PREFLIGHT_BLOCKERS",
            "B2": "NOT_AUTHORIZED",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }


def validate_contract(doc: dict[str, Any]) -> None:
    need(doc["schema"] == SCHEMA, "schema")
    need(doc["status"] == STATUS and doc["sealed"] is True, "sealed status")
    need(doc["artifact_kind"].startswith("ZERO_CREDIT_READ_ONLY"), "artifact kind")
    scope = doc["scope"]
    need(scope["preserved_member_count"] == 126_468, "preserved count")
    need(scope["non_graph_member_count"] == 17_828, "non-graph count")
    need(scope["exact_scope_member_count"] == 144_296, "scope count")
    need(
        tuple((r["source"], r["count"]) for r in scope["preserved_source_counts"])
        == PRESERVED_COUNTS,
        "preserved fine census",
    )
    need(
        tuple((r["source"], r["count"]) for r in scope["non_graph_source_counts"])
        == NON_GRAPH_COUNTS,
        "non-graph fine census",
    )
    pins = doc["exact_input_pins"]
    need(pins["count"] == len(INPUT_PINS) == 28, "pin count")
    need(pins["total_bytes"] == sum(row[2] for row in INPUT_PINS), "pin bytes")
    need(pins["files"] == _pin_documents(), "pin files")
    need(pins["pin_set_sha256"] == digest(_pin_documents()), "pin digest")
    need(pins["upstream_python_imported_or_executed"] is False, "no upstream exec")
    security = doc["input_security"]
    need(all(security[k] is True for k in (
        "held_directory_descriptor", "O_NOFOLLOW", "regular_file_required",
        "two_full_sha256_passes_per_held_fd",
        "path_fd_identity_checked_before_and_after",
        "whole_JSON_document_structure_replayed_to_EOF",
        "duplicate_object_keys_rejected_at_every_depth",
        "selected_table_exact_property_path_required_once",
        "selected_table_offsets_derived_from_exact_structural_paths",
    )), "input security")
    need(security["nlink_must_equal"] == 1, "nlink")
    need(security["raw_marker_search_used"] is False, "no raw marker search")
    authority = doc["authority_frontier"]
    need(authority["identity_binding_may_supply_geometry"] is False, "identity geometry")
    need(authority["witness_or_outer_envelope_may_equal_full_support"] is False, "witness full support")
    joins = doc["required_join_replay"]
    need("forward_antijoin_zero" in joins["every_link_requires"], "forward anti-join")
    need("reverse_antijoin_zero" in joins["every_link_requires"], "reverse anti-join")
    need("duplicate_identity_zero" in joins["every_link_requires"], "duplicate identity")
    need(
        "available_row_hash_backbinding_or_pinned_content_address"
        in joins["every_link_requires"],
        "available row-hash backbinding",
    )
    need(
        joins["row_hash_scope"]["blanket_every_row_has_own_hash_claimed"] is False,
        "precise row-hash scope",
    )
    aliases = doc["representation_alias_dispatch"]
    need(aliases["R294_total"] == 46_288, "R294 alias count")
    need(aliases["R294_preserved_target"] == 39_000, "R294 preserved aliases")
    need(aliases["R294_R288_residual_outside_scope"] == 7_288, "R294 residual aliases")
    need(aliases["R295A_preserved_target"] == 276, "R295A aliases")
    need(aliases["R294_unique_preserved_target_occurrence_ids"] == 37_388, "alias targets")
    need(aliases["namespaced_global_owner_keys_unique"] == 46_564, "alias owners")
    need(aliases["R294_R295A_target_occurrence_intersection"] == 0, "alias disjoint")
    need(
        tuple((r["source"], r["count"]) for r in aliases["preserved_source_class_counts"])
        == ALIAS_SOURCE_CLASS_COUNTS,
        "alias source census",
    )
    need(
        tuple((r["kind"], r["count"]) for r in aliases["preserved_representation_semantics"])
        == ALIAS_REPRESENTATION_COUNTS,
        "alias representation census",
    )
    blueprints = doc["ast_blueprints"]
    need(blueprints["rows"] == list(AST_BLUEPRINTS), "blueprints")
    need(blueprints["source_by_source_blueprint_sha256"] == digest(AST_BLUEPRINTS), "blueprint digest")
    need(blueprints["typed_AST_rows_are_constructed_by_this_preflight"] is False, "no AST construction")
    obligations = doc["A1_A2_obligation_census"]
    need(obligations["A1"] == 17_940 and obligations["A2"] == 62_152, "A1/A2")
    need(obligations["total"] == 80_092, "A1/A2 total")
    need(obligations["counts_are_obligations_not_proved_features"] is True, "obligation only")
    resource = doc["resource_contract"]
    need(resource["bounded_external_sort"] is True, "external sort")
    need(resource["strict_selected_array_single_comma_grammar"] is True, "strict array grammar")
    need(resource["missing_double_and_trailing_commas_rejected"] is True, "comma attacks")
    need(resource["trailing_document_garbage_rejected"] is True, "EOF garbage")
    need(resource["nonstandard_NaN_Infinity_constants_rejected"] is True, "nonstandard constants")
    need(resource["decoded_and_canonical_row_cap_bytes"] == DECODED_CANONICAL_ROW_CAP, "decoded row cap")
    need(resource["parser_buffer_cap_bytes"] == PARSER_BUFFER_CAP, "parser buffer cap")
    need(resource["parser_chunk_bytes"] == PARSER_CHUNK_BYTES, "parser chunk")
    need(PARSER_BUFFER_CAP == DECODED_CANONICAL_ROW_CAP + PARSER_CHUNK_BYTES, "parser cap equation")
    need(resource["OS_temp_root_realpath_outside_deliverables_required"] is True, "external temp root")
    need(resource["OS_temp_root_non_symlink_held_identity_required"] is True, "held temp root")
    need(resource["created_temp_directory_realpath_outside_deliverables_required"] is True, "external created temp")
    need(resource["created_temp_directory_non_symlink_required"] is True, "created temp no symlink")
    need(resource["sort_buffer_limit_bytes"] == SORT_BUFFER_LIMIT, "sort bound")
    need(resource["measured_RSS_bytes"] is None and resource["RSS_claimed"] is False, "no RSS claim")
    need(doc["remaining_blocker_count"] == len(doc["remaining_blockers"]) == 6, "six blockers")
    need(doc["remaining_blockers"] == list(BLOCKERS), "blocker exactness")
    modes = doc["candidate_and_production_modes"]
    need(modes["enabled"] is False and modes["block_reason"] == CANDIDATE_BLOCK_REASON, "modes blocked")
    need(all(modes[k] is True for k in ("block_before_path", "block_before_open", "block_before_temp", "block_before_write")), "mode boundary")
    need(all(value == 0 for value in doc["formal_credit"].values()), "zero credit")
    need(doc["downstream_state"] == {
        "B1A": "BLOCKED_BY_EXACT_SIX_PREFLIGHT_BLOCKERS",
        "B2": "NOT_AUTHORIZED",
        "D02": "BLOCKED",
        "CM2": "NO-GO_FOR_CLAIM",
    }, "downstream state")
    # This final equality is deliberate: validation is an exact sealed
    # document check, not a sparse collection of predicates.  No unvalidated
    # field can be promoted, erased, appended, or silently rewritten.
    need(doc == contract_document(), "exact entire contract document")


def contract_envelope() -> dict[str, Any]:
    doc = contract_document()
    validate_contract(doc)
    return {"contract": doc, "canonical_contract_digest_sha256": digest(doc)}


def _stat_fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
        info.st_size, info.st_mtime_ns, info.st_ctime_ns,
    )


def _directory_identity(info: os.stat_result) -> tuple[int, int, int]:
    return info.st_dev, info.st_ino, info.st_mode


def _hash_fd(fd: int) -> tuple[int, str]:
    os.lseek(fd, 0, os.SEEK_SET)
    h = hashlib.sha256()
    total = 0
    while True:
        block = os.read(fd, 1024 * 1024)
        if not block:
            break
        total += len(block)
        h.update(block)
    return total, h.hexdigest()


class _ByteJSONReader:
    """Buffered byte reader for strict, allocation-bounded JSON validation."""

    def __init__(self, stream: io.BufferedIOBase) -> None:
        self.stream = stream
        self.buffer = b""
        self.position = 0
        self.eof = False
        self.offset = 0

    def _fill(self) -> bool:
        if self.position < len(self.buffer):
            return True
        block = self.stream.read(PARSER_CHUNK_BYTES)
        if not block:
            self.buffer = b""
            self.position = 0
            self.eof = True
            return False
        self.buffer = block
        self.position = 0
        return True

    def peek(self) -> int | None:
        return self.buffer[self.position] if self._fill() else None

    def take(self) -> int:
        value = self.peek()
        need(value is not None, "unexpected JSON EOF")
        self.position += 1
        self.offset += 1
        return value

    def whitespace(self) -> None:
        while True:
            if not self._fill():
                return
            start = self.position
            while self.position < len(self.buffer) and self.buffer[self.position] in b" \t\r\n":
                self.position += 1
                self.offset += 1
            if self.position == start:
                return

    def string(self, decode: bool) -> str | None:
        need(self.take() == 0x22, "JSON string opening quote")
        pieces = bytearray() if decode else None
        escaped = False
        while True:
            need(self._fill(), "unterminated JSON string")
            quote = self.buffer.find(b'"', self.position)
            slash = self.buffer.find(b"\\", self.position)
            candidates = [at for at in (quote, slash) if at >= 0]
            stop = min(candidates) if candidates else len(self.buffer)
            segment = self.buffer[self.position:stop]
            need(not segment or min(segment) >= 0x20, "unescaped JSON control byte")
            need(not segment or max(segment) < 0x80, "non-ASCII pinned JSON")
            if pieces is not None:
                pieces.extend(segment)
            self.position = stop
            self.offset += len(segment)
            if stop == len(self.buffer):
                continue
            token = self.buffer[self.position]
            self.position += 1
            self.offset += 1
            if token == 0x22:
                if pieces is None:
                    return None
                if not escaped:
                    return pieces.decode("ascii")
                return json.loads(b'"' + bytes(pieces) + b'"')
            escaped = True
            if pieces is not None:
                pieces.append(0x5C)
            escape = self.take()
            need(escape in b'"\\/bfnrtu', "invalid JSON escape")
            if pieces is not None:
                pieces.append(escape)
            if escape == ord("u"):
                for _ in range(4):
                    hexdigit = self.take()
                    need(hexdigit in b"0123456789abcdefABCDEF", "invalid JSON unicode escape")
                    if pieces is not None:
                        pieces.append(hexdigit)


class _StrictJSONStructure:
    """Validate one complete JSON document, paths, duplicate keys, and EOF."""

    def __init__(self, stream: io.BufferedIOBase, wanted_paths: Iterable[tuple[str, ...]]) -> None:
        self.reader = _ByteJSONReader(stream)
        self.wanted = set(wanted_paths)
        self.path_counts: Counter[tuple[str, ...]] = Counter()
        self.path_offsets: dict[tuple[str, ...], int] = {}
        self.object_count = 0
        self.array_count = 0
        self.scalar_count = 0
        self.key_count = 0
        self.max_depth = 0
        self.array_element_count = 0
        self.maximum_array_element_bytes = 0
        self.decoder = json.JSONDecoder(
            object_pairs_hook=self._array_object_pairs,
            parse_constant=_reject_nonstandard_constant,
        )

    def _array_object_pairs(self, pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        self.object_count += 1
        for key, value in pairs:
            need(key not in result, "duplicate JSON object key:" + key)
            result[key] = value
            self.key_count += 1
        return result

    def run(self) -> dict[str, Any]:
        self.reader.whitespace()
        self._value((), 0)
        self.reader.whitespace()
        need(self.reader.peek() is None, "trailing JSON document garbage")
        need(set(self.path_counts) == self.wanted, "selected JSON path set")
        need(all(self.path_counts[path] == 1 for path in self.wanted), "selected JSON path uniqueness")
        return {
            "selected_path_count": len(self.wanted),
            "selected_paths_sha256": digest(sorted([list(path) for path in self.wanted])),
            "all_selected_paths_exactly_once": True,
            "selected_array_content_offsets": {
                ".".join(path): self.path_offsets[path] for path in sorted(self.path_offsets)
            },
            "raw_marker_search_used": False,
            "duplicate_object_key_count": 0,
            "document_EOF_verified": True,
            "object_count": self.object_count,
            "array_count": self.array_count,
            "scalar_count": self.scalar_count,
            "key_count": self.key_count,
            "maximum_depth": self.max_depth,
            "array_element_count": self.array_element_count,
            "maximum_array_element_bytes": self.maximum_array_element_bytes,
        }

    def _value(self, path: tuple[str, ...], depth: int) -> None:
        self.max_depth = max(self.max_depth, depth)
        token = self.reader.peek()
        need(token is not None, "missing JSON value")
        if token == ord("{"):
            self._object(path, depth)
        elif token == ord("["):
            self._array(path, depth)
        elif token == ord('"'):
            self.reader.string(False)
            self.scalar_count += 1
        elif token == ord("t"):
            self._literal(b"true")
        elif token == ord("f"):
            self._literal(b"false")
        elif token == ord("n"):
            self._literal(b"null")
        else:
            self._number()

    def _literal(self, literal: bytes) -> None:
        for expected in literal:
            need(self.reader.take() == expected, "invalid JSON literal")
        self.scalar_count += 1

    def _number(self) -> None:
        token = self.reader.peek()
        if token == ord("-"):
            self.reader.take()
            token = self.reader.peek()
        need(token is not None, "truncated JSON number")
        if token == ord("0"):
            self.reader.take()
            following = self.reader.peek()
            need(following is None or following not in b"0123456789", "JSON leading zero")
        else:
            need(token in b"123456789", "invalid JSON value token")
            while self.reader.peek() is not None and self.reader.peek() in b"0123456789":
                self.reader.take()
        if self.reader.peek() == ord("."):
            self.reader.take()
            need(self.reader.peek() is not None and self.reader.peek() in b"0123456789", "JSON fraction digit")
            while self.reader.peek() is not None and self.reader.peek() in b"0123456789":
                self.reader.take()
        if self.reader.peek() in (ord("e"), ord("E")):
            self.reader.take()
            if self.reader.peek() in (ord("+"), ord("-")):
                self.reader.take()
            need(self.reader.peek() is not None and self.reader.peek() in b"0123456789", "JSON exponent digit")
            while self.reader.peek() is not None and self.reader.peek() in b"0123456789":
                self.reader.take()
        self.scalar_count += 1

    def _object(self, path: tuple[str, ...], depth: int) -> None:
        need(self.reader.take() == ord("{"), "JSON object")
        self.object_count += 1
        keys: set[str] = set()
        self.reader.whitespace()
        if self.reader.peek() == ord("}"):
            self.reader.take()
            return
        while True:
            need(self.reader.peek() == ord('"'), "JSON object key")
            key = self.reader.string(True)
            assert isinstance(key, str)
            need(key not in keys, "duplicate JSON object key:" + key)
            keys.add(key)
            self.key_count += 1
            self.reader.whitespace()
            need(self.reader.take() == ord(":"), "JSON object colon")
            self.reader.whitespace()
            child = path + (key,)
            if child in self.wanted:
                need(self.reader.peek() == ord("["), "selected table is not array")
                self.path_counts[child] += 1
                need(child not in self.path_offsets, "duplicate selected table path offset")
                self.path_offsets[child] = self.reader.offset + 1
            self._value(child, depth + 1)
            self.reader.whitespace()
            delimiter = self.reader.take()
            if delimiter == ord("}"):
                return
            need(delimiter == ord(","), "JSON object single comma")
            self.reader.whitespace()
            need(self.reader.peek() not in (ord("}"), ord(","), None), "JSON object trailing/double comma")

    def _array(self, path: tuple[str, ...], depth: int) -> None:
        need(self.reader.take() == ord("["), "JSON array")
        self.array_count += 1
        self.reader.whitespace()
        if self.reader.peek() == ord("]"):
            self.reader.take()
            return
        while True:
            need(self.reader.peek() not in (ord(","), ord("]"), None), "JSON array missing value")
            self._decode_array_element()
            self.reader.whitespace()
            delimiter = self.reader.take()
            if delimiter == ord("]"):
                return
            need(delimiter == ord(","), "JSON array single comma")
            self.reader.whitespace()
            need(self.reader.peek() not in (ord("]"), ord(","), None), "JSON array trailing/double comma")

    def _decode_array_element(self) -> None:
        """Decode one bounded array element with CPython's strict decoder.

        Ledger arrays contain bounded row values.  Decoding one row at a time
        keeps memory independent of table cardinality while the pairs hook
        rejects duplicate keys throughout every row/nested row object.
        """

        need(self.reader._fill(), "missing JSON array element")
        payload = self.reader.buffer[self.reader.position:].decode("ascii")
        need(len(payload.encode("ascii")) <= PARSER_BUFFER_CAP, "structure parser initial buffer cap")
        self.reader.position = len(self.reader.buffer)
        while True:
            try:
                value, end = self.decoder.raw_decode(payload)
                break
            except json.JSONDecodeError:
                block = self.reader.stream.read(PARSER_CHUNK_BYTES)
                need(bool(block), "truncated/invalid JSON array element")
                need(len(payload.encode("ascii")) + len(block) <= PARSER_BUFFER_CAP, "structure parser append cap")
                payload += block.decode("ascii")
        consumed = len(payload[:end].encode("ascii"))
        need(consumed <= DECODED_CANONICAL_ROW_CAP, "structure decoded row cap")
        canonical_replay_row_bytes(value)
        remainder = payload[end:].encode("ascii")
        self.reader.buffer = remainder
        self.reader.position = 0
        self.reader.eof = False
        self.reader.offset += consumed
        self.array_element_count += 1
        self.maximum_array_element_bytes = max(self.maximum_array_element_bytes, consumed)


def _validate_complete_json_stream(
    stream: io.BufferedIOBase,
    wanted_paths: Iterable[tuple[str, ...]],
) -> dict[str, Any]:
    return _StrictJSONStructure(stream, wanted_paths).run()


class HeldInputs:
    """Open and hold every pinned input through the entire replay."""

    def __init__(self) -> None:
        self.directory_fd = -1
        self.directory_before: os.stat_result | None = None
        self.fds: dict[str, int] = {}
        self.rows: list[dict[str, Any]] = []
        self._initial_stats: dict[str, os.stat_result] = {}
        self.final_identity_stable = False
        self.structure_rows: list[dict[str, Any]] = []
        self.structure_validated_labels: set[str] = set()
        self.table_offsets: dict[tuple[str, tuple[str, ...]], int] = {}

    def __enter__(self) -> "HeldInputs":
        directory_text = os.fspath(INPUT_DIRECTORY)
        before = os.stat(directory_text, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode), "input directory")
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        self.directory_fd = os.open(directory_text, flags)
        held = os.fstat(self.directory_fd)
        need(_directory_identity(before) == _directory_identity(held), "directory open race")
        self.directory_before = held
        try:
            for label, filename, exact_size, expected_sha in INPUT_PINS:
                need(filename == os.path.basename(filename) and filename not in ("", ".", ".."), "input basename")
                path_before = os.stat(filename, dir_fd=self.directory_fd, follow_symlinks=False)
                need(stat.S_ISREG(path_before.st_mode), f"regular input:{label}")
                need(path_before.st_nlink == 1, f"nlink:{label}")
                need(path_before.st_size == exact_size, f"size:{label}")
                file_flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
                fd = os.open(filename, file_flags, dir_fd=self.directory_fd)
                held_before = os.fstat(fd)
                need(_stat_fingerprint(path_before) == _stat_fingerprint(held_before), f"path/open race:{label}")
                size1, sha1 = _hash_fd(fd)
                between = os.fstat(fd)
                need(_stat_fingerprint(held_before) == _stat_fingerprint(between), f"pass1 race:{label}")
                size2, sha2 = _hash_fd(fd)
                after = os.fstat(fd)
                need(_stat_fingerprint(held_before) == _stat_fingerprint(after), f"pass2 race:{label}")
                need(size1 == size2 == exact_size, f"two-pass size:{label}")
                need(sha1 == sha2 == expected_sha, f"two-pass SHA:{label}")
                self.fds[label] = fd
                self._initial_stats[label] = held_before
                self.rows.append({
                    "label": label,
                    "filename": filename,
                    "exact_size": exact_size,
                    "pass1_sha256": sha1,
                    "pass2_sha256": sha2,
                    "regular_file": True,
                    "nlink_one": True,
                })
            return self
        except BaseException:
            self.close()
            raise

    def finalize(self) -> None:
        need(self.directory_fd >= 0 and self.directory_before is not None, "held inputs active")
        pin_by_label = {row[0]: row for row in INPUT_PINS}
        for label, fd in self.fds.items():
            filename = pin_by_label[label][1]
            held_after = os.fstat(fd)
            path_after = os.stat(filename, dir_fd=self.directory_fd, follow_symlinks=False)
            need(_stat_fingerprint(self._initial_stats[label]) == _stat_fingerprint(held_after), f"held fd changed:{label}")
            need(_stat_fingerprint(self._initial_stats[label]) == _stat_fingerprint(path_after), f"path replaced:{label}")
        directory_after = os.fstat(self.directory_fd)
        directory_path_after = os.stat(os.fspath(INPUT_DIRECTORY), follow_symlinks=False)
        need(_directory_identity(self.directory_before) == _directory_identity(directory_after), "held directory changed")
        need(_directory_identity(self.directory_before) == _directory_identity(directory_path_after), "directory path replaced")
        self.final_identity_stable = True

    def close(self) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        self.fds.clear()
        if self.directory_fd >= 0:
            try:
                os.close(self.directory_fd)
            except OSError:
                pass
            self.directory_fd = -1

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    def _binary_stream(self, label: str) -> tuple[io.BufferedReader, io.BufferedIOBase]:
        need(label in self.fds, f"unknown held input:{label}")
        duplicate = os.dup(self.fds[label])
        os.lseek(duplicate, 0, os.SEEK_SET)
        raw = os.fdopen(duplicate, "rb", closefd=True)
        filename = next(row[1] for row in INPUT_PINS if row[0] == label)
        if filename.endswith(".gz"):
            return raw, gzip.GzipFile(fileobj=raw, mode="rb")
        return raw, raw

    def validate_selected_documents(self) -> list[dict[str, Any]]:
        """Replay complete JSON structure before any selected-table decode."""

        need(not self.structure_validated_labels, "JSON structure validation once")
        for label, paths in SELECTED_TABLE_PATHS.items():
            raw, stream = self._binary_stream(label)
            try:
                stats = _validate_complete_json_stream(stream, paths)
            finally:
                if stream is not raw:
                    stream.close()
                raw.close()
            self.structure_validated_labels.add(label)
            for path in paths:
                offset_key = ".".join(path)
                offset = stats["selected_array_content_offsets"][offset_key]
                need(isinstance(offset, int) and offset >= 1, "selected array byte offset")
                self.table_offsets[(label, path)] = offset
            self.structure_rows.append({"label": label, **stats})
        need(self.structure_validated_labels == set(SELECTED_TABLE_PATHS), "all selected documents structurally validated")
        return list(self.structure_rows)

    def iter_array(self, label: str, path: tuple[str, ...]) -> Iterator[Any]:
        need(label in self.structure_validated_labels, f"pin-first structure validation:{label}")
        need((label, path) in self.table_offsets, f"exact selected table path:{label}:{path}")
        raw, stream = self._binary_stream(label)
        try:
            remaining = self.table_offsets[(label, path)]
            while remaining:
                block = stream.read(min(PARSER_CHUNK_BYTES, remaining))
                need(bool(block), f"selected table offset beyond EOF:{label}:{path}")
                remaining -= len(block)
            tail = stream.read(PARSER_CHUNK_BYTES)
            need(bool(tail), f"selected table content missing:{label}:{path}")
            def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
                result: dict[str, Any] = {}
                for key, value in pairs:
                    need(key not in result, "duplicate selected-row JSON key:" + key)
                    result[key] = value
                return result

            decoder = json.JSONDecoder(
                object_pairs_hook=reject_duplicate_pairs,
                parse_constant=_reject_nonstandard_constant,
            )
            text = tail.decode("ascii")
            need(len(tail) <= PARSER_BUFFER_CAP, f"selected parser initial buffer cap:{label}")
            position = 0
            eof = False
            first = True
            while True:
                while True:
                    while position < len(text) and text[position] in " \t\r\n,":
                        position += 1
                    if position < len(text):
                        break
                    block = stream.read(PARSER_CHUNK_BYTES)
                    if not block:
                        eof = True
                        break
                    text = block.decode("ascii")
                    position = 0
                need(not eof, f"unterminated table:{label}")
                if text[position] == "]":
                    need(first, f"selected table trailing comma:{label}")
                    return
                need(text[position] != ",", f"selected table double/leading comma:{label}")
                while True:
                    try:
                        value, end = decoder.raw_decode(text, position)
                        break
                    except json.JSONDecodeError:
                        block = stream.read(PARSER_CHUNK_BYTES)
                        need(bool(block), f"truncated JSON row:{label}")
                        need(
                            len(text[position:].encode("ascii")) + len(block) <= PARSER_BUFFER_CAP,
                            f"selected parser append cap:{label}",
                        )
                        text = text[position:] + block.decode("ascii")
                        position = 0
                need(
                    len(text[position:end].encode("ascii")) <= DECODED_CANONICAL_ROW_CAP,
                    f"selected decoded row cap:{label}",
                )
                canonical_replay_row_bytes(value)
                yield value
                first = False
                position = end
                while True:
                    while position < len(text) and text[position] in " \t\r\n":
                        position += 1
                    if position < len(text):
                        break
                    block = stream.read(PARSER_CHUNK_BYTES)
                    need(bool(block), f"unterminated selected table:{label}")
                    text = block.decode("ascii")
                    position = 0
                delimiter = text[position]
                position += 1
                if delimiter == "]":
                    return
                need(delimiter == ",", f"selected table missing comma:{label}")
                while True:
                    while position < len(text) and text[position] in " \t\r\n":
                        position += 1
                    if position < len(text):
                        break
                    block = stream.read(PARSER_CHUNK_BYTES)
                    need(bool(block), f"selected table comma at EOF:{label}")
                    text = block.decode("ascii")
                    position = 0
                need(text[position] not in ",]", f"selected table trailing/double comma:{label}")
                if position > 2 * PARSER_CHUNK_BYTES:
                    text = text[position:]
                    position = 0
        finally:
            if stream is not raw:
                stream.close()
            raw.close()


def direct_rows(held: HeldInputs, label: str, key: str) -> Iterator[Any]:
    matches = [path for path in SELECTED_TABLE_PATHS[label] if path[-1] == key]
    need(len(matches) == 1, f"direct selected path resolution:{label}:{key}")
    return held.iter_array(label, matches[0])


def nested_rows(held: HeldInputs, label: str, table: str, rows_key: str = "rows") -> Iterator[Any]:
    matches = [
        path for path in SELECTED_TABLE_PATHS[label]
        if table in path and path[-1] == rows_key
    ]
    need(len(matches) == 1, f"nested selected path resolution:{label}:{table}:{rows_key}")
    return held.iter_array(label, matches[0])


class ExternalCanonicalSorter:
    """Bounded canonical-byte sorter used for replay commitments."""

    def __init__(self, directory: str, label: str, limit: int = SORT_BUFFER_LIMIT) -> None:
        self.directory = directory
        self.label = label
        self.limit = limit
        self.buffer: list[bytes] = []
        self.buffer_bytes = 0
        self.peak_buffer_bytes = 0
        self.paths: list[str] = []
        self.record_count = 0
        self.temp_bytes = 0

    def add(self, record: Any) -> None:
        line = canonical_replay_row_bytes(record) + b"\n"
        need(b"\n" not in line[:-1], "canonical record newline")
        if self.buffer and self.buffer_bytes + len(line) > self.limit:
            self._flush()
        self.buffer.append(line)
        self.buffer_bytes += len(line)
        self.peak_buffer_bytes = max(self.peak_buffer_bytes, self.buffer_bytes)
        self.record_count += 1

    def _flush(self) -> None:
        if not self.buffer:
            return
        self.buffer.sort()
        fd, path = tempfile.mkstemp(prefix=self.label + "-", suffix=".sort", dir=self.directory)
        with os.fdopen(fd, "wb") as out:
            out.writelines(self.buffer)
        size = os.stat(path, follow_symlinks=False).st_size
        self.temp_bytes += size
        self.paths.append(path)
        self.buffer.clear()
        self.buffer_bytes = 0

    def commit_unique_keyed(self) -> dict[str, Any]:
        self._flush()
        files = [open(path, "rb") for path in self.paths]
        h = hashlib.sha256()
        seen = 0
        previous: str | None = None
        try:
            for line in heapq.merge(*files):
                record = json.loads(line)
                need(isinstance(record, list) and len(record) >= 2 and isinstance(record[0], str), f"sort key:{self.label}")
                need(record[0] != previous, f"duplicate sorted key:{self.label}:{record[0]}")
                previous = record[0]
                h.update(line)
                seen += 1
        finally:
            for file in files:
                file.close()
        need(seen == self.record_count, f"sort record count:{self.label}")
        return {
            "record_count": seen,
            "wire": "canonical_json(record)+LF sorted bytewise",
            "sha256": h.hexdigest(),
            "chunk_count": len(self.paths),
            "sort_buffer_limit_bytes": self.limit,
            "peak_buffer_payload_bytes": self.peak_buffer_bytes,
            "temporary_bytes": self.temp_bytes,
            "measured_RSS_bytes": None,
        }


def _realpath_is_outside(candidate: str, protected: str) -> bool:
    candidate_real = os.path.realpath(candidate)
    protected_real = os.path.realpath(protected)
    try:
        return os.path.commonpath((candidate_real, protected_real)) != protected_real
    except ValueError:
        return True


class SafeExternalTempDirectory:
    """Private spill directory rooted outside the real deliverables tree."""

    def __init__(self) -> None:
        self.root_fd = -1
        self.created_fd = -1
        self.temp: tempfile.TemporaryDirectory[str] | None = None
        self.root_real = ""
        self.created_real = ""
        self.root_before: os.stat_result | None = None
        self.created_before: os.stat_result | None = None
        self.audit: dict[str, Any] = {}

    def __enter__(self) -> str:
        deliverables_real = os.path.realpath(os.fspath(INPUT_DIRECTORY))
        root_text = tempfile.gettempdir()
        root_lstat = os.lstat(root_text)
        root_stat = os.stat(root_text)
        need(stat.S_ISDIR(root_lstat.st_mode), "OS temp root directory")
        need(not stat.S_ISLNK(root_lstat.st_mode), "OS temp root symlink")
        need(_directory_identity(root_lstat) == _directory_identity(root_stat), "OS temp root follow identity")
        self.root_real = os.path.realpath(root_text)
        need(_realpath_is_outside(self.root_real, deliverables_real), "OS temp root inside deliverables")
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        self.root_fd = os.open(self.root_real, flags)
        self.root_before = os.fstat(self.root_fd)
        need(_directory_identity(self.root_before) == _directory_identity(root_stat), "OS temp root open race")

        self.temp = tempfile.TemporaryDirectory(prefix="cm2-af4p1-sort-", dir=self.root_real)
        created = self.temp.name
        created_lstat = os.lstat(created)
        need(stat.S_ISDIR(created_lstat.st_mode), "created spill directory")
        need(not stat.S_ISLNK(created_lstat.st_mode), "created spill symlink")
        self.created_real = os.path.realpath(created)
        need(_realpath_is_outside(self.created_real, deliverables_real), "created spill inside deliverables")
        self.created_fd = os.open(self.created_real, flags)
        self.created_before = os.fstat(self.created_fd)
        need(_directory_identity(created_lstat) == _directory_identity(self.created_before), "created spill open race")
        parent = os.stat("..", dir_fd=self.created_fd, follow_symlinks=False)
        need(_directory_identity(parent) == _directory_identity(self.root_before), "created spill parent/root mismatch")
        root_after_create = os.stat(self.root_real, follow_symlinks=False)
        need(_directory_identity(root_after_create) == _directory_identity(self.root_before), "temp root replaced during create")
        self.audit = {
            "OS_temp_root_realpath_outside_deliverables": True,
            "OS_temp_root_non_symlink": True,
            "OS_temp_root_held_identity_stable": True,
            "created_temp_directory_realpath_outside_deliverables": True,
            "created_temp_directory_non_symlink": True,
            "created_temp_directory_parent_is_held_root": True,
            "created_temp_directory_removed": False,
        }
        return self.created_real

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        try:
            if self.created_fd >= 0 and self.created_before is not None:
                held_after = os.fstat(self.created_fd)
                path_after = os.stat(self.created_real, follow_symlinks=False)
                need(_directory_identity(held_after) == _directory_identity(self.created_before), "held spill directory changed")
                need(_directory_identity(path_after) == _directory_identity(self.created_before), "spill directory replaced")
                parent = os.stat("..", dir_fd=self.created_fd, follow_symlinks=False)
                need(self.root_before is not None and _directory_identity(parent) == _directory_identity(self.root_before), "spill parent changed")
        finally:
            if self.created_fd >= 0:
                os.close(self.created_fd)
                self.created_fd = -1
            if self.temp is not None:
                self.temp.cleanup()
            if self.root_fd >= 0:
                try:
                    root_after = os.fstat(self.root_fd)
                    need(self.root_before is not None and _directory_identity(root_after) == _directory_identity(self.root_before), "held temp root changed")
                    root_path_after = os.stat(self.root_real, follow_symlinks=False)
                    need(_directory_identity(root_path_after) == _directory_identity(root_after), "temp root path replaced")
                finally:
                    os.close(self.root_fd)
                    self.root_fd = -1
        need(not os.path.lexists(self.created_real), "spill directory cleanup")
        self.audit["created_temp_directory_removed"] = True


def _insert(mapping: dict[str, Any], key: str, value: Any, label: str) -> None:
    need(isinstance(key, str) and key != "", f"key:{label}")
    need(key not in mapping, f"duplicate:{label}:{key}")
    mapping[key] = value


def _set_equal(left: Iterable[str], right: Iterable[str], label: str) -> None:
    a, b = set(left), set(right)
    need(not (a - b), f"forward anti-join:{label}:{len(a-b)}")
    need(not (b - a), f"reverse anti-join:{label}:{len(b-a)}")


def _load_preserved_geometry(held: HeldInputs) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    counts: Counter[str] = Counter()
    for row in direct_rows(held, "R174", "resolved_3d_occurrence_rows"):
        need(isinstance(row, list) and len(row) == 21, "R174 packed row")
        item = {"family": "ROUND174_RESOLVED", "row_sha256": replay_row_digest(row), "box": row[4]}
        _insert(result, row[0], item, "R174 geometry")
        counts[item["family"]] += 1
    for row in direct_rows(held, "R179", "resolved_3d_child_rows"):
        need(isinstance(row, list) and len(row) == 20, "R179 packed row")
        item = {"family": "ROUND179_RESOLVED", "row_sha256": replay_row_digest(row), "box": row[6]}
        _insert(result, row[0], item, "R179 geometry")
        counts[item["family"]] += 1
    for row in nested_rows(held, "R204", "formal_local_open_3D_region_ledger"):
        row_digest(row)
        item = {"family": "ROUND204_REGION", "row_sha256": row["row_sha256"], "box": row["leaf_exact_box"]}
        _insert(result, row["region_row_id"], item, "R204 geometry")
        counts[item["family"]] += 1
    for row in nested_rows(held, "R208", "formal_local_open_3D_signature_ledger"):
        row_digest(row)
        item = {"family": "ROUND208_REGION", "row_sha256": row["row_sha256"], "box": row["Round182_leaf_box"]}
        _insert(result, row["region_row_id"], item, "R208 geometry")
        counts[item["family"]] += 1
    need(counts == Counter(dict(PRESERVED_COUNTS)), f"preserved geometry census:{counts}")
    return result


def _load_r266_expanded(held: HeldInputs, geometry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    geometry_seen: set[str] = set()
    for row in nested_rows(held, "R266", "formal_post_Round266_expanded_occurrence_frontier_ledger"):
        row_digest(row)
        geometry_id = row["source_geometry_row_id"]
        source = geometry.get(geometry_id)
        need(source is not None, "R266 geometry forward join")
        need(source["row_sha256"] == row["source_geometry_row_sha256"], "R266 geometry SHA")
        need(source["family"] == row["occurrence_source"], "R266 geometry class")
        need(row["local_occurrence_row_id"] == geometry_id, "R266 occurrence/geometry identity")
        geometry_seen.add(geometry_id)
        _insert(result, row["post_Round266_expanded_occurrence_frontier_row_id"], {
            "row_sha256": row["row_sha256"],
            "member_id": row["local_occurrence_row_id"],
            "geometry_id": geometry_id,
            "geometry_sha256": row["source_geometry_row_sha256"],
            "family": row["occurrence_source"],
            "box": source["box"],
        }, "R266 expanded")
    _set_equal(geometry_seen, geometry, "geometry/R266 expanded")
    need(len(result) == 126_468, "R266 expanded count")
    return result


def _load_preserved_registry(held: HeldInputs, expanded: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    by_row: dict[str, dict[str, Any]] = {}
    by_member: dict[str, dict[str, Any]] = {}
    expanded_seen: set[str] = set()
    for row in direct_rows(held, "R294_REGISTRY", "rows"):
        if row.get("registry_entry_kind") != "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE":
            continue
        row_digest(row)
        source = expanded.get(row["source_row_id"])
        need(source is not None, "R294/R266 forward join")
        need(source["row_sha256"] == row["source_row_sha256"], "R294/R266 SHA")
        need(source["member_id"] == row["registry_occurrence_id"], "R294/R266 member")
        need(source["geometry_id"] == row["source_geometry_row_id"], "R294 geometry ID")
        need(source["geometry_sha256"] == row["source_geometry_row_sha256"], "R294 geometry SHA")
        expanded_seen.add(row["source_row_id"])
        value = {
            "row_id": row["Round294_occurrence_registry_row_id"],
            "row_sha256": row["row_sha256"],
            "member_id": row["registry_occurrence_id"],
            "family": source["family"],
            "box": source["box"],
        }
        _insert(by_row, value["row_id"], value, "R294 preserved row")
        _insert(by_member, value["member_id"], value, "R294 preserved member")
    _set_equal(expanded_seen, expanded, "R266 expanded/R294 preserved")
    need(len(by_row) == len(by_member) == 126_468, "R294 preserved count")
    return by_row, by_member


def _load_preserved_b0(held: HeldInputs, registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    source_seen: set[str] = set()
    for row in direct_rows(held, "B0", "member_support_source_rows"):
        source = registry.get(row.get("primary_source_row_id"))
        if source is None:
            continue
        row_digest(row)
        need(row["primary_source_package"] == "R294", "B0 preserved package")
        need(row["primary_source_row_sha256"] == source["row_sha256"], "B0/R294 SHA")
        need(row["member_id"] == source["member_id"], "B0/R294 member")
        source_seen.add(row["primary_source_row_id"])
        _insert(result, row["member_id"], {
            "family": source["family"], "box": source["box"],
            "b0_row_id": row["Round306B0_member_support_source_row_id"],
        }, "B0 preserved member")
    _set_equal(source_seen, registry, "R294 preserved/B0")
    need(len(result) == 126_468, "B0 preserved count")
    return result


def _load_non_graph_sources(held: HeldInputs) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    counts: Counter[str] = Counter()
    for row in nested_rows(held, "R245", "formal_retained_stratum_node_ledger"):
        if row["stratum_kind"] != "WHOLE_ROOT_ZERO_ABSENCE_BULK":
            continue
        row_digest(row)
        family = "R245_WHOLE_ROOT_ZERO_ABSENCE_BULK"
        _insert(result, row["retained_stratum_node_id"], {
            "package": "R245", "row_sha256": row["row_sha256"], "family": family,
            "retained_id": row["Round179_retained_child_row_id"],
            "interface_id": row["Round220_split_interface_id"],
        }, "R245 non-graph")
        counts[family] += 1
    for row in nested_rows(held, "R246", "formal_new_whole_signature_retained_stratum_node_ledger"):
        row_digest(row)
        family = "R246_WHOLE_ORIGIN_SINGLE_SIGNATURE_RETAINED_BULK"
        _insert(result, row["retained_stratum_node_id"], {
            "package": "R246", "row_sha256": row["row_sha256"], "family": family,
            "retained_id": row["Round179_retained_child_row_id"],
            "interface_id": row["Round220_split_interface_id"],
            "promotion_id": row["Round232_whole_origin_promotion_row_id"],
        }, "R246 non-graph")
        counts[family] += 1
    for row in nested_rows(held, "R247", "formal_new_crossing_and_source_seam_retained_stratum_node_ledger"):
        row_digest(row)
        classification = row["source_classification"]
        if classification == "CROSSING_TIME":
            family = "R247_CROSSING_TIME_WHOLE_SIGNATURE_RETAINED_BULK"
        elif classification == "SOURCE_CHART_SEAM":
            family = "R247_SOURCE_CHART_SEAM_WHOLE_SIGNATURE_RETAINED_BULK"
        else:
            raise PreflightBlocked("R247 source classification")
        _insert(result, row["retained_stratum_node_id"], {
            "package": "R247", "row_sha256": row["row_sha256"], "family": family,
            "retained_id": row["Round179_retained_child_row_id"],
            "interface_id": row["Round220_split_interface_id"],
            "promotion_id": row["source_whole_origin_promotion_row_id"],
        }, "R247 non-graph")
        counts[family] += 1
    allowed = {"ROUND234_RESOLVED_DESCENDANT", "ROUND236_CROSSING_DISCHARGE_BULK"}
    for row in nested_rows(held, "R248", "formal_wall_positive_volume_bulk_ledger"):
        kind = row["source_partition_kind"]
        if kind not in allowed:
            continue
        row_digest(row)
        family = "R248_" + kind
        need(row["exact_positive_3D_box"] is not None, "R248 exact box")
        _insert(result, row["wall_bulk_node_id"], {
            "package": "R248", "row_sha256": row["row_sha256"], "family": family,
            "interface_id": row["Round220_split_interface_id"],
            "source_partition_id": row["source_partition_row_id"],
            "box": row["exact_positive_3D_box"],
        }, "R248 non-graph")
        counts[family] += 1
    need(counts == Counter(dict(NON_GRAPH_COUNTS)), f"non-graph source census:{counts}")
    need(len(result) == 17_828, "non-graph total")
    return result


def _validate_non_graph_lineage(held: HeldInputs, nodes: dict[str, dict[str, Any]]) -> dict[str, int]:
    retained_need = {v["retained_id"] for v in nodes.values() if "retained_id" in v}
    need(
        len(retained_need) == sum("retained_id" in value for value in nodes.values()),
        "duplicate non-graph source/retained edge",
    )
    retained: dict[str, list[Any]] = {}
    for row in direct_rows(held, "R179", "retained_3d_child_rows"):
        need(isinstance(row, list) and len(row) == 13, "R179 retained packed row")
        if row[0] in retained_need:
            _insert(retained, row[0], row[6], "R179 retained source")
    _set_equal(retained, retained_need, "non-graph/R179 retained")
    for node in nodes.values():
        if "retained_id" in node:
            node["box"] = retained[node["retained_id"]]

    interface_need = {v["interface_id"] for v in nodes.values()}
    interface_seen: set[str] = set()
    interface_retained: dict[str, set[str]] = defaultdict(set)
    for row in nested_rows(held, "R220", "one_step_split_interface_rows"):
        need(isinstance(row, list) and len(row) == 20, "R220 interface packed row")
        if row[0] in interface_need:
            need(row[0] not in interface_seen, "duplicate R220 interface")
            interface_seen.add(row[0])
            for kind_index, id_index in ((7, 8), (9, 10)):
                if row[kind_index] == "RETAINED":
                    interface_retained[row[0]].add(row[id_index])
    _set_equal(interface_seen, interface_need, "source/R220 interface")
    for node in nodes.values():
        if "retained_id" in node:
            need(node["retained_id"] in interface_retained[node["interface_id"]], "R220 retained incidence")

    r245_interfaces = {v["interface_id"] for v in nodes.values() if v["package"] == "R245"}
    need(
        len(r245_interfaces) == sum(v["package"] == "R245" for v in nodes.values()),
        "duplicate R245 source/interface edge",
    )
    r242_seen: set[str] = set()
    r242_row_ids: set[str] = set()
    for row in nested_rows(held, "R242", "formal_zero_absence_base_partition_ledger"):
        interface = row["Round220_split_interface_id"]
        if interface in r245_interfaces:
            row_digest(row)
            need(row["strict_zero_absence_on_closed_box"] is True, "R242 zero absence")
            row_id = row["zero_absence_leaf_row_id"]
            need(row_id not in r242_row_ids, "duplicate R242 zero-absence row")
            r242_row_ids.add(row_id)
            r242_seen.add(interface)
    _set_equal(r242_seen, r245_interfaces, "R245/R242 zero absence")

    def validate_promotions(label: str, table: str, package: str) -> int:
        wanted: dict[str, dict[str, Any]] = {}
        for value in nodes.values():
            if value["package"] == package:
                _insert(wanted, value["promotion_id"], value, f"{package} promotion source edge")
        seen: set[str] = set()
        for row in direct_rows(held, label, table):
            key = row["whole_origin_promotion_row_id"]
            node = wanted.get(key)
            if node is None:
                continue
            if "row_sha256" in row:
                row_digest(row)
            need(key not in seen, f"duplicate {label} promotion")
            seen.add(key)
            need(row["Round179_retained_child_row_id"] == node["retained_id"], f"{label} retained join")
            need(row["Round220_split_interface_id"] == node["interface_id"], f"{label} interface join")
        _set_equal(seen, wanted, f"{package}/{label} promotion")
        return len(seen)

    r232_count = validate_promotions("R232", "whole_origin_promotion_rows", "R246")
    # R247 contains two disjoint promotion sources, so replay R237 and R238
    # separately instead of treating either one as authority for all 504 rows.
    r237_wanted: dict[str, dict[str, Any]] = {}
    r238_wanted: dict[str, dict[str, Any]] = {}
    for value in nodes.values():
        if value["family"].startswith("R247_CROSSING"):
            _insert(r237_wanted, value["promotion_id"], value, "R237 promotion source edge")
        elif value["family"].startswith("R247_SOURCE"):
            _insert(r238_wanted, value["promotion_id"], value, "R238 promotion source edge")
    seen237: set[str] = set()
    for row in direct_rows(held, "R237", "whole_origin_promotion_rows"):
        key = row["whole_origin_promotion_row_id"]
        if key in r237_wanted:
            if "row_sha256" in row:
                row_digest(row)
            node = r237_wanted[key]
            need(row["Round179_retained_child_row_id"] == node["retained_id"], "R237 retained join")
            need(row["Round220_split_interface_id"] == node["interface_id"], "R237 interface join")
            need(key not in seen237, "duplicate R237 promotion")
            seen237.add(key)
    seen238: set[str] = set()
    for row in direct_rows(held, "R238", "whole_origin_promotion_rows"):
        key = row["whole_origin_promotion_row_id"]
        if key in r238_wanted:
            if "row_sha256" in row:
                row_digest(row)
            node = r238_wanted[key]
            need(row["Round179_retained_child_row_id"] == node["retained_id"], "R238 retained join")
            need(row["Round220_split_interface_id"] == node["interface_id"], "R238 interface join")
            need(key not in seen238, "duplicate R238 promotion")
            seen238.add(key)
    _set_equal(seen237, r237_wanted, "R247 crossing/R237")
    _set_equal(seen238, r238_wanted, "R247 seam/R238")

    r234_wanted: dict[str, dict[str, Any]] = {}
    for value in nodes.values():
        if value["family"] == "R248_ROUND234_RESOLVED_DESCENDANT":
            _insert(r234_wanted, value["source_partition_id"], value, "R234 source edge")
    seen234: set[str] = set()
    for row in direct_rows(held, "R234", "resolved_descendant_rows"):
        node = r234_wanted.get(row["materialized_row_id"])
        if node is None:
            continue
        if "row_sha256" in row:
            row_digest(row)
        need(row["materialized_row_id"] not in seen234, "duplicate R234 resolved row")
        need(row["box"] == node["box"], "R234/R248 box")
        need(row["Round220_split_interface_id"] == node["interface_id"], "R234/R248 interface")
        seen234.add(row["materialized_row_id"])
    _set_equal(seen234, r234_wanted, "R248/R234")

    r236_wanted: dict[str, dict[str, Any]] = {}
    for value in nodes.values():
        if value["family"] == "R248_ROUND236_CROSSING_DISCHARGE_BULK":
            _insert(r236_wanted, value["source_partition_id"], value, "R236 source edge")
    seen236: set[str] = set()
    for row in direct_rows(held, "R236", "crossing_dependency_discharge_rows"):
        node = r236_wanted.get(row["crossing_dependency_discharge_row_id"])
        if node is None:
            continue
        if "row_sha256" in row:
            row_digest(row)
        need(row["crossing_dependency_discharge_row_id"] not in seen236, "duplicate R236 discharge row")
        need(row["Round220_split_interface_id"] == node["interface_id"], "R236/R248 interface")
        seen236.add(row["crossing_dependency_discharge_row_id"])
    _set_equal(seen236, r236_wanted, "R248/R236")
    return {
        "R179_retained": len(retained), "R220_interfaces": len(interface_seen),
        "R242_interfaces": len(r242_seen), "R242_rows": len(r242_row_ids),
        "R232_promotions": r232_count,
        "R237_promotions": len(seen237), "R238_promotions": len(seen238),
        "R234_rows": len(seen234), "R236_rows": len(seen236),
    }


def _load_non_graph_r266_b0(held: HeldInputs, nodes: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    valid: dict[str, dict[str, Any]] = {}
    for row in nested_rows(held, "R266", "formal_post_Round266_valid_virtual_node_frontier_ledger"):
        member = row["valid_virtual_stratum_node_id"]
        if member not in nodes:
            continue
        row_digest(row)
        _insert(valid, member, {
            "row_id": row["post_Round266_valid_virtual_node_frontier_row_id"],
            "row_sha256": row["row_sha256"],
        }, "R266 valid non-graph")
    _set_equal(valid, nodes, "non-graph source/R266 valid")

    components: dict[str, dict[str, Any]] = {}
    member_seen: set[str] = set()
    for row in nested_rows(held, "R266", "formal_post_Round266_component_member_frontier_ledger"):
        member = row["component_member_id"]
        if member not in nodes:
            continue
        need(row["component_member_kind"] == "VALID_VIRTUAL_STRATUM", "R266 component kind")
        row_digest(row)
        frontier = valid[member]
        need(row["source_Round266_frontier_row_id"] == frontier["row_id"], "R266 component/valid ID")
        need(row["source_Round266_frontier_row_sha256"] == frontier["row_sha256"], "R266 component/valid SHA")
        need(member not in member_seen, "duplicate R266 non-graph member")
        member_seen.add(member)
        _insert(components, row["post_Round266_component_member_frontier_row_id"], {
            "row_sha256": row["row_sha256"], "member_id": member,
        }, "R266 non-graph component")
    _set_equal(member_seen, nodes, "R266 valid/component")

    result: dict[str, dict[str, Any]] = {}
    component_seen: set[str] = set()
    for row in direct_rows(held, "B0", "member_support_source_rows"):
        source = components.get(row.get("primary_source_row_id"))
        if source is None:
            continue
        row_digest(row)
        node = nodes[source["member_id"]]
        need(row["primary_source_package"] == "R266", "B0 non-graph package")
        need(row["primary_source_row_sha256"] == source["row_sha256"], "B0/R266 SHA")
        need(row["member_id"] == source["member_id"], "B0/R266 member")
        inherited_package = row["inherited_virtual_source_package"]
        if inherited_package is not None:
            need(inherited_package == node["package"], "B0 inherited package")
            need(row["inherited_virtual_source_row_id"] == row["member_id"], "B0 inherited row ID")
            need(row["inherited_virtual_source_row_sha256"] == node["row_sha256"], "B0 inherited SHA")
        else:
            # B0 deliberately leaves the R248 inherited convenience columns
            # null; the exact identity still closes through component -> valid
            # frontier -> the directly replayed R248 node row.
            need(node["package"] == "R248", "null inherited source only for R248")
            need(row["inherited_virtual_source_row_id"] is None, "null R248 inherited row")
            need(row["inherited_virtual_source_row_sha256"] is None, "null R248 inherited SHA")
        component_seen.add(row["primary_source_row_id"])
        _insert(result, row["member_id"], {
            "family": node["family"], "box": node["box"],
            "b0_row_id": row["Round306B0_member_support_source_row_id"],
        }, "B0 non-graph member")
    _set_equal(component_seen, components, "R266 component/B0")
    need(len(result) == 17_828, "B0 non-graph total")
    return result


def _alias_replay(held: HeldInputs, registry_by_row: dict[str, Any], registry_by_member: dict[str, Any], sorter: ExternalCanonicalSorter) -> dict[str, Any]:
    total = 0
    preserved = 0
    residual = 0
    source_counts: Counter[str] = Counter()
    representation_counts: Counter[str] = Counter()
    owner_keys: set[tuple[str, str]] = set()
    preserved_targets: set[str] = set()
    r294_targets: set[str] = set()
    for row in direct_rows(held, "R294_ALIAS", "rows"):
        row_digest(row)
        total += 1
        owner = (row["alias_source_kind"], row["source_representation_id"])
        need(owner not in owner_keys, "R294 duplicate alias owner")
        owner_keys.add(owner)
        sorter.add(["R294\u0000" + owner[0] + "\u0000" + owner[1], row["target_registry_occurrence_id"], row["support_representation_kind"]])
        target = registry_by_member.get(row["target_registry_occurrence_id"])
        if target is None:
            residual += 1
            continue
        preserved += 1
        need(row["target_registry_entry_kind"] == "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE", "R294 alias target kind")
        preserved_targets.add(target["member_id"])
        r294_targets.add(target["member_id"])
        source_counts[target["family"]] += 1
        support_kind = row["support_representation_kind"]
        if support_kind == "EXACT_EQUAL_SUPPORT_ENVELOPE_ALIAS_EVIDENCE":
            representation_counts["TPS_EXACT_EQUAL"] += 1
        elif support_kind == "EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER":
            representation_counts["TPS_INCLUSION_SUBCOVER"] += 1
        elif support_kind == "EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL":
            representation_counts["T2PS_REFINED_SUBCOVER"] += 1
        else:
            raise PreflightBlocked("R294 alias representation kind")
    need(total == 46_288 and preserved == 39_000 and residual == 7_288, "R294 alias dispatch")
    need(source_counts == Counter(dict(ALIAS_SOURCE_CLASS_COUNTS)), f"alias source counts:{source_counts}")
    need(representation_counts == Counter(dict(ALIAS_REPRESENTATION_COUNTS)), f"alias representation counts:{representation_counts}")
    need(len(owner_keys) == 46_288 and len(preserved_targets) == 37_388, "R294 alias uniqueness")

    r295_owners: set[str] = set()
    r295_targets: set[str] = set()
    r295_count = 0
    for row in direct_rows(held, "R295A_ALIAS", "rows"):
        row_digest(row)
        r295_count += 1
        target = registry_by_row.get(row["target_Round294_occurrence_registry_row_id"])
        need(target is not None, "R295A registry row join")
        need(row["target_Round294_occurrence_registry_row_sha256"] == target["row_sha256"], "R295A registry SHA")
        need(row["target_Round294_registry_occurrence_id"] == target["member_id"], "R295A target member")
        need(target["family"] == "ROUND179_RESOLVED", "R295A target class")
        owner = row["source_Round179_retained_child_row_id"]
        need(owner not in r295_owners, "R295A duplicate source owner")
        r295_owners.add(owner)
        r295_targets.add(target["member_id"])
        sorter.add(["R295A\u0000" + owner, target["member_id"], "ADJACENT_POSITIVE_T_CONTINUATION"])
    need(r295_count == len(r295_owners) == len(r295_targets) == 276, "R295A alias count")
    need(not (r294_targets & r295_targets), "R294/R295A target overlap")
    need(len(owner_keys) + len(r295_owners) == 46_564, "global alias owner count")
    return {
        "R294_total": total, "R294_preserved": preserved, "R294_residual": residual,
        "R294_unique_source_owners": len(owner_keys),
        "R294_unique_preserved_targets": len(preserved_targets),
        "R295A_count": r295_count, "R295A_unique_source_owners": len(r295_owners),
        "namespaced_global_owner_count": len(owner_keys) + len(r295_owners),
        "target_intersection": len(r294_targets & r295_targets),
        "preserved_source_class_counts": dict(sorted(source_counts.items())),
        "preserved_representation_counts": dict(sorted(representation_counts.items())),
    }


def _obligation_replay(held: HeldInputs, sorter: ExternalCanonicalSorter) -> dict[str, int]:
    counts: Counter[str] = Counter()
    r204_sheets: set[str] = set()
    for row in nested_rows(held, "R204", "formal_2D_sheet_lineage", "target_sheet_rows"):
        row_digest(row)
        need(row["sheet_row_id"] not in r204_sheets, "duplicate R204 target sheet")
        r204_sheets.add(row["sheet_row_id"])
        sorter.add(["A1_R204_TARGET_SHEET\u0000" + row["sheet_row_id"], row["row_sha256"]])
        counts["A1_R204_TARGET_SHEET"] += 1
    r204_curves: set[str] = set()
    referenced_sheets: set[str] = set()
    for row in nested_rows(held, "R204", "formal_1D_boundary_and_intersection_lineage"):
        if not row["geometry_kind"].startswith("TARGET_GRAPH_"):
            continue
        row_digest(row)
        need(row["edge_row_id"] not in r204_curves, "duplicate R204 curve")
        r204_curves.add(row["edge_row_id"])
        refs = set(row["incident_sheet_row_ids"]) & r204_sheets
        need(bool(refs), "R204 curve/target-sheet join")
        referenced_sheets.update(refs)
        sorter.add(["A2_R204_SOURCE_TARGET_CURVE\u0000" + row["edge_row_id"], row["row_sha256"]])
        counts["A2_R204_SOURCE_TARGET_CURVE"] += 1
    _set_equal(referenced_sheets, r204_sheets, "R204 target sheet/target-graph curves")
    referenced_curves: set[str] = set()
    for row in nested_rows(held, "R204", "formal_0D_endpoint_and_corner_lineage"):
        if row["geometry_kind"] != "TARGET_GRAPH_P_S_POINT":
            continue
        row_digest(row)
        refs = set(row["incident_1D_row_ids"]) & r204_curves
        need(bool(refs), "R204 endpoint/curve join")
        referenced_curves.update(refs)
        sorter.add(["A2_R204_SOURCE_TARGET_ENDPOINT\u0000" + row["point_row_id"], row["row_sha256"]])
        counts["A2_R204_SOURCE_TARGET_ENDPOINT"] += 1
    _set_equal(referenced_curves, r204_curves, "R204 target-graph curve/endpoints")

    r211_sheets: dict[str, str] = {}
    for row in nested_rows(held, "R211", "formal_2D_sheet_owner_ledger"):
        row_digest(row)
        _insert(r211_sheets, row["sheet_row_id"], row["row_sha256"], "R211 sheet")
        sorter.add(["A1_R211_OWNER_SHEET\u0000" + row["sheet_row_id"], row["row_sha256"]])
        counts["A1_R211_OWNER_SHEET"] += 1
    r211_curves: dict[str, str] = {}
    sheet_refs: set[str] = set()
    for row in nested_rows(held, "R211", "formal_1D_curve_incidence_owner_ledger"):
        row_digest(row)
        need(row["sheet_row_id"] in r211_sheets, "R211 curve/sheet")
        need(row["sheet_row_sha256"] == r211_sheets[row["sheet_row_id"]], "R211 curve/sheet SHA")
        sheet_refs.add(row["sheet_row_id"])
        _insert(r211_curves, row["curve_row_id"], row["row_sha256"], "R211 curve")
        sorter.add(["A2_R211_OWNER_CURVE\u0000" + row["curve_row_id"], row["row_sha256"]])
        counts["A2_R211_OWNER_CURVE"] += 1
    # 408 owner sheets carry no boundary-curve obligation.  As with R204,
    # reference integrity is exact but reverse incidence is not asserted.
    need(sheet_refs <= set(r211_sheets), "R211 curve sheet reference anti-join")
    curve_refs: set[str] = set()
    endpoint_ids: set[str] = set()
    for row in nested_rows(held, "R211", "formal_0D_endpoint_incidence_owner_ledger"):
        row_digest(row)
        need(row["curve_row_id"] in r211_curves, "R211 endpoint/curve")
        need(row["curve_row_sha256"] == r211_curves[row["curve_row_id"]], "R211 endpoint/curve SHA")
        need(row["endpoint_row_id"] not in endpoint_ids, "duplicate R211 endpoint")
        endpoint_ids.add(row["endpoint_row_id"])
        curve_refs.add(row["curve_row_id"])
        sorter.add(["A2_R211_OWNER_ENDPOINT\u0000" + row["endpoint_row_id"], row["row_sha256"]])
        counts["A2_R211_OWNER_ENDPOINT"] += 1
    _set_equal(curve_refs, r211_curves, "R211 curve/endpoint")
    need(counts == Counter(dict(A1_A2_COUNTS)), f"A1/A2 source census:{counts}")
    return dict(sorted(counts.items()))


def full_replay() -> dict[str, Any]:
    document = contract_document()
    validate_contract(document)
    held = HeldInputs()
    with held:
        structure_rows = held.validate_selected_documents()
        geometry = _load_preserved_geometry(held)
        expanded = _load_r266_expanded(held, geometry)
        registry_by_row, registry_by_member = _load_preserved_registry(held, expanded)
        preserved = _load_preserved_b0(held, registry_by_row)
        # Geometry and expanded maps are no longer needed after all reverse
        # anti-joins have closed.
        del geometry, expanded

        non_graph_nodes = _load_non_graph_sources(held)
        lineage_counts = _validate_non_graph_lineage(held, non_graph_nodes)
        non_graph = _load_non_graph_r266_b0(held, non_graph_nodes)

        _set_equal(preserved.keys(), registry_by_member.keys(), "preserved B0/member registry")
        need(not (set(preserved) & set(non_graph)), "scope family overlap")
        need(len(preserved) + len(non_graph) == 144_296, "exact replay scope")

        safe_temp = SafeExternalTempDirectory()
        with safe_temp as tempdir:
            member_sorter = ExternalCanonicalSorter(tempdir, "member-blueprint")
            family_counts: Counter[str] = Counter()
            for member, value in preserved.items():
                family_counts[value["family"]] += 1
                member_sorter.add([
                    member, value["family"],
                    "R" + value["family"].split("_")[0][5:] + "_PRESERVED_BLUEPRINT" if value["family"].startswith("ROUND") else value["family"],
                    digest(value["box"]), value["b0_row_id"],
                ])
            for member, value in non_graph.items():
                family_counts[value["family"]] += 1
                member_sorter.add([member, value["family"], value["family"] + "_BLUEPRINT", digest(value["box"]), value["b0_row_id"]])
            member_commitment = member_sorter.commit_unique_keyed()
            need(member_commitment["record_count"] == 144_296, "member commitment count")

            alias_sorter = ExternalCanonicalSorter(tempdir, "alias-dispatch")
            alias = _alias_replay(held, registry_by_row, registry_by_member, alias_sorter)
            alias_commitment = alias_sorter.commit_unique_keyed()
            need(alias_commitment["record_count"] == 46_564, "alias commitment count")

            obligation_sorter = ExternalCanonicalSorter(tempdir, "A1-A2")
            obligation_counts = _obligation_replay(held, obligation_sorter)
            obligation_commitment = obligation_sorter.commit_unique_keyed()
            need(obligation_commitment["record_count"] == 80_092, "obligation commitment count")
        temp_directory_audit = dict(safe_temp.audit)
        need(temp_directory_audit["created_temp_directory_removed"] is True, "spill cleanup audit")

        held.finalize()
        pin_rows = list(held.rows)
        final_stable = held.final_identity_stable

    fine_expected = Counter(dict(PRESERVED_COUNTS)) + Counter(dict(NON_GRAPH_COUNTS))
    need(family_counts == fine_expected, f"full scope fine census:{family_counts}")
    body = {
        "schema": SCHEMA + ".full-replay-result.v1",
        "status": REPLAY_STATUS,
        "contract_digest_sha256": digest(document),
        "input_pin_set_sha256": digest(_pin_documents()),
        "input_count": len(pin_rows),
        "input_total_bytes": sum(row["exact_size"] for row in pin_rows),
        "all_inputs_two_pass_sha256_verified": True,
        "held_fd_and_path_identity_stable_through_replay": final_stable,
        "upstream_python_imported_or_executed": False,
        "JSON_structure_replay": {
            "document_count": len(structure_rows),
            "selected_table_path_count": sum(row["selected_path_count"] for row in structure_rows),
            "all_documents_validated_to_EOF": True,
            "duplicate_object_key_count": 0,
            "all_selected_paths_exactly_once": True,
            "selected_offsets_derived_from_exact_structural_paths": True,
            "raw_marker_search_used": False,
            "document_structure_rows_sha256": digest(structure_rows),
        },
        "exact_scope": {
            "preserved": len(preserved), "non_graph": len(non_graph),
            "total": len(preserved) + len(non_graph),
            "fine_counts": dict(sorted(family_counts.items())),
            "all_identity_join_forward_antijoins": 0,
            "all_identity_join_reverse_antijoins": 0,
            "duplicate_member_ids": 0,
        },
        "lineage_replay_counts": lineage_counts,
        "alias_dispatch": alias,
        "A1_A2_obligation_counts": obligation_counts,
        "commitments": {
            "member_source_AST_blueprint_stream": member_commitment,
            "alias_dispatch_stream": alias_commitment,
            "A1_A2_obligation_stream": obligation_commitment,
            "static_source_blueprints_sha256": digest(AST_BLUEPRINTS),
        },
        "resource_observation": {
            "bounded_external_sort_buffer_limit_bytes": SORT_BUFFER_LIMIT,
            "decoded_and_canonical_row_cap_bytes": DECODED_CANONICAL_ROW_CAP,
            "parser_buffer_cap_bytes": PARSER_BUFFER_CAP,
            "parser_chunk_bytes": PARSER_CHUNK_BYTES,
            "safe_external_temp_directory": temp_directory_audit,
            "measured_RSS_bytes": None,
            "RSS_claimed": False,
        },
        "remaining_blocker_count": 6,
        "remaining_blockers_sha256": digest(BLOCKERS),
        "formal_credit": 0,
        "B1A": "BLOCKED",
        "B2": "NOT_AUTHORIZED",
        "D02": "BLOCKED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**body, "replay_result_digest_sha256": digest(body)}


def _set_path(doc: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    cursor: Any = doc
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def semantic_mutations() -> list[Mutation]:
    def setter(path: tuple[Any, ...], value: Any) -> Callable[[dict[str, Any]], None]:
        return lambda doc: _set_path(doc, path, value)
    return [
        ("schema", setter(("schema",), SCHEMA + ".bad")),
        ("status", setter(("status",), "PASS_FORMAL")),
        ("seal", setter(("sealed",), False)),
        ("artifact", setter(("artifact_kind",), "FORMAL_CONSTRUCTOR")),
        ("scope", setter(("scope", "exact_scope_member_count"), 144_295)),
        ("preserved", setter(("scope", "preserved_member_count"), 126_467)),
        ("non graph", setter(("scope", "non_graph_member_count"), 17_827)),
        ("fine", setter(("scope", "non_graph_source_counts", 0, "count"), 2_871)),
        ("pin count", setter(("exact_input_pins", "count"), 26)),
        ("pin size", setter(("exact_input_pins", "files", 0, "exact_size"), 1)),
        ("pin SHA", setter(("exact_input_pins", "files", 1, "sha256"), "0" * 64)),
        ("upstream exec", setter(("exact_input_pins", "upstream_python_imported_or_executed"), True)),
        ("two pass", setter(("input_security", "two_full_sha256_passes_per_held_fd"), False)),
        ("nlink", setter(("input_security", "nlink_must_equal"), 2)),
        ("identity geometry", setter(("authority_frontier", "identity_binding_may_supply_geometry"), True)),
        ("witness support", setter(("authority_frontier", "witness_or_outer_envelope_may_equal_full_support"), True)),
        ("anti join", lambda doc: doc["required_join_replay"]["every_link_requires"].remove("reverse_antijoin_zero")),
        ("duplicate identity erased", lambda doc: doc["required_join_replay"]["every_link_requires"].remove("duplicate_identity_zero")),
        ("available row hash erased", lambda doc: doc["required_join_replay"]["every_link_requires"].remove("available_row_hash_backbinding_or_pinned_content_address")),
        ("non graph joins erased", lambda doc: doc["required_join_replay"]["non_graph"].clear()),
        ("blanket row hash invented", setter(("required_join_replay", "row_hash_scope", "blanket_every_row_has_own_hash_claimed"), True)),
        ("R294", setter(("representation_alias_dispatch", "R294_preserved_target"), 38_999)),
        ("R295A", setter(("representation_alias_dispatch", "R295A_preserved_target"), 275)),
        ("T2PS", setter(("representation_alias_dispatch", "preserved_representation_semantics", 2, "count"), 1_599)),
        ("T2PS reclassified", setter(("representation_alias_dispatch", "T2PS_1600_classification"), "R288_RESIDUAL")),
        ("alias owner uniqueness", setter(("representation_alias_dispatch", "R294_source_owner_keys_unique"), 46_287)),
        ("alias overlap", setter(("representation_alias_dispatch", "R294_R295A_target_occurrence_intersection"), 1)),
        ("blueprint", lambda doc: doc["ast_blueprints"]["rows"].pop()),
        ("AST producer", setter(("ast_blueprints", "typed_AST_rows_are_constructed_by_this_preflight"), True)),
        ("A1", setter(("A1_A2_obligation_census", "A1"), 17_939)),
        ("A2", setter(("A1_A2_obligation_census", "A2"), 62_151)),
        ("A1A2 rows erased", lambda doc: doc["A1_A2_obligation_census"]["rows"].clear()),
        ("obligation credit", setter(("A1_A2_obligation_census", "counts_are_obligations_not_proved_features"), False)),
        ("sort", setter(("resource_contract", "bounded_external_sort"), False)),
        ("sort bound", setter(("resource_contract", "sort_buffer_limit_bytes"), SORT_BUFFER_LIMIT + 1)),
        ("decoded cap", setter(("resource_contract", "decoded_and_canonical_row_cap_bytes"), DECODED_CANONICAL_ROW_CAP + 1)),
        ("parser cap", setter(("resource_contract", "parser_buffer_cap_bytes"), PARSER_BUFFER_CAP + 1)),
        ("nonstandard constant", setter(("resource_contract", "nonstandard_NaN_Infinity_constants_rejected"), False)),
        ("temp root external", setter(("resource_contract", "OS_temp_root_realpath_outside_deliverables_required"), False)),
        ("temp created external", setter(("resource_contract", "created_temp_directory_realpath_outside_deliverables_required"), False)),
        ("RSS", setter(("resource_contract", "measured_RSS_bytes"), 1)),
        ("security", setter(("input_security", "O_NOFOLLOW"), False)),
        ("blocker count", setter(("remaining_blocker_count",), 5)),
        ("blocker", setter(("remaining_blockers", 0, "id"), "REMOVED")),
        ("candidate", setter(("candidate_and_production_modes", "enabled"), True)),
        ("candidate open", setter(("candidate_and_production_modes", "block_before_open"), False)),
        ("formal", setter(("formal_credit", "B1A"), 1)),
        ("formal credit erased", setter(("formal_credit",), {})),
        ("success promoted", setter(("full_replay_success_means",), "FORMAL_B1A_MINTED")),
        ("does not mean erased", lambda doc: doc["full_replay_success_does_not_mean"].clear()),
        ("B1A", setter(("downstream_state", "B1A"), "PASS")),
        ("B2", setter(("downstream_state", "B2"), "AUTHORIZED")),
        ("D02", setter(("downstream_state", "D02"), "PASS")),
        ("CM2", setter(("downstream_state", "CM2"), "GO")),
    ]


def blocked_candidate_entry(_path: str | None, _production: bool) -> None:
    raise PreflightBlocked(CANDIDATE_BLOCK_REASON)


def boundary_probe() -> dict[str, int]:
    counters = {
        "builtins_open": 0, "os_open": 0, "os_stat": 0,
        "os_mkdir": 0, "os_replace": 0, "os_unlink": 0,
        "path_lstat": 0, "path_stat": 0, "path_resolve": 0,
        "path_open": 0, "path_write": 0, "path_mkdir": 0, "path_touch": 0,
        "temporary_directory": 0, "mkstemp": 0, "named_temp": 0,
    }
    def trip(name: str) -> Callable[..., Any]:
        def inner(*_args: Any, **_kwargs: Any) -> Any:
            counters[name] += 1
            raise AssertionError("filesystem boundary crossed:" + name)
        return inner
    with (
        mock.patch.object(builtins, "open", side_effect=trip("builtins_open")),
        mock.patch("os.open", side_effect=trip("os_open")),
        mock.patch("os.stat", side_effect=trip("os_stat")),
        mock.patch("os.mkdir", side_effect=trip("os_mkdir")),
        mock.patch("os.replace", side_effect=trip("os_replace")),
        mock.patch("os.unlink", side_effect=trip("os_unlink")),
        mock.patch.object(Path, "lstat", side_effect=trip("path_lstat")),
        mock.patch.object(Path, "stat", side_effect=trip("path_stat")),
        mock.patch.object(Path, "resolve", side_effect=trip("path_resolve")),
        mock.patch.object(Path, "open", side_effect=trip("path_open")),
        mock.patch.object(Path, "write_bytes", side_effect=trip("path_write")),
        mock.patch.object(Path, "mkdir", side_effect=trip("path_mkdir")),
        mock.patch.object(Path, "touch", side_effect=trip("path_touch")),
        mock.patch("tempfile.TemporaryDirectory", side_effect=trip("temporary_directory")),
        mock.patch("tempfile.mkstemp", side_effect=trip("mkstemp")),
        mock.patch("tempfile.NamedTemporaryFile", side_effect=trip("named_temp")),
    ):
        for production in (False, True):
            try:
                blocked_candidate_entry("/must/not/be/inspected", production)
            except PreflightBlocked as exc:
                need(str(exc) == CANDIDATE_BLOCK_REASON, "blocked reason")
            else:
                raise AssertionError("candidate mode accepted")
    need(all(value == 0 for value in counters.values()), "candidate zero FS calls")
    return counters


def structure_attack_test() -> dict[str, Any]:
    wanted = (("result", "rows"),)
    # A same-named decoy table is legal elsewhere: extraction is bound to the
    # exact structural path/offset and never to a globally searched marker.
    good = b'{"decoy":{"rows":[]},"result":{"rows":[{"a":1},{"a":2}]},"z":null}'
    stats = _validate_complete_json_stream(io.BytesIO(good), wanted)
    need(stats["selected_path_count"] == 1, "structure good path")
    attacks = (
        ("missing array comma", b'{"result":{"rows":[1 2]}}'),
        ("double array comma", b'{"result":{"rows":[1,,2]}}'),
        ("trailing array comma", b'{"result":{"rows":[1,]}}'),
        ("missing object comma", b'{"result":{"rows":[] "x":1}}'),
        ("double object comma", b'{"result":{"rows":[],,"x":1}}'),
        ("trailing object comma", b'{"result":{"rows":[],}}'),
        ("trailing document garbage", b'{"result":{"rows":[]}}X'),
        ("duplicate outer key", b'{"result":{"rows":[]},"result":{"rows":[]}}'),
        ("duplicate selected row key", b'{"result":{"rows":[{"a":1,"a":2}]}}'),
        ("wrong exact path", b'{"wrong":{"rows":[]}}'),
        ("selected value not array", b'{"result":{"rows":{}}}'),
    )
    rejected: list[str] = []
    for label, payload in attacks:
        try:
            _validate_complete_json_stream(io.BytesIO(payload), wanted)
        except PreflightBlocked:
            rejected.append(label)
        else:
            raise AssertionError("JSON structure attack accepted:" + label)
    need(len(rejected) == len(attacks), "JSON structure attack total")
    return {
        "attack_count": len(attacks),
        "attacks_rejected": len(rejected),
        "valid_document_EOF_verified": stats["document_EOF_verified"],
        "valid_document_duplicate_key_count": stats["duplicate_object_key_count"],
    }


def lineage_attack_test() -> dict[str, int]:
    rejected = 0
    mapping: dict[str, Any] = {}
    _insert(mapping, "edge", 1, "attack edge")
    try:
        _insert(mapping, "edge", 2, "attack edge")
    except PreflightBlocked:
        rejected += 1
    else:
        raise AssertionError("duplicate lineage edge accepted")

    protected = {"edge": "x", "value": 1}
    protected["row_sha256"] = digest(protected)
    row_digest(protected)
    corrupted = dict(protected)
    corrupted["value"] = 2
    try:
        row_digest(corrupted)
    except PreflightBlocked:
        rejected += 1
    else:
        raise AssertionError("lineage row hash corruption accepted")

    for left, right in (({"a"}, {"a", "b"}), ({"a", "b"}, {"a"})):
        try:
            _set_equal(left, right, "attack anti-join")
        except PreflightBlocked:
            rejected += 1
        else:
            raise AssertionError("lineage anti-join gap accepted")
    need(rejected == 4, "lineage attack rejection total")
    return {"attack_count": 4, "attacks_rejected": rejected}


def parser_limit_and_constant_attack_test() -> dict[str, int]:
    wanted = (("result", "rows"),)

    def quoted_element(size: int) -> bytes:
        need(size >= 2, "quoted test size")
        return b'"' + (b"a" * (size - 2)) + b'"'

    def structure_payload(element: bytes) -> bytes:
        return b'{"result":{"rows":[' + element + b']}}'

    def selected_values(content_after_open_bracket: bytes) -> list[Any]:
        held = HeldInputs()
        path = ("rows",)
        held.structure_validated_labels.add("TEST")
        held.table_offsets[("TEST", path)] = 0

        def memory_stream(_label: str) -> tuple[io.BytesIO, io.BytesIO]:
            stream = io.BytesIO(content_after_open_bracket)
            return stream, stream

        held._binary_stream = memory_stream  # type: ignore[method-assign]
        return list(held.iter_array("TEST", path))

    exact = quoted_element(DECODED_CANONICAL_ROW_CAP)
    plus_one = quoted_element(DECODED_CANONICAL_ROW_CAP + 1)
    structure_ok = _validate_complete_json_stream(io.BytesIO(structure_payload(exact)), wanted)
    need(structure_ok["selected_path_count"] == 1, "structure exact-cap accept")
    selected_ok = selected_values(exact + b"]")
    need(len(selected_ok) == 1, "selected exact-cap accept")

    rejected = 0
    attacks = 0
    for label, call in (
        ("structure decoded cap+1", lambda: _validate_complete_json_stream(io.BytesIO(structure_payload(plus_one)), wanted)),
        ("selected decoded cap+1", lambda: selected_values(plus_one + b"]")),
        ("structure parser buffer cap", lambda: _validate_complete_json_stream(io.BytesIO(structure_payload(b'"' + b"a" * (PARSER_BUFFER_CAP + 1))), wanted)),
        ("selected parser buffer cap", lambda: selected_values(b'"' + b"a" * (PARSER_BUFFER_CAP + 1))),
    ):
        attacks += 1
        try:
            call()
        except PreflightBlocked:
            rejected += 1
        else:
            raise AssertionError("parser cap attack accepted:" + label)

    for token in (b"NaN", b"Infinity", b"-Infinity"):
        for label, call in (
            ("structure", lambda token=token: _validate_complete_json_stream(io.BytesIO(structure_payload(token)), wanted)),
            ("selected", lambda token=token: selected_values(token + b"]")),
        ):
            attacks += 1
            try:
                call()
            except PreflightBlocked:
                rejected += 1
            else:
                raise AssertionError(f"nonstandard constant accepted:{label}:{token!r}")
    need(attacks == rejected == 10, "parser limit/constant attacks")
    return {
        "exact_cap_accept_paths": 2,
        "attack_count": attacks,
        "attacks_rejected": rejected,
    }


def self_test() -> dict[str, Any]:
    doc = contract_document()
    validate_contract(doc)
    raw = canonical_bytes(doc)
    need(canonical_bytes(json.loads(raw)) == raw, "canonical round trip")
    need(hashlib.sha256(raw).hexdigest() == digest(doc), "canonical digest")
    rejected: list[str] = []
    for label, mutate in semantic_mutations():
        candidate = copy.deepcopy(doc)
        mutate(candidate)
        try:
            validate_contract(candidate)
        except PreflightBlocked:
            rejected.append(label)
        else:
            raise AssertionError("semantic mutation accepted:" + label)
    structure_attacks = structure_attack_test()
    lineage_attacks = lineage_attack_test()
    parser_limit_attacks = parser_limit_and_constant_attack_test()
    boundary = boundary_probe()
    return {
        "schema": SCHEMA + ".self-test.v1",
        "status": "PASS",
        "contract_digest_sha256": digest(doc),
        "semantic_mutation_count": len(rejected),
        "semantic_mutations_rejected": len(rejected),
        "JSON_structure_attacks": structure_attacks,
        "lineage_attacks": lineage_attacks,
        "parser_limit_and_constant_attacks": parser_limit_attacks,
        "candidate_and_production_refusals": 2,
        "filesystem_boundary_call_counts": boundary,
        "formal_credit": 0,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--print-contract", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--full-replay", action="store_true")
    modes.add_argument("--candidate-output", metavar="PATH")
    modes.add_argument("--production-output", metavar="PATH")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.candidate_output is not None or args.production_output is not None:
        try:
            blocked_candidate_entry(
                args.candidate_output if args.candidate_output is not None else args.production_output,
                args.production_output is not None,
            )
        except PreflightBlocked:
            return 1
        raise AssertionError("unreachable candidate path")
    if args.print_contract:
        print(canonical_bytes(contract_envelope()).decode("ascii"))
        return 0
    if args.self_test:
        print(canonical_bytes(self_test()).decode("ascii"))
        return 0
    if args.full_replay:
        print(canonical_bytes(full_replay()).decode("ascii"))
        return 0
    raise AssertionError("unreachable mode")


if __name__ == "__main__":
    raise SystemExit(main())
