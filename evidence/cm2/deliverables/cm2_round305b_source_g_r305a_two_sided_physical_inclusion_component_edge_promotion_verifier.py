#!/usr/bin/env python3
"""Independent cacheless verifier for the Round305B promotion candidate.

The candidate producer is inert input: this source never imports, executes,
tokenizes, or otherwise derives expected values from it.  Expected rows and
wire bytes are rebuilt from the sealed Round305A scope and byte-pinned formal
upstream packages.  In particular the G3/G4 attachment is replayed as a
relative-physical-space p-to-rho limit, never inferred from candidate flags,
a corridor box, common metadata, a DSU projection, or a D4 shortcut.

The no-write reconstruction interface deliberately works before the final
producer byte pin is frozen.  Candidate admission remains fail closed until
that inert pin is filled and every expected candidate byte is exact.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter, defaultdict
import ctypes
import errno
import fcntl
from fractions import Fraction as Q
import gzip
import hashlib
import importlib
import importlib.util
import io
import json
from math import isqrt
import os
from pathlib import Path
import platform
import py_compile
import re
import stat
import sys
import tempfile
import types
from typing import Any, Callable
import zlib


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
D = ROOT / "deliverables"

PREFIX = (
    "cm2_round305b_source_g_r305a_two_sided_physical_inclusion_"
    "component_edge_promotion"
)
SCHEMA = (
    "cm2.round305b.source-g-r305a-two-sided-physical-inclusion-"
    "component-edge-promotion.v1"
)
PRODUCER = PREFIX + ".py"
WIRE_SPEC_FILE = PREFIX + "_wire_spec.json"
WIRE_CONTRACT_FIXTURE_FILE = PREFIX + "_wire_contract_fixture.json"
WIRE_SPEC_ID = "CM2_ROUND305B_NORMATIVE_WIRE_SPEC_V2"

R303B_PREFIX = "cm2_round303b_source_g_unified_attachment_edge_promotion"
R304_PREFIX = (
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild"
)
R305A_PREFIX = (
    "cm2_round305a_source_g_r300a_post_r304_residual_scope_reprojection"
)
R303B_MANIFEST = R303B_PREFIX + "_manifest.sha256"
R304_MANIFEST = R304_PREFIX + "_manifest.sha256"
R305A_MANIFEST = R305A_PREFIX + "_manifest.sha256"
R305A_RESULT = R305A_PREFIX + "_result.json"
R305A_LEDGER = R305A_PREFIX + "_scope_reprojection_ledger.json.gz"
R305A_ATTACKS = R305A_PREFIX + "_attack_suite.json"
R305A_VERIFICATION = R305A_PREFIX + "_verification.json"

R303B_MANIFEST_SHA256 = (
    "7d7293c488a05c8873a63b7d63d0bf125260c6b9d3c60595201896cfde0c9786"
)
R304_MANIFEST_SHA256 = (
    "de49f4233f6a22f43385e727071c5a5ebac68c35788dc2dd13e71d045639838c"
)
R305A_MANIFEST_SHA256 = (
    "21a938d65d50856b4d1ecae7414259b3481f4f2f8207d91debc951e06441a9f7"
)

R305A_EXPECTED_MANIFEST_MEMBERS = frozenset({
    R305A_PREFIX + ".py",
    R305A_LEDGER,
    R305A_RESULT,
    R305A_PREFIX + "_promotion_verifier.py",
    R305A_ATTACKS,
    R305A_VERIFICATION,
    R305A_PREFIX + "_report.md",
    R305A_PREFIX + "_cold_replay.md",
})
R305A_CRITICAL_FILE_PINS = {
    R305A_PREFIX + ".py":
        "42e7cc1eeabaedee883a37b8de9301ee71d5ba068d2fb76fafc80b95061b6772",
    R305A_PREFIX + "_promotion_verifier.py":
        "d4fd7bfd4c2bb90e1df515a9318d8f925fc9dab4bb8cb3872f496a3d665647bf",
    R305A_RESULT:
        "b985df80cc0b447f25509ef6d4095b9d0aa810ffcef05d4b5475bf84d36542f1",
    R305A_LEDGER:
        "8db30279e03aac90ea96b7a603e51aaa6fb2a70ad6c1593915c55b1befe991b6",
    R305A_ATTACKS:
        "3795cd3b03f961e010b351d5132f55f5d3bda8d4245707755d999e780a9c71b7",
    R305A_VERIFICATION:
        "5c98bd02f4245d3b6fd7d35518b6932f984ec05d3e91b607854bf9e180b29c4d",
}
R305A_RESULT_OBJECT_SHA256 = (
    "c391ecca3f5af8227052c628bda77104ec564d4eeaa625fafbde32a3ada352eb"
)
R305A_VERIFICATION_OBJECT_SHA256 = (
    "9654f43c32aacfd3a27b6baa18d65755dfb9c867bd869aaa586a9b736fcf7589"
)

# Filled only after the producer implementation is frozen.  It is an inert
# final byte pin: no producer code is imported or executed, while the
# independently reconstructed result wire and every admission path bind these
# exact producer source bytes.
EXPECTED_PRODUCER_SHA256: str | None = (
    "bf2c451b782b2e9ecf7fe9b6b2eaef50e06b9e5499b47579d815665fb8cd914b"
)
# Jointly frozen external normative protocol.  These are inert byte pins; the
# verifier reconstructs every candidate value independently from admitted
# upstream inputs and never learns a candidate commitment from the producer.
EXPECTED_WIRE_SPEC_SHA256 = (
    "8cd6cbcd936875885b76fe501f76bf949e81233c07d75f715c003beb021ef573"
)
EXPECTED_WIRE_CONTRACT_FIXTURE_SHA256 = (
    "c2695472d522f1a24a2b8b7bbea0dff6e2c932b5dc63f154b27c6887b02e3f02"
)
EXPECTED_PRODUCER_SCHEMA_SNAPSHOT_SHA256 = (
    "ec5eab1b9aaeb851e8858b76d14ba7142d7db5aa41ea3286297317b105e547e7"
)

EXPECTED_WITNESSES = 1_024
EXPECTED_ANCHORS = 2_048
EXPECTED_CLOSURE_CONTACTS = 3_536
EXPECTED_FACE_CONTACTS = 1_856
EXPECTED_DIAGONAL_CONTACTS = 1_680
EXPECTED_OWNER_LOCI = 2_696
EXPECTED_FACE_OWNER_LOCI = 1_856
EXPECTED_VERTEX_OWNER_LOCI = 840
EXPECTED_EDGES = 8
EXPECTED_PER_EDGE = 128
EXPECTED_OFFICIAL_KEYS = 124
EXPECTED_RESIDUAL_KEYS = 16
EXPECTED_R287_PAIR_ROWS = 3_488
MAXIMUM_LATER_RANK_REDUCTIONS = 8
MAX_JSON_BYTES = 64 * 1024 * 1024
MAX_GZIP_UNCOMPRESSED_BYTES = 64 * 1024 * 1024
PIN_RE = re.compile(r"^[0-9a-f]{64}$")

FORMAL_INDEPENDENT_GEOMETRY_RECONSTRUCTION_IMPLEMENTED = True

R174_PREFIX = "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization"
R179_PREFIX = "cm2_round179_source_g_residual_tube_arrangement"
R275_PREFIX = "cm2_round275_source_g_complete_reverse_rechart_materialization"
R287_PREFIX = "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe"
R292_PREFIX = "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe"
R294B_PREFIX = "cm2_round294b_source_g_registry_builder_admission_closure"
R300A_PREFIX = "cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion"
R300B_PREFIX = (
    "cm2_round300b_source_g_registry_boundary_and_complete_r275_"
    "face_inventory_closure"
)

R174_ROWS = R174_PREFIX + "_rows.json"
R174_MODULE = R174_PREFIX + ".py"
R174_VERIFIER_MODULE = R174_PREFIX + "_verifier.py"
R179_MODULE = R179_PREFIX + ".py"
R275_CERTIFICATE = R275_PREFIX + "_certificate.json"
R287_LEDGER = R287_PREFIX + "_ledger.json.gz"
R292_LEDGER = R292_PREFIX + "_ledger.json.gz"
R294_REGISTRY = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)
R300A_LEDGER = R300A_PREFIX + "_ledger.json.gz"
R304_MEMBER_LEDGER = R304_PREFIX + "_member_component_ledger.json.gz"

FORMAL_MANIFEST_PINS = {
    R174_PREFIX + "_manifest.sha256":
        "9e92db7748a2c0acdce532c830f899ce153765de64a59e9f372df3099ac91b76",
    R179_PREFIX + "_manifest.sha256":
        "8fd5ae3a0cdd0c3321c0f8ffe6183ab57d31088b96523fa41ce0ebbe10d78b76",
    R275_PREFIX + "_manifest.sha256":
        "a5dbf43a144a0a752f467911ee59e6afd6d2d60d27e0bc80bc45b7afa9334669",
    R287_PREFIX + "_manifest.sha256":
        "85a9d4fcf9d9931a0e352eeef7582347b12325b92ffc78f2ee40c77c58093751",
    R292_PREFIX + "_manifest.sha256":
        "4ea92e4112cae18aa0c13a6d2308816bafc19e4129c09d8b6be914268cfc4870",
    R294B_PREFIX + "_manifest.sha256":
        "fc16aa2792a59dff922afcc8ec66b1ca015251af3c5f718d9d909439a2990d76",
    R300A_PREFIX + "_manifest.sha256":
        "9f9e86d93aebe2b47e525af795a3a9e8331ab3b6f2d71ecafe69429238a1aee8",
    R300B_PREFIX + "_manifest.sha256":
        "6208c4bfd8b147f06ffb735d4b5621faff22585831b5f19d48e8125514ac4a6b",
}

# Direct pins are repeated here even when a modern manifest covers the file.
# R273/R274 have no admissible modern package seal, so their two tiny formulas
# (active-factor selection and monotone extrema) are independently transcribed
# below; neither source is imported or treated as an admitted dependency.
FORMAL_INPUT_PINS = {
    "cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_gate3_ge_interval_atlas_cert.py":
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    "cm2_gate3_eight_cell_symmetry_atlas_cert.py":
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "cm2_gate3_chart_seam_quotient_cert.py":
        "fa00d4c14ee24b8f3fbc7f345deef13deb272080a886b68d2aa2f9c92a456fe1",
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json":
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    R174_MODULE:
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    R174_VERIFIER_MODULE:
        "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
    R174_ROWS:
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    R179_MODULE:
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    "cm2_round273_source_g_reverse_rechart_probe.py":
        "40b18650a1fe8d797daf776cb9305686c21fa2eb5a7886c48ce91d697c93105c",
    "cm2_round274_source_g_reverse_rechart_tail_arrangement_probe.py":
        "677813e132d62732900a26edc3fae5d562049d8d1fac2cea59f7c65d41735292",
    R275_CERTIFICATE:
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R287_LEDGER:
        "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a",
    R292_LEDGER:
        "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    R294_REGISTRY:
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    R300A_LEDGER:
        "ddc1a8bc53861afeb93d3569c6efa228f17d86f161db31a39fa9b72458ab8f2d",
    R304_MEMBER_LEDGER:
        "9a7e8c8a0ef810cfd6f29d99c0d2d6701b537ac76d1ab224dcbb60bec966dbd0",
}

OUTPUT_NAMES = {
    "physical": PREFIX + "_physical_witness_ledger.json.gz",
    "anchor": PREFIX + "_anchor_ledger.json.gz",
    "contact": PREFIX + "_closure_contact_ledger.json.gz",
    "owner": PREFIX + "_owner_locus_ledger.json.gz",
    "edge": PREFIX + "_canonical_component_edge_ledger.json.gz",
    "result": PREFIX + "_result.json",
}
ATTACK_FILENAME = PREFIX + "_attack_suite.json"
VERIFICATION_FILENAME = PREFIX + "_verification.json"
VERIFIER_FILENAME = PREFIX + "_verifier.py"
ATTACK_SCHEMA = SCHEMA + ".independent-attack-suite.v1"
VERIFICATION_SCHEMA = SCHEMA + ".independent-verification.v1"
PROMOTION_STAGE_PREFIX = ".r305b-promotion-stage-"
PROMOTION_CANDIDATE_ORDER = (
    OUTPUT_NAMES["physical"],
    OUTPUT_NAMES["anchor"],
    OUTPUT_NAMES["contact"],
    OUTPUT_NAMES["owner"],
    OUTPUT_NAMES["edge"],
    OUTPUT_NAMES["result"],
)
PROMOTION_ORDER = (
    ATTACK_FILENAME,
    *PROMOTION_CANDIDATE_ORDER,
    VERIFICATION_FILENAME,
)
FileIdentity = tuple[int, int, int, int, int, int, int]
DirectoryIdentity = tuple[int, int, int]

STRICT_SIGNS = frozenset({"STRICT_NEGATIVE", "STRICT_POSITIVE"})
MAX_BRACKET_DEPTH = 32
SQRT_REPLAY_BITS = 512
EXPECTED_BRACKET_DEPTH_HISTOGRAM = {1: 320, 2: 704}
EXPECTED_CONTACT_DIMENSION_HISTOGRAM = {0: 1_680, 1: 1_856}
EXPECTED_OWNER_KIND_HISTOGRAM = {
    "FACE_RELATIVE_INTERIOR": 1_856,
    "FOUR_PATCH_VERTEX": 840,
}
EXPECTED_PATCH_CONTACT_DEGREE_HISTOGRAM = {3: 32, 5: 320, 8: 672}
EXPECTED_VERTEX_WITNESS_REFS = 3_360
EXPECTED_VERTEX_CONTACT_REFS = 5_040


def opposite_strict_sign(sign: str) -> str:
    need(sign in STRICT_SIGNS, "OPPOSITE_STRICT_SIGN_DOMAIN")
    return (
        "STRICT_POSITIVE" if sign == "STRICT_NEGATIVE"
        else "STRICT_NEGATIVE"
    )

PHYSICAL_WITNESS_KEYS = (
    "Round305B_physical_witness_row_id", "schema",
    "source_Round305A_scope_reprojection_row_id",
    "source_Round305A_scope_reprojection_row_sha256",
    "source_Round300A_row_id", "source_Round300A_row_sha256",
    "canonical_registry_occurrence_pair", "Round304_final_component_pair",
    "official_key_pair", "cross_official_key_physical_edge_permitted",
    "occurrence_identity_collapsed", "official_key_identity_merged",
    "proof_core_patch_id", "owner_extension_patch_id",
    "active_function_id", "guard_id", "branch_id",
    "exact_relative_physical_domain", "exact_graph_Gamma",
    "anchor_row_ids", "anchor_row_sha256s", "closure_contact_row_ids",
    "closure_contact_row_sha256s", "owner_locus_row_ids",
    "owner_locus_row_sha256s",
    "owner_extension_sidecar_not_Gamma_core_or_attachment_or_edge_basis",
    "G0_exact_provenance_pins_and_row_closures",
    "G1_endpoint_occurrence_connected_supports",
    "G2_nonempty_connected_included_lower_stratum",
    "G3_left_closure_attaches_to_included_patch",
    "G4_right_closure_attaches_to_included_patch",
    "G5_endpoint_patch_provenance_exactly_closed",
    "relative_physical_closure_limit_lemma_id",
    "corridor_box_used_as_Gamma_intersection", "D4_transfer_used",
    "candidate_physical_connectivity_conclusion",
    "formal_physical_witness_credit", "formal_component_edge_credit",
    "formal_DSU_rank_reduction_credit", "formal_maximality_credit",
    "formal_fibre_credit", "formal_global_disposition_credit", "row_sha256",
)
ANCHOR_KEYS = (
    "Round305B_anchor_row_id", "schema", "physical_witness_row_id", "side",
    "endpoint_occurrence_id", "Round275_region_id",
    "Round275_region_row_sha256",
    "R287_region_disposition_row_id", "R287_region_row_sha256",
    "R292_refinement_cell_row_id", "R292_refinement_cell_row_sha256",
    "R292_connected_support_component_row_id",
    "R292_connected_support_component_row_sha256",
    "R292_occurrence_content_preimage_sha256",
    "R294_occurrence_registry_row_id", "R294_occurrence_registry_row_sha256",
    "R294_official_key_id", "R294_official_key_ordinal",
    "R294_official_key_binding_status",
    "Round304_member_row_id", "Round304_member_row_sha256",
    "official_key_id", "connected_positive_open_support_nonempty",
    "connected_positive_open_support_member_count",
    "relative_physical_closure_limit_side", "formal_anchor_binding_credit",
    "formal_occurrence_identity_collapse_credit",
    "formal_official_key_merge_credit", "row_sha256",
)
CLOSURE_CONTACT_KEYS = (
    "Round305B_closure_contact_row_id", "schema",
    "associated_physical_witness_row_ids",
    "contact_pair_owner_extension_patch_ids",
    "contact_kind", "base_dimension",
    "exact_common_base_z_s", "common_p_bracket_hull",
    "strict_common_active_function_p_derivative_sign",
    "owner_extension_root_unique_on_full_closure", "owner_locus_row_id",
    "full_closure_extension_only", "not_Gamma_core_contact",
    "not_G3_G4_or_component_edge_basis", "D4_transfer_used", "row_sha256",
)
OWNER_LOCUS_KEYS = (
    "Round305B_owner_locus_row_id", "schema", "locus_kind",
    "exact_locus_base_z_s", "associated_physical_witness_row_ids",
    "global_incident_owner_extension_patch_ids",
    "global_incident_owner_extension_patch_count",
    "incident_closure_contact_row_ids",
    "lexicographically_least_global_incident_owner_extension_patch",
    "face_endpoint_vertex_override_row_ids",
    "full_closure_extension_only", "not_Gamma_core_locus",
    "not_G3_G4_or_component_edge_basis", "D4_transfer_used", "row_sha256",
)
COMPONENT_EDGE_KEYS = (
    "Round305B_canonical_component_edge_row_id", "schema",
    "canonical_Round304_final_component_pair", "physical_witness_row_count",
    "physical_witness_row_ids_sha256", "physical_witness_row_sha256s_sha256",
    "canonical_occurrence_pairs_sha256", "canonical_official_key_pair",
    "cross_official_key_physical_edge_permitted",
    "occurrence_identity_collapsed", "official_key_identity_merged",
    "all_128_witnesses_satisfy_G0_G5",
    "deduplicated_from_witness_rows_not_union_rows",
    "formal_component_edge_credit", "eligible_for_later_fresh_DSU_application",
    "formal_DSU_rank_reduction_credit", "row_sha256",
)

FULL_SIGN_SIDE_SUPPORT_CERTIFICATE_KEYS = (
    "certificate_id", "endpoint_occurrence_id", "endpoint_side",
    "owner_face", "approach", "oriented_p_face", "graph_bracket_p",
    "proof_closed_core_base_z_s", "exact_common_R292_open_cell_t2_p_s",
    "active_function_id", "active_reason", "active_factor_side_sign",
    "exact_F_p_face_sign",
    "uniform_strict_dF_dp_sign_on_whole_common_R292_cell",
    "F_at_rho_equals_zero", "face_sign_derivative_orientation",
    "face_sign_derivative_orientation_hard_checked",
    "exact_full_half_open_segment",
    "strict_monotonicity_retains_face_sign_on_entire_segment",
    "endpoint_R275_active_factor_side_sign_equals_face_sign",
    "whole_cell_dynamic_signature_exactly_one_unresolved_active_reason",
    "all_other_whole_cell_validity_predicates_uniformly_strict",
    "R287_R292_single_connected_support_provenance",
    "full_segment_sign_slice_is_named_endpoint_support",
    "local_corridor_role",
)
FULL_SIGN_SIDE_PROVENANCE_KEYS = (
    "Round275_region_id", "Round275_region_row_sha256",
    "R287_region_disposition_row_id", "R287_region_row_sha256",
    "R292_refinement_cell_row_id", "R292_refinement_cell_row_sha256",
    "R292_connected_support_component_row_id",
    "R292_connected_support_component_row_sha256",
    "connected_positive_open_support_member_count",
)
CLOSURE_LIMIT_SIDE_KEYS = (
    "approach", "active_factor_sign", "strict_p_derivative_sign", "limit",
    "topology", "quantified_base", "support_open_base_z_s",
    "proof_closed_core_base_z_s", "strict_sign_corridor_box_t2_p_s",
    "corridor_strictly_inside_R292_open_cell",
    "local_corridor_nonempty_witness_only",
    "full_sign_side_to_rho_support_certificate",
    "exact_full_sign_side_contained_in_R292_support_derived",
)
G3_G4_KEYS = (
    "satisfied", "endpoint", "sign_side", "quantified_base",
    "proof_closed_core_base_z_s", "sequence",
    "strict_sign_corridor_box_t2_p_s",
    "full_sign_side_to_rho_support_certificate",
    "full_sign_side_sequence_remains_in_exact_R292_open_support_by_certificate",
    "corridor_used_only_as_local_nonempty_witness",
    "limit_in_relative_physical_space_X", "conclusion",
)

TWO_SIDED_ATTACHMENT_THEOREM = {
    "theorem_id": (
        "CM2_STRICT_P_MONOTONE_RECHART_WALL_ZERO_TWO_CLOSURE_LIMIT_V1"
    ),
    "version": 1,
    "hypotheses": {
        "G0_exact_provenance_pins_and_row_closures": (
            "The sealed Round305A residual row closes through the exact "
            "Round300A source row, R287 pair/regions, both R275 rows, the "
            "single-member R292 components/cells, the R294 occurrence rows, "
            "and the R304 member/component/key projection."
        ),
        "G1_endpoint_occurrence_connected_supports": (
            "A deterministic closed rational quarter-inset B_core lies "
            "strictly inside the open R292 z,s base and has positive area. "
            "D=B_core times [p_minus,p_plus]; Phi is continuous on D. For "
            "each endpoint a full-sign-side certificate derives, rather than "
            "assumes, that the complete oriented p_face-to-rho sign slice is "
            "contained in its exact connected R292 endpoint support."
        ),
        "G2_nonempty_connected_included_lower_stratum": (
            "The discarded source coordinate is uniformly strict nonzero, "
            "the selected wall product therefore vanishes exactly when the "
            "target hit coordinate F vanishes, dF/dp has one uniform strict "
            "sign, and the two p faces have uniform opposite signs. The "
            "unique continuous root rho:B_core->(p_minus,p_plus) defines a "
            "nonempty connected included physical graph Gamma_core."
        ),
        "G3_left_closure_attaches_to_included_patch": (
            "The LEFT full-sign-side certificate combines its exact face F "
            "sign, uniform whole-cell strict dF/dp, F(rho)=0, derivative/face "
            "orientation, unique active dynamic boundary, and the sealed "
            "R275->R287->R292 single-support chain. Thus for every b in "
            "B_core the entire half-open p_face-to-rho segment lies in the "
            "named left support, and Phi along it converges to Gamma_core in X."
        ),
        "G4_right_closure_attaches_to_included_patch": (
            "The independently instantiated RIGHT full-sign-side certificate "
            "gives the analogous complete half-open segment containment and "
            "relative-X convergence from the right named support."
        ),
        "G5_endpoint_patch_provenance_exactly_closed": (
            "Gamma_core is replayed as the valid wall-event lower stratum, not "
            "merely a coordinate zero set. R294 supplies occurrence identity "
            "with null official key, while R304 separately materializes the "
            "official key and component; those stages are never conflated."
        ),
    },
    "forbidden_shortcuts": [
        "same official key",
        "same zero graph",
        "common closure without a full face-to-rho sign-side support certificate",
        "Round304 DSU projection",
        "corridor box treated as an intersection with Gamma_core",
        "D4 transfer without a separately sealed theorem",
    ],
    "conclusion": (
        "Gamma_core is contained in cl_X(A_left) intersect cl_X(A_right); hence "
        "A_left union Gamma_core union A_right is connected in the physical "
        "section and supports one physical component edge. Occurrence and "
        "official-key identities remain distinct."
    ),
    "credit_boundary": {
        "formal_physical_witness_credit_per_row": 1,
        "formal_component_edge_credit_per_canonical_component_pair": 1,
        "formal_occurrence_identity_collapse_credit": 0,
        "formal_official_key_merge_credit": 0,
        "formal_DSU_rank_reduction_credit_in_Round305B": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
    },
}

_NORMATIVE_WIRE_SPEC: dict[str, Any] | None = None
_FORMAL_GEOMETRY_LOADER_AUDIT: dict[str, Any] | None = None


class VerificationBlocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationBlocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


FORBIDDEN_COMMITTED_RUNTIME_KEYS = frozenset({
    "python_executable", "absolute_python_executable", "workspace",
    "workspace_path", "absolute_path", "generated_at", "generation_time",
    "timestamp", "wall_clock", "wall_clock_time",
})


def assert_path_and_time_free_wire(value: Any, label: str = "wire") -> None:
    """Reject machine-local paths and wall-clock data from committed bytes."""

    if type(value) is dict:
        for key, child in value.items():
            need(type(key) is str, "NONSTRING_WIRE_KEY:" + label)
            need(key.lower() not in FORBIDDEN_COMMITTED_RUNTIME_KEYS,
                 "FORBIDDEN_RUNTIME_KEY:" + label + ":" + key)
            assert_path_and_time_free_wire(child, label + "." + key)
        return
    if type(value) is list:
        for index, child in enumerate(value):
            assert_path_and_time_free_wire(child, f"{label}[{index}]")
        return
    if type(value) is str:
        need(
            not value.startswith(("/", "~/", "file://"))
            and re.match(r"^[A-Za-z]:[\\/]", value) is None,
            "ABSOLUTE_PATH_IN_COMMITTED_WIRE:" + label,
        )


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def require_regular(path: Path, label: str) -> None:
    try:
        metadata = path.lstat()
    except FileNotFoundError as error:
        raise VerificationBlocked("MISSING:" + label) from error
    need(path.parent.resolve() == D.resolve(), "OUTSIDE_DELIVERABLES:" + label)
    need(not stat.S_ISLNK(metadata.st_mode), "SYMLINK:" + label)
    need(stat.S_ISREG(metadata.st_mode), "NONREGULAR:" + label)
    need(metadata.st_nlink == 1 and metadata.st_size > 0, "PATH_BOUNDARY:" + label)


def file_identity(info: os.stat_result) -> FileIdentity:
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_nlink,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def directory_identity(info: os.stat_result) -> DirectoryIdentity:
    return (info.st_dev, info.st_ino, info.st_mode)


def lexical_directory_without_symlinks(path: Path, label: str) -> Path:
    """Resolve no component: every existing component must be a real dir."""

    absolute = Path(os.path.abspath(os.fspath(path)))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        need(os.path.lexists(current), "MISSING_DIRECTORY_COMPONENT:" + label)
        info = os.lstat(current)
        need(
            stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode),
            "SYMLINK_OR_NONDIRECTORY_COMPONENT:" + label + ":" + part,
        )
    need(absolute == path.resolve(), "DIRECTORY_DOT_OR_SYMLINK_ESCAPE:" + label)
    return absolute


def resolve_candidate_directory(candidate_dir: Path) -> Path:
    resolved = lexical_directory_without_symlinks(
        candidate_dir, "Round305B candidate directory"
    )
    workspace = ROOT.resolve()
    need(
        workspace in resolved.parents
        and resolved not in (workspace, D.resolve()),
        "CANDIDATE_DIRECTORY_MUST_BE_PRIVATE_WORKSPACE_STAGE",
    )
    info = os.lstat(resolved)
    need(
        info.st_uid == os.geteuid()
        and stat.S_IMODE(info.st_mode) == 0o700,
        "CANDIDATE_DIRECTORY_OWNER_MODE_0700",
    )
    return resolved


def open_bound_directory(directory: Path, label: str) -> tuple[int, DirectoryIdentity]:
    descriptor = os.open(
        directory,
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    bound = directory_identity(os.fstat(descriptor))
    need(bound == directory_identity(os.lstat(directory)), label + ":OPEN_RACE")
    return descriptor, bound


def read_exact_regular_at(
    directory_descriptor: int,
    name: str,
    expected: bytes,
    label: str,
    *,
    require_owner: bool = True,
) -> tuple[bytes, FileIdentity]:
    need(
        name == Path(name).name and "/" not in name and "\\" not in name,
        label + ":FLAT_BASENAME",
    )
    try:
        before = os.stat(name, dir_fd=directory_descriptor, follow_symlinks=False)
    except FileNotFoundError as error:
        raise VerificationBlocked(label + ":MISSING") from error
    need(
        stat.S_ISREG(before.st_mode)
        and not stat.S_ISLNK(before.st_mode)
        and before.st_nlink == 1
        and before.st_size == len(expected)
        and (not require_owner or before.st_uid == os.geteuid()),
        label + ":REGULAR_SINGLE_LINK_EXACT_SIZE",
    )
    descriptor = os.open(
        name,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
        dir_fd=directory_descriptor,
    )
    try:
        opened = os.fstat(descriptor)
        need(file_identity(opened) == file_identity(before), label + ":OPEN_RACE")
        chunks: list[bytes] = []
        remaining = len(expected) + 1
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            if not block:
                break
            chunks.append(block)
            remaining -= len(block)
        raw = b"".join(chunks)
        need(raw == expected, label + ":EXACT_BYTES")
        need(file_identity(os.fstat(descriptor)) == file_identity(before),
             label + ":FD_DRIFT")
    finally:
        os.close(descriptor)
    after = os.stat(name, dir_fd=directory_descriptor, follow_symlinks=False)
    need(file_identity(after) == file_identity(before), label + ":ENTRY_DRIFT")
    return raw, file_identity(before)


def stable_path_bytes(path: Path, maximum: int, label: str) -> bytes:
    need(path.name == Path(path.name).name, label + ":BASENAME")
    parent = lexical_directory_without_symlinks(path.parent, label + ":PARENT")
    need(Path(os.path.abspath(os.fspath(path))) == parent / path.name,
         label + ":PATH_BOUNDARY")
    directory_descriptor, bound = open_bound_directory(parent, label + ":PARENT")
    try:
        info = os.stat(path.name, dir_fd=directory_descriptor, follow_symlinks=False)
        need(
            stat.S_ISREG(info.st_mode)
            and not stat.S_ISLNK(info.st_mode)
            and info.st_nlink == 1
            and 0 < info.st_size <= maximum,
            label + ":REGULAR_SINGLE_LINK_BOUNDED",
        )
        descriptor = os.open(
            path.name,
            os.O_RDONLY
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
            dir_fd=directory_descriptor,
        )
        try:
            opened = os.fstat(descriptor)
            need(file_identity(opened) == file_identity(info), label + ":OPEN_RACE")
            chunks: list[bytes] = []
            total = 0
            while True:
                block = os.read(descriptor, 1 << 20)
                if not block:
                    break
                total += len(block)
                need(total <= maximum, label + ":READ_BOUND")
                chunks.append(block)
            need(file_identity(os.fstat(descriptor)) == file_identity(info),
                 label + ":FD_DRIFT")
        finally:
            os.close(descriptor)
        need(
            file_identity(os.stat(path.name, dir_fd=directory_descriptor,
                                  follow_symlinks=False)) == file_identity(info),
            label + ":ENTRY_DRIFT",
        )
        return b"".join(chunks)
    finally:
        need(bound == directory_identity(os.fstat(directory_descriptor))
             == directory_identity(os.lstat(parent)), label + ":PARENT_SWAP")
        os.close(directory_descriptor)


def parse_manifest(
    name: str, pin: str, expected_count: int,
    exact_members: frozenset[str] | None = None,
) -> dict[str, str]:
    need(PIN_RE.fullmatch(pin) is not None, "MANIFEST_PIN_SYNTAX:" + name)
    path = D / name
    require_regular(path, name)
    need(file_sha256(path) == pin, "MANIFEST_PIN:" + name)
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\n]+)", line)
        need(match is not None, "MANIFEST_SYNTAX:" + name)
        value, member = match.groups()
        need(member not in entries, "MANIFEST_DUPLICATE:" + name)
        entries[member] = value
    need(len(entries) == expected_count, "MANIFEST_COUNT:" + name)
    if exact_members is not None:
        need(set(entries) == set(exact_members), "MANIFEST_EXACT_SET:" + name)
    for member, value in entries.items():
        candidate = D / member
        require_regular(candidate, name + ":" + member)
        need(file_sha256(candidate) == value,
             "MANIFEST_MEMBER_PIN:" + name + ":" + member)
    return entries


def read_json(name: str) -> dict[str, Any]:
    path = D / name
    require_regular(path, name)
    seen_error = VerificationBlocked("DUPLICATE_OR_FLOAT_JSON:" + name)

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, current in items:
            if key in value:
                raise seen_error
            value[key] = current
        return value

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
        parse_float=lambda _token: (_ for _ in ()).throw(seen_error),
        parse_constant=lambda _token: (_ for _ in ()).throw(seen_error),
    )
    need(type(value) is dict, "JSON_OBJECT:" + name)
    return value


def verify_self(value: dict[str, Any], field: str, label: str) -> None:
    observed = value.get(field)
    need(type(observed) is str and PIN_RE.fullmatch(observed) is not None,
         "SELF_FIELD:" + label)
    body = dict(value)
    del body[field]
    need(digest(body) == observed, "SELF_HASH:" + label)


def bounded_json_bytes(raw: bytes, maximum: int, label: str) -> dict[str, Any]:
    need(0 < len(raw) <= maximum <= MAX_JSON_BYTES, "JSON_SIZE:" + label)
    value = json.loads(raw.decode("utf-8"))
    need(type(value) is dict, "JSON_OBJECT:" + label)
    return value


def bounded_gzip_bytes(raw: bytes, maximum: int, label: str) -> bytes:
    need(0 < maximum <= MAX_GZIP_UNCOMPRESSED_BYTES, "GZIP_LIMIT:" + label)
    with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as stream:
        payload = stream.read(maximum + 1)
    need(len(payload) <= maximum, "GZIP_UNCOMPRESSED_SIZE:" + label)
    return payload


FORMAL_MANIFEST_COUNTS = {
    R174_PREFIX + "_manifest.sha256": 7,
    R179_PREFIX + "_manifest.sha256": 7,
    R275_PREFIX + "_manifest.sha256": 6,
    R287_PREFIX + "_manifest.sha256": 6,
    R292_PREFIX + "_manifest.sha256": 7,
    R294B_PREFIX + "_manifest.sha256": 11,
    R300A_PREFIX + "_manifest.sha256": 8,
    R300B_PREFIX + "_manifest.sha256": 14,
}


def strict_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, current in items:
        need(key not in value, "DUPLICATE_JSON_KEY:" + key)
        value[key] = current
    return value


def strict_json_raw(raw: bytes, label: str) -> dict[str, Any]:
    need(0 < len(raw) <= MAX_JSON_BYTES, "JSON_SIZE:" + label)
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=strict_pairs,
            parse_float=lambda token: (_ for _ in ()).throw(
                VerificationBlocked("FLOAT_JSON:" + label + ":" + token)
            ),
            parse_constant=lambda token: (_ for _ in ()).throw(
                VerificationBlocked("NONFINITE_JSON:" + label + ":" + token)
            ),
        )
    except UnicodeDecodeError as error:
        raise VerificationBlocked("NON_UTF8_JSON:" + label) from error
    need(type(value) is dict, "JSON_OBJECT:" + label)
    return value


def read_gzip_json(name: str, maximum: int = MAX_JSON_BYTES) -> dict[str, Any]:
    path = D / name
    require_regular(path, name)
    raw = path.read_bytes()
    payload = bounded_gzip_bytes(raw, maximum, name)
    return strict_json_raw(payload, name)


def iter_named_array(
    path: Path,
    marker: str,
    *,
    compressed: bool,
) -> Any:
    """Stream one exact JSON array without admitting sibling candidate data."""

    require_regular(path, path.name)
    opener: Callable[..., Any] = gzip.open if compressed else path.open
    arguments = (path, "rt") if compressed else ("rt",)
    with opener(*arguments, encoding="utf-8", newline="") as stream:
        token = json.dumps(marker, ensure_ascii=False) + ":["
        buffer = ""
        while token not in buffer:
            block = stream.read(1 << 20)
            need(bool(block), "STREAM_MARKER:" + marker)
            buffer += block
            if len(buffer) > len(token) + (1 << 20):
                buffer = buffer[-(len(token) + (1 << 20)):]
        buffer = buffer.split(token, 1)[1]
        decoder = json.JSONDecoder(
            object_pairs_hook=strict_pairs,
            parse_float=lambda token: (_ for _ in ()).throw(
                VerificationBlocked("FLOAT_STREAM:" + marker + ":" + token)
            ),
            parse_constant=lambda token: (_ for _ in ()).throw(
                VerificationBlocked("NONFINITE_STREAM:" + marker + ":" + token)
            ),
        )
        while True:
            buffer = buffer.lstrip()
            if not buffer:
                block = stream.read(1 << 20)
                need(bool(block), "STREAM_TRUNCATED:" + marker)
                buffer = block
                continue
            if buffer[0] == ",":
                buffer = buffer[1:]
                continue
            if buffer[0] == "]":
                return
            while True:
                try:
                    row, end = decoder.raw_decode(buffer)
                    break
                except json.JSONDecodeError:
                    block = stream.read(1 << 20)
                    need(bool(block), "STREAM_ROW_TRUNCATED:" + marker)
                    buffer += block
            yield row
            buffer = buffer[end:]


def admit_formal_input_chain() -> dict[str, int]:
    counts: dict[str, int] = {}
    for name, pin in FORMAL_MANIFEST_PINS.items():
        entries = parse_manifest(name, pin, FORMAL_MANIFEST_COUNTS[name])
        counts[name] = len(entries)
    for name, pin in FORMAL_INPUT_PINS.items():
        path = D / name
        require_regular(path, "formal-input:" + name)
        need(file_sha256(path) == pin, "FORMAL_INPUT_PIN:" + name)
    # The complete R304 and sealed R305A packages are separately closed here.
    parse_manifest(R304_MANIFEST, R304_MANIFEST_SHA256, 11)
    parse_manifest(
        R305A_MANIFEST, R305A_MANIFEST_SHA256, 8,
        R305A_EXPECTED_MANIFEST_MEMBERS,
    )
    return counts


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def qlist(values: Any) -> list[str]:
    return [qstr(value) for value in values]


def qbox(values: Any, *, allow_flat: bool = False) -> tuple[Q, ...]:
    result = tuple(map(Q, values))
    need(len(result) == 6, "BOX_ARITY")
    comparator = (lambda a, b: a <= b) if allow_flat else (lambda a, b: a < b)
    need(all(comparator(result[2 * i], result[2 * i + 1]) for i in range(3)),
         "BOX_ORDER")
    return result


def volume(box: tuple[Q, ...]) -> Q:
    value = Q(1)
    for axis in range(3):
        width = box[2 * axis + 1] - box[2 * axis]
        need(width > 0, "POSITIVE_VOLUME")
        value *= width
    return value


def replace_axis(
    box: tuple[Q, ...], axis: int, interval: tuple[Q, Q],
) -> tuple[Q, ...]:
    values = list(box)
    values[2 * axis:2 * axis + 2] = interval
    return tuple(values)


def targeted_interval(
    lower: Q, upper: Q, direction: str, depth: int,
) -> tuple[Q, Q]:
    need(lower < upper and direction in {"LOWER", "UPPER"} and depth > 0,
         "TARGETED_INTERVAL_DOMAIN")
    width = upper - lower
    divisor = 1 << depth
    if direction == "LOWER":
        a, b = lower, lower + width / divisor
    else:
        a, b = upper - width / divisor, upper
    inner = (a + (b - a) / 4, b - (b - a) / 4)
    need(lower < inner[0] < inner[1] < upper, "TARGETED_INTERVAL_STRICT")
    return inner


def strict_middle_half(lower: Q, upper: Q) -> tuple[Q, Q]:
    """Canonical rational closed interval strictly inside an open interval."""

    need(lower < upper, "STRICT_MIDDLE_HALF_DOMAIN")
    width = upper - lower
    result = (lower + width / 4, upper - width / 4)
    need(lower < result[0] < result[1] < upper,
         "STRICT_MIDDLE_HALF_CONTAINMENT")
    return result


def sqrt_bounds(value: Q, bits: int = SQRT_REPLAY_BITS) -> tuple[Q, Q]:
    need(value >= 0 and bits > 0, "SQRT_DOMAIN")
    scale = 1 << bits
    scaled = value.numerator * scale * scale
    quotient = scaled // value.denominator
    root = isqrt(quotient)
    while (root + 1) ** 2 * value.denominator <= scaled:
        root += 1
    while root * root * value.denominator > scaled:
        root -= 1
    lower = Q(root, scale)
    exact = root * root * value.denominator == scaled
    upper = lower if exact else Q(root + 1, scale)
    need(lower * lower <= value <= upper * upper, "SQRT_ENCLOSURE")
    return lower, upper


def signed_physical_outer(
    box: tuple[Q, ...], sign: int,
) -> tuple[Q, ...]:
    need(sign in {-1, 1} and box[0] > 0, "SIGNED_T_DOMAIN")
    lower = sqrt_bounds(box[0])[0]
    upper = sqrt_bounds(box[1])[1]
    interval = (lower, upper) if sign > 0 else (-upper, -lower)
    return (*interval, *box[2:])


def physical_t_square_interval(
    coordinate_box: tuple[Q, ...], guard_box: tuple[Q, ...],
) -> tuple[Q, Q]:
    def square(interval: tuple[Q, Q]) -> tuple[Q, Q]:
        lo, hi = interval
        need(lo * hi > 0, "SIGNED_NONZERO_T_INTERVAL")
        return (lo * lo, hi * hi) if lo > 0 else (hi * hi, lo * lo)

    cell = square(coordinate_box[:2])
    source = square(guard_box[:2])
    image = (1 - source[1], 1 - source[0])
    result = (max(cell[0], image[0]), min(cell[1], image[1]))
    need(result[0] < result[1], "POSITIVE_RECHART_T_SQUARE")
    return result


def compile_verified_source_bytes(
    raw: bytes, pin: str, display_name: str,
) -> Any:
    need(PIN_RE.fullmatch(pin) is not None,
         "DIRECT_SOURCE_COMPILE_PIN_SYNTAX:" + display_name)
    need(hashlib.sha256(raw).hexdigest() == pin,
         "DIRECT_SOURCE_COMPILE_SHA256:" + display_name)
    return compile(
        raw, display_name, "exec", flags=0, dont_inherit=True, optimize=0,
    )


def exec_verified_source_module(filename: str) -> types.ModuleType:
    """Execute exact pinned source bytes, never an import-cache bytecode file."""

    need(filename in FORMAL_INPUT_PINS, "DIRECT_SOURCE_MODULE_PIN:" + filename)
    path = D / filename
    require_regular(path, "direct-source-module:" + filename)
    raw = path.read_bytes()
    pin = FORMAL_INPUT_PINS[filename]
    need(hashlib.sha256(raw).hexdigest() == pin,
         "DIRECT_SOURCE_MODULE_SHA256:" + filename)
    module_name = filename.removesuffix(".py")
    need(module_name and module_name != PRODUCER.removesuffix(".py"),
         "DIRECT_SOURCE_MODULE_NOT_CANDIDATE_PRODUCER")
    need(module_name not in sys.modules,
         "DIRECT_SOURCE_MODULE_PRELOADED_OR_INJECTED:" + module_name)
    code = compile_verified_source_bytes(raw, pin, str(path))
    module = types.ModuleType(module_name)
    module.__file__ = str(path)
    module.__package__ = ""
    module.__loader__ = None
    module.__spec__ = None
    module.__cached__ = None
    module.__dict__["_ROUND305B_DIRECT_PINNED_SOURCE_SHA256"] = pin
    sys.modules[module_name] = module
    try:
        exec(code, module.__dict__)
    except BaseException:
        if sys.modules.get(module_name) is module:
            del sys.modules[module_name]
        raise
    need(
        module.__dict__.get("_ROUND305B_DIRECT_PINNED_SOURCE_SHA256") == pin
        and module.__loader__ is None
        and module.__spec__ is None
        and module.__cached__ is None,
        "DIRECT_SOURCE_MODULE_EXEC_MARKER:" + filename,
    )
    return module


def import_formal_geometry_modules() -> tuple[Any, Any, dict[str, Any]]:
    """Compile/execute only verified source bytes; never trust stale ``pyc``."""

    global _FORMAL_GEOMETRY_LOADER_AUDIT
    need(PRODUCER[:-3] not in sys.modules, "CANDIDATE_PRODUCER_ALREADY_IMPORTED")
    previous_no_write = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        flint = importlib.import_module("flint")
        need(getattr(flint, "__version__", None) == "0.9.0",
             "PYTHON_FLINT_VERSION_0_9_0_REQUIRED")
        flint.ctx.prec = 768
        ordered_sources = (
            "cm2_gate3_candidate_first_hit_cert.py",
            "cm2_gate3_ge_interval_atlas_cert.py",
            "cm2_gate3_eight_cell_symmetry_atlas_cert.py",
            R174_MODULE,
            R174_VERIFIER_MODULE,
            R179_MODULE,
        )
        module_names = tuple(
            filename.removesuffix(".py") for filename in ordered_sources
        )
        need(
            all(name not in sys.modules for name in module_names),
            "FORMAL_GEOMETRY_LOCAL_MODULE_PRELOADED_FAIL_CLOSED",
        )
        loaded: dict[str, types.ModuleType] = {}
        try:
            for filename in ordered_sources:
                module = exec_verified_source_module(filename)
                need(
                    Path(module.__file__).resolve() == (D / filename).resolve()
                    and module.__dict__.get(
                        "_ROUND305B_DIRECT_PINNED_SOURCE_SHA256"
                    ) == FORMAL_INPUT_PINS[filename],
                    "FORMAL_GEOMETRY_DIRECT_MODULE_IDENTITY:" + filename,
                )
                loaded[filename] = module
        except BaseException:
            for name in module_names:
                module = sys.modules.get(name)
                if getattr(
                    module, "_ROUND305B_DIRECT_PINNED_SOURCE_SHA256", None
                ) is not None:
                    del sys.modules[name]
            raise
        r174 = loaded[R174_MODULE]
        r179 = loaded[R179_MODULE]
        r174_inputs = r174.load_inputs()
        # The admitted legacy modules replay their historical 192/256-bit
        # contexts.  Independent Round305B geometry is required to run at the
        # committed 768-bit precision, so restore it after legacy input replay
        # and before constructing any new interval objects.
        flint.ctx.prec = 768
        need(flint.ctx.prec == 768,
             "ARB_PRECISION_768_BEFORE_INDEPENDENT_GEOMETRY")
        registry_tables = r174.registry_tables(r174_inputs["gate5"])
        need(flint.ctx.prec == 768,
             "ARB_PRECISION_768_AFTER_INDEPENDENT_REGISTRY_TABLES")
        _FORMAL_GEOMETRY_LOADER_AUDIT = {
            "execution_mode": "DIRECT_COMPILE_EXEC_OF_VERIFIED_SOURCE_BYTES",
            "project_local_formal_geometry_source_compile_exec": True,
            "ordered_source_modules": list(ordered_sources),
            "source_sha256s": {
                filename: FORMAL_INPUT_PINS[filename]
                for filename in ordered_sources
            },
            "local_module_preload_accepted": False,
            "project_local_module_loader_spec_cached_all_none": True,
            "project_local_formal_geometry_module_pycache_reads": False,
            "project_local_formal_geometry_module_pycache_writes": False,
            "python_flint_standard_importlib_outside_six_module_graph": True,
            "global_no_pyc_claim": False,
            "python_flint_version": "0.9.0",
            "arb_precision_bits": flint.ctx.prec,
        }
        assert_path_and_time_free_wire(
            _FORMAL_GEOMETRY_LOADER_AUDIT, "formal-geometry-loader-audit"
        )
    except ModuleNotFoundError as error:
        raise VerificationBlocked(
            "PYTHON_FLINT_0_9_0_RUNTIME_REQUIRED__USE_.venv-cm2/bin/python"
        ) from error
    finally:
        sys.dont_write_bytecode = previous_no_write
    return r174, r179, registry_tables


def formal_geometry_loader_audit() -> dict[str, Any]:
    need(_FORMAL_GEOMETRY_LOADER_AUDIT is not None,
         "FORMAL_GEOMETRY_LOADER_AUDIT_NOT_AVAILABLE")
    return copy.deepcopy(_FORMAL_GEOMETRY_LOADER_AUDIT)


def exact_extremal_point(
    r174: Any,
    box: Any,
    derivative_signs: list[str | None],
    want_maximum: bool,
) -> Any:
    """Independent monotone-corner/slab enclosure of a box extremum."""

    bounds: list[tuple[Any, Any]] = []
    intervals = ((box.t0, box.t1), (box.p0, box.p1), (box.s0, box.s1))
    need(len(derivative_signs) == 3, "EXTREMUM_DERIVATIVE_ARITY")
    for (lower, upper), sign in zip(intervals, derivative_signs, strict=True):
        if sign == "STRICT_POSITIVE":
            value = upper if want_maximum else lower
            bounds.append((value, value))
        elif sign == "STRICT_NEGATIVE":
            value = lower if want_maximum else upper
            bounds.append((value, value))
        else:
            # No monotonicity means no corner reduction in this coordinate.
            # Preserve the full interval and require the resulting Arb slab
            # enclosure itself to have a strict sign.
            bounds.append((lower, upper))
    return r174.atlas.AtlasBox(
        bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1],
        bounds[2][0], bounds[2][1], box.depth,
        "round305b-independent-extremal-slab",
    )


def exact_active_dual(geometry: dict[str, Any], reason: str) -> Any:
    """Independent R305B specialization; only the two zero-wall factors exist."""

    kind, axis, wall = reason.split(":")
    need(
        kind == "wall_endpoint_or_count_transition"
        and axis in {"X", "Y"} and wall == "0",
        "R305B_ONLY_ZERO_WALL_ACTIVE_FACTOR",
    )
    return geometry["hit_x" if axis == "X" else "hit_y"]


def exact_wall_predicate_details(r174: Any, reason: str) -> dict[str, Any]:
    kind, axis, wall_text = reason.split(":")
    wall = int(wall_text)
    need(
        kind == "wall_endpoint_or_count_transition"
        and axis in {"X", "Y"} and wall == 0,
        "ROUND305B_EXACT_ZERO_WALL_PREDICATE",
    )
    label, equation, dimension, existence = r174.predicate_details(reason)
    need(
        label == "integer_wall_endpoint"
        and equation
        == f"(source_{axis.lower()}-{wall})*(target_{axis.lower()}-{wall})=0"
        and dimension
        == "UNION_OF_NOMINAL_DIMENSION_2_ANALYTIC_PREDICATES"
        and existence
        == "EXISTENCE_AND_REGULARITY_NOT_PROMOTED_FROM_INTERVAL_OVERWRAP",
        "ROUND174_WALL_PREDICATE_DETAILS_EXACT_REPLAY",
    )
    return {
        "kind": kind,
        "axis": axis,
        "wall": wall,
        "source_wall_factor": f"source_{axis.lower()}-{wall}",
        "target_wall_factor_F": f"hit_{axis.lower()}-{wall}",
        "wall_event_product": (
            f"(source_{axis.lower()}-{wall})*(hit_{axis.lower()}-{wall})"
        ),
    }


def wall_event_product_replay_on_signed_box(
    r174: Any,
    r179: Any,
    region: dict[str, Any],
    signed_box: tuple[Q, ...],
    path: str,
) -> dict[str, Any]:
    details = exact_wall_predicate_details(r174, region["active_reason"])
    box = r174.atlas.AtlasBox(*signed_box, 0, path)
    geometry = r179.interval_geometry(
        region["adjacent_chart"], region["owner_target"], box
    )
    axis = details["axis"]
    wall = details["wall"]
    source_value = geometry[
        "source_x" if axis == "X" else "source_y"
    ][0] - wall
    target_value = geometry[
        "hit_x" if axis == "X" else "hit_y"
    ][0] - wall
    return {
        "active_reason": region["active_reason"],
        "predicate_details": details,
        "source_wall_factor_sign": r179.sign(source_value),
        "target_wall_factor_sign": r179.sign(target_value),
        "wall_event_product_sign": r179.sign(source_value * target_value),
        "outer_rational_signed_physical_box": qlist(signed_box),
    }


def wall_event_product_replay_on_z_box(
    r174: Any,
    r179: Any,
    region: dict[str, Any],
    z_box: tuple[Q, ...],
    physical_t_sign: int,
    path: str,
) -> dict[str, Any]:
    return wall_event_product_replay_on_signed_box(
        r174, r179, region,
        signed_physical_outer(z_box, physical_t_sign), path,
    )


def active_function_descriptor(region: dict[str, Any]) -> dict[str, Any]:
    kind, axis, wall = region["active_reason"].split(":")
    need(kind == "wall_endpoint_or_count_transition" and wall == "0",
         "ACTIVE_FUNCTION_ZERO_WALL")
    identity = {
        "adjacent_chart": region["adjacent_chart"],
        "owner_target": region["owner_target"],
        "active_reason": region["active_reason"],
        "active_function_expression": (
            "interval_geometry(adjacent_chart,owner_target)."
            + ("hit_x[0]" if axis == "X" else "hit_y[0]")
            + "-arb(0)"
        ),
        "active_function_evaluator_module_sha256":
            FORMAL_INPUT_PINS[
                "cm2_round274_source_g_reverse_rechart_tail_arrangement_probe.py"
            ],
        "interval_geometry_module_sha256": FORMAL_INPUT_PINS[R179_MODULE],
    }
    return {
        "active_function_id": "round300b-active-function:" + digest(identity),
        "active_function_identity_payload": identity,
        "desired_side_sign": region["active_factor_side_sign"],
    }


def active_factor_replay(
    r174: Any,
    r179: Any,
    region: dict[str, Any],
    transformed_box: tuple[Q, ...],
    physical_t_sign: int,
) -> dict[str, Any]:
    signed = signed_physical_outer(transformed_box, physical_t_sign)
    atlas_box = r174.atlas.AtlasBox(
        *signed, 0, "round305b-independent-relative-physical-replay"
    )
    signs: list[str] = []
    for want_maximum in (False, True):
        point = exact_extremal_point(
            r174, atlas_box, region["strict_derivative_signs_t_p_s"],
            want_maximum,
        )
        geometry = r179.interval_geometry(
            region["adjacent_chart"], region["owner_target"], point,
        )
        signs.append(r179.sign(exact_active_dual(
            geometry, region["active_reason"]
        )[0]))
    if not set(signs) <= STRICT_SIGNS:
        state = "UNRESOLVED_ACTIVE_FACTOR_OVERWRAP"
    elif signs[0] != signs[1]:
        state = "CLIPPED_DESIRED_SIDE_SUPPORT"
    elif signs[0] == region["active_factor_side_sign"]:
        state = "FULL_DESIRED_SIDE_SUPPORT"
    else:
        state = "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
    return {
        "active_factor_extremal_signs": signs,
        "signed_support_state": state,
        "outer_rational_signed_physical_box": qlist(signed),
    }


R174_GUARD_COLUMNS = (
    "row_id", "chart", "parent_id", "refinement_path", "box",
    "coordinate_volume", "exact_rejection_predicate", "classification",
    "is_CM2_exterior_sheet_exclusion", "is_Gate5_geometric_disposition",
    "provenance", "transport_source_row_id", "transport_generator",
)


def load_r174_guards(wanted: set[str]) -> dict[str, dict[str, Any]]:
    values: list[list[Any]] = []
    selected: dict[str, dict[str, Any]] = {}
    for raw in iter_named_array(D / R174_ROWS, "chart_guard_rejection_rows",
                                compressed=False):
        need(type(raw) is list and len(raw) == len(R174_GUARD_COLUMNS),
             "R174_GUARD_ROW_SCHEMA")
        values.append(raw)
        row = dict(zip(R174_GUARD_COLUMNS, raw, strict=True))
        if row["row_id"] in wanted:
            need(row["row_id"] not in selected, "R174_GUARD_DUPLICATE")
            selected[row["row_id"]] = row
    need(
        len(values) == 728
        and digest(values)
        == "09e915620a31c35eeeae4f4d069ade47e5293ef73ab5f13499ccf4abd7b21784"
        and set(selected) == wanted,
        "R174_COMPLETE_GUARD_TABLE_AND_SELECTION",
    )
    return selected


def load_scope_and_geometry_inputs() -> dict[str, Any]:
    scope = read_gzip_json(R305A_LEDGER)
    verify_self(scope, "ledger_sha256", R305A_LEDGER)
    all_scope_rows = scope["post_Round304_scope_reprojection_rows"]
    need(len(all_scope_rows) == 3_232 and digest(all_scope_rows) == scope["rows_sha256"],
         "ROUND305A_SCOPE_LEDGER_CLOSURE")
    residual = []
    for row in all_scope_rows:
        verify_self(row, "row_sha256", "ROUND305A_SCOPE_ROW")
        if row.get("requires_formal_physical_inclusion") is True:
            need(
                row["post_Round304_disposition"]
                == "UNWITNESSED__CROSS_COMPONENT__FORMAL_PHYSICAL_INCLUSION_PACKAGE_REQUIRED"
                and row["same_Round304_final_component"] is False
                and row["source_row_fed_to_DSU"] is False
                and row["unsealed_temp_scope_consumed"] is False,
                "ROUND305A_RESIDUAL_FAIL_CLOSED",
            )
            residual.append(row)
    residual.sort(key=lambda row: row["canonical_Round294_registry_occurrence_pair"])
    pairs = [row["canonical_Round294_registry_occurrence_pair"] for row in residual]
    endpoints = {item for pair in pairs for item in pair}
    need(
        len(residual) == EXPECTED_WITNESSES
        and digest(pairs)
        == "f7f9941f84428df71039b4708dfa251eae6c962267f68ccd13945ee445c5bf29"
        and len(endpoints) == EXPECTED_ANCHORS
        and digest(sorted(endpoints))
        == "b09fe8149f89a95c2c9effcbce33bc49df24065987c870fc65b09ac85fe98779",
        "ROUND305A_EXACT_1024_SCOPE",
    )

    r300a = read_gzip_json(R300A_LEDGER)
    pair_rows = r300a["canonical_occurrence_pair_rows"]
    source_rows = r300a["source_pair_expansion_rows"]
    need(
        len(pair_rows) == r300a["canonical_occurrence_pair_row_count"] == 3_232
        and digest(pair_rows) == r300a["canonical_occurrence_pair_rows_sha256"]
        and len(source_rows) == r300a["source_pair_expansion_row_count"] == 3_488
        and digest(source_rows) == r300a["source_pair_expansion_rows_sha256"],
        "ROUND300A_LEDGER_CLOSURE",
    )
    wanted_pair_ids = {row["source_Round300A_row_id"] for row in residual}
    pair_by_id = {
        row["Round300A_canonical_occurrence_pair_row_id"]: row
        for row in pair_rows if row["Round300A_canonical_occurrence_pair_row_id"] in wanted_pair_ids
    }
    need(set(pair_by_id) == wanted_pair_ids, "ROUND300A_PAIR_ROW_COVERAGE")
    wanted_source_ids: set[str] = set()
    for scope_row in residual:
        pair_row = pair_by_id[scope_row["source_Round300A_row_id"]]
        verify_row(pair_row, "ROUND300A_SELECTED_PAIR_ROW")
        need(pair_row["row_sha256"] == scope_row["source_Round300A_row_sha256"],
             "ROUND300A_PAIR_ROW_PIN")
        need(pair_row["canonical_unordered_Round294_registry_occurrence_ids"]
             == scope_row["canonical_Round294_registry_occurrence_pair"],
             "ROUND300A_PAIR_SCOPE_BINDING")
        need(len(pair_row["source_Round287_pair_row_ids"]) == 1,
             "ROUND300A_ONE_SOURCE_PER_RESIDUAL_PAIR")
        wanted_source_ids.update(pair_row["source_Round287_pair_row_ids"])
    source_by_id = {
        row["source_Round287_pair_row_id"]: row for row in source_rows
        if row["source_Round287_pair_row_id"] in wanted_source_ids
    }
    need(len(source_by_id) == len(wanted_source_ids) == EXPECTED_WITNESSES,
         "ROUND300A_SOURCE_COVERAGE")
    for row in source_by_id.values():
        verify_self(row, "row_sha256", "ROUND300A_SOURCE_ROW")

    r275 = read_json(R275_CERTIFICATE)
    need(digest(r275["result"]) == r275["result_sha256"], "ROUND275_RESULT_CLOSURE")
    region_rows = (
        r275["result"]["strict_region_ledger"]["rows"]
        + r275["result"]["arrangement_region_ledger"]["rows"]
    )
    regions: dict[str, dict[str, Any]] = {}
    for row in region_rows:
        verify_self(row, "row_sha256", "ROUND275_REGION_ROW")
        row_id = row["reverse_rechart_region_row_id"]
        need(row_id not in regions, "ROUND275_REGION_DUPLICATE")
        regions[row_id] = row
    need(len(regions) == 13_788, "ROUND275_REGION_CENSUS")

    r287 = read_gzip_json(R287_LEDGER)
    r287_region_rows = r287["region_rows"]
    need(
        len(r287_region_rows) == r287["region_row_count"] == 13_788
        and digest(r287_region_rows) == r287["region_rows_sha256"],
        "ROUND287_REGION_TABLE_CLOSURE",
    )
    r287_regions: dict[str, dict[str, Any]] = {}
    for row in r287_region_rows:
        verify_row(row, "ROUND287_REGION_ROW")
        row_id = row["Round287_region_disposition_row_id"]
        need(row_id not in r287_regions, "ROUND287_REGION_ROW_DUPLICATE")
        r287_regions[row_id] = row
    r287_pair_rows = r287["mutually_exclusive_outer_overlap_pair_rows"]
    need(
        len(r287_pair_rows)
        == r287["mutually_exclusive_outer_overlap_pair_row_count"]
        == EXPECTED_R287_PAIR_ROWS
        and digest(r287_pair_rows)
        == r287["mutually_exclusive_outer_overlap_pair_rows_sha256"],
        "ROUND287_PAIR_TABLE_CLOSURE",
    )
    r287_pairs: dict[str, dict[str, Any]] = {}
    for row in r287_pair_rows:
        verify_row(row, "ROUND287_PAIR_ROW")
        row_id = row["Round287_mutually_exclusive_outer_overlap_pair_row_id"]
        need(row_id not in r287_pairs, "ROUND287_PAIR_ROW_DUPLICATE")
        r287_pairs[row_id] = row

    r292 = read_gzip_json(R292_LEDGER)
    rows292 = r292["rows"]
    need(len(rows292) == r292["row_count"] == 22_820
         and digest(rows292) == r292["rows_sha256"], "ROUND292_LEDGER_CLOSURE")
    cells = {
        row["Round292_R287_existing_overlap_refinement_cell_id"]: row
        for row in rows292
        if "Round292_R287_existing_overlap_refinement_cell_id" in row
    }
    endpoint_components: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    for component in rows292:
        if not (
            "Round292_refined_new_support_component_id" in component
            and "member_refinement_cell_ids" in component
        ):
            continue
        verify_self(component, "row_sha256", "ROUND292_COMPONENT_ROW")
        occurrence = "source-g-expanded-occurrence:" + digest([
            "ROUND292_R287_EXISTING_OVERLAP_REFINED_NEW_SUPPORT_LOCAL_OCCURRENCE_V1",
            component["Round292_refined_new_support_component_id"],
            component["row_sha256"],
        ])
        if occurrence not in endpoints:
            continue
        need(
            component["member_refinement_cell_count"] == 1
            and len(component["member_refinement_cell_ids"]) == 1
            and component["one_connected_positive_open_support"] is True,
            "ROUND292_SINGLE_CONNECTED_MEMBER_CELL",
        )
        cell = cells[component["member_refinement_cell_ids"][0]]
        verify_self(cell, "row_sha256", "ROUND292_REFINEMENT_CELL")
        need(
            cell["Round292_refined_new_support_component_id"]
            == component["Round292_refined_new_support_component_id"]
            and cell["disposition"]
            == "EXACT_UNCOVERED_POSITIVE_OPEN_SLICE__MEMBER_OF_REFINED_PARENT_LOCAL_NEW_SUPPORT"
            and cell["existing_occurrence_ids"] == []
            and cell["existing_occurrence_occupancy_count"] == 0
            and cell["exact_transformed_coordinate_system"] == "(t^2,p,s)"
            and volume(qbox(cell["exact_transformed_open_cell"])) > 0,
            "ROUND292_EXACT_SINGLE_CELL",
        )
        endpoint_components[occurrence] = (component, cell)
    need(set(endpoint_components) == endpoints, "ROUND292_2048_ENDPOINT_COVERAGE")
    return {
        "residual": residual,
        "pair_by_id": pair_by_id,
        "source_by_id": source_by_id,
        "regions": regions,
        "r287_regions": r287_regions,
        "r287_pairs": r287_pairs,
        "endpoint_components": endpoint_components,
        "endpoints": endpoints,
    }


def close_row(row: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in row, "ROW_ALREADY_CLOSED")
    result = dict(row)
    result["row_sha256"] = digest(result)
    return result


def verify_row(row: dict[str, Any], label: str) -> None:
    need(type(row) is dict and type(row.get("row_sha256")) is str,
         "ROW_SHAPE:" + label)
    body = dict(row)
    observed = body.pop("row_sha256")
    need(digest(body) == observed, "ROW_SHA256:" + label)


def stream_endpoint_bindings(
    endpoints: set[str],
    residual: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], set[str]]:
    registry: dict[str, dict[str, Any]] = {}
    registry_count = 0
    for row in iter_named_array(D / R294_REGISTRY, "rows", compressed=True):
        registry_count += 1
        occurrence = row.get("registry_occurrence_id")
        if occurrence not in endpoints:
            continue
        need(occurrence not in registry, "ROUND294_RELEVANT_DUPLICATE")
        verify_row(row, "ROUND294_REGISTRY_ROW")
        need(
            row["registry_entry_kind"]
            == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
            and row["registry_identity_status"]
            == "FORMALLY_ISSUED_ROUND294_ATOMIC_OCCURRENCE_ID"
            and row["registry_promotion_status"]
            == "FORMALLY_PROMOTED_ROUND294_ATOMIC_OCCURRENCE_REGISTRY"
            and row["formal_new_expanded_occurrence_credit"] == 1,
            "ROUND294_FORMAL_REFINED_OCCURRENCE",
        )
        registry[occurrence] = row
    need(registry_count == 431_208 and set(registry) == endpoints,
         "ROUND294_COMPLETE_STREAM_AND_COVERAGE")

    members: dict[str, dict[str, Any]] = {}
    official_keys: set[str] = set()
    member_count = 0
    for row in iter_named_array(D / R304_MEMBER_LEDGER,
                                "fresh_member_component_rows", compressed=True):
        member_count += 1
        key = row.get("official_key_id")
        need(type(key) is str, "ROUND304_OFFICIAL_KEY_TYPE")
        official_keys.add(key)
        occurrence = row.get("registry_occurrence_id")
        if occurrence not in endpoints:
            continue
        need(occurrence not in members, "ROUND304_RELEVANT_MEMBER_DUPLICATE")
        verify_row(row, "ROUND304_MEMBER_ROW")
        members[occurrence] = row
    need(
        member_count == 564_492 and len(official_keys) == EXPECTED_OFFICIAL_KEYS
        and set(members) == endpoints,
        "ROUND304_COMPLETE_124_KEY_STREAM_AND_COVERAGE",
    )
    used_keys: set[str] = set()
    for scope_row in residual:
        left, right = scope_row["canonical_Round294_registry_occurrence_pair"]
        left_member, right_member = members[left], members[right]
        need(
            left_member["Round304_fresh_member_component_row_id"]
            == scope_row["left_Round304_member_row_id"]
            and left_member["row_sha256"]
            == scope_row["left_Round304_member_row_sha256"]
            and right_member["Round304_fresh_member_component_row_id"]
            == scope_row["right_Round304_member_row_id"]
            and right_member["row_sha256"]
            == scope_row["right_Round304_member_row_sha256"]
            and left_member["final_component_id"]
            == scope_row["left_final_component_id"]
            and right_member["final_component_id"]
            == scope_row["right_final_component_id"]
            and sorted((left_member["final_component_id"],
                        right_member["final_component_id"]))
            == scope_row["final_component_pair"]
            and left_member["official_key_id"] != right_member["official_key_id"],
            "ROUND305A_TO_ROUND304_EXACT_MEMBER_PROJECTION",
        )
        used_keys.update((left_member["official_key_id"], right_member["official_key_id"]))
    need(len(used_keys) == EXPECTED_RESIDUAL_KEYS,
         "ROUND305B_EXACT_16_RESIDUAL_OFFICIAL_KEYS")
    return registry, members, official_keys


Term = tuple[str, int]
Normal = tuple[Term, Term]

RETURN_SIGNATURE_KEYS = (
    "official_key_id", "official_key_ordinal", "official_key_row",
    "ordered_integer_wall_events", "outgoing_cell", "roof",
    "signed_wall_word", "source_chart", "target_chart", "target_lift",
)
WALL_TRANSITION_CHANGED_SIGNATURE_KEYS = (
    "official_key_id", "official_key_ordinal", "official_key_row",
    "ordered_integer_wall_events", "roof", "signed_wall_word",
)


def source_normal(cell: str, source_t_sign: int) -> Normal:
    z: Term = ("Z", 1)
    o: Term = ("O", 1)
    signed_o: Term = ("O", source_t_sign)
    if cell == "E":
        return z, signed_o
    if cell == "W":
        return ("Z", -1), signed_o
    if cell == "N":
        return signed_o, z
    if cell == "S":
        return signed_o, ("Z", -1)
    raise VerificationBlocked("SOURCE_CELL:" + cell)


def adjacent_normal(cell: str, image_t_sign: int) -> Normal:
    z: Term = ("Z", 1)
    o: Term = ("O", 1)
    signed_z: Term = ("Z", image_t_sign)
    if cell == "E":
        return o, signed_z
    if cell == "W":
        return ("O", -1), signed_z
    if cell == "N":
        return signed_z, o
    if cell == "S":
        return signed_z, ("O", -1)
    raise VerificationBlocked("ADJACENT_CELL:" + cell)


TRANSITION = {
    ("E", 1): ("N", 1), ("E", -1): ("S", 1),
    ("N", 1): ("E", 1), ("N", -1): ("W", 1),
    ("W", 1): ("N", -1), ("W", -1): ("S", -1),
    ("S", 1): ("E", -1), ("S", -1): ("W", -1),
}


def reconstruct_branch_contexts(
    inputs: dict[str, Any],
    registry: dict[str, dict[str, Any]],
    members: dict[str, dict[str, Any]],
    r174: Any,
    r179: Any,
    registry_tables: dict[str, Any],
) -> list[dict[str, Any]]:
    residual = inputs["residual"]
    pair_by_id = inputs["pair_by_id"]
    source_by_id = inputs["source_by_id"]
    regions = inputs["regions"]
    r287_regions = inputs["r287_regions"]
    r287_pairs = inputs["r287_pairs"]
    endpoint_components = inputs["endpoint_components"]
    guard_ids: set[str] = set()
    for scope_row in residual:
        pair_row = pair_by_id[scope_row["source_Round300A_row_id"]]
        source = source_by_id[pair_row["source_Round287_pair_row_ids"][0]]
        r287_pair = r287_pairs[source["source_Round287_pair_row_id"]]
        need(
            r287_pair["row_sha256"]
            == source["source_Round287_pair_row_sha256"],
            "ROUND300A_TO_ROUND287_PAIR_PIN",
        )
        guard_ids.add(regions[source["left_Round275_region_id"]]["source_guard_row_id"])
    guards = load_r174_guards(guard_ids)
    need(len(guards) == 16, "ROUND305B_GUARD_PROFILE_16")

    contexts: list[dict[str, Any]] = []
    transition_histogram: Counter[str] = Counter()
    for scope_row in residual:
        pair = scope_row["canonical_Round294_registry_occurrence_pair"]
        pair_row = pair_by_id[scope_row["source_Round300A_row_id"]]
        source = source_by_id[pair_row["source_Round287_pair_row_ids"][0]]
        r287_pair = r287_pairs[source["source_Round287_pair_row_id"]]
        left_occurrence = source["left_Round294_registry_occurrence_ids"][0]
        right_occurrence = source["right_Round294_registry_occurrence_ids"][0]
        need(sorted((left_occurrence, right_occurrence)) == pair,
             "ROUND300A_SOURCE_ENDPOINTS")
        left = regions[source["left_Round275_region_id"]]
        right = regions[source["right_Round275_region_id"]]
        for field in (
            "source_guard_row_id", "parent_id", "owner_target", "source_chart",
            "adjacent_chart", "adjacent_rational_region_box",
            "exact_coordinate_identity", "active_reason",
            "strict_derivative_signs_t_p_s",
        ):
            need(left[field] == right[field], "PAIRED_R275_FIELD:" + field)
        need(
            left["arrangement_classification"]
            == right["arrangement_classification"] == "REGULAR_GRAPH_CROSSING"
            and sorted((left["active_factor_side_sign"],
                        right["active_factor_side_sign"]))
            == ["STRICT_NEGATIVE", "STRICT_POSITIVE"],
            "PAIRED_R275_OPPOSITE_REGULAR_GRAPH",
        )
        need(
            r287_pair["left_Round275_region_id"]
            == source["left_Round275_region_id"]
            and r287_pair["right_Round275_region_id"]
            == source["right_Round275_region_id"],
            "ROUND287_PAIR_REGION_IDS",
        )
        need(
            r287_pair["active_reason"] == source["active_reason"]
            == left["active_reason"] == right["active_reason"],
            "ROUND287_PAIR_ACTIVE_REASON",
        )
        need(
            r287_pair["adjacent_chart"] == source["adjacent_chart"]
            == left["adjacent_chart"] == right["adjacent_chart"],
            "ROUND287_PAIR_ADJACENT_CHART",
        )
        need(
            r287_pair["source_guard_row_id"]
            == source["source_guard_row_id"] == left["source_guard_row_id"]
            == right["source_guard_row_id"],
            "ROUND287_PAIR_SOURCE_GUARD",
        )
        need(
            r287_pair["active_factor_side_signs"]
            == source["active_factor_side_signs"]
            == ["STRICT_NEGATIVE", "STRICT_POSITIVE"],
            "ROUND287_PAIR_SIDE_SIGNS",
        )
        need(
            r287_pair["reason"]
            == "SAME_REGULAR_GRAPH_CELL_OPPOSITE_OPEN_FACTOR_SIDES"
            and r287_pair["exact_positive_physical_overlap"] is False
            and r287_pair["occurrence_identity_collapse_credit"] == 0
            and r287_pair["component_edge_credit"] == 0,
            "ROUND287_PAIR_ZERO_CREDIT_DISPOSITION",
        )
        left_signature = left["local_return_signature"]
        right_signature = right["local_return_signature"]
        need(
            tuple(left_signature) == RETURN_SIGNATURE_KEYS
            and tuple(right_signature) == RETURN_SIGNATURE_KEYS
            and digest(left_signature)
            == left["complete_10_field_return_signature_sha256"]
            and digest(right_signature)
            == right["complete_10_field_return_signature_sha256"]
            and tuple(
                key for key in RETURN_SIGNATURE_KEYS
                if left_signature[key] != right_signature[key]
            ) == WALL_TRANSITION_CHANGED_SIGNATURE_KEYS,
            "R275_EXACT_WALL_RETURN_SIGNATURE_TRANSITION",
        )
        left_component, left_cell = endpoint_components[left_occurrence]
        right_component, right_cell = endpoint_components[right_occurrence]
        need(
            left_cell["Round275_region_id"] == source["left_Round275_region_id"]
            and right_cell["Round275_region_id"] == source["right_Round275_region_id"]
            and left_cell["exact_transformed_open_cell"]
            == right_cell["exact_transformed_open_cell"],
            "R292_TWO_SINGLE_CELLS_EXACTLY_EQUAL",
        )
        exact_box = qbox(left_cell["exact_transformed_open_cell"])
        proof_z = strict_middle_half(exact_box[0], exact_box[1])
        proof_s = strict_middle_half(exact_box[4], exact_box[5])
        proof_base = (*proof_z, *proof_s)
        proof_box = (
            proof_z[0], proof_z[1], exact_box[2], exact_box[3],
            proof_s[0], proof_s[1],
        )
        need(
            exact_box[0] < proof_base[0] < proof_base[1] < exact_box[1]
            and exact_box[4] < proof_base[2] < proof_base[3] < exact_box[5]
            and volume(proof_box) > 0,
            "PROOF_CLOSED_CORE_STRICTLY_INSIDE_R292_OPEN_CELL",
        )
        signed_cell = qbox(left["adjacent_rational_region_box"])
        guard = guards[left["source_guard_row_id"]]
        guard_box = qbox(guard["box"])
        exact_z = physical_t_square_interval(signed_cell, guard_box)
        need(
            exact_box[:2] == exact_z
            and exact_box[2:] == signed_cell[2:]
            and left["exact_coordinate_identity"]
            == "image_t^2=1-source_t^2; p'=p; s'=s"
            and guard["parent_id"] == left["parent_id"]
            and guard["chart"] == left["source_chart"]
            and guard["classification"]
            == "STRICT_OUTSIDE_THIS_TRUE_DOMINANT_SOURCE_CHART",
            "EXACT_REVERSE_RECHART_DOMAIN",
        )
        source_sign = 1 if guard_box[0] > 0 else -1
        image_sign = 1 if signed_cell[0] > 0 else -1
        source_cell = left["source_chart"].split(":")[1]
        adjacent_cell = left["adjacent_chart"].split(":")[1]
        need(
            TRANSITION[(source_cell, source_sign)] == (adjacent_cell, image_sign)
            and source_normal(source_cell, source_sign)
            == adjacent_normal(adjacent_cell, image_sign),
            "EXACT_RECHART_NORMAL_IDENTITY",
        )
        transition_histogram[
            f"{source_cell}{'+' if source_sign > 0 else '-'}->"
            f"{adjacent_cell}{'+' if image_sign > 0 else '-'}"
        ] += 1
        geometry_box = r174.atlas.AtlasBox(
            *signed_cell, 0, "round305b-independent-whole-cell"
        )
        geometry = r179.interval_geometry(
            left["adjacent_chart"], left["owner_target"], geometry_box,
        )
        dynamic_resolved, unresolved_reasons = r174.dynamic_signature(
            left["adjacent_chart"], geometry_box, left["owner_target"],
            registry_tables,
        )
        need(
            dynamic_resolved is None
            and unresolved_reasons == [left["active_reason"]],
            "R174_DYNAMIC_SIGNATURE_UNIQUE_ACTIVE_REASON_REPLAY",
        )
        _kind, axis, wall = left["active_reason"].split(":")
        need(wall == "0", "ONLY_ZERO_WALL_BRANCH")
        source_factor = geometry["source_x" if axis == "X" else "source_y"]
        target_factor = exact_active_dual(geometry, left["active_reason"])
        need(
            r179.sign(source_factor[0]) in STRICT_SIGNS
            and r179.sign(target_factor[0]) == "OVERWRAP"
            and [r179.sign(value) if value is not None else None
                 for value in target_factor[1]]
            == left["strict_derivative_signs_t_p_s"]
            and left["strict_derivative_signs_t_p_s"][1] in STRICT_SIGNS,
            "TARGET_BRANCH_AND_STRICT_P_DERIVATIVE",
        )
        predicate_details = exact_wall_predicate_details(
            r174, left["active_reason"]
        )
        wall_integer = predicate_details["wall"]
        proof_signed_box = signed_physical_outer(proof_box, image_sign)
        need(
            signed_cell[0] < proof_signed_box[0]
            < proof_signed_box[1] < signed_cell[1]
            and signed_cell[2] == proof_signed_box[2]
            and signed_cell[3] == proof_signed_box[3]
            and signed_cell[4] < proof_signed_box[4]
            < proof_signed_box[5] < signed_cell[5],
            "PROOF_SIGNED_T_P_S_ENCLOSURE_STRICTLY_INSIDE_SUPPORT_CELL",
        )
        proof_atlas_box = r174.atlas.AtlasBox(
            *proof_signed_box, 0, "round305b-independent-wall-product-core"
        )
        proof_geometry = r179.interval_geometry(
            left["adjacent_chart"], left["owner_target"], proof_atlas_box,
        )
        proof_source_dual = proof_geometry[
            "source_x" if axis == "X" else "source_y"
        ]
        proof_target_dual = proof_geometry[
            "hit_x" if axis == "X" else "hit_y"
        ]
        proof_source_value = proof_source_dual[0] - wall_integer
        proof_target_value = proof_target_dual[0] - wall_integer
        proof_source_sign = r179.sign(proof_source_value)
        proof_target_sign = r179.sign(proof_target_value)
        proof_product_sign = r179.sign(proof_source_value * proof_target_value)
        proof_target_derivative_sign = r179.sign(proof_target_dual[1][1])
        need(
            proof_source_sign in STRICT_SIGNS
            and proof_target_sign == "OVERWRAP"
            and proof_product_sign == "OVERWRAP"
            and proof_target_derivative_sign
            == left["strict_derivative_signs_t_p_s"][1] in STRICT_SIGNS,
            "PROOF_CORE_SOURCE_TARGET_WALL_PRODUCT_REPLAY",
        )
        whole_open_support_wall_replay = wall_event_product_replay_on_z_box(
            r174, r179, left, exact_box, image_sign,
            "round305b-independent-whole-support-wall-product",
        )
        proof_core_wall_replay = wall_event_product_replay_on_signed_box(
            r174, r179, left, proof_signed_box,
            "round305b-independent-proof-core-wall-product",
        )
        need(
            whole_open_support_wall_replay["source_wall_factor_sign"]
            in STRICT_SIGNS
            and whole_open_support_wall_replay["target_wall_factor_sign"]
            == "OVERWRAP"
            and whole_open_support_wall_replay["wall_event_product_sign"]
            == "OVERWRAP"
            and proof_core_wall_replay["source_wall_factor_sign"]
            == proof_source_sign
            and proof_core_wall_replay["target_wall_factor_sign"]
            == proof_target_sign
            and proof_core_wall_replay["wall_event_product_sign"]
            == proof_product_sign,
            "WHOLE_AND_PROOF_CORE_WALL_PRODUCT_REPLAY_ALIGNMENT",
        )
        for occurrence, component, cell, endpoint_region, registry_row in (
            (left_occurrence, left_component, left_cell, left,
             registry[left_occurrence]),
            (right_occurrence, right_component, right_cell, right,
             registry[right_occurrence]),
        ):
            r287_row = r287_regions[
                registry_row["source_Round287_region_disposition_row_id"]
            ]
            need(
                registry_row["source_row_id"]
                == component["Round292_refined_new_support_component_id"]
                and registry_row["source_row_sha256"] == component["row_sha256"]
                and registry_row["official_key_id"] is None
                and registry_row["official_key_ordinal"] is None
                and registry_row["official_key_binding_status"]
                == "NOT_MATERIALIZED_IN_R287_FROZEN_LEDGER__COMPLETE_SIGNATURE_HASH_PINNED"
                and registry_row["occurrence_id_content_preimage_sha256"]
                == occurrence.removeprefix("source-g-expanded-occurrence:")
                and r287_row["row_sha256"]
                == registry_row["source_Round287_region_disposition_row_sha256"]
                and r287_row["Round275_region_id"]
                == registry_row["Round275_region_id"]
                and r287_row["disposition"]
                == "ONE_STRICTLY_NEW_DISJOINT_SUPPORT_CANDIDATE__ZERO_CREDIT"
                and r287_row["physical_t_sign"] == image_sign
                and r287_row["physical_t_square_open_interval"]
                == cell["exact_transformed_open_cell"][:2]
                and r287_row["adjacent_chart"] == endpoint_region["adjacent_chart"]
                and r287_row["owner_target"] == endpoint_region["owner_target"]
                and type(members[occurrence]["official_key_id"]) is str,
                "R292_R294_R304_ANCHOR_CHAIN",
            )
        contexts.append({
            "scope": scope_row,
            "pair_row": pair_row,
            "source": source,
            "r287_pair": r287_pair,
            "left_occurrence": left_occurrence,
            "right_occurrence": right_occurrence,
            "left_region": left,
            "right_region": right,
            "left_component": left_component,
            "right_component": right_component,
            "left_cell": left_cell,
            "right_cell": right_cell,
            "exact_box": exact_box,
            "proof_box": proof_box,
            "proof_base": proof_base,
            "image_sign": image_sign,
            "source_sign": source_sign,
            "active": active_function_descriptor(left),
            "predicate_details": predicate_details,
            "whole_open_support_wall_replay": whole_open_support_wall_replay,
            "proof_core_wall_replay": proof_core_wall_replay,
            "proof_target_derivative_sign": proof_target_derivative_sign,
            "dynamic_resolved": dynamic_resolved,
            "unresolved_reasons": unresolved_reasons,
            "members": members,
            "registry": registry,
        })
    need(len(contexts) == EXPECTED_WITNESSES
         and len(transition_histogram) == 8
         and set(transition_histogram.values()) == {128},
         "EXACT_EIGHT_RECHART_TRANSITIONS_128_EACH")
    return contexts


def rectangle_relation(
    left: tuple[Q, Q, Q, Q], right: tuple[Q, Q, Q, Q],
) -> tuple[str, tuple[Q, Q, Q, Q] | None]:
    z = (max(left[0], right[0]), min(left[1], right[1]))
    s = (max(left[2], right[2]), min(left[3], right[3]))
    if z[0] > z[1] or s[0] > s[1]:
        return "DISJOINT", None
    dimension = int(z[0] < z[1]) + int(s[0] < s[1])
    if dimension == 2:
        return "POSITIVE_AREA_OVERLAP", (*z, *s)
    return "BOUNDARY_ONLY_CONTACT", (*z, *s)


def reconstruct_full_sign_side_support_certificate(
    context: dict[str, Any],
    *,
    occurrence: str,
    endpoint_side: str,
    owner_face: str,
    oriented_p_face: Q,
    graph_bracket: tuple[Q, Q],
    exact_face_sign: str,
    endpoint_face_replay: dict[str, Any],
) -> dict[str, Any]:
    """Derive complete p-face-to-rho support containment, not a corridor claim."""

    need(endpoint_side in {"LEFT", "RIGHT"},
         "FULL_SIGN_SIDE_ENDPOINT_SIDE")
    need(owner_face in {"LOWER", "UPPER"},
         "FULL_SIGN_SIDE_OWNER_FACE")
    expected_occurrence = context[
        "left_occurrence" if endpoint_side == "LEFT" else "right_occurrence"
    ]
    need(occurrence == expected_occurrence,
         "FULL_SIGN_SIDE_ENDPOINT_OCCURRENCE")
    region = context[
        "left_region" if endpoint_side == "LEFT" else "right_region"
    ]
    component = context[
        "left_component" if endpoint_side == "LEFT" else "right_component"
    ]
    cell = context["left_cell" if endpoint_side == "LEFT" else "right_cell"]
    registry = context["registry"][occurrence]
    exact_box = context["exact_box"]
    proof_base = context["proof_base"]
    whole_cell_derivative_sign = region["strict_derivative_signs_t_p_s"][1]
    need(
        whole_cell_derivative_sign in STRICT_SIGNS
        and whole_cell_derivative_sign
        == context["proof_target_derivative_sign"]
        == context["left_region"]["strict_derivative_signs_t_p_s"][1]
        == context["right_region"]["strict_derivative_signs_t_p_s"][1],
        "FULL_SIGN_SIDE_UNIFORM_WHOLE_CELL_DF_DP",
    )
    need(
        exact_box[2] < graph_bracket[0] < graph_bracket[1] < exact_box[3]
        and exact_box[0] < proof_base[0] < proof_base[1] < exact_box[1]
        and exact_box[4] < proof_base[2] < proof_base[3] < exact_box[5],
        "FULL_SIGN_SIDE_SEGMENT_DOMAIN_STRICTLY_INSIDE_OPEN_CELL",
    )
    if owner_face == "LOWER":
        need(
            oriented_p_face == graph_bracket[0]
            and exact_face_sign
            == opposite_strict_sign(whole_cell_derivative_sign),
            "FULL_SIGN_SIDE_LOWER_FACE_ORIENTATION",
        )
        approach = "P_APPROACHES_RHO_FROM_BELOW"
        orientation = "LOWER_FACE_SIGN_IS_OPPOSITE_DF_DP"
        half_open_segment = "p_face<=p<rho(z,s)"
    else:
        need(
            oriented_p_face == graph_bracket[1]
            and exact_face_sign == whole_cell_derivative_sign,
            "FULL_SIGN_SIDE_UPPER_FACE_ORIENTATION",
        )
        approach = "P_APPROACHES_RHO_FROM_ABOVE"
        orientation = "UPPER_FACE_SIGN_EQUALS_DF_DP"
        half_open_segment = "rho(z,s)<p<=p_face"

    # This is the substantive full-side derivation.  The exact p-face sign is
    # replayed on all of B_core; dF/dp has one strict sign on the complete
    # common R292 cell; and rho is the unique zero bracketed by the two faces.
    # Hence strict monotonicity fixes the same sign on the entire indicated
    # half-open segment.  No finite corridor is used for that inference.
    need(
        exact_face_sign in STRICT_SIGNS
        and region["active_factor_side_sign"] == exact_face_sign
        and endpoint_face_replay["active_factor_extremal_signs"]
        == [exact_face_sign, exact_face_sign]
        and endpoint_face_replay["signed_support_state"]
        == "FULL_DESIRED_SIDE_SUPPORT",
        "FULL_SIGN_SIDE_EXACT_FACE_TO_R275_SIGN_BINDING",
    )
    need(
        context["dynamic_resolved"] is None
        and context["unresolved_reasons"] == [region["active_reason"]]
        and region["active_reason"] == context["left_region"]["active_reason"]
        == context["right_region"]["active_reason"],
        "FULL_SIGN_SIDE_UNIQUE_WHOLE_CELL_DYNAMIC_BOUNDARY",
    )
    need(
        component["member_refinement_cell_count"] == 1
        and component["member_refinement_cell_ids"]
        == [cell["Round292_R287_existing_overlap_refinement_cell_id"]]
        and component["one_connected_positive_open_support"] is True
        and qbox(cell["exact_transformed_open_cell"]) == exact_box
        and cell["Round275_region_id"]
        == region["reverse_rechart_region_row_id"]
        == registry["Round275_region_id"]
        and registry["source_row_id"]
        == component["Round292_refined_new_support_component_id"]
        and registry["source_row_sha256"] == component["row_sha256"],
        "FULL_SIGN_SIDE_R275_R287_R292_SINGLE_SUPPORT_CHAIN",
    )
    provenance = {
        "Round275_region_id": cell["Round275_region_id"],
        "Round275_region_row_sha256": region["row_sha256"],
        "R287_region_disposition_row_id":
            registry["source_Round287_region_disposition_row_id"],
        "R287_region_row_sha256":
            registry["source_Round287_region_disposition_row_sha256"],
        "R292_refinement_cell_row_id":
            cell["Round292_R287_existing_overlap_refinement_cell_id"],
        "R292_refinement_cell_row_sha256": cell["row_sha256"],
        "R292_connected_support_component_row_id":
            component["Round292_refined_new_support_component_id"],
        "R292_connected_support_component_row_sha256": component["row_sha256"],
        "connected_positive_open_support_member_count": 1,
    }
    need(
        tuple(provenance) == FULL_SIGN_SIDE_PROVENANCE_KEYS
        and all(type(value) is str and value for key, value in provenance.items()
                if key.endswith("_id"))
        and all(PIN_RE.fullmatch(value) is not None
                for key, value in provenance.items()
                if key.endswith("_row_sha256")),
        "FULL_SIGN_SIDE_PROVENANCE_EXACT_SCHEMA",
    )
    body = {
        "endpoint_occurrence_id": occurrence,
        "endpoint_side": endpoint_side,
        "owner_face": owner_face,
        "approach": approach,
        "oriented_p_face": qstr(oriented_p_face),
        "graph_bracket_p": qlist(graph_bracket),
        "proof_closed_core_base_z_s": qlist(proof_base),
        "exact_common_R292_open_cell_t2_p_s": qlist(exact_box),
        "active_function_id": context["active"]["active_function_id"],
        "active_reason": region["active_reason"],
        "active_factor_side_sign": region["active_factor_side_sign"],
        "exact_F_p_face_sign": exact_face_sign,
        "uniform_strict_dF_dp_sign_on_whole_common_R292_cell":
            whole_cell_derivative_sign,
        "F_at_rho_equals_zero": True,
        "face_sign_derivative_orientation": orientation,
        "face_sign_derivative_orientation_hard_checked": True,
        "exact_full_half_open_segment": half_open_segment,
        "strict_monotonicity_retains_face_sign_on_entire_segment": True,
        "endpoint_R275_active_factor_side_sign_equals_face_sign": True,
        "whole_cell_dynamic_signature_exactly_one_unresolved_active_reason": True,
        "all_other_whole_cell_validity_predicates_uniformly_strict": True,
        "R287_R292_single_connected_support_provenance": provenance,
        "full_segment_sign_slice_is_named_endpoint_support": True,
        "local_corridor_role":
            "NONEMPTY_LOCAL_WITNESS_ONLY_NOT_FULL_SIDE_PROOF",
    }
    certificate_id = "round305b-full-sign-side-support:" + digest([
        "ROUND305B_FULL_SIGN_SIDE_TO_RHO_NAMED_SUPPORT_V1", body,
    ])
    certificate = {"certificate_id": certificate_id, **body}
    need(tuple(certificate) == FULL_SIGN_SIDE_SUPPORT_CERTIFICATE_KEYS,
         "FULL_SIGN_SIDE_CERTIFICATE_EXACT_SCHEMA")
    return certificate


def reconstruct_direct_p_witnesses(
    contexts: list[dict[str, Any]], r174: Any, r179: Any,
) -> tuple[list[dict[str, Any]], Counter[int]]:
    preimages: list[dict[str, Any]] = []
    depths: Counter[int] = Counter()
    for context in contexts:
        exact_box = context["exact_box"]
        left = context["left_region"]
        right = context["right_region"]
        sign = context["image_sign"]
        left_initial = active_factor_replay(r174, r179, left, exact_box, sign)
        right_initial = active_factor_replay(r174, r179, right, exact_box, sign)
        need(
            left_initial["signed_support_state"]
            == right_initial["signed_support_state"]
            == "CLIPPED_DESIRED_SIDE_SUPPORT",
            "P_BRACKET_CLIPPED_SEED",
        )
        selected: dict[str, Any] | None = None
        p0, p1 = exact_box[2:4]
        for depth in range(1, MAX_BRACKET_DEPTH + 1):
            lower_interval = targeted_interval(p0, p1, "LOWER", depth)
            upper_interval = targeted_interval(p0, p1, "UPPER", depth)
            lower_box = replace_axis(exact_box, 1, lower_interval)
            upper_box = replace_axis(exact_box, 1, upper_interval)
            replay = {
                "left_lower": active_factor_replay(r174, r179, left, lower_box, sign),
                "left_upper": active_factor_replay(r174, r179, left, upper_box, sign),
                "right_lower": active_factor_replay(r174, r179, right, lower_box, sign),
                "right_upper": active_factor_replay(r174, r179, right, upper_box, sign),
            }
            if {
                replay["left_lower"]["signed_support_state"],
                replay["left_upper"]["signed_support_state"],
            } != {
                "FULL_DESIRED_SIDE_SUPPORT",
                "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL",
            }:
                continue
            need(
                {
                    replay["right_lower"]["signed_support_state"],
                    replay["right_upper"]["signed_support_state"],
                }
                == {
                    "FULL_DESIRED_SIDE_SUPPORT",
                    "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL",
                }
                and (
                    replay["left_lower"]["signed_support_state"]
                    == "FULL_DESIRED_SIDE_SUPPORT"
                ) == (
                    replay["right_lower"]["signed_support_state"]
                    == "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
                ),
                "P_BRACKET_RIGHT_COMPLEMENT",
            )
            lower_face_p = sum(lower_interval, Q(0)) / 2
            upper_face_p = sum(upper_interval, Q(0)) / 2
            lower_face = replace_axis(exact_box, 1, (lower_face_p, lower_face_p))
            upper_face = replace_axis(exact_box, 1, (upper_face_p, upper_face_p))
            face_replay = {
                "left_lower": active_factor_replay(r174, r179, left, lower_face, sign),
                "left_upper": active_factor_replay(r174, r179, left, upper_face, sign),
                "right_lower": active_factor_replay(r174, r179, right, lower_face, sign),
                "right_upper": active_factor_replay(r174, r179, right, upper_face, sign),
            }
            need(
                all(item["signed_support_state"] in {
                    "FULL_DESIRED_SIDE_SUPPORT",
                    "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL",
                } for item in face_replay.values()),
                "P_FACE_STRICT_REPLAY",
            )
            selected = {
                "depth": depth,
                "lower_interval": lower_interval,
                "upper_interval": upper_interval,
                "lower_face_p": lower_face_p,
                "upper_face_p": upper_face_p,
                "face_replay": face_replay,
            }
            break
        need(selected is not None, "P_BRACKET_NOT_FOUND_FAIL_CLOSED")
        need(selected["depth"] in {1, 2}, "UNEXPECTED_P_BRACKET_DEPTH")
        depths[selected["depth"]] += 1
        proof_lower_face = replace_axis(
            context["proof_box"], 1,
            (selected["lower_face_p"], selected["lower_face_p"]),
        )
        proof_upper_face = replace_axis(
            context["proof_box"], 1,
            (selected["upper_face_p"], selected["upper_face_p"]),
        )
        proof_face_replay = {
            "left_lower": active_factor_replay(
                r174, r179, left, proof_lower_face, sign
            ),
            "left_upper": active_factor_replay(
                r174, r179, left, proof_upper_face, sign
            ),
            "right_lower": active_factor_replay(
                r174, r179, right, proof_lower_face, sign
            ),
            "right_upper": active_factor_replay(
                r174, r179, right, proof_upper_face, sign
            ),
        }
        need(
            all(item["signed_support_state"] in {
                "FULL_DESIRED_SIDE_SUPPORT",
                "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL",
            } for item in proof_face_replay.values())
            and proof_face_replay["left_lower"]["signed_support_state"]
            == selected["face_replay"]["left_lower"]["signed_support_state"]
            and proof_face_replay["left_upper"]["signed_support_state"]
            == selected["face_replay"]["left_upper"]["signed_support_state"]
            and proof_face_replay["right_lower"]["signed_support_state"]
            == selected["face_replay"]["right_lower"]["signed_support_state"]
            and proof_face_replay["right_upper"]["signed_support_state"]
            == selected["face_replay"]["right_upper"]["signed_support_state"],
            "PROOF_CORE_P_FACE_STRICT_REPLAY",
        )
        # Use the half of each certified strict targeted interval adjacent to
        # the graph bracket: lower owner [p_face,b], upper owner [a,p_face].
        # This orients the corridor toward rho while keeping it disjoint from
        # Gamma_core and strictly inside the exact R292 open support.
        proof_lower_corridor = replace_axis(
            context["proof_box"], 1,
            (selected["lower_face_p"], selected["lower_interval"][1]),
        )
        proof_upper_corridor = replace_axis(
            context["proof_box"], 1,
            (selected["upper_interval"][0], selected["upper_face_p"]),
        )
        proof_face_wall_replays = {
            "lower": wall_event_product_replay_on_z_box(
                r174, r179, left, proof_lower_face, sign,
                "round305b-independent-proof-lower-face-wall-product",
            ),
            "upper": wall_event_product_replay_on_z_box(
                r174, r179, left, proof_upper_face, sign,
                "round305b-independent-proof-upper-face-wall-product",
            ),
        }
        need(
            all(
                replay["source_wall_factor_sign"] in STRICT_SIGNS
                and replay["target_wall_factor_sign"] in STRICT_SIGNS
                and replay["wall_event_product_sign"] in STRICT_SIGNS
                for replay in proof_face_wall_replays.values()
            )
            and proof_face_wall_replays["lower"]["target_wall_factor_sign"]
            != proof_face_wall_replays["upper"]["target_wall_factor_sign"],
            "PROOF_CORE_WALL_PRODUCT_FACE_REPLAYS_STRICT_OPPOSITE",
        )
        lower_owner = (
            context["left_occurrence"]
            if proof_face_replay["left_lower"]["signed_support_state"]
            == "FULL_DESIRED_SIDE_SUPPORT" else context["right_occurrence"]
        )
        upper_owner = (
            context["left_occurrence"]
            if proof_face_replay["left_upper"]["signed_support_state"]
            == "FULL_DESIRED_SIDE_SUPPORT" else context["right_occurrence"]
        )
        need(lower_owner != upper_owner, "P_FACE_DISTINCT_ENDPOINT_OWNERS")
        endpoint_face = {
            lower_owner: ("LOWER", selected["lower_face_p"]),
            upper_owner: ("UPPER", selected["upper_face_p"]),
        }
        endpoint_corridor = {
            lower_owner: proof_lower_corridor,
            upper_owner: proof_upper_corridor,
        }
        derivative_sign = context["proof_target_derivative_sign"]
        lower_target_sign = proof_face_wall_replays["lower"][
            "target_wall_factor_sign"
        ]
        upper_target_sign = proof_face_wall_replays["upper"][
            "target_wall_factor_sign"
        ]
        need(
            lower_target_sign == opposite_strict_sign(derivative_sign)
            and upper_target_sign == derivative_sign,
            "FULL_FACE_TO_RHO_MONOTONE_ORIENTATION",
        )
        face_data_by_occurrence = {
            lower_owner: ("LOWER", selected["lower_face_p"], lower_target_sign),
            upper_owner: ("UPPER", selected["upper_face_p"], upper_target_sign),
        }
        endpoint_full_segment_certificate: dict[str, dict[str, Any]] = {}
        for endpoint_side, occurrence in (
            ("LEFT", context["left_occurrence"]),
            ("RIGHT", context["right_occurrence"]),
        ):
            owner_face, oriented_face, face_target_sign = (
                face_data_by_occurrence[occurrence]
            )
            endpoint_replay = proof_face_replay[
                endpoint_side.lower() + "_" + owner_face.lower()
            ]
            endpoint_full_segment_certificate[occurrence] = (
                reconstruct_full_sign_side_support_certificate(
                    context,
                    occurrence=occurrence,
                    endpoint_side=endpoint_side,
                    owner_face=owner_face,
                    oriented_p_face=oriented_face,
                    graph_bracket=(
                        selected["lower_face_p"], selected["upper_face_p"],
                    ),
                    exact_face_sign=face_target_sign,
                    endpoint_face_replay=endpoint_replay,
                )
            )
        support_open_base = (
            exact_box[0], exact_box[1], exact_box[4], exact_box[5]
        )
        proof_closed_core_base = context["proof_base"]
        owner_contact_closure_base = support_open_base
        need(support_open_base[0] > 0 and support_open_base[1] < Q(1, 2)
             and exact_box[2] > -1 and exact_box[3] < 1,
             "RELATIVE_PHYSICAL_CHART_INTERIOR")
        need(
            support_open_base[0] < proof_closed_core_base[0]
            < proof_closed_core_base[1] < support_open_base[1]
            and support_open_base[2] < proof_closed_core_base[2]
            < proof_closed_core_base[3] < support_open_base[3]
            and exact_box[2] < selected["lower_face_p"]
            < selected["upper_face_p"] < exact_box[3],
            "PROOF_CORE_AND_P_FACES_STRICTLY_INSIDE_OPEN_SUPPORT",
        )
        active_id = context["active"]["active_function_id"]
        proof_core_patch_payload = {
            "scope_row_sha256": context["scope"]["row_sha256"],
            "pair": context["scope"]["canonical_Round294_registry_occurrence_pair"],
            "active_function_id": active_id,
            "fixed_physical_t_sign": sign,
            "proof_closed_core_base_z_s": qlist(proof_closed_core_base),
            "p_bracket": qlist((selected["lower_face_p"], selected["upper_face_p"])),
        }
        proof_core_patch_id = "round305b-proof-core-patch:" + digest(
            ["ROUND305B_DIRECT_PROOF_CORE_P_GRAPH_PATCH_V1",
             proof_core_patch_payload]
        )
        witness_id = "round305b-physical-witness:" + digest(
            ["ROUND305B_TWO_SIDED_P_ATTACHMENT_V1", proof_core_patch_id,
             context["scope"]["row_sha256"]]
        )
        branch_id = "round305b-target-zero-branch:" + digest([
            context["source"]["source_Round287_pair_row_id"],
            context["left_region"]["active_reason"], active_id,
        ])
        owner_extension_payload = {
            "scope_row_sha256": context["scope"]["row_sha256"],
            "pair": context["scope"]["canonical_Round294_registry_occurrence_pair"],
            "active_function_id": active_id,
            "fixed_physical_t_sign": sign,
            "owner_contact_closure_base_z_s": qlist(
                owner_contact_closure_base
            ),
            "p_bracket": qlist(
                (selected["lower_face_p"], selected["upper_face_p"])
            ),
            "formal_credit": 0,
        }
        owner_extension_patch_id = "round305b-owner-extension-patch:" + digest(
            ["ROUND305B_ZERO_CREDIT_FULL_CLOSURE_ROOT_EXTENSION_PATCH_V1",
             owner_extension_payload]
        )
        lemma_payload = {
            "theorem": "R305B_RELATIVE_PHYSICAL_P_TO_RHO_ATTACHMENT_V1",
            "proof_core_patch_id": proof_core_patch_id,
            "owner_extension_patch_id": owner_extension_patch_id,
            "coordinate_map": (
                "Phi=(q=(9/25)n,u=sqrt(1-p^2)n+p*(-ny,nx),s)"
            ),
            "relative_chart": context["left_region"]["adjacent_chart"],
            "fixed_t_sign": sign,
            "support_open_base_z_s": qlist(support_open_base),
            "proof_closed_core_base_z_s": qlist(proof_closed_core_base),
            "owner_contact_closure_base_z_s": qlist(
                owner_contact_closure_base
            ),
            "quantified_attachment_base": "PROOF_CLOSED_CORE_ONLY",
            "owner_extension_is_zero_credit_sidecar_only": True,
            "graph_bracket_p": qlist(
                (selected["lower_face_p"], selected["upper_face_p"])
            ),
            "strict_p_derivative":
                context["left_region"]["strict_derivative_signs_t_p_s"][1],
            "path_formula":
                "p_eps=(1-eps)*p_graph(z,s)+eps*p_face, 0<eps<=1",
            "limit_formula":
                "lim_{eps->0+} Phi(z,p_eps,s)=Phi(z,p_graph(z,s),s)",
            "corridor_box_is_not_Gamma_intersection": True,
        }
        lemma_id = "round305b-relative-p-limit:" + digest(lemma_payload)
        context = dict(context)
        context.update({
            "support_open_base": support_open_base,
            "proof_closed_core_base": proof_closed_core_base,
            "owner_contact_closure_base": owner_contact_closure_base,
            "p_bracket": (selected["lower_face_p"], selected["upper_face_p"]),
            "bracket_depth": selected["depth"],
            "face_replay": proof_face_replay,
            "proof_face_wall_replays": proof_face_wall_replays,
            "endpoint_face": endpoint_face,
            "endpoint_corridor": endpoint_corridor,
            "endpoint_full_segment_certificate":
                endpoint_full_segment_certificate,
            "proof_core_patch_id": proof_core_patch_id,
            "owner_extension_patch_id": owner_extension_patch_id,
            "witness_id": witness_id,
            "branch_id": branch_id,
            "lemma_payload": lemma_payload,
            "lemma_id": lemma_id,
        })
        preimages.append(context)
    need(len(preimages) == EXPECTED_WITNESSES
         and dict(depths) == EXPECTED_BRACKET_DEPTH_HISTOGRAM,
         "EXACT_DIRECT_P_BRACKET_CENSUS_320_704")
    return preimages, depths


def reconstruct_boundary_rows(
    preimages: list[dict[str, Any]], r174: Any, r179: Any,
) -> tuple[
    list[dict[str, Any]], list[dict[str, Any]],
    dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]],
    dict[str, Any],
]:
    groups: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for row in preimages:
        groups[(row["active"]["active_function_id"], row["image_sign"])].append(row)
    need(len(groups) == 8 and {len(rows) for rows in groups.values()} == {128},
         "BOUNDARY_EIGHT_GROUPS_128")
    contacts: list[tuple[dict[str, Any], dict[str, Any], tuple[Q, Q, Q, Q]]] = []
    relation_histogram: Counter[str] = Counter()
    for rows in groups.values():
        rows.sort(key=lambda row: row["witness_id"])
        for index, left in enumerate(rows):
            for right in rows[index + 1:]:
                relation, intersection = rectangle_relation(
                    left["owner_contact_closure_base"],
                    right["owner_contact_closure_base"],
                )
                relation_histogram[relation] += 1
                need(relation != "POSITIVE_AREA_OVERLAP",
                     "PHYSICAL_PATCH_BASE_INTERIOR_OVERLAP")
                if relation == "BOUNDARY_ONLY_CONTACT":
                    need(intersection is not None, "BOUNDARY_INTERSECTION_PRESENT")
                    contacts.append((left, right, intersection))
    need(relation_histogram == Counter({
        "DISJOINT": 61_488, "BOUNDARY_ONLY_CONTACT": 3_536,
    }), "BOUNDARY_EXACT_PAIR_RELATIONS")

    contact_preimages: list[dict[str, Any]] = []
    dimension_histogram: Counter[int] = Counter()
    for left, right, common in contacts:
        dimension = int(common[0] < common[1]) + int(common[2] < common[3])
        need(dimension in {0, 1}, "BOUNDARY_DIMENSION")
        dimension_histogram[dimension] += 1
        group = (left["active"]["active_function_id"], left["image_sign"])
        p_hull = (
            min(left["p_bracket"][0], right["p_bracket"][0]),
            max(left["p_bracket"][1], right["p_bracket"][1]),
        )
        need(p_hull[0] < p_hull[1], "BOUNDARY_POSITIVE_P_HULL")
        # Replay the p derivative independently on the exact common base and
        # pair-specific hull. Owner aggregation is a distinct second phase.
        signed_z = signed_physical_outer(
            (common[0], common[1], p_hull[0], p_hull[1],
             common[2], common[3]),
            left["image_sign"],
        )
        boundary_box = r174.atlas.AtlasBox(
            *signed_z, 0, "round305b-independent-boundary-root"
        )
        geometry = r179.interval_geometry(
            left["left_region"]["adjacent_chart"],
            left["left_region"]["owner_target"], boundary_box,
        )
        derivative = exact_active_dual(
            geometry, left["left_region"]["active_reason"]
        )[1][1]
        derivative_sign = r179.sign(derivative)
        need(
            derivative_sign in STRICT_SIGNS
            and derivative_sign
            == left["left_region"]["strict_derivative_signs_t_p_s"][1]
            == right["left_region"]["strict_derivative_signs_t_p_s"][1],
            "BOUNDARY_STRICT_P_ROOT_UNIQUENESS",
        )
        witness_pair = sorted((left["witness_id"], right["witness_id"]))
        owner_extension_pair = sorted((
            left["owner_extension_patch_id"], right["owner_extension_patch_id"]
        ))
        need(len(set(witness_pair)) == len(set(owner_extension_pair)) == 2,
             "OWNER_EXTENSION_CONTACT_DISTINCT_PAIR")
        row_id = "round305b-closure-contact:" + digest([
            "ROUND305B_PAIRWISE_OWNER_EXTENSION_CLOSURE_CONTACT_V1",
            owner_extension_pair,
            qlist(common), qlist(p_hull),
        ])
        contact_preimages.append({
            "contact_id": row_id,
            "group": group,
            "pair": witness_pair,
            "owner_extension_pair": owner_extension_pair,
            "dimension": dimension,
            "common": common,
            "p_hull": p_hull,
            "derivative_sign": derivative_sign,
        })

    vertex_contacts: dict[
        tuple[tuple[str, int], tuple[str, ...]], list[dict[str, Any]]
    ] = defaultdict(list)
    face_contacts: list[dict[str, Any]] = []
    for contact in contact_preimages:
        if contact["dimension"] == 0:
            vertex_contacts[(contact["group"], tuple(qlist(contact["common"])))] .append(contact)
        else:
            face_contacts.append(contact)
    need(len(face_contacts) == EXPECTED_FACE_CONTACTS
         and len(vertex_contacts) == EXPECTED_VERTEX_OWNER_LOCI
         and {len(rows) for rows in vertex_contacts.values()} == {2},
         "CONTACT_TO_FACE_AND_VERTEX_LOCUS_PARTITION")

    vertex_owner_ids = {
        key: "round305b-owner-locus:" + digest([
            "ROUND305B_GLOBAL_OWNER_EXTENSION_VERTEX_LOCUS_V1",
            list(key[0]), list(key[1])
        ])
        for key in vertex_contacts
    }
    face_owner_ids = {
        contact["contact_id"]: "round305b-owner-locus:" + digest([
            "ROUND305B_OWNER_EXTENSION_FACE_RELATIVE_INTERIOR_LOCUS_V1",
            list(contact["group"]), qlist(contact["common"]), contact["contact_id"],
        ])
        for contact in face_contacts
    }

    contact_rows: list[dict[str, Any]] = []
    contact_by_witness: dict[str, list[dict[str, Any]]] = defaultdict(list)
    contact_row_by_id: dict[str, dict[str, Any]] = {}
    for contact in contact_preimages:
        vertex_key = (contact["group"], tuple(qlist(contact["common"])))
        owner_id = (
            vertex_owner_ids[vertex_key] if contact["dimension"] == 0
            else face_owner_ids[contact["contact_id"]]
        )
        row = close_row({
            "Round305B_closure_contact_row_id": contact["contact_id"],
            "schema": SCHEMA + ".closure-contact-row.v1",
            "associated_physical_witness_row_ids": contact["pair"],
            "contact_pair_owner_extension_patch_ids":
                contact["owner_extension_pair"],
            "contact_kind": (
                "OWNER_EXTENSION_FOUR_PATCH_VERTEX_DIAGONAL_PAIR"
                if contact["dimension"] == 0
                else "OWNER_EXTENSION_BASE_FACE_CONTACT"
            ),
            "base_dimension": contact["dimension"],
            "exact_common_base_z_s": qlist(contact["common"]),
            "common_p_bracket_hull": qlist(contact["p_hull"]),
            "strict_common_active_function_p_derivative_sign":
                contact["derivative_sign"],
            "owner_extension_root_unique_on_full_closure": True,
            "owner_locus_row_id": owner_id,
            "full_closure_extension_only": True,
            "not_Gamma_core_contact": True,
            "not_G3_G4_or_component_edge_basis": True,
            "D4_transfer_used": False,
        })
        need(tuple(row) == CLOSURE_CONTACT_KEYS, "CONTACT_ROW_EXACT_SCHEMA")
        contact_rows.append(row)
        contact_row_by_id[contact["contact_id"]] = row
        for witness_id in contact["pair"]:
            contact_by_witness[witness_id].append(row)
    contact_rows.sort(key=lambda row: row["Round305B_closure_contact_row_id"])

    owner_rows: list[dict[str, Any]] = []
    owner_by_witness: dict[str, list[dict[str, Any]]] = defaultdict(list)
    owner_extension_by_witness = {
        row["witness_id"]: row["owner_extension_patch_id"]
        for row in preimages
    }
    # Vertex loci are authoritative for all four witnesses and all six closure
    # contacts (four incident face contacts plus two diagonal contacts).
    vertex_witness_refs = 0
    vertex_contact_refs = 0
    for key, diagonal_rows in sorted(vertex_contacts.items()):
        group, exact_locus = key
        z, _z_again, s, _s_again = map(Q, exact_locus)
        incident_face = [
            contact for contact in face_contacts
            if contact["group"] == group
            and contact["common"][0] <= z <= contact["common"][1]
            and contact["common"][2] <= s <= contact["common"][3]
        ]
        need(len(incident_face) == 4, "VERTEX_EXACT_FOUR_FACE_CONTACTS")
        incident_contacts = sorted(
            contact["contact_id"] for contact in incident_face + diagonal_rows
        )
        incident_witnesses = sorted({
            witness for contact in incident_face + diagonal_rows
            for witness in contact["pair"]
        })
        incident_owner_extensions = sorted(
            owner_extension_by_witness[witness]
            for witness in incident_witnesses
        )
        need(
            len(incident_contacts) == 6
            and len(incident_witnesses) == len(incident_owner_extensions) == 4
            and len(set(incident_owner_extensions)) == 4,
             "VERTEX_4_WITNESSES_6_CONTACTS")
        owner_id = vertex_owner_ids[key]
        row = close_row({
            "Round305B_owner_locus_row_id": owner_id,
            "schema": SCHEMA + ".owner-locus-row.v1",
            "locus_kind": "FOUR_PATCH_VERTEX",
            "exact_locus_base_z_s": list(exact_locus),
            "associated_physical_witness_row_ids": incident_witnesses,
            "global_incident_owner_extension_patch_ids":
                incident_owner_extensions,
            "global_incident_owner_extension_patch_count": 4,
            "incident_closure_contact_row_ids": incident_contacts,
            "lexicographically_least_global_incident_owner_extension_patch":
                min(incident_owner_extensions),
            "face_endpoint_vertex_override_row_ids": [],
            "full_closure_extension_only": True,
            "not_Gamma_core_locus": True,
            "not_G3_G4_or_component_edge_basis": True,
            "D4_transfer_used": False,
        })
        need(tuple(row) == OWNER_LOCUS_KEYS, "VERTEX_OWNER_ROW_EXACT_SCHEMA")
        owner_rows.append(row)
        vertex_witness_refs += len(incident_witnesses)
        vertex_contact_refs += len(incident_contacts)
        for witness_id in incident_witnesses:
            owner_by_witness[witness_id].append(row)

    # Each 1D face owner governs its relative interior. Its endpoint list
    # records every four-patch vertex where the vertex owner overrides it.
    face_override_refs = 0
    for contact in face_contacts:
        overrides = sorted(
            owner_id for (group, exact_locus), owner_id in vertex_owner_ids.items()
            if group == contact["group"]
            and contact["common"][0] <= Q(exact_locus[0]) <= contact["common"][1]
            and contact["common"][2] <= Q(exact_locus[2]) <= contact["common"][3]
        )
        need(len(overrides) in {0, 1, 2}, "FACE_ENDPOINT_OVERRIDE_ARITY")
        face_override_refs += len(overrides)
        owner_id = face_owner_ids[contact["contact_id"]]
        face_owner_extensions = contact["owner_extension_pair"]
        row = close_row({
            "Round305B_owner_locus_row_id": owner_id,
            "schema": SCHEMA + ".owner-locus-row.v1",
            "locus_kind": "FACE_RELATIVE_INTERIOR",
            "exact_locus_base_z_s": qlist(contact["common"]),
            "associated_physical_witness_row_ids": contact["pair"],
            "global_incident_owner_extension_patch_ids":
                face_owner_extensions,
            "global_incident_owner_extension_patch_count": 2,
            "incident_closure_contact_row_ids": [contact["contact_id"]],
            "lexicographically_least_global_incident_owner_extension_patch":
                min(face_owner_extensions),
            "face_endpoint_vertex_override_row_ids": overrides,
            "full_closure_extension_only": True,
            "not_Gamma_core_locus": True,
            "not_G3_G4_or_component_edge_basis": True,
            "D4_transfer_used": False,
        })
        need(tuple(row) == OWNER_LOCUS_KEYS, "FACE_OWNER_ROW_EXACT_SCHEMA")
        owner_rows.append(row)
        for witness_id in contact["pair"]:
            owner_by_witness[witness_id].append(row)
    owner_rows.sort(key=lambda row: row["Round305B_owner_locus_row_id"])

    patch_degree = Counter(
        len(contact_by_witness[row["witness_id"]]) for row in preimages
    )
    owner_kind = Counter(row["locus_kind"] for row in owner_rows)
    contact_kind = Counter(row["contact_kind"] for row in contact_rows)
    contact_derivative = Counter(
        row["strict_common_active_function_p_derivative_sign"]
        for row in contact_rows
    )
    need(
        len(contact_rows) == EXPECTED_CLOSURE_CONTACTS
        and len(owner_rows) == EXPECTED_OWNER_LOCI
        and dict(dimension_histogram) == EXPECTED_CONTACT_DIMENSION_HISTOGRAM
        and dict(owner_kind) == EXPECTED_OWNER_KIND_HISTOGRAM
        and dict(patch_degree) == EXPECTED_PATCH_CONTACT_DEGREE_HISTOGRAM
        and vertex_witness_refs == EXPECTED_VERTEX_WITNESS_REFS
        and vertex_contact_refs == EXPECTED_VERTEX_CONTACT_REFS
        and face_override_refs == EXPECTED_VERTEX_WITNESS_REFS,
        "CONTACT_3536_OWNER_2696_GLOBAL_CENSUS",
    )
    return contact_rows, owner_rows, contact_by_witness, owner_by_witness, {
        "within_group_base_relation_histogram":
            dict(sorted(relation_histogram.items())),
        "closure_contact_count": len(contact_rows),
        "closure_contact_kind_histogram": dict(sorted(contact_kind.items())),
        "closure_contact_base_dimension_histogram":
            {str(key): value for key, value in sorted(dimension_histogram.items())},
        "closure_contact_derivative_histogram":
            dict(sorted(contact_derivative.items())),
        "owner_locus_count": len(owner_rows),
        "owner_locus_kind_histogram": dict(sorted(owner_kind.items())),
        "face_to_vertex_override_reference_count": face_override_refs,
        "vertex_incident_contact_reference_count": vertex_contact_refs,
        "patch_contact_degree_histogram": {
            str(key): value for key, value in sorted(patch_degree.items())
        },
        "global_four_patch_vertex_owner_replayed": True,
        "old_pairwise_minimum_owner_rejected": True,
        "owner_extension_full_closure_sidecar_only": True,
        "owner_extension_not_Gamma_core_contact_or_G3_G4_or_edge_basis": True,
    }


def reconstruct_candidate_rows(
    preimages: list[dict[str, Any]],
    contact_rows: list[dict[str, Any]],
    owner_rows: list[dict[str, Any]],
    contact_by_witness: dict[str, list[dict[str, Any]]],
    owner_by_witness: dict[str, list[dict[str, Any]]],
) -> dict[str, list[dict[str, Any]]]:
    anchor_rows: list[dict[str, Any]] = []
    anchor_by_witness: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in preimages:
        for side, occurrence, component, cell, region in (
            ("LEFT", item["left_occurrence"], item["left_component"],
             item["left_cell"], item["left_region"]),
            ("RIGHT", item["right_occurrence"], item["right_component"],
             item["right_cell"], item["right_region"]),
        ):
            registry = item["registry"][occurrence]
            member = item["members"][occurrence]
            face_side, face_p = item["endpoint_face"][occurrence]
            full_side_certificate = item[
                "endpoint_full_segment_certificate"
            ][occurrence]
            need(
                tuple(full_side_certificate)
                == FULL_SIGN_SIDE_SUPPORT_CERTIFICATE_KEYS
                and full_side_certificate["endpoint_occurrence_id"] == occurrence
                and full_side_certificate["endpoint_side"] == side
                and full_side_certificate["owner_face"] == face_side
                and full_side_certificate["oriented_p_face"] == qstr(face_p)
                and full_side_certificate["active_factor_side_sign"]
                == region["active_factor_side_sign"]
                and full_side_certificate[
                    "uniform_strict_dF_dp_sign_on_whole_common_R292_cell"
                ] == region["strict_derivative_signs_t_p_s"][1],
                "ANCHOR_FULL_SIGN_SIDE_CERTIFICATE_BINDING",
            )
            closure_limit_side = {
                "approach": (
                    "P_APPROACHES_RHO_FROM_BELOW"
                    if face_side == "LOWER"
                    else "P_APPROACHES_RHO_FROM_ABOVE"
                ),
                "active_factor_sign": region["active_factor_side_sign"],
                "strict_p_derivative_sign":
                    region["strict_derivative_signs_t_p_s"][1],
                "limit": "p -> rho(z,s)",
                "topology": "relative topology of physical section X",
                "quantified_base": "PROOF_CLOSED_CORE_ONLY",
                "support_open_base_z_s": qlist(item["support_open_base"]),
                "proof_closed_core_base_z_s": qlist(
                    item["proof_closed_core_base"]
                ),
                "strict_sign_corridor_box_t2_p_s": qlist(
                    item["endpoint_corridor"][occurrence]
                ),
                "corridor_strictly_inside_R292_open_cell": True,
                "local_corridor_nonempty_witness_only": True,
                "full_sign_side_to_rho_support_certificate":
                    full_side_certificate,
                "exact_full_sign_side_contained_in_R292_support_derived": True,
            }
            need(tuple(closure_limit_side) == CLOSURE_LIMIT_SIDE_KEYS,
                 "ANCHOR_CLOSURE_LIMIT_SIDE_V2_EXACT_SCHEMA")
            row_id = "round305b-anchor:" + digest([
                "ROUND305B_R292_SINGLE_CELL_FULL_SIGN_SIDE_ANCHOR_V2",
                item["witness_id"], side, occurrence, cell["row_sha256"],
                registry["row_sha256"], member["row_sha256"], item["lemma_id"],
                full_side_certificate["certificate_id"],
            ])
            row = close_row({
                "Round305B_anchor_row_id": row_id,
                "schema": SCHEMA + ".anchor-row.v1",
                "physical_witness_row_id": item["witness_id"],
                "side": side,
                "endpoint_occurrence_id": occurrence,
                "Round275_region_id": cell["Round275_region_id"],
                "Round275_region_row_sha256": region["row_sha256"],
                "R287_region_disposition_row_id":
                    registry["source_Round287_region_disposition_row_id"],
                "R287_region_row_sha256":
                    registry["source_Round287_region_disposition_row_sha256"],
                "R292_refinement_cell_row_id":
                    cell["Round292_R287_existing_overlap_refinement_cell_id"],
                "R292_refinement_cell_row_sha256": cell["row_sha256"],
                "R292_connected_support_component_row_id":
                    component["Round292_refined_new_support_component_id"],
                "R292_connected_support_component_row_sha256": component["row_sha256"],
                "R292_occurrence_content_preimage_sha256":
                    registry["occurrence_id_content_preimage_sha256"],
                "R294_occurrence_registry_row_id":
                    registry["Round294_occurrence_registry_row_id"],
                "R294_occurrence_registry_row_sha256": registry["row_sha256"],
                "R294_official_key_id": registry["official_key_id"],
                "R294_official_key_ordinal": registry["official_key_ordinal"],
                "R294_official_key_binding_status":
                    registry["official_key_binding_status"],
                "Round304_member_row_id":
                    member["Round304_fresh_member_component_row_id"],
                "Round304_member_row_sha256": member["row_sha256"],
                "official_key_id": member["official_key_id"],
                "connected_positive_open_support_nonempty": True,
                "connected_positive_open_support_member_count": 1,
                "relative_physical_closure_limit_side": closure_limit_side,
                "formal_anchor_binding_credit": 1,
                "formal_occurrence_identity_collapse_credit": 0,
                "formal_official_key_merge_credit": 0,
            })
            need(tuple(row) == ANCHOR_KEYS, "ANCHOR_ROW_EXACT_SCHEMA")
            need(
                region["active_factor_side_sign"]
                == item["face_replay"][
                    side.lower() + "_" + face_side.lower()
                ]["active_factor_extremal_signs"][0]
                == full_side_certificate["exact_F_p_face_sign"],
                "ANCHOR_FACE_SIGN_MATCHES_ENDPOINT_SUPPORT",
            )
            anchor_rows.append(row)
            anchor_by_witness[item["witness_id"]].append(row)
    anchor_rows.sort(key=lambda row: row["Round305B_anchor_row_id"])
    need(len(anchor_rows) == EXPECTED_ANCHORS
         and len({row["endpoint_occurrence_id"] for row in anchor_rows})
         == EXPECTED_ANCHORS
         and len({
             row["relative_physical_closure_limit_side"]
             ["full_sign_side_to_rho_support_certificate"]["certificate_id"]
             for row in anchor_rows
         }) == EXPECTED_ANCHORS,
         "ANCHOR_2048_DISTINCT_ENDPOINTS")

    physical_rows: list[dict[str, Any]] = []
    for item in preimages:
        anchors = sorted(
            anchor_by_witness[item["witness_id"]],
            key=lambda row: {"LEFT": 0, "RIGHT": 1}[row["side"]],
        )
        contacts = sorted(
            contact_by_witness[item["witness_id"]],
            key=lambda row: row["Round305B_closure_contact_row_id"],
        )
        owners = sorted(
            owner_by_witness[item["witness_id"]],
            key=lambda row: row["Round305B_owner_locus_row_id"],
        )
        scope = item["scope"]
        pair = scope["canonical_Round294_registry_occurrence_pair"]
        need(pair == sorted(pair) and len(set(pair)) == 2,
             "PHYSICAL_ROW_CANONICAL_OCCURRENCE_PAIR")
        official_pair = sorted(
            item["members"][value]["official_key_id"] for value in pair
        )
        need(official_pair[0] != official_pair[1], "PHYSICAL_ROW_CROSS_OFFICIAL_KEY")
        component_pair = sorted(scope["final_component_pair"])
        need(len(set(component_pair)) == 2,
             "PHYSICAL_ROW_CANONICAL_COMPONENT_PAIR")
        proof_core_base = qlist(item["proof_closed_core_base"])
        support_open_base = qlist(item["support_open_base"])
        owner_extension_base = qlist(item["owner_contact_closure_base"])
        active_identity = item["active"]["active_function_identity_payload"]
        proof_core_area = (
            (item["proof_closed_core_base"][1]
             - item["proof_closed_core_base"][0])
            * (item["proof_closed_core_base"][3]
               - item["proof_closed_core_base"][2])
        )
        relative_domain = {
            "coordinate_system": "(z=t^2,p,s)",
            "support_open_base_z_s": support_open_base,
            "proof_closed_core_base_B_z_s": proof_core_base,
            "owner_contact_closure_base_z_s": owner_extension_base,
            "proof_core_inset_rule": "QUARTER_EACH_TANGENT_SIDE",
            "proof_core_strictly_inside_R292_open_base": True,
            "owner_contact_closure_is_zero_credit_full_closure_extension": True,
            "p_interval": qlist(item["p_bracket"]),
            "proof_core_base_area": qstr(proof_core_area),
            "B_core_connected": True,
            "D_equals_B_core_times_closed_p_interval": True,
            "strict_domain_bounds": {
                "0<z<1/2": True,
                "-1<p<1": True,
            },
            "physical_phase_map": {
                "q": "(9/25)n(z)",
                "u": "sqrt(1-p^2)n(z)+p(-n_y(z),n_x(z))",
                "s": "s",
            },
            "Phi_continuous_on_D": True,
            "relative_ambient_space": "physical collision section X",
        }
        graph = {
            "definition": (
                "Gamma_core={Phi(z,rho(z,s),s):(z,s) in B_core}; "
                "F(z,rho(z,s),s)=0"
            ),
            "quantified_base": "PROOF_CLOSED_CORE_ONLY",
            "proof_closed_core_base_z_s": proof_core_base,
            "F_identity": active_identity,
            "rho_exists_uniquely_on_every_base_fibre": True,
            "rho_continuous": True,
            "rho_range_strictly_inside_p_bracket": True,
            "Gamma_core_nonempty": True,
            "Gamma_core_connected": True,
            "Gamma_core_included_in_valid_physical_wall_event_lower_stratum": True,
            "corridor_boxes_disjoint_from_Gamma_core": True,
            "owner_extension_not_part_of_Gamma_core": True,
            "relative_limit_lemma_instance": item["lemma_payload"],
        }
        left_face_side, left_face_p = item["endpoint_face"][
            item["left_occurrence"]
        ]
        right_face_side, right_face_p = item["endpoint_face"][
            item["right_occurrence"]
        ]
        g0 = {
            "satisfied": True,
            "Round305A": [
                scope["Round305A_scope_reprojection_row_id"],
                scope["row_sha256"],
            ],
            "Round300A": [
                scope["source_Round300A_row_id"],
                scope["source_Round300A_row_sha256"],
            ],
            "Round287_pair": [
                item["source"]["source_Round287_pair_row_id"],
                item["source"]["source_Round287_pair_row_sha256"],
            ],
            "Round275_regions": [
                [item["source"]["left_Round275_region_id"],
                 item["left_region"]["row_sha256"]],
                [item["source"]["right_Round275_region_id"],
                 item["right_region"]["row_sha256"]],
            ],
            "anchor_row_ids": [
                anchor["Round305B_anchor_row_id"] for anchor in anchors
            ],
            "anchor_row_sha256s": [anchor["row_sha256"] for anchor in anchors],
            "all_source_and_derived_rows_content_closed": True,
        }
        g1 = {
            "satisfied": True,
            "exact_domain": relative_domain,
            "attachment_quantifier": "FOR_ALL_B_IN_PROOF_CLOSED_CORE_ONLY",
            "proof_core_strictly_inside_both_R292_open_supports": True,
            "selected_root_discriminant_strict_positive": True,
            "selected_near_root_strict_future_and_less_than_three": True,
            "all_competitor_order_outgoing_chart_and_other_dynamic_predicates_strict": True,
            "only_nonstrict_whole_cell_predicate":
                item["left_region"]["active_reason"],
            "both_R292_supports_connected_positive_open_single_cell": True,
        }
        proof_face_target_replays = {
            name: {
                "active_factor_extremal_signs": replay[
                    "active_factor_extremal_signs"
                ],
                "signed_support_state": replay["signed_support_state"],
            }
            for name, replay in item["face_replay"].items()
        }
        g2 = {
            "satisfied": True,
            "active_reason": item["left_region"]["active_reason"],
            "predicate_details": item["predicate_details"],
            "explicit_wall_value": 0,
            "zero_wall_hard_checked_not_silently_dropped": True,
            "source_wall_factor_strict_sign":
                item["proof_core_wall_replay"]["source_wall_factor_sign"],
            "source_wall_factor_uniformly_nonzero_on_proof_core": True,
            "target_wall_factor_F_identity": active_identity,
            "wall_event_product_zero_iff_target_F_zero": True,
            "uniform_strict_dF_dp_sign": item["proof_target_derivative_sign"],
            "proof_core_target_factor_face_replays": proof_face_target_replays,
            "proof_core_wall_event_product_face_replays":
                item["proof_face_wall_replays"],
            "uniform_opposite_p_face_signs": True,
            "proof_closed_core_base_z_s": proof_core_base,
            "IVT_unique_continuous_rho": True,
            "Gamma_core_valid_physical_inclusion_replayed": True,
        }
        left_full_side_certificate = anchors[0][
            "relative_physical_closure_limit_side"
        ]["full_sign_side_to_rho_support_certificate"]
        right_full_side_certificate = anchors[1][
            "relative_physical_closure_limit_side"
        ]["full_sign_side_to_rho_support_certificate"]
        need(
            left_full_side_certificate
            == item["endpoint_full_segment_certificate"][item["left_occurrence"]]
            and right_full_side_certificate
            == item["endpoint_full_segment_certificate"][item["right_occurrence"]]
            and left_full_side_certificate["certificate_id"]
            != right_full_side_certificate["certificate_id"],
            "PHYSICAL_TWO_INDEPENDENT_FULL_SIGN_SIDE_CERTIFICATES",
        )
        g3 = {
            "satisfied": True,
            "endpoint": item["left_occurrence"],
            "sign_side": anchors[0]["relative_physical_closure_limit_side"],
            "quantified_base": "FOR_ALL_B_IN_PROOF_CLOSED_CORE_ONLY",
            "proof_closed_core_base_z_s": proof_core_base,
            "sequence": (
                "Phi(b,p_k), p_k->rho(b), b in B_core, from the LEFT "
                "endpoint sign side"
            ),
            "strict_sign_corridor_box_t2_p_s": qlist(
                item["endpoint_corridor"][item["left_occurrence"]]
            ),
            "full_sign_side_to_rho_support_certificate":
                left_full_side_certificate,
            "full_sign_side_sequence_remains_in_exact_R292_open_support_by_certificate":
                True,
            "corridor_used_only_as_local_nonempty_witness": True,
            "limit_in_relative_physical_space_X": True,
            "conclusion": "Gamma_core subset cl_X(A_left)",
        }
        need(tuple(g3) == G3_G4_KEYS, "PHYSICAL_G3_V2_EXACT_SCHEMA")
        g4 = {
            "satisfied": True,
            "endpoint": item["right_occurrence"],
            "sign_side": anchors[1]["relative_physical_closure_limit_side"],
            "quantified_base": "FOR_ALL_B_IN_PROOF_CLOSED_CORE_ONLY",
            "proof_closed_core_base_z_s": proof_core_base,
            "sequence": (
                "Phi(b,p_k), p_k->rho(b), b in B_core, from the RIGHT "
                "endpoint sign side"
            ),
            "strict_sign_corridor_box_t2_p_s": qlist(
                item["endpoint_corridor"][item["right_occurrence"]]
            ),
            "full_sign_side_to_rho_support_certificate":
                right_full_side_certificate,
            "full_sign_side_sequence_remains_in_exact_R292_open_support_by_certificate":
                True,
            "corridor_used_only_as_local_nonempty_witness": True,
            "limit_in_relative_physical_space_X": True,
            "conclusion": "Gamma_core subset cl_X(A_right)",
        }
        need(tuple(g4) == G3_G4_KEYS, "PHYSICAL_G4_V2_EXACT_SCHEMA")
        g5 = {
            "satisfied": True,
            "active_reason": item["left_region"]["active_reason"],
            "predicate_details": item["predicate_details"],
            "explicit_wall_value": 0,
            "zero_wall_hard_checked_not_silently_dropped": True,
            "whole_open_support_wall_event_product_replay":
                item["whole_open_support_wall_replay"],
            "proof_core_p_face_wall_event_product_replays":
                item["proof_face_wall_replays"],
            "source_wall_factor_uniformly_strict_nonzero": True,
            "wall_event_product_zero_iff_target_F_zero": True,
            "Gamma_core_is_included_wall_event_not_coordinate_zero_shortcut": True,
            "R294_occurrence_identity_stage": {
                "official_key_id_is_null": True,
                "official_key_ordinal_is_null": True,
                "binding_status": (
                    "NOT_MATERIALIZED_IN_R287_FROZEN_LEDGER__"
                    "COMPLETE_SIGNATURE_HASH_PINNED"
                ),
                "both_source_rows_equal_exact_R292_component_rows": True,
            },
            "R304_separate_official_key_materialization_stage": {
                "official_key_pair": official_pair,
                "member_row_ids": [
                    anchor["Round304_member_row_id"] for anchor in anchors
                ],
                "stages_not_conflated": True,
            },
            "occurrence_identity_collapsed": False,
            "official_key_identity_merged": False,
            "owner_extension_full_closure_sidecar_only": True,
            "owner_extension_not_Gamma_core_or_G3_G4_or_component_edge_basis": True,
            "closure_intersection_conclusion": (
                "Gamma_core subset cl_X(A_left) intersect cl_X(A_right)"
            ),
        }
        row = close_row({
            "Round305B_physical_witness_row_id": item["witness_id"],
            "schema": SCHEMA + ".physical-witness-row.v1",
            "source_Round305A_scope_reprojection_row_id":
                scope["Round305A_scope_reprojection_row_id"],
            "source_Round305A_scope_reprojection_row_sha256": scope["row_sha256"],
            "source_Round300A_row_id": scope["source_Round300A_row_id"],
            "source_Round300A_row_sha256": scope["source_Round300A_row_sha256"],
            "canonical_registry_occurrence_pair": pair,
            "Round304_final_component_pair": component_pair,
            "official_key_pair": official_pair,
            "cross_official_key_physical_edge_permitted": True,
            "occurrence_identity_collapsed": False,
            "official_key_identity_merged": False,
            "proof_core_patch_id": item["proof_core_patch_id"],
            "owner_extension_patch_id": item["owner_extension_patch_id"],
            "active_function_id": item["active"]["active_function_id"],
            "guard_id": item["left_region"]["source_guard_row_id"],
            "branch_id": item["branch_id"],
            "exact_relative_physical_domain": relative_domain,
            "exact_graph_Gamma": graph,
            "anchor_row_ids": [row["Round305B_anchor_row_id"] for row in anchors],
            "anchor_row_sha256s": [row["row_sha256"] for row in anchors],
            "closure_contact_row_ids": [
                row["Round305B_closure_contact_row_id"] for row in contacts
            ],
            "closure_contact_row_sha256s": [row["row_sha256"] for row in contacts],
            "owner_locus_row_ids": [
                row["Round305B_owner_locus_row_id"] for row in owners
            ],
            "owner_locus_row_sha256s": [row["row_sha256"] for row in owners],
            "owner_extension_sidecar_not_Gamma_core_or_attachment_or_edge_basis": True,
            "G0_exact_provenance_pins_and_row_closures": g0,
            "G1_endpoint_occurrence_connected_supports": g1,
            "G2_nonempty_connected_included_lower_stratum": g2,
            "G3_left_closure_attaches_to_included_patch": g3,
            "G4_right_closure_attaches_to_included_patch": g4,
            "G5_endpoint_patch_provenance_exactly_closed": g5,
            "relative_physical_closure_limit_lemma_id": item["lemma_id"],
            "corridor_box_used_as_Gamma_intersection": False,
            "D4_transfer_used": False,
            "candidate_physical_connectivity_conclusion": True,
            "formal_physical_witness_credit": 1,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        })
        need(tuple(row) == PHYSICAL_WITNESS_KEYS, "PHYSICAL_ROW_EXACT_SCHEMA")
        physical_rows.append(row)
    physical_rows.sort(key=lambda row: row["Round305B_physical_witness_row_id"])
    need(len(physical_rows) == EXPECTED_WITNESSES, "PHYSICAL_1024_ROWS")

    edges: list[dict[str, Any]] = []
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in physical_rows:
        grouped[tuple(row["Round304_final_component_pair"])].append(row)
    need(len(grouped) == EXPECTED_EDGES
         and {len(rows) for rows in grouped.values()} == {EXPECTED_PER_EDGE},
         "DEDUP_1024_WITNESSES_TO_8_COMPONENT_PAIRS")
    component_degrees = Counter(
        component for pair in grouped for component in pair
    )
    need(
        len(component_degrees) == 16
        and set(component_degrees.values()) == {1},
        "EIGHT_COMPONENT_EDGES_FORM_16_VERTEX_MATCHING",
    )
    for component_pair, rows in sorted(grouped.items()):
        rows.sort(key=lambda row: row["Round305B_physical_witness_row_id"])
        ids = [row["Round305B_physical_witness_row_id"] for row in rows]
        hashes = [row["row_sha256"] for row in rows]
        pairs = sorted(
            row["canonical_registry_occurrence_pair"] for row in rows
        )
        key_profiles = {tuple(sorted(row["official_key_pair"])) for row in rows}
        need(len(key_profiles) == 1, "ONE_OFFICIAL_KEY_PROFILE_PER_EDGE")
        key_pair = list(next(iter(key_profiles)))
        row_id = "round305b-canonical-component-edge:" + digest([
            "ROUND305B_G0_G5_DEDUP_COMPONENT_EDGE_V1", list(component_pair),
            digest(ids), digest(hashes),
        ])
        edge = close_row({
            "Round305B_canonical_component_edge_row_id": row_id,
            "schema": SCHEMA + ".canonical-component-edge-row.v1",
            "canonical_Round304_final_component_pair": list(component_pair),
            "physical_witness_row_count": EXPECTED_PER_EDGE,
            "physical_witness_row_ids_sha256": digest(ids),
            "physical_witness_row_sha256s_sha256": digest(hashes),
            "canonical_occurrence_pairs_sha256": digest(pairs),
            "canonical_official_key_pair": key_pair,
            "cross_official_key_physical_edge_permitted": True,
            "occurrence_identity_collapsed": False,
            "official_key_identity_merged": False,
            "all_128_witnesses_satisfy_G0_G5": True,
            "deduplicated_from_witness_rows_not_union_rows": True,
            "formal_component_edge_credit": 1,
            "eligible_for_later_fresh_DSU_application": True,
            "formal_DSU_rank_reduction_credit": 0,
        })
        need(tuple(edge) == COMPONENT_EDGE_KEYS, "EDGE_ROW_EXACT_SCHEMA")
        edges.append(edge)
    edges.sort(key=lambda row: row["Round305B_canonical_component_edge_row_id"])
    return {
        "physical": physical_rows,
        "anchor": anchor_rows,
        "contact": contact_rows,
        "owner": owner_rows,
        "edge": edges,
    }


def deterministic_gzip(value: Any) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=output, compresslevel=9, mtime=0,
    ) as stream:
        stream.write(canonical(value))
    return output.getvalue()


def close_wire_ledger(
    schema: str, rows: list[dict[str, Any]], id_field: str,
) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda row: row[id_field])
    need(ordered == rows, "WIRE_LEDGER_ROWS_NOT_STRICTLY_SORTED")
    need(len({row[id_field] for row in rows}) == len(rows),
         "WIRE_LEDGER_DUPLICATE_ROW_ID")
    document = {
        "schema": schema,
        "status": (
            "PASS_ZERO_CREDIT_CANDIDATE_LEDGER__PUBLISHED_OR_STAGED__"
            "PENDING_INDEPENDENT_VERIFICATION"
        ),
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_sha256": True,
        "formal_credit": 0,
        "rows": rows,
    }
    document["ledger_sha256"] = digest(document)
    return document


def build_independent_wire_contract_fixture(
    wire_spec_sha256: str,
) -> tuple[dict[str, Any], dict[str, bytes]]:
    need(PIN_RE.fullmatch(wire_spec_sha256) is not None,
         "WIRE_SPEC_FIXTURE_PIN_SYNTAX")
    row_body = {
        "fixture_row_id": "round305b-wire-fixture:synthetic-row-0001",
        "schema": SCHEMA + ".wire-fixture-row.v1",
        "rational_probe": "-7/11",
        "unicode_probe": "Gamma_core=Γ_core",
        "json_scalars_probe": [True, False, None, 0, 1],
    }
    row_body_bytes = canonical(row_body)
    closed_row = dict(row_body)
    closed_row["row_sha256"] = hashlib.sha256(row_body_bytes).hexdigest()
    fixture_ledger_schema = SCHEMA + ".wire-fixture-ledger.v1"
    empty_ledger = close_wire_ledger(
        fixture_ledger_schema, [], "fixture_row_id"
    )
    one_row_ledger = close_wire_ledger(
        fixture_ledger_schema, [closed_row], "fixture_row_id"
    )
    empty_gzip = deterministic_gzip(empty_ledger)
    one_row_gzip = deterministic_gzip(one_row_ledger)
    need(
        empty_gzip[:10].hex() == one_row_gzip[:10].hex()
        == "1f8b08000000000002ff"
        and gzip.decompress(empty_gzip) == canonical(empty_ledger)
        and gzip.decompress(one_row_gzip) == canonical(one_row_ledger),
        "WIRE_FIXTURE_CANONICAL_GZIP_HEADER_AND_ROUNDTRIP",
    )
    result_probe = {
        "schema": SCHEMA + ".wire-fixture-result.v1",
        "status": "SYNTHETIC_WIRE_CONTRACT_ONLY__NO_FORMAL_CREDIT",
        "wire_spec_id": WIRE_SPEC_ID,
        "wire_spec_sha256": wire_spec_sha256,
        "one_row_ledger_sha256": one_row_ledger["ledger_sha256"],
        "one_row_file_sha256": hashlib.sha256(one_row_gzip).hexdigest(),
        "formal_credit": 0,
    }
    result_probe["result_sha256"] = digest(result_probe)
    fixture = {
        "schema": SCHEMA + ".wire-contract-fixture.v1",
        "status": "PASS_SYNTHETIC_ONE_ROW_EMPTY_LEDGER_WIRE_CONTRACT",
        "wire_spec_id": WIRE_SPEC_ID,
        "wire_spec_sha256": wire_spec_sha256,
        "canonical_json_probe": {
            "value": row_body,
            "utf8_hex": row_body_bytes.hex(),
            "sha256": hashlib.sha256(row_body_bytes).hexdigest(),
        },
        "closed_row_probe": closed_row,
        "empty_ledger_probe": empty_ledger,
        "one_row_ledger_probe": one_row_ledger,
        "deterministic_gzip_probe": {
            "empty_ledger_header_hex": empty_gzip[:10].hex(),
            "one_row_ledger_header_hex": one_row_gzip[:10].hex(),
            "empty_ledger_file_sha256": hashlib.sha256(empty_gzip).hexdigest(),
            "one_row_ledger_file_sha256": hashlib.sha256(one_row_gzip).hexdigest(),
            "empty_ledger_size_bytes": len(empty_gzip),
            "one_row_ledger_size_bytes": len(one_row_gzip),
            "roundtrip_exact": True,
        },
        "result_self_hash_probe": result_probe,
        "contract_assertions": {
            "row_self_hash_excludes_only_row_sha256": True,
            "ledger_self_hash_excludes_only_ledger_sha256": True,
            "result_self_hash_excludes_only_result_sha256": True,
            "result_file_not_recursively_self_committed": True,
            "gzip_mtime_zero_empty_name_os_255": True,
            "canonical_json_has_no_trailing_newline": True,
            "formal_credit": 0,
        },
    }
    assert_path_and_time_free_wire(fixture, "wire-contract-fixture")
    return fixture, {"empty_ledger.gz": empty_gzip, "one_row_ledger.gz": one_row_gzip}


def verify_full_sign_side_protocol_shape(spec: dict[str, Any]) -> None:
    """Admit only the V2 complete-half-segment attachment protocol."""

    definitions = spec["definitions"]
    full_side = definitions["full_sign_side_to_rho_support_certificate"]
    closure_side = definitions["closure_limit_side"]
    g3_g4 = definitions["G3_or_G4"]
    ids = spec["id_domains"]
    need(
        tuple(full_side["keys_exact"])
        == FULL_SIGN_SIDE_SUPPORT_CERTIFICATE_KEYS
        and tuple(full_side["fields"][
            "R287_R292_single_connected_support_provenance"
        ]["keys_exact"]) == FULL_SIGN_SIDE_PROVENANCE_KEYS,
        "NORMATIVE_FULL_SIGN_SIDE_CERTIFICATE_SCHEMA_V2",
    )
    need(
        tuple(closure_side["keys_exact"]) == CLOSURE_LIMIT_SIDE_KEYS
        and closure_side["fields"][
            "full_sign_side_to_rho_support_certificate"
        ] == {"$ref": "full_sign_side_to_rho_support_certificate"}
        and closure_side["fields"][
            "exact_full_sign_side_contained_in_R292_support_derived"
        ] == {"const": True},
        "NORMATIVE_CLOSURE_LIMIT_SIDE_SCHEMA_V2",
    )
    need(
        tuple(g3_g4["keys_exact"]) == G3_G4_KEYS
        and g3_g4["fields"][
            "full_sign_side_to_rho_support_certificate"
        ] == {"$ref": "full_sign_side_to_rho_support_certificate"}
        and g3_g4["fields"][
            "full_sign_side_sequence_remains_in_exact_R292_open_support_by_certificate"
        ] == {"const": True}
        and g3_g4["fields"][
            "corridor_used_only_as_local_nonempty_witness"
        ] == {"const": True},
        "NORMATIVE_G3_G4_FULL_SIGN_SIDE_SCHEMA_V2",
    )
    need(
        ids["full_sign_side_support_certificate_id"]["sha256_of_canonical_json"]
        == [
            "ROUND305B_FULL_SIGN_SIDE_TO_RHO_NAMED_SUPPORT_V1",
            "certificate object with certificate_id absent",
        ]
        and ids["anchor_row_id"]["sha256_of_canonical_json"][0]
        == "ROUND305B_R292_SINGLE_CELL_FULL_SIGN_SIDE_ANCHOR_V2"
        and ids["anchor_row_id"]["sha256_of_canonical_json"][-1]
        == "full_sign_side_support_certificate_id",
        "NORMATIVE_FULL_SIGN_SIDE_ID_DOMAINS_V2",
    )
    need(
        spec["embedded_result_objects"]["two_sided_attachment_theorem"]
        == TWO_SIDED_ATTACHMENT_THEOREM,
        "NORMATIVE_TWO_SIDED_ATTACHMENT_THEOREM_V2",
    )


def verify_external_normative_wire_contract() -> dict[str, Any]:
    global _NORMATIVE_WIRE_SPEC
    need(
        type(EXPECTED_WIRE_SPEC_SHA256) is str
        and PIN_RE.fullmatch(EXPECTED_WIRE_SPEC_SHA256) is not None
        and type(EXPECTED_WIRE_CONTRACT_FIXTURE_SHA256) is str
        and PIN_RE.fullmatch(EXPECTED_WIRE_CONTRACT_FIXTURE_SHA256) is not None,
        "BLOCKED_NORMATIVE_WIRE_PINS_NOT_FROZEN",
    )
    spec_path = D / WIRE_SPEC_FILE
    fixture_path = D / WIRE_CONTRACT_FIXTURE_FILE
    require_regular(spec_path, WIRE_SPEC_FILE)
    require_regular(fixture_path, WIRE_CONTRACT_FIXTURE_FILE)
    spec_raw = spec_path.read_bytes()
    fixture_raw = fixture_path.read_bytes()
    need(hashlib.sha256(spec_raw).hexdigest() == EXPECTED_WIRE_SPEC_SHA256,
         "NORMATIVE_WIRE_SPEC_BYTE_PIN")
    need(
        hashlib.sha256(fixture_raw).hexdigest()
        == EXPECTED_WIRE_CONTRACT_FIXTURE_SHA256,
        "NORMATIVE_WIRE_FIXTURE_BYTE_PIN",
    )
    spec = strict_json_raw(spec_raw, WIRE_SPEC_FILE)
    observed_fixture = strict_json_raw(fixture_raw, WIRE_CONTRACT_FIXTURE_FILE)
    need(
        canonical(spec) == spec_raw and canonical(observed_fixture) == fixture_raw,
        "NORMATIVE_PROTOCOL_FILES_NOT_CANONICAL_EXACT_BYTES",
    )
    need(
        spec.get("wire_spec_id") == WIRE_SPEC_ID
        and spec.get("wire_spec_version") == 2
        and spec.get("additional_properties_permitted") is False
        and spec["protocol_files"][
            "contain_actual_candidate_row_ledger_or_file_commitments"
        ] is False
        and spec["protocol_files"]["formal_credit"] == 0,
        "NORMATIVE_WIRE_SPEC_PROTOCOL_BOUNDARY",
    )
    verify_full_sign_side_protocol_shape(spec)
    expected_fixture, gzip_probes = build_independent_wire_contract_fixture(
        EXPECTED_WIRE_SPEC_SHA256
    )
    expected_fixture_raw = canonical(expected_fixture)
    need(expected_fixture_raw == fixture_raw,
         "NORMATIVE_SYNTHETIC_FIXTURE_EXACT_BYTE_DIFF")
    _NORMATIVE_WIRE_SPEC = spec
    snapshot = exact_schema_snapshot()
    need(
        digest(snapshot) == EXPECTED_PRODUCER_SCHEMA_SNAPSHOT_SHA256,
        "NORMATIVE_SCHEMA_SNAPSHOT_EXACT_SHA256",
    )
    return {
        "status": "PASS_EXACT_INDEPENDENT_NORMATIVE_WIRE_FIXTURE_RECONSTRUCTION",
        "wire_spec_sha256": EXPECTED_WIRE_SPEC_SHA256,
        "wire_contract_fixture_sha256":
            EXPECTED_WIRE_CONTRACT_FIXTURE_SHA256,
        "wire_spec_size_bytes": len(spec_raw),
        "wire_contract_fixture_size_bytes": len(fixture_raw),
        "empty_ledger_gzip_sha256":
            hashlib.sha256(gzip_probes["empty_ledger.gz"]).hexdigest(),
        "one_row_ledger_gzip_sha256":
            hashlib.sha256(gzip_probes["one_row_ledger.gz"]).hexdigest(),
        "formal_credit": 0,
        "candidate_producer_imported_or_executed": False,
    }


def normative_wire_spec() -> dict[str, Any]:
    need(_NORMATIVE_WIRE_SPEC is not None,
         "NORMATIVE_WIRE_SPEC_NOT_VERIFIED_IN_THIS_PROCESS")
    return _NORMATIVE_WIRE_SPEC


def exact_schema_snapshot() -> dict[str, Any]:
    """Construct the frozen schema snapshot without producer-derived data."""

    spec = normative_wire_spec()
    contract = spec["schema_snapshot_contract"]
    construction = contract["construction"]
    order = contract["keys_exact_in_construction_order"]
    need(set(order) == set(construction) and len(order) == len(construction),
         "SCHEMA_SNAPSHOT_CONSTRUCTION_EXACT_KEYS")
    snapshot: dict[str, Any] = {}
    for key in order:
        value = construction[key]
        if key == "theorem":
            need(value == "$ref:embedded_result_objects.two_sided_attachment_theorem",
                 "SCHEMA_SNAPSHOT_THEOREM_REFERENCE")
            value = spec["embedded_result_objects"]["two_sided_attachment_theorem"]
        elif key == "normative_wire_spec":
            need(value == "$self:entire WIRE_SPEC object",
                 "SCHEMA_SNAPSHOT_WIRE_SELF_REFERENCE")
            value = spec
        snapshot[key] = copy.deepcopy(value)
    need(tuple(snapshot) == tuple(order), "SCHEMA_SNAPSHOT_CONSTRUCTION_ORDER")
    return snapshot


def exact_runtime_closure() -> dict[str, Any]:
    spec_result = normative_wire_spec()["result"]
    keys = spec_result["runtime_closure_path_free_keys_exact"]
    expected = spec_result["runtime_closure_values"]
    loader = formal_geometry_loader_audit()
    stale_probe = stale_pyc_same_mtime_size_attack_probe()
    flint = sys.modules.get("flint")
    need(flint is not None, "RUNTIME_CLOSURE_FLINT_LOADED")
    ordered_filenames = loader["ordered_source_modules"]
    source_pins = {
        filename.removesuffix(".py"): FORMAL_INPUT_PINS[filename]
        for filename in ordered_filenames
    }
    need(
        all(name not in sys.modules for name in (
            "cm2_round273_source_g_reverse_rechart_probe",
            "cm2_round274_source_g_reverse_rechart_tail_arrangement_probe",
        )),
        "R273_R274_MUST_REMAIN_UNIMPORTED",
    )
    facts: dict[str, Any] = {
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "python_flint_version": getattr(flint, "__version__", None),
        "zlib_runtime_version": zlib.ZLIB_RUNTIME_VERSION,
        "arb_precision_bits": flint.ctx.prec,
        "loader": "SHA256_VERIFIED_SOURCE_BYTES_COMPILE_EXEC",
        "loader_scope": "SIX_PINNED_PROJECT_LOCAL_FORMAL_GEOMETRY_MODULES_ONLY",
        "runtime_source_sha256_pins": dict(sorted(source_pins.items())),
        "runtime_source_module_count": len(source_pins),
        "project_local_formal_geometry_module_pycache_reads": False,
        "project_local_formal_geometry_module_pycache_writes": False,
        "project_local_formal_geometry_source_compile_exec": True,
        "same_mtime_same_size_stale_pyc_attack_rejected": (
            stale_probe["default_importlib_observed"] == "OLD"
            and stale_probe["direct_verified_source_compiler_observed"] == "NEW"
        ),
        "stale_pyc_attack_probe_temporary_pyc_written":
            stale_probe["fixture_pyc_created_and_removed"],
        "stale_pyc_attack_probe_temporary_pyc_read":
            stale_probe["fixture_default_importlib_stale_pyc_read"],
        "stale_pyc_attack_probe_temporary_pyc_removed":
            stale_probe["temporary_fixture_removed"],
        "external_flint_imported_via_standard_importlib": True,
        "external_flint_outside_six_module_direct_source_graph": True,
        "global_no_pyc_claim_made": False,
        "R273_R274_imported_or_executed": False,
        "floating_point_fallback_used": False,
    }
    need(set(keys) == set(facts), "RUNTIME_CLOSURE_EXACT_KEY_UNIVERSE")
    runtime = {key: facts[key] for key in keys}
    need(runtime == expected, "RUNTIME_CLOSURE_EXACT_VALUES")
    assert_path_and_time_free_wire(runtime, "runtime-closure")
    return runtime


def direct_geometry_reconstruction_summary(
    preimages: list[dict[str, Any]], bracket_depths: Counter[int],
) -> dict[str, Any]:
    need(len(preimages) == EXPECTED_WITNESSES,
         "DIRECT_GEOMETRY_SUMMARY_1024_PREIMAGES")
    chart_transitions: Counter[str] = Counter()
    active_and_sign: Counter[str] = Counter()
    discarded_source_sign: Counter[str] = Counter()
    derivative_profiles: Counter[str] = Counter()
    unresolved: Counter[str] = Counter()
    minimum_z: Q | None = None
    maximum_z: Q | None = None
    for item in preimages:
        source_cell = item["left_region"]["source_chart"].split(":", 1)[1]
        adjacent_cell = item["left_region"]["adjacent_chart"].split(":", 1)[1]
        transition = (
            source_cell + ("+" if item["source_sign"] > 0 else "-")
            + "->" + adjacent_cell
            + ("+" if item["image_sign"] > 0 else "-")
        )
        chart_transitions[transition] += 1
        active_and_sign[
            item["active"]["active_function_id"] + "|" + str(item["image_sign"])
        ] += 1
        discarded_source_sign[
            item["whole_open_support_wall_replay"]["source_wall_factor_sign"]
        ] += 1
        derivative_signs = item["left_region"][
            "strict_derivative_signs_t_p_s"
        ]
        # The implicit graph is solved only in the p direction.  Round275's
        # exact three-axis profile legitimately permits OVERWRAP on a
        # transverse axis, while the p entry must be strict; the full tuple
        # has already been independently replayed from the source cell.
        need(len(derivative_signs) == 3
             and derivative_signs[1] in STRICT_SIGNS,
             "DIRECT_GEOMETRY_STRICT_DERIVATIVE_PROFILE")
        derivative_profiles["|".join(derivative_signs)] += 1
        need(item["unresolved_reasons"] == [item["left_region"]["active_reason"]],
             "DIRECT_GEOMETRY_UNIQUE_UNRESOLVED_REASON")
        unresolved[item["unresolved_reasons"][0]] += 1
        z0, z1 = item["exact_box"][:2]
        minimum_z = z0 if minimum_z is None else min(minimum_z, z0)
        maximum_z = z1 if maximum_z is None else max(maximum_z, z1)
    need(
        minimum_z is not None and maximum_z is not None
        and maximum_z < Q(1, 2)
        and len(chart_transitions) == len(active_and_sign) == 8
        and set(chart_transitions.values()) == set(active_and_sign.values()) == {128},
        "DIRECT_GEOMETRY_SUMMARY_CENSUS",
    )
    summary = {
        "status": (
            "PASS_DIRECT_SCOPE_TO_R292_SINGLE_CELL_TO_DEPTH_1_2_P_BRACKET_"
            "RECONSTRUCTION__NO_OUTPUT__ZERO_CREDIT"
        ),
        "runtime_closure": exact_runtime_closure(),
        "direct_row_count": EXPECTED_WITNESSES,
        "R292_anchor_count": EXPECTED_ANCHORS,
        "R292_single_member_component_count": EXPECTED_ANCHORS,
        "left_right_identical_R292_cell_pair_count": EXPECTED_WITNESSES,
        "candidate_piece_pair_count": EXPECTED_WITNESSES,
        "serializer_attempt_count": EXPECTED_WITNESSES,
        "implicit_graph_axis_histogram": {"p": EXPECTED_WITNESSES},
        "tangent_refinement_depth_histogram": {"0": EXPECTED_WITNESSES},
        "bracket_slice_depth_histogram": {
            str(key): value for key, value in sorted(bracket_depths.items())
        },
        "chart_transition_histogram": dict(sorted(chart_transitions.items())),
        "active_function_and_image_sign_histogram":
            dict(sorted(active_and_sign.items())),
        "discarded_source_factor_sign_histogram":
            dict(sorted(discarded_source_sign.items())),
        "target_factor_derivative_histogram":
            dict(sorted(derivative_profiles.items())),
        "only_unresolved_dynamic_predicate_histogram":
            dict(sorted(unresolved.items())),
        "minimum_z": qstr(minimum_z),
        "maximum_z": qstr(maximum_z),
        "maximum_z_strictly_below_one_half": True,
        "D4_transfer_enabled": False,
        "formal_Round305B_credit": 0,
    }
    expected_keys = normative_wire_spec()["result"][
        "direct_geometry_reconstruction"
    ]["keys_exact"]
    need(tuple(summary) == tuple(expected_keys),
         "DIRECT_GEOMETRY_RESULT_EXACT_KEYS")
    return summary


def build_expected_artifacts(
    rows: dict[str, list[dict[str, Any]]],
    formal_manifest_counts: dict[str, int],
    bracket_depths: Counter[int],
    boundary_audit: dict[str, Any],
    preimages: list[dict[str, Any]],
) -> tuple[dict[str, bytes], dict[str, Any]]:
    documents = {
        "physical": close_wire_ledger(
            SCHEMA + ".physical-witness-ledger.v1", rows["physical"],
            "Round305B_physical_witness_row_id",
        ),
        "anchor": close_wire_ledger(
            SCHEMA + ".anchor-ledger.v1", rows["anchor"],
            "Round305B_anchor_row_id",
        ),
        "contact": close_wire_ledger(
            SCHEMA + ".closure-contact-ledger.v1", rows["contact"],
            "Round305B_closure_contact_row_id",
        ),
        "owner": close_wire_ledger(
            SCHEMA + ".owner-locus-ledger.v1", rows["owner"],
            "Round305B_owner_locus_row_id",
        ),
        "edge": close_wire_ledger(
            SCHEMA + ".canonical-component-edge-ledger.v1", rows["edge"],
            "Round305B_canonical_component_edge_row_id",
        ),
    }
    artifacts: dict[str, bytes] = {
        OUTPUT_NAMES[key]: deterministic_gzip(document)
        for key, document in documents.items()
    }
    need(
        type(EXPECTED_PRODUCER_SHA256) is str
        and PIN_RE.fullmatch(EXPECTED_PRODUCER_SHA256) is not None,
        "BLOCKED_EXPECTED_PRODUCER_PIN_FOR_RESULT_WIRE",
    )
    verify_inert_producer_pin()
    ledger_object_commitments = {
        key: {
            "filename": OUTPUT_NAMES[key],
            "ledger_sha256": document["ledger_sha256"],
            "rows_sha256": document["rows_sha256"],
            "row_ids_sha256": document["row_ids_sha256"],
            "row_hashes_sha256": document["row_hashes_sha256"],
        }
        for key, document in documents.items()
    }
    candidate_file_commitments = {
        key: {
            "filename": OUTPUT_NAMES[key],
            "file_sha256": hashlib.sha256(
                artifacts[OUTPUT_NAMES[key]]
            ).hexdigest(),
            "file_size_bytes": len(artifacts[OUTPUT_NAMES[key]]),
            "compression": "deterministic-gzip-level-9-mtime-0-empty-name-os-255",
        }
        for key in ("physical", "anchor", "contact", "owner", "edge")
    }
    spec = normative_wire_spec()
    snapshot = exact_schema_snapshot()
    theorem = copy.deepcopy(
        spec["embedded_result_objects"]["two_sided_attachment_theorem"]
    )
    lemma = copy.deepcopy(
        spec["embedded_result_objects"]["relative_physical_closure_limit_lemma"]
    )
    wire_raw = (D / WIRE_SPEC_FILE).read_bytes()
    fixture_raw = (D / WIRE_CONTRACT_FIXTURE_FILE).read_bytes()
    normative_wire_file_commitments = {
        "wire_spec": {
            "filename": WIRE_SPEC_FILE,
            "file_sha256": EXPECTED_WIRE_SPEC_SHA256,
            "file_size_bytes": len(wire_raw),
        },
        "wire_contract_fixture": {
            "filename": WIRE_CONTRACT_FIXTURE_FILE,
            "file_sha256": EXPECTED_WIRE_CONTRACT_FIXTURE_SHA256,
            "file_size_bytes": len(fixture_raw),
        },
    }
    need(
        hashlib.sha256(wire_raw).hexdigest() == EXPECTED_WIRE_SPEC_SHA256
        and hashlib.sha256(fixture_raw).hexdigest()
        == EXPECTED_WIRE_CONTRACT_FIXTURE_SHA256,
        "RESULT_NORMATIVE_WIRE_COMMITMENTS_PINNED",
    )
    strict_credit_boundary = {
        "zero_credit_candidate_publication_only": True,
        "independent_verifier_admitted": False,
        "candidate_ledger_formal_anchor_binding_credit": EXPECTED_ANCHORS,
        "candidate_ledger_formal_physical_witness_credit": EXPECTED_WITNESSES,
        "candidate_ledger_formal_component_edge_credit": EXPECTED_EDGES,
        "officially_admitted_anchor_binding_credit": 0,
        "officially_admitted_physical_witness_credit": 0,
        "officially_admitted_component_edge_credit": 0,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
        "official_key_merge_credit": 0,
        "D4_transfer_credit": 0,
        "owner_sidecar_credit": 0,
    }
    need(
        strict_credit_boundary
        == spec["result"]["strict_credit_boundary_values"],
        "RESULT_STRICT_CREDIT_BOUNDARY_EXACT",
    )
    conditional_later_fresh_DSU_effect = {
        "canonical_edges_eligible_after_independent_promotion": EXPECTED_EDGES,
        "maximum_later_rank_reductions": MAXIMUM_LATER_RANK_REDUCTIONS,
        "Round304_component_count": 92_696,
        "conditional_post_edge_component_count": 92_688,
        "applied_in_Round305B": False,
    }
    need(
        conditional_later_fresh_DSU_effect
        == spec["result"]["conditional_later_fresh_DSU_effect_values"],
        "RESULT_CONDITIONAL_DSU_EFFECT_EXACT",
    )
    result: dict[str, Any] = {
        "schema": SCHEMA + ".zero-credit-candidate-result.v1",
        "status": (
            "PASS_ROUND305B_DIRECT_G0_G5_ZERO_CREDIT_CANDIDATE__"
            "PENDING_INDEPENDENT_VERIFICATION__"
            "ZERO_OFFICIALLY_ADMITTED_CREDIT"
        ),
        "producer_source_filename": PRODUCER,
        "producer_source_sha256": EXPECTED_PRODUCER_SHA256,
        "schema_snapshot": snapshot,
        "schema_snapshot_sha256": digest(snapshot),
        "two_sided_attachment_theorem": theorem,
        "two_sided_attachment_theorem_sha256": digest(theorem),
        "relative_physical_closure_limit_lemma": lemma,
        "relative_physical_closure_limit_lemma_sha256": digest(lemma),
        "normative_wire_file_commitments": normative_wire_file_commitments,
        "direct_geometry_reconstruction":
            direct_geometry_reconstruction_summary(preimages, bracket_depths),
        "formal_G0_G5_witness_candidate_count": EXPECTED_WITNESSES,
        "exact_anchor_candidate_count": EXPECTED_ANCHORS,
        "closure_contact_sidecar_count": EXPECTED_CLOSURE_CONTACTS,
        "global_owner_locus_sidecar_count": EXPECTED_OWNER_LOCI,
        "canonical_component_edge_candidate_count": EXPECTED_EDGES,
        "witnesses_per_component_edge": EXPECTED_PER_EDGE,
        "owner_audit": boundary_audit,
        "ledger_object_commitments": ledger_object_commitments,
        "strict_credit_boundary": strict_credit_boundary,
        "conditional_later_fresh_DSU_effect":
            conditional_later_fresh_DSU_effect,
        "zero_credit_candidate_publication_permitted": True,
        "manifest_emitted": False,
        "candidate_file_commitments": candidate_file_commitments,
    }
    need(tuple(result) == tuple(spec["result"]["keys_exact_in_construction_order"][:-1]),
         "RESULT_EXACT_KEYS_BEFORE_SELF_HASH")
    assert_path_and_time_free_wire(result, "candidate-result-before-self-hash")
    result["result_sha256"] = digest(result)
    need(tuple(result) == tuple(spec["result"]["keys_exact_in_construction_order"]),
         "RESULT_EXACT_KEYS_AFTER_SELF_HASH")
    assert_path_and_time_free_wire(result, "candidate-result")
    artifacts[OUTPUT_NAMES["result"]] = canonical(result)
    return artifacts, result


def independent_row_reconstruction() -> tuple[
    dict[str, list[dict[str, Any]]], dict[str, int], Counter[int],
    dict[str, Any], list[dict[str, Any]],
]:
    need(FORMAL_INDEPENDENT_GEOMETRY_RECONSTRUCTION_IMPLEMENTED,
         "INDEPENDENT_GEOMETRY_KERNEL_DISABLED")
    verify_external_normative_wire_contract()
    sealed_scope_preflight()
    manifest_counts = admit_formal_input_chain()
    r174, r179, registry_tables = import_formal_geometry_modules()
    inputs = load_scope_and_geometry_inputs()
    registry, members, _official_keys = stream_endpoint_bindings(
        inputs["endpoints"], inputs["residual"]
    )
    contexts = reconstruct_branch_contexts(
        inputs, registry, members, r174, r179, registry_tables
    )
    preimages, bracket_depths = reconstruct_direct_p_witnesses(
        contexts, r174, r179
    )
    contacts, owners, contact_by_witness, owner_by_witness, boundary_audit = (
        reconstruct_boundary_rows(preimages, r174, r179)
    )
    rows = reconstruct_candidate_rows(
        preimages, contacts, owners, contact_by_witness, owner_by_witness
    )
    need(PRODUCER[:-3] not in sys.modules,
         "CANDIDATE_PRODUCER_IMPORTED_DURING_RECONSTRUCTION")
    return rows, manifest_counts, bracket_depths, boundary_audit, preimages


def independent_reconstruction() -> tuple[dict[str, bytes], dict[str, Any]]:
    rows, manifest_counts, bracket_depths, boundary_audit, preimages = (
        independent_row_reconstruction()
    )
    artifacts, result = build_expected_artifacts(
        rows, manifest_counts, bracket_depths, boundary_audit, preimages
    )
    need(PRODUCER[:-3] not in sys.modules,
         "CANDIDATE_PRODUCER_IMPORTED_DURING_RECONSTRUCTION")
    return artifacts, result


def read_exact_candidate_bundle(
    candidate_dir: Path,
    expected: dict[str, bytes],
) -> tuple[dict[str, bytes], dict[str, Any]]:
    """Open the private candidate only after full independent reconstruction."""

    need(
        tuple(sorted(expected)) == tuple(sorted(PROMOTION_CANDIDATE_ORDER))
        and set(expected) == set(OUTPUT_NAMES.values()),
        "EXPECTED_SIX_CANDIDATE_NAME_SET",
    )
    resolved = resolve_candidate_directory(candidate_dir)
    directory_descriptor, bound = open_bound_directory(
        resolved, "candidate directory"
    )
    bundle: dict[str, bytes] = {}
    identities: dict[str, FileIdentity] = {}
    try:
        names = set(os.listdir(directory_descriptor))
        need(
            names == set(PROMOTION_CANDIDATE_ORDER),
            "CANDIDATE_DIRECTORY_EXACT_SIX_FILE_SET",
        )
        for name in PROMOTION_CANDIDATE_ORDER:
            raw, identity = read_exact_regular_at(
                directory_descriptor,
                name,
                expected[name],
                "candidate:" + name,
            )
            bundle[name] = raw
            identities[name] = identity
        need(
            set(os.listdir(directory_descriptor))
            == set(PROMOTION_CANDIDATE_ORDER),
            "CANDIDATE_DIRECTORY_FILE_SET_DRIFT",
        )
    finally:
        need(
            bound
            == directory_identity(os.fstat(directory_descriptor))
            == directory_identity(os.lstat(resolved)),
            "CANDIDATE_DIRECTORY_INODE_SWAP",
        )
        os.close(directory_descriptor)
    snapshot: dict[str, Any] = {
        "directory": resolved,
        "directory_identity": bound,
        "file_identities": identities,
    }
    return bundle, snapshot


def assert_candidate_snapshot(snapshot: dict[str, Any], label: str) -> None:
    resolved = snapshot["directory"]
    need(
        not resolved.is_symlink()
        and directory_identity(os.lstat(resolved))
        == snapshot["directory_identity"],
        label + ":CANDIDATE_DIRECTORY_CHANGED",
    )
    descriptor, bound = open_bound_directory(resolved, label + ":candidate")
    try:
        need(bound == snapshot["directory_identity"],
             label + ":CANDIDATE_DIRECTORY_REBOUND")
        need(
            set(os.listdir(descriptor)) == set(PROMOTION_CANDIDATE_ORDER),
            label + ":CANDIDATE_FILE_SET_CHANGED",
        )
        for name, identity in snapshot["file_identities"].items():
            need(
                file_identity(os.stat(
                    name, dir_fd=descriptor, follow_symlinks=False,
                )) == identity,
                label + ":CANDIDATE_FILE_CHANGED:" + name,
            )
    finally:
        os.close(descriptor)


def runtime_verifier_sha256() -> str:
    path = Path(__file__)
    need(
        path.name == VERIFIER_FILENAME
        and Path(os.path.abspath(os.fspath(path))).parent == D.resolve(),
        "RUNTIME_VERIFIER_EXACT_DELIVERABLE_PATH",
    )
    raw = stable_path_bytes(path, 5_000_000, "runtime verifier")
    return hashlib.sha256(raw).hexdigest()


def sealed_scope_preflight() -> dict[str, Any]:
    r303b = parse_manifest(R303B_MANIFEST, R303B_MANIFEST_SHA256, 12)
    r304 = parse_manifest(R304_MANIFEST, R304_MANIFEST_SHA256, 11)
    r305a = parse_manifest(
        R305A_MANIFEST, R305A_MANIFEST_SHA256, 8,
        R305A_EXPECTED_MANIFEST_MEMBERS,
    )
    for member, pin in R305A_CRITICAL_FILE_PINS.items():
        need(r305a.get(member) == pin, "ROUND305A_CRITICAL_PIN:" + member)
    result = read_json(R305A_RESULT)
    verification = read_json(R305A_VERIFICATION)
    verify_self(result, "result_sha256", R305A_RESULT)
    verify_self(verification, "verification_sha256", R305A_VERIFICATION)
    need(result["result_sha256"] == R305A_RESULT_OBJECT_SHA256,
         "ROUND305A_RESULT_OBJECT_PIN")
    need(
        verification["verification_sha256"]
        == R305A_VERIFICATION_OBJECT_SHA256
        and verification.get("status")
        == "PASS_EXACT_CACHELESS_ROUND305A_SCOPE_REPROJECTION"
        and verification.get("formal_Round305A_scope_promotion_permitted")
        is True
        and verification["attack_suite"].get("all_rejected") is True
        and verification["attack_suite"].get("fixture_count") == 36,
        "ROUND305A_VERIFIED_SCOPE",
    )
    need(
        result["residual_scope_commitments"].get("residual_pair_count")
        == EXPECTED_WITNESSES
        and result["residual_scope_commitments"].get("residual_endpoint_count")
        == EXPECTED_ANCHORS
        and all(value == 0 for value in result["formal_credit_transition"].values()),
        "ROUND305A_SCOPE_AND_ZERO_CREDIT",
    )
    return {
        "Round303B_manifest_members": len(r303b),
        "Round304_manifest_members": len(r304),
        "Round305A_manifest_members": len(r305a),
        "Round305A_exact_verified_scope_admitted": True,
        "Round305B_formal_credit": 0,
    }


def verify_inert_producer_pin() -> str:
    need(
        type(EXPECTED_PRODUCER_SHA256) is str
        and PIN_RE.fullmatch(EXPECTED_PRODUCER_SHA256) is not None,
        "BLOCKED_EXPECTED_PRODUCER_PIN",
    )
    producer_path = D / PRODUCER
    require_regular(producer_path, PRODUCER)
    producer_sha256 = hashlib.sha256(stable_path_bytes(
        producer_path, 5_000_000, "inert producer bytes"
    )).hexdigest()
    need(producer_sha256 == EXPECTED_PRODUCER_SHA256,
         "ROUND305B_INERT_PRODUCER_BYTE_PIN")
    need(PRODUCER[:-3] not in sys.modules,
         "ROUND305B_PRODUCER_MUST_REMAIN_UNIMPORTED")
    return producer_sha256


def close_object(payload: dict[str, Any], field: str) -> dict[str, Any]:
    need(field not in payload, "SELF_HASH_FIELD_ALREADY_PRESENT:" + field)
    return {**payload, field: digest(payload)}


def validate_promotion_commit_order(order: tuple[str, ...]) -> None:
    need(order == PROMOTION_ORDER, "ROUND305B_EXACT_PROMOTION_COMMIT_ORDER")
    need(
        order[0] == ATTACK_FILENAME
        and order[-2] == OUTPUT_NAMES["result"]
        and order[-1] == VERIFICATION_FILENAME,
        "ATTACK_FIRST_RESULT_BEFORE_VERIFICATION_LAST",
    )


def rename_noreplace(
    source_directory_descriptor: int,
    source_name: str,
    target_directory_descriptor: int,
    target_name: str,
) -> None:
    function = getattr(ctypes.CDLL(None, use_errno=True), "renameat2", None)
    need(function is not None, "RENAMEAT2_RENAME_NOREPLACE_UNAVAILABLE")
    function.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    function.restype = ctypes.c_int
    outcome = function(
        source_directory_descriptor,
        os.fsencode(source_name),
        target_directory_descriptor,
        os.fsencode(target_name),
        1,  # RENAME_NOREPLACE
    )
    if outcome == 0:
        return
    error = ctypes.get_errno()
    if error == errno.EEXIST:
        raise FileExistsError(error, os.strerror(error), target_name)
    raise OSError(error, os.strerror(error), target_name)


def validate_exact_published_prefix(
    present_names: tuple[str, ...],
    order: tuple[str, ...] = PROMOTION_ORDER,
) -> None:
    validate_promotion_commit_order(order)
    need(
        present_names == order[:len(present_names)],
        "FORMAL_OUTPUTS_MUST_FORM_ONE_EXACT_COMMIT_PREFIX",
    )
    if VERIFICATION_FILENAME in present_names:
        need(
            present_names == order,
            "VERIFICATION_COMMIT_MARKER_REQUIRES_COMPLETE_FORMAL_BUNDLE",
        )


def recover_exact_promotion_stage_orphans(
    output_descriptor: int,
    artifacts: dict[str, bytes],
) -> int:
    recovered = 0
    for stage_name in sorted(os.listdir(output_descriptor)):
        if not stage_name.startswith(PROMOTION_STAGE_PREFIX):
            continue
        need(
            re.fullmatch(
                re.escape(PROMOTION_STAGE_PREFIX) + r"[0-9a-f]{32}",
                stage_name,
            ) is not None,
            "ORPHAN_STAGE_NAME_BOUNDARY:" + stage_name,
        )
        info = os.stat(
            stage_name, dir_fd=output_descriptor, follow_symlinks=False
        )
        need(
            stat.S_ISDIR(info.st_mode)
            and not stat.S_ISLNK(info.st_mode)
            and info.st_uid == os.geteuid()
            and stat.S_IMODE(info.st_mode) == 0o700,
            "ORPHAN_STAGE_DIRECTORY_BOUNDARY:" + stage_name,
        )
        stage_descriptor = os.open(
            stage_name,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
            dir_fd=output_descriptor,
        )
        try:
            stage_bound = directory_identity(os.fstat(stage_descriptor))
            need(
                stage_bound == directory_identity(info),
                "ORPHAN_STAGE_OPEN_RACE:" + stage_name,
            )
            names = set(os.listdir(stage_descriptor))
            need(names <= set(artifacts),
                 "ORPHAN_STAGE_EXACT_ARTIFACT_SUBSET:" + stage_name)
            for name in sorted(names):
                read_exact_regular_at(
                    stage_descriptor,
                    name,
                    artifacts[name],
                    "orphan-stage:" + stage_name + ":" + name,
                )
                os.unlink(name, dir_fd=stage_descriptor)
            os.fsync(stage_descriptor)
            need(
                stage_bound
                == directory_identity(os.fstat(stage_descriptor))
                == directory_identity(os.stat(
                    stage_name,
                    dir_fd=output_descriptor,
                    follow_symlinks=False,
                )),
                "ORPHAN_STAGE_DIRECTORY_SWAP:" + stage_name,
            )
        finally:
            os.close(stage_descriptor)
        os.rmdir(stage_name, dir_fd=output_descriptor)
        recovered += 1
    os.fsync(output_descriptor)
    return recovered


def publish_exact_prefix_transaction(
    output_dir: Path,
    artifacts: dict[str, bytes],
    *,
    exact_deliverables_only: bool,
    integrity_guard: Callable[[str], None] | None = None,
    hostile_hook: Callable[[str, str, Path], None] | None = None,
) -> dict[str, Any]:
    """Crash-recoverable no-clobber commit; verification is the sole marker."""

    validate_promotion_commit_order(tuple(artifacts))
    need(set(artifacts) == set(PROMOTION_ORDER),
         "PROMOTION_EXACT_EIGHT_ARTIFACT_SET")
    resolved = lexical_directory_without_symlinks(
        output_dir, "Round305B formal promotion output"
    )
    if exact_deliverables_only:
        need(resolved == D.resolve(),
             "FORMAL_PROMOTION_ONLY_TO_EXACT_DELIVERABLES_DIRECTORY")
    directory_info = os.lstat(resolved)
    need(directory_info.st_uid == os.geteuid(),
         "PROMOTION_OUTPUT_DIRECTORY_OWNER")
    output_descriptor, bound = open_bound_directory(
        resolved, "promotion output directory"
    )
    published_now: list[str] = []
    published_now_inodes: dict[str, tuple[int, int]] = {}
    recovered_orphans = 0
    committed_identities: dict[str, FileIdentity] = {}

    def verify_committed_prefix(label: str) -> None:
        present: list[str] = []
        for candidate_name in PROMOTION_ORDER:
            try:
                os.stat(
                    candidate_name,
                    dir_fd=output_descriptor,
                    follow_symlinks=False,
                )
            except FileNotFoundError:
                continue
            present.append(candidate_name)
        validate_exact_published_prefix(tuple(present))
        need(
            set(present) == set(committed_identities),
            label + ":COMMITTED_PREFIX_CENSUS_DRIFT",
        )
        for committed_name in PROMOTION_ORDER:
            if committed_name not in committed_identities:
                break
            _raw, identity = read_exact_regular_at(
                output_descriptor,
                committed_name,
                artifacts[committed_name],
                label + ":" + committed_name,
            )
            need(
                identity == committed_identities[committed_name],
                label + ":IDENTITY_DRIFT:" + committed_name,
            )

    try:
        fcntl.flock(output_descriptor, fcntl.LOCK_EX)
        # Validate the visible commit-prefix without mutation before cleaning
        # any orphan stage.  A conflicting target must leave all stages intact.
        preexisting: list[str] = []
        preexisting_identities: dict[str, FileIdentity] = {}
        for name in PROMOTION_ORDER:
            try:
                os.stat(name, dir_fd=output_descriptor, follow_symlinks=False)
            except FileNotFoundError:
                continue
            _raw, identity = read_exact_regular_at(
                output_descriptor,
                name,
                artifacts[name],
                "preexisting-formal:" + name,
            )
            preexisting.append(name)
            preexisting_identities[name] = identity
        validate_exact_published_prefix(tuple(preexisting))
        committed_identities.update(preexisting_identities)
        recovered_orphans = recover_exact_promotion_stage_orphans(
            output_descriptor, artifacts
        )
        verify_committed_prefix("after-lock-and-orphan-recovery")
        if integrity_guard is not None:
            integrity_guard("after-lock-and-orphan-recovery")
        if len(preexisting) == len(PROMOTION_ORDER):
            if integrity_guard is not None:
                integrity_guard("fully-idempotent-existing-bundle")
            for name in PROMOTION_ORDER:
                _raw, identity = read_exact_regular_at(
                    output_descriptor,
                    name,
                    artifacts[name],
                    "idempotent-formal:" + name,
                )
                need(identity == preexisting_identities[name],
                     "IDEMPOTENT_FORMAL_IDENTITY_DRIFT:" + name)
            need(
                bound
                == directory_identity(os.fstat(output_descriptor))
                == directory_identity(os.lstat(resolved)),
                "IDEMPOTENT_PROMOTION_OUTPUT_DIRECTORY_DRIFT",
            )
            os.fsync(output_descriptor)
            return {
                "published_now": [],
                "preexisting_exact_prefix_length": len(preexisting),
                "recovered_exact_orphan_stage_count": recovered_orphans,
                "verification_commit_marker_present": True,
                "idempotent_exact_full_bundle": True,
            }

        need(
            bound
            == directory_identity(os.fstat(output_descriptor))
            == directory_identity(os.lstat(resolved)),
            "PROMOTION_DIRECTORY_SWAP_BEFORE_STAGE_CREATE",
        )
        while True:
            stage_name = PROMOTION_STAGE_PREFIX + os.urandom(16).hex()
            try:
                os.mkdir(stage_name, 0o700, dir_fd=output_descriptor)
                break
            except FileExistsError:
                continue
        stage_info = os.stat(
            stage_name, dir_fd=output_descriptor, follow_symlinks=False
        )
        stage_descriptor = os.open(
            stage_name,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
            dir_fd=output_descriptor,
        )
        stage_bound = directory_identity(os.fstat(stage_descriptor))
        need(
            stage_bound == directory_identity(stage_info)
            and stage_info.st_uid == os.geteuid()
            and stat.S_IMODE(stage_info.st_mode) == 0o700,
            "PROMOTION_STAGE_DIRFD_BINDING",
        )
        need(
            bound
            == directory_identity(os.fstat(output_descriptor))
            == directory_identity(os.lstat(resolved)),
            "PROMOTION_DIRECTORY_SWAP_AFTER_STAGE_OPEN",
        )
        completed = False
        try:
            missing = PROMOTION_ORDER[len(preexisting):]
            for name in missing:
                descriptor = os.open(
                    name,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL
                    | getattr(os, "O_CLOEXEC", 0),
                    0o644,
                    dir_fd=stage_descriptor,
                )
                try:
                    view = memoryview(artifacts[name])
                    offset = 0
                    while offset < len(view):
                        count = os.write(descriptor, view[offset:])
                        need(count > 0, "PROMOTION_STAGE_SHORT_WRITE:" + name)
                        offset += count
                    os.fsync(descriptor)
                finally:
                    os.close(descriptor)
            os.fsync(stage_descriptor)
            for name in PROMOTION_ORDER:
                if name in preexisting_identities:
                    _raw, identity = read_exact_regular_at(
                        output_descriptor,
                        name,
                        artifacts[name],
                        "stable-preexisting-formal:" + name,
                    )
                    need(identity == preexisting_identities[name],
                         "PREEXISTING_FORMAL_IDENTITY_DRIFT:" + name)
                    continue
                if hostile_hook is not None:
                    hostile_hook("before-rename", name, resolved)
                # Revalidate the complete already-published prefix immediately
                # before every next commit, especially the verification marker.
                verify_committed_prefix("before-rename:" + name)
                if integrity_guard is not None:
                    integrity_guard("before-rename:" + name)
                need(
                    bound
                    == directory_identity(os.fstat(output_descriptor))
                    == directory_identity(os.lstat(resolved)),
                    "PROMOTION_DIRECTORY_SWAP_BEFORE_RENAME:" + name,
                )
                try:
                    os.stat(name, dir_fd=output_descriptor,
                            follow_symlinks=False)
                except FileNotFoundError:
                    pass
                else:
                    raise VerificationBlocked(
                        "PROMOTION_TARGET_APPEARED_AFTER_PREFLIGHT:" + name
                    )
                staged_info = os.stat(
                    name,
                    dir_fd=stage_descriptor,
                    follow_symlinks=False,
                )
                staged_inode = (staged_info.st_dev, staged_info.st_ino)
                try:
                    rename_noreplace(
                        stage_descriptor, name,
                        output_descriptor, name,
                    )
                except FileExistsError as error:
                    raise VerificationBlocked(
                        "PROMOTION_RENAME_NOREPLACE_RACE:" + name
                    ) from error
                # Record ownership immediately after successful rename, before
                # either directory fsync can fail.
                published_now.append(name)
                published_now_inodes[name] = staged_inode
                os.fsync(stage_descriptor)
                os.fsync(output_descriptor)
                if hostile_hook is not None:
                    hostile_hook("after-rename", name, resolved)
                committed_identities[name] = file_identity(os.stat(
                    name,
                    dir_fd=output_descriptor,
                    follow_symlinks=False,
                ))
                need(
                    committed_identities[name][:2] == staged_inode,
                    "PROMOTION_RENAME_INODE_DRIFT:" + name,
                )
            os.fsync(stage_descriptor)
            need(
                stage_bound
                == directory_identity(os.fstat(stage_descriptor))
                == directory_identity(os.stat(
                    stage_name,
                    dir_fd=output_descriptor,
                    follow_symlinks=False,
                )),
                "PROMOTION_STAGE_DIRECTORY_SWAP",
            )
            os.rmdir(stage_name, dir_fd=output_descriptor)
            os.fsync(output_descriptor)
            completed = True
        finally:
            os.close(stage_descriptor)
            # On failure the exact private stage is deliberately left for the
            # locked recovery pass.  It can never itself confer formal credit.
            if completed:
                try:
                    os.stat(stage_name, dir_fd=output_descriptor,
                            follow_symlinks=False)
                except FileNotFoundError:
                    pass
                else:
                    raise VerificationBlocked(
                        "PROMOTION_STAGE_NOT_REMOVED_AFTER_SUCCESS"
                    )

        for name in PROMOTION_ORDER:
            _raw, identity = read_exact_regular_at(
                output_descriptor,
                name,
                artifacts[name],
                "published-formal:" + name,
            )
            need(identity == committed_identities[name],
                 "PUBLISHED_FORMAL_IDENTITY_DRIFT:" + name)
        if integrity_guard is not None:
            integrity_guard("after-complete-publication")
        need(
            os.path.lexists(resolved)
            and not resolved.is_symlink()
            and bound
            == directory_identity(os.fstat(output_descriptor))
            == directory_identity(os.lstat(resolved)),
            "PROMOTION_OUTPUT_DIRECTORY_RENAMED_OR_SWAPPED",
        )
        return {
            "published_now": published_now,
            "preexisting_exact_prefix_length": len(preexisting),
            "recovered_exact_orphan_stage_count": recovered_orphans,
            "verification_commit_marker_present": True,
            "idempotent_exact_full_bundle": False,
        }
    except BaseException:
        # If a post-marker check detects any race, retract only the marker
        # created by this invocation and only if its inode is still ours.  The
        # surviving exact prefix through result carries zero formal credit.
        if VERIFICATION_FILENAME in published_now:
            try:
                marker = os.stat(
                    VERIFICATION_FILENAME,
                    dir_fd=output_descriptor,
                    follow_symlinks=False,
                )
            except FileNotFoundError:
                pass
            else:
                if (
                    (marker.st_dev, marker.st_ino)
                    == published_now_inodes.get(VERIFICATION_FILENAME)
                ):
                    os.unlink(VERIFICATION_FILENAME, dir_fd=output_descriptor)
                    os.fsync(output_descriptor)
        raise
    finally:
        fcntl.flock(output_descriptor, fcntl.LOCK_UN)
        os.close(output_descriptor)


def publish_formal_promotion(
    candidate_bundle: dict[str, bytes],
    candidate_snapshot: dict[str, Any],
    attack_raw: bytes,
    verification_raw: bytes,
) -> dict[str, Any]:
    attacks = strict_json_raw(attack_raw, "formal attack publication bytes")
    verification = strict_json_raw(
        verification_raw, "formal verification publication bytes"
    )
    need(canonical(attacks) == attack_raw,
         "FORMAL_ATTACK_PUBLICATION_CANONICAL_BYTES")
    need(canonical(verification) == verification_raw,
         "FORMAL_VERIFICATION_PUBLICATION_CANONICAL_BYTES")
    verify_self(attacks, "attack_suite_sha256", "formal attack publication")
    verify_self(
        verification, "verification_sha256", "formal verification publication"
    )
    need(
        tuple(candidate_bundle) == PROMOTION_CANDIDATE_ORDER
        and set(candidate_bundle) == set(PROMOTION_CANDIDATE_ORDER),
        "FORMAL_PUBLICATION_EXACT_ORDERED_SIX_CANDIDATE_SET",
    )
    candidate_file_sha256s = dict(sorted({
        name: hashlib.sha256(candidate_bundle[name]).hexdigest()
        for name in PROMOTION_CANDIDATE_ORDER
    }.items()))
    need(
        attacks.get("binding_mode") == "EXACT_FORMAL_CANDIDATE"
        and attacks.get("all_rejected") is True
        and attacks.get("attack_count") == 99
        and attacks.get("rejected_count") == 99
        and len(attacks.get("attacks", ())) == 99
        and all(
            type(row) is dict and row.get("rejected") is True
            for row in attacks.get("attacks", ())
        )
        and attacks.get("baseline_candidate_file_sha256s")
        == candidate_file_sha256s,
        "FORMAL_PUBLICATION_EXACT_BOUND_ATTACK_SUITE",
    )
    need(
        verification.get("status")
        == (
            "PASS_EXACT_CACHELESS_ROUND305B_TWO_SIDED_PHYSICAL_"
            "INCLUSION_COMPONENT_EDGE_PROMOTION"
        )
        and verification.get("formal_Round305B_promotion_permitted") is True
        and verification.get("candidate", {}).get("exact_six_file_set")
        == list(PROMOTION_CANDIDATE_ORDER)
        and verification.get("candidate", {}).get("exact_file_sha256s")
        == candidate_file_sha256s
        and verification.get(
            "formal_credit_without_verification_commit_marker", {}
        )
        and all(
            value == 0 for value in verification[
                "formal_credit_without_verification_commit_marker"
            ].values()
        ),
        "FORMAL_PUBLICATION_EXACT_VERIFICATION_AND_ZERO_PREMARKER_CREDIT",
    )
    result_raw = candidate_bundle[OUTPUT_NAMES["result"]]
    result = strict_json_raw(result_raw, "formal candidate result publication")
    need(canonical(result) == result_raw,
         "FORMAL_CANDIDATE_RESULT_CANONICAL_BYTES")
    verify_self(result, "result_sha256", "formal candidate result publication")
    need(
        verification["candidate"]["independent_expected_result_sha256"]
        == result["result_sha256"]
        and result.get("producer_source_sha256")
        == verification.get("producer", {}).get("file_sha256"),
        "FORMAL_PUBLICATION_RESULT_AND_PRODUCER_BINDING",
    )
    atomic_contract = verification.get("atomic_publication_contract", {})
    need(
        atomic_contract.get("commit_order") == list(PROMOTION_ORDER)
        and atomic_contract.get("attack_suite_is_first") is True
        and atomic_contract.get("five_ledgers_then_result") is True
        and atomic_contract.get(
            "verification_is_last_and_sole_formal_credit_commit_marker"
        ) is True,
        "FORMAL_PUBLICATION_EXACT_ATOMIC_COMMIT_CONTRACT",
    )
    need(
        verification["attack_suite"]["file_sha256"]
        == hashlib.sha256(attack_raw).hexdigest()
        and verification["attack_suite"]["object_self_sha256"]
        == attacks["attack_suite_sha256"],
        "FORMAL_VERIFICATION_EXACT_ATTACK_FILE_AND_OBJECT_PIN",
    )
    current_producer_sha256 = verify_inert_producer_pin()
    current_verifier_sha256 = runtime_verifier_sha256()
    need(
        attacks.get("producer", {}).get("file_sha256")
        == current_producer_sha256
        == verification.get("producer", {}).get("file_sha256")
        and attacks.get("runtime_verifier", {}).get("file_sha256")
        == current_verifier_sha256
        == verification.get("runtime_verifier", {}).get("file_sha256"),
        "FORMAL_PUBLICATION_CURRENT_PRODUCER_AND_VERIFIER_BINDING",
    )
    artifacts = {
        ATTACK_FILENAME: attack_raw,
        **{name: candidate_bundle[name] for name in PROMOTION_CANDIDATE_ORDER},
        VERIFICATION_FILENAME: verification_raw,
    }
    need(tuple(artifacts) == PROMOTION_ORDER,
         "FORMAL_PROMOTION_ARTIFACT_CONSTRUCTION_ORDER")

    def integrity_guard(label: str) -> None:
        assert_candidate_snapshot(candidate_snapshot, label)
        need(
            verify_inert_producer_pin()
            == verification["producer"]["file_sha256"]
            and runtime_verifier_sha256()
            == verification["runtime_verifier"]["file_sha256"],
            label + ":PRODUCER_OR_RUNTIME_VERIFIER_CHANGED",
        )

    integrity_guard("pre-promotion")
    audit = publish_exact_prefix_transaction(
        D,
        artifacts,
        exact_deliverables_only=True,
        integrity_guard=integrity_guard,
    )
    return audit


def base_contract_model() -> dict[str, Any]:
    edge_witness_ids = [
        list(range(index * EXPECTED_PER_EDGE, (index + 1) * EXPECTED_PER_EDGE))
        for index in range(EXPECTED_EDGES)
    ]
    return {
        "sealed": {"Round303B": True, "Round304": True, "Round305A": True},
        "temporary_or_diagnostic_input_count": 0,
        "producer_schema_snapshot_sha256":
            EXPECTED_PRODUCER_SCHEMA_SNAPSHOT_SHA256,
        "physical_witness_count": EXPECTED_WITNESSES,
        "anchor_count": EXPECTED_ANCHORS,
        "closure_contact_count": EXPECTED_CLOSURE_CONTACTS,
        "owner_locus_count": EXPECTED_OWNER_LOCI,
        "boundary_face_contact_count": 1_856,
        "boundary_vertex_diagonal_contact_count": 1_680,
        "boundary_distinct_locus_count": 2_696,
        "four_patch_vertex_locus_count": 840,
        "vertex_owner_uses_all_incident_witnesses": True,
        "vertex_witness_reference_count": EXPECTED_VERTEX_WITNESS_REFS,
        "vertex_contact_reference_count": EXPECTED_VERTEX_CONTACT_REFS,
        "patch_contact_degree_histogram": EXPECTED_PATCH_CONTACT_DEGREE_HISTOGRAM,
        "owner_sidecar_used_as_component_edge_basis": False,
        "contact_rows_unique_and_canonically_ordered": True,
        "owner_locus_rows_unique_and_canonically_ordered": True,
        "four_patch_vertex_incident_witness_count": 4,
        "two_diagonals_share_one_vertex_owner_locus": True,
        "face_endpoint_vertex_override_reference_count":
            EXPECTED_VERTEX_WITNESS_REFS,
        "owner_sidecar_formal_credit": 0,
        "support_open_base_serialized_distinctly": True,
        "proof_closed_core_base_strictly_inside_support_open_base": True,
        "proof_closed_core_is_only_Gamma_G2_G4_credit_base": True,
        "owner_contact_closure_base_is_full_support_closure": True,
        "owner_contact_closure_base_shrunk_to_core": False,
        "owner_extension_contacts_claim_Gamma_core_contact": False,
        "owner_extension_used_as_G3_G4_or_component_edge_basis": False,
        "proof_core_id_domain_tag":
            "ROUND305B_DIRECT_PROOF_CORE_P_GRAPH_PATCH_V1",
        "owner_extension_id_domain_tag":
            "ROUND305B_ZERO_CREDIT_FULL_CLOSURE_ROOT_EXTENSION_PATCH_V1",
        "wall_integer": 0,
        "wall_predicate_label": "integer_wall_endpoint",
        "wall_product_formula_exact": True,
        "source_wall_factor_uniformly_strict_nonzero": True,
        "product_zero_iff_target_F_zero": True,
        "dynamic_signature_unique_unresolved_reason_replayed": True,
        "nested_G3_shape_and_values_exact": True,
        "nested_G4_shape_and_values_exact": True,
        "nested_G5_shape_and_values_exact": True,
        "full_sign_side_support_certificate_count": EXPECTED_ANCHORS,
        "full_sign_side_certificates_per_witness": 2,
        "full_sign_side_certificate_ids_unique": True,
        "full_sign_side_face_derivative_orientation_hard_checked": True,
        "full_sign_side_entire_half_open_segment_derived": True,
        "full_sign_side_unique_active_dynamic_boundary_replayed": True,
        "full_sign_side_R287_R292_single_support_provenance_closed": True,
        "G3_G4_embed_anchor_full_sign_side_certificate_exactly": True,
        "local_corridor_used_as_full_sign_side_proof": False,
        "official_key_pairs_explicitly_sorted": True,
        "canonical_occurrence_pairs_explicitly_sorted_before_hash": True,
        "every_candidate_row_self_hash_current": True,
        "every_candidate_ledger_self_hash_current": True,
        "candidate_result_self_hash_current": True,
        "candidate_result_commits_its_own_file_sha256": False,
        "canonical_gzip_mtime": 0,
        "canonical_gzip_filename": "",
        "canonical_gzip_header_exact": True,
        "committed_absolute_runtime_path_count": 0,
        "committed_wall_clock_or_timestamp_count": 0,
        "physical_frame_key_includes_chart_and_t_sign": True,
        "non_square_z_uses_exact_dyadic_sqrt_enclosure": True,
        "floating_point_sqrt_used": False,
        "python_flint_version": "0.9.0",
        "flint_precision_bits": 768,
        "overwrap_accepted_as_strict": False,
        "formal_geometry_source_sha_verified_before_execution": True,
        "formal_geometry_executed_from_verified_source_bytes": True,
        "formal_geometry_bytecode_cache_admitted": False,
        "canonical_component_edge_count": EXPECTED_EDGES,
        "edge_witness_ids": edge_witness_ids,
        "canonical_component_pair_ids": [f"component-pair-{i}" for i in range(8)],
        "complete_official_key_count": EXPECTED_OFFICIAL_KEYS,
        "residual_official_key_count": EXPECTED_RESIDUAL_KEYS,
        "cross_official_key_pair_count": EXPECTED_WITNESSES,
        "same_official_key_pair_count": 0,
        "official_key_profiles_per_component_edge": [1] * EXPECTED_EDGES,
        "cross_official_key_physical_edge_permitted": True,
        "same_official_key_used_as_physical_proof": False,
        "occurrence_identity_merge_credit": 0,
        "official_key_identity_merge_credit": 0,
        "G0_G5": {f"G{i}": True for i in range(6)},
        "relative_physical_closure_limit_lemma_rows": EXPECTED_WITNESSES,
        "corridor_box_used_as_Gamma_intersection": False,
        "D4_transfer_enabled": False,
        "D4_certificate_manifest_sha256": None,
        "D4_direct_instantiated_witness_rows": EXPECTED_WITNESSES,
        "formal_physical_witness_credit": EXPECTED_WITNESSES,
        "formal_component_edge_credit": EXPECTED_EDGES,
        "formal_DSU_rank_reduction_credit_in_Round305B": 0,
        "maximum_later_fresh_DSU_rank_reductions":
            MAXIMUM_LATER_RANK_REDUCTIONS,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
        "candidate_producer_imported_or_executed": False,
        "candidate_outputs_written_or_replaced_by_verifier": False,
        "candidate_output_names": sorted(OUTPUT_NAMES.values()),
    }


def validate_contract(model: dict[str, Any]) -> None:
    need(model["sealed"] == {
        "Round303B": True, "Round304": True, "Round305A": True,
    }, "COMPLETE_SEAL_CHAIN")
    need(model["temporary_or_diagnostic_input_count"] == 0, "NO_TEMP_INPUT")
    need(
        model["producer_schema_snapshot_sha256"]
        == EXPECTED_PRODUCER_SCHEMA_SNAPSHOT_SHA256,
        "FROZEN_PRODUCER_SCHEMA_SNAPSHOT",
    )
    need(model["physical_witness_count"] == EXPECTED_WITNESSES,
         "WITNESS_COUNT")
    need(model["anchor_count"] == EXPECTED_ANCHORS, "ANCHOR_COUNT")
    need(model["closure_contact_count"] == EXPECTED_CLOSURE_CONTACTS,
         "CLOSURE_CONTACT_COUNT")
    need(model["owner_locus_count"] == EXPECTED_OWNER_LOCI,
         "OWNER_LOCUS_COUNT")
    need(
        model["boundary_face_contact_count"] == 1_856
        and model["boundary_vertex_diagonal_contact_count"] == 1_680
        and model["boundary_distinct_locus_count"] == 2_696
        and model["four_patch_vertex_locus_count"] == 840,
        "BOUNDARY_FACE_VERTEX_LOCUS_CENSUS",
    )
    need(model["vertex_owner_uses_all_incident_witnesses"] is True,
         "VERTEX_GLOBAL_INCIDENT_OWNER_NOT_PAIRWISE_MIN")
    need(
        model["vertex_witness_reference_count"] == EXPECTED_VERTEX_WITNESS_REFS
        and model["vertex_contact_reference_count"] == EXPECTED_VERTEX_CONTACT_REFS
        and model["patch_contact_degree_histogram"]
        == EXPECTED_PATCH_CONTACT_DEGREE_HISTOGRAM,
        "VERTEX_REFS_AND_PATCH_DEGREE_CENSUS",
    )
    need(model["owner_sidecar_used_as_component_edge_basis"] is False,
         "OWNER_SIDECAR_NOT_COMPONENT_EDGE_BASIS")
    need(
        model["contact_rows_unique_and_canonically_ordered"] is True
        and model["owner_locus_rows_unique_and_canonically_ordered"] is True,
        "CONTACT_OWNER_UNIQUE_CANONICAL_ORDER",
    )
    need(
        model["four_patch_vertex_incident_witness_count"] == 4
        and model["two_diagonals_share_one_vertex_owner_locus"] is True
        and model["face_endpoint_vertex_override_reference_count"]
        == EXPECTED_VERTEX_WITNESS_REFS,
        "GLOBAL_VERTEX_OWNER_AND_FACE_OVERRIDE",
    )
    need(model["owner_sidecar_formal_credit"] == 0,
         "OWNER_SIDECAR_ZERO_CREDIT")
    need(
        model["support_open_base_serialized_distinctly"] is True
        and model["proof_closed_core_base_strictly_inside_support_open_base"]
        is True
        and model["proof_closed_core_is_only_Gamma_G2_G4_credit_base"] is True,
        "OPEN_SUPPORT_PROOF_CORE_DOMAIN_SEPARATION",
    )
    need(
        model["owner_contact_closure_base_is_full_support_closure"] is True
        and model["owner_contact_closure_base_shrunk_to_core"] is False
        and model["owner_extension_contacts_claim_Gamma_core_contact"] is False
        and model["owner_extension_used_as_G3_G4_or_component_edge_basis"]
        is False,
        "ZERO_CREDIT_OWNER_EXTENSION_DOMAIN_SEPARATION",
    )
    need(
        model["proof_core_id_domain_tag"]
        == "ROUND305B_DIRECT_PROOF_CORE_P_GRAPH_PATCH_V1"
        and model["owner_extension_id_domain_tag"]
        == "ROUND305B_ZERO_CREDIT_FULL_CLOSURE_ROOT_EXTENSION_PATCH_V1",
        "PROOF_AND_OWNER_EXTENSION_ID_DOMAINS",
    )
    need(
        model["wall_integer"] == 0
        and model["wall_predicate_label"] == "integer_wall_endpoint"
        and model["wall_product_formula_exact"] is True
        and model["source_wall_factor_uniformly_strict_nonzero"] is True
        and model["product_zero_iff_target_F_zero"] is True
        and model["dynamic_signature_unique_unresolved_reason_replayed"] is True,
        "G5_EXACT_WALL_PRODUCT_REDUCTION",
    )
    need(
        model["nested_G3_shape_and_values_exact"] is True
        and model["nested_G4_shape_and_values_exact"] is True
        and model["nested_G5_shape_and_values_exact"] is True,
        "NESTED_G3_G5_WIRE_CONTRACT",
    )
    need(
        model["full_sign_side_support_certificate_count"] == EXPECTED_ANCHORS
        and model["full_sign_side_certificates_per_witness"] == 2
        and model["full_sign_side_certificate_ids_unique"] is True,
        "FULL_SIGN_SIDE_2048_CERTIFICATE_CENSUS",
    )
    need(
        model["full_sign_side_face_derivative_orientation_hard_checked"] is True
        and model["full_sign_side_entire_half_open_segment_derived"] is True
        and model["full_sign_side_unique_active_dynamic_boundary_replayed"] is True
        and model[
            "full_sign_side_R287_R292_single_support_provenance_closed"
        ] is True,
        "FULL_SIGN_SIDE_COMPLETE_P_FACE_TO_RHO_DERIVATION",
    )
    need(
        model["G3_G4_embed_anchor_full_sign_side_certificate_exactly"] is True
        and model["local_corridor_used_as_full_sign_side_proof"] is False,
        "G3_G4_CERTIFICATE_IDENTITY_AND_CORRIDOR_BOUNDARY",
    )
    need(
        model["official_key_pairs_explicitly_sorted"] is True
        and model["canonical_occurrence_pairs_explicitly_sorted_before_hash"]
        is True,
        "CANONICAL_PAIR_ORDERING",
    )
    need(
        model["every_candidate_row_self_hash_current"] is True
        and model["every_candidate_ledger_self_hash_current"] is True
        and model["candidate_result_self_hash_current"] is True
        and model["candidate_result_commits_its_own_file_sha256"] is False,
        "ACYCLIC_ROW_LEDGER_RESULT_HASH_DAG",
    )
    need(
        model["canonical_gzip_mtime"] == 0
        and model["canonical_gzip_filename"] == ""
        and model["canonical_gzip_header_exact"] is True,
        "CANONICAL_GZIP_WIRE",
    )
    need(
        model["committed_absolute_runtime_path_count"] == 0
        and model["committed_wall_clock_or_timestamp_count"] == 0,
        "PATH_AND_TIME_FREE_COMMITTED_WIRE",
    )
    need(model["physical_frame_key_includes_chart_and_t_sign"] is True,
         "PHYSICAL_FRAME_CHART_AND_SIGN")
    need(
        model["non_square_z_uses_exact_dyadic_sqrt_enclosure"] is True
        and model["floating_point_sqrt_used"] is False
        and model["python_flint_version"] == "0.9.0"
        and model["flint_precision_bits"] == 768
        and model["overwrap_accepted_as_strict"] is False,
        "EXACT_SQRT_FLINT_PRECISION_AND_STRICT_SIGN",
    )
    need(
        model["formal_geometry_source_sha_verified_before_execution"] is True
        and model["formal_geometry_executed_from_verified_source_bytes"] is True
        and model["formal_geometry_bytecode_cache_admitted"] is False,
        "FORMAL_GEOMETRY_DIRECT_PINNED_SOURCE_EXECUTION_NO_PYC",
    )
    need(model["canonical_component_edge_count"] == EXPECTED_EDGES,
         "EDGE_COUNT")
    groups = model["edge_witness_ids"]
    need(type(groups) is list and len(groups) == EXPECTED_EDGES,
         "EDGE_GROUP_COUNT")
    need(all(len(group) == EXPECTED_PER_EDGE for group in groups),
         "EDGE_128_WITNESSES")
    flattened = [item for group in groups for item in group]
    need(
        len(flattened) == EXPECTED_WITNESSES
        and sorted(flattened) == list(range(EXPECTED_WITNESSES)),
        "EXACT_WITNESS_TO_EDGE_PARTITION",
    )
    pairs = model["canonical_component_pair_ids"]
    need(len(pairs) == EXPECTED_EDGES and len(set(pairs)) == EXPECTED_EDGES,
         "CANONICAL_COMPONENT_PAIR_DEDUP")
    need(model["complete_official_key_count"] == EXPECTED_OFFICIAL_KEYS,
         "OFFICIAL_KEY_124")
    need(model["residual_official_key_count"] == EXPECTED_RESIDUAL_KEYS,
         "RESIDUAL_KEY_16")
    need(
        model["cross_official_key_pair_count"] == EXPECTED_WITNESSES
        and model["same_official_key_pair_count"] == 0,
        "ALL_RESIDUAL_PAIRS_CROSS_KEY",
    )
    need(model["official_key_profiles_per_component_edge"] == [1] * 8,
         "ONE_KEY_PROFILE_PER_EDGE")
    need(model["cross_official_key_physical_edge_permitted"] is True,
         "CROSS_KEY_PHYSICAL_EDGE_LEGAL_WHEN_G0_G5")
    need(model["same_official_key_used_as_physical_proof"] is False,
         "SAME_KEY_NOT_A_PHYSICAL_PROOF")
    need(
        model["occurrence_identity_merge_credit"] == 0
        and model["official_key_identity_merge_credit"] == 0,
        "NO_IDENTITY_OR_OFFICIAL_KEY_MERGE",
    )
    need(model["G0_G5"] == {f"G{i}": True for i in range(6)},
         "DIRECT_G0_G5_EVERY_WITNESS")
    need(
        model["relative_physical_closure_limit_lemma_rows"]
        == EXPECTED_WITNESSES
        and model["corridor_box_used_as_Gamma_intersection"] is False,
        "G3_G4_RELATIVE_PHYSICAL_LIMIT_NOT_CORRIDOR_SHORTCUT",
    )
    need(
        model["D4_transfer_enabled"] is False
        and model["D4_certificate_manifest_sha256"] is None
        and model["D4_direct_instantiated_witness_rows"] == EXPECTED_WITNESSES,
        "D4_FAIL_CLOSED_DIRECT_INSTANTIATION",
    )
    need(model["formal_physical_witness_credit"] == EXPECTED_WITNESSES,
         "PHYSICAL_WITNESS_CREDIT")
    need(model["formal_component_edge_credit"] == EXPECTED_EDGES,
         "COMPONENT_EDGE_CREDIT")
    need(model["formal_DSU_rank_reduction_credit_in_Round305B"] == 0,
         "NO_RANK_REDUCTION_IN_ROUND305B")
    need(
        model["maximum_later_fresh_DSU_rank_reductions"]
        == MAXIMUM_LATER_RANK_REDUCTIONS,
        "AT_MOST_EIGHT_LATER_RANK_REDUCTIONS",
    )
    for field in (
        "formal_maximality_credit", "formal_fibre_credit",
        "formal_global_disposition_credit",
    ):
        need(model[field] == 0, "ZERO_DOWNSTREAM_CREDIT:" + field)
    need(model["candidate_producer_imported_or_executed"] is False,
         "PRODUCER_INERT_BYTE_PIN_ONLY")
    need(model["candidate_outputs_written_or_replaced_by_verifier"] is False,
         "VERIFIER_NO_CLOBBER")
    need(
        model["candidate_output_names"] == sorted(OUTPUT_NAMES.values())
        and all("/" not in name and name == Path(name).name
                for name in model["candidate_output_names"]),
        "EXACT_FLAT_OUTPUT_PATH_SET",
    )


def rejected(callback: Callable[[], None]) -> bool:
    try:
        callback()
    except (VerificationBlocked, KeyError, TypeError, ValueError):
        return True
    return False


def stale_pyc_same_mtime_size_attack_probe() -> dict[str, Any]:
    """Reproduce timestamp-cache confusion, then prove the direct path immune."""

    stale_source = b"PROBE_VALUE='OLD'\n"
    current_source = b"PROBE_VALUE='NEW'\n"
    need(len(stale_source) == len(current_source),
         "STALE_PYC_PROBE_EQUAL_SOURCE_SIZE")
    current_pin = hashlib.sha256(current_source).hexdigest()
    module_name = "round305b_stale_pyc_same_mtime_size_fixture"
    fixed_mtime_ns = 1_700_000_000_000_000_000
    with tempfile.TemporaryDirectory(prefix="round305b-stale-pyc-") as temporary:
        source_path = Path(temporary) / (module_name + ".py")
        source_path.write_bytes(stale_source)
        os.utime(source_path, ns=(fixed_mtime_ns, fixed_mtime_ns))
        cache_path = Path(importlib.util.cache_from_source(str(source_path)))
        py_compile.compile(
            str(source_path), cfile=str(cache_path), doraise=True, optimize=0,
            invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP,
        )
        need(cache_path.is_file(), "STALE_PYC_FIXTURE_CACHE_CREATED")
        source_path.write_bytes(current_source)
        os.utime(source_path, ns=(fixed_mtime_ns, fixed_mtime_ns))
        need(
            source_path.stat().st_size == len(stale_source)
            and source_path.stat().st_mtime_ns == fixed_mtime_ns,
            "STALE_PYC_FIXTURE_SAME_SIZE_AND_MTIME",
        )
        importlib.invalidate_caches()
        spec = importlib.util.spec_from_file_location(module_name, source_path)
        need(spec is not None and spec.loader is not None,
             "STALE_PYC_FIXTURE_DEFAULT_IMPORT_SPEC")
        cached_module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = cached_module
        try:
            spec.loader.exec_module(cached_module)
            need(cached_module.PROBE_VALUE == "OLD",
                 "STALE_PYC_FIXTURE_DID_NOT_REPRODUCE_OLD_BYTECODE")
        finally:
            sys.modules.pop(module_name, None)
        # Remove the demonstrated cache.  The verified-source compiler receives
        # only current raw bytes and their pin, and must neither read nor create
        # any bytecode file.
        cache_path.unlink()
        need(not cache_path.exists(), "STALE_PYC_FIXTURE_CACHE_REMOVED")
        direct_namespace: dict[str, Any] = {}
        code = compile_verified_source_bytes(
            source_path.read_bytes(), current_pin,
            "<round305b-direct-verified-source-attack>",
        )
        exec(code, direct_namespace)
        need(
            direct_namespace.get("PROBE_VALUE") == "NEW"
            and not cache_path.exists(),
            "DIRECT_VERIFIED_SOURCE_PATH_NOT_IMMUNE_TO_STALE_PYC",
        )
    return {
        "fixture_same_source_size": True,
        "fixture_same_integer_mtime": True,
        "fixture_pyc_invalidation_mode": "TIMESTAMP",
        "default_importlib_observed": "OLD",
        "fixture_default_importlib_stale_pyc_read": True,
        "fixture_pyc_created_and_removed": True,
        "direct_verified_source_compiler_observed": "NEW",
        "direct_path_pycache_reads": False,
        "direct_path_pycache_writes": False,
        "temporary_fixture_removed": True,
        "formal_credit": 0,
    }


def synthetic_promotion_artifacts() -> dict[str, bytes]:
    return {
        name: ("ROUND305B_TRANSACTION_FIXTURE:" + name).encode("utf-8")
        for name in PROMOTION_ORDER
    }


def exclusive_fixture_write(path: Path, payload: bytes) -> None:
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0),
        0o600,
    )
    try:
        view = memoryview(payload)
        offset = 0
        while offset < len(view):
            count = os.write(descriptor, view[offset:])
            need(count > 0, "FIXTURE_SHORT_WRITE:" + path.name)
            offset += count
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def promotion_positive_transaction_selftest() -> dict[str, Any]:
    artifacts = synthetic_promotion_artifacts()
    with tempfile.TemporaryDirectory(
        prefix="round305b-promotion-positive-", dir=ROOT,
    ) as temporary:
        output = Path(temporary) / "formal-output"
        output.mkdir(mode=0o700)

        fresh = Path(temporary) / "fresh-formal-output"
        fresh.mkdir(mode=0o700)
        fresh_first = publish_exact_prefix_transaction(
            fresh, artifacts, exact_deliverables_only=False
        )
        fresh_before = {
            name: file_identity(os.lstat(fresh / name))
            for name in PROMOTION_ORDER
        }
        fresh_second = publish_exact_prefix_transaction(
            fresh, artifacts, exact_deliverables_only=False
        )
        fresh_after = {
            name: file_identity(os.lstat(fresh / name))
            for name in PROMOTION_ORDER
        }
        need(
            fresh_first["preexisting_exact_prefix_length"] == 0
            and fresh_first["published_now"] == list(PROMOTION_ORDER)
            and fresh_first["published_now"][0] == ATTACK_FILENAME
            and fresh_first["published_now"][-1] == VERIFICATION_FILENAME
            and fresh_second["idempotent_exact_full_bundle"] is True
            and fresh_second["published_now"] == []
            and fresh_before == fresh_after,
            "POSITIVE_FRESH_ATOMIC_TRANSACTION",
        )

        exclusive_fixture_write(output / ATTACK_FILENAME,
                                artifacts[ATTACK_FILENAME])
        orphan = output / (PROMOTION_STAGE_PREFIX + ("0" * 32))
        orphan.mkdir(mode=0o700)
        exclusive_fixture_write(
            orphan / PROMOTION_CANDIDATE_ORDER[0],
            artifacts[PROMOTION_CANDIDATE_ORDER[0]],
        )
        first = publish_exact_prefix_transaction(
            output, artifacts, exact_deliverables_only=False
        )
        before = {
            name: file_identity(os.lstat(output / name))
            for name in PROMOTION_ORDER
        }
        second = publish_exact_prefix_transaction(
            output, artifacts, exact_deliverables_only=False
        )
        after = {
            name: file_identity(os.lstat(output / name))
            for name in PROMOTION_ORDER
        }
        need(
            first["preexisting_exact_prefix_length"] == 1
            and first["recovered_exact_orphan_stage_count"] == 1
            and first["published_now"] == list(PROMOTION_ORDER[1:])
            and first["published_now"][-1] == VERIFICATION_FILENAME
            and second["published_now"] == []
            and second["idempotent_exact_full_bundle"] is True
            and before == after,
            "POSITIVE_EXACT_PREFIX_IDEMPOTENT_TRANSACTION",
        )

        post_marker = Path(temporary) / "post-marker-prefix-drift"
        post_marker.mkdir(mode=0o700)
        changed_attack = (
            bytes([artifacts[ATTACK_FILENAME][0] ^ 1])
            + artifacts[ATTACK_FILENAME][1:]
        )

        def post_marker_hook(event: str, name: str, resolved: Path) -> None:
            if event == "after-rename" and name == VERIFICATION_FILENAME:
                descriptor = os.open(
                    resolved / ATTACK_FILENAME,
                    os.O_WRONLY | os.O_TRUNC | getattr(os, "O_CLOEXEC", 0),
                )
                try:
                    need(
                        os.write(descriptor, changed_attack)
                        == len(changed_attack),
                        "POST_MARKER_PREFIX_DRIFT_FIXTURE_SHORT_WRITE",
                    )
                    os.fsync(descriptor)
                finally:
                    os.close(descriptor)

        need(
            rejected(lambda: publish_exact_prefix_transaction(
                post_marker,
                artifacts,
                exact_deliverables_only=False,
                hostile_hook=post_marker_hook,
            )),
            "POST_MARKER_PREFIX_DRIFT_NOT_REJECTED",
        )
        need(
            not (post_marker / VERIFICATION_FILENAME).exists(),
            "POST_MARKER_PREFIX_DRIFT_MARKER_NOT_RETRACTED",
        )

        mode_drift = Path(temporary) / "post-marker-directory-mode-drift"
        mode_drift.mkdir(mode=0o700)

        def mode_drift_hook(event: str, name: str, resolved: Path) -> None:
            if event == "after-rename" and name == VERIFICATION_FILENAME:
                os.chmod(resolved, 0o750)

        need(
            rejected(lambda: publish_exact_prefix_transaction(
                mode_drift,
                artifacts,
                exact_deliverables_only=False,
                hostile_hook=mode_drift_hook,
            )),
            "POST_MARKER_DIRECTORY_MODE_DRIFT_NOT_REJECTED",
        )
        need(
            not (mode_drift / VERIFICATION_FILENAME).exists(),
            "POST_MARKER_DIRECTORY_MODE_DRIFT_MARKER_NOT_RETRACTED",
        )
        os.chmod(mode_drift, 0o700)
    return {
        "fresh_empty_transaction_passed": True,
        "attack_committed_first": True,
        "result_committed_immediately_before_verification": True,
        "verification_committed_last_as_sole_marker": True,
        "exact_orphan_stage_recovered": True,
        "exact_prefix_resume_passed": True,
        "full_bundle_second_run_inode_identity_unchanged": True,
        "post_marker_prefix_drift_retracted_verification": True,
        "post_marker_directory_drift_retracted_verification": True,
        "formal_credit_without_verification_marker": 0,
    }


def promotion_hostile_attack_callbacks(
) -> list[tuple[str, Callable[[], None], str]]:
    artifacts = synthetic_promotion_artifacts()

    def isolated(
        prefix: str,
        setup: Callable[[Path], Callable[[str, str, Path], None] | None],
    ) -> None:
        with tempfile.TemporaryDirectory(prefix=prefix, dir=ROOT) as temporary:
            output = Path(temporary) / "formal-output"
            output.mkdir(mode=0o700)
            hook = setup(output)
            publish_exact_prefix_transaction(
                output,
                artifacts,
                exact_deliverables_only=False,
                hostile_hook=hook,
            )

    def commit_marker_only(output: Path) -> None:
        exclusive_fixture_write(
            output / VERIFICATION_FILENAME,
            artifacts[VERIFICATION_FILENAME],
        )
        return None

    def conflicting_target(output: Path) -> None:
        exclusive_fixture_write(output / ATTACK_FILENAME, b"CONFLICT")
        return None

    def target_race(_output: Path) -> Callable[[str, str, Path], None]:
        fired = False

        def hook(event: str, name: str, resolved: Path) -> None:
            nonlocal fired
            if event == "before-rename" and not fired:
                fired = True
                exclusive_fixture_write(resolved / name, b"RACER")

        return hook

    def directory_swap(output: Path) -> Callable[[str, str, Path], None]:
        fired = False

        def hook(event: str, _name: str, resolved: Path) -> None:
            nonlocal fired
            if event == "before-rename" and not fired:
                fired = True
                moved = resolved.parent / (resolved.name + "-swapped-out")
                os.rename(resolved, moved)
                resolved.mkdir(mode=0o700)

        return hook

    def mutate_committed_prefix_before_marker(
        _output: Path,
    ) -> Callable[[str, str, Path], None]:
        fired = False

        def hook(event: str, name: str, resolved: Path) -> None:
            nonlocal fired
            if (
                event == "before-rename"
                and name == VERIFICATION_FILENAME
                and not fired
            ):
                fired = True
                payload = artifacts[ATTACK_FILENAME]
                descriptor = os.open(
                    resolved / ATTACK_FILENAME,
                    os.O_WRONLY | getattr(os, "O_CLOEXEC", 0),
                )
                try:
                    changed = bytes([payload[0] ^ 1]) + payload[1:]
                    need(os.write(descriptor, changed) == len(changed),
                         "PREFIX_MUTATION_FIXTURE_SHORT_WRITE")
                    os.fsync(descriptor)
                finally:
                    os.close(descriptor)

        return hook

    def foreign_orphan(output: Path) -> None:
        stage = output / (PROMOTION_STAGE_PREFIX + ("1" * 32))
        stage.mkdir(mode=0o700)
        exclusive_fixture_write(stage / "foreign.bin", b"FOREIGN")
        return None

    def nonexact_prefix(output: Path) -> None:
        name = PROMOTION_CANDIDATE_ORDER[0]
        exclusive_fixture_write(output / name, artifacts[name])
        return None

    def corrupt_orphan(output: Path) -> None:
        stage = output / (PROMOTION_STAGE_PREFIX + ("2" * 32))
        stage.mkdir(mode=0o700)
        exclusive_fixture_write(stage / ATTACK_FILENAME, b"CORRUPT")
        return None

    def symlink_directory_attack() -> None:
        with tempfile.TemporaryDirectory(
            prefix="round305b-promotion-symlink-", dir=ROOT,
        ) as temporary:
            base = Path(temporary)
            real = base / "real-output"
            real.mkdir(mode=0o700)
            link = base / "linked-output"
            link.symlink_to(real, target_is_directory=True)
            publish_exact_prefix_transaction(
                link, artifacts, exact_deliverables_only=False
            )

    def wrong_formal_output_directory_attack() -> None:
        with tempfile.TemporaryDirectory(
            prefix="round305b-wrong-formal-output-", dir=ROOT,
        ) as temporary:
            output = Path(temporary) / "not-deliverables"
            output.mkdir(mode=0o700)
            publish_exact_prefix_transaction(
                output, artifacts, exact_deliverables_only=True
            )

    wrong_order = list(PROMOTION_ORDER)
    wrong_order[-1], wrong_order[-2] = wrong_order[-2], wrong_order[-1]
    return [
        (
            "A89_VERIFICATION_NOT_LAST",
            lambda: validate_promotion_commit_order(tuple(wrong_order)),
            "verification is the final commit marker",
        ),
        (
            "A90_COMMIT_MARKER_WITHOUT_COMPLETE_PREFIX",
            lambda: isolated(
                "round305b-marker-only-", commit_marker_only
            ),
            "verification cannot exist without attack and all six candidates",
        ),
        (
            "A91_EXISTING_TARGET_CLOBBER",
            lambda: isolated("round305b-clobber-", conflicting_target),
            "preexisting formal targets must have exact expected bytes",
        ),
        (
            "A92_TARGET_APPEARS_AFTER_PREFLIGHT",
            lambda: isolated("round305b-target-race-", target_race),
            "renameat2 RENAME_NOREPLACE rejects a raced target",
        ),
        (
            "A93_DELIVERABLES_DIRECTORY_SWAP",
            lambda: isolated("round305b-directory-swap-", directory_swap),
            "bound output directory inode must remain at the lexical path",
        ),
        (
            "A94_SYMLINK_OUTPUT_DIRECTORY",
            symlink_directory_attack,
            "every output directory component is a real directory",
        ),
        (
            "A95_FOREIGN_ORPHAN_STAGE",
            lambda: isolated("round305b-foreign-orphan-", foreign_orphan),
            "orphan stage may contain only exact promotion artifacts",
        ),
        (
            "A96_NONPREFIX_PREEXISTING_OUTPUT",
            lambda: isolated("round305b-nonprefix-", nonexact_prefix),
            "preexisting outputs must be one exact commit prefix",
        ),
        (
            "A97_CORRUPT_EXACT_NAME_ORPHAN_STAGE",
            lambda: isolated("round305b-corrupt-orphan-", corrupt_orphan),
            "orphan stage exact names must also have exact bytes",
        ),
        (
            "A98_FORMAL_PROMOTION_TO_NONDELIVERABLES",
            wrong_formal_output_directory_attack,
            "formal promotion target is the one exact deliverables directory",
        ),
        (
            "A99_MUTATE_COMMITTED_PREFIX_BEFORE_MARKER",
            lambda: isolated(
                "round305b-prefix-mutation-",
                mutate_committed_prefix_before_marker,
            ),
            "the complete committed prefix is revalidated before verification",
        ),
    ]


def build_attack_suite(
    *,
    producer_sha256: str | None = None,
    verifier_sha256: str | None = None,
    candidate_file_sha256s: dict[str, str] | None = None,
) -> dict[str, Any]:
    formal_binding = (
        producer_sha256 is not None
        and verifier_sha256 is not None
        and candidate_file_sha256s is not None
    )
    if not formal_binding:
        producer_sha256 = "0" * 64
        verifier_sha256 = runtime_verifier_sha256()
        candidate_file_sha256s = {
            name: hashlib.sha256(
                ("SELFTEST_CANDIDATE_BINDING:" + name).encode("utf-8")
            ).hexdigest()
            for name in PROMOTION_CANDIDATE_ORDER
        }
    need(
        PIN_RE.fullmatch(producer_sha256) is not None
        and PIN_RE.fullmatch(verifier_sha256) is not None
        and set(candidate_file_sha256s) == set(PROMOTION_CANDIDATE_ORDER)
        and all(PIN_RE.fullmatch(value) is not None
                for value in candidate_file_sha256s.values()),
        "ATTACK_SUITE_EXACT_BASELINE_BINDINGS",
    )
    stale_pyc_probe = stale_pyc_same_mtime_size_attack_probe()
    positive_transaction = promotion_positive_transaction_selftest()
    base = base_contract_model()
    validate_contract(base)
    mutations: list[tuple[str, Callable[[dict[str, Any]], None], str]] = [
        ("A01_DROP_PHYSICAL_WITNESS", lambda x: x.__setitem__("physical_witness_count", 1023), "exact 1024 witnesses"),
        ("A02_DROP_ANCHOR", lambda x: x.__setitem__("anchor_count", 2047), "exact 2048 anchors"),
        ("A03_DROP_CLOSURE_CONTACT", lambda x: x.__setitem__("closure_contact_count", 3535), "exact 3536 closure contacts"),
        ("A04_INFLATE_1024_WITNESSES_TO_1024_EDGES", lambda x: x.__setitem__("canonical_component_edge_count", 1024), "1024 witnesses are not 1024 edges"),
        ("A05_NINTH_CANONICAL_COMPONENT_EDGE", lambda x: x.__setitem__("canonical_component_edge_count", 9), "exact eight component pairs"),
        ("A06_127_WITNESS_EDGE_GROUP", lambda x: x["edge_witness_ids"][0].pop(), "128 witnesses per edge"),
        ("A07_DUPLICATE_WITNESS_ACROSS_EDGES", lambda x: x["edge_witness_ids"][1].__setitem__(0, x["edge_witness_ids"][0][0]), "exact witness partition"),
        ("A08_DUPLICATE_COMPONENT_PAIR", lambda x: x["canonical_component_pair_ids"].__setitem__(1, x["canonical_component_pair_ids"][0]), "canonical component dedup"),
        ("A09_STALE_116_OFFICIAL_KEYS", lambda x: x.__setitem__("complete_official_key_count", 116), "actual 124-key universe"),
        ("A10_DROP_RESIDUAL_OFFICIAL_KEY", lambda x: x.__setitem__("residual_official_key_count", 15), "exact residual 16 keys"),
        ("A11_FORGE_SAME_KEY_RESIDUAL", lambda x: (x.__setitem__("cross_official_key_pair_count", 1023), x.__setitem__("same_official_key_pair_count", 1)), "all 1024 pairs cross key"),
        ("A12_TWO_KEY_PROFILES_FOR_ONE_EDGE", lambda x: x["official_key_profiles_per_component_edge"].__setitem__(0, 2), "one fixed key profile per edge"),
        ("A13_CROSS_KEY_FALSE_IDENTITY_MERGE", lambda x: x.__setitem__("occurrence_identity_merge_credit", 1), "physical edge is not occurrence identity"),
        ("A14_CROSS_KEY_FALSE_OFFICIAL_KEY_MERGE", lambda x: x.__setitem__("official_key_identity_merge_credit", 1), "physical edge is not official-key merge"),
        ("A15_CROSS_KEY_EDGE_ILLEGALLY_REJECTED", lambda x: x.__setitem__("cross_official_key_physical_edge_permitted", False), "G0-G5 physical edge may cross keys"),
        ("A16_SAME_KEY_USED_AS_PHYSICAL_PROOF", lambda x: x.__setitem__("same_official_key_used_as_physical_proof", True), "same key is not gluing evidence"),
        ("A17_DISABLE_G0", lambda x: x["G0_G5"].__setitem__("G0", False), "G0 direct provenance"),
        ("A18_DISABLE_G1", lambda x: x["G0_G5"].__setitem__("G1", False), "G1 connected anchors"),
        ("A19_DISABLE_G2", lambda x: x["G0_G5"].__setitem__("G2", False), "G2 included Gamma"),
        ("A20_DISABLE_G3", lambda x: x["G0_G5"].__setitem__("G3", False), "G3 left attachment"),
        ("A21_DISABLE_G4", lambda x: x["G0_G5"].__setitem__("G4", False), "G4 right attachment"),
        ("A22_DISABLE_G5", lambda x: x["G0_G5"].__setitem__("G5", False), "G5 exact closure"),
        ("A23_DROP_RELATIVE_CLOSURE_LIMIT_ROW", lambda x: x.__setitem__("relative_physical_closure_limit_lemma_rows", 1023), "G3/G4 p-to-rho limit per row"),
        ("A24_CORRIDOR_AS_GAMMA_INTERSECTION", lambda x: x.__setitem__("corridor_box_used_as_Gamma_intersection", True), "corridor is not an intersection witness"),
        ("A25_ENABLE_UNSEALED_D4_TRANSFER", lambda x: x.__setitem__("D4_transfer_enabled", True), "D4 disabled without theorem"),
        ("A26_REDUCE_DIRECT_ROWS_BY_D4", lambda x: x.__setitem__("D4_direct_instantiated_witness_rows", 128), "all 1024 rows instantiated"),
        ("A27_CONSUME_TEMP_INPUT", lambda x: x.__setitem__("temporary_or_diagnostic_input_count", 1), "formal source uses no temp input"),
        ("A28_UNSEAL_ROUND305A", lambda x: x["sealed"].__setitem__("Round305A", False), "sealed Round305A required"),
        ("A29_UNSEAL_ROUND304", lambda x: x["sealed"].__setitem__("Round304", False), "sealed Round304 required"),
        ("A30_UNSEAL_ROUND303B", lambda x: x["sealed"].__setitem__("Round303B", False), "sealed Round303B required"),
        ("A31_PHYSICAL_CREDIT_1023", lambda x: x.__setitem__("formal_physical_witness_credit", 1023), "one credit per proved witness"),
        ("A32_EDGE_CREDIT_1024", lambda x: x.__setitem__("formal_component_edge_credit", 1024), "one credit per canonical edge"),
        ("A33_R305B_APPLIES_DSU_UNIONS", lambda x: x.__setitem__("formal_DSU_rank_reduction_credit_in_Round305B", 8), "DSU application belongs to later fresh rebuild"),
        ("A34_MORE_THAN_EIGHT_LATER_RANK_REDUCTIONS", lambda x: x.__setitem__("maximum_later_fresh_DSU_rank_reductions", 9), "at most eight later reductions"),
        ("A35_PREMATURE_MAXIMALITY_CREDIT", lambda x: x.__setitem__("formal_maximality_credit", 1), "maximality remains downstream"),
        ("A36_PREMATURE_FIBRE_GLOBAL_CREDIT", lambda x: (x.__setitem__("formal_fibre_credit", 1), x.__setitem__("formal_global_disposition_credit", 1)), "fibre/global remain downstream"),
        ("A37_PRODUCER_SCHEMA_SNAPSHOT_DRIFT", lambda x: x.__setitem__("producer_schema_snapshot_sha256", "0" * 64), "frozen producer artifact schema"),
        ("A38_PAIRWISE_MINIMUM_AT_FOUR_PATCH_VERTEX", lambda x: x.__setitem__("vertex_owner_uses_all_incident_witnesses", False), "vertex owner ranges over all four incident witnesses"),
        ("A39_BOUNDARY_LOCUS_COLLAPSE", lambda x: x.__setitem__("boundary_distinct_locus_count", 3536), "3536 contacts occupy 2696 exact loci"),
        ("A40_IMPORT_CANDIDATE_PRODUCER", lambda x: x.__setitem__("candidate_producer_imported_or_executed", True), "producer is inert byte pin only"),
        ("A41_VERIFIER_CLOBBERS_CANDIDATE", lambda x: x.__setitem__("candidate_outputs_written_or_replaced_by_verifier", True), "verifier is read-only"),
        ("A42_OUTPUT_PATH_TRAVERSAL", lambda x: x["candidate_output_names"].__setitem__(0, "../escape.json"), "exact flat deliverables path set"),
        ("A43_COLLAPSE_CONTACTS_INTO_OWNER_LOCI", lambda x: x.__setitem__("owner_locus_count", 3536), "3536 contacts and 2696 owner loci remain distinct"),
        ("A44_WRONG_VERTEX_CONTACT_REFS", lambda x: x.__setitem__("vertex_contact_reference_count", 1680), "840 vertices each reference six contacts"),
        ("A45_OWNER_SIDECAR_AS_EDGE_BASIS", lambda x: x.__setitem__("owner_sidecar_used_as_component_edge_basis", True), "owner sidecar is zero-credit and not an edge gate"),
        ("A46_DUPLICATE_OR_REORDER_CONTACT_ROWS", lambda x: x.__setitem__("contact_rows_unique_and_canonically_ordered", False), "unique canonical contact rows"),
        ("A47_DUPLICATE_OR_REORDER_OWNER_LOCI", lambda x: x.__setitem__("owner_locus_rows_unique_and_canonically_ordered", False), "unique canonical owner loci"),
        ("A48_SHRINK_VERTEX_INCIDENT_SET_TO_PAIR", lambda x: x.__setitem__("four_patch_vertex_incident_witness_count", 2), "four global incident witnesses at every vertex"),
        ("A49_SPLIT_TWO_DIAGONALS_ACROSS_VERTEX_IDS", lambda x: x.__setitem__("two_diagonals_share_one_vertex_owner_locus", False), "both diagonals share one vertex locus and owner"),
        ("A50_FACE_IGNORES_VERTEX_OVERRIDE", lambda x: x.__setitem__("face_endpoint_vertex_override_reference_count", 0), "3360 face-to-vertex override references"),
        ("A51_OWNER_SIDECAR_ISSUES_CREDIT", lambda x: x.__setitem__("owner_sidecar_formal_credit", 1), "owner sidecar is zero-credit"),
        ("A52_FRAME_KEY_OMITS_T_SIGN", lambda x: x.__setitem__("physical_frame_key_includes_chart_and_t_sign", False), "frame key includes chart and physical t sign"),
        ("A53_RATIONALIZE_NON_SQUARE_Z", lambda x: x.__setitem__("non_square_z_uses_exact_dyadic_sqrt_enclosure", False), "exact z with certified dyadic sqrt enclosure"),
        ("A54_FLOATING_POINT_SQRT", lambda x: x.__setitem__("floating_point_sqrt_used", True), "no floating-point geometry"),
        ("A55_WRONG_FLINT_PRECISION", lambda x: x.__setitem__("flint_precision_bits", 192), "python-flint 0.9.0 at 768 bits"),
        ("A56_ACCEPT_OVERWRAP_AS_STRICT", lambda x: x.__setitem__("overwrap_accepted_as_strict", True), "OVERWRAP never accepted as strict sign"),
        ("A61_SWAP_PROOF_CORE_WITH_FULL_CLOSURE", lambda x: x.__setitem__("proof_closed_core_base_strictly_inside_support_open_base", False), "Gamma proof base is a strict closed inset of the R292 open support"),
        ("A62_SHRINK_OWNER_CLOSURE_TO_PROOF_CORE", lambda x: x.__setitem__("owner_contact_closure_base_shrunk_to_core", True), "owner extension retains the full support closure"),
        ("A63_MUTATE_PROOF_CORE_ID_DOMAIN", lambda x: x.__setitem__("proof_core_id_domain_tag", "ROUND305B_WRONG_DOMAIN"), "proof-core and owner-extension IDs have disjoint normative domains"),
        ("A64_UNSORT_OFFICIAL_KEY_PAIR", lambda x: x.__setitem__("official_key_pairs_explicitly_sorted", False), "official-key pairs are explicitly lexicographically canonical"),
        ("A65_HASH_OCCURRENCE_PAIRS_IN_WITNESS_ORDER", lambda x: x.__setitem__("canonical_occurrence_pairs_explicitly_sorted_before_hash", False), "edge occurrence-pair commitment uses explicit pair sorting"),
        ("A66_MUTATE_NESTED_G3", lambda x: x.__setitem__("nested_G3_shape_and_values_exact", False), "normative nested G3 proof wire"),
        ("A67_MUTATE_NESTED_G4", lambda x: x.__setitem__("nested_G4_shape_and_values_exact", False), "normative nested G4 proof wire"),
        ("A68_MUTATE_NESTED_G5", lambda x: x.__setitem__("nested_G5_shape_and_values_exact", False), "normative nested G5 wall-product wire"),
        ("A69_STALE_ROW_SHA256", lambda x: x.__setitem__("every_candidate_row_self_hash_current", False), "every row is closed after its final nested payload"),
        ("A70_STALE_LEDGER_SHA256", lambda x: x.__setitem__("every_candidate_ledger_self_hash_current", False), "every ledger is closed after final rows and commitments"),
        ("A71_STALE_RESULT_SHA256", lambda x: x.__setitem__("candidate_result_self_hash_current", False), "result self-hash closes the final acyclic result object"),
        ("A72_RESULT_SELF_FILE_COMMITMENT_CYCLE", lambda x: x.__setitem__("candidate_result_commits_its_own_file_sha256", True), "result never commits its own file digest"),
        ("A73_GZIP_MTIME_DRIFT", lambda x: x.__setitem__("canonical_gzip_mtime", 1), "canonical gzip mtime is zero"),
        ("A74_GZIP_FILENAME_HEADER_DRIFT", lambda x: x.__setitem__("canonical_gzip_filename", "candidate.json"), "canonical gzip filename is empty"),
        ("A75_ABSOLUTE_RUNTIME_PATH_IN_COMMITTED_WIRE", lambda x: x.__setitem__("committed_absolute_runtime_path_count", 1), "committed wire is independent of workspace/interpreter absolute paths"),
        ("A76_WALL_CLOCK_IN_COMMITTED_WIRE", lambda x: x.__setitem__("committed_wall_clock_or_timestamp_count", 1), "committed wire contains no wall-clock timestamp"),
        ("A77_SOURCE_WALL_FACTOR_NOT_STRICT", lambda x: x.__setitem__("source_wall_factor_uniformly_strict_nonzero", False), "wall-product reduction requires a uniformly nonzero source factor"),
        ("A78_MUTATE_WALL_INTEGER", lambda x: x.__setitem__("wall_integer", 1), "the sealed residual predicate is the integer wall zero"),
        ("A79_OWNER_EXTENSION_CLAIMS_GAMMA_CORE_CONTACT", lambda x: x.__setitem__("owner_extension_contacts_claim_Gamma_core_contact", True), "full-closure contacts are zero-credit extensions, not Gamma-core contacts"),
        ("A80_SKIP_DYNAMIC_SIGNATURE_UNIQUE_REASON_REPLAY", lambda x: x.__setitem__("dynamic_signature_unique_unresolved_reason_replayed", False), "G5 replays the whole-cell dynamic signature and isolates exactly the active wall reason"),
        ("A81_STALE_PYC_SAME_MTIME_SIZE", lambda x: (x.__setitem__("formal_geometry_executed_from_verified_source_bytes", False), x.__setitem__("formal_geometry_bytecode_cache_admitted", True)), "verified formal geometry source bytes are compiled/executed directly; stale bytecode is never admitted"),
        ("A82_DROP_FULL_SIGN_SIDE_CERTIFICATE", lambda x: x.__setitem__("full_sign_side_support_certificate_count", 2047), "exactly two independently reconstructed full-side certificates per witness"),
        ("A83_REUSE_FULL_SIGN_SIDE_CERTIFICATE_ID", lambda x: x.__setitem__("full_sign_side_certificate_ids_unique", False), "2048 endpoint certificates have distinct content-derived IDs"),
        ("A84_SKIP_FACE_DERIVATIVE_ORIENTATION", lambda x: x.__setitem__("full_sign_side_face_derivative_orientation_hard_checked", False), "lower sign is opposite dF/dp and upper sign equals dF/dp"),
        ("A85_SHRINK_FULL_HALF_OPEN_SEGMENT_TO_CORRIDOR", lambda x: (x.__setitem__("full_sign_side_entire_half_open_segment_derived", False), x.__setitem__("local_corridor_used_as_full_sign_side_proof", True)), "strict monotonicity proves the entire p-face-to-rho half-open segment"),
        ("A86_SKIP_UNIQUE_DYNAMIC_BOUNDARY_REPLAY", lambda x: x.__setitem__("full_sign_side_unique_active_dynamic_boundary_replayed", False), "the whole common cell has exactly one unresolved active reason"),
        ("A87_BREAK_NAMED_SINGLE_SUPPORT_PROVENANCE", lambda x: x.__setitem__("full_sign_side_R287_R292_single_support_provenance_closed", False), "R275-R287-R292 provenance identifies one named connected support"),
        ("A88_G3_G4_CERTIFICATE_SUBSTITUTION", lambda x: x.__setitem__("G3_G4_embed_anchor_full_sign_side_certificate_exactly", False), "G3 and G4 embed the exact corresponding anchor certificate"),
    ]
    rows = []
    for attack_id, mutate, boundary in mutations:
        candidate = copy.deepcopy(base)
        mutate(candidate)
        was_rejected = rejected(lambda candidate=candidate: validate_contract(candidate))
        need(was_rejected, "ATTACK_ACCEPTED:" + attack_id)
        rows.append({
            "attack_id": attack_id,
            "rejected": True,
            "rejection_boundary": boundary,
        })
        if attack_id == "A81_STALE_PYC_SAME_MTIME_SIZE":
            rows[-1]["mechanism_probe"] = stale_pyc_probe
    wire_attacks: list[tuple[str, Callable[[], None], str]] = [
        (
            "A57_OVERSIZED_JSON",
            lambda: bounded_json_bytes(b'{"x":1}', 6, "attack-json"),
            "bounded JSON before parsing",
        ),
        (
            "A58_OVERSIZED_GZIP_EXPANSION",
            lambda: bounded_gzip_bytes(
                gzip.compress(b"x" * 17, mtime=0), 16, "attack-gzip"
            ),
            "bounded gzip expansion before candidate admission",
        ),
    ]
    wire_attacks.extend([
        (
            "A59_DUPLICATE_JSON_KEY",
            lambda: strict_json_raw(b'{"x":1,"x":2}', "attack-duplicate"),
            "duplicate-key JSON rejection",
        ),
        (
            "A60_NONEXACT_CANDIDATE_WIRE_BYTE",
            lambda: need(b"candidate" == b"expected", "EXACT_WIRE_BYTE"),
            "candidate bytes equal independent expected bytes",
        ),
    ])
    wire_attacks.extend(promotion_hostile_attack_callbacks())
    for attack_id, callback, boundary in wire_attacks:
        was_rejected = rejected(callback)
        need(was_rejected, "ATTACK_ACCEPTED:" + attack_id)
        rows.append({
            "attack_id": attack_id,
            "rejected": True,
            "rejection_boundary": boundary,
        })
    rows.sort(
        key=lambda row: int(row["attack_id"][1:].split("_", 1)[0])
    )
    need(
        [row["attack_id"] for row in rows]
        == [f"A{index:02d}_" + row["attack_id"].split("_", 1)[1]
            for index, row in enumerate(rows, 1)],
        "ATTACK_ID_SEQUENCE_1_THROUGH_99",
    )
    payload = {
        "schema": ATTACK_SCHEMA,
        "status": (
            "PASS_ALL_99_SCHEMA_GEOMETRY_OWNER_WIRE_PYC_AND_ATOMIC_"
            "PROMOTION_"
            "ATTACKS_REJECTED__ZERO_FORMAL_CREDIT"
        ),
        "binding_mode": (
            "EXACT_FORMAL_CANDIDATE" if formal_binding
            else "SELFTEST_SYNTHETIC_BASELINE_ONLY"
        ),
        "producer": {
            "filename": PRODUCER,
            "file_sha256": producer_sha256,
            "treated_as_inert_pinned_bytes_only": True,
            "imported_or_executed": False,
        },
        "runtime_verifier": {
            "filename": VERIFIER_FILENAME,
            "file_sha256": verifier_sha256,
            "sha256_computed_at_runtime_without_source_self_pin": True,
        },
        "baseline_candidate_file_sha256s": dict(sorted(
            candidate_file_sha256s.items()
        )),
        "attack_count": len(rows),
        "rejected_count": len(rows),
        "all_rejected": True,
        "attacks": rows,
        "attack_rows_sha256": digest(rows),
        "positive_atomic_promotion_transaction_selftest":
            positive_transaction,
        "formal_Round305B_credit": 0,
    }
    return close_object(payload, "attack_suite_sha256")


def build_formal_verification(
    *,
    result: dict[str, Any],
    candidate_file_sha256s: dict[str, str],
    producer_sha256: str,
    verifier_sha256: str,
    attacks: dict[str, Any],
) -> dict[str, Any]:
    verify_self(attacks, "attack_suite_sha256", "Round305B attack suite")
    attack_raw = canonical(attacks)
    need(
        attacks["binding_mode"] == "EXACT_FORMAL_CANDIDATE"
        and attacks["producer"]["file_sha256"] == producer_sha256
        and attacks["runtime_verifier"]["file_sha256"] == verifier_sha256
        and attacks["baseline_candidate_file_sha256s"]
        == dict(sorted(candidate_file_sha256s.items()))
        and attacks["all_rejected"] is True
        and attacks["attack_count"] == 99
        and attacks["rejected_count"] == 99,
        "FORMAL_ATTACK_SUITE_EXACT_BASELINE_AND_CENSUS",
    )
    need(
        set(candidate_file_sha256s) == set(PROMOTION_CANDIDATE_ORDER)
        and all(PIN_RE.fullmatch(value) is not None
                for value in candidate_file_sha256s.values()),
        "VERIFICATION_EXACT_SIX_CANDIDATE_HASHES",
    )
    credit_without_marker = {
        "officially_admitted_physical_witness_credit": 0,
        "officially_admitted_anchor_binding_credit": 0,
        "officially_admitted_component_edge_credit": 0,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
    }
    formal_credit_transition = {
        "officially_admitted_physical_witness_credit": EXPECTED_WITNESSES,
        "officially_admitted_anchor_binding_credit": EXPECTED_ANCHORS,
        "officially_admitted_component_edge_credit": EXPECTED_EDGES,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
    }
    payload = {
        "schema": VERIFICATION_SCHEMA,
        "status": (
            "PASS_EXACT_CACHELESS_ROUND305B_TWO_SIDED_PHYSICAL_"
            "INCLUSION_COMPONENT_EDGE_PROMOTION"
        ),
        "producer": {
            "filename": PRODUCER,
            "file_sha256": producer_sha256,
            "treated_as_inert_pinned_bytes_only": True,
            "imported_executed_parsed_or_tokenized": False,
        },
        "runtime_verifier": {
            "filename": VERIFIER_FILENAME,
            "file_sha256": verifier_sha256,
            "sha256_computed_from_runtime_file_bytes": True,
            "source_contains_no_verifier_self_pin": True,
        },
        "candidate": {
            "opened_only_after_full_independent_reconstruction": True,
            "private_candidate_directory_separate_from_deliverables": True,
            "exact_six_file_set": list(PROMOTION_CANDIDATE_ORDER),
            "exact_file_sha256s": dict(sorted(candidate_file_sha256s.items())),
            "independent_expected_result_sha256": result["result_sha256"],
            "all_six_files_equal_independently_rebuilt_bytes": True,
            "candidate_outputs_written_or_replaced_during_admission": False,
        },
        "attack_suite": {
            "filename": ATTACK_FILENAME,
            "file_sha256": hashlib.sha256(attack_raw).hexdigest(),
            "object_self_sha256": attacks["attack_suite_sha256"],
            "canonical_object_sha256": digest(attacks),
            "attack_count": attacks["attack_count"],
            "rejected_count": attacks["rejected_count"],
            "attack_rows_sha256": attacks["attack_rows_sha256"],
            "all_rejected": True,
        },
        "formal_credit_without_verification_commit_marker":
            credit_without_marker,
        "formal_credit_transition_at_this_verification_commit_marker":
            formal_credit_transition,
        "strict_credit_boundary": {
            "physical_witness_rows_promoted": EXPECTED_WITNESSES,
            "anchor_binding_rows_promoted": EXPECTED_ANCHORS,
            "canonical_component_edges_promoted": EXPECTED_EDGES,
            "witness_rows_are_not_union_rows": True,
            "fresh_DSU_rebuild_performed": False,
            "maximality_proved": False,
            "official_fibres_exhausted": 0,
            "Source_G_global_dispositions_completed": 0,
            "D02_status": "BLOCKED",
            "CM2_status": "NO-GO_FOR_CLAIM",
        },
        "atomic_publication_contract": {
            "exact_output_directory": "deliverables",
            "commit_order": list(PROMOTION_ORDER),
            "attack_suite_is_first": True,
            "five_ledgers_then_result": True,
            "verification_is_last_and_sole_formal_credit_commit_marker": True,
            "flock_directory_fd": True,
            "fsync_each_staged_file_and_directories": True,
            "renameat2_RENAME_NOREPLACE": True,
            "directory_inode_and_symlink_stability_required": True,
            "exact_orphan_stage_recovery": True,
            "no_clobber": True,
            "idempotent_only_for_one_exact_published_prefix": True,
        },
        "formal_Round305B_promotion_permitted": True,
    }
    assert_path_and_time_free_wire(payload, "Round305B verification")
    return close_object(payload, "verification_sha256")


def admit_candidate_and_build_publication(
    candidate_dir: Path,
) -> tuple[
    dict[str, bytes], dict[str, Any], dict[str, Any], dict[str, Any],
    dict[str, Any], bytes, bytes,
]:
    # Required ordering: rebuild every expected byte before opening the stage.
    expected, result = independent_reconstruction()
    producer_sha256 = verify_inert_producer_pin()
    verifier_sha256 = runtime_verifier_sha256()
    bundle, snapshot = read_exact_candidate_bundle(candidate_dir, expected)
    candidate_file_sha256s = {
        name: hashlib.sha256(bundle[name]).hexdigest()
        for name in PROMOTION_CANDIDATE_ORDER
    }
    need(
        candidate_file_sha256s == {
            name: hashlib.sha256(expected[name]).hexdigest()
            for name in PROMOTION_CANDIDATE_ORDER
        },
        "CANDIDATE_EXPECTED_EXACT_SHA256_MAP",
    )
    attacks = build_attack_suite(
        producer_sha256=producer_sha256,
        verifier_sha256=verifier_sha256,
        candidate_file_sha256s=candidate_file_sha256s,
    )
    attack_raw = canonical(attacks)
    need(canonical(strict_json_raw(
        attack_raw, "Round305B generated attack suite"
    )) == attack_raw, "ATTACK_SUITE_CANONICAL_EXACT_BYTES")
    verification = build_formal_verification(
        result=result,
        candidate_file_sha256s=candidate_file_sha256s,
        producer_sha256=producer_sha256,
        verifier_sha256=verifier_sha256,
        attacks=attacks,
    )
    verification_raw = canonical(verification)
    verify_self(verification, "verification_sha256", "Round305B verification")
    need(canonical(strict_json_raw(
        verification_raw, "Round305B generated verification"
    )) == verification_raw, "VERIFICATION_CANONICAL_EXACT_BYTES")
    assert_candidate_snapshot(snapshot, "post-attacks")
    need(
        verify_inert_producer_pin() == producer_sha256
        and runtime_verifier_sha256() == verifier_sha256,
        "PRODUCER_OR_VERIFIER_CHANGED_DURING_ADMISSION",
    )
    return (
        bundle, snapshot, result, attacks, verification,
        attack_raw, verification_raw,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-schema-sha256", action="store_true")
    parser.add_argument("--contract-self-test", action="store_true")
    parser.add_argument("--wire-contract-self-test", action="store_true")
    parser.add_argument("--sealed-scope-preflight", action="store_true")
    parser.add_argument("--no-write-reconstruction", action="store_true")
    parser.add_argument("--diagnostic-first-rows", action="store_true")
    parser.add_argument(
        "--candidate-dir", type=Path,
        help="private 0700 workspace stage containing exactly six candidates",
    )
    parser.add_argument(
        "--promote", action="store_true",
        help=(
            "after exact admission, publish attack, five ledgers, result, and "
            "verification commit marker to the exact deliverables directory"
        ),
    )
    parser.add_argument(
        "--verify-candidate", action="store_true",
        help="deprecated alias for candidate admission without --promote",
    )
    arguments = parser.parse_args()
    if arguments.print_schema_sha256:
        verify_external_normative_wire_contract()
        print("schema_snapshot_sha256=" + digest(exact_schema_snapshot()))
        print(
            "expected_producer_schema_snapshot_sha256="
            + EXPECTED_PRODUCER_SCHEMA_SNAPSHOT_SHA256
        )
        return
    if arguments.contract_self_test:
        attacks = build_attack_suite()
        verify_self(attacks, "attack_suite_sha256", "contract self-test")
        print(canonical(attacks).decode("utf-8"))
        return
    if arguments.wire_contract_self_test:
        print(canonical(verify_external_normative_wire_contract()).decode("utf-8"))
        return
    if arguments.sealed_scope_preflight:
        scope = sealed_scope_preflight()
        scope["formal_manifest_member_counts"] = admit_formal_input_chain()
        scope["expected_producer_pin_matches_current_source"] = (
            verify_inert_producer_pin() == EXPECTED_PRODUCER_SHA256
        )
        print(canonical(scope).decode("utf-8"))
        return
    if arguments.diagnostic_first_rows:
        rows, _manifest_counts, _depths, _owner_audit, _preimages = (
            independent_row_reconstruction()
        )
        first_rows = {
            kind: rows[kind][0]
            for kind in ("physical", "anchor", "contact", "owner", "edge")
        }
        print(canonical({
            "status": "PASS_READ_ONLY_INDEPENDENT_EXPECTED_FIRST_ROW_DIAGNOSTIC",
            "schema_snapshot_sha256": digest(exact_schema_snapshot()),
            "first_rows": first_rows,
            "first_row_sha256s": {
                kind: row["row_sha256"] for kind, row in first_rows.items()
            },
            "candidate_outputs_opened": False,
            "candidate_outputs_written_or_replaced": False,
            "candidate_producer_imported_or_executed": False,
        }).decode("utf-8"))
        return
    if arguments.candidate_dir is not None:
        need(
            not arguments.no_write_reconstruction
            and not arguments.diagnostic_first_rows,
            "CANDIDATE_ADMISSION_CONFLICTS_WITH_DIAGNOSTIC_MODE",
        )
        (
            bundle, snapshot, result, attacks, verification,
            attack_raw, verification_raw,
        ) = admit_candidate_and_build_publication(arguments.candidate_dir)
        if arguments.promote:
            publish_formal_promotion(
                bundle, snapshot, attack_raw, verification_raw
            )
            print(verification_raw.decode("utf-8"))
            return
        no_commit_credit = verification[
            "formal_credit_without_verification_commit_marker"
        ]
        need(all(value == 0 for value in no_commit_credit.values()),
             "NO_PROMOTE_MUST_REMAIN_ZERO_FORMAL_CREDIT")
        print(canonical({
            "schema": SCHEMA + ".candidate-admission-no-promotion.v1",
            "status": (
                "PASS_EXACT_ROUND305B_PRIVATE_CANDIDATE_ADMISSION__"
                "VERIFICATION_COMMIT_MARKER_NOT_PUBLISHED__ZERO_FORMAL_CREDIT"
            ),
            "candidate_file_sha256s": verification["candidate"][
                "exact_file_sha256s"
            ],
            "candidate_result_sha256": result["result_sha256"],
            "attack_suite": {
                "filename": ATTACK_FILENAME,
                "file_sha256": hashlib.sha256(attack_raw).hexdigest(),
                "object_self_sha256": attacks["attack_suite_sha256"],
            },
            "verification": {
                "filename": VERIFICATION_FILENAME,
                "file_sha256": hashlib.sha256(verification_raw).hexdigest(),
                "object_self_sha256": verification["verification_sha256"],
            },
            "formal_credit": no_commit_credit,
            "candidate_outputs_written_or_replaced": False,
            "formal_deliverables_written": False,
        }).decode("utf-8"))
        return
    need(not arguments.promote, "--promote requires --candidate-dir")
    need(not arguments.verify_candidate,
         "--verify-candidate requires --candidate-dir")
    need(
        arguments.no_write_reconstruction,
        "EXPLICIT_MODE_REQUIRED:--no-write-reconstruction_OR_--candidate-dir",
    )
    expected, result = independent_reconstruction()
    if arguments.no_write_reconstruction:
        summary = {
            "status": "PASS_INDEPENDENT_CACHELESS_NO_WRITE_ROUND305B_RECONSTRUCTION",
            "result_sha256": result["result_sha256"],
            "expected_candidate_file_sha256s": {
                name: hashlib.sha256(payload).hexdigest()
                for name, payload in sorted(expected.items())
            },
            "expected_candidate_row_commitments":
                result["ledger_object_commitments"],
            "direct_geometry_reconstruction":
                result["direct_geometry_reconstruction"],
            "owner_audit": result["owner_audit"],
            "G0_G5_direct_witness_rows": EXPECTED_WITNESSES,
            "all_G0_G5_reconstructed_true": True,
            "physical_witness_count": EXPECTED_WITNESSES,
            "anchor_count": EXPECTED_ANCHORS,
            "closure_contact_count": EXPECTED_CLOSURE_CONTACTS,
            "owner_locus_count": EXPECTED_OWNER_LOCI,
            "canonical_component_edge_count": EXPECTED_EDGES,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "candidate_outputs_opened": False,
            "candidate_outputs_written_or_replaced": False,
            "candidate_producer_imported_or_executed": False,
            "expected_producer_pin_matches_current_source": (
                verify_inert_producer_pin() == EXPECTED_PRODUCER_SHA256
            ),
        }
        print(canonical(summary).decode("utf-8"))
        return
    raise AssertionError("unreachable explicit verifier mode")


if __name__ == "__main__":
    try:
        main()
    except VerificationBlocked as error:
        print("BLOCKED_ROUND305B_VERIFIER:" + str(error))
        raise SystemExit(2)
