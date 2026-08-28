#!/usr/bin/env python3
"""Fail-closed Round305B zero-credit candidate producer.

Round305B is the formal rebase of the 1,024 Round300A residual pairs onto a
sealed Round305A scope.  This source deliberately has no formal promotion
path until all of the following are true:

* the now-sealed complete Round303B, Round304, and Round305A manifests are
  admitted by exact source-level pins;
* the exact 1,024 residual rows and 2,048 endpoints are reconstructed;
* all 124 official keys are enumerated from the sealed Round304 universe;
* every residual pair receives a direct G0--G5 two-sided physical proof;
* all 3,536 boundary owners and all 2,048 anchors are reconstructed; and
* 1,024 witness conclusions are deduplicated to exactly eight canonical
  component edges (never 1,024 component edges or DSU unions).

Round305A is now sealed and the direct geometry kernel is implemented.  This
source may publish only the exact five-ledger-plus-result candidate byte set;
the result is the last candidate commit marker.  Publication grants zero
officially admitted credit until a separately frozen independent verifier
publishes its attack suite and verification object.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import ctypes
import errno
import fcntl
from fractions import Fraction as Q
import gzip
import hashlib
import importlib
import importlib.machinery
import importlib.util
import io
import json
from math import isqrt
import os
from pathlib import Path
import py_compile
import re
import stat
import sys
import tempfile
from types import ModuleType
from typing import Any, Callable, Iterator, TextIO
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
PRODUCER_FILENAME = PREFIX + ".py"
WIRE_SPEC_FILENAME = PREFIX + "_wire_spec.json"
WIRE_CONTRACT_FIXTURE_FILENAME = PREFIX + "_wire_contract_fixture.json"

R303B_PREFIX = "cm2_round303b_source_g_unified_attachment_edge_promotion"
R304_PREFIX = (
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild"
)
R305A_PREFIX = (
    "cm2_round305a_source_g_r300a_post_r304_residual_scope_reprojection"
)

R174_PREFIX = "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization"
R179_PREFIX = "cm2_round179_source_g_residual_tube_arrangement"
R275_PREFIX = "cm2_round275_source_g_complete_reverse_rechart_materialization"
R287_PREFIX = "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe"
R292_PREFIX = "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe"
R294_PREFIX = "cm2_round294_source_g_occurrence_registry_atomic_promotion"
R294B_PREFIX = "cm2_round294b_source_g_registry_builder_admission_closure"
R300A_PREFIX = "cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion"
R300B_PREFIX = (
    "cm2_round300b_source_g_registry_boundary_and_complete_r275_"
    "face_inventory_closure"
)

R303B_MANIFEST = R303B_PREFIX + "_manifest.sha256"
R304_MANIFEST = R304_PREFIX + "_manifest.sha256"
R305A_MANIFEST = R305A_PREFIX + "_manifest.sha256"
R305A_RESULT = R305A_PREFIX + "_result.json"
R305A_LEDGER = R305A_PREFIX + "_scope_reprojection_ledger.json.gz"
R305A_ATTACKS = R305A_PREFIX + "_attack_suite.json"
R305A_VERIFICATION = R305A_PREFIX + "_verification.json"
R304_MEMBER_LEDGER = R304_PREFIX + "_member_component_ledger.json.gz"

R174_MANIFEST = R174_PREFIX + "_manifest.sha256"
R179_MANIFEST = R179_PREFIX + "_manifest.sha256"
R275_MANIFEST = R275_PREFIX + "_manifest.sha256"
R287_MANIFEST = R287_PREFIX + "_manifest.sha256"
R292_MANIFEST = R292_PREFIX + "_manifest.sha256"
R294_MANIFEST = R294_PREFIX + "_manifest.sha256"
R294B_MANIFEST = R294B_PREFIX + "_manifest.sha256"
R300A_MANIFEST = R300A_PREFIX + "_manifest.sha256"
R300B_MANIFEST = R300B_PREFIX + "_manifest.sha256"

R174_ROWS = R174_PREFIX + "_rows.json"
R275_CERTIFICATE = R275_PREFIX + "_certificate.json"
R287_LEDGER = R287_PREFIX + "_ledger.json.gz"
R292_LEDGER = R292_PREFIX + "_ledger.json.gz"
R294_REGISTRY_LEDGER = R294_PREFIX + "_registry_ledger.json.gz"
R300A_LEDGER = R300A_PREFIX + "_ledger.json.gz"

# Complete formal input closure.  A manifest digest plus its exact member
# count closes the complete member-name/hash table before any ledger opens.
FORMAL_MANIFEST_PINS: dict[str, tuple[str, int]] = {
    R174_MANIFEST: (
        "9e92db7748a2c0acdce532c830f899ce153765de64a59e9f372df3099ac91b76", 7,
    ),
    R179_MANIFEST: (
        "8fd5ae3a0cdd0c3321c0f8ffe6183ab57d31088b96523fa41ce0ebbe10d78b76", 7,
    ),
    R275_MANIFEST: (
        "a5dbf43a144a0a752f467911ee59e6afd6d2d60d27e0bc80bc45b7afa9334669", 6,
    ),
    R287_MANIFEST: (
        "85a9d4fcf9d9931a0e352eeef7582347b12325b92ffc78f2ee40c77c58093751", 6,
    ),
    R292_MANIFEST: (
        "4ea92e4112cae18aa0c13a6d2308816bafc19e4129c09d8b6be914268cfc4870", 7,
    ),
    R294_MANIFEST: (
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131", 9,
    ),
    R294B_MANIFEST: (
        "fc16aa2792a59dff922afcc8ec66b1ca015251af3c5f718d9d909439a2990d76", 11,
    ),
    R300A_MANIFEST: (
        "9f9e86d93aebe2b47e525af795a3a9e8331ab3b6f2d71ecafe69429238a1aee8", 8,
    ),
    R300B_MANIFEST: (
        "6208c4bfd8b147f06ffb735d4b5621faff22585831b5f19d48e8125514ac4a6b", 14,
    ),
}

FORMAL_CRITICAL_PINS = {
    R174_PREFIX + ".py":
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    R179_PREFIX + ".py":
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    R174_ROWS:
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    R275_CERTIFICATE:
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R287_LEDGER:
        "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a",
    R292_LEDGER:
        "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    R294_REGISTRY_LEDGER:
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    R300A_LEDGER:
        "ddc1a8bc53861afeb93d3569c6efa228f17d86f161db31a39fa9b72458ab8f2d",
    R300B_PREFIX + ".py":
        "e760511408ac78e627155f55671b3e2e8d6f9b1b8163a82ffac65230b10fa93d",
}

# R273/R274 are lineage references only.  Their needed rational transforms
# and extremal-point formula are transcribed below; neither source is ever
# imported or executed by Round305B.
REFERENCE_ONLY_SOURCE_PINS = {
    "cm2_gate3_chart_seam_quotient_cert.py":
        "fa00d4c14ee24b8f3fbc7f345deef13deb272080a886b68d2aa2f9c92a456fe1",
    "cm2_round273_source_g_reverse_rechart_probe.py":
        "40b18650a1fe8d797daf776cb9305686c21fa2eb5a7886c48ce91d697c93105c",
    "cm2_round274_source_g_reverse_rechart_tail_arrangement_probe.py":
        "677813e132d62732900a26edc3fae5d562049d8d1fac2cea59f7c65d41735292",
}

# Every project-local module executed by the direct interval kernel is loaded
# from these exact source bytes with compile()+exec().  No importlib source/
# bytecode loader is permitted for this graph, so a timestamp-valid stale pyc
# cannot influence formal geometry.
CACHELESS_RUNTIME_SOURCE_MODULES = (
    (
        "cm2_gate3_candidate_first_hit_cert",
        "cm2_gate3_candidate_first_hit_cert.py",
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    ),
    (
        "cm2_gate3_ge_interval_atlas_cert",
        "cm2_gate3_ge_interval_atlas_cert.py",
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    ),
    (
        "cm2_gate3_eight_cell_symmetry_atlas_cert",
        "cm2_gate3_eight_cell_symmetry_atlas_cert.py",
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    ),
    (
        R174_PREFIX,
        R174_PREFIX + ".py",
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    ),
    (
        R174_PREFIX + "_verifier",
        R174_PREFIX + "_verifier.py",
        "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
    ),
    (
        R179_PREFIX,
        R179_PREFIX + ".py",
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    ),
)

FORBIDDEN_RUNTIME_SOURCE_FRAGMENTS = (
    ".tmp", "openclaw-spikes", "r305-r300a-physical-package",
)

R303B_MANIFEST_SHA256 = (
    "7d7293c488a05c8873a63b7d63d0bf125260c6b9d3c60595201896cfde0c9786"
)
R304_MANIFEST_SHA256 = (
    "de49f4233f6a22f43385e727071c5a5ebac68c35788dc2dd13e71d045639838c"
)

# Filled only after P0 published the complete eight-member, cold-replayed
# Round305A manifest.  Presence of a file or a caller-supplied hash is not an
# admissible replacement for this source-level pin.
R305A_MANIFEST_SHA256: str | None = (
    "21a938d65d50856b4d1ecae7414259b3481f4f2f8207d91debc951e06441a9f7"
)

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

R305A_RESULT_OBJECT_SHA256 = (
    "c391ecca3f5af8227052c628bda77104ec564d4eeaa625fafbde32a3ada352eb"
)
R305A_VERIFICATION_OBJECT_SHA256 = (
    "9654f43c32aacfd3a27b6baa18d65755dfb9c867bd869aaa586a9b736fcf7589"
)
R305A_SCHEMA_SNAPSHOT_SHA256 = (
    "19dd648b76f13ff02d161d4e5f3968c7e527f74887cb37c725c7a467912515f3"
)
RESIDUAL_PAIR_SET_SHA256 = (
    "f7f9941f84428df71039b4708dfa251eae6c962267f68ccd13945ee445c5bf29"
)
RESIDUAL_ENDPOINT_SET_SHA256 = (
    "b09fe8149f89a95c2c9effcbce33bc49df24065987c870fc65b09ac85fe98779"
)
RESIDUAL_FINAL_COMPONENT_PAIR_SET_SHA256 = (
    "0e783f8ded68b885bd4e0a70dd27049e6e74194c6f301c8e49ebfc8d1add1344"
)
RESIDUAL_SOURCE_ROW_IDS_SHA256 = (
    "72bebd529ba7bdda941c5cdd198d04a7d4bec878c8f65ea5688929f75e64832c"
)
RESIDUAL_SOURCE_ROW_HASHES_SHA256 = (
    "c726bdc422969e2280457f0ed6d87de03ab63b8d410b6c61171fbf85138a7017"
)

EXPECTED_WITNESSES = 1_024
EXPECTED_ANCHORS = 2_048
EXPECTED_CLOSURE_CONTACTS = 3_536
EXPECTED_FACE_CONTACTS = 1_856
EXPECTED_DIAGONAL_CONTACTS = 1_680
EXPECTED_OWNER_LOCI = 2_696
EXPECTED_FACE_OWNER_LOCI = 1_856
EXPECTED_VERTEX_OWNER_LOCI = 840
EXPECTED_CANONICAL_COMPONENT_EDGES = 8
EXPECTED_WITNESSES_PER_COMPONENT_EDGE = 128
EXPECTED_R304_MEMBERS = 564_492
EXPECTED_OFFICIAL_KEYS = 124
EXPECTED_RESIDUAL_OFFICIAL_KEYS = 16
MAXIMUM_LATER_DSU_RANK_REDUCTIONS = 8

# D4 is an optimization only.  Every one of the 1,024 rows remains a direct
# verification obligation unless a separately sealed transfer theorem is
# admitted by a future source revision.
D4_TRANSFER_ENABLED = False
D4_TRANSFER_CERTIFICATE_MANIFEST_SHA256: str | None = None

# The direct G0--G5 kernel and the zero-credit candidate publication path are
# implemented.  Neither flag authorizes mathematical promotion: officially
# admitted witness/edge/DSU/downstream credit remains zero until a separately
# frozen independent verifier publishes its attack suite and verification.
DIRECT_GEOMETRY_KERNEL_IMPLEMENTED = True
FORMAL_GEOMETRY_KERNEL_IMPLEMENTED = True
CANDIDATE_PUBLICATION_ENABLED = True

PIN_RE = re.compile(r"^[0-9a-f]{64}$")
MAX_JSON_BYTES = 64 * 1024 * 1024


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

RELATIVE_PHYSICAL_CLOSURE_LIMIT_LEMMA = {
    "lemma_id": "CM2_RELATIVE_PHYSICAL_P_TO_RHO_TWO_SIDED_LIMIT_V1",
    "ambient_space": (
        "X is the physical collision section with its relative topology; "
        "Phi(z,p,s)=(q=(9/25)n(z), "
        "u=sqrt(1-p^2)n(z)+p*(-n_y(z),n_x(z)),s)."
    ),
    "statement": (
        "Let B_core be a connected positive-area closed rational rectangle "
        "strictly contained in the open endpoint-support base, and let "
        "F:B_core times [p_minus,p_plus]->R be continuous, with a uniform "
        "strict nonzero dF/dp sign on the whole common R292 cell, and uniform "
        "opposite nonzero F signs on the two p faces. Then there is a unique "
        "continuous rho:B_core->(p_minus,p_plus). On the lower half-open "
        "segment p_minus<=p<rho(b), F has the sign opposite dF/dp; on the "
        "upper half-open segment rho(b)<p<=p_plus, F has the dF/dp sign. If "
        "each endpoint face sign equals its R275 desired side, the whole-cell "
        "dynamic signature has only that wall predicate unresolved, and the "
        "sealed R287->R292 chain identifies the corresponding sign slice as "
        "one named connected support, then both full segments lie in their "
        "named supports. Phi continuity makes every Phi(b,rho(b)) a "
        "relative-X limit of each side, so Gamma_core is contained in both closures."
    ),
    "proof": [
        "Existence and uniqueness on every p fibre follow from IVT and strict monotonicity.",
        "Uniform bracketing on B_core plus continuity of F and uniqueness imply continuity of rho.",
        "Strict monotonicity and F(rho(b))=0 give the opposite-derivative sign on the full lower half-open segment and the derivative sign on the full upper half-open segment.",
        "The exact p-face replay selects the endpoint whose R275 desired sign equals that segment sign.",
        "Because the whole common cell has exactly the active wall predicate unresolved, no other validity boundary cuts either segment.",
        "The content-closed R287 region, R292 cell, and single-member connected-support component identify the complete retained sign slice with the named endpoint support.",
        "For fixed b, choose rational p_k monotonically inside that certified full sign side toward rho(b).",
        "Continuity of Phi gives Phi(b,p_k)->Phi(b,rho(b)) in the relative topology of X.",
        "Repeat from the opposite side; the common limit is the included physical wall-event state.",
    ],
    "corridor_role": (
        "Positive-volume corridor boxes certify only a local nonempty strict "
        "sign witness. Complete p_face-to-rho support containment is derived "
        "by the full-sign-side certificate; corridors are disjoint from "
        "Gamma_core and are never attachment or intersection witnesses."
    ),
}

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
    "contact_pair_owner_extension_patch_ids", "contact_kind", "base_dimension",
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

# Normative, data-independent wire contract.  This object contains schemas,
# vocabularies, and digest recipes only: it deliberately contains no digest
# observed from a Round305B row, ledger, result, or output file.  The verifier
# must carry an independently transcribed literal and independently reconstruct
# every dynamic value.
WIRE_SPEC = {
    "wire_spec_id": "CM2_ROUND305B_NORMATIVE_WIRE_SPEC_V2",
    "wire_spec_version": 2,
    "additional_properties_permitted": False,
    "contract_notation": {
        "$ref:path": (
            "normative reference to the exact value or shape at dot-separated "
            "path in this WIRE_SPEC; the marker string itself is never emitted"
        ),
        "$self:entire WIRE_SPEC object": (
            "substitute the complete enclosing WIRE_SPEC object; the marker "
            "string itself is never emitted"
        ),
        "keys_exact": (
            "the emitted object has exactly this key set and no additional keys"
        ),
        "keys_exact_in_construction_order": (
            "the semantic key set is exact; construction order is documented "
            "for audits, while canonical JSON sorts object keys"
        ),
    },
    "protocol_files": {
        "wire_spec_filename": WIRE_SPEC_FILENAME,
        "wire_contract_fixture_filename": WIRE_CONTRACT_FIXTURE_FILENAME,
        "bytes": "canonical JSON UTF-8 with no trailing newline",
        "contain_actual_candidate_row_ledger_or_file_commitments": False,
        "formal_credit": 0,
        "required_as_future_formal_manifest_members": True,
        "producer_embedded_literal_must_equal_wire_spec_file_object": True,
        "producer_synthetic_fixture_must_equal_fixture_file_object": True,
    },
    "definitions": {
        "sha256": {
            "json_type": "string",
            "regex": "^[0-9a-f]{64}$",
        },
        "rational": {
            "json_type": "string",
            "grammar": "0|-?[1-9][0-9]*|-?[1-9][0-9]*/[1-9][0-9]*",
            "normal_form": (
                "lowest terms; positive denominator; denominator one encoded "
                "as an integer; negative zero forbidden"
            ),
        },
        "rational_base_z_s": {
            "json_type": "array",
            "length": 4,
            "items": "$ref:rational",
            "coordinate_order": ["z_lower", "z_upper", "s_lower", "s_upper"],
        },
        "rational_box_z_p_s": {
            "json_type": "array",
            "length": 6,
            "items": "$ref:rational",
            "coordinate_order": [
                "z_lower", "z_upper", "p_lower", "p_upper",
                "s_lower", "s_upper",
            ],
        },
        "rational_box_t_p_s": {
            "json_type": "array",
            "length": 6,
            "items": "$ref:rational",
            "coordinate_order": [
                "t_lower", "t_upper", "p_lower", "p_upper",
                "s_lower", "s_upper",
            ],
        },
        "strict_sign": {
            "json_type": "string",
            "enum": ["STRICT_NEGATIVE", "STRICT_POSITIVE"],
        },
        "wall_predicate_details": {
            "json_type": "object",
            "keys_exact": [
                "kind", "axis", "wall", "source_wall_factor",
                "target_wall_factor_F", "wall_event_product",
            ],
            "fields": {
                "kind": {"const": "wall_endpoint_or_count_transition"},
                "axis": {"enum": ["X", "Y"]},
                "wall": {"const": 0},
                "source_wall_factor": {
                    "enum": ["source_x-0", "source_y-0"],
                },
                "target_wall_factor_F": {
                    "enum": ["hit_x-0", "hit_y-0"],
                },
                "wall_event_product": {
                    "enum": [
                        "(source_x-0)*(hit_x-0)",
                        "(source_y-0)*(hit_y-0)",
                    ],
                },
            },
        },
        "wall_event_product_replay": {
            "json_type": "object",
            "keys_exact": [
                "active_reason", "predicate_details",
                "source_wall_factor_sign", "target_wall_factor_sign",
                "wall_event_product_sign",
                "outer_rational_signed_physical_box",
            ],
            "fields": {
                "active_reason": {
                    "enum": [
                        "wall_endpoint_or_count_transition:X:0",
                        "wall_endpoint_or_count_transition:Y:0",
                    ],
                },
                "predicate_details": "$ref:wall_predicate_details",
                "source_wall_factor_sign": "$ref:strict_sign",
                "target_wall_factor_sign": {
                    "enum": ["STRICT_NEGATIVE", "STRICT_POSITIVE", "OVERWRAP"],
                },
                "wall_event_product_sign": {
                    "enum": ["STRICT_NEGATIVE", "STRICT_POSITIVE", "OVERWRAP"],
                },
                "outer_rational_signed_physical_box": {
                    "$ref": "rational_box_t_p_s",
                    "derived_by": (
                        "$ref:deterministic_construction_recipes."
                        "signed_t_outward_dyadic_enclosure"
                    ),
                },
            },
        },
        "active_function_identity": {
            "json_type": "object",
            "keys_exact": [
                "adjacent_chart", "owner_target", "active_reason",
                "active_function_expression",
                "active_function_evaluator_module_sha256",
                "interval_geometry_module_sha256",
            ],
            "fields": {
                "adjacent_chart": {"type": "nonempty-string"},
                "owner_target": {"type": "nonempty-string"},
                "active_reason": {
                    "enum": [
                        "wall_endpoint_or_count_transition:X:0",
                        "wall_endpoint_or_count_transition:Y:0",
                    ],
                },
                "active_function_expression": {
                    "enum": [
                        "interval_geometry(adjacent_chart,owner_target).hit_x[0]-arb(0)",
                        "interval_geometry(adjacent_chart,owner_target).hit_y[0]-arb(0)",
                    ],
                },
                "active_function_evaluator_module_sha256": "$ref:sha256",
                "interval_geometry_module_sha256": "$ref:sha256",
            },
        },
        "full_sign_side_to_rho_support_certificate": {
            "json_type": "object",
            "keys_exact": [
                "certificate_id", "endpoint_occurrence_id", "endpoint_side",
                "owner_face", "approach", "oriented_p_face",
                "graph_bracket_p", "proof_closed_core_base_z_s",
                "exact_common_R292_open_cell_t2_p_s", "active_function_id",
                "active_reason", "active_factor_side_sign",
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
            ],
            "fields": {
                "certificate_id": {
                    "prefix": "round305b-full-sign-side-support:",
                    "derived_by": "$ref:id_domains.full_sign_side_support_certificate_id",
                },
                "endpoint_occurrence_id": {"type": "source-occurrence-id"},
                "endpoint_side": {"enum": ["LEFT", "RIGHT"]},
                "owner_face": {"enum": ["LOWER", "UPPER"]},
                "approach": {
                    "enum": [
                        "P_APPROACHES_RHO_FROM_BELOW",
                        "P_APPROACHES_RHO_FROM_ABOVE",
                    ],
                },
                "oriented_p_face": "$ref:rational",
                "graph_bracket_p": {"type": "array[2]<rational>"},
                "proof_closed_core_base_z_s": "$ref:rational_base_z_s",
                "exact_common_R292_open_cell_t2_p_s": "$ref:rational_box_z_p_s",
                "active_function_id": {"prefix": "round305b-active-function:"},
                "active_reason": {
                    "enum": [
                        "wall_endpoint_or_count_transition:X:0",
                        "wall_endpoint_or_count_transition:Y:0",
                    ],
                },
                "active_factor_side_sign": "$ref:strict_sign",
                "exact_F_p_face_sign": "$ref:strict_sign",
                "uniform_strict_dF_dp_sign_on_whole_common_R292_cell":
                    "$ref:strict_sign",
                "F_at_rho_equals_zero": {"const": True},
                "face_sign_derivative_orientation": {
                    "enum": [
                        "LOWER_FACE_SIGN_IS_OPPOSITE_DF_DP",
                        "UPPER_FACE_SIGN_EQUALS_DF_DP",
                    ],
                },
                "face_sign_derivative_orientation_hard_checked": {"const": True},
                "exact_full_half_open_segment": {
                    "enum": [
                        "p_face<=p<rho(z,s)",
                        "rho(z,s)<p<=p_face",
                    ],
                },
                "strict_monotonicity_retains_face_sign_on_entire_segment": {
                    "const": True,
                },
                "endpoint_R275_active_factor_side_sign_equals_face_sign": {
                    "const": True,
                },
                "whole_cell_dynamic_signature_exactly_one_unresolved_active_reason": {
                    "const": True,
                },
                "all_other_whole_cell_validity_predicates_uniformly_strict": {
                    "const": True,
                },
                "R287_R292_single_connected_support_provenance": {
                    "keys_exact": [
                        "Round275_region_id", "Round275_region_row_sha256",
                        "R287_region_disposition_row_id", "R287_region_row_sha256",
                        "R292_refinement_cell_row_id", "R292_refinement_cell_row_sha256",
                        "R292_connected_support_component_row_id",
                        "R292_connected_support_component_row_sha256",
                        "connected_positive_open_support_member_count",
                    ],
                    "all_id_fields_nonempty_string": True,
                    "all_fields_ending_row_sha256_are_sha256": True,
                    "connected_positive_open_support_member_count_const": 1,
                },
                "full_segment_sign_slice_is_named_endpoint_support": {
                    "const": True,
                },
                "local_corridor_role": {
                    "const": "NONEMPTY_LOCAL_WITNESS_ONLY_NOT_FULL_SIDE_PROOF",
                },
            },
        },
        "closure_limit_side": {
            "json_type": "object",
            "keys_exact": [
                "approach", "active_factor_sign", "strict_p_derivative_sign",
                "limit", "topology", "quantified_base",
                "support_open_base_z_s", "proof_closed_core_base_z_s",
                "strict_sign_corridor_box_t2_p_s",
                "corridor_strictly_inside_R292_open_cell",
                "local_corridor_nonempty_witness_only",
                "full_sign_side_to_rho_support_certificate",
                "exact_full_sign_side_contained_in_R292_support_derived",
            ],
            "fields": {
                "approach": {
                    "enum": [
                        "P_APPROACHES_RHO_FROM_BELOW",
                        "P_APPROACHES_RHO_FROM_ABOVE",
                    ],
                },
                "active_factor_sign": "$ref:strict_sign",
                "strict_p_derivative_sign": "$ref:strict_sign",
                "limit": {"const": "p -> rho(z,s)"},
                "topology": {
                    "const": "relative topology of physical section X",
                },
                "quantified_base": {"const": "PROOF_CLOSED_CORE_ONLY"},
                "support_open_base_z_s": "$ref:rational_base_z_s",
                "proof_closed_core_base_z_s": "$ref:rational_base_z_s",
                "strict_sign_corridor_box_t2_p_s": {
                    "$ref": "rational_box_z_p_s",
                },
                "corridor_strictly_inside_R292_open_cell": {"const": True},
                "local_corridor_nonempty_witness_only": {"const": True},
                "full_sign_side_to_rho_support_certificate": {
                    "$ref": "full_sign_side_to_rho_support_certificate",
                },
                "exact_full_sign_side_contained_in_R292_support_derived": {
                    "const": True,
                },
            },
            "deterministic_corridor_subinterval_recipe": (
                "$ref:deterministic_construction_recipes.oriented_half_corridor"
            ),
        },
        "exact_relative_physical_domain": {
            "json_type": "object",
            "keys_exact": [
                "coordinate_system", "support_open_base_z_s",
                "proof_closed_core_base_B_z_s",
                "owner_contact_closure_base_z_s", "proof_core_inset_rule",
                "proof_core_strictly_inside_R292_open_base",
                "owner_contact_closure_is_zero_credit_full_closure_extension",
                "p_interval", "proof_core_base_area", "B_core_connected",
                "D_equals_B_core_times_closed_p_interval",
                "strict_domain_bounds", "physical_phase_map",
                "Phi_continuous_on_D", "relative_ambient_space",
            ],
            "fields": {
                "coordinate_system": {"const": "(z=t^2,p,s)"},
                "support_open_base_z_s": "$ref:rational_base_z_s",
                "proof_closed_core_base_B_z_s": "$ref:rational_base_z_s",
                "owner_contact_closure_base_z_s": "$ref:rational_base_z_s",
                "proof_core_inset_rule": {
                    "const": "QUARTER_EACH_TANGENT_SIDE",
                    "derived_by": (
                        "$ref:deterministic_construction_recipes."
                        "proof_closed_core_middle_half"
                    ),
                },
                "proof_core_strictly_inside_R292_open_base": {"const": True},
                "owner_contact_closure_is_zero_credit_full_closure_extension": {
                    "const": True,
                },
                "p_interval": {
                    "type": "array[2]<rational>",
                    "derived_by": (
                        "$ref:deterministic_construction_recipes."
                        "targeted_p_bracket_selection"
                    ),
                },
                "proof_core_base_area": "$ref:rational",
                "B_core_connected": {"const": True},
                "D_equals_B_core_times_closed_p_interval": {"const": True},
                "strict_domain_bounds": {
                    "keys_exact": ["0<z<1/2", "-1<p<1"],
                    "all_values_const": True,
                },
                "physical_phase_map": {
                    "keys_exact": ["q", "u", "s"],
                    "values_exact": {
                        "q": "(9/25)n(z)",
                        "u": "sqrt(1-p^2)n(z)+p(-n_y(z),n_x(z))",
                        "s": "s",
                    },
                },
                "Phi_continuous_on_D": {"const": True},
                "relative_ambient_space": {
                    "const": "physical collision section X",
                },
            },
        },
        "relative_limit_lemma_instance": {
            "json_type": "object",
            "keys_exact": [
                "theorem", "proof_core_patch_id", "owner_extension_patch_id",
                "coordinate_map", "relative_chart", "fixed_t_sign",
                "support_open_base_z_s", "proof_closed_core_base_z_s",
                "owner_contact_closure_base_z_s",
                "quantified_attachment_base",
                "owner_extension_is_zero_credit_sidecar_only",
                "graph_bracket_p", "strict_p_derivative", "path_formula",
                "limit_formula", "corridor_box_is_not_Gamma_intersection",
            ],
            "fields": {
                "theorem": {
                    "const": "R305B_RELATIVE_PHYSICAL_P_TO_RHO_ATTACHMENT_V1",
                },
                "proof_core_patch_id": {
                    "prefix": "round305b-proof-core-patch:",
                },
                "owner_extension_patch_id": {
                    "prefix": "round305b-owner-extension-patch:",
                },
                "coordinate_map": {
                    "const": "Phi=(q=(9/25)n,u=sqrt(1-p^2)n+p*(-ny,nx),s)",
                },
                "relative_chart": {"type": "nonempty-string"},
                "fixed_t_sign": {"enum": [-1, 1]},
                "support_open_base_z_s": "$ref:rational_base_z_s",
                "proof_closed_core_base_z_s": "$ref:rational_base_z_s",
                "owner_contact_closure_base_z_s": "$ref:rational_base_z_s",
                "quantified_attachment_base": {
                    "const": "PROOF_CLOSED_CORE_ONLY",
                },
                "owner_extension_is_zero_credit_sidecar_only": {"const": True},
                "graph_bracket_p": {
                    "type": "array[2]<rational>",
                    "derived_by": (
                        "$ref:deterministic_construction_recipes."
                        "targeted_p_bracket_selection"
                    ),
                },
                "strict_p_derivative": "$ref:strict_sign",
                "path_formula": {
                    "const": "p_eps=(1-eps)*p_graph(z,s)+eps*p_face, 0<eps<=1",
                },
                "limit_formula": {
                    "const": "lim_{eps->0+} Phi(z,p_eps,s)=Phi(z,p_graph(z,s),s)",
                },
                "corridor_box_is_not_Gamma_intersection": {"const": True},
            },
        },
        "exact_graph_Gamma_core": {
            "json_type": "object",
            "keys_exact": [
                "definition", "quantified_base", "proof_closed_core_base_z_s",
                "F_identity", "rho_exists_uniquely_on_every_base_fibre",
                "rho_continuous", "rho_range_strictly_inside_p_bracket",
                "Gamma_core_nonempty", "Gamma_core_connected",
                "Gamma_core_included_in_valid_physical_wall_event_lower_stratum",
                "corridor_boxes_disjoint_from_Gamma_core",
                "owner_extension_not_part_of_Gamma_core",
                "relative_limit_lemma_instance",
            ],
            "fields": {
                "definition": {
                    "const": (
                        "Gamma_core={Phi(z,rho(z,s),s):(z,s) in B_core}; "
                        "F(z,rho(z,s),s)=0"
                    ),
                },
                "quantified_base": {"const": "PROOF_CLOSED_CORE_ONLY"},
                "proof_closed_core_base_z_s": "$ref:rational_base_z_s",
                "F_identity": "$ref:active_function_identity",
                "relative_limit_lemma_instance": {
                    "$ref": "relative_limit_lemma_instance",
                },
                "all_other_boolean_fields_const": True,
            },
        },
        "G0": {
            "keys_exact": [
                "satisfied", "Round305A", "Round300A", "Round287_pair",
                "Round275_regions", "anchor_row_ids", "anchor_row_sha256s",
                "all_source_and_derived_rows_content_closed",
            ],
            "fields": {
                "satisfied": {"const": True},
                "Round305A": {"type": "array[2]<source-id,sha256>"},
                "Round300A": {"type": "array[2]<source-id,sha256>"},
                "Round287_pair": {"type": "array[2]<source-id,sha256>"},
                "Round275_regions": {
                    "type": "array[2]<array[2]<source-id,sha256>>",
                    "order": "LEFT Round275 region then RIGHT Round275 region",
                },
                "anchor_row_ids": {
                    "type": "array[2]<round305b-anchor-id>",
                    "order": "LEFT anchor then RIGHT anchor",
                },
                "anchor_row_sha256s": (
                    "array[2]<sha256>; LEFT then RIGHT aligned to anchor_row_ids"
                ),
                "all_source_and_derived_rows_content_closed": {"const": True},
            },
        },
        "G1": {
            "keys_exact": [
                "satisfied", "exact_domain", "attachment_quantifier",
                "proof_core_strictly_inside_both_R292_open_supports",
                "selected_root_discriminant_strict_positive",
                "selected_near_root_strict_future_and_less_than_three",
                "all_competitor_order_outgoing_chart_and_other_dynamic_predicates_strict",
                "only_nonstrict_whole_cell_predicate",
                "both_R292_supports_connected_positive_open_single_cell",
            ],
            "fields": {
                "satisfied": {"const": True},
                "exact_domain": "$ref:exact_relative_physical_domain",
                "attachment_quantifier": {
                    "const": "FOR_ALL_B_IN_PROOF_CLOSED_CORE_ONLY",
                },
                "only_nonstrict_whole_cell_predicate": {
                    "enum": [
                        "wall_endpoint_or_count_transition:X:0",
                        "wall_endpoint_or_count_transition:Y:0",
                    ],
                },
                "all_other_boolean_fields_const": True,
            },
        },
        "G2": {
            "keys_exact": [
                "satisfied", "active_reason", "predicate_details",
                "explicit_wall_value",
                "zero_wall_hard_checked_not_silently_dropped",
                "source_wall_factor_strict_sign",
                "source_wall_factor_uniformly_nonzero_on_proof_core",
                "target_wall_factor_F_identity",
                "wall_event_product_zero_iff_target_F_zero",
                "uniform_strict_dF_dp_sign",
                "proof_core_target_factor_face_replays",
                "proof_core_wall_event_product_face_replays",
                "uniform_opposite_p_face_signs",
                "proof_closed_core_base_z_s", "IVT_unique_continuous_rho",
                "Gamma_core_valid_physical_inclusion_replayed",
            ],
            "fields": {
                "satisfied": {"const": True},
                "active_reason": {
                    "enum": [
                        "wall_endpoint_or_count_transition:X:0",
                        "wall_endpoint_or_count_transition:Y:0",
                    ],
                },
                "predicate_details": "$ref:wall_predicate_details",
                "explicit_wall_value": {"const": 0},
                "source_wall_factor_strict_sign": "$ref:strict_sign",
                "target_wall_factor_F_identity": "$ref:active_function_identity",
                "uniform_strict_dF_dp_sign": "$ref:strict_sign",
                "proof_core_target_factor_face_replays": (
                    "object exact keys left_lower,left_upper,right_lower,right_upper; "
                    "each exact keys active_factor_extremal_signs[2]<strict_sign>,"
                    "signed_support_state in FULL_DESIRED_SIDE_SUPPORT|"
                    "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
                ),
                "proof_core_wall_event_product_face_replays": {
                    "keys_exact": ["lower", "upper"],
                    "values": "$ref:wall_event_product_replay",
                },
                "proof_closed_core_base_z_s": "$ref:rational_base_z_s",
                "all_unlisted_boolean_fields_const": True,
            },
        },
        "G3_or_G4": {
            "keys_exact": [
                "satisfied", "endpoint", "sign_side", "quantified_base",
                "proof_closed_core_base_z_s", "sequence",
                "strict_sign_corridor_box_t2_p_s",
                "full_sign_side_to_rho_support_certificate",
                "full_sign_side_sequence_remains_in_exact_R292_open_support_by_certificate",
                "corridor_used_only_as_local_nonempty_witness",
                "limit_in_relative_physical_space_X", "conclusion",
            ],
            "fields": {
                "satisfied": {"const": True},
                "endpoint": {"type": "source-occurrence-id"},
                "sign_side": "$ref:closure_limit_side",
                "quantified_base": {
                    "const": "FOR_ALL_B_IN_PROOF_CLOSED_CORE_ONLY",
                },
                "proof_closed_core_base_z_s": "$ref:rational_base_z_s",
                "sequence": {
                    "enum": [
                        "Phi(b,p_k), p_k->rho(b), b in B_core, from the LEFT endpoint sign side",
                        "Phi(b,p_k), p_k->rho(b), b in B_core, from the RIGHT endpoint sign side",
                    ],
                },
                "strict_sign_corridor_box_t2_p_s": {
                    "$ref": "rational_box_z_p_s",
                    "derived_by": (
                        "$ref:definitions.closure_limit_side."
                        "deterministic_corridor_subinterval_recipe"
                    ),
                },
                "full_sign_side_to_rho_support_certificate": {
                    "$ref": "full_sign_side_to_rho_support_certificate",
                },
                "full_sign_side_sequence_remains_in_exact_R292_open_support_by_certificate": {
                    "const": True,
                },
                "corridor_used_only_as_local_nonempty_witness": {"const": True},
                "limit_in_relative_physical_space_X": {"const": True},
                "conclusion": {
                    "enum": [
                        "Gamma_core subset cl_X(A_left)",
                        "Gamma_core subset cl_X(A_right)",
                    ],
                },
            },
        },
        "G5": {
            "keys_exact": [
                "satisfied", "active_reason", "predicate_details",
                "explicit_wall_value",
                "zero_wall_hard_checked_not_silently_dropped",
                "whole_open_support_wall_event_product_replay",
                "proof_core_p_face_wall_event_product_replays",
                "source_wall_factor_uniformly_strict_nonzero",
                "wall_event_product_zero_iff_target_F_zero",
                "Gamma_core_is_included_wall_event_not_coordinate_zero_shortcut",
                "R294_occurrence_identity_stage",
                "R304_separate_official_key_materialization_stage",
                "occurrence_identity_collapsed", "official_key_identity_merged",
                "owner_extension_full_closure_sidecar_only",
                "owner_extension_not_Gamma_core_or_G3_G4_or_component_edge_basis",
                "closure_intersection_conclusion",
            ],
            "fields": {
                "satisfied": {"const": True},
                "active_reason": {
                    "enum": [
                        "wall_endpoint_or_count_transition:X:0",
                        "wall_endpoint_or_count_transition:Y:0",
                    ],
                },
                "predicate_details": "$ref:wall_predicate_details",
                "explicit_wall_value": {"const": 0},
                "whole_open_support_wall_event_product_replay": {
                    "$ref": "wall_event_product_replay",
                },
                "proof_core_p_face_wall_event_product_replays": {
                    "keys_exact": ["lower", "upper"],
                    "values": "$ref:wall_event_product_replay",
                },
                "R294_occurrence_identity_stage": {
                    "keys_exact": [
                        "official_key_id_is_null", "official_key_ordinal_is_null",
                        "binding_status",
                        "both_source_rows_equal_exact_R292_component_rows",
                    ],
                    "fields": {
                        "official_key_id_is_null": {"const": True},
                        "official_key_ordinal_is_null": {"const": True},
                        "binding_status": {
                            "const": (
                                "NOT_MATERIALIZED_IN_R287_FROZEN_LEDGER__"
                                "COMPLETE_SIGNATURE_HASH_PINNED"
                            ),
                        },
                        "both_source_rows_equal_exact_R292_component_rows": {
                            "const": True,
                        },
                    },
                },
                "R304_separate_official_key_materialization_stage": {
                    "keys_exact": [
                        "official_key_pair", "member_row_ids", "stages_not_conflated",
                    ],
                    "fields": {
                        "official_key_pair": "sorted-array[2]<official-key-id>",
                        "member_row_ids": "array[2]<Round304-member-row-id>",
                        "member_row_ids_order": "LEFT anchor then RIGHT anchor",
                        "stages_not_conflated": {"const": True},
                    },
                },
                "occurrence_identity_collapsed": {"const": False},
                "official_key_identity_merged": {"const": False},
                "closure_intersection_conclusion": {
                    "const": (
                        "Gamma_core subset cl_X(A_left) intersect cl_X(A_right)"
                    ),
                },
                "all_unlisted_boolean_fields_const": True,
            },
        },
    },
    "base_role_separation": {
        "support_open_base_z_s": (
            "open R292 endpoint-support base; endpoints encode its closure but "
            "are not quantified by G3/G4"
        ),
        "proof_closed_core_base_z_s": (
            "deterministic quarter inset in z and s; sole B_core quantified by "
            "the formal witness, Gamma_core, lemma, G2, G3, and G4"
        ),
        "owner_contact_closure_base_z_s": (
            "full-closure unique-root extension used only by zero-credit owner/contact "
            "sidecars; never a Gamma_core contact, attachment, or edge basis"
        ),
    },
    "deterministic_construction_recipes": {
        "proof_closed_core_middle_half": {
            "input": (
                "support_open_base_z_s=[z0,z1,s0,s1] with z0<z1 and s0<s1"
            ),
            "formula": [
                "zc0=z0+(z1-z0)/4",
                "zc1=z1-(z1-z0)/4",
                "sc0=s0+(s1-s0)/4",
                "sc1=s1-(s1-s0)/4",
            ],
            "output": "proof_closed_core_base_z_s=[zc0,zc1,sc0,sc1]",
            "p_coordinate_is_not_part_of_the_base_inset": True,
        },
        "targeted_p_bracket_selection": {
            "input_full_open_p_interval": "[L,U] with L<U; w=U-L",
            "depth_iteration_order": [1, 2],
            "for_each_depth_d": {
                "LOWER_outer_slice": "[L,L+w/2^d]",
                "UPPER_outer_slice": "[U-w/2^d,U]",
                "middle_half_function": (
                    "middle_half([x,y])=[x+(y-x)/4,y-(y-x)/4]"
                ),
                "I_lower": "middle_half(LOWER_outer_slice)=[a_l,b_l]",
                "I_upper": "middle_half(UPPER_outer_slice)=[a_u,b_u]",
                "lower_face": "m_l=(a_l+b_l)/2",
                "upper_face": "m_u=(a_u+b_u)/2",
                "candidate_p_bracket": "[m_l,m_u]",
            },
            "first_feasible_depth_rule": (
                "select the first d in [1,2] for which the two endpoint supports "
                "are complementary on I_lower and I_upper, all four exact "
                "B_core p-face extremal signs are strict, the full-base face "
                "support states equal the B_core face states, and the explicit "
                "wall-product p-face signs are strict and consistent"
            ),
            "output": (
                "bracket_slice_depth=d, lower_interval=I_lower, "
                "upper_interval=I_upper, lower_p=m_l, upper_p=m_u"
            ),
            "selection_only": (
                "this recipe fixes wire bytes and IDs; interval signs and all "
                "geometry predicates must still be independently recomputed"
            ),
        },
        "direct_geometry_reconstruction_summary": {
            "input_rows": (
                "all 1024 sealed R305A residual rows in canonical occurrence-"
                "pair order, with the common LEFT=RIGHT R292 box encoded as "
                "[z0,z1,p0,p1,s0,s1]"
            ),
            "chart_transition_histogram_key": (
                "source_cell + ('+' iff source_guard_t_lower>0 else '-') + "
                "'->' + adjacent_cell + ('+' iff physical_t_sign=1 else '-'); "
                "source_cell and adjacent_cell are the substrings after the "
                "first ':' in the exact Round275 source_chart and adjacent_chart"
            ),
            "active_function_and_image_sign_histogram_key": (
                "active_function_id + '|' + decimal physical_t_sign, where "
                "physical_t_sign is exactly -1 or 1"
            ),
            "target_factor_derivative_histogram_key": (
                "strict derivative signs in exact coordinate order t,p,s joined "
                "by '|'; each token is STRICT_NEGATIVE or STRICT_POSITIVE"
            ),
            "minimum_z": "minimum of common R292 box z0 over all 1024 rows",
            "maximum_z": "maximum of common R292 box z1 over all 1024 rows",
            "histogram_object_order": "keys sorted lexicographically",
            "rational_output_rule": "$ref:definitions.rational.normal_form",
        },
        "oriented_half_corridor": {
            "LOWER_input": "I_lower=[a_l,b_l], lower_face=m_l=(a_l+b_l)/2",
            "UPPER_input": "I_upper=[a_u,b_u], upper_face=m_u=(a_u+b_u)/2",
            "LOWER_owner_corridor_p_interval": "[m_l,b_l]",
            "UPPER_owner_corridor_p_interval": "[a_u,m_u]",
            "corridor_z_s_intervals": (
                "exactly proof_closed_core_base_z_s in z,s coordinate order"
            ),
            "role": (
                "strict sign-side and nonintersection evidence only; a corridor "
                "is not Gamma_core, not an attachment witness, and not a "
                "component-edge basis"
            ),
        },
        "signed_t_outward_dyadic_enclosure": {
            "precision_bits": 512,
            "sqrt_endpoint_algorithm_for_nonnegative_rational_r=N/D": [
                "scale=2^512",
                "scaled=N*scale^2",
                "q=floor(scaled/D)",
                "k=integer_isqrt(q)",
                "adjust k until k^2*D<=scaled<(k+1)^2*D",
                "sqrt_lower=k/scale",
                "sqrt_upper=k/scale if k^2*D==scaled else (k+1)/scale",
            ],
            "z_interval_input": "[z_lo,z_hi] with 0<z_lo<=z_hi",
            "physical_t_sign_positive_output": (
                "[sqrt_lower(z_lo),sqrt_upper(z_hi)]"
            ),
            "physical_t_sign_negative_output": (
                "[-sqrt_upper(z_hi),-sqrt_lower(z_lo)]"
            ),
            "exact_square_rule": "do not add one ulp when the endpoint is exact",
            "selection_only": (
                "this recipe fixes emitted rational t-box bytes; Arb interval "
                "geometry and signs must still be independently recomputed"
            ),
        },
        "owner_contact_full_closure_sidecar": {
            "patch_group_key": "[active_function_id,physical_t_sign]",
            "patch_group_count_and_size": "8 groups, exactly 128 patches per group",
            "patch_base": "owner_contact_closure_base_z_s",
            "pair_enumeration": (
                "all unordered distinct patch pairs within one group; associated "
                "witness IDs and owner-extension patch IDs each sorted lexicographically"
            ),
            "contact_selection": (
                "retain exactly pairs whose closed z,s rectangles intersect only "
                "on a boundary: each axis intersection is nonempty and the number "
                "of positive-length intersection axes is 0 or 1"
            ),
            "contact_base": (
                "coordinatewise closed intersection [max lowers,min uppers] in z,s"
            ),
            "contact_p_hull": (
                "[minimum patch bracket lower,maximum patch bracket upper]"
            ),
            "contact_kind": {
                "base_dimension_1": "OWNER_EXTENSION_BASE_FACE_CONTACT",
                "base_dimension_0": (
                    "OWNER_EXTENSION_FOUR_PATCH_VERTEX_DIAGONAL_PAIR"
                ),
            },
            "face_owner": (
                "one FACE_RELATIVE_INTERIOR owner per dimension-1 contact; its "
                "incident arrays contain that pair/contact and its endpoint "
                "override list contains every existing global vertex owner at "
                "the two closed-face endpoints"
            ),
            "vertex_owner": (
                "globally aggregate by [group key,exact point]; start from every "
                "dimension-0 diagonal contact, then add every incident face-contact "
                "pair at that endpoint; require exactly 4 extension patches, 4 "
                "associated witnesses, and 6 contacts"
            ),
            "lexicographic_owner": (
                "minimum sorted global_incident_owner_extension_patch_ids"
            ),
            "all_emitted_id_arrays": "sorted unique lexicographically",
            "credit": (
                "zero-credit full-closure extension sidecar only; never Gamma_core, "
                "G3/G4, attachment, or component-edge basis"
            ),
        },
    },
    "embedded_result_objects": {
        "two_sided_attachment_theorem": TWO_SIDED_ATTACHMENT_THEOREM,
        "relative_physical_closure_limit_lemma":
            RELATIVE_PHYSICAL_CLOSURE_LIMIT_LEMMA,
    },
    "schema_snapshot_contract": {
        "keys_exact_in_construction_order": [
            "schema", "physical_witness_row_keys", "anchor_row_keys",
            "closure_contact_row_keys", "owner_locus_row_keys",
            "component_edge_row_keys", "expected_counts",
            "official_key_contract", "D4_transfer_enabled",
            "D4_direct_row_instantiation_required", "theorem",
            "normative_wire_spec",
        ],
        "construction": {
            "schema": SCHEMA,
            "physical_witness_row_keys": list(PHYSICAL_WITNESS_KEYS),
            "anchor_row_keys": list(ANCHOR_KEYS),
            "closure_contact_row_keys": list(CLOSURE_CONTACT_KEYS),
            "owner_locus_row_keys": list(OWNER_LOCUS_KEYS),
            "component_edge_row_keys": list(COMPONENT_EDGE_KEYS),
            "expected_counts": {
                "physical_witness_rows": 1024,
                "anchor_rows": 2048,
                "closure_contact_rows": 3536,
                "owner_locus_rows": 2696,
                "canonical_component_edge_rows": 8,
                "witnesses_per_component_edge": 128,
                "formal_DSU_rank_reductions_in_Round305B": 0,
                "maximum_later_fresh_DSU_rank_reductions": 8,
            },
            "official_key_contract": {
                "complete_Round304_official_key_count": 124,
                "residual_official_key_count": 16,
                "all_1024_residual_pairs_cross_official_key": True,
                "physical_component_edge_across_keys_permitted_when_G0_G5": True,
                "occurrence_identity_merge_credit": 0,
                "official_key_identity_merge_credit": 0,
            },
            "D4_transfer_enabled": False,
            "D4_direct_row_instantiation_required": 1024,
            "theorem": "$ref:embedded_result_objects.two_sided_attachment_theorem",
            "normative_wire_spec": "$self:entire WIRE_SPEC object",
        },
        "sha256_rule": "sha256(canonical_json(exact constructed object))",
    },
    "id_domains": {
        "active_function_id": {
            "prefix": "round300b-active-function:",
            "sha256_of_canonical_json": (
                "the exact dynamic active_function_identity value whose shape is "
                "$ref:definitions.active_function_identity"
            ),
        },
        "proof_core_patch_id": {
            "prefix": "round305b-proof-core-patch:",
            "sha256_of_canonical_json": [
                "ROUND305B_DIRECT_PROOF_CORE_P_GRAPH_PATCH_V1",
                {
                    "scope_row_sha256": "sha256",
                    "pair": "canonical sorted occurrence pair",
                    "active_function_id": "$ref:id_domains.active_function_id",
                    "fixed_physical_t_sign": "-1|1",
                    "proof_closed_core_base_z_s": "rational_base_z_s",
                    "p_bracket": {
                        "shape": "array[2]<rational>",
                        "derived_by": (
                            "$ref:deterministic_construction_recipes."
                            "targeted_p_bracket_selection"
                        ),
                    },
                },
            ],
        },
        "owner_extension_patch_id": {
            "prefix": "round305b-owner-extension-patch:",
            "sha256_of_canonical_json": [
                "ROUND305B_ZERO_CREDIT_FULL_CLOSURE_ROOT_EXTENSION_PATCH_V1",
                {
                    "scope_row_sha256": "sha256",
                    "pair": "canonical sorted occurrence pair",
                    "active_function_id": "$ref:id_domains.active_function_id",
                    "fixed_physical_t_sign": "-1|1",
                    "owner_contact_closure_base_z_s": "rational_base_z_s",
                    "p_bracket": {
                        "shape": "array[2]<rational>",
                        "derived_by": (
                            "$ref:deterministic_construction_recipes."
                            "targeted_p_bracket_selection"
                        ),
                    },
                    "formal_credit": 0,
                },
            ],
        },
        "physical_witness_row_id": {
            "prefix": "round305b-physical-witness:",
            "sha256_of_canonical_json": [
                "ROUND305B_TWO_SIDED_P_ATTACHMENT_V1",
                "proof_core_patch_id", "scope_row_sha256",
            ],
        },
        "relative_limit_lemma_id": {
            "prefix": "round305b-relative-p-limit:",
            "sha256_of_canonical_json": "relative_limit_lemma_instance",
        },
        "full_sign_side_support_certificate_id": {
            "prefix": "round305b-full-sign-side-support:",
            "sha256_of_canonical_json": [
                "ROUND305B_FULL_SIGN_SIDE_TO_RHO_NAMED_SUPPORT_V1",
                "certificate object with certificate_id absent",
            ],
        },
        "anchor_row_id": {
            "prefix": "round305b-anchor:",
            "sha256_of_canonical_json": [
                "ROUND305B_R292_SINGLE_CELL_FULL_SIGN_SIDE_ANCHOR_V2",
                "physical_witness_row_id", "side", "endpoint_occurrence_id",
                "R292_cell_row_sha256", "R294_row_sha256",
                "Round304_member_row_sha256", "relative_limit_lemma_id",
                "full_sign_side_support_certificate_id",
            ],
        },
        "branch_id": {
            "prefix": "round305b-target-zero-branch:",
            "sha256_of_canonical_json": [
                "source_Round287_pair_row_id", "active_reason",
                "active_function_id",
            ],
        },
        "closure_contact_row_id": {
            "prefix": "round305b-closure-contact:",
            "sha256_of_canonical_json": [
                "ROUND305B_PAIRWISE_OWNER_EXTENSION_CLOSURE_CONTACT_V1",
                "sorted owner-extension patch id pair",
                "exact_common_base_z_s", "common_p_bracket_hull",
            ],
        },
        "vertex_owner_locus_row_id": {
            "prefix": "round305b-owner-locus:",
            "sha256_of_canonical_json": [
                "ROUND305B_GLOBAL_OWNER_EXTENSION_VERTEX_LOCUS_V1",
                "[active_function_id,physical_t_sign]", "exact_locus_base_z_s",
            ],
        },
        "face_owner_locus_row_id": {
            "prefix": "round305b-owner-locus:",
            "sha256_of_canonical_json": [
                "ROUND305B_OWNER_EXTENSION_FACE_RELATIVE_INTERIOR_LOCUS_V1",
                "[active_function_id,physical_t_sign]", "exact_locus_base_z_s",
                "closure_contact_row_id",
            ],
        },
        "canonical_component_edge_row_id": {
            "prefix": "round305b-canonical-component-edge:",
            "sha256_of_canonical_json": [
                "ROUND305B_G0_G5_DEDUP_COMPONENT_EDGE_V1",
                "canonical Round304 component pair",
                "sha256(canonical(sorted witness row ids))",
                "sha256(canonical(witness row hashes in the same order))",
            ],
        },
    },
    "row_types": {
        "physical": {
            "keys_exact_in_construction_order": list(PHYSICAL_WITNESS_KEYS),
            "schema_const": SCHEMA + ".physical-witness-row.v1",
            "id_field": "Round305B_physical_witness_row_id",
            "id_domain": "$ref:id_domains.physical_witness_row_id",
            "sha256_fields": [
                "source_Round305A_scope_reprojection_row_sha256",
                "source_Round300A_row_sha256",
            ],
            "sorted_pair_fields_length_2": [
                "canonical_registry_occurrence_pair",
                "Round304_final_component_pair", "official_key_pair",
            ],
            "id_array_hash_array_pairs": {
                "anchors": {
                    "fields": ["anchor_row_ids", "anchor_row_sha256s"],
                    "order": "LEFT anchor then RIGHT anchor; hashes aligned",
                },
                "contacts": {
                    "fields": [
                        "closure_contact_row_ids",
                        "closure_contact_row_sha256s",
                    ],
                    "order": (
                        "strict lexicographic closure_contact_row_id order; "
                        "hashes aligned"
                    ),
                },
                "owners": {
                    "fields": ["owner_locus_row_ids", "owner_locus_row_sha256s"],
                    "order": (
                        "strict lexicographic owner_locus_row_id order; hashes aligned"
                    ),
                },
            },
            "nested_fields": {
                "exact_relative_physical_domain": (
                    "$ref:exact_relative_physical_domain"
                ),
                "exact_graph_Gamma": "$ref:exact_graph_Gamma_core",
                "G0_exact_provenance_pins_and_row_closures": "$ref:G0",
                "G1_endpoint_occurrence_connected_supports": "$ref:G1",
                "G2_nonempty_connected_included_lower_stratum": "$ref:G2",
                "G3_left_closure_attaches_to_included_patch": "$ref:G3_or_G4",
                "G4_right_closure_attaches_to_included_patch": "$ref:G3_or_G4",
                "G5_endpoint_patch_provenance_exactly_closed": "$ref:G5",
            },
            "constant_fields": {
                "cross_official_key_physical_edge_permitted": True,
                "occurrence_identity_collapsed": False,
                "official_key_identity_merged": False,
                "owner_extension_sidecar_not_Gamma_core_or_attachment_or_edge_basis":
                    True,
                "corridor_box_used_as_Gamma_intersection": False,
                "D4_transfer_used": False,
                "candidate_physical_connectivity_conclusion": True,
                "formal_physical_witness_credit": 1,
                "formal_component_edge_credit": 0,
                "formal_DSU_rank_reduction_credit": 0,
                "formal_maximality_credit": 0,
                "formal_fibre_credit": 0,
                "formal_global_disposition_credit": 0,
            },
        },
        "anchor": {
            "keys_exact_in_construction_order": list(ANCHOR_KEYS),
            "schema_const": SCHEMA + ".anchor-row.v1",
            "id_field": "Round305B_anchor_row_id",
            "id_domain": "$ref:id_domains.anchor_row_id",
            "side_enum": ["LEFT", "RIGHT"],
            "nullable_fields_exact_null": [
                "R294_official_key_id", "R294_official_key_ordinal",
            ],
            "binding_status_const": (
                "NOT_MATERIALIZED_IN_R287_FROZEN_LEDGER__"
                "COMPLETE_SIGNATURE_HASH_PINNED"
            ),
            "nested_fields": {
                "relative_physical_closure_limit_side": "$ref:closure_limit_side",
            },
            "constant_fields": {
                "connected_positive_open_support_nonempty": True,
                "connected_positive_open_support_member_count": 1,
                "formal_anchor_binding_credit": 1,
                "formal_occurrence_identity_collapse_credit": 0,
                "formal_official_key_merge_credit": 0,
            },
            "all_fields_ending_row_sha256_are_sha256": True,
        },
        "contact": {
            "keys_exact_in_construction_order": list(CLOSURE_CONTACT_KEYS),
            "schema_const": SCHEMA + ".closure-contact-row.v1",
            "id_field": "Round305B_closure_contact_row_id",
            "id_domain": "$ref:id_domains.closure_contact_row_id",
            "construction_recipe": (
                "$ref:deterministic_construction_recipes."
                "owner_contact_full_closure_sidecar"
            ),
            "associated_physical_witness_row_ids": (
                "sorted unique array[2]; association only, not contact basis"
            ),
            "contact_pair_owner_extension_patch_ids": (
                "sorted unique array[2]; sole patch-contact basis"
            ),
            "contact_kind_by_base_dimension": {
                "1": "OWNER_EXTENSION_BASE_FACE_CONTACT",
                "0": "OWNER_EXTENSION_FOUR_PATCH_VERTEX_DIAGONAL_PAIR",
            },
            "exact_common_base_z_s": "$ref:rational_base_z_s",
            "common_p_bracket_hull": "array[2]<rational>",
            "strict_common_active_function_p_derivative_sign": "$ref:strict_sign",
            "constant_fields": {
                "owner_extension_root_unique_on_full_closure": True,
                "full_closure_extension_only": True,
                "not_Gamma_core_contact": True,
                "not_G3_G4_or_component_edge_basis": True,
                "D4_transfer_used": False,
            },
        },
        "owner": {
            "keys_exact_in_construction_order": list(OWNER_LOCUS_KEYS),
            "schema_const": SCHEMA + ".owner-locus-row.v1",
            "id_field": "Round305B_owner_locus_row_id",
            "construction_recipe": (
                "$ref:deterministic_construction_recipes."
                "owner_contact_full_closure_sidecar"
            ),
            "id_domain_by_locus_kind": {
                "FACE_RELATIVE_INTERIOR": "$ref:id_domains.face_owner_locus_row_id",
                "FOUR_PATCH_VERTEX": "$ref:id_domains.vertex_owner_locus_row_id",
            },
            "exact_locus_base_z_s": "$ref:rational_base_z_s",
            "incidence_by_locus_kind": {
                "FACE_RELATIVE_INTERIOR": {
                    "associated_witness_count": 2,
                    "owner_extension_patch_count": 2,
                    "incident_contact_count": 1,
                    "vertex_override_count": "0|1|2",
                },
                "FOUR_PATCH_VERTEX": {
                    "associated_witness_count": 4,
                    "owner_extension_patch_count": 4,
                    "incident_contact_count": 6,
                    "vertex_override_count": 0,
                },
            },
            "all_id_arrays_sorted_unique": True,
            "lexicographic_owner": (
                "minimum(global_incident_owner_extension_patch_ids)"
            ),
            "constant_fields": {
                "full_closure_extension_only": True,
                "not_Gamma_core_locus": True,
                "not_G3_G4_or_component_edge_basis": True,
                "D4_transfer_used": False,
            },
        },
        "edge": {
            "keys_exact_in_construction_order": list(COMPONENT_EDGE_KEYS),
            "schema_const": SCHEMA + ".canonical-component-edge-row.v1",
            "id_field": "Round305B_canonical_component_edge_row_id",
            "id_domain": "$ref:id_domains.canonical_component_edge_row_id",
            "physical_witness_row_count_const": 128,
            "canonical_Round304_final_component_pair": (
                "sorted unique array[2]<Round304-final-component-id>"
            ),
            "canonical_official_key_pair": (
                "sorted unique array[2]<Round304-official-key-id>"
            ),
            "digest_fields": [
                "physical_witness_row_ids_sha256",
                "physical_witness_row_sha256s_sha256",
                "canonical_occurrence_pairs_sha256",
            ],
            "digest_recipes": {
                "physical_witness_row_ids_sha256": (
                    "sha256(canonical_json(128 witness ids sorted lexicographically))"
                ),
                "physical_witness_row_sha256s_sha256": (
                    "sha256(canonical_json(128 witness row hashes aligned to the "
                    "same sorted witness-id order))"
                ),
                "canonical_occurrence_pairs_sha256": (
                    "sha256(canonical_json(128 canonical occurrence-id pairs, each "
                    "pair internally sorted and the pair list sorted lexicographically))"
                ),
            },
            "constant_fields": {
                "cross_official_key_physical_edge_permitted": True,
                "occurrence_identity_collapsed": False,
                "official_key_identity_merged": False,
                "all_128_witnesses_satisfy_G0_G5": True,
                "deduplicated_from_witness_rows_not_union_rows": True,
                "formal_component_edge_credit": 1,
                "eligible_for_later_fresh_DSU_application": True,
                "formal_DSU_rank_reduction_credit": 0,
            },
        },
    },
    "row_closure": {
        "rule": (
            "row_sha256 = sha256(canonical_json(row object with the "
            "row_sha256 member absent))"
        ),
        "self_hash_member_excluded_exactly_once": True,
        "row_sha256_is_last_construction_member_but_canonical_sort_ignores_order":
            True,
    },
    "ledger": {
        "keys_exact_in_construction_order": [
            "schema", "status", "row_count", "rows_sha256",
            "row_ids_sha256", "row_hashes_sha256",
            "every_row_closed_by_own_sha256", "formal_credit", "rows",
            "ledger_sha256",
        ],
        "schemas_by_type": {
            "physical": SCHEMA + ".physical-witness-ledger.v1",
            "anchor": SCHEMA + ".anchor-ledger.v1",
            "contact": SCHEMA + ".closure-contact-ledger.v1",
            "owner": SCHEMA + ".owner-locus-ledger.v1",
            "edge": SCHEMA + ".canonical-component-edge-ledger.v1",
        },
        "status_const": (
            "PASS_ZERO_CREDIT_CANDIDATE_LEDGER__PUBLISHED_OR_STAGED__"
            "PENDING_INDEPENDENT_VERIFICATION"
        ),
        "rows_order": "strict ascending lexicographic row id",
        "row_count_rule": "len(rows)",
        "rows_sha256_rule": "sha256(canonical_json(rows))",
        "row_ids_sha256_rule": (
            "sha256(canonical_json(row ids in rows order))"
        ),
        "row_hashes_sha256_rule": (
            "sha256(canonical_json(row_sha256 values in rows order))"
        ),
        "every_row_closed_by_own_sha256_const": True,
        "formal_credit_const": 0,
        "ledger_sha256_rule": (
            "sha256(canonical_json(ledger object with ledger_sha256 absent))"
        ),
    },
    "result": {
        "keys_exact_in_construction_order": [
            "schema", "status", "producer_source_filename",
            "producer_source_sha256", "schema_snapshot",
            "schema_snapshot_sha256", "two_sided_attachment_theorem",
            "two_sided_attachment_theorem_sha256",
            "relative_physical_closure_limit_lemma",
            "relative_physical_closure_limit_lemma_sha256",
            "normative_wire_file_commitments",
            "direct_geometry_reconstruction",
            "formal_G0_G5_witness_candidate_count",
            "exact_anchor_candidate_count", "closure_contact_sidecar_count",
            "global_owner_locus_sidecar_count",
            "canonical_component_edge_candidate_count",
            "witnesses_per_component_edge", "owner_audit",
            "ledger_object_commitments", "strict_credit_boundary",
            "conditional_later_fresh_DSU_effect",
            "zero_credit_candidate_publication_permitted", "manifest_emitted",
            "candidate_file_commitments", "result_sha256",
        ],
        "schema_const": SCHEMA + ".zero-credit-candidate-result.v1",
        "status_const": (
            "PASS_ROUND305B_DIRECT_G0_G5_ZERO_CREDIT_CANDIDATE__"
            "PENDING_INDEPENDENT_VERIFICATION__"
            "ZERO_OFFICIALLY_ADMITTED_CREDIT"
        ),
        "producer_source_filename_const": PRODUCER_FILENAME,
        "producer_source_sha256_type": "$ref:sha256",
        "schema_snapshot_rule": "$ref:schema_snapshot_contract",
        "schema_snapshot_sha256_rule": "sha256(canonical_json(schema_snapshot))",
        "two_sided_attachment_theorem_rule": (
            "$ref:embedded_result_objects.two_sided_attachment_theorem"
        ),
        "two_sided_attachment_theorem_sha256_rule": (
            "sha256(canonical_json(two_sided_attachment_theorem))"
        ),
        "relative_physical_closure_limit_lemma_rule": (
            "$ref:embedded_result_objects.relative_physical_closure_limit_lemma"
        ),
        "relative_physical_closure_limit_lemma_sha256_rule": (
            "sha256(canonical_json(relative_physical_closure_limit_lemma))"
        ),
        "runtime_closure_path_free_keys_exact": [
            "python_implementation", "python_version", "python_flint_version",
            "zlib_runtime_version", "arb_precision_bits",
            "loader", "loader_scope", "runtime_source_sha256_pins",
            "runtime_source_module_count",
            "project_local_formal_geometry_module_pycache_reads",
            "project_local_formal_geometry_module_pycache_writes",
            "project_local_formal_geometry_source_compile_exec",
            "same_mtime_same_size_stale_pyc_attack_rejected",
            "stale_pyc_attack_probe_temporary_pyc_written",
            "stale_pyc_attack_probe_temporary_pyc_read",
            "stale_pyc_attack_probe_temporary_pyc_removed",
            "external_flint_imported_via_standard_importlib",
            "external_flint_outside_six_module_direct_source_graph",
            "global_no_pyc_claim_made",
            "R273_R274_imported_or_executed", "floating_point_fallback_used",
        ],
        "runtime_closure_values": {
            "python_implementation": "CPython",
            "python_version": "3.12.3",
            "python_flint_version": "0.9.0",
            "zlib_runtime_version": "1.3",
            "arb_precision_bits": 768,
            "loader": "SHA256_VERIFIED_SOURCE_BYTES_COMPILE_EXEC",
            "loader_scope": "SIX_PINNED_PROJECT_LOCAL_FORMAL_GEOMETRY_MODULES_ONLY",
            "runtime_source_sha256_pins": {
                module_name: expected_sha256
                for module_name, _filename, expected_sha256
                in CACHELESS_RUNTIME_SOURCE_MODULES
            },
            "runtime_source_module_count": 6,
            "project_local_formal_geometry_module_pycache_reads": False,
            "project_local_formal_geometry_module_pycache_writes": False,
            "project_local_formal_geometry_source_compile_exec": True,
            "same_mtime_same_size_stale_pyc_attack_rejected": True,
            "stale_pyc_attack_probe_temporary_pyc_written": True,
            "stale_pyc_attack_probe_temporary_pyc_read": True,
            "stale_pyc_attack_probe_temporary_pyc_removed": True,
            "external_flint_imported_via_standard_importlib": True,
            "external_flint_outside_six_module_direct_source_graph": True,
            "global_no_pyc_claim_made": False,
            "R273_R274_imported_or_executed": False,
            "floating_point_fallback_used": False,
        },
        "absolute_paths_forbidden_recursively": True,
        "direct_geometry_reconstruction": {
            "keys_exact": [
                "status", "runtime_closure", "direct_row_count",
                "R292_anchor_count",
                "R292_single_member_component_count",
                "left_right_identical_R292_cell_pair_count",
                "candidate_piece_pair_count", "serializer_attempt_count",
                "implicit_graph_axis_histogram",
                "tangent_refinement_depth_histogram",
                "bracket_slice_depth_histogram", "chart_transition_histogram",
                "active_function_and_image_sign_histogram",
                "discarded_source_factor_sign_histogram",
                "target_factor_derivative_histogram",
                "only_unresolved_dynamic_predicate_histogram",
                "minimum_z", "maximum_z",
                "maximum_z_strictly_below_one_half", "D4_transfer_enabled",
                "formal_Round305B_credit",
            ],
            "status_const": (
                "PASS_DIRECT_SCOPE_TO_R292_SINGLE_CELL_TO_DEPTH_1_2_P_BRACKET_"
                "RECONSTRUCTION__NO_OUTPUT__ZERO_CREDIT"
            ),
            "internal_direct_record_ids_rows_and_hashes_not_committed": True,
            "count_values": {
                "direct_row_count": 1024,
                "R292_anchor_count": 2048,
                "R292_single_member_component_count": 2048,
                "left_right_identical_R292_cell_pair_count": 1024,
                "candidate_piece_pair_count": 1024,
                "serializer_attempt_count": 1024,
            },
            "histogram_shapes": {
                "implicit_graph_axis_histogram": {"p": 1024},
                "tangent_refinement_depth_histogram": {"0": 1024},
                "bracket_slice_depth_histogram": {"1": 320, "2": 704},
                "chart_transition_histogram": (
                    "object exactly 8 keys derived by $ref:deterministic_"
                    "construction_recipes.direct_geometry_reconstruction_"
                    "summary.chart_transition_histogram_key, each value 128"
                ),
                "active_function_and_image_sign_histogram": (
                    "object exactly 8 keys derived by $ref:deterministic_"
                    "construction_recipes.direct_geometry_reconstruction_"
                    "summary.active_function_and_image_sign_histogram_key, "
                    "each value 128"
                ),
                "discarded_source_factor_sign_histogram": (
                    "keys subset of strict_sign vocabulary; integer counts sum 1024"
                ),
                "target_factor_derivative_histogram": (
                    "keys derived by $ref:deterministic_construction_recipes."
                    "direct_geometry_reconstruction_summary.target_factor_"
                    "derivative_histogram_key; integer counts sum 1024"
                ),
                "only_unresolved_dynamic_predicate_histogram": (
                    "keys from active_reason vocabulary; integer counts sum 1024"
                ),
            },
            "minimum_z": (
                "$ref:deterministic_construction_recipes.direct_geometry_"
                "reconstruction_summary.minimum_z"
            ),
            "maximum_z": (
                "$ref:deterministic_construction_recipes.direct_geometry_"
                "reconstruction_summary.maximum_z"
            ),
            "maximum_z_strictly_below_one_half_const": True,
            "D4_transfer_enabled_const": False,
            "formal_Round305B_credit_const": 0,
        },
        "owner_audit": {
            "keys_exact": [
                "within_group_base_relation_histogram",
                "closure_contact_count", "closure_contact_kind_histogram",
                "closure_contact_base_dimension_histogram",
                "closure_contact_derivative_histogram", "owner_locus_count",
                "owner_locus_kind_histogram",
                "face_to_vertex_override_reference_count",
                "vertex_incident_contact_reference_count",
                "patch_contact_degree_histogram",
                "global_four_patch_vertex_owner_replayed",
                "old_pairwise_minimum_owner_rejected",
                "owner_extension_full_closure_sidecar_only",
                "owner_extension_not_Gamma_core_contact_or_G3_G4_or_edge_basis",
            ],
            "exact_histograms": {
                "within_group_base_relation_histogram": {
                    "BOUNDARY_ONLY_CONTACT": 3536,
                    "DISJOINT": 61488,
                },
                "closure_contact_kind_histogram": {
                    "OWNER_EXTENSION_BASE_FACE_CONTACT": 1856,
                    "OWNER_EXTENSION_FOUR_PATCH_VERTEX_DIAGONAL_PAIR": 1680,
                },
                "closure_contact_base_dimension_histogram": {
                    "0": 1680, "1": 1856,
                },
                "owner_locus_kind_histogram": {
                    "FACE_RELATIVE_INTERIOR": 1856,
                    "FOUR_PATCH_VERTEX": 840,
                },
                "patch_contact_degree_histogram": {
                    "3": 32, "5": 320, "8": 672,
                },
            },
            "count_values": {
                "closure_contact_count": 3536,
                "owner_locus_count": 2696,
                "face_to_vertex_override_reference_count": 3360,
                "vertex_incident_contact_reference_count": 5040,
            },
            "closure_contact_derivative_histogram": (
                "keys subset of strict_sign vocabulary; integer counts sum 3536"
            ),
            "all_boolean_fields_const": True,
        },
        "normative_wire_file_commitments": {
            "keys_exact": ["wire_spec", "wire_contract_fixture"],
            "entry_keys_exact": ["filename", "file_sha256", "file_size_bytes"],
            "filenames_by_key": {
                "wire_spec": WIRE_SPEC_FILENAME,
                "wire_contract_fixture": WIRE_CONTRACT_FIXTURE_FILENAME,
            },
            "file_sha256_type": "$ref:sha256",
            "file_size_bytes_type": "positive-integer",
            "candidate_output_commitment": False,
        },
        "ledger_object_commitments": {
            "keys_exact": ["physical", "anchor", "contact", "owner", "edge"],
            "entry_keys_exact": [
                "filename", "ledger_sha256", "rows_sha256",
                "row_ids_sha256", "row_hashes_sha256",
            ],
            "filenames_by_key": {
                "physical": PREFIX + "_physical_witness_ledger.json.gz",
                "anchor": PREFIX + "_anchor_ledger.json.gz",
                "contact": PREFIX + "_closure_contact_ledger.json.gz",
                "owner": PREFIX + "_owner_locus_ledger.json.gz",
                "edge": PREFIX + "_canonical_component_edge_ledger.json.gz",
            },
            "all_commitment_fields_ending_sha256_are_sha256": True,
        },
        "candidate_file_commitments": {
            "keys_exact": ["physical", "anchor", "contact", "owner", "edge"],
            "entry_keys_exact": [
                "filename", "file_sha256", "file_size_bytes", "compression",
            ],
            "filenames_by_key": {
                "physical": PREFIX + "_physical_witness_ledger.json.gz",
                "anchor": PREFIX + "_anchor_ledger.json.gz",
                "contact": PREFIX + "_closure_contact_ledger.json.gz",
                "owner": PREFIX + "_owner_locus_ledger.json.gz",
                "edge": PREFIX + "_canonical_component_edge_ledger.json.gz",
            },
            "file_sha256_type": "$ref:sha256",
            "file_size_bytes_type": "positive-integer",
            "compression_const": (
                "deterministic-gzip-level-9-mtime-0-empty-name-os-255"
            ),
            "result_file_is_deliberately_not_self_committed": True,
        },
        "count_values": {
            "formal_G0_G5_witness_candidate_count": 1024,
            "exact_anchor_candidate_count": 2048,
            "closure_contact_sidecar_count": 3536,
            "global_owner_locus_sidecar_count": 2696,
            "canonical_component_edge_candidate_count": 8,
            "witnesses_per_component_edge": 128,
        },
        "strict_credit_boundary_values": {
            "zero_credit_candidate_publication_only": True,
            "independent_verifier_admitted": False,
            "candidate_ledger_formal_anchor_binding_credit": 2048,
            "candidate_ledger_formal_physical_witness_credit": 1024,
            "candidate_ledger_formal_component_edge_credit": 8,
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
        },
        "conditional_later_fresh_DSU_effect_values": {
            "canonical_edges_eligible_after_independent_promotion": 8,
            "maximum_later_rank_reductions": 8,
            "Round304_component_count": 92696,
            "conditional_post_edge_component_count": 92688,
            "applied_in_Round305B": False,
        },
        "zero_credit_candidate_publication_permitted_const": True,
        "manifest_emitted_const": False,
        "result_sha256_rule": (
            "sha256(canonical_json(final result object with result_sha256 "
            "absent, after candidate_file_commitments has been inserted))"
        ),
        "no_recursive_result_file_commitment": True,
    },
    "serialization": {
        "canonical_json": {
            "encoding": "UTF-8",
            "sort_object_keys": True,
            "object_key_sort": "Unicode code-point order",
            "separators": [",", ":"],
            "ensure_ascii": False,
            "allow_nan": False,
            "trailing_newline": False,
            "array_order_preserved": True,
        },
        "ledger_file": {
            "format": "RFC1952 gzip over canonical JSON bytes",
            "compression_level": 9,
            "mtime_uint32": 0,
            "filename": "empty",
            "comment": "absent",
            "extra": "absent",
            "text_flag": 0,
            "os_header_byte": 255,
            "xfl_for_level_9": 2,
            "deflate_runtime": "zlib-1.3",
        },
        "result_file": {
            "format": "uncompressed canonical JSON bytes",
            "trailing_newline": False,
        },
    },
}

SCHEMA_SNAPSHOT = {
    "schema": SCHEMA,
    "physical_witness_row_keys": list(PHYSICAL_WITNESS_KEYS),
    "anchor_row_keys": list(ANCHOR_KEYS),
    "closure_contact_row_keys": list(CLOSURE_CONTACT_KEYS),
    "owner_locus_row_keys": list(OWNER_LOCUS_KEYS),
    "component_edge_row_keys": list(COMPONENT_EDGE_KEYS),
    "expected_counts": {
        "physical_witness_rows": EXPECTED_WITNESSES,
        "anchor_rows": EXPECTED_ANCHORS,
        "closure_contact_rows": EXPECTED_CLOSURE_CONTACTS,
        "owner_locus_rows": EXPECTED_OWNER_LOCI,
        "canonical_component_edge_rows": EXPECTED_CANONICAL_COMPONENT_EDGES,
        "witnesses_per_component_edge": EXPECTED_WITNESSES_PER_COMPONENT_EDGE,
        "formal_DSU_rank_reductions_in_Round305B": 0,
        "maximum_later_fresh_DSU_rank_reductions":
            MAXIMUM_LATER_DSU_RANK_REDUCTIONS,
    },
    "official_key_contract": {
        "complete_Round304_official_key_count": EXPECTED_OFFICIAL_KEYS,
        "residual_official_key_count": EXPECTED_RESIDUAL_OFFICIAL_KEYS,
        "all_1024_residual_pairs_cross_official_key": True,
        "physical_component_edge_across_keys_permitted_when_G0_G5": True,
        "occurrence_identity_merge_credit": 0,
        "official_key_identity_merge_credit": 0,
    },
    "D4_transfer_enabled": D4_TRANSFER_ENABLED,
    "D4_direct_row_instantiation_required": EXPECTED_WITNESSES,
    "theorem": TWO_SIDED_ATTACHMENT_THEOREM,
    "normative_wire_spec": WIRE_SPEC,
}
FROZEN_SCHEMA_SNAPSHOT_SHA256 = (
    "ec5eab1b9aaeb851e8858b76d14ba7142d7db5aa41ea3286297317b105e547e7"
)

OUTPUT_NAMES = {
    "physical": PREFIX + "_physical_witness_ledger.json.gz",
    "anchor": PREFIX + "_anchor_ledger.json.gz",
    "contact": PREFIX + "_closure_contact_ledger.json.gz",
    "owner": PREFIX + "_owner_locus_ledger.json.gz",
    "edge": PREFIX + "_canonical_component_edge_ledger.json.gz",
    "result": PREFIX + "_result.json",
}
CANDIDATE_OUTPUT_KEYS = (
    "physical", "anchor", "contact", "owner", "edge", "result",
)
CANDIDATE_COMMIT_ORDER = tuple(
    OUTPUT_NAMES[key] for key in CANDIDATE_OUTPUT_KEYS
)
CANDIDATE_STAGE_PREFIX = ".r305b-zero-credit-candidate-stage-"
RENAME_NOREPLACE = 1


class PromotionBlocked(RuntimeError):
    """A fail-closed admission or theorem obligation is unsatisfied."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise PromotionBlocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


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
        raise PromotionBlocked("MISSING:" + label) from error
    need(path.parent.resolve() == D.resolve(), "OUTSIDE_DELIVERABLES:" + label)
    need(not stat.S_ISLNK(metadata.st_mode), "SYMLINK:" + label)
    need(stat.S_ISREG(metadata.st_mode), "NONREGULAR:" + label)
    need(metadata.st_nlink == 1, "HARDLINK:" + label)
    need(metadata.st_size > 0, "EMPTY:" + label)


def strict_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "DUPLICATE_JSON_KEY:" + key)
        result[key] = value
    return result


def strict_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    need(0 < len(raw) <= MAX_JSON_BYTES, "JSON_SIZE:" + label)
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=strict_object_pairs,
            parse_float=lambda token: (_ for _ in ()).throw(
                PromotionBlocked("FLOAT_JSON:" + label + ":" + token)
            ),
            parse_constant=lambda token: (_ for _ in ()).throw(
                PromotionBlocked("NONFINITE_JSON:" + label + ":" + token)
            ),
        )
    except UnicodeDecodeError as error:
        raise PromotionBlocked("NON_UTF8_JSON:" + label) from error
    need(type(value) is dict, "TOP_LEVEL_JSON_OBJECT:" + label)
    return value


def read_json(name: str) -> dict[str, Any]:
    path = D / name
    require_regular(path, name)
    return strict_json_bytes(path.read_bytes(), name)


def verify_self(value: dict[str, Any], field: str, label: str) -> None:
    observed = value.get(field)
    need(type(observed) is str and PIN_RE.fullmatch(observed) is not None,
         "SELF_HASH_FIELD:" + label)
    body = dict(value)
    del body[field]
    need(digest(body) == observed, "SELF_HASH:" + label)


def parse_manifest(name: str, expected_sha256: str) -> dict[str, str]:
    need(PIN_RE.fullmatch(expected_sha256) is not None,
         "UNFILLED_MANIFEST_PIN:" + name)
    path = D / name
    require_regular(path, name)
    need(file_sha256(path) == expected_sha256, "MANIFEST_PIN:" + name)
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\n]+)", line)
        need(match is not None, "MANIFEST_SYNTAX:" + name)
        pin, member = match.groups()
        need(member not in entries, "MANIFEST_DUPLICATE:" + name)
        entries[member] = pin
    need(bool(entries), "EMPTY_MANIFEST:" + name)
    return entries


def verify_complete_manifest(
    name: str,
    expected_sha256: str,
    *,
    expected_count: int,
    exact_members: frozenset[str] | None = None,
) -> dict[str, str]:
    entries = parse_manifest(name, expected_sha256)
    need(len(entries) == expected_count, "MANIFEST_MEMBER_COUNT:" + name)
    if exact_members is not None:
        need(set(entries) == set(exact_members), "MANIFEST_EXACT_SET:" + name)
    for member, pin in sorted(entries.items()):
        path = D / member
        require_regular(path, name + ":" + member)
        need(file_sha256(path) == pin, "MANIFEST_MEMBER_PIN:" + name + ":" + member)
    return entries


def audit_reference_source(name: str, expected_sha256: str) -> None:
    """Pin and parse a formal source without importing or executing it."""

    path = D / name
    require_regular(path, "reference-source:" + name)
    need(file_sha256(path) == expected_sha256, "REFERENCE_SOURCE_PIN:" + name)
    raw = path.read_bytes()
    try:
        source = raw.decode("utf-8")
        ast.parse(source, filename=name)
    except (UnicodeDecodeError, SyntaxError) as error:
        raise PromotionBlocked("REFERENCE_SOURCE_PARSE:" + name) from error
    lowered = source.lower()
    for fragment in FORBIDDEN_RUNTIME_SOURCE_FRAGMENTS:
        need(fragment.lower() not in lowered,
             "FORBIDDEN_REFERENCE_SOURCE_FRAGMENT:" + name + ":" + fragment)


def admit_formal_geometry_inputs() -> dict[str, dict[str, str]]:
    """Admit the complete direct geometry lineage before opening ledgers."""

    manifests: dict[str, dict[str, str]] = {}
    flattened: dict[str, set[str]] = defaultdict(set)
    for name, (pin, count) in FORMAL_MANIFEST_PINS.items():
        entries = verify_complete_manifest(name, pin, expected_count=count)
        manifests[name] = entries
        for member, member_pin in entries.items():
            flattened[member].add(member_pin)
    for member, pin in FORMAL_CRITICAL_PINS.items():
        need(flattened.get(member) == {pin},
             "FORMAL_CRITICAL_MANIFEST_PIN:" + member)
    runtime_source_pins = {
        filename: pin for _module_name, filename, pin
        in CACHELESS_RUNTIME_SOURCE_MODULES
    }
    need(
        runtime_source_pins[R174_PREFIX + ".py"]
        == FORMAL_CRITICAL_PINS[R174_PREFIX + ".py"]
        and runtime_source_pins[R179_PREFIX + ".py"]
        == FORMAL_CRITICAL_PINS[R179_PREFIX + ".py"]
        and flattened.get(R174_PREFIX + "_verifier.py")
        == {runtime_source_pins[R174_PREFIX + "_verifier.py"]},
        "CACHELESS_RUNTIME_SOURCE_PIN_CLOSURE",
    )
    for filename, pin in runtime_source_pins.items():
        audit_reference_source(filename, pin)
    for name, pin in REFERENCE_ONLY_SOURCE_PINS.items():
        audit_reference_source(name, pin)

    # R273/R274 may document lineage, but this producer's executable import
    # graph deliberately stops at the exact-pinned R174/R179 runtime roots.
    own_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"), __file__)
    imported: set[str] = set()
    for node in ast.walk(own_tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imported.add(node.module)
    need(not any("round273" in name or "round274" in name for name in imported),
         "REFERENCE_ONLY_R273_R274_IMPORTED")
    return manifests


def admit_sealed_inputs() -> dict[str, dict[str, str]]:
    # Refuse before opening any Round305A result or ledger.
    need(
        type(R305A_MANIFEST_SHA256) is str
        and PIN_RE.fullmatch(R305A_MANIFEST_SHA256) is not None,
        "BLOCKED_UNFILLED_ROUND305A_COMPLETE_MANIFEST_SHA256_PIN",
    )
    geometry = admit_formal_geometry_inputs()
    r303b = verify_complete_manifest(
        R303B_MANIFEST, R303B_MANIFEST_SHA256, expected_count=12,
    )
    r304 = verify_complete_manifest(
        R304_MANIFEST, R304_MANIFEST_SHA256, expected_count=11,
    )
    r305a = verify_complete_manifest(
        R305A_MANIFEST, R305A_MANIFEST_SHA256, expected_count=8,
        exact_members=R305A_EXPECTED_MANIFEST_MEMBERS,
    )
    for member, pin in R305A_CRITICAL_FILE_PINS.items():
        need(r305a.get(member) == pin, "ROUND305A_CRITICAL_PIN:" + member)

    result = read_json(R305A_RESULT)
    verification = read_json(R305A_VERIFICATION)
    attacks = read_json(R305A_ATTACKS)
    verify_self(result, "result_sha256", R305A_RESULT)
    verify_self(verification, "verification_sha256", R305A_VERIFICATION)
    need(result["result_sha256"] == R305A_RESULT_OBJECT_SHA256,
         "ROUND305A_RESULT_OBJECT_PIN")
    need(
        verification["verification_sha256"]
        == R305A_VERIFICATION_OBJECT_SHA256,
        "ROUND305A_VERIFICATION_OBJECT_PIN",
    )
    need(
        result.get("status")
        == (
            "PASS_ROUND305A_EXACT_R300A_POST_R304_RESIDUAL_SCOPE_"
            "REPROJECTION__1024_RESIDUAL_PAIRS__ZERO_DOWNSTREAM_CREDIT"
        ),
        "ROUND305A_RESULT_STATUS",
    )
    need(
        verification.get("status")
        == "PASS_EXACT_CACHELESS_ROUND305A_SCOPE_REPROJECTION"
        and verification.get("formal_Round305A_scope_promotion_permitted")
        is True
        and verification.get("schema_snapshot_sha256")
        == R305A_SCHEMA_SNAPSHOT_SHA256
        and verification["attack_suite"].get("all_rejected") is True
        and verification["attack_suite"].get("fixture_count") == 36
        and verification["attack_suite"].get("rejected_count") == 36,
        "ROUND305A_INDEPENDENT_VERIFICATION",
    )
    need(
        attacks.get("status")
        == "PASS_ALL_ROUND305A_ATTACK_FIXTURES_REJECTED",
        "ROUND305A_ATTACK_STATUS",
    )
    zero = result["formal_credit_transition"]
    need(all(value == 0 for value in zero.values()),
         "ROUND305A_ZERO_DOWNSTREAM_CREDIT")
    need(
        result["strict_boundary"].get("exact_residual_scope_reprojection_sealed")
        is True
        and result["strict_boundary"].get("physical_inclusion_package_present")
        is False
        and result["strict_boundary"].get("two_sided_gluing_theorem_present")
        is False,
        "ROUND305A_SCOPE_ONLY_BOUNDARY",
    )
    return {
        **{"geometry:" + key: value for key, value in geometry.items()},
        "Round303B": r303b,
        "Round304": r304,
        "Round305A": r305a,
    }


def read_r305a_scope() -> tuple[list[dict[str, Any]], set[str]]:
    path = D / R305A_LEDGER
    require_regular(path, R305A_LEDGER)
    with gzip.open(path, "rb") as stream:
        raw = stream.read(MAX_JSON_BYTES + 1)
    ledger = strict_json_bytes(raw, R305A_LEDGER)
    verify_self(ledger, "ledger_sha256", R305A_LEDGER)
    rows = ledger.get("post_Round304_scope_reprojection_rows")
    need(type(rows) is list and len(rows) == 3_232, "ROUND305A_LEDGER_ROWS")
    need(digest(rows) == ledger.get("rows_sha256"), "ROUND305A_ROWS_SHA256")

    residual: list[dict[str, Any]] = []
    for row in rows:
        need(type(row) is dict, "ROUND305A_ROW_OBJECT")
        verify_self(row, "row_sha256", "ROUND305A_ROW")
        if row.get("requires_formal_physical_inclusion") is not True:
            continue
        need(
            row.get("post_Round304_disposition")
            == (
                "UNWITNESSED__CROSS_COMPONENT__FORMAL_PHYSICAL_"
                "INCLUSION_PACKAGE_REQUIRED"
            )
            and row.get("same_Round304_final_component") is False
            and row.get("source_row_fed_to_DSU") is False
            and row.get("unsealed_temp_scope_consumed") is False,
            "ROUND305A_RESIDUAL_BOUNDARY",
        )
        for credit in (
            "formal_physical_inclusion_credit", "formal_component_edge_credit",
            "formal_DSU_rank_reduction_credit", "formal_maximality_credit",
            "formal_fibre_credit", "formal_global_disposition_credit",
            "formal_Jx_Jy_same_point_glue_credit",
        ):
            need(row.get(credit) == 0, "ROUND305A_RESIDUAL_CREDIT:" + credit)
        pair = row["canonical_Round294_registry_occurrence_pair"]
        components = row["final_component_pair"]
        need(
            type(pair) is list and len(pair) == 2 and pair == sorted(pair)
            and pair[0] != pair[1],
            "ROUND305A_CANONICAL_OCCURRENCE_PAIR",
        )
        need(
            type(components) is list and len(components) == 2
            and components == sorted(components) and components[0] != components[1],
            "ROUND305A_CANONICAL_COMPONENT_PAIR",
        )
        residual.append(row)

    need(len(residual) == EXPECTED_WITNESSES, "RESIDUAL_COUNT")
    occurrence_pairs = sorted(
        row["canonical_Round294_registry_occurrence_pair"] for row in residual
    )
    endpoints = {
        endpoint for pair in occurrence_pairs for endpoint in pair
    }
    all_component_pairs = sorted(
        row["final_component_pair"] for row in residual
    )
    component_pairs = sorted({
        tuple(row["final_component_pair"]) for row in residual
    })
    component_histogram = Counter(
        tuple(row["final_component_pair"]) for row in residual
    )
    need(digest(occurrence_pairs) == RESIDUAL_PAIR_SET_SHA256,
         "RESIDUAL_PAIR_SET")
    need(
        len(endpoints) == EXPECTED_ANCHORS
        and digest(sorted(endpoints)) == RESIDUAL_ENDPOINT_SET_SHA256,
        "RESIDUAL_ENDPOINT_SET",
    )
    need(
        len(component_pairs) == EXPECTED_CANONICAL_COMPONENT_EDGES
        and digest(all_component_pairs)
        == RESIDUAL_FINAL_COMPONENT_PAIR_SET_SHA256
        and set(component_histogram.values())
        == {EXPECTED_WITNESSES_PER_COMPONENT_EDGE},
        "RESIDUAL_COMPONENT_PAIR_8_BY_128",
    )
    need(
        digest([row["source_Round300A_row_id"] for row in residual])
        == RESIDUAL_SOURCE_ROW_IDS_SHA256
        and digest([row["source_Round300A_row_sha256"] for row in residual])
        == RESIDUAL_SOURCE_ROW_HASHES_SHA256,
        "RESIDUAL_SOURCE_ROWS",
    )
    return residual, endpoints


def iter_json_array(stream: TextIO, marker: str) -> Iterator[dict[str, Any]]:
    buffer = ""
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "STREAM_MARKER:" + marker)
        buffer += block
    buffer = buffer.split(marker, 1)[1]
    decoder = json.JSONDecoder(object_pairs_hook=strict_object_pairs)
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "STREAM_TRUNCATED")
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
                need(bool(block), "STREAM_ROW_TRUNCATED")
                buffer += block
        need(type(row) is dict, "STREAM_ROW_OBJECT")
        yield row
        buffer = buffer[end:]


def iter_json_values(stream: TextIO, marker: str) -> Iterator[Any]:
    """Stream one exact JSON array whose rows need not be objects."""

    buffer = ""
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "STREAM_VALUE_MARKER:" + marker)
        buffer += block
    buffer = buffer.split(marker, 1)[1]
    decoder = json.JSONDecoder(object_pairs_hook=strict_object_pairs)
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "STREAM_VALUE_TRUNCATED")
            buffer = block
            continue
        if buffer[0] == ",":
            buffer = buffer[1:]
            continue
        if buffer[0] == "]":
            return
        while True:
            try:
                value, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = stream.read(1 << 20)
                need(bool(block), "STREAM_VALUE_ROW_TRUNCATED")
                buffer += block
        yield value
        buffer = buffer[end:]


def read_gzip_json(name: str) -> dict[str, Any]:
    path = D / name
    require_regular(path, name)
    with gzip.open(path, "rb") as stream:
        raw = stream.read(MAX_JSON_BYTES + 1)
    return strict_json_bytes(raw, name)


def verify_closed_row(row: dict[str, Any], label: str) -> None:
    need(type(row) is dict and "row_sha256" in row, "ROW_OBJECT:" + label)
    observed = row["row_sha256"]
    need(type(observed) is str and PIN_RE.fullmatch(observed) is not None,
         "ROW_HASH_FIELD:" + label)
    payload = dict(row)
    del payload["row_sha256"]
    need(digest(payload) == observed, "ROW_HASH:" + label)


def verify_embedded_table(
    document: dict[str, Any], rows_key: str, count_key: str, hash_key: str,
) -> list[dict[str, Any]]:
    rows = document.get(rows_key)
    need(
        type(rows) is list
        and document.get(count_key) == len(rows)
        and document.get(hash_key) == digest(rows),
        "EMBEDDED_TABLE_CLOSURE:" + rows_key,
    )
    return rows


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def qlist(values: Iterator[Q] | tuple[Q, ...] | list[Q]) -> list[str]:
    return [qstr(value) for value in values]


def qbox(values: list[str], label: str) -> tuple[Q, ...]:
    result = tuple(map(Q, values))
    need(
        len(result) == 6
        and all(result[2 * axis] < result[2 * axis + 1] for axis in range(3)),
        "POSITIVE_RATIONAL_BOX:" + label,
    )
    return result


def square_interval(lower: Q, upper: Q) -> tuple[Q, Q]:
    need(lower < upper and lower * upper > 0, "SIGNED_SQUARE_INTERVAL")
    return (lower * lower, upper * upper) if lower > 0 else (
        upper * upper, lower * lower,
    )


def physical_t_square_interval(
    adjacent_box: tuple[Q, ...], source_guard_box: tuple[Q, ...],
) -> tuple[Q, Q]:
    adjacent = square_interval(adjacent_box[0], adjacent_box[1])
    source = square_interval(source_guard_box[0], source_guard_box[1])
    image = (Q(1) - source[1], Q(1) - source[0])
    result = (max(adjacent[0], image[0]), min(adjacent[1], image[1]))
    need(result[0] < result[1], "POSITIVE_EXACT_PHYSICAL_T_SQUARE")
    return result


def sqrt_dyadic_bounds(value: Q, bits: int = 512) -> tuple[Q, Q]:
    need(value >= 0 and bits >= 256, "SQRT_DYADIC_DOMAIN")
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
    need(lower * lower <= value <= upper * upper, "SQRT_DYADIC_ENCLOSURE")
    return lower, upper


def signed_sqrt_outer(
    z_interval: tuple[Q, Q], physical_t_sign: int,
) -> tuple[Q, Q]:
    need(physical_t_sign in {-1, 1}, "PHYSICAL_T_SIGN")
    lower = sqrt_dyadic_bounds(z_interval[0])[0]
    upper = sqrt_dyadic_bounds(z_interval[1])[1]
    need(Q(0) < lower <= upper, "STRICT_SIGNED_SQRT")
    return (lower, upper) if physical_t_sign > 0 else (-upper, -lower)


def targeted_interval(
    lower: Q, upper: Q, direction: str, depth: int,
) -> tuple[Q, Q]:
    need(
        lower < upper and direction in {"LOWER", "UPPER"} and depth > 0,
        "TARGETED_INTERVAL_DOMAIN",
    )
    width = upper - lower
    divisor = 1 << depth
    if direction == "LOWER":
        outer = (lower, lower + width / divisor)
    else:
        outer = (upper - width / divisor, upper)
    result = (
        outer[0] + (outer[1] - outer[0]) / 4,
        outer[1] - (outer[1] - outer[0]) / 4,
    )
    need(lower < result[0] < result[1] < upper,
         "STRICT_TARGETED_INTERVAL")
    return result


def replace_axis(
    box: tuple[Q, ...], axis: int, interval: tuple[Q, Q],
) -> tuple[Q, ...]:
    values = list(box)
    values[2 * axis:2 * axis + 2] = interval
    return tuple(values)


def strict_quarter_inset_core(
    transformed_box: tuple[Q, ...],
) -> tuple[Q, ...]:
    """Deterministic closed core strictly inside an open (z,p,s) cell."""

    values = list(transformed_box)
    for axis in (0, 2):
        lower = transformed_box[2 * axis]
        upper = transformed_box[2 * axis + 1]
        width = upper - lower
        need(width > 0, "STRICT_CORE_POSITIVE_TANGENT_WIDTH")
        values[2 * axis] = lower + width / 4
        values[2 * axis + 1] = upper - width / 4
    result = tuple(values)
    need(
        all(
            transformed_box[2 * axis] < result[2 * axis]
            < result[2 * axis + 1] < transformed_box[2 * axis + 1]
            for axis in (0, 2)
        ),
        "STRICT_QUARTER_CORE_INSIDE_OPEN_BASE",
    )
    return result


Term = tuple[str, int]
Normal = tuple[Term, Term]


def source_normal(cell: str, source_t_sign: int) -> Normal:
    z: Term = ("Z", 1)
    signed_o: Term = ("O", source_t_sign)
    if cell == "E":
        return z, signed_o
    if cell == "W":
        return ("Z", -1), signed_o
    if cell == "N":
        return signed_o, z
    if cell == "S":
        return signed_o, ("Z", -1)
    raise PromotionBlocked("SOURCE_CELL:" + cell)


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
    raise PromotionBlocked("ADJACENT_CELL:" + cell)


TRANSITION = {
    ("E", 1): ("N", 1), ("E", -1): ("S", 1),
    ("N", 1): ("E", 1), ("N", -1): ("W", 1),
    ("W", 1): ("N", -1), ("W", -1): ("S", -1),
    ("S", 1): ("E", -1), ("S", -1): ("W", -1),
}


def factor_descriptor(region: dict[str, Any]) -> dict[str, Any]:
    need(region.get("arrangement_classification") == "REGULAR_GRAPH_CROSSING",
         "FACTOR_GRAPH_REGION")
    reason = region["active_reason"]
    kind, axis, wall = reason.split(":")
    need(
        kind == "wall_endpoint_or_count_transition"
        and axis in {"X", "Y"},
        "ROUND305B_FIXED_WALL_FACTOR_SCOPE",
    )
    expression = (
        "interval_geometry(adjacent_chart,owner_target)."
        + ("hit_x[0]" if axis == "X" else "hit_y[0]")
        + f"-arb({int(wall)})"
    )
    identity = {
        "adjacent_chart": region["adjacent_chart"],
        "owner_target": region["owner_target"],
        "active_reason": reason,
        "active_function_expression": expression,
        "active_function_evaluator_module_sha256":
            REFERENCE_ONLY_SOURCE_PINS[
                "cm2_round274_source_g_reverse_rechart_tail_arrangement_probe.py"
            ],
        "interval_geometry_module_sha256":
            FORMAL_CRITICAL_PINS[R179_PREFIX + ".py"],
    }
    return {
        "active_function_id": "round300b-active-function:" + digest(identity),
        "active_function_identity_payload": identity,
        "desired_side_sign": region["active_factor_side_sign"],
        "strict_derivative_signs_t_p_s":
            region["strict_derivative_signs_t_p_s"],
    }


def compile_exec_verified_source_module(
    module_name: str,
    path: Path,
    expected_sha256: str,
) -> ModuleType:
    """Execute exact source bytes without consulting any importlib/pyc loader."""

    need(module_name not in sys.modules, "CACHELESS_MODULE_PRELOADED:" + module_name)
    raw = path.read_bytes()
    need(
        hashlib.sha256(raw).hexdigest() == expected_sha256,
        "CACHELESS_SOURCE_SHA256:" + module_name,
    )
    try:
        code = compile(
            raw, str(path), "exec", flags=0, dont_inherit=True, optimize=0,
        )
    except (SyntaxError, ValueError) as error:
        raise PromotionBlocked("CACHELESS_SOURCE_COMPILE:" + module_name) from error
    module = ModuleType(module_name)
    module.__file__ = str(path)
    module.__package__ = ""
    module.__loader__ = None
    module.__spec__ = None
    module.__cached__ = None
    sys.modules[module_name] = module
    try:
        exec(code, module.__dict__)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    need(
        module.__loader__ is None
        and module.__spec__ is None
        and module.__cached__ is None,
        "CACHELESS_MODULE_METADATA:" + module_name,
    )
    return module


def cacheless_same_mtime_size_stale_pyc_selftest() -> dict[str, Any]:
    """Prove a timestamp-valid stale pyc cannot affect compile(bytes)+exec()."""

    fresh = b'VALUE = "FRESH"\n'
    stale = b'VALUE = "STALE"\n'
    need(len(fresh) == len(stale), "STALE_PYC_ATTACK_EQUAL_SOURCE_SIZE")
    with tempfile.TemporaryDirectory(prefix="cm2-r305b-stale-pyc-attack-") as root:
        directory = Path(root)
        source = directory / "probe.py"
        fixed_ns = 1_700_000_000_000_000_000
        source.write_bytes(stale)
        os.utime(source, ns=(fixed_ns, fixed_ns))
        py_compile.compile(
            str(source), doraise=True,
            invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP,
        )
        pyc = Path(importlib.util.cache_from_source(str(source)))
        stale_stat = source.stat()
        source.write_bytes(fresh)
        os.utime(source, ns=(fixed_ns, fixed_ns))
        fresh_stat = source.stat()
        need(
            stale_stat.st_size == fresh_stat.st_size == len(fresh)
            and stale_stat.st_mtime_ns == fresh_stat.st_mtime_ns == fixed_ns
            and pyc.is_file(),
            "STALE_PYC_ATTACK_TIMESTAMP_SIZE_COLLISION",
        )

        # Demonstrate that a conventional loader is in fact vulnerable to the
        # deliberately forged timestamp/size cache in this isolated directory.
        vulnerable_name = "_r305b_stale_pyc_vulnerable_probe"
        vulnerable_spec = importlib.util.spec_from_file_location(
            vulnerable_name, source,
        )
        need(
            vulnerable_spec is not None and vulnerable_spec.loader is not None,
            "STALE_PYC_ATTACK_VULNERABLE_SPEC",
        )
        vulnerable = importlib.util.module_from_spec(vulnerable_spec)
        vulnerable_spec.loader.exec_module(vulnerable)
        need(vulnerable.VALUE == "STALE", "STALE_PYC_ATTACK_NOT_EFFECTIVE")

        safe_name = "_r305b_stale_pyc_cacheless_probe"
        safe = compile_exec_verified_source_module(
            safe_name, source, hashlib.sha256(fresh).hexdigest(),
        )
        try:
            need(safe.VALUE == "FRESH", "STALE_PYC_AFFECTED_CACHELESS_EXEC")
        finally:
            sys.modules.pop(safe_name, None)
    need(not directory.exists(), "STALE_PYC_ATTACK_TEMPORARY_PYC_NOT_REMOVED")
    return {
        "same_mtime": True,
        "same_size": True,
        "conventional_stale_pyc_attack_effective": True,
        "cacheless_source_compile_exec_returned_fresh_value": True,
        "stale_pyc_influenced_formal_runtime": False,
        "temporary_pyc_written": True,
        "temporary_pyc_read": True,
        "temporary_pyc_removed": True,
    }


def cacheless_runtime_closure() -> dict[str, Any]:
    """Path-free exact runtime statement committed by every candidate."""

    return {
        "python_implementation": "CPython",
        "python_version": "3.12.3",
        "python_flint_version": "0.9.0",
        "zlib_runtime_version": "1.3",
        "arb_precision_bits": 768,
        "loader": "SHA256_VERIFIED_SOURCE_BYTES_COMPILE_EXEC",
        "loader_scope": "SIX_PINNED_PROJECT_LOCAL_FORMAL_GEOMETRY_MODULES_ONLY",
        "runtime_source_sha256_pins": {
            module_name: expected_sha256
            for module_name, _filename, expected_sha256
            in CACHELESS_RUNTIME_SOURCE_MODULES
        },
        "runtime_source_module_count": 6,
        "project_local_formal_geometry_module_pycache_reads": False,
        "project_local_formal_geometry_module_pycache_writes": False,
        "project_local_formal_geometry_source_compile_exec": True,
        "same_mtime_same_size_stale_pyc_attack_rejected": True,
        "stale_pyc_attack_probe_temporary_pyc_written": True,
        "stale_pyc_attack_probe_temporary_pyc_read": True,
        "stale_pyc_attack_probe_temporary_pyc_removed": True,
        "external_flint_imported_via_standard_importlib": True,
        "external_flint_outside_six_module_direct_source_graph": True,
        "global_no_pyc_claim_made": False,
        "R273_R274_imported_or_executed": False,
        "floating_point_fallback_used": False,
    }


def load_interval_runtime() -> tuple[Any, Any, Any, dict[str, Any]]:
    """Load the complete pinned interval graph by source compile+exec only."""

    expected_python = ROOT / ".venv-cm2" / "bin" / "python"
    need(
        Path(sys.executable).absolute() == expected_python.absolute(),
        "ROUND305B_REQUIRES_DOT_VENV_CM2_PYTHON",
    )
    need(
        sys.implementation.name == "cpython"
        and sys.version_info[:3] == (3, 12, 3),
        "ROUND305B_REQUIRES_CPYTHON_3_12_3",
    )
    need(
        zlib.ZLIB_RUNTIME_VERSION == "1.3",
        "ROUND305B_REQUIRES_ZLIB_1_3",
    )
    module_names = [row[0] for row in CACHELESS_RUNTIME_SOURCE_MODULES]
    need(
        len(module_names) == len(set(module_names)) == 6
        and not any(name in sys.modules for name in module_names),
        "CACHELESS_FORMAL_RUNTIME_PRELOADED",
    )
    flint = importlib.import_module("flint")
    need(getattr(flint, "__version__", None) == "0.9.0",
         "PYTHON_FLINT_VERSION_0_9_0_REQUIRED")
    flint.ctx.prec = 768
    need(flint.ctx.prec == 768, "ARB_PRECISION_768_REQUIRED")
    attack = cacheless_same_mtime_size_stale_pyc_selftest()
    need(
        attack["stale_pyc_influenced_formal_runtime"] is False,
        "STALE_PYC_ATTACK_REJECTION",
    )

    loaded: dict[str, ModuleType] = {}
    previous_dont_write = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        for module_name, filename, expected_sha256 in (
            CACHELESS_RUNTIME_SOURCE_MODULES
        ):
            path = D / filename
            require_regular(path, "cacheless-runtime-source:" + filename)
            loaded[module_name] = compile_exec_verified_source_module(
                module_name, path, expected_sha256,
            )
    except BaseException:
        for module_name in loaded:
            sys.modules.pop(module_name, None)
        raise
    finally:
        sys.dont_write_bytecode = previous_dont_write

    first_hit = loaded["cm2_gate3_candidate_first_hit_cert"]
    ge = loaded["cm2_gate3_ge_interval_atlas_cert"]
    atlas = loaded["cm2_gate3_eight_cell_symmetry_atlas_cert"]
    producer = loaded[R174_PREFIX]
    verifier = loaded[R174_PREFIX + "_verifier"]
    module = loaded[R179_PREFIX]
    need(
        ge.base is first_hit
        and atlas.base is first_hit
        and atlas.ge is ge
        and producer.first_hit is first_hit
        and producer.atlas is atlas
        and verifier.first_hit is first_hit
        and verifier.atlas is atlas
        and module.r174 is verifier,
        "CACHELESS_RUNTIME_DEPENDENCY_IDENTITY",
    )
    for module_name, filename, expected_sha256 in CACHELESS_RUNTIME_SOURCE_MODULES:
        loaded_module = loaded[module_name]
        need(
            Path(loaded_module.__file__).resolve() == (D / filename).resolve()
            and file_sha256(Path(loaded_module.__file__)) == expected_sha256
            and loaded_module.__loader__ is None
            and loaded_module.__cached__ is None,
            "CACHELESS_RUNTIME_FINAL_IDENTITY:" + module_name,
        )
    need(
        not any("round273" in name or "round274" in name for name in sys.modules),
        "REFERENCE_ONLY_R273_R274_RUNTIME_IMPORT",
    )
    # The pinned legacy modules set their historical 192/256-bit contexts at
    # import time.  Round305B's direct kernel promises 768-bit Arb arithmetic,
    # so reassert that precision after the complete source graph is loaded.
    flint.ctx.prec = 768
    need(flint.ctx.prec == 768, "ARB_PRECISION_768_AFTER_SOURCE_LOAD")
    return producer, module, flint, attack


def extremal_point(
    r179: Any,
    box: Any,
    derivative_signs: list[str | None],
    want_maximum: bool,
) -> Any:
    bounds: list[tuple[Q, Q]] = []
    for (lower, upper), sign in zip(
        ((box.t0, box.t1), (box.p0, box.p1), (box.s0, box.s1)),
        derivative_signs,
        strict=True,
    ):
        if sign == "STRICT_POSITIVE":
            value = upper if want_maximum else lower
            bounds.append((value, value))
        elif sign == "STRICT_NEGATIVE":
            value = lower if want_maximum else upper
            bounds.append((value, value))
        else:
            # An OVERWRAP/unknown transverse derivative gives no monotone
            # corner reduction.  Retain the entire coordinate interval so the
            # ensuing Arb evaluation is a rigorous slab enclosure; a midpoint
            # would prove only one sample and is not a box extremum.
            bounds.append((lower, upper))
    return r179.r174.atlas.AtlasBox(
        bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1],
        bounds[2][0], bounds[2][1], box.depth, "round305b-extremal-slab",
    )


def active_dual(geometry: dict[str, Any], reason: str, arb: Any) -> Any:
    kind, axis, wall = reason.split(":")
    need(
        kind == "wall_endpoint_or_count_transition" and axis in {"X", "Y"},
        "ACTIVE_DUAL_FIXED_WALL_SCOPE",
    )
    dual = geometry["hit_x" if axis == "X" else "hit_y"]
    return dual[0] - arb(int(wall)), dual[1]


def active_factor_replay(
    piece: dict[str, Any],
    transformed_box: tuple[Q, ...],
    regions: dict[str, dict[str, Any]],
    r179: Any,
    flint: Any,
    cache: dict[tuple[str, tuple[Q, ...], int], dict[str, Any]],
) -> dict[str, Any]:
    key = (piece["region_id"], transformed_box, piece["physical_t_sign"])
    if key in cache:
        return cache[key]
    region = regions[piece["region_id"]]
    t_interval = signed_sqrt_outer(
        transformed_box[:2], piece["physical_t_sign"]
    )
    physical_box = (*t_interval, *transformed_box[2:])
    box = r179.r174.atlas.AtlasBox(
        *physical_box, 0, "round305b-direct-active-factor-replay"
    )
    signs: list[str] = []
    for want_maximum in (False, True):
        point = extremal_point(
            r179, box, region["strict_derivative_signs_t_p_s"], want_maximum,
        )
        geometry = r179.interval_geometry(
            region["adjacent_chart"], region["owner_target"], point,
        )
        signs.append(r179.sign(active_dual(
            geometry, region["active_reason"], flint.arb,
        )[0]))
    strict = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
    if not set(signs) <= strict:
        state = "UNRESOLVED_ACTIVE_FACTOR_OVERWRAP"
    elif signs[0] != signs[1]:
        state = "CLIPPED_DESIRED_SIDE_SUPPORT"
    elif signs[0] == region["active_factor_side_sign"]:
        state = "FULL_DESIRED_SIDE_SUPPORT"
    else:
        state = "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
    result = {
        "region_id": piece["region_id"],
        "active_function_id": factor_descriptor(region)["active_function_id"],
        "desired_side_sign": region["active_factor_side_sign"],
        "active_factor_extremal_signs": signs,
        "signed_support_state": state,
        "outer_rational_signed_physical_box": qlist(physical_box),
        "outer_box_contains_exact_algebraic_sqrt_boundaries": True,
        "sqrt_enclosure_bits": 512,
    }
    cache[key] = result
    return result


def wall_event_product_replay(
    transformed_box: tuple[Q, ...],
    physical_t_sign: int,
    region: dict[str, Any],
    r179: Any,
    flint: Any,
    label: str,
) -> dict[str, Any]:
    kind, axis, wall_token = region["active_reason"].split(":")
    need(
        kind == "wall_endpoint_or_count_transition"
        and axis in {"X", "Y"},
        "WALL_PRODUCT_ACTIVE_REASON:" + label,
    )
    wall = int(wall_token)
    # This residual scope is exactly the central wall.  Hard-checking it
    # prevents silently replacing (axis-wall) by the raw axis coordinate.
    need(wall == 0, "ROUND305B_SCOPE_REQUIRES_EXPLICIT_ZERO_WALL:" + label)
    t_interval = signed_sqrt_outer(transformed_box[:2], physical_t_sign)
    physical_box = (*t_interval, *transformed_box[2:])
    box = r179.r174.atlas.AtlasBox(
        *physical_box, 0, "round305b-wall-product-" + label,
    )
    geometry = r179.interval_geometry(
        region["adjacent_chart"], region["owner_target"], box,
    )
    source_dual = geometry["source_x" if axis == "X" else "source_y"]
    target_dual = geometry["hit_x" if axis == "X" else "hit_y"]
    wall_ball = flint.arb(wall)
    source_wall = source_dual[0] - wall_ball
    target_wall = target_dual[0] - wall_ball
    product = source_wall * target_wall
    return {
        "active_reason": region["active_reason"],
        "predicate_details": {
            "kind": kind,
            "axis": axis,
            "wall": wall,
            "source_wall_factor": f"source_{axis.lower()}-{wall}",
            "target_wall_factor_F": f"hit_{axis.lower()}-{wall}",
            "wall_event_product": (
                f"(source_{axis.lower()}-{wall})*(hit_{axis.lower()}-{wall})"
            ),
        },
        "source_wall_factor_sign": r179.sign(source_wall),
        "target_wall_factor_sign": r179.sign(target_wall),
        "wall_event_product_sign": r179.sign(product),
        "outer_rational_signed_physical_box": qlist(physical_box),
    }


R174_GUARD_COLUMNS = (
    "row_id", "chart", "parent_id", "refinement_path", "box",
    "coordinate_volume", "exact_rejection_predicate", "classification",
    "is_CM2_exterior_sheet_exclusion", "is_Gate5_geometric_disposition",
    "provenance", "transport_source_row_id", "transport_generator",
)


def load_r174_guards(required_ids: set[str]) -> dict[str, dict[str, Any]]:
    path = D / R174_ROWS
    found: dict[str, dict[str, Any]] = {}
    with path.open("rt", encoding="utf-8", newline="") as stream:
        for packed in iter_json_values(
            stream, '"chart_guard_rejection_rows":[',
        ):
            need(type(packed) is list and len(packed) == len(R174_GUARD_COLUMNS),
                 "R174_PACKED_GUARD_ARITY")
            row = dict(zip(R174_GUARD_COLUMNS, packed, strict=True))
            row_id = row["row_id"]
            if row_id in required_ids:
                need(row_id not in found, "R174_REQUIRED_GUARD_DUPLICATE")
                found[row_id] = row
    need(set(found) == required_ids, "R174_REQUIRED_GUARD_COVERAGE")
    return found


def load_r275_regions(required_ids: set[str]) -> dict[str, dict[str, Any]]:
    wrapper = read_json(R275_CERTIFICATE)
    need(wrapper.get("result_sha256") == digest(wrapper.get("result")),
         "R275_RESULT_CLOSURE")
    result = wrapper["result"]
    found: dict[str, dict[str, Any]] = {}
    total = 0
    for table_name in ("strict_region_ledger", "arrangement_region_ledger"):
        table = result[table_name]
        rows = table["rows"]
        need(
            table["row_count"] == len(rows)
            and table["rows_sha256"] == digest(rows)
            and table["row_hashes_sha256"]
            == digest([row["row_sha256"] for row in rows]),
            "R275_TABLE_CLOSURE:" + table_name,
        )
        total += len(rows)
        for row in rows:
            row_id = row["reverse_rechart_region_row_id"]
            if row_id in required_ids:
                verify_closed_row(row, "R275:" + row_id)
                need(row_id not in found, "R275_REQUIRED_REGION_DUPLICATE")
                found[row_id] = row
    need(total == 13_788 and set(found) == required_ids,
         "R275_REQUIRED_REGION_COVERAGE")
    return found


def load_r300a_bindings(
    residual: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    document = read_gzip_json(R300A_LEDGER)
    canonical_rows = verify_embedded_table(
        document,
        "canonical_occurrence_pair_rows",
        "canonical_occurrence_pair_row_count",
        "canonical_occurrence_pair_rows_sha256",
    )
    source_rows = verify_embedded_table(
        document,
        "source_pair_expansion_rows",
        "source_pair_expansion_row_count",
        "source_pair_expansion_rows_sha256",
    )
    wanted_canonical = {
        row["source_Round300A_row_id"]: row for row in residual
    }
    need(len(wanted_canonical) == EXPECTED_WITNESSES,
         "R300A_SCOPE_CANONICAL_IDS")
    canonical_by_id: dict[str, dict[str, Any]] = {}
    for row in canonical_rows:
        row_id = row["Round300A_canonical_occurrence_pair_row_id"]
        if row_id in wanted_canonical:
            verify_closed_row(row, "R300A_CANONICAL:" + row_id)
            need(row_id not in canonical_by_id,
                 "R300A_CANONICAL_REQUIRED_DUPLICATE")
            canonical_by_id[row_id] = row
    need(set(canonical_by_id) == set(wanted_canonical),
         "R300A_CANONICAL_REQUIRED_COVERAGE")
    wanted_source_ids: set[str] = set()
    for row in canonical_by_id.values():
        ids = row["source_Round287_pair_row_ids"]
        need(type(ids) is list and len(ids) == 1,
             "R300A_ONE_SOURCE_PAIR_PER_RESIDUAL")
        wanted_source_ids.add(ids[0])
    need(len(wanted_source_ids) == EXPECTED_WITNESSES,
         "R300A_DISTINCT_SOURCE_PAIR_SCOPE")
    source_by_id: dict[str, dict[str, Any]] = {}
    for row in source_rows:
        source_id = row["source_Round287_pair_row_id"]
        if source_id in wanted_source_ids:
            verify_closed_row(row, "R300A_SOURCE:" + source_id)
            need(source_id not in source_by_id,
                 "R300A_SOURCE_REQUIRED_DUPLICATE")
            source_by_id[source_id] = row
    need(set(source_by_id) == wanted_source_ids,
         "R300A_SOURCE_REQUIRED_COVERAGE")

    bindings: list[dict[str, Any]] = []
    for scope in residual:
        canonical_row = canonical_by_id[scope["source_Round300A_row_id"]]
        pair = scope["canonical_Round294_registry_occurrence_pair"]
        need(
            canonical_row["row_sha256"]
            == scope["source_Round300A_row_sha256"]
            and canonical_row["canonical_unordered_Round294_registry_occurrence_ids"]
            == pair
            and canonical_row["frontier_disposition"]
            == (
                "UNRESOLVED_ENDPOINT_SPECIFIC_COMMON_ZERO_TRACE__"
                "OUTER_OVERLAP_AND_CLOSURE_ZERO_SET_INSUFFICIENT__ZERO_CREDIT"
            )
            and canonical_row["formal_component_edge_credit"] == 0
            and canonical_row["formal_DSU_rank_reduction_credit"] == 0,
            "R300A_CANONICAL_SCOPE_BINDING",
        )
        source_id = canonical_row["source_Round287_pair_row_ids"][0]
        source = source_by_id[source_id]
        left_occurrences = source["left_Round294_registry_occurrence_ids"]
        right_occurrences = source["right_Round294_registry_occurrence_ids"]
        need(
            len(left_occurrences) == len(right_occurrences) == 1
            and sorted((left_occurrences[0], right_occurrences[0])) == pair
            and source["active_factor_side_signs"]
            == ["STRICT_NEGATIVE", "STRICT_POSITIVE"]
            and source["regular_graph_zero_present_in_parent_cell_closure"]
            is True
            and source["formal_component_edge_credit"] == 0
            and source["formal_DSU_rank_reduction_credit"] == 0,
            "R300A_SOURCE_SCOPE_BINDING",
        )
        bindings.append({
            "pair": pair,
            "scope": scope,
            "canonical": canonical_row,
            "source": source,
            "source_Round287_pair_row_id": source_id,
            "left_endpoint": left_occurrences[0],
            "right_endpoint": right_occurrences[0],
            "left_region_id": source["left_Round275_region_id"],
            "right_region_id": source["right_Round275_region_id"],
        })
    bindings.sort(key=lambda item: item["pair"])
    need(
        len(bindings) == EXPECTED_WITNESSES
        and digest([item["pair"] for item in bindings])
        == RESIDUAL_PAIR_SET_SHA256,
        "R300A_BINDING_SCOPE_HASH",
    )
    return bindings


def load_r287_scope(
    bindings: list[dict[str, Any]],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    document = read_gzip_json(R287_LEDGER)
    pair_rows = verify_embedded_table(
        document,
        "mutually_exclusive_outer_overlap_pair_rows",
        "mutually_exclusive_outer_overlap_pair_row_count",
        "mutually_exclusive_outer_overlap_pair_rows_sha256",
    )
    region_rows = verify_embedded_table(
        document, "region_rows", "region_row_count", "region_rows_sha256",
    )
    union_rows = verify_embedded_table(
        document,
        "potential_new_support_union_rows",
        "potential_new_support_union_row_count",
        "potential_new_support_union_rows_sha256",
    )
    wanted_pairs = {item["source_Round287_pair_row_id"] for item in bindings}
    wanted_regions = {
        item[key]
        for item in bindings
        for key in ("left_region_id", "right_region_id")
    }
    pairs: dict[str, dict[str, Any]] = {}
    for row in pair_rows:
        row_id = row["Round287_mutually_exclusive_outer_overlap_pair_row_id"]
        if row_id in wanted_pairs:
            verify_closed_row(row, "R287_PAIR:" + row_id)
            need(row_id not in pairs, "R287_PAIR_REQUIRED_DUPLICATE")
            pairs[row_id] = row
    regions: dict[str, dict[str, Any]] = {}
    wanted_unions: set[str] = set()
    for row in region_rows:
        region_id = row["Round275_region_id"]
        if region_id in wanted_regions:
            verify_closed_row(row, "R287_REGION:" + region_id)
            need(region_id not in regions, "R287_REGION_REQUIRED_DUPLICATE")
            regions[region_id] = row
            wanted_unions.add(row["Round287_potential_new_support_union_id"])
    unions: dict[str, dict[str, Any]] = {}
    for row in union_rows:
        union_id = row["Round287_potential_new_support_union_id"]
        if union_id in wanted_unions:
            verify_closed_row(row, "R287_UNION:" + union_id)
            need(union_id not in unions, "R287_UNION_REQUIRED_DUPLICATE")
            unions[union_id] = row
    need(
        set(pairs) == wanted_pairs
        and set(regions) == wanted_regions
        and set(unions) == wanted_unions
        and len(regions) == EXPECTED_ANCHORS,
        "R287_REQUIRED_SCOPE_COVERAGE",
    )
    for item in bindings:
        source = item["source"]
        pair_row = pairs[item["source_Round287_pair_row_id"]]
        need(
            pair_row["row_sha256"] == source["source_Round287_pair_row_sha256"]
            and pair_row["left_Round275_region_id"] == item["left_region_id"]
            and pair_row["right_Round275_region_id"] == item["right_region_id"]
            and pair_row["source_guard_row_id"] == source["source_guard_row_id"]
            and pair_row["active_reason"] == source["active_reason"]
            and pair_row["adjacent_chart"] == source["adjacent_chart"]
            and pair_row["reason"]
            == "SAME_REGULAR_GRAPH_CELL_OPPOSITE_OPEN_FACTOR_SIDES"
            and pair_row["component_edge_credit"] == 0,
            "R287_PAIR_TO_R300A_BINDING",
        )
        for side in ("left", "right"):
            region_id = item[side + "_region_id"]
            region = regions[region_id]
            union = unions[region["Round287_potential_new_support_union_id"]]
            need(
                region["row_sha256"]
                == source[side + "_Round287_region_row_sha256"]
                and region["R275_region_kind"] == "REGULAR_GRAPH_CROSSING"
                and region["disposition"]
                == "ONE_STRICTLY_NEW_DISJOINT_SUPPORT_CANDIDATE__ZERO_CREDIT"
                and region["physical_t_sign"] in {-1, 1}
                and region["formal_occurrence_credit"] == 0
                and region["formal_component_credit"] == 0
                and union["Round275_region_id"] == region_id
                and union["source_kind"] == "WHOLE_R275_DISJOINT_REGION"
                and union["one_connected_positive_open_support"] is True
                and union["conditional_new_occurrence_count"] == 1
                and union["formal_occurrence_credit"] == 0,
                "R287_REGION_UNION_CHAIN",
            )
    return pairs, regions, unions


def load_r292_anchors(
    endpoints: set[str],
) -> dict[str, dict[str, Any]]:
    document = read_gzip_json(R292_LEDGER)
    rows = verify_embedded_table(document, "rows", "row_count", "rows_sha256")
    need(len(rows) == 22_820, "R292_COMPLETE_ROW_CENSUS")
    relevant_components: dict[str, tuple[dict[str, Any], str]] = {}
    cells_by_id: dict[str, dict[str, Any]] = {}
    refinement_count = 0
    component_count = 0
    for row in rows:
        if "Round292_R287_existing_overlap_refinement_cell_id" in row:
            refinement_count += 1
            cells_by_id[
                row["Round292_R287_existing_overlap_refinement_cell_id"]
            ] = row
        if (
            "Round292_refined_new_support_component_id" in row
            and "member_refinement_cell_ids" in row
        ):
            component_count += 1
            preimage = [
                "ROUND292_R287_EXISTING_OVERLAP_REFINED_NEW_SUPPORT_"
                "LOCAL_OCCURRENCE_V1",
                row["Round292_refined_new_support_component_id"],
                row["row_sha256"],
            ]
            occurrence = "source-g-expanded-occurrence:" + digest(preimage)
            if occurrence in endpoints:
                verify_closed_row(row, "R292_COMPONENT:" + occurrence)
                need(occurrence not in relevant_components,
                     "R292_ENDPOINT_COMPONENT_DUPLICATE")
                relevant_components[occurrence] = (row, digest(preimage))
    need(
        refinement_count == 11_852
        and component_count == 9_404
        and set(relevant_components) == endpoints,
        "R292_ENDPOINT_COMPONENT_COVERAGE",
    )
    result: dict[str, dict[str, Any]] = {}
    used_cells: set[str] = set()
    for occurrence, (component, preimage_hash) in relevant_components.items():
        cell_ids = component["member_refinement_cell_ids"]
        need(
            component["member_refinement_cell_count"] == 1
            and len(cell_ids) == 1
            and component["one_connected_positive_open_support"] is True
            and component[
                "strictly_disjoint_from_complete_conditional_base_atom_registry"
            ] is True
            and component["formal_new_occurrence_credit"] == 0
            and component["formal_component_credit"] == 0,
            "R292_SINGLE_CONNECTED_ENDPOINT_COMPONENT",
        )
        cell_id = cell_ids[0]
        need(cell_id not in used_cells, "R292_ENDPOINT_CELL_DISTINCTNESS")
        used_cells.add(cell_id)
        cell = cells_by_id[cell_id]
        verify_closed_row(cell, "R292_CELL:" + cell_id)
        need(
            cell["Round292_refined_new_support_component_id"]
            == component["Round292_refined_new_support_component_id"]
            and cell["Round287_potential_new_support_union_id"]
            == component["source_Round287_potential_new_support_union_id"]
            and cell["disposition"]
            == (
                "EXACT_UNCOVERED_POSITIVE_OPEN_SLICE__"
                "MEMBER_OF_REFINED_PARENT_LOCAL_NEW_SUPPORT"
            )
            and cell["exact_transformed_coordinate_system"] == "(t^2,p,s)"
            and cell["existing_occurrence_ids"] == []
            and cell["existing_occurrence_occupancy_count"] == 0
            and cell["formal_new_occurrence_credit"] == 0
            and cell["formal_component_credit"] == 0
            and cell["formal_DSU_rank_reduction_credit"] == 0,
            "R292_ENDPOINT_CELL_CHAIN",
        )
        result[occurrence] = {
            "occurrence_id": occurrence,
            "occurrence_content_preimage_sha256": preimage_hash,
            "component": component,
            "cell": cell,
            "box": qbox(cell["exact_transformed_open_cell"], "R292:" + cell_id),
        }
    need(len(result) == EXPECTED_ANCHORS, "R292_ANCHOR_COUNT")
    return result


def load_r294_occurrence_rows(
    anchors: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    path = D / R294_REGISTRY_LEDGER
    require_regular(path, R294_REGISTRY_LEDGER)
    found: dict[str, dict[str, Any]] = {}
    scan_count = 0
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        for row in iter_json_array(stream, '"rows":['):
            scan_count += 1
            occurrence = row.get("registry_occurrence_id")
            if occurrence not in anchors:
                continue
            need(occurrence not in found, "R294_REQUIRED_OCCURRENCE_DUPLICATE")
            verify_closed_row(row, "R294_OCCURRENCE:" + occurrence)
            anchor = anchors[occurrence]
            component = anchor["component"]
            cell = anchor["cell"]
            need(
                row["registry_entry_kind"]
                == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
                and row["source_row_id"]
                == component["Round292_refined_new_support_component_id"]
                and row["source_row_sha256"] == component["row_sha256"]
                and row["registry_identity_status"]
                == "FORMALLY_ISSUED_ROUND294_ATOMIC_OCCURRENCE_ID"
                and row["registry_promotion_status"]
                == "FORMALLY_PROMOTED_ROUND294_ATOMIC_OCCURRENCE_REGISTRY"
                and row["formal_new_expanded_occurrence_credit"] == 1
                and row["formal_component_union_credit"] == 0
                and row["formal_DSU_rank_reduction_credit"] == 0
                and row["member_refinement_cell_count"] == 1
                and row["member_refinement_cells"][0][
                    "Round292_refinement_cell_id"
                ] == cell["Round292_R287_existing_overlap_refinement_cell_id"]
                and row["occurrence_id_content_preimage_sha256"]
                == occurrence.split(":", 1)[1]
                == anchor["occurrence_content_preimage_sha256"]
                and row["official_key_id"] is None
                and row["official_key_ordinal"] is None
                and row["official_key_binding_status"]
                == (
                    "NOT_MATERIALIZED_IN_R287_FROZEN_LEDGER__"
                    "COMPLETE_SIGNATURE_HASH_PINNED"
                ),
                "R294_EXACT_TWO_STAGE_OCCURRENCE_BINDING",
            )
            found[occurrence] = row
    need(
        scan_count == 431_208 and set(found) == set(anchors),
        "R294_COMPLETE_REGISTRY_SCAN_AND_COVERAGE",
    )
    return found


def load_round304_endpoint_members(
    residual: list[dict[str, Any]], endpoints: set[str],
) -> dict[str, dict[str, Any]]:
    expected: dict[str, tuple[str, str, str]] = {}
    for row in residual:
        for side in ("left", "right"):
            occurrence = row[side + "_Round294_registry_occurrence_id"]
            value = (
                row[side + "_Round304_member_row_id"],
                row[side + "_Round304_member_row_sha256"],
                row[side + "_final_component_id"],
            )
            prior = expected.setdefault(occurrence, value)
            need(prior == value, "ROUND305A_ENDPOINT_MEMBER_BINDING_CONSISTENCY")
    need(set(expected) == endpoints, "ROUND305A_ENDPOINT_MEMBER_SCOPE")
    found: dict[str, dict[str, Any]] = {}
    count = 0
    path = D / R304_MEMBER_LEDGER
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        for row in iter_json_array(stream, '"fresh_member_component_rows":['):
            count += 1
            occurrence = row.get("registry_occurrence_id")
            if occurrence not in endpoints:
                continue
            need(occurrence not in found, "ROUND304_ENDPOINT_MEMBER_DUPLICATE")
            verify_closed_row(row, "ROUND304_MEMBER:" + occurrence)
            row_id, row_hash, component_id = expected[occurrence]
            need(
                row["Round304_fresh_member_component_row_id"] == row_id
                and row["row_sha256"] == row_hash
                and row["final_component_id"] == component_id
                and row["base_root_id"] == occurrence
                and row["member_identity_preserved"] is True
                and type(row["official_key_id"]) is str
                and row["formal_maximality_credit"] == 0
                and row["formal_fibre_credit"] == 0
                and row["formal_global_disposition_credit"] == 0,
                "ROUND304_EXACT_ENDPOINT_MEMBER_BINDING",
            )
            found[occurrence] = row
    need(
        count == EXPECTED_R304_MEMBERS and set(found) == endpoints,
        "ROUND304_COMPLETE_MEMBER_SCAN_AND_ENDPOINT_COVERAGE",
    )
    return found


def direct_scope_to_r292_p_brackets(
    residual: list[dict[str, Any]], endpoints: set[str],
) -> dict[str, Any]:
    """Rebuild the fixed 1,024-row direct geometry kernel without output."""

    bindings = load_r300a_bindings(residual)
    _r287_pairs, r287_regions, r287_unions = load_r287_scope(bindings)
    anchors = load_r292_anchors(endpoints)
    required_region_ids = {
        item[key]
        for item in bindings
        for key in ("left_region_id", "right_region_id")
    }
    regions = load_r275_regions(required_region_ids)
    guard_ids = {item["source"]["source_guard_row_id"] for item in bindings}
    guards = load_r174_guards(guard_ids)
    r174, r179, flint, stale_pyc_attack = load_interval_runtime()
    need(
        stale_pyc_attack == {
            "same_mtime": True,
            "same_size": True,
            "conventional_stale_pyc_attack_effective": True,
            "cacheless_source_compile_exec_returned_fresh_value": True,
            "stale_pyc_influenced_formal_runtime": False,
            "temporary_pyc_written": True,
            "temporary_pyc_read": True,
            "temporary_pyc_removed": True,
        },
        "CACHELESS_STALE_PYC_ATTACK_EXACT_RESULT",
    )
    r174_inputs = r174.load_inputs()
    # load_inputs() intentionally replays Round174 at its historical atlas
    # precision.  Restore the stronger Round305B context before constructing
    # any new interval geometry or dynamic signatures.
    flint.ctx.prec = 768
    need(flint.ctx.prec == 768, "ARB_PRECISION_768_BEFORE_DIRECT_GEOMETRY")
    registry_tables = r174.registry_tables(r174_inputs["gate5"])
    need(flint.ctx.prec == 768, "ARB_PRECISION_768_AFTER_REGISTRY_TABLES")

    cache: dict[tuple[str, tuple[Q, ...], int], dict[str, Any]] = {}
    records: list[dict[str, Any]] = []
    transition_histogram: Counter[str] = Counter()
    function_histogram: Counter[str] = Counter()
    bracket_depth_histogram: Counter[int] = Counter()
    source_factor_histogram: Counter[str] = Counter()
    derivative_histogram: Counter[str] = Counter()
    dynamic_reason_histogram: Counter[str] = Counter()
    minimum_z = Q(1)
    maximum_z = Q(0)

    for item in bindings:
        source = item["source"]
        left_region = regions[item["left_region_id"]]
        right_region = regions[item["right_region_id"]]
        left_r287 = r287_regions[item["left_region_id"]]
        right_r287 = r287_regions[item["right_region_id"]]
        left_anchor = anchors[item["left_endpoint"]]
        right_anchor = anchors[item["right_endpoint"]]
        for field in (
            "source_guard_row_id", "parent_id", "owner_target",
            "source_chart", "adjacent_chart", "adjacent_rational_region_box",
            "exact_coordinate_identity", "active_reason",
            "strict_derivative_signs_t_p_s",
        ):
            need(left_region[field] == right_region[field],
                 "R275_PAIRED_FIELD:" + field)
        need(
            left_region["arrangement_classification"]
            == right_region["arrangement_classification"]
            == "REGULAR_GRAPH_CROSSING"
            and sorted((
                left_region["active_factor_side_sign"],
                right_region["active_factor_side_sign"],
            )) == ["STRICT_NEGATIVE", "STRICT_POSITIVE"]
            and left_region["source_guard_row_id"]
            == source["source_guard_row_id"]
            and left_region["adjacent_chart"] == source["adjacent_chart"]
            and left_region["active_reason"] == source["active_reason"],
            "R275_PAIRED_GRAPH_BINDING",
        )
        for side, anchor, region_id, r287_region in (
            ("LEFT", left_anchor, item["left_region_id"], left_r287),
            ("RIGHT", right_anchor, item["right_region_id"], right_r287),
        ):
            cell = anchor["cell"]
            component = anchor["component"]
            union = r287_unions[
                r287_region["Round287_potential_new_support_union_id"]
            ]
            need(
                cell["Round275_region_id"] == region_id
                and cell["Round287_potential_new_support_union_id"]
                == r287_region["Round287_potential_new_support_union_id"]
                == union["Round287_potential_new_support_union_id"]
                and component["source_Round287_potential_new_support_union_id"]
                == union["Round287_potential_new_support_union_id"],
                "R292_TO_R287_TO_R275_ANCHOR:" + side,
            )
        need(left_anchor["box"] == right_anchor["box"],
             "PAIR_ENDPOINT_R292_SINGLE_CELL_EQUALITY")
        common_box = left_anchor["box"]
        core_box = strict_quarter_inset_core(common_box)
        z_interval = common_box[:2]
        need(Q(0) < z_interval[0] < z_interval[1] < Q(1, 2),
             "STRICT_R292_Z_INTERIOR")
        minimum_z = min(minimum_z, z_interval[0])
        maximum_z = max(maximum_z, z_interval[1])

        guard = guards[source["source_guard_row_id"]]
        guard_box = qbox(guard["box"], "R174_GUARD")
        adjacent_box = qbox(
            left_region["adjacent_rational_region_box"], "R275_ADJACENT",
        )
        exact_z = physical_t_square_interval(adjacent_box, guard_box)
        exact_transformed_box = (*exact_z, *adjacent_box[2:])
        need(
            common_box == exact_transformed_box
            and list(map(qstr, exact_z))
            == left_r287["physical_t_square_open_interval"]
            == right_r287["physical_t_square_open_interval"]
            and guard["chart"] == left_region["source_chart"]
            and guard["parent_id"] == left_region["parent_id"]
            and guard["classification"]
            == "STRICT_OUTSIDE_THIS_TRUE_DOMINANT_SOURCE_CHART"
            and guard["is_CM2_exterior_sheet_exclusion"] is False
            and guard["is_Gate5_geometric_disposition"] is False
            and left_region["exact_coordinate_identity"]
            == "image_t^2=1-source_t^2; p'=p; s'=s",
            "DIRECT_EXACT_RECHART_R292_CELL",
        )

        source_sign = 1 if guard_box[0] > 0 else -1
        image_sign = left_r287["physical_t_sign"]
        need(
            image_sign == right_r287["physical_t_sign"]
            == (1 if adjacent_box[0] > 0 else -1),
            "R287_IMAGE_T_SIGN",
        )
        source_cell = left_region["source_chart"].split(":")[1]
        adjacent_cell = left_region["adjacent_chart"].split(":")[1]
        need(
            TRANSITION[(source_cell, source_sign)]
            == (adjacent_cell, image_sign)
            and source_normal(source_cell, source_sign)
            == adjacent_normal(adjacent_cell, image_sign),
            "EXACT_BRANCH_TRANSPORT_NORMAL_IDENTITY",
        )
        transition = (
            f"{source_cell}{'+' if source_sign > 0 else '-'}->"
            f"{adjacent_cell}{'+' if image_sign > 0 else '-'}"
        )
        transition_histogram[transition] += 1

        left_factor = factor_descriptor(left_region)
        right_factor = factor_descriptor(right_region)
        need(
            left_factor["active_function_id"]
            == right_factor["active_function_id"]
            and left_factor["desired_side_sign"]
            != right_factor["desired_side_sign"]
            and left_region["strict_derivative_signs_t_p_s"][1]
            in {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
            "COMMON_STRICT_P_ACTIVE_FACTOR",
        )
        function_key = left_factor["active_function_id"] + f"|{image_sign}"
        function_histogram[function_key] += 1

        whole_box = r179.r174.atlas.AtlasBox(
            *adjacent_box, 0, "round305b-whole-R275-cell"
        )
        whole_geometry = r179.interval_geometry(
            left_region["adjacent_chart"], left_region["owner_target"], whole_box,
        )
        axis = left_region["active_reason"].split(":")[1]
        source_factor = whole_geometry[
            "source_x" if axis == "X" else "source_y"
        ]
        source_factor_sign = r179.sign(source_factor[0])
        target_factor = active_dual(
            whole_geometry, left_region["active_reason"], flint.arb,
        )
        target_factor_sign = r179.sign(target_factor[0])
        derivative_signs = [
            None if value is None else r179.sign(value)
            for value in target_factor[1]
        ]
        resolved_signature, unresolved_reasons = r174.dynamic_signature(
            left_region["adjacent_chart"], whole_box,
            left_region["owner_target"], registry_tables,
        )
        whole_product_replay = wall_event_product_replay(
            common_box, image_sign, left_region, r179, flint, "whole-cell",
        )
        need(
            source_factor_sign
            == whole_product_replay["source_wall_factor_sign"]
            in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
            and target_factor_sign == "OVERWRAP"
            == whole_product_replay["target_wall_factor_sign"]
            == whole_product_replay["wall_event_product_sign"]
            and derivative_signs
            == left_region["strict_derivative_signs_t_p_s"]
            and resolved_signature is None
            and unresolved_reasons == [left_region["active_reason"]],
            "DISCARDED_SOURCE_NONZERO_TARGET_MONOTONE_BRANCH",
        )
        source_factor_histogram[source_factor_sign] += 1
        derivative_histogram["|".join(derivative_signs)] += 1
        dynamic_reason_histogram[unresolved_reasons[0]] += 1

        left_piece = {
            "region_id": item["left_region_id"],
            "physical_t_sign": image_sign,
            "endpoint_occurrence_id": item["left_endpoint"],
        }
        right_piece = {
            "region_id": item["right_region_id"],
            "physical_t_sign": image_sign,
            "endpoint_occurrence_id": item["right_endpoint"],
        }
        initial_left = active_factor_replay(
            left_piece, common_box, regions, r179, flint, cache,
        )
        initial_right = active_factor_replay(
            right_piece, common_box, regions, r179, flint, cache,
        )
        need(
            initial_left["signed_support_state"]
            == initial_right["signed_support_state"]
            == "CLIPPED_DESIRED_SIDE_SUPPORT",
            "R292_SINGLE_CELL_ACTIVE_FACTOR_CLIPPED",
        )

        selected: dict[str, Any] | None = None
        for depth in (1, 2):
            lower_interval = targeted_interval(
                common_box[2], common_box[3], "LOWER", depth,
            )
            upper_interval = targeted_interval(
                common_box[2], common_box[3], "UPPER", depth,
            )
            lower_box = replace_axis(common_box, 1, lower_interval)
            upper_box = replace_axis(common_box, 1, upper_interval)
            left_lower = active_factor_replay(
                left_piece, lower_box, regions, r179, flint, cache,
            )
            left_upper = active_factor_replay(
                left_piece, upper_box, regions, r179, flint, cache,
            )
            if {
                left_lower["signed_support_state"],
                left_upper["signed_support_state"],
            } != {
                "FULL_DESIRED_SIDE_SUPPORT",
                "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL",
            }:
                continue
            right_lower = active_factor_replay(
                right_piece, lower_box, regions, r179, flint, cache,
            )
            right_upper = active_factor_replay(
                right_piece, upper_box, regions, r179, flint, cache,
            )
            need(
                {
                    right_lower["signed_support_state"],
                    right_upper["signed_support_state"],
                } == {
                    "FULL_DESIRED_SIDE_SUPPORT",
                    "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL",
                }
                and (
                    left_lower["signed_support_state"]
                    == "FULL_DESIRED_SIDE_SUPPORT"
                ) == (
                    right_lower["signed_support_state"]
                    == "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
                )
                and (
                    left_upper["signed_support_state"]
                    == "FULL_DESIRED_SIDE_SUPPORT"
                ) == (
                    right_upper["signed_support_state"]
                    == "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
                ),
                "RIGHT_COMPLEMENTARY_P_BRACKET",
            )
            lower_p = sum(lower_interval, Q(0)) / 2
            upper_p = sum(upper_interval, Q(0)) / 2
            full_lower_face = replace_axis(common_box, 1, (lower_p, lower_p))
            full_upper_face = replace_axis(common_box, 1, (upper_p, upper_p))
            lower_face = replace_axis(core_box, 1, (lower_p, lower_p))
            upper_face = replace_axis(core_box, 1, (upper_p, upper_p))
            faces = {
                "left_lower": active_factor_replay(
                    left_piece, lower_face, regions, r179, flint, cache,
                ),
                "left_upper": active_factor_replay(
                    left_piece, upper_face, regions, r179, flint, cache,
                ),
                "right_lower": active_factor_replay(
                    right_piece, lower_face, regions, r179, flint, cache,
                ),
                "right_upper": active_factor_replay(
                    right_piece, upper_face, regions, r179, flint, cache,
                ),
            }
            full_faces = {
                "left_lower": active_factor_replay(
                    left_piece, full_lower_face, regions, r179, flint, cache,
                ),
                "left_upper": active_factor_replay(
                    left_piece, full_upper_face, regions, r179, flint, cache,
                ),
                "right_lower": active_factor_replay(
                    right_piece, full_lower_face, regions, r179, flint, cache,
                ),
                "right_upper": active_factor_replay(
                    right_piece, full_upper_face, regions, r179, flint, cache,
                ),
            }
            need(
                faces["left_lower"]["signed_support_state"]
                == left_lower["signed_support_state"]
                and faces["left_upper"]["signed_support_state"]
                == left_upper["signed_support_state"]
                and faces["right_lower"]["signed_support_state"]
                == right_lower["signed_support_state"]
                and faces["right_upper"]["signed_support_state"]
                == right_upper["signed_support_state"]
                and all(
                    faces[key]["signed_support_state"]
                    == full_faces[key]["signed_support_state"]
                    for key in faces
                ),
                "EXACT_RATIONAL_CORE_P_FACE_REPLAY",
            )
            lower_owner = (
                (left_piece, left_lower)
                if left_lower["signed_support_state"]
                == "FULL_DESIRED_SIDE_SUPPORT"
                else (right_piece, right_lower)
            )
            upper_owner = (
                (left_piece, left_upper)
                if left_upper["signed_support_state"]
                == "FULL_DESIRED_SIDE_SUPPORT"
                else (right_piece, right_upper)
            )
            lower_corridor = replace_axis(
                core_box, 1, (lower_p, lower_interval[1]),
            )
            upper_corridor = replace_axis(
                core_box, 1, (upper_interval[0], upper_p),
            )
            lower_inner = active_factor_replay(
                lower_owner[0], lower_corridor, regions, r179, flint, cache,
            )
            upper_inner = active_factor_replay(
                upper_owner[0], upper_corridor, regions, r179, flint, cache,
            )
            need(
                lower_inner["signed_support_state"]
                == upper_inner["signed_support_state"]
                == "FULL_DESIRED_SIDE_SUPPORT"
                and lower_owner[0]["endpoint_occurrence_id"]
                != upper_owner[0]["endpoint_occurrence_id"]
                and all(
                    common_box[2 * axis] < corridor[2 * axis]
                    < corridor[2 * axis + 1] < common_box[2 * axis + 1]
                    for corridor in (lower_corridor, upper_corridor)
                    for axis in range(3)
                ),
                "TWO_SIDED_POSITIVE_VOLUME_CORRIDOR_REPLAY",
            )
            lower_product = wall_event_product_replay(
                lower_face, image_sign, left_region, r179, flint,
                "core-lower-p-face",
            )
            upper_product = wall_event_product_replay(
                upper_face, image_sign, left_region, r179, flint,
                "core-upper-p-face",
            )
            for face_name, product_replay in (
                ("left_lower", lower_product),
                ("left_upper", upper_product),
            ):
                target_sign = faces[face_name]["active_factor_extremal_signs"][0]
                need(
                    faces[face_name]["active_factor_extremal_signs"]
                    == [target_sign, target_sign]
                    and product_replay["source_wall_factor_sign"]
                    == source_factor_sign
                    and product_replay["target_wall_factor_sign"] == target_sign
                    and product_replay["wall_event_product_sign"]
                    == (
                        "STRICT_POSITIVE"
                        if product_replay["source_wall_factor_sign"] == target_sign
                        else "STRICT_NEGATIVE"
                    ),
                    "CORE_FACE_EXPLICIT_WALL_PRODUCT_REPLAY",
                )
            selected = {
                "bracket_slice_depth": depth,
                "lower_p": qstr(lower_p),
                "upper_p": qstr(upper_p),
                "lower_interval": qlist(lower_interval),
                "upper_interval": qlist(upper_interval),
                "lower_owner_endpoint":
                    lower_owner[0]["endpoint_occurrence_id"],
                "upper_owner_endpoint":
                    upper_owner[0]["endpoint_occurrence_id"],
                "face_replays": {
                    key: {
                        "active_factor_extremal_signs":
                            value["active_factor_extremal_signs"],
                        "signed_support_state": value["signed_support_state"],
                    }
                    for key, value in sorted(faces.items())
                },
                "full_base_face_states_match_core_face_states": True,
                "core_face_wall_event_product_replays": {
                    "lower": lower_product,
                    "upper": upper_product,
                },
                "lower_corridor_inner_box": qlist(lower_corridor),
                "upper_corridor_inner_box": qlist(upper_corridor),
                "corridors_strictly_inside_R292_open_cell": True,
                "corridor_box_used_as_Gamma_intersection": False,
            }
            break
        need(selected is not None, "DEPTH_1_OR_2_P_BRACKET_REQUIRED")
        bracket_depth_histogram[selected["bracket_slice_depth"]] += 1

        payload = {
            "schema": SCHEMA + ".direct-r292-p-bracket-preflight.v1",
            "canonical_occurrence_pair": item["pair"],
            "source_Round305A_row_id":
                item["scope"]["Round305A_scope_reprojection_row_id"],
            "source_Round305A_row_sha256": item["scope"]["row_sha256"],
            "source_Round300A_row_id":
                item["canonical"]["Round300A_canonical_occurrence_pair_row_id"],
            "source_Round300A_row_sha256": item["canonical"]["row_sha256"],
            "source_Round287_pair_row_id": item["source_Round287_pair_row_id"],
            "source_Round287_pair_row_sha256":
                item["source"]["source_Round287_pair_row_sha256"],
            "left_Round275_region_id": item["left_region_id"],
            "right_Round275_region_id": item["right_region_id"],
            "left_R292_cell_id": left_anchor["cell"][
                "Round292_R287_existing_overlap_refinement_cell_id"
            ],
            "left_R292_cell_row_sha256": left_anchor["cell"]["row_sha256"],
            "right_R292_cell_id": right_anchor["cell"][
                "Round292_R287_existing_overlap_refinement_cell_id"
            ],
            "right_R292_cell_row_sha256": right_anchor["cell"]["row_sha256"],
            "both_R292_components_have_exactly_one_member_cell": True,
            "left_and_right_exact_R292_cells_identical": True,
            "exact_transformed_open_cell_t2_p_s": qlist(common_box),
            "source_guard_row_id": source["source_guard_row_id"],
            "source_guard_box_t_p_s": qlist(guard_box),
            "source_chart": left_region["source_chart"],
            "adjacent_chart": left_region["adjacent_chart"],
            "chart_transition": transition,
            "physical_t_sign": image_sign,
            "source_and_adjacent_physical_normals_symbolically_identical": True,
            "owner_target": left_region["owner_target"],
            "active_reason": left_region["active_reason"],
            "active_function_id": left_factor["active_function_id"],
            "active_function_identity_payload":
                left_factor["active_function_identity_payload"],
            "discarded_source_factor_strict_sign": source_factor_sign,
            "whole_cell_wall_event_product_replay": whole_product_replay,
            "target_factor_whole_cell_sign": target_factor_sign,
            "target_factor_derivative_signs_t_p_s": derivative_signs,
            "only_unresolved_dynamic_predicate": unresolved_reasons[0],
            "all_other_dynamic_signature_predicates_strict": True,
            "implicit_graph_axis": "p",
            "tangent_refinement_depth": 0,
            "support_open_base_z_s": qlist((
                common_box[0], common_box[1], common_box[4], common_box[5],
            )),
            "proof_closed_core_base_z_s": qlist((
                core_box[0], core_box[1], core_box[4], core_box[5],
            )),
            "owner_contact_closure_base_z_s": qlist((
                common_box[0], common_box[1], common_box[4], common_box[5],
            )),
            "proof_core_inset_rule": "QUARTER_EACH_TANGENT_SIDE",
            "proof_core_strictly_inside_R292_open_base": True,
            "owner_contact_closure_is_zero_credit_full_closure_extension": True,
            **selected,
            "D4_transfer_used": False,
            "formal_Round305B_credit": 0,
        }
        record_id = "round305b-direct-p-bracket:" + digest([
            "ROUND305B_DIRECT_R292_SINGLE_CELL_P_BRACKET_V1", payload,
        ])
        record = {"Round305B_direct_p_bracket_row_id": record_id, **payload}
        record["row_sha256"] = digest(record)
        records.append(record)

    records.sort(key=lambda row: row["canonical_occurrence_pair"])
    need(
        len(records) == EXPECTED_WITNESSES
        and bracket_depth_histogram == {1: 320, 2: 704}
        and len(transition_histogram) == 8
        and set(transition_histogram.values()) == {128}
        and len(function_histogram) == 8
        and set(function_histogram.values()) == {128}
        and maximum_z < Q(1, 2),
        "DIRECT_FIXED_SCOPE_CENSUS",
    )
    return {
        "status": (
            "PASS_DIRECT_SCOPE_TO_R292_SINGLE_CELL_TO_DEPTH_1_2_P_BRACKET_"
            "RECONSTRUCTION__NO_OUTPUT__ZERO_CREDIT"
        ),
        "runtime_closure": cacheless_runtime_closure(),
        "direct_row_count": len(records),
        "direct_rows_sha256": digest(records),
        "direct_row_ids_sha256": digest([
            row["Round305B_direct_p_bracket_row_id"] for row in records
        ]),
        "direct_row_hashes_sha256": digest([
            row["row_sha256"] for row in records
        ]),
        "R292_anchor_count": len(anchors),
        "R292_single_member_component_count": len(anchors),
        "left_right_identical_R292_cell_pair_count": len(records),
        "candidate_piece_pair_count": len(records),
        "serializer_attempt_count": len(records),
        "implicit_graph_axis_histogram": {"p": len(records)},
        "tangent_refinement_depth_histogram": {"0": len(records)},
        "bracket_slice_depth_histogram": {
            str(key): value for key, value in sorted(bracket_depth_histogram.items())
        },
        "chart_transition_histogram": dict(sorted(transition_histogram.items())),
        "active_function_and_image_sign_histogram":
            dict(sorted(function_histogram.items())),
        "discarded_source_factor_sign_histogram":
            dict(sorted(source_factor_histogram.items())),
        "target_factor_derivative_histogram":
            dict(sorted(derivative_histogram.items())),
        "only_unresolved_dynamic_predicate_histogram":
            dict(sorted(dynamic_reason_histogram.items())),
        "minimum_z": qstr(minimum_z),
        "maximum_z": qstr(maximum_z),
        "maximum_z_strictly_below_one_half": True,
        "D4_transfer_enabled": False,
        "formal_Round305B_credit": 0,
        "records": records,
        "_bindings": bindings,
        "_r287_regions": r287_regions,
        "_r287_unions": r287_unions,
        "_anchors": anchors,
        "_regions": regions,
        "_guards": guards,
        "_r174": r174,
        "_r179": r179,
        "_flint": flint,
    }


def no_write_geometry_preflight() -> dict[str, Any]:
    wire_files = admit_normative_wire_files()
    manifests = admit_sealed_inputs()
    residual, endpoints = read_r305a_scope()
    official = project_official_keys(residual, endpoints)
    direct = direct_scope_to_r292_p_brackets(residual, endpoints)
    audit = {
        key: value
        for key, value in direct.items()
        if key != "records" and not key.startswith("_")
    }
    audit["manifest_member_counts"] = {
        key: len(value) for key, value in manifests.items()
    }
    audit["official_key_audit"] = official
    audit["normative_wire_files"] = wire_files
    audit["formal_geometry_kernel_implemented"] = (
        FORMAL_GEOMETRY_KERNEL_IMPLEMENTED
    )
    audit["direct_geometry_kernel_implemented"] = (
        DIRECT_GEOMETRY_KERNEL_IMPLEMENTED
    )
    audit["formal_physical_witness_credit"] = 0
    audit["formal_component_edge_credit"] = 0
    audit["formal_DSU_rank_reduction_credit"] = 0
    return audit


def interval_relation(
    left: tuple[Q, Q], right: tuple[Q, Q],
) -> str:
    overlap = min(left[1], right[1]) - max(left[0], right[0])
    if overlap > 0:
        return "POSITIVE"
    if overlap == 0:
        return "BOUNDARY"
    return "DISJOINT"


def rectangle_relation(
    left: tuple[Q, Q, Q, Q], right: tuple[Q, Q, Q, Q],
) -> str:
    z_relation = interval_relation(left[:2], right[:2])
    s_relation = interval_relation(left[2:], right[2:])
    if z_relation == s_relation == "POSITIVE":
        return "POSITIVE_AREA_OVERLAP"
    if z_relation != "DISJOINT" and s_relation != "DISJOINT":
        return "BOUNDARY_ONLY_CONTACT"
    return "DISJOINT"


def close_row(payload: dict[str, Any], id_field: str) -> dict[str, Any]:
    need(id_field in payload and "row_sha256" not in payload,
         "CLOSE_ROW_CONTRACT:" + id_field)
    row = dict(payload)
    row["row_sha256"] = digest(row)
    return row


def closed_ledger(
    schema: str, rows: list[dict[str, Any]], id_field: str,
) -> dict[str, Any]:
    ledger = {
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
    ledger["ledger_sha256"] = digest(ledger)
    return ledger


def build_contact_and_owner_rows(
    direct_rows: list[dict[str, Any]],
    witness_id_by_pair: dict[tuple[str, str], str],
    owner_extension_id_by_pair: dict[tuple[str, str], str],
    regions: dict[str, dict[str, Any]],
    r179: Any,
    flint: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    patches: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for row in direct_rows:
        pair = tuple(row["canonical_occurrence_pair"])
        witness_id = witness_id_by_pair[pair]
        patches[(row["active_function_id"], row["physical_t_sign"])].append({
            "witness_id": witness_id,
            "owner_extension_patch_id": owner_extension_id_by_pair[pair],
            "base": tuple(map(Q, row["owner_contact_closure_base_z_s"])),
            "p_bracket": (Q(row["lower_p"]), Q(row["upper_p"])),
            "region_id": row["left_Round275_region_id"],
            "derivative_sign": row["target_factor_derivative_signs_t_p_s"][1],
            "active_function_id": row["active_function_id"],
            "physical_t_sign": row["physical_t_sign"],
        })
    need(len(patches) == 8 and {len(group) for group in patches.values()} == {128},
         "OWNER_EIGHT_PATCH_GROUPS")

    relation_histogram: Counter[str] = Counter()
    dimension_histogram: Counter[int] = Counter()
    derivative_histogram: Counter[str] = Counter()
    contact_specs: list[dict[str, Any]] = []
    for group_key, group in sorted(patches.items()):
        group.sort(key=lambda patch: patch["witness_id"])
        for index, left in enumerate(group):
            for right in group[index + 1:]:
                relation = rectangle_relation(left["base"], right["base"])
                relation_histogram[relation] += 1
                if relation != "BOUNDARY_ONLY_CONTACT":
                    continue
                z_intersection = (
                    max(left["base"][0], right["base"][0]),
                    min(left["base"][1], right["base"][1]),
                )
                s_intersection = (
                    max(left["base"][2], right["base"][2]),
                    min(left["base"][3], right["base"][3]),
                )
                dimension = int(z_intersection[0] < z_intersection[1]) + int(
                    s_intersection[0] < s_intersection[1]
                )
                need(dimension in {0, 1}, "CONTACT_BASE_DIMENSION")
                dimension_histogram[dimension] += 1
                p_hull = (
                    min(left["p_bracket"][0], right["p_bracket"][0]),
                    max(left["p_bracket"][1], right["p_bracket"][1]),
                )
                need(p_hull[0] < p_hull[1], "CONTACT_POSITIVE_P_HULL")
                t_outer = signed_sqrt_outer(
                    z_intersection, left["physical_t_sign"],
                )
                boundary_box = r179.r174.atlas.AtlasBox(
                    t_outer[0], t_outer[1], p_hull[0], p_hull[1],
                    s_intersection[0], s_intersection[1], 0,
                    "round305b-global-owner-boundary",
                )
                region = regions[left["region_id"]]
                geometry = r179.interval_geometry(
                    region["adjacent_chart"], region["owner_target"],
                    boundary_box,
                )
                derivative_sign = r179.sign(active_dual(
                    geometry, region["active_reason"], flint.arb,
                )[1][1])
                need(
                    derivative_sign
                    in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
                    and derivative_sign == left["derivative_sign"]
                    == right["derivative_sign"],
                    "CONTACT_STRICT_COMMON_P_DERIVATIVE",
                )
                derivative_histogram[derivative_sign] += 1
                witness_ids = sorted((left["witness_id"], right["witness_id"]))
                extension_ids = sorted((
                    left["owner_extension_patch_id"],
                    right["owner_extension_patch_id"],
                ))
                exact_base = qlist((
                    z_intersection[0], z_intersection[1],
                    s_intersection[0], s_intersection[1],
                ))
                contact_kind = (
                    "OWNER_EXTENSION_BASE_FACE_CONTACT" if dimension == 1
                    else "OWNER_EXTENSION_FOUR_PATCH_VERTEX_DIAGONAL_PAIR"
                )
                locus_kind = "FACE" if dimension == 1 else "VERTEX"
                locus_key = (
                    locus_kind, group_key[0], group_key[1], *exact_base,
                )
                contact_id = "round305b-closure-contact:" + digest([
                    "ROUND305B_PAIRWISE_OWNER_EXTENSION_CLOSURE_CONTACT_V1",
                    extension_ids,
                    exact_base, qlist(p_hull),
                ])
                if dimension == 0:
                    owner_locus_id = "round305b-owner-locus:" + digest([
                        "ROUND305B_GLOBAL_OWNER_EXTENSION_VERTEX_LOCUS_V1",
                        list(group_key), exact_base,
                    ])
                else:
                    owner_locus_id = "round305b-owner-locus:" + digest([
                        "ROUND305B_OWNER_EXTENSION_FACE_RELATIVE_INTERIOR_LOCUS_V1",
                        list(group_key), exact_base, contact_id,
                    ])
                contact_specs.append({
                    "contact_id": contact_id,
                    "associated_physical_witness_row_ids": witness_ids,
                    "contact_pair_owner_extension_patch_ids": extension_ids,
                    "contact_kind": contact_kind,
                    "base_dimension": dimension,
                    "exact_common_base_z_s": exact_base,
                    "common_p_bracket_hull": qlist(p_hull),
                    "derivative_sign": derivative_sign,
                    "locus_key": locus_key,
                    "owner_locus_id": owner_locus_id,
                    "group_key": group_key,
                })
    need(
        relation_histogram
        == {"DISJOINT": 61_488, "BOUNDARY_ONLY_CONTACT": 3_536}
        and dimension_histogram
        == {0: EXPECTED_DIAGONAL_CONTACTS, 1: EXPECTED_FACE_CONTACTS}
        and len({row["contact_id"] for row in contact_specs})
        == EXPECTED_CLOSURE_CONTACTS,
        "CONTACT_EXACT_CENSUS",
    )

    face_specs = [row for row in contact_specs if row["base_dimension"] == 1]
    vertex_specs = [row for row in contact_specs if row["base_dimension"] == 0]
    vertex_loci: dict[tuple[Any, ...], dict[str, Any]] = {}
    for spec in vertex_specs:
        entry = vertex_loci.setdefault(spec["locus_key"], {
            "owner_locus_id": spec["owner_locus_id"],
            "associated_witness_ids": set(),
            "incident_extension_ids": set(),
            "incident_contact_ids": set(),
            "base": spec["exact_common_base_z_s"],
        })
        entry["associated_witness_ids"].update(
            spec["associated_physical_witness_row_ids"]
        )
        entry["incident_extension_ids"].update(
            spec["contact_pair_owner_extension_patch_ids"]
        )
        entry["incident_contact_ids"].add(spec["contact_id"])
    need(len(vertex_loci) == EXPECTED_VERTEX_OWNER_LOCI,
         "VERTEX_LOCUS_COUNT")

    face_vertex_refs: dict[str, list[str]] = defaultdict(list)
    face_loci: dict[tuple[Any, ...], dict[str, Any]] = {}
    for spec in face_specs:
        face_loci[spec["locus_key"]] = {
            "owner_locus_id": spec["owner_locus_id"],
            "associated_witness_ids": set(
                spec["associated_physical_witness_row_ids"]
            ),
            "incident_extension_ids": set(
                spec["contact_pair_owner_extension_patch_ids"]
            ),
            "incident_contact_ids": {spec["contact_id"]},
            "base": spec["exact_common_base_z_s"],
        }
        base = tuple(map(Q, spec["exact_common_base_z_s"]))
        if base[0] < base[1]:
            endpoints = (
                (base[0], base[0], base[2], base[3]),
                (base[1], base[1], base[2], base[3]),
            )
        else:
            need(base[2] < base[3], "FACE_LOCUS_POSITIVE_AXIS")
            endpoints = (
                (base[0], base[1], base[2], base[2]),
                (base[0], base[1], base[3], base[3]),
            )
        for endpoint in endpoints:
            key = (
                "VERTEX", spec["group_key"][0], spec["group_key"][1],
                *qlist(endpoint),
            )
            vertex = vertex_loci.get(key)
            if vertex is None:
                continue
            face_vertex_refs[spec["owner_locus_id"]].append(
                vertex["owner_locus_id"]
            )
            vertex["associated_witness_ids"].update(
                spec["associated_physical_witness_row_ids"]
            )
            vertex["incident_extension_ids"].update(
                spec["contact_pair_owner_extension_patch_ids"]
            )
            vertex["incident_contact_ids"].add(spec["contact_id"])
    need(
        len(face_loci) == EXPECTED_FACE_OWNER_LOCI
        and sum(map(len, face_vertex_refs.values())) == 3_360,
        "FACE_TO_VERTEX_OVERRIDE_CENSUS",
    )
    need(
        all(
            len(row["incident_extension_ids"]) == 4
            and len(row["associated_witness_ids"]) == 4
            and len(row["incident_contact_ids"]) == 6
            for row in vertex_loci.values()
        )
        and sum(len(row["incident_contact_ids"]) for row in vertex_loci.values())
        == 5_040,
        "GLOBAL_FOUR_PATCH_VERTEX_OWNER_CLOSURE",
    )

    owner_rows: list[dict[str, Any]] = []
    for locus_key, entry in sorted(
        [*face_loci.items(), *vertex_loci.items()],
        key=lambda item: item[1]["owner_locus_id"],
    ):
        locus_kind = locus_key[0]
        associated_witnesses = sorted(entry["associated_witness_ids"])
        incident_extensions = sorted(entry["incident_extension_ids"])
        incident_contacts = sorted(entry["incident_contact_ids"])
        overrides = sorted(set(face_vertex_refs.get(entry["owner_locus_id"], [])))
        payload = {
            "Round305B_owner_locus_row_id": entry["owner_locus_id"],
            "schema": SCHEMA + ".owner-locus-row.v1",
            "locus_kind": (
                "FACE_RELATIVE_INTERIOR"
                if locus_kind == "FACE" else "FOUR_PATCH_VERTEX"
            ),
            "exact_locus_base_z_s": entry["base"],
            "associated_physical_witness_row_ids": associated_witnesses,
            "global_incident_owner_extension_patch_ids": incident_extensions,
            "global_incident_owner_extension_patch_count":
                len(incident_extensions),
            "incident_closure_contact_row_ids": incident_contacts,
            "lexicographically_least_global_incident_owner_extension_patch":
                min(incident_extensions),
            "face_endpoint_vertex_override_row_ids": overrides,
            "full_closure_extension_only": True,
            "not_Gamma_core_locus": True,
            "not_G3_G4_or_component_edge_basis": True,
            "D4_transfer_used": False,
        }
        need(set(payload) | {"row_sha256"} == set(OWNER_LOCUS_KEYS),
             "OWNER_LOCUS_SCHEMA_KEYS")
        owner_rows.append(close_row(payload, "Round305B_owner_locus_row_id"))
    owner_rows.sort(key=lambda row: row["Round305B_owner_locus_row_id"])
    need(
        len(owner_rows) == EXPECTED_OWNER_LOCI
        and Counter(
            row["global_incident_owner_extension_patch_count"]
            for row in owner_rows
        )
        == {2: EXPECTED_FACE_OWNER_LOCI, 4: EXPECTED_VERTEX_OWNER_LOCI},
        "OWNER_LOCUS_EXACT_CENSUS",
    )

    contact_rows: list[dict[str, Any]] = []
    for spec in sorted(contact_specs, key=lambda row: row["contact_id"]):
        payload = {
            "Round305B_closure_contact_row_id": spec["contact_id"],
            "schema": SCHEMA + ".closure-contact-row.v1",
            "associated_physical_witness_row_ids":
                spec["associated_physical_witness_row_ids"],
            "contact_pair_owner_extension_patch_ids":
                spec["contact_pair_owner_extension_patch_ids"],
            "contact_kind": spec["contact_kind"],
            "base_dimension": spec["base_dimension"],
            "exact_common_base_z_s": spec["exact_common_base_z_s"],
            "common_p_bracket_hull": spec["common_p_bracket_hull"],
            "strict_common_active_function_p_derivative_sign":
                spec["derivative_sign"],
            "owner_extension_root_unique_on_full_closure": True,
            "owner_locus_row_id": spec["owner_locus_id"],
            "full_closure_extension_only": True,
            "not_Gamma_core_contact": True,
            "not_G3_G4_or_component_edge_basis": True,
            "D4_transfer_used": False,
        }
        need(set(payload) | {"row_sha256"} == set(CLOSURE_CONTACT_KEYS),
             "CLOSURE_CONTACT_SCHEMA_KEYS")
        contact_rows.append(
            close_row(payload, "Round305B_closure_contact_row_id")
        )

    degree: Counter[str] = Counter()
    for row in contact_rows:
        degree.update(row["contact_pair_owner_extension_patch_ids"])
    degree_histogram = Counter(degree.values())
    need(
        len(degree) == EXPECTED_WITNESSES
        and degree_histogram == {3: 32, 5: 320, 8: 672},
        "PATCH_CONTACT_DEGREE_HISTOGRAM",
    )
    audit = {
        "within_group_base_relation_histogram": dict(sorted(relation_histogram.items())),
        "closure_contact_count": len(contact_rows),
        "closure_contact_kind_histogram": dict(sorted(Counter(
            row["contact_kind"] for row in contact_rows
        ).items())),
        "closure_contact_base_dimension_histogram": {
            str(key): value for key, value in sorted(dimension_histogram.items())
        },
        "closure_contact_derivative_histogram":
            dict(sorted(derivative_histogram.items())),
        "owner_locus_count": len(owner_rows),
        "owner_locus_kind_histogram": dict(sorted(Counter(
            row["locus_kind"] for row in owner_rows
        ).items())),
        "face_to_vertex_override_reference_count": 3_360,
        "vertex_incident_contact_reference_count": 5_040,
        "patch_contact_degree_histogram": {
            str(key): value for key, value in sorted(degree_histogram.items())
        },
        "global_four_patch_vertex_owner_replayed": True,
        "old_pairwise_minimum_owner_rejected": True,
        "owner_extension_full_closure_sidecar_only": True,
        "owner_extension_not_Gamma_core_contact_or_G3_G4_or_edge_basis": True,
    }
    return contact_rows, owner_rows, audit


def opposite_strict_sign(value: str) -> str:
    need(value in {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
         "FULL_SIGN_SIDE_STRICT_SIGN_DOMAIN")
    return (
        "STRICT_POSITIVE"
        if value == "STRICT_NEGATIVE"
        else "STRICT_NEGATIVE"
    )


def build_full_sign_side_to_rho_support_certificate(
    *,
    endpoint_side: str,
    endpoint_occurrence_id: str,
    region_id: str,
    region: dict[str, Any],
    r287_region: dict[str, Any],
    cell: dict[str, Any],
    component: dict[str, Any],
    direct_row: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    """Derive one V2 full-face-to-rho support certificate from sealed rows."""

    need(endpoint_side in {"LEFT", "RIGHT"},
         "FULL_SIGN_SIDE_ENDPOINT_SIDE")
    lower_endpoint = direct_row["lower_owner_endpoint"]
    upper_endpoint = direct_row["upper_owner_endpoint"]
    need(lower_endpoint != upper_endpoint,
         "FULL_SIGN_SIDE_DISTINCT_FACE_OWNERS")
    if endpoint_occurrence_id == lower_endpoint:
        owner_face = "LOWER"
        approach = "P_APPROACHES_RHO_FROM_BELOW"
        oriented_p_face = direct_row["lower_p"]
        corridor_box = direct_row["lower_corridor_inner_box"]
        exact_full_half_open_segment = "p_face<=p<rho(z,s)"
        face_sign_derivative_orientation = (
            "LOWER_FACE_SIGN_IS_OPPOSITE_DF_DP"
        )
    else:
        need(endpoint_occurrence_id == upper_endpoint,
             "FULL_SIGN_SIDE_ENDPOINT_FACE_OWNER_COVERAGE")
        owner_face = "UPPER"
        approach = "P_APPROACHES_RHO_FROM_ABOVE"
        oriented_p_face = direct_row["upper_p"]
        corridor_box = direct_row["upper_corridor_inner_box"]
        exact_full_half_open_segment = "rho(z,s)<p<=p_face"
        face_sign_derivative_orientation = "UPPER_FACE_SIGN_EQUALS_DF_DP"

    face_key = endpoint_side.lower() + "_" + owner_face.lower()
    face_replay = direct_row["face_replays"][face_key]
    face_signs = face_replay["active_factor_extremal_signs"]
    need(
        type(face_signs) is list
        and len(face_signs) == 2
        and face_signs[0] == face_signs[1]
        and face_signs[0] in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
        and face_replay["signed_support_state"]
        == "FULL_DESIRED_SIDE_SUPPORT",
        "FULL_SIGN_SIDE_EXACT_OWNER_FACE_REPLAY:" + endpoint_side,
    )
    exact_face_sign = face_signs[0]
    derivative_sign = direct_row["target_factor_derivative_signs_t_p_s"][1]
    need(
        derivative_sign == region["strict_derivative_signs_t_p_s"][1]
        and derivative_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
        "FULL_SIGN_SIDE_UNIFORM_WHOLE_CELL_DF_DP:" + endpoint_side,
    )

    def unique_owner_face_sign(face: str) -> str:
        replays = [
            direct_row["face_replays"][side.lower() + "_" + face.lower()]
            for side in ("LEFT", "RIGHT")
        ]
        owners = [
            replay for replay in replays
            if replay["signed_support_state"] == "FULL_DESIRED_SIDE_SUPPORT"
        ]
        need(len(owners) == 1,
             "FULL_SIGN_SIDE_UNIQUE_" + face + "_FACE_OWNER")
        signs = owners[0]["active_factor_extremal_signs"]
        need(
            type(signs) is list
            and len(signs) == 2
            and signs[0] == signs[1]
            and signs[0] in {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
            "FULL_SIGN_SIDE_" + face + "_FACE_STRICT_SIGN",
        )
        return signs[0]

    lower_face_sign = unique_owner_face_sign("LOWER")
    upper_face_sign = unique_owner_face_sign("UPPER")
    root_zero_derived = (
        lower_face_sign == opposite_strict_sign(derivative_sign)
        and upper_face_sign == derivative_sign
        and lower_face_sign != upper_face_sign
    )
    orientation_hard_checked = exact_face_sign == (
        opposite_strict_sign(derivative_sign)
        if owner_face == "LOWER"
        else derivative_sign
    )
    endpoint_side_matches_face = (
        region["active_factor_side_sign"] == exact_face_sign
    )
    signature_has_only_active_reason = (
        direct_row["target_factor_whole_cell_sign"] == "OVERWRAP"
        and direct_row["only_unresolved_dynamic_predicate"]
        == direct_row["active_reason"]
        == region["active_reason"]
    )
    all_other_predicates_strict = (
        direct_row["all_other_dynamic_signature_predicates_strict"] is True
        and direct_row["discarded_source_factor_strict_sign"]
        in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
    )

    cell_id = cell["Round292_R287_existing_overlap_refinement_cell_id"]
    component_id = component["Round292_refined_new_support_component_id"]
    exact_support_chain = (
        r287_region["Round275_region_id"] == region_id
        and r287_region["R275_region_kind"] == "REGULAR_GRAPH_CROSSING"
        and r287_region["disposition"]
        == "ONE_STRICTLY_NEW_DISJOINT_SUPPORT_CANDIDATE__ZERO_CREDIT"
        and cell["Round275_region_id"] == region_id
        and cell["Round292_refined_new_support_component_id"] == component_id
        and cell["disposition"]
        == (
            "EXACT_UNCOVERED_POSITIVE_OPEN_SLICE__"
            "MEMBER_OF_REFINED_PARENT_LOCAL_NEW_SUPPORT"
        )
        and component["member_refinement_cell_count"] == 1
        and component["member_refinement_cell_ids"] == [cell_id]
        and component["one_connected_positive_open_support"] is True
        and cell["exact_transformed_open_cell"]
        == direct_row["exact_transformed_open_cell_t2_p_s"]
    )
    common_box = tuple(map(
        Q, direct_row["exact_transformed_open_cell_t2_p_s"],
    ))
    corridor = tuple(map(Q, corridor_box))
    corridor_strictly_inside = (
        len(common_box) == len(corridor) == 6
        and all(
            common_box[2 * axis] < corridor[2 * axis]
            < corridor[2 * axis + 1] < common_box[2 * axis + 1]
            for axis in range(3)
        )
        and direct_row["corridors_strictly_inside_R292_open_cell"] is True
    )
    full_segment_named_support = all((
        root_zero_derived,
        orientation_hard_checked,
        endpoint_side_matches_face,
        signature_has_only_active_reason,
        all_other_predicates_strict,
        exact_support_chain,
    ))
    need(
        full_segment_named_support
        and corridor_strictly_inside
        and direct_row["active_function_id"]
        == factor_descriptor(region)["active_function_id"]
        and direct_row["lower_p"] == str(Q(direct_row["lower_p"]))
        and direct_row["upper_p"] == str(Q(direct_row["upper_p"]))
        and Q(direct_row["lower_p"]) < Q(direct_row["upper_p"])
        and Q(oriented_p_face) in {
            Q(direct_row["lower_p"]), Q(direct_row["upper_p"]),
        },
        "FULL_SIGN_SIDE_UPSTREAM_DERIVATION:" + endpoint_side,
    )

    provenance = {
        "Round275_region_id": region_id,
        "Round275_region_row_sha256": region["row_sha256"],
        "R287_region_disposition_row_id":
            r287_region["Round287_region_disposition_row_id"],
        "R287_region_row_sha256": r287_region["row_sha256"],
        "R292_refinement_cell_row_id": cell_id,
        "R292_refinement_cell_row_sha256": cell["row_sha256"],
        "R292_connected_support_component_row_id": component_id,
        "R292_connected_support_component_row_sha256": component["row_sha256"],
        "connected_positive_open_support_member_count":
            component["member_refinement_cell_count"],
    }
    certificate_without_id = {
        "endpoint_occurrence_id": endpoint_occurrence_id,
        "endpoint_side": endpoint_side,
        "owner_face": owner_face,
        "approach": approach,
        "oriented_p_face": oriented_p_face,
        "graph_bracket_p": [direct_row["lower_p"], direct_row["upper_p"]],
        "proof_closed_core_base_z_s":
            direct_row["proof_closed_core_base_z_s"],
        "exact_common_R292_open_cell_t2_p_s":
            direct_row["exact_transformed_open_cell_t2_p_s"],
        "active_function_id": direct_row["active_function_id"],
        "active_reason": direct_row["active_reason"],
        "active_factor_side_sign": region["active_factor_side_sign"],
        "exact_F_p_face_sign": exact_face_sign,
        "uniform_strict_dF_dp_sign_on_whole_common_R292_cell":
            derivative_sign,
        "F_at_rho_equals_zero": root_zero_derived,
        "face_sign_derivative_orientation": face_sign_derivative_orientation,
        "face_sign_derivative_orientation_hard_checked":
            orientation_hard_checked,
        "exact_full_half_open_segment": exact_full_half_open_segment,
        "strict_monotonicity_retains_face_sign_on_entire_segment":
            root_zero_derived and orientation_hard_checked,
        "endpoint_R275_active_factor_side_sign_equals_face_sign":
            endpoint_side_matches_face,
        "whole_cell_dynamic_signature_exactly_one_unresolved_active_reason":
            signature_has_only_active_reason,
        "all_other_whole_cell_validity_predicates_uniformly_strict":
            all_other_predicates_strict,
        "R287_R292_single_connected_support_provenance": provenance,
        "full_segment_sign_slice_is_named_endpoint_support":
            full_segment_named_support,
        "local_corridor_role":
            "NONEMPTY_LOCAL_WITNESS_ONLY_NOT_FULL_SIDE_PROOF",
    }
    certificate = {
        "certificate_id": "round305b-full-sign-side-support:" + digest([
            "ROUND305B_FULL_SIGN_SIDE_TO_RHO_NAMED_SUPPORT_V1",
            certificate_without_id,
        ]),
        **certificate_without_id,
    }
    need(
        tuple(certificate)
        == tuple(WIRE_SPEC["definitions"][
            "full_sign_side_to_rho_support_certificate"
        ]["keys_exact"]),
        "FULL_SIGN_SIDE_CERTIFICATE_SCHEMA_KEYS",
    )
    return certificate, corridor_box


def build_full_zero_credit_candidate(
    residual: list[dict[str, Any]], endpoints: set[str],
) -> dict[str, Any]:
    wire_files = admit_normative_wire_files()
    direct = direct_scope_to_r292_p_brackets(residual, endpoints)
    direct_rows = direct["records"]
    bindings: list[dict[str, Any]] = direct["_bindings"]
    r287_regions: dict[str, dict[str, Any]] = direct["_r287_regions"]
    anchors: dict[str, dict[str, Any]] = direct["_anchors"]
    regions: dict[str, dict[str, Any]] = direct["_regions"]
    r179 = direct["_r179"]
    flint = direct["_flint"]
    r294_rows = load_r294_occurrence_rows(anchors)
    r304_members = load_round304_endpoint_members(residual, endpoints)
    binding_by_pair = {
        tuple(item["pair"]): item for item in bindings
    }
    direct_by_pair = {
        tuple(row["canonical_occurrence_pair"]): row for row in direct_rows
    }
    need(
        set(binding_by_pair) == set(direct_by_pair)
        and len(binding_by_pair) == EXPECTED_WITNESSES,
        "FULL_CANDIDATE_DIRECT_BINDING_SCOPE",
    )

    theorem_sha256 = digest(TWO_SIDED_ATTACHMENT_THEOREM)
    lemma_sha256 = digest(RELATIVE_PHYSICAL_CLOSURE_LIMIT_LEMMA)
    witness_id_by_pair: dict[tuple[str, str], str] = {}
    patch_id_by_pair: dict[tuple[str, str], str] = {}
    owner_extension_id_by_pair: dict[tuple[str, str], str] = {}
    lemma_payload_by_pair: dict[tuple[str, str], dict[str, Any]] = {}
    lemma_id_by_pair: dict[tuple[str, str], str] = {}
    for pair, row in direct_by_pair.items():
        scope_hash = binding_by_pair[pair]["scope"]["row_sha256"]
        patch_payload = {
            "scope_row_sha256": scope_hash,
            "pair": list(pair),
            "active_function_id": row["active_function_id"],
            "fixed_physical_t_sign": row["physical_t_sign"],
            "proof_closed_core_base_z_s": row["proof_closed_core_base_z_s"],
            "p_bracket": [row["lower_p"], row["upper_p"]],
        }
        patch_id = "round305b-proof-core-patch:" + digest([
            "ROUND305B_DIRECT_PROOF_CORE_P_GRAPH_PATCH_V1", patch_payload,
        ])
        patch_id_by_pair[pair] = patch_id
        owner_extension_payload = {
            "scope_row_sha256": scope_hash,
            "pair": list(pair),
            "active_function_id": row["active_function_id"],
            "fixed_physical_t_sign": row["physical_t_sign"],
            "owner_contact_closure_base_z_s":
                row["owner_contact_closure_base_z_s"],
            "p_bracket": [row["lower_p"], row["upper_p"]],
            "formal_credit": 0,
        }
        owner_extension_id_by_pair[pair] = (
            "round305b-owner-extension-patch:" + digest([
                "ROUND305B_ZERO_CREDIT_FULL_CLOSURE_ROOT_EXTENSION_PATCH_V1",
                owner_extension_payload,
            ])
        )
        witness_id_by_pair[pair] = "round305b-physical-witness:" + digest([
            "ROUND305B_TWO_SIDED_P_ATTACHMENT_V1", patch_id, scope_hash,
        ])
        lemma_payload = {
            "theorem": "R305B_RELATIVE_PHYSICAL_P_TO_RHO_ATTACHMENT_V1",
            "proof_core_patch_id": patch_id,
            "owner_extension_patch_id": owner_extension_id_by_pair[pair],
            "coordinate_map": (
                "Phi=(q=(9/25)n,u=sqrt(1-p^2)n+p*(-ny,nx),s)"
            ),
            "relative_chart": row["adjacent_chart"],
            "fixed_t_sign": row["physical_t_sign"],
            "support_open_base_z_s": row["support_open_base_z_s"],
            "proof_closed_core_base_z_s": row["proof_closed_core_base_z_s"],
            "owner_contact_closure_base_z_s":
                row["owner_contact_closure_base_z_s"],
            "quantified_attachment_base": "PROOF_CLOSED_CORE_ONLY",
            "owner_extension_is_zero_credit_sidecar_only": True,
            "graph_bracket_p": [row["lower_p"], row["upper_p"]],
            "strict_p_derivative":
                row["target_factor_derivative_signs_t_p_s"][1],
            "path_formula": (
                "p_eps=(1-eps)*p_graph(z,s)+eps*p_face, 0<eps<=1"
            ),
            "limit_formula": (
                "lim_{eps->0+} Phi(z,p_eps,s)=Phi(z,p_graph(z,s),s)"
            ),
            "corridor_box_is_not_Gamma_intersection": True,
        }
        lemma_payload_by_pair[pair] = lemma_payload
        lemma_id_by_pair[pair] = "round305b-relative-p-limit:" + digest(
            lemma_payload
        )

    contact_rows, owner_rows, owner_audit = build_contact_and_owner_rows(
        direct_rows, witness_id_by_pair, owner_extension_id_by_pair,
        regions, r179, flint,
    )
    contacts_by_witness: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in contact_rows:
        for witness_id in row["associated_physical_witness_row_ids"]:
            contacts_by_witness[witness_id].append(row)
    owners_by_witness: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in owner_rows:
        for witness_id in row["associated_physical_witness_row_ids"]:
            owners_by_witness[witness_id].append(row)

    anchor_rows: list[dict[str, Any]] = []
    anchor_rows_by_witness: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for pair in sorted(binding_by_pair):
        item = binding_by_pair[pair]
        direct_row = direct_by_pair[pair]
        witness_id = witness_id_by_pair[pair]
        for side, occurrence, region_id in (
            ("LEFT", item["left_endpoint"], item["left_region_id"]),
            ("RIGHT", item["right_endpoint"], item["right_region_id"]),
        ):
            anchor = anchors[occurrence]
            cell = anchor["cell"]
            component = anchor["component"]
            r287_region = r287_regions[region_id]
            region = regions[region_id]
            r294 = r294_rows[occurrence]
            member = r304_members[occurrence]
            full_sign_side_certificate, corridor_box = (
                build_full_sign_side_to_rho_support_certificate(
                    endpoint_side=side,
                    endpoint_occurrence_id=occurrence,
                    region_id=region_id,
                    region=region,
                    r287_region=r287_region,
                    cell=cell,
                    component=component,
                    direct_row=direct_row,
                )
            )
            closure_side = {
                "approach": full_sign_side_certificate["approach"],
                "active_factor_sign": full_sign_side_certificate[
                    "active_factor_side_sign"
                ],
                "strict_p_derivative_sign":
                    full_sign_side_certificate[
                        "uniform_strict_dF_dp_sign_on_whole_common_R292_cell"
                    ],
                "limit": "p -> rho(z,s)",
                "topology": "relative topology of physical section X",
                "quantified_base": "PROOF_CLOSED_CORE_ONLY",
                "support_open_base_z_s": direct_row["support_open_base_z_s"],
                "proof_closed_core_base_z_s":
                    direct_row["proof_closed_core_base_z_s"],
                "strict_sign_corridor_box_t2_p_s": corridor_box,
                "corridor_strictly_inside_R292_open_cell":
                    direct_row["corridors_strictly_inside_R292_open_cell"],
                "local_corridor_nonempty_witness_only":
                    full_sign_side_certificate["local_corridor_role"]
                    == "NONEMPTY_LOCAL_WITNESS_ONLY_NOT_FULL_SIDE_PROOF",
                "full_sign_side_to_rho_support_certificate":
                    full_sign_side_certificate,
                "exact_full_sign_side_contained_in_R292_support_derived":
                    full_sign_side_certificate[
                        "full_segment_sign_slice_is_named_endpoint_support"
                    ],
            }
            need(
                tuple(closure_side)
                == tuple(WIRE_SPEC["definitions"]["closure_limit_side"][
                    "keys_exact"
                ]),
                "ANCHOR_CLOSURE_LIMIT_SIDE_SCHEMA_KEYS",
            )
            anchor_payload_without_id = {
                "schema": SCHEMA + ".anchor-row.v1",
                "physical_witness_row_id": witness_id,
                "side": side,
                "endpoint_occurrence_id": occurrence,
                "Round275_region_id": region_id,
                "Round275_region_row_sha256": region["row_sha256"],
                "R287_region_disposition_row_id":
                    r287_region["Round287_region_disposition_row_id"],
                "R287_region_row_sha256": r287_region["row_sha256"],
                "R292_refinement_cell_row_id": cell[
                    "Round292_R287_existing_overlap_refinement_cell_id"
                ],
                "R292_refinement_cell_row_sha256": cell["row_sha256"],
                "R292_connected_support_component_row_id": component[
                    "Round292_refined_new_support_component_id"
                ],
                "R292_connected_support_component_row_sha256":
                    component["row_sha256"],
                "R292_occurrence_content_preimage_sha256":
                    anchor["occurrence_content_preimage_sha256"],
                "R294_occurrence_registry_row_id":
                    r294["Round294_occurrence_registry_row_id"],
                "R294_occurrence_registry_row_sha256": r294["row_sha256"],
                "R294_official_key_id": None,
                "R294_official_key_ordinal": None,
                "R294_official_key_binding_status":
                    r294["official_key_binding_status"],
                "Round304_member_row_id":
                    member["Round304_fresh_member_component_row_id"],
                "Round304_member_row_sha256": member["row_sha256"],
                "official_key_id": member["official_key_id"],
                "connected_positive_open_support_nonempty": True,
                "connected_positive_open_support_member_count": 1,
                "relative_physical_closure_limit_side": closure_side,
                "formal_anchor_binding_credit": 1,
                "formal_occurrence_identity_collapse_credit": 0,
                "formal_official_key_merge_credit": 0,
            }
            anchor_id = "round305b-anchor:" + digest([
                "ROUND305B_R292_SINGLE_CELL_FULL_SIGN_SIDE_ANCHOR_V2",
                witness_id, side, occurrence, cell["row_sha256"],
                r294["row_sha256"], member["row_sha256"],
                lemma_id_by_pair[pair],
                full_sign_side_certificate["certificate_id"],
            ])
            payload = {
                "Round305B_anchor_row_id": anchor_id,
                **anchor_payload_without_id,
            }
            need(tuple(payload) + ("row_sha256",) == ANCHOR_KEYS,
                 "ANCHOR_SCHEMA_KEYS")
            closed = close_row(payload, "Round305B_anchor_row_id")
            anchor_rows.append(closed)
            anchor_rows_by_witness[witness_id].append(closed)
    anchor_rows.sort(key=lambda row: row["Round305B_anchor_row_id"])
    need(
        len(anchor_rows) == EXPECTED_ANCHORS
        and len({row["endpoint_occurrence_id"] for row in anchor_rows})
        == EXPECTED_ANCHORS
        and len({
            row["relative_physical_closure_limit_side"]
            ["full_sign_side_to_rho_support_certificate"]["certificate_id"]
            for row in anchor_rows
        }) == EXPECTED_ANCHORS
        and all(len(rows) == 2 for rows in anchor_rows_by_witness.values()),
        "FULL_ANCHOR_CENSUS",
    )

    physical_rows: list[dict[str, Any]] = []
    physical_by_id: dict[str, dict[str, Any]] = {}
    for pair in sorted(binding_by_pair):
        item = binding_by_pair[pair]
        direct_row = direct_by_pair[pair]
        scope = item["scope"]
        witness_id = witness_id_by_pair[pair]
        patch_id = patch_id_by_pair[pair]
        two_anchors = sorted(
            anchor_rows_by_witness[witness_id], key=lambda row: row["side"]
        )
        need([row["side"] for row in two_anchors] == ["LEFT", "RIGHT"],
             "PHYSICAL_TWO_ORDERED_ANCHORS")
        contacts = sorted(
            contacts_by_witness[witness_id],
            key=lambda row: row["Round305B_closure_contact_row_id"],
        )
        owner_loci = sorted(
            owners_by_witness[witness_id],
            key=lambda row: row["Round305B_owner_locus_row_id"],
        )
        left_anchor = next(row for row in two_anchors if row["side"] == "LEFT")
        right_anchor = next(row for row in two_anchors if row["side"] == "RIGHT")
        official_pair = sorted((
            left_anchor["official_key_id"], right_anchor["official_key_id"],
        ))
        need(official_pair[0] != official_pair[1],
             "PHYSICAL_CROSS_OFFICIAL_KEY")
        support_base = tuple(map(Q, direct_row["support_open_base_z_s"]))
        core_base = tuple(map(Q, direct_row["proof_closed_core_base_z_s"]))
        closure_base = tuple(map(
            Q, direct_row["owner_contact_closure_base_z_s"],
        ))
        core_area = (
            (core_base[1] - core_base[0])
            * (core_base[3] - core_base[2])
        )
        need(
            core_area > 0
            and support_base == closure_base
            and support_base[0] < core_base[0] < core_base[1] < support_base[1]
            and support_base[2] < core_base[2] < core_base[3] < support_base[3],
            "PHYSICAL_STRICT_POSITIVE_CORE_INSIDE_OPEN_SUPPORT",
        )
        exact_domain = {
            "coordinate_system": "(z=t^2,p,s)",
            "support_open_base_z_s": direct_row["support_open_base_z_s"],
            "proof_closed_core_base_B_z_s":
                direct_row["proof_closed_core_base_z_s"],
            "owner_contact_closure_base_z_s":
                direct_row["owner_contact_closure_base_z_s"],
            "proof_core_inset_rule": direct_row["proof_core_inset_rule"],
            "proof_core_strictly_inside_R292_open_base": True,
            "owner_contact_closure_is_zero_credit_full_closure_extension": True,
            "p_interval": [direct_row["lower_p"], direct_row["upper_p"]],
            "proof_core_base_area": qstr(core_area),
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
        exact_gamma = {
            "definition": (
                "Gamma_core={Phi(z,rho(z,s),s):(z,s) in B_core}; "
                "F(z,rho(z,s),s)=0"
            ),
            "quantified_base": "PROOF_CLOSED_CORE_ONLY",
            "proof_closed_core_base_z_s":
                direct_row["proof_closed_core_base_z_s"],
            "F_identity": direct_row["active_function_identity_payload"],
            "rho_exists_uniquely_on_every_base_fibre": True,
            "rho_continuous": True,
            "rho_range_strictly_inside_p_bracket": True,
            "Gamma_core_nonempty": True,
            "Gamma_core_connected": True,
            "Gamma_core_included_in_valid_physical_wall_event_lower_stratum": True,
            "corridor_boxes_disjoint_from_Gamma_core": True,
            "owner_extension_not_part_of_Gamma_core": True,
            "relative_limit_lemma_instance": lemma_payload_by_pair[pair],
        }
        G0 = {
            "satisfied": True,
            "Round305A": [
                scope["Round305A_scope_reprojection_row_id"], scope["row_sha256"],
            ],
            "Round300A": [
                item["canonical"]["Round300A_canonical_occurrence_pair_row_id"],
                item["canonical"]["row_sha256"],
            ],
            "Round287_pair": [
                item["source_Round287_pair_row_id"],
                item["source"]["source_Round287_pair_row_sha256"],
            ],
            "Round275_regions": [
                [item["left_region_id"], regions[item["left_region_id"]]["row_sha256"]],
                [item["right_region_id"], regions[item["right_region_id"]]["row_sha256"]],
            ],
            "anchor_row_ids": [row["Round305B_anchor_row_id"] for row in two_anchors],
            "anchor_row_sha256s": [row["row_sha256"] for row in two_anchors],
            "all_source_and_derived_rows_content_closed": True,
        }
        G1 = {
            "satisfied": True,
            "exact_domain": exact_domain,
            "attachment_quantifier": "FOR_ALL_B_IN_PROOF_CLOSED_CORE_ONLY",
            "proof_core_strictly_inside_both_R292_open_supports": True,
            "selected_root_discriminant_strict_positive": True,
            "selected_near_root_strict_future_and_less_than_three": True,
            "all_competitor_order_outgoing_chart_and_other_dynamic_predicates_strict":
                direct_row["all_other_dynamic_signature_predicates_strict"],
            "only_nonstrict_whole_cell_predicate":
                direct_row["only_unresolved_dynamic_predicate"],
            "both_R292_supports_connected_positive_open_single_cell": True,
        }
        G2 = {
            "satisfied": True,
            "active_reason": direct_row["active_reason"],
            "predicate_details": direct_row[
                "whole_cell_wall_event_product_replay"
            ]["predicate_details"],
            "explicit_wall_value": 0,
            "zero_wall_hard_checked_not_silently_dropped": True,
            "source_wall_factor_strict_sign":
                direct_row["discarded_source_factor_strict_sign"],
            "source_wall_factor_uniformly_nonzero_on_proof_core": True,
            "target_wall_factor_F_identity":
                direct_row["active_function_identity_payload"],
            "wall_event_product_zero_iff_target_F_zero": True,
            "uniform_strict_dF_dp_sign":
                direct_row["target_factor_derivative_signs_t_p_s"][1],
            "proof_core_target_factor_face_replays": direct_row["face_replays"],
            "proof_core_wall_event_product_face_replays":
                direct_row["core_face_wall_event_product_replays"],
            "uniform_opposite_p_face_signs": True,
            "proof_closed_core_base_z_s":
                direct_row["proof_closed_core_base_z_s"],
            "IVT_unique_continuous_rho": True,
            "Gamma_core_valid_physical_inclusion_replayed": True,
        }
        G3 = {
            "satisfied": True,
            "endpoint": left_anchor["endpoint_occurrence_id"],
            "sign_side": left_anchor["relative_physical_closure_limit_side"],
            "quantified_base": "FOR_ALL_B_IN_PROOF_CLOSED_CORE_ONLY",
            "proof_closed_core_base_z_s":
                direct_row["proof_closed_core_base_z_s"],
            "sequence": (
                "Phi(b,p_k), p_k->rho(b), b in B_core, from the LEFT "
                "endpoint sign side"
            ),
            "strict_sign_corridor_box_t2_p_s": left_anchor[
                "relative_physical_closure_limit_side"
            ]["strict_sign_corridor_box_t2_p_s"],
            "full_sign_side_to_rho_support_certificate": left_anchor[
                "relative_physical_closure_limit_side"
            ]["full_sign_side_to_rho_support_certificate"],
            "full_sign_side_sequence_remains_in_exact_R292_open_support_by_certificate":
                left_anchor["relative_physical_closure_limit_side"]
                ["exact_full_sign_side_contained_in_R292_support_derived"],
            "corridor_used_only_as_local_nonempty_witness": left_anchor[
                "relative_physical_closure_limit_side"
            ]["local_corridor_nonempty_witness_only"],
            "limit_in_relative_physical_space_X": True,
            "conclusion": "Gamma_core subset cl_X(A_left)",
        }
        G4 = {
            "satisfied": True,
            "endpoint": right_anchor["endpoint_occurrence_id"],
            "sign_side": right_anchor["relative_physical_closure_limit_side"],
            "quantified_base": "FOR_ALL_B_IN_PROOF_CLOSED_CORE_ONLY",
            "proof_closed_core_base_z_s":
                direct_row["proof_closed_core_base_z_s"],
            "sequence": (
                "Phi(b,p_k), p_k->rho(b), b in B_core, from the RIGHT "
                "endpoint sign side"
            ),
            "strict_sign_corridor_box_t2_p_s": right_anchor[
                "relative_physical_closure_limit_side"
            ]["strict_sign_corridor_box_t2_p_s"],
            "full_sign_side_to_rho_support_certificate": right_anchor[
                "relative_physical_closure_limit_side"
            ]["full_sign_side_to_rho_support_certificate"],
            "full_sign_side_sequence_remains_in_exact_R292_open_support_by_certificate":
                right_anchor["relative_physical_closure_limit_side"]
                ["exact_full_sign_side_contained_in_R292_support_derived"],
            "corridor_used_only_as_local_nonempty_witness": right_anchor[
                "relative_physical_closure_limit_side"
            ]["local_corridor_nonempty_witness_only"],
            "limit_in_relative_physical_space_X": True,
            "conclusion": "Gamma_core subset cl_X(A_right)",
        }
        need(
            tuple(G3) == tuple(WIRE_SPEC["definitions"]["G3_or_G4"][
                "keys_exact"
            ])
            and tuple(G4) == tuple(WIRE_SPEC["definitions"]["G3_or_G4"][
                "keys_exact"
            ]),
            "PHYSICAL_G3_G4_SCHEMA_KEYS",
        )
        G5 = {
            "satisfied": True,
            "active_reason": direct_row["active_reason"],
            "predicate_details": direct_row[
                "whole_cell_wall_event_product_replay"
            ]["predicate_details"],
            "explicit_wall_value": 0,
            "zero_wall_hard_checked_not_silently_dropped": True,
            "whole_open_support_wall_event_product_replay":
                direct_row["whole_cell_wall_event_product_replay"],
            "proof_core_p_face_wall_event_product_replays":
                direct_row["core_face_wall_event_product_replays"],
            "source_wall_factor_uniformly_strict_nonzero": True,
            "wall_event_product_zero_iff_target_F_zero": True,
            "Gamma_core_is_included_wall_event_not_coordinate_zero_shortcut":
                True,
            "R294_occurrence_identity_stage": {
                "official_key_id_is_null": True,
                "official_key_ordinal_is_null": True,
                "binding_status": left_anchor["R294_official_key_binding_status"],
                "both_source_rows_equal_exact_R292_component_rows": True,
            },
            "R304_separate_official_key_materialization_stage": {
                "official_key_pair": official_pair,
                "member_row_ids": [
                    left_anchor["Round304_member_row_id"],
                    right_anchor["Round304_member_row_id"],
                ],
                "stages_not_conflated": True,
            },
            "occurrence_identity_collapsed": False,
            "official_key_identity_merged": False,
            "owner_extension_full_closure_sidecar_only": True,
            "owner_extension_not_Gamma_core_or_G3_G4_or_component_edge_basis":
                True,
            "closure_intersection_conclusion":
                "Gamma_core subset cl_X(A_left) intersect cl_X(A_right)",
        }
        payload = {
            "Round305B_physical_witness_row_id": witness_id,
            "schema": SCHEMA + ".physical-witness-row.v1",
            "source_Round305A_scope_reprojection_row_id":
                scope["Round305A_scope_reprojection_row_id"],
            "source_Round305A_scope_reprojection_row_sha256": scope["row_sha256"],
            "source_Round300A_row_id":
                item["canonical"]["Round300A_canonical_occurrence_pair_row_id"],
            "source_Round300A_row_sha256": item["canonical"]["row_sha256"],
            "canonical_registry_occurrence_pair": list(pair),
            "Round304_final_component_pair": scope["final_component_pair"],
            "official_key_pair": official_pair,
            "cross_official_key_physical_edge_permitted": True,
            "occurrence_identity_collapsed": False,
            "official_key_identity_merged": False,
            "proof_core_patch_id": patch_id,
            "owner_extension_patch_id": owner_extension_id_by_pair[pair],
            "active_function_id": direct_row["active_function_id"],
            "guard_id": direct_row["source_guard_row_id"],
            "branch_id": "round305b-target-zero-branch:" + digest([
                item["source_Round287_pair_row_id"],
                direct_row["active_reason"], direct_row["active_function_id"],
            ]),
            "exact_relative_physical_domain": exact_domain,
            "exact_graph_Gamma": exact_gamma,
            "anchor_row_ids": [row["Round305B_anchor_row_id"] for row in two_anchors],
            "anchor_row_sha256s": [row["row_sha256"] for row in two_anchors],
            "closure_contact_row_ids": [
                row["Round305B_closure_contact_row_id"] for row in contacts
            ],
            "closure_contact_row_sha256s": [row["row_sha256"] for row in contacts],
            "owner_locus_row_ids": [
                row["Round305B_owner_locus_row_id"] for row in owner_loci
            ],
            "owner_locus_row_sha256s": [row["row_sha256"] for row in owner_loci],
            "owner_extension_sidecar_not_Gamma_core_or_attachment_or_edge_basis":
                True,
            "G0_exact_provenance_pins_and_row_closures": G0,
            "G1_endpoint_occurrence_connected_supports": G1,
            "G2_nonempty_connected_included_lower_stratum": G2,
            "G3_left_closure_attaches_to_included_patch": G3,
            "G4_right_closure_attaches_to_included_patch": G4,
            "G5_endpoint_patch_provenance_exactly_closed": G5,
            "relative_physical_closure_limit_lemma_id":
                lemma_id_by_pair[pair],
            "corridor_box_used_as_Gamma_intersection": False,
            "D4_transfer_used": False,
            "candidate_physical_connectivity_conclusion": True,
            "formal_physical_witness_credit": 1,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        }
        need(set(payload) | {"row_sha256"} == set(PHYSICAL_WITNESS_KEYS),
             "PHYSICAL_WITNESS_SCHEMA_KEYS")
        physical = close_row(payload, "Round305B_physical_witness_row_id")
        physical_rows.append(physical)
        physical_by_id[witness_id] = physical
    physical_rows.sort(key=lambda row: row["Round305B_physical_witness_row_id"])
    need(
        len(physical_rows) == EXPECTED_WITNESSES
        and all(
            all(row[field]["satisfied"] for field in (
                "G0_exact_provenance_pins_and_row_closures",
                "G1_endpoint_occurrence_connected_supports",
                "G2_nonempty_connected_included_lower_stratum",
                "G3_left_closure_attaches_to_included_patch",
                "G4_right_closure_attaches_to_included_patch",
                "G5_endpoint_patch_provenance_exactly_closed",
            ))
            for row in physical_rows
        ),
        "PHYSICAL_G0_G5_CENSUS",
    )

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    pair_by_witness_id = {
        witness_id_by_pair[pair]: pair for pair in witness_id_by_pair
    }
    for row in physical_rows:
        grouped[tuple(row["Round304_final_component_pair"])].append(row)
    component_degrees = Counter(
        component for pair in grouped for component in pair
    )
    need(
        len(grouped) == EXPECTED_CANONICAL_COMPONENT_EDGES
        and len(component_degrees) == 16
        and set(component_degrees.values()) == {1},
        "EIGHT_COMPONENT_EDGES_FORM_16_VERTEX_MATCHING",
    )
    edge_rows: list[dict[str, Any]] = []
    for component_pair, witnesses in sorted(grouped.items()):
        witnesses.sort(key=lambda row: row["Round305B_physical_witness_row_id"])
        occurrence_pairs = sorted(
            row["canonical_registry_occurrence_pair"] for row in witnesses
        )
        official_pairs = {tuple(row["official_key_pair"]) for row in witnesses}
        need(
            len(witnesses) == EXPECTED_WITNESSES_PER_COMPONENT_EDGE
            and len(official_pairs) == 1,
            "EDGE_128_WITNESS_ONE_KEY_PROFILE",
        )
        official_pair = list(next(iter(official_pairs)))
        witness_ids = [row["Round305B_physical_witness_row_id"] for row in witnesses]
        witness_hashes = [row["row_sha256"] for row in witnesses]
        edge_id = "round305b-canonical-component-edge:" + digest([
            "ROUND305B_G0_G5_DEDUP_COMPONENT_EDGE_V1",
            list(component_pair), digest(witness_ids), digest(witness_hashes),
        ])
        payload = {
            "Round305B_canonical_component_edge_row_id": edge_id,
            "schema": SCHEMA + ".canonical-component-edge-row.v1",
            "canonical_Round304_final_component_pair": list(component_pair),
            "physical_witness_row_count": len(witnesses),
            "physical_witness_row_ids_sha256": digest(witness_ids),
            "physical_witness_row_sha256s_sha256": digest(witness_hashes),
            "canonical_occurrence_pairs_sha256": digest(occurrence_pairs),
            "canonical_official_key_pair": official_pair,
            "cross_official_key_physical_edge_permitted": True,
            "occurrence_identity_collapsed": False,
            "official_key_identity_merged": False,
            "all_128_witnesses_satisfy_G0_G5": True,
            "deduplicated_from_witness_rows_not_union_rows": True,
            "formal_component_edge_credit": 1,
            "eligible_for_later_fresh_DSU_application": True,
            "formal_DSU_rank_reduction_credit": 0,
        }
        need(set(payload) | {"row_sha256"} == set(COMPONENT_EDGE_KEYS),
             "COMPONENT_EDGE_SCHEMA_KEYS")
        edge_rows.append(close_row(
            payload, "Round305B_canonical_component_edge_row_id"
        ))
    edge_rows.sort(key=lambda row: row["Round305B_canonical_component_edge_row_id"])
    need(
        len(edge_rows) == EXPECTED_CANONICAL_COMPONENT_EDGES
        and {row["physical_witness_row_count"] for row in edge_rows} == {128}
        and len({tuple(row["canonical_Round304_final_component_pair"])
                 for row in edge_rows}) == 8,
        "EIGHT_CANONICAL_COMPONENT_EDGES",
    )

    ledgers = {
        "physical": closed_ledger(
            SCHEMA + ".physical-witness-ledger.v1", physical_rows,
            "Round305B_physical_witness_row_id",
        ),
        "anchor": closed_ledger(
            SCHEMA + ".anchor-ledger.v1", anchor_rows,
            "Round305B_anchor_row_id",
        ),
        "contact": closed_ledger(
            SCHEMA + ".closure-contact-ledger.v1", contact_rows,
            "Round305B_closure_contact_row_id",
        ),
        "owner": closed_ledger(
            SCHEMA + ".owner-locus-ledger.v1", owner_rows,
            "Round305B_owner_locus_row_id",
        ),
        "edge": closed_ledger(
            SCHEMA + ".canonical-component-edge-ledger.v1", edge_rows,
            "Round305B_canonical_component_edge_row_id",
        ),
    }
    result_payload = {
        "schema": SCHEMA + ".zero-credit-candidate-result.v1",
        "status": (
            "PASS_ROUND305B_DIRECT_G0_G5_ZERO_CREDIT_CANDIDATE__"
            "PENDING_INDEPENDENT_VERIFICATION__"
            "ZERO_OFFICIALLY_ADMITTED_CREDIT"
        ),
        "producer_source_filename": PRODUCER_FILENAME,
        "producer_source_sha256": file_sha256(Path(__file__)),
        "schema_snapshot": SCHEMA_SNAPSHOT,
        "schema_snapshot_sha256": digest(SCHEMA_SNAPSHOT),
        "two_sided_attachment_theorem": TWO_SIDED_ATTACHMENT_THEOREM,
        "two_sided_attachment_theorem_sha256": theorem_sha256,
        "relative_physical_closure_limit_lemma":
            RELATIVE_PHYSICAL_CLOSURE_LIMIT_LEMMA,
        "relative_physical_closure_limit_lemma_sha256": lemma_sha256,
        "normative_wire_file_commitments": wire_files["file_commitments"],
        "direct_geometry_reconstruction": {
            key: value for key, value in direct.items()
            if key != "records"
            and not key.startswith("_")
            and key not in {
                "direct_rows_sha256", "direct_row_ids_sha256",
                "direct_row_hashes_sha256",
            }
        },
        "formal_G0_G5_witness_candidate_count": len(physical_rows),
        "exact_anchor_candidate_count": len(anchor_rows),
        "closure_contact_sidecar_count": len(contact_rows),
        "global_owner_locus_sidecar_count": len(owner_rows),
        "canonical_component_edge_candidate_count": len(edge_rows),
        "witnesses_per_component_edge": 128,
        "owner_audit": owner_audit,
        "ledger_object_commitments": {
            key: {
                "filename": OUTPUT_NAMES[key],
                "ledger_sha256": value["ledger_sha256"],
                "rows_sha256": value["rows_sha256"],
                "row_ids_sha256": value["row_ids_sha256"],
                "row_hashes_sha256": value["row_hashes_sha256"],
            }
            for key, value in ledgers.items()
        },
        "strict_credit_boundary": {
            "zero_credit_candidate_publication_only": True,
            "independent_verifier_admitted": False,
            "candidate_ledger_formal_anchor_binding_credit": 2_048,
            "candidate_ledger_formal_physical_witness_credit": 1_024,
            "candidate_ledger_formal_component_edge_credit": 8,
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
        },
        "conditional_later_fresh_DSU_effect": {
            "canonical_edges_eligible_after_independent_promotion": 8,
            "maximum_later_rank_reductions": 8,
            "Round304_component_count": 92_696,
            "conditional_post_edge_component_count": 92_688,
            "applied_in_Round305B": False,
        },
        "zero_credit_candidate_publication_permitted": True,
        "manifest_emitted": False,
    }
    result = dict(result_payload)
    result["result_sha256"] = digest(result)
    return {"result": result, **ledgers}


def deterministic_gzip_bytes(value: Any) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=output, compresslevel=9, mtime=0,
    ) as stream:
        stream.write(canonical(value))
    payload = bytearray(output.getvalue())
    need(
        len(payload) >= 18
        and payload[:3] == b"\x1f\x8b\x08"
        and payload[3] == 0
        and payload[4:8] == b"\x00\x00\x00\x00"
        and payload[8] == 2,
        "DETERMINISTIC_GZIP_HEADER",
    )
    # RFC1952 OS=255 is explicitly normalized so the wire does not inherit a
    # host-platform byte from the compression runtime.
    payload[9] = 255
    return bytes(payload)


def contains_absolute_path(value: Any) -> bool:
    if type(value) is str:
        return value.startswith("/") or re.match(r"^[A-Za-z]:[\\/]", value) is not None
    if type(value) is list:
        return any(contains_absolute_path(item) for item in value)
    if type(value) is dict:
        return any(
            contains_absolute_path(key) or contains_absolute_path(item)
            for key, item in value.items()
        )
    return False


def wire_contract_fixture() -> dict[str, Any]:
    """Small source-data-free contract vector for producer/verifier diffing."""

    fixture_payload = {
        "fixture_row_id": "round305b-wire-fixture:synthetic-row-0001",
        "schema": SCHEMA + ".wire-fixture-row.v1",
        "rational_probe": "-7/11",
        "unicode_probe": "Gamma_core=Γ_core",
        "json_scalars_probe": [True, False, None, 0, 1],
    }
    fixture_row = close_row(fixture_payload, "fixture_row_id")
    empty_ledger = closed_ledger(
        SCHEMA + ".wire-fixture-ledger.v1", [], "fixture_row_id",
    )
    one_row_ledger = closed_ledger(
        SCHEMA + ".wire-fixture-ledger.v1", [fixture_row], "fixture_row_id",
    )
    empty_gzip = deterministic_gzip_bytes(empty_ledger)
    one_gzip = deterministic_gzip_bytes(one_row_ledger)
    result_payload = {
        "schema": SCHEMA + ".wire-fixture-result.v1",
        "status": "SYNTHETIC_WIRE_CONTRACT_ONLY__NO_FORMAL_CREDIT",
        "wire_spec_id": WIRE_SPEC["wire_spec_id"],
        "wire_spec_sha256": digest(WIRE_SPEC),
        "one_row_ledger_sha256": one_row_ledger["ledger_sha256"],
        "one_row_file_sha256": hashlib.sha256(one_gzip).hexdigest(),
        "formal_credit": 0,
    }
    fixture_result = dict(result_payload)
    fixture_result["result_sha256"] = digest(fixture_result)
    need(
        gzip.decompress(empty_gzip) == canonical(empty_ledger)
        and gzip.decompress(one_gzip) == canonical(one_row_ledger)
        and empty_gzip[:10] == b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff"
        and one_gzip[:10] == b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff",
        "WIRE_FIXTURE_GZIP_REPLAY",
    )
    return {
        "schema": SCHEMA + ".wire-contract-fixture.v1",
        "status": "PASS_SYNTHETIC_ONE_ROW_EMPTY_LEDGER_WIRE_CONTRACT",
        "wire_spec_id": WIRE_SPEC["wire_spec_id"],
        "wire_spec_sha256": digest(WIRE_SPEC),
        "canonical_json_probe": {
            "value": fixture_payload,
            "utf8_hex": canonical(fixture_payload).hex(),
            "sha256": digest(fixture_payload),
        },
        "closed_row_probe": fixture_row,
        "empty_ledger_probe": empty_ledger,
        "one_row_ledger_probe": one_row_ledger,
        "deterministic_gzip_probe": {
            "empty_ledger_header_hex": empty_gzip[:10].hex(),
            "empty_ledger_file_sha256": hashlib.sha256(empty_gzip).hexdigest(),
            "empty_ledger_size_bytes": len(empty_gzip),
            "one_row_ledger_header_hex": one_gzip[:10].hex(),
            "one_row_ledger_file_sha256": hashlib.sha256(one_gzip).hexdigest(),
            "one_row_ledger_size_bytes": len(one_gzip),
            "roundtrip_exact": True,
        },
        "result_self_hash_probe": fixture_result,
        "contract_assertions": {
            "row_self_hash_excludes_only_row_sha256": True,
            "ledger_self_hash_excludes_only_ledger_sha256": True,
            "result_self_hash_excludes_only_result_sha256": True,
            "result_file_not_recursively_self_committed": True,
            "canonical_json_has_no_trailing_newline": True,
            "gzip_mtime_zero_empty_name_os_255": True,
            "formal_credit": 0,
        },
    }


def admit_normative_wire_files() -> dict[str, Any]:
    expected = {
        WIRE_SPEC_FILENAME: WIRE_SPEC,
        WIRE_CONTRACT_FIXTURE_FILENAME: wire_contract_fixture(),
    }
    commitments: dict[str, dict[str, Any]] = {}
    keys = {
        WIRE_SPEC_FILENAME: "wire_spec",
        WIRE_CONTRACT_FIXTURE_FILENAME: "wire_contract_fixture",
    }
    for filename, value in expected.items():
        path = D / filename
        require_regular(path, filename)
        raw = path.read_bytes()
        need(
            raw == canonical(value)
            and strict_json_bytes(raw, filename) == value,
            "NORMATIVE_WIRE_FILE_EXACT_BYTES:" + filename,
        )
        commitments[keys[filename]] = {
            "filename": filename,
            "file_sha256": hashlib.sha256(raw).hexdigest(),
            "file_size_bytes": len(raw),
        }
    return {
        "wire_spec_filename": WIRE_SPEC_FILENAME,
        "wire_contract_fixture_filename": WIRE_CONTRACT_FIXTURE_FILENAME,
        "canonical_bytes_exact": True,
        "contains_actual_candidate_commitments": False,
        "formal_credit": 0,
        "file_commitments": commitments,
    }


def build_full_candidate_bytes() -> tuple[dict[str, Any], dict[str, bytes], dict[str, Any]]:
    producer_path = Path(os.path.abspath(os.fspath(__file__)))
    producer_entry = os.lstat(producer_path)
    need(
        producer_path.parent == D.resolve()
        and stat.S_ISREG(producer_entry.st_mode)
        and not stat.S_ISLNK(producer_entry.st_mode)
        and producer_entry.st_uid == os.geteuid()
        and producer_entry.st_nlink == 1,
        "PRODUCER_SOURCE_SNAPSHOT_BOUNDARY",
    )
    producer_source_identity = publication_file_identity(producer_entry)
    producer_source_sha256 = file_sha256(producer_path)
    wire_files = admit_normative_wire_files()
    manifests = admit_sealed_inputs()
    residual, endpoints = read_r305a_scope()
    official = project_official_keys(residual, endpoints)
    bundle = build_full_zero_credit_candidate(residual, endpoints)
    need(
        bundle["result"]["producer_source_sha256"]
        == producer_source_sha256,
        "PRODUCER_SOURCE_CHANGED_DURING_CANDIDATE_CONSTRUCTION",
    )
    raw: dict[str, bytes] = {
        key: deterministic_gzip_bytes(bundle[key])
        for key in ("physical", "anchor", "contact", "owner", "edge")
    }
    result = dict(bundle["result"])
    del result["result_sha256"]
    result["candidate_file_commitments"] = {
        key: {
            "filename": OUTPUT_NAMES[key],
            "file_sha256": hashlib.sha256(raw[key]).hexdigest(),
            "file_size_bytes": len(raw[key]),
            "compression": (
                "deterministic-gzip-level-9-mtime-0-empty-name-os-255"
            ),
        }
        for key in ("physical", "anchor", "contact", "owner", "edge")
    }
    need(not contains_absolute_path(result), "RESULT_WIRE_ABSOLUTE_PATH_FORBIDDEN")
    result["result_sha256"] = digest(result)
    bundle["result"] = result
    raw["result"] = canonical(result)
    audit = {
        "status": (
            "PASS_FULL_ROUND305B_ZERO_CREDIT_CANDIDATE_NO_WRITE_REBUILD__"
            "INDEPENDENT_VERIFIER_REQUIRED__ZERO_OFFICIALLY_ADMITTED_CREDIT"
        ),
        "producer_source_sha256": producer_source_sha256,
        "normative_wire_files": wire_files,
        "manifest_member_counts": {
            key: len(value) for key, value in manifests.items()
        },
        "official_key_audit": official,
        "row_counts": {
            key: bundle[key]["row_count"]
            for key in ("physical", "anchor", "contact", "owner", "edge")
        },
        "object_commitments": {
            key: {
                "ledger_sha256": bundle[key]["ledger_sha256"],
                "rows_sha256": bundle[key]["rows_sha256"],
                "row_ids_sha256": bundle[key]["row_ids_sha256"],
                "row_hashes_sha256": bundle[key]["row_hashes_sha256"],
            }
            for key in ("physical", "anchor", "contact", "owner", "edge")
        },
        "first_row_diagnostics": {
            key: {
                "row_id": bundle[key]["rows"][0][{
                    "physical": "Round305B_physical_witness_row_id",
                    "anchor": "Round305B_anchor_row_id",
                    "contact": "Round305B_closure_contact_row_id",
                    "owner": "Round305B_owner_locus_row_id",
                    "edge": "Round305B_canonical_component_edge_row_id",
                }[key]],
                "row_sha256": bundle[key]["rows"][0]["row_sha256"],
            }
            for key in ("physical", "anchor", "contact", "owner", "edge")
        },
        "file_commitments": {
            key: {
                "filename": OUTPUT_NAMES[key],
                "file_sha256": hashlib.sha256(raw[key]).hexdigest(),
                "file_size_bytes": len(raw[key]),
            }
            for key in ("physical", "anchor", "contact", "owner", "edge", "result")
        },
        "result_sha256": result["result_sha256"],
        "schema_snapshot_sha256": digest(SCHEMA_SNAPSHOT),
        "two_sided_attachment_theorem_sha256":
            digest(TWO_SIDED_ATTACHMENT_THEOREM),
        "relative_physical_closure_limit_lemma_sha256":
            digest(RELATIVE_PHYSICAL_CLOSURE_LIMIT_LEMMA),
        "all_1024_rows_satisfy_G0_G5": all(
            all(row[field]["satisfied"] for field in (
                "G0_exact_provenance_pins_and_row_closures",
                "G1_endpoint_occurrence_connected_supports",
                "G2_nonempty_connected_included_lower_stratum",
                "G3_left_closure_attaches_to_included_patch",
                "G4_right_closure_attaches_to_included_patch",
                "G5_endpoint_patch_provenance_exactly_closed",
            ))
            for row in bundle["physical"]["rows"]
        ),
        "all_R294_official_keys_null_before_R304_materialization": all(
            row["R294_official_key_id"] is None
            and row["R294_official_key_ordinal"] is None
            and type(row["official_key_id"]) is str
            for row in bundle["anchor"]["rows"]
        ),
        "owner_audit": result["owner_audit"],
        "zero_credit_candidate_publication_permitted": True,
        "manifest_emitted": False,
        "candidate_ledger_formal_anchor_binding_credit": 2_048,
        "candidate_ledger_formal_physical_witness_credit": 1_024,
        "candidate_ledger_formal_component_edge_credit": 8,
        "officially_admitted_formal_anchor_binding_credit": 0,
        "officially_admitted_formal_physical_witness_credit": 0,
        "officially_admitted_formal_component_edge_credit": 0,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
        "official_key_merge_credit": 0,
        "D4_transfer_credit": 0,
        "owner_sidecar_credit": 0,
    }
    final_producer_entry = os.lstat(producer_path)
    need(
        not stat.S_ISLNK(final_producer_entry.st_mode)
        and publication_file_identity(final_producer_entry)
        == producer_source_identity
        and file_sha256(producer_path) == producer_source_sha256,
        "PRODUCER_SOURCE_DRIFT_DURING_COMPLETE_CANDIDATE_BUILD",
    )
    return bundle, raw, audit


def record_fsync(
    descriptor: int, label: str, audit: Counter[str] | None,
) -> None:
    os.fsync(descriptor)
    if audit is not None:
        audit[label] += 1


def open_workspace_parent_fd(parent: Path) -> int:
    """Open an existing workspace parent without following any symlink."""

    root = Path(os.path.abspath(os.fspath(ROOT)))
    candidate = Path(os.path.abspath(os.fspath(parent)))
    try:
        relative = candidate.relative_to(root)
    except ValueError as error:
        raise PromotionBlocked("PRIVATE_STAGE_PARENT_OUTSIDE_WORKSPACE") from error
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    root_lstat = os.lstat(root)
    need(
        stat.S_ISDIR(root_lstat.st_mode)
        and not stat.S_ISLNK(root_lstat.st_mode),
        "PRIVATE_STAGE_WORKSPACE_ROOT_NOT_PLAIN_DIRECTORY",
    )
    descriptor = os.open(root, directory_flags)
    try:
        root_fstat = os.fstat(descriptor)
        need(
            (root_fstat.st_dev, root_fstat.st_ino)
            == (root_lstat.st_dev, root_lstat.st_ino)
            and root_fstat.st_uid == os.geteuid(),
            "PRIVATE_STAGE_WORKSPACE_ROOT_FD_BINDING",
        )
        for part in relative.parts:
            entry = os.stat(part, dir_fd=descriptor, follow_symlinks=False)
            need(
                stat.S_ISDIR(entry.st_mode) and not stat.S_ISLNK(entry.st_mode),
                "PRIVATE_STAGE_PARENT_CHAIN_SYMLINK_OR_NON_DIRECTORY:" + part,
            )
            child = os.open(part, directory_flags, dir_fd=descriptor)
            child_stat = os.fstat(child)
            need(
                (child_stat.st_dev, child_stat.st_ino)
                == (entry.st_dev, entry.st_ino)
                and child_stat.st_uid == os.geteuid(),
                "PRIVATE_STAGE_PARENT_CHAIN_FD_BINDING:" + part,
            )
            os.close(descriptor)
            descriptor = child
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def create_private_stage_directory(
    stage: Path, audit: Counter[str] | None = None,
) -> tuple[Path, int, int]:
    """Exclusively create and fd-bind one private 0700 stage directory."""

    resolved = Path(os.path.abspath(os.fspath(stage)))
    root = Path(os.path.abspath(os.fspath(ROOT)))
    deliverables = Path(os.path.abspath(os.fspath(D)))
    try:
        relative = resolved.relative_to(root)
    except ValueError as error:
        raise PromotionBlocked(
            "PRIVATE_STAGE_MUST_BE_A_WORKSPACE_SUBDIRECTORY"
        ) from error
    need(relative.parts, "PRIVATE_STAGE_REFUSES_WORKSPACE_ROOT")
    try:
        resolved.relative_to(deliverables)
    except ValueError:
        pass
    else:
        raise PromotionBlocked("PRIVATE_STAGE_REFUSES_DELIVERABLES_SUBTREE")
    need(resolved.name not in {"", ".", ".."}, "PRIVATE_STAGE_INVALID_NAME")

    parent_fd = open_workspace_parent_fd(resolved.parent)
    stage_fd: int | None = None
    try:
        try:
            os.mkdir(resolved.name, mode=0o700, dir_fd=parent_fd)
        except FileExistsError as error:
            raise PromotionBlocked("PRIVATE_STAGE_ALREADY_EXISTS") from error
        record_fsync(parent_fd, "parent_directory_after_mkdir", audit)
        stage_entry = os.stat(
            resolved.name, dir_fd=parent_fd, follow_symlinks=False,
        )
        need(
            stat.S_ISDIR(stage_entry.st_mode)
            and not stat.S_ISLNK(stage_entry.st_mode),
            "PRIVATE_STAGE_CREATED_ENTRY_NOT_DIRECTORY",
        )
        stage_fd = os.open(
            resolved.name,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=parent_fd,
        )
        os.fchmod(stage_fd, 0o700)
        stage_stat = os.fstat(stage_fd)
        need(
            (stage_stat.st_dev, stage_stat.st_ino)
            == (stage_entry.st_dev, stage_entry.st_ino)
            and stage_stat.st_uid == os.geteuid()
            and stage_stat.st_nlink >= 2
            and stat.S_IMODE(stage_stat.st_mode) == 0o700,
            "PRIVATE_STAGE_DIRECTORY_FD_MODE_OWNER_BINDING",
        )
        return resolved, parent_fd, stage_fd
    except BaseException:
        if stage_fd is not None:
            os.close(stage_fd)
        os.close(parent_fd)
        raise


def exclusive_private_write(
    stage_fd: int,
    filename: str,
    payload: bytes,
    audit: Counter[str] | None = None,
) -> dict[str, Any]:
    """Create one flat 0600 file without an existence check or replacement."""

    need(
        filename == Path(filename).name and filename not in {"", ".", ".."},
        "PRIVATE_STAGE_NON_FLAT_FILENAME",
    )
    flags = (
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC
    )
    try:
        descriptor = os.open(filename, flags, 0o600, dir_fd=stage_fd)
    except FileExistsError as error:
        raise PromotionBlocked(
            "PRIVATE_STAGE_REFUSES_EXISTING_OR_RACED_TARGET:" + filename
        ) from error
    try:
        os.fchmod(descriptor, 0o600)
        opened = os.fstat(descriptor)
        need(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and opened.st_uid == os.geteuid()
            and stat.S_IMODE(opened.st_mode) == 0o600,
            "PRIVATE_STAGE_FILE_FD_MODE_LINK_OWNER:" + filename,
        )
        view = memoryview(payload)
        written = 0
        while written < len(view):
            count = os.write(descriptor, view[written:])
            need(count > 0, "PRIVATE_STAGE_ZERO_LENGTH_WRITE:" + filename)
            written += count
        need(written == len(payload), "PRIVATE_STAGE_SHORT_WRITE:" + filename)
        record_fsync(descriptor, "private_file", audit)
        final = os.fstat(descriptor)
        need(
            final.st_size == len(payload)
            and final.st_nlink == 1
            and stat.S_ISREG(final.st_mode),
            "PRIVATE_STAGE_FINAL_FILE_FSTAT:" + filename,
        )
    finally:
        os.close(descriptor)
    entry = os.stat(filename, dir_fd=stage_fd, follow_symlinks=False)
    need(
        (entry.st_dev, entry.st_ino) == (final.st_dev, final.st_ino)
        and stat.S_ISREG(entry.st_mode),
        "PRIVATE_STAGE_FINAL_FILE_ENTRY_BINDING:" + filename,
    )
    return {
        "filename": filename,
        "file_size_bytes": len(payload),
        "file_sha256": hashlib.sha256(payload).hexdigest(),
        "mode_octal": "0600",
        "link_count": 1,
        "owned_by_effective_uid": True,
    }


def emit_private_stage(stage: Path) -> dict[str, Any]:
    bundle, raw, audit = build_full_candidate_bytes()
    durability: Counter[str] = Counter()
    resolved, parent_fd, stage_fd = create_private_stage_directory(
        stage, durability,
    )
    file_audit: list[dict[str, Any]] = []
    try:
        for key in ("physical", "anchor", "contact", "owner", "edge", "result"):
            file_audit.append(exclusive_private_write(
                stage_fd, OUTPUT_NAMES[key], raw[key], durability,
            ))
        record_fsync(stage_fd, "stage_directory_after_files", durability)
        entry = os.stat(
            resolved.name, dir_fd=parent_fd, follow_symlinks=False,
        )
        bound = os.fstat(stage_fd)
        need(
            (entry.st_dev, entry.st_ino) == (bound.st_dev, bound.st_ino),
            "PRIVATE_STAGE_FINAL_DIRECTORY_ENTRY_BINDING",
        )
        record_fsync(parent_fd, "parent_directory_after_files", durability)
    finally:
        os.close(stage_fd)
        os.close(parent_fd)
    # Deliberately no manifest: this directory is not a formal publication.
    return {
        **audit,
        "private_stage_directory": str(resolved),
        "private_stage_written": True,
        "private_stage_directory_mode_octal": "0700",
        "private_stage_file_audit": file_audit,
        "private_stage_durability_audit": dict(sorted(durability.items())),
        "private_stage_never_replaces_or_overwrites": True,
        "private_stage_symlink_parent_chain_rejected": True,
        "formal_deliverables_written": False,
        "manifest_emitted": False,
    }


def private_stage_writer_selftest_report() -> dict[str, Any]:
    """Hostile no-publication fixtures for the fd-bound private writer."""

    outcomes: dict[str, bool] = {}
    with tempfile.TemporaryDirectory(
        prefix=".cm2-r305b-private-writer-selftest-", dir=ROOT,
    ) as temporary:
        sandbox = Path(temporary)
        os.chmod(sandbox, 0o700)
        durability: Counter[str] = Counter()
        stage = sandbox / "exact-stage"
        resolved, parent_fd, stage_fd = create_private_stage_directory(
            stage, durability,
        )
        try:
            stage_stat = os.fstat(stage_fd)
            need(
                stat.S_IMODE(stage_stat.st_mode) == 0o700,
                "PRIVATE_STAGE_SELFTEST_DIRECTORY_MODE",
            )
            file_result = exclusive_private_write(
                stage_fd, "race-target.bin", b"ORIGINAL", durability,
            )
            need(
                file_result["mode_octal"] == "0600"
                and (resolved / "race-target.bin").read_bytes() == b"ORIGINAL",
                "PRIVATE_STAGE_SELFTEST_FILE_MODE_CONTENT",
            )
            try:
                exclusive_private_write(
                    stage_fd, "race-target.bin", b"OVERWRITE", durability,
                )
            except PromotionBlocked:
                outcomes["preexisting_or_raced_target_rejected"] = True
            else:
                raise PromotionBlocked("PRIVATE_STAGE_SELFTEST_TARGET_RACE_ACCEPTED")
            need(
                (resolved / "race-target.bin").read_bytes() == b"ORIGINAL",
                "PRIVATE_STAGE_SELFTEST_TARGET_RACE_OVERWROTE",
            )

            os.symlink("race-target.bin", "file-symlink.bin", dir_fd=stage_fd)
            try:
                exclusive_private_write(
                    stage_fd, "file-symlink.bin", b"OVERWRITE", durability,
                )
            except PromotionBlocked:
                outcomes["preexisting_file_symlink_rejected"] = True
            else:
                raise PromotionBlocked("PRIVATE_STAGE_SELFTEST_FILE_SYMLINK_ACCEPTED")
            need(
                (resolved / "race-target.bin").read_bytes() == b"ORIGINAL",
                "PRIVATE_STAGE_SELFTEST_FILE_SYMLINK_OVERWROTE",
            )
            record_fsync(stage_fd, "stage_directory_after_files", durability)
            record_fsync(parent_fd, "parent_directory_after_files", durability)
        finally:
            os.close(stage_fd)
            os.close(parent_fd)

        try:
            duplicate = create_private_stage_directory(stage)
        except PromotionBlocked:
            outcomes["duplicate_existing_directory_rejected"] = True
        else:
            os.close(duplicate[2])
            os.close(duplicate[1])
            raise PromotionBlocked("PRIVATE_STAGE_SELFTEST_DUPLICATE_DIRECTORY_ACCEPTED")

        real_parent = sandbox / "real-parent"
        real_parent.mkdir(mode=0o700)
        parent_symlink = sandbox / "parent-symlink"
        parent_symlink.symlink_to(real_parent.name, target_is_directory=True)
        try:
            escaped = create_private_stage_directory(parent_symlink / "stage")
        except PromotionBlocked:
            outcomes["parent_symlink_rejected"] = True
        else:
            os.close(escaped[2])
            os.close(escaped[1])
            raise PromotionBlocked("PRIVATE_STAGE_SELFTEST_PARENT_SYMLINK_ACCEPTED")

        need(
            durability == {
                "parent_directory_after_mkdir": 1,
                "private_file": 1,
                "stage_directory_after_files": 1,
                "parent_directory_after_files": 1,
            },
            "PRIVATE_STAGE_SELFTEST_FSYNC_COUNTS",
        )
        outcomes["directory_mode_0700"] = True
        outcomes["file_mode_0600"] = True
        outcomes["file_and_directory_fsync_path_exercised"] = True
        outcomes["no_replace_or_overwrite_path_exists"] = True
    need(
        not Path(temporary).exists(),
        "PRIVATE_STAGE_SELFTEST_TEMPORARY_TREE_NOT_REMOVED",
    )
    return {
        "status": (
            "PASS_PRIVATE_STAGE_FD_BOUND_EXCLUSIVE_WRITER_HOSTILE_SELFTEST__"
            "NO_CANDIDATE_OUTPUT__ZERO_CREDIT"
        ),
        "hostile_fixture_results": dict(sorted(outcomes.items())),
        "formal_Round305B_credit": 0,
    }


def publication_file_identity(info: os.stat_result) -> tuple[int, ...]:
    """Identity used to reject input/output replacement during publication."""

    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_uid,
        info.st_nlink,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def publication_inode_identity(info: os.stat_result) -> tuple[int, int]:
    """Stable identity retained across a same-filesystem rename."""

    return (info.st_dev, info.st_ino)


def publication_directory_identity(info: os.stat_result) -> tuple[int, ...]:
    """Stable directory identity; mutable timestamps are deliberately absent."""

    return (info.st_dev, info.st_ino, info.st_mode, info.st_uid)


def snapshot_candidate_publication_inputs() -> dict[Path, tuple[int, ...]]:
    """Snapshot the complete manifest/member closure before candidate build."""

    manifest_specs: list[tuple[str, str]] = [
        (name, pin) for name, (pin, _count) in FORMAL_MANIFEST_PINS.items()
    ]
    manifest_specs.extend((
        (R303B_MANIFEST, R303B_MANIFEST_SHA256),
        (R304_MANIFEST, R304_MANIFEST_SHA256),
        (R305A_MANIFEST, str(R305A_MANIFEST_SHA256)),
    ))
    paths = {
        Path(os.path.abspath(os.fspath(__file__))),
        D / WIRE_SPEC_FILENAME,
        D / WIRE_CONTRACT_FIXTURE_FILENAME,
    }
    # Some source pins are transitive runtime dependencies or intentionally
    # reference-only lineage inputs rather than members of the admitted
    # manifests.  They still affect the committed proof closure and therefore
    # must remain inode/size/time stable throughout candidate construction and
    # publication.
    explicit_source_pins = {
        filename: pin
        for _module_name, filename, pin in CACHELESS_RUNTIME_SOURCE_MODULES
    }
    explicit_source_pins.update(REFERENCE_ONLY_SOURCE_PINS)
    paths.update(
        D / filename
        for _module_name, filename, _pin in CACHELESS_RUNTIME_SOURCE_MODULES
    )
    paths.update(D / filename for filename in REFERENCE_ONLY_SOURCE_PINS)
    for manifest_name, manifest_pin in manifest_specs:
        entries = parse_manifest(manifest_name, manifest_pin)
        paths.add(D / manifest_name)
        paths.update(D / member for member in entries)

    snapshots: dict[Path, tuple[int, ...]] = {}
    for path in sorted(paths, key=lambda item: str(item)):
        try:
            info = os.lstat(path)
        except FileNotFoundError as error:
            raise PromotionBlocked(
                "CANDIDATE_PUBLICATION_INPUT_MISSING:" + path.name
            ) from error
        need(
            stat.S_ISREG(info.st_mode)
            and not stat.S_ISLNK(info.st_mode)
            and info.st_uid == os.geteuid()
            and info.st_nlink == 1,
            "CANDIDATE_PUBLICATION_INPUT_BOUNDARY:" + path.name,
        )
        if path.name in explicit_source_pins:
            need(
                file_sha256(path) == explicit_source_pins[path.name],
                "CANDIDATE_PUBLICATION_EXPLICIT_SOURCE_PIN:" + path.name,
            )
        snapshots[path] = publication_file_identity(info)
    return snapshots


def assert_candidate_publication_inputs_unchanged(
    snapshots: dict[Path, tuple[int, ...]] | None,
    label: str,
) -> None:
    if snapshots is None:
        return
    for path, expected in sorted(
        snapshots.items(), key=lambda item: str(item[0]),
    ):
        try:
            observed = os.lstat(path)
        except FileNotFoundError as error:
            raise PromotionBlocked(
                "CANDIDATE_PUBLICATION_INPUT_DISAPPEARED:"
                + label + ":" + path.name
            ) from error
        need(
            not stat.S_ISLNK(observed.st_mode)
            and publication_file_identity(observed) == expected,
            "CANDIDATE_PUBLICATION_INPUT_DRIFT:"
            + label + ":" + path.name,
        )


def exact_candidate_output_directory(output_dir: Path) -> Path:
    """Accept only this workspace's exact deliverables directory."""

    lexical = Path(os.path.abspath(os.fspath(output_dir)))
    expected = Path(os.path.abspath(os.fspath(D)))
    need(
        lexical == expected,
        "CANDIDATE_PUBLICATION_OUTPUT_MUST_BE_EXACT_DELIVERABLES_DIRECTORY",
    )
    return lexical


def open_bound_candidate_directory(directory: Path) -> tuple[int, tuple[int, ...]]:
    """Open a workspace directory through the existing no-symlink fd walk."""

    lexical = Path(os.path.abspath(os.fspath(directory)))
    descriptor = open_workspace_parent_fd(lexical)
    try:
        entry = os.lstat(lexical)
        bound = os.fstat(descriptor)
        identity = publication_directory_identity(bound)
        need(
            stat.S_ISDIR(entry.st_mode)
            and not stat.S_ISLNK(entry.st_mode)
            and entry.st_uid == os.geteuid()
            and identity == publication_directory_identity(entry),
            "CANDIDATE_PUBLICATION_DIRECTORY_FD_BINDING",
        )
        return descriptor, identity
    except BaseException:
        os.close(descriptor)
        raise


def assert_candidate_directory_unchanged(
    directory: Path,
    descriptor: int,
    expected: tuple[int, ...],
    label: str,
) -> None:
    try:
        entry = os.lstat(directory)
    except FileNotFoundError as error:
        raise PromotionBlocked(
            "CANDIDATE_PUBLICATION_DIRECTORY_DISAPPEARED:" + label
        ) from error
    need(
        not stat.S_ISLNK(entry.st_mode)
        and publication_directory_identity(entry) == expected
        and publication_directory_identity(os.fstat(descriptor)) == expected,
        "CANDIDATE_PUBLICATION_DIRECTORY_SWAP:" + label,
    )


def candidate_rename_noreplace(
    source_directory_descriptor: int,
    source_name: str,
    target_directory_descriptor: int,
    target_name: str,
) -> None:
    """Linux atomic renameat2 with the mandatory no-replace flag."""

    function = getattr(ctypes.CDLL(None, use_errno=True), "renameat2", None)
    need(
        function is not None,
        "CANDIDATE_PUBLICATION_RENAMEAT2_NOREPLACE_UNAVAILABLE",
    )
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
        RENAME_NOREPLACE,
    )
    if outcome == 0:
        return
    error_number = ctypes.get_errno()
    if error_number == errno.EEXIST:
        raise FileExistsError(
            error_number, os.strerror(error_number), target_name,
        )
    raise OSError(error_number, os.strerror(error_number), target_name)


def read_candidate_file_exact_at(
    directory_descriptor: int,
    filename: str,
    expected: bytes,
    label: str,
) -> tuple[int, ...]:
    """Read exact bytes through a no-follow fd and bind both filename ends."""

    need(
        filename == Path(filename).name and filename not in {"", ".", ".."},
        "CANDIDATE_PUBLICATION_NON_FLAT_FILENAME:" + label,
    )
    try:
        entry = os.stat(
            filename, dir_fd=directory_descriptor, follow_symlinks=False,
        )
    except FileNotFoundError as error:
        raise PromotionBlocked(
            "CANDIDATE_PUBLICATION_FILE_MISSING:" + label
        ) from error
    expected_identity = publication_file_identity(entry)
    need(
        stat.S_ISREG(entry.st_mode)
        and not stat.S_ISLNK(entry.st_mode)
        and entry.st_uid == os.geteuid()
        and entry.st_nlink == 1
        and entry.st_size == len(expected),
        "CANDIDATE_PUBLICATION_FILE_BOUNDARY:" + label,
    )
    descriptor = os.open(
        filename,
        os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
        dir_fd=directory_descriptor,
    )
    try:
        need(
            publication_file_identity(os.fstat(descriptor)) == expected_identity,
            "CANDIDATE_PUBLICATION_FILE_OPEN_RACE:" + label,
        )
        blocks: list[bytes] = []
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            blocks.append(block)
        need(
            b"".join(blocks) == expected,
            "CANDIDATE_PUBLICATION_FILE_EXACT_BYTES:" + label,
        )
        need(
            publication_file_identity(os.fstat(descriptor)) == expected_identity,
            "CANDIDATE_PUBLICATION_FILE_FD_DRIFT:" + label,
        )
    finally:
        os.close(descriptor)
    final_entry = os.stat(
        filename, dir_fd=directory_descriptor, follow_symlinks=False,
    )
    need(
        publication_file_identity(final_entry) == expected_identity,
        "CANDIDATE_PUBLICATION_FILE_NAME_SWAP:" + label,
    )
    return expected_identity


def candidate_visible_prefix(
    output_descriptor: int,
    artifacts: dict[str, bytes],
) -> tuple[list[str], dict[str, tuple[int, ...]]]:
    """Admit only an exact existing prefix; later-without-earlier is invalid."""

    prefix: list[str] = []
    identities: dict[str, tuple[int, ...]] = {}
    missing_seen = False
    for filename in CANDIDATE_COMMIT_ORDER:
        try:
            os.stat(
                filename,
                dir_fd=output_descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            missing_seen = True
            continue
        need(
            not missing_seen,
            "CANDIDATE_PUBLICATION_NONPREFIX_VISIBLE_SET:" + filename,
        )
        identities[filename] = read_candidate_file_exact_at(
            output_descriptor,
            filename,
            artifacts[filename],
            "visible-prefix:" + filename,
        )
        prefix.append(filename)
    return prefix, identities


def recover_exact_candidate_stages(
    output_descriptor: int,
    artifacts: dict[str, bytes],
    durability: Counter[str],
) -> int:
    """Remove only owned 0700 orphan stages containing an exact byte subset."""

    recovered = 0
    for stage_name in sorted(os.listdir(output_descriptor)):
        if not stage_name.startswith(CANDIDATE_STAGE_PREFIX):
            continue
        need(
            re.fullmatch(
                re.escape(CANDIDATE_STAGE_PREFIX) + r"[0-9a-f]{32}",
                stage_name,
            ) is not None,
            "CANDIDATE_PUBLICATION_ORPHAN_STAGE_NAME_BOUNDARY:" + stage_name,
        )
        stage_entry = os.stat(
            stage_name,
            dir_fd=output_descriptor,
            follow_symlinks=False,
        )
        need(
            stat.S_ISDIR(stage_entry.st_mode)
            and not stat.S_ISLNK(stage_entry.st_mode)
            and stage_entry.st_uid == os.geteuid()
            and stat.S_IMODE(stage_entry.st_mode) == 0o700,
            "CANDIDATE_PUBLICATION_ORPHAN_STAGE_BOUNDARY:" + stage_name,
        )
        stage_descriptor = os.open(
            stage_name,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=output_descriptor,
        )
        try:
            need(
                publication_directory_identity(os.fstat(stage_descriptor))
                == publication_directory_identity(stage_entry),
                "CANDIDATE_PUBLICATION_ORPHAN_STAGE_OPEN_RACE:" + stage_name,
            )
            names = set(os.listdir(stage_descriptor))
            need(
                names <= set(artifacts),
                "CANDIDATE_PUBLICATION_ORPHAN_STAGE_UNKNOWN_MEMBER:"
                + stage_name,
            )
            # Validate every file before mutating any part of this stage.
            for filename in sorted(names):
                read_candidate_file_exact_at(
                    stage_descriptor,
                    filename,
                    artifacts[filename],
                    "orphan-stage:" + stage_name + ":" + filename,
                )
            for filename in sorted(names):
                os.unlink(filename, dir_fd=stage_descriptor)
            record_fsync(
                stage_descriptor,
                "orphan_stage_directory_after_exact_cleanup",
                durability,
            )
        finally:
            os.close(stage_descriptor)
        os.rmdir(stage_name, dir_fd=output_descriptor)
        record_fsync(
            output_descriptor,
            "output_directory_after_orphan_stage_removal",
            durability,
        )
        recovered += 1
    return recovered


def create_candidate_stage(
    output_descriptor: int,
    durability: Counter[str],
) -> tuple[str, int]:
    """Create an fd-bound owned 0700 transaction stage inside output."""

    stage_name: str | None = None
    for _attempt in range(128):
        candidate = CANDIDATE_STAGE_PREFIX + os.urandom(16).hex()
        try:
            os.mkdir(candidate, mode=0o700, dir_fd=output_descriptor)
        except FileExistsError:
            continue
        stage_name = candidate
        break
    need(stage_name is not None, "CANDIDATE_PUBLICATION_STAGE_NAME_EXHAUSTED")
    record_fsync(
        output_descriptor,
        "output_directory_after_stage_mkdir",
        durability,
    )
    entry = os.stat(
        stage_name, dir_fd=output_descriptor, follow_symlinks=False,
    )
    descriptor = os.open(
        stage_name,
        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
        dir_fd=output_descriptor,
    )
    try:
        os.fchmod(descriptor, 0o700)
        bound = os.fstat(descriptor)
        need(
            publication_directory_identity(bound)
            == publication_directory_identity(entry)
            and bound.st_uid == os.geteuid()
            and stat.S_IMODE(bound.st_mode) == 0o700,
            "CANDIDATE_PUBLICATION_STAGE_FD_MODE_OWNER_BINDING",
        )
        return stage_name, descriptor
    except BaseException:
        os.close(descriptor)
        raise


def exclusive_candidate_stage_write(
    stage_descriptor: int,
    filename: str,
    payload: bytes,
    durability: Counter[str],
) -> None:
    """Write one exact staged candidate file, never replacing a name."""

    need(
        filename == Path(filename).name and filename not in {"", ".", ".."},
        "CANDIDATE_PUBLICATION_STAGE_NON_FLAT_FILENAME",
    )
    try:
        descriptor = os.open(
            filename,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            0o644,
            dir_fd=stage_descriptor,
        )
    except FileExistsError as error:
        raise PromotionBlocked(
            "CANDIDATE_PUBLICATION_STAGE_REFUSES_EXISTING:" + filename
        ) from error
    try:
        os.fchmod(descriptor, 0o644)
        opened = os.fstat(descriptor)
        need(
            stat.S_ISREG(opened.st_mode)
            and opened.st_uid == os.geteuid()
            and opened.st_nlink == 1
            and stat.S_IMODE(opened.st_mode) == 0o644,
            "CANDIDATE_PUBLICATION_STAGE_FILE_BOUNDARY:" + filename,
        )
        view = memoryview(payload)
        offset = 0
        while offset < len(view):
            written = os.write(descriptor, view[offset:])
            need(
                written > 0,
                "CANDIDATE_PUBLICATION_STAGE_ZERO_WRITE:" + filename,
            )
            offset += written
        need(
            offset == len(payload),
            "CANDIDATE_PUBLICATION_STAGE_SHORT_WRITE:" + filename,
        )
        record_fsync(
            descriptor, "staged_candidate_file", durability,
        )
        final = os.fstat(descriptor)
        need(
            final.st_size == len(payload)
            and final.st_nlink == 1
            and stat.S_ISREG(final.st_mode),
            "CANDIDATE_PUBLICATION_STAGE_FINAL_FSTAT:" + filename,
        )
    finally:
        os.close(descriptor)
    read_candidate_file_exact_at(
        stage_descriptor,
        filename,
        payload,
        "new-stage:" + filename,
    )


def remove_exact_candidate_stage(
    output_descriptor: int,
    stage_name: str,
    stage_descriptor: int,
    artifacts: dict[str, bytes],
    durability: Counter[str],
) -> None:
    """Remove the current stage only after exact-subset validation."""

    try:
        names = set(os.listdir(stage_descriptor))
        need(
            names <= set(artifacts),
            "CANDIDATE_PUBLICATION_ACTIVE_STAGE_UNKNOWN_MEMBER",
        )
        for filename in sorted(names):
            read_candidate_file_exact_at(
                stage_descriptor,
                filename,
                artifacts[filename],
                "active-stage-cleanup:" + filename,
            )
        for filename in sorted(names):
            os.unlink(filename, dir_fd=stage_descriptor)
        record_fsync(
            stage_descriptor,
            "active_stage_directory_after_exact_cleanup",
            durability,
        )
    finally:
        os.close(stage_descriptor)
    os.rmdir(stage_name, dir_fd=output_descriptor)
    record_fsync(
        output_descriptor,
        "output_directory_after_active_stage_removal",
        durability,
    )


def rollback_new_candidate_result_marker(
    output_descriptor: int,
    artifacts: dict[str, bytes],
    published_now: dict[str, tuple[int, int]],
    durability: Counter[str],
) -> bool:
    """Remove only this call's exact result marker after a failed commit."""

    marker = CANDIDATE_COMMIT_ORDER[-1]
    expected_inode = published_now.get(marker)
    if expected_inode is None:
        return False
    try:
        entry = os.stat(
            marker, dir_fd=output_descriptor, follow_symlinks=False,
        )
    except FileNotFoundError:
        return False
    need(
        publication_inode_identity(entry) == expected_inode,
        "CANDIDATE_PUBLICATION_RESULT_MARKER_ROLLBACK_INODE_DRIFT",
    )
    read_candidate_file_exact_at(
        output_descriptor,
        marker,
        artifacts[marker],
        "failed-transaction-result-marker-rollback",
    )
    os.unlink(marker, dir_fd=output_descriptor)
    record_fsync(
        output_descriptor,
        "output_directory_after_result_marker_rollback",
        durability,
    )
    try:
        os.stat(marker, dir_fd=output_descriptor, follow_symlinks=False)
    except FileNotFoundError:
        return True
    raise PromotionBlocked(
        "CANDIDATE_PUBLICATION_RESULT_MARKER_ROLLBACK_NAME_REAPPEARED"
    )


def publish_candidate_prefix_transaction(
    output_directory: Path,
    output_descriptor: int,
    artifacts: dict[str, bytes],
    input_snapshots: dict[Path, tuple[int, ...]] | None = None,
    hostile_hook: Callable[[str, str, int], None] | None = None,
) -> dict[str, Any]:
    """Publish five ledgers then result as an exact resumable prefix."""

    need(
        tuple(artifacts) == CANDIDATE_COMMIT_ORDER
        and set(artifacts) == set(CANDIDATE_COMMIT_ORDER),
        "CANDIDATE_PUBLICATION_EXACT_ORDERED_SIX_FILE_SET",
    )
    need(
        all(type(payload) is bytes and payload for payload in artifacts.values()),
        "CANDIDATE_PUBLICATION_NONEMPTY_BYTE_PAYLOADS",
    )
    directory_identity = publication_directory_identity(
        os.fstat(output_descriptor)
    )
    durability: Counter[str] = Counter()
    recovered_stage_count = 0
    fcntl.flock(output_descriptor, fcntl.LOCK_EX)
    try:
        assert_candidate_directory_unchanged(
            output_directory,
            output_descriptor,
            directory_identity,
            "locked-preflight",
        )
        assert_candidate_publication_inputs_unchanged(
            input_snapshots, "locked-preflight",
        )
        # Conflict/nonprefix validation is read-only and must precede orphan
        # cleanup, so a doomed transaction cannot mutate even an exact stage.
        prefix, preexisting_identities = candidate_visible_prefix(
            output_descriptor, artifacts,
        )
        recovered_stage_count = recover_exact_candidate_stages(
            output_descriptor, artifacts, durability,
        )
        prefix_after_recovery, identities_after_recovery = (
            candidate_visible_prefix(output_descriptor, artifacts)
        )
        need(
            prefix_after_recovery == prefix
            and identities_after_recovery == preexisting_identities,
            "CANDIDATE_PUBLICATION_PREFIX_DRIFT_DURING_ORPHAN_RECOVERY",
        )
        preexisting_count = len(prefix)
        if preexisting_count == len(CANDIDATE_COMMIT_ORDER):
            assert_candidate_publication_inputs_unchanged(
                input_snapshots, "idempotent-complete",
            )
            assert_candidate_directory_unchanged(
                output_directory,
                output_descriptor,
                directory_identity,
                "idempotent-complete",
            )
            return {
                "status": (
                    "PASS_EXACT_EXISTING_ROUND305B_ZERO_CREDIT_CANDIDATE_"
                    "SIX_FILE_PREFIX_IDEMPOTENT__ZERO_OFFICIALLY_ADMITTED_CREDIT"
                ),
                "candidate_commit_order": list(CANDIDATE_COMMIT_ORDER),
                "candidate_result_commit_marker": CANDIDATE_COMMIT_ORDER[-1],
                "preexisting_exact_prefix_file_count": preexisting_count,
                "newly_published_file_count": 0,
                "recovered_exact_orphan_stage_count": recovered_stage_count,
                "exact_existing_idempotent": True,
                "candidate_six_file_commit_complete": True,
                "formal_promotion_admitted": False,
                "officially_admitted_anchor_binding_credit": 0,
                "officially_admitted_physical_witness_credit": 0,
                "officially_admitted_component_edge_credit": 0,
                "official_key_merge_credit": 0,
                "D4_transfer_credit": 0,
                "owner_sidecar_credit": 0,
                "formal_DSU_rank_reduction_credit": 0,
                "formal_maximality_credit": 0,
                "formal_fibre_credit": 0,
                "formal_global_disposition_credit": 0,
                "durability_audit": dict(sorted(durability.items())),
            }

        stage_name, stage_descriptor = create_candidate_stage(
            output_descriptor, durability,
        )
        committed_identities = dict(preexisting_identities)
        published_now: dict[str, tuple[int, int]] = {}

        def verify_committed_prefix(expected_count: int, label: str) -> None:
            visible, identities = candidate_visible_prefix(
                output_descriptor, artifacts,
            )
            need(
                tuple(visible) == CANDIDATE_COMMIT_ORDER[:expected_count],
                "CANDIDATE_PUBLICATION_COMMITTED_PREFIX_CENSUS:"
                + label,
            )
            need(
                set(committed_identities)
                == set(CANDIDATE_COMMIT_ORDER[:expected_count]),
                "CANDIDATE_PUBLICATION_COMMITTED_IDENTITY_CENSUS:"
                + label,
            )
            for committed_name, expected_identity in (
                committed_identities.items()
            ):
                need(
                    identities[committed_name] == expected_identity,
                    "CANDIDATE_PUBLICATION_COMMITTED_PREFIX_DRIFT:"
                    + label + ":" + committed_name,
                )

        publication_error: BaseException | None = None
        try:
            for filename in CANDIDATE_COMMIT_ORDER:
                exclusive_candidate_stage_write(
                    stage_descriptor,
                    filename,
                    artifacts[filename],
                    durability,
                )
            record_fsync(
                stage_descriptor,
                "stage_directory_before_candidate_commit",
                durability,
            )
            for index, filename in enumerate(CANDIDATE_COMMIT_ORDER):
                if index < preexisting_count:
                    observed = read_candidate_file_exact_at(
                        output_descriptor,
                        filename,
                        artifacts[filename],
                        "stable-preexisting-prefix:" + filename,
                    )
                    need(
                        observed == preexisting_identities[filename],
                        "CANDIDATE_PUBLICATION_PREEXISTING_PREFIX_DRIFT:"
                        + filename,
                    )
                    continue
                if hostile_hook is not None:
                    hostile_hook("before-rename", filename, output_descriptor)
                verify_committed_prefix(index, "before-rename:" + filename)
                assert_candidate_publication_inputs_unchanged(
                    input_snapshots, "before-rename:" + filename,
                )
                assert_candidate_directory_unchanged(
                    output_directory,
                    output_descriptor,
                    directory_identity,
                    "before-rename:" + filename,
                )
                try:
                    os.stat(
                        filename,
                        dir_fd=output_descriptor,
                        follow_symlinks=False,
                    )
                except FileNotFoundError:
                    pass
                else:
                    raise PromotionBlocked(
                        "CANDIDATE_PUBLICATION_TARGET_APPEARED_AFTER_PREFLIGHT:"
                        + filename
                    )
                staged_identity = read_candidate_file_exact_at(
                    stage_descriptor,
                    filename,
                    artifacts[filename],
                    "immediately-before-rename:" + filename,
                )
                try:
                    candidate_rename_noreplace(
                        stage_descriptor,
                        filename,
                        output_descriptor,
                        filename,
                    )
                except FileExistsError as error:
                    raise PromotionBlocked(
                        "CANDIDATE_PUBLICATION_TARGET_RACED_RENAME_NOREPLACE:"
                        + filename
                    ) from error
                published_now[filename] = (
                    staged_identity[0], staged_identity[1]
                )
                record_fsync(
                    stage_descriptor,
                    "stage_directory_after_candidate_rename",
                    durability,
                )
                record_fsync(
                    output_descriptor,
                    "output_directory_after_candidate_rename",
                    durability,
                )
                if hostile_hook is not None:
                    hostile_hook("after-rename", filename, output_descriptor)
                committed_identity = read_candidate_file_exact_at(
                    output_descriptor,
                    filename,
                    artifacts[filename],
                    "immediately-after-rename:" + filename,
                )
                need(
                    (committed_identity[0], committed_identity[1])
                    == published_now[filename],
                    "CANDIDATE_PUBLICATION_RENAME_INODE_DRIFT:" + filename,
                )
                committed_identities[filename] = committed_identity
        except BaseException as error:
            publication_error = error
            rollback_new_candidate_result_marker(
                output_descriptor, artifacts, published_now, durability,
            )
            raise
        finally:
            try:
                remove_exact_candidate_stage(
                    output_descriptor,
                    stage_name,
                    stage_descriptor,
                    artifacts,
                    durability,
                )
            except BaseException as cleanup_error:
                rollback_new_candidate_result_marker(
                    output_descriptor, artifacts, published_now, durability,
                )
                if publication_error is None:
                    raise
                raise PromotionBlocked(
                    "CANDIDATE_PUBLICATION_ACTIVE_STAGE_CLEANUP_FAILED"
                ) from cleanup_error

        try:
            verify_committed_prefix(
                len(CANDIDATE_COMMIT_ORDER), "committed-final",
            )
            assert_candidate_publication_inputs_unchanged(
                input_snapshots, "committed-final",
            )
            assert_candidate_directory_unchanged(
                output_directory,
                output_descriptor,
                directory_identity,
                "committed-final",
            )
        except BaseException:
            rollback_new_candidate_result_marker(
                output_descriptor, artifacts, published_now, durability,
            )
            raise
        return {
            "status": (
                "PASS_ROUND305B_ZERO_CREDIT_CANDIDATE_SIX_FILE_PREFIX_"
                "TRANSACTION__PENDING_INDEPENDENT_VERIFICATION__"
                "ZERO_OFFICIALLY_ADMITTED_CREDIT"
            ),
            "candidate_commit_order": list(CANDIDATE_COMMIT_ORDER),
            "candidate_result_commit_marker": CANDIDATE_COMMIT_ORDER[-1],
            "preexisting_exact_prefix_file_count": preexisting_count,
            "newly_published_file_count": (
                len(CANDIDATE_COMMIT_ORDER) - preexisting_count
            ),
            "recovered_exact_orphan_stage_count": recovered_stage_count,
            "exact_existing_idempotent": False,
            "candidate_six_file_commit_complete": True,
            "formal_promotion_admitted": False,
            "officially_admitted_anchor_binding_credit": 0,
            "officially_admitted_physical_witness_credit": 0,
            "officially_admitted_component_edge_credit": 0,
            "official_key_merge_credit": 0,
            "D4_transfer_credit": 0,
            "owner_sidecar_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "durability_audit": dict(sorted(durability.items())),
        }
    finally:
        fcntl.flock(output_descriptor, fcntl.LOCK_UN)


def publish_zero_credit_candidate(output_dir: Path) -> dict[str, Any]:
    """Build once, then publish only those exact six bytes with zero credit."""

    need(
        DIRECT_GEOMETRY_KERNEL_IMPLEMENTED
        and FORMAL_GEOMETRY_KERNEL_IMPLEMENTED,
        "CANDIDATE_PUBLICATION_GEOMETRY_KERNEL_NOT_IMPLEMENTED",
    )
    need(
        CANDIDATE_PUBLICATION_ENABLED,
        "CANDIDATE_PUBLICATION_EXPLICIT_GATE_DISABLED",
    )
    resolved = exact_candidate_output_directory(output_dir)
    input_snapshots = snapshot_candidate_publication_inputs()
    bundle, raw, audit = build_full_candidate_bytes()
    assert_candidate_publication_inputs_unchanged(
        input_snapshots, "after-build-before-publication",
    )
    need(
        tuple(raw) == CANDIDATE_OUTPUT_KEYS,
        "CANDIDATE_PUBLICATION_BUILD_BYTE_KEYS",
    )
    result = bundle["result"]
    boundary = result["strict_credit_boundary"]
    need(
        result["zero_credit_candidate_publication_permitted"] is True
        and result["manifest_emitted"] is False
        and boundary["zero_credit_candidate_publication_only"] is True
        and boundary["independent_verifier_admitted"] is False
        and boundary["officially_admitted_anchor_binding_credit"] == 0
        and boundary["officially_admitted_physical_witness_credit"] == 0
        and boundary["officially_admitted_component_edge_credit"] == 0
        and boundary["official_key_merge_credit"] == 0
        and boundary["D4_transfer_credit"] == 0
        and boundary["owner_sidecar_credit"] == 0
        and boundary["formal_DSU_rank_reduction_credit"] == 0
        and boundary["formal_maximality_credit"] == 0
        and boundary["formal_fibre_credit"] == 0
        and boundary["formal_global_disposition_credit"] == 0,
        "CANDIDATE_PUBLICATION_NONZERO_OR_UNTRUTHFUL_CREDIT_BOUNDARY",
    )
    # This mapping is the formal path's sole byte source.  The transaction
    # writes and renames values without reserialization or transformation.
    artifacts = {
        OUTPUT_NAMES[key]: raw[key] for key in CANDIDATE_OUTPUT_KEYS
    }
    output_descriptor, directory_identity = open_bound_candidate_directory(
        resolved
    )
    try:
        need(
            publication_directory_identity(os.fstat(output_descriptor))
            == directory_identity,
            "CANDIDATE_PUBLICATION_OUTPUT_FD_DRIFT_BEFORE_LOCK",
        )
        receipt = publish_candidate_prefix_transaction(
            resolved,
            output_descriptor,
            artifacts,
            input_snapshots,
        )
    finally:
        os.close(output_descriptor)
    return {
        **audit,
        "status": receipt["status"],
        "candidate_publication": receipt,
        "candidate_bytes_source_function": "build_full_candidate_bytes",
        "candidate_bytes_reserialized_after_build": False,
        "candidate_publication_is_independent_verification": False,
        "candidate_publication_is_formal_promotion": False,
        "manifest_emitted": False,
        "officially_admitted_formal_anchor_binding_credit": 0,
        "officially_admitted_formal_physical_witness_credit": 0,
        "officially_admitted_formal_component_edge_credit": 0,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
    }


def candidate_publisher_hostile_selftest_report() -> dict[str, Any]:
    """Data-free hostile fixtures for the exact six-file prefix transaction."""

    artifacts = {
        filename: b"ROUND305B-ZERO-CREDIT-FIXTURE:" + filename.encode("ascii")
        for filename in CANDIDATE_COMMIT_ORDER
    }
    outcomes: dict[str, bool] = {}

    def fixture_directory(parent: Path, name: str) -> tuple[Path, int]:
        directory = parent / name
        directory.mkdir(mode=0o700)
        os.chmod(directory, 0o700)
        descriptor, _identity = open_bound_candidate_directory(directory)
        return directory, descriptor

    def fixture_write(
        descriptor: int, filename: str, payload: bytes,
    ) -> None:
        local_durability: Counter[str] = Counter()
        exclusive_candidate_stage_write(
            descriptor, filename, payload, local_durability,
        )

    def fixture_overwrite(
        descriptor: int, filename: str, payload: bytes,
    ) -> None:
        file_descriptor = os.open(
            filename,
            os.O_WRONLY | os.O_TRUNC | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=descriptor,
        )
        try:
            view = memoryview(payload)
            offset = 0
            while offset < len(view):
                written = os.write(file_descriptor, view[offset:])
                need(written > 0, "CANDIDATE_PUBLISHER_SELFTEST_ZERO_WRITE")
                offset += written
            os.fsync(file_descriptor)
        finally:
            os.close(file_descriptor)

    with tempfile.TemporaryDirectory(
        prefix=".cm2-r305b-candidate-publisher-selftest-", dir=ROOT,
    ) as temporary:
        sandbox = Path(temporary)
        os.chmod(sandbox, 0o700)

        fresh, fresh_fd = fixture_directory(sandbox, "fresh")
        try:
            fresh_receipt = publish_candidate_prefix_transaction(
                fresh, fresh_fd, artifacts,
            )
            need(
                fresh_receipt["newly_published_file_count"] == 6
                and fresh_receipt["candidate_commit_order"]
                == list(CANDIDATE_COMMIT_ORDER)
                and fresh_receipt["candidate_result_commit_marker"]
                == CANDIDATE_COMMIT_ORDER[-1]
                and fresh_receipt["officially_admitted_anchor_binding_credit"]
                == 0
                and fresh_receipt["officially_admitted_physical_witness_credit"]
                == 0
                and fresh_receipt["officially_admitted_component_edge_credit"]
                == 0
                and fresh_receipt["official_key_merge_credit"] == 0
                and fresh_receipt["D4_transfer_credit"] == 0
                and fresh_receipt["owner_sidecar_credit"] == 0
                and fresh_receipt["formal_DSU_rank_reduction_credit"] == 0
                and fresh_receipt["formal_maximality_credit"] == 0
                and fresh_receipt["formal_fibre_credit"] == 0
                and fresh_receipt["formal_global_disposition_credit"] == 0,
                "CANDIDATE_PUBLISHER_SELFTEST_FRESH_RECEIPT",
            )
            outcomes["fresh_five_ledgers_then_result_commit"] = True
            outcomes["result_is_last_candidate_commit_marker"] = True
            outcomes["all_official_credit_remains_zero"] = True
            outcomes["file_and_directory_fsync_path_exercised"] = (
                fresh_receipt["durability_audit"].get(
                    "staged_candidate_file"
                ) == 6
                and fresh_receipt["durability_audit"].get(
                    "output_directory_after_candidate_rename"
                ) == 6
                and fresh_receipt["durability_audit"].get(
                    "stage_directory_after_candidate_rename"
                ) == 6
            )

            idempotent = publish_candidate_prefix_transaction(
                fresh, fresh_fd, artifacts,
            )
            need(
                idempotent["exact_existing_idempotent"] is True
                and idempotent["newly_published_file_count"] == 0,
                "CANDIDATE_PUBLISHER_SELFTEST_IDEMPOTENT",
            )
            outcomes["exact_complete_set_is_idempotent"] = True
        finally:
            os.close(fresh_fd)

        partial, partial_fd = fixture_directory(sandbox, "partial-prefix")
        try:
            for filename in CANDIDATE_COMMIT_ORDER[:2]:
                fixture_write(partial_fd, filename, artifacts[filename])
            resumed = publish_candidate_prefix_transaction(
                partial, partial_fd, artifacts,
            )
            need(
                resumed["preexisting_exact_prefix_file_count"] == 2
                and resumed["newly_published_file_count"] == 4,
                "CANDIDATE_PUBLISHER_SELFTEST_PREFIX_RESUME",
            )
            outcomes["exact_partial_prefix_resumes_without_replace"] = True
        finally:
            os.close(partial_fd)

        before_marker, before_marker_fd = fixture_directory(
            sandbox, "mutate-before-result",
        )
        try:
            first = CANDIDATE_COMMIT_ORDER[0]
            marker = CANDIDATE_COMMIT_ORDER[-1]
            corrupted = bytes([artifacts[first][0] ^ 1]) + artifacts[first][1:]
            hook_fired = False

            def before_marker_hook(event: str, name: str, descriptor: int) -> None:
                nonlocal hook_fired
                if event == "before-rename" and name == marker:
                    fixture_overwrite(descriptor, first, corrupted)
                    hook_fired = True

            try:
                publish_candidate_prefix_transaction(
                    before_marker,
                    before_marker_fd,
                    artifacts,
                    hostile_hook=before_marker_hook,
                )
            except PromotionBlocked:
                pass
            else:
                raise PromotionBlocked(
                    "CANDIDATE_PUBLISHER_SELFTEST_PREMARKER_MUTATION_ACCEPTED"
                )
            need(
                hook_fired
                and not (before_marker / marker).exists()
                and (before_marker / first).read_bytes() == corrupted,
                "CANDIDATE_PUBLISHER_SELFTEST_PREMARKER_FAIL_CLOSED",
            )
            outcomes["committed_prefix_rechecked_before_result_marker"] = True
        finally:
            os.close(before_marker_fd)

        after_marker, after_marker_fd = fixture_directory(
            sandbox, "mutate-after-result",
        )
        try:
            first = CANDIDATE_COMMIT_ORDER[0]
            marker = CANDIDATE_COMMIT_ORDER[-1]
            corrupted = bytes([artifacts[first][0] ^ 1]) + artifacts[first][1:]
            hook_fired = False

            def after_marker_hook(event: str, name: str, descriptor: int) -> None:
                nonlocal hook_fired
                if event == "after-rename" and name == marker:
                    fixture_overwrite(descriptor, first, corrupted)
                    hook_fired = True

            try:
                publish_candidate_prefix_transaction(
                    after_marker,
                    after_marker_fd,
                    artifacts,
                    hostile_hook=after_marker_hook,
                )
            except PromotionBlocked:
                pass
            else:
                raise PromotionBlocked(
                    "CANDIDATE_PUBLISHER_SELFTEST_POSTMARKER_MUTATION_ACCEPTED"
                )
            need(
                hook_fired
                and not (after_marker / marker).exists()
                and (after_marker / first).read_bytes() == corrupted,
                "CANDIDATE_PUBLISHER_SELFTEST_POSTMARKER_ROLLBACK",
            )
            outcomes["post_result_drift_rolls_back_this_call_marker"] = True
        finally:
            os.close(after_marker_fd)

        conflict, conflict_fd = fixture_directory(sandbox, "conflict")
        try:
            first = CANDIDATE_COMMIT_ORDER[0]
            fixture_write(conflict_fd, first, b"CONFLICT")
            try:
                publish_candidate_prefix_transaction(
                    conflict, conflict_fd, artifacts,
                )
            except PromotionBlocked:
                outcomes["conflicting_preexisting_target_rejected"] = True
            else:
                raise PromotionBlocked(
                    "CANDIDATE_PUBLISHER_SELFTEST_CONFLICT_ACCEPTED"
                )
            need(
                (conflict / first).read_bytes() == b"CONFLICT",
                "CANDIDATE_PUBLISHER_SELFTEST_CONFLICT_OVERWROTE",
            )
        finally:
            os.close(conflict_fd)

        orphan_conflict, orphan_conflict_fd = fixture_directory(
            sandbox, "orphan-plus-conflict",
        )
        try:
            first = CANDIDATE_COMMIT_ORDER[0]
            orphan_name = CANDIDATE_STAGE_PREFIX + ("2" * 32)
            os.mkdir(orphan_name, mode=0o700, dir_fd=orphan_conflict_fd)
            orphan_stage_fd = os.open(
                orphan_name,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=orphan_conflict_fd,
            )
            try:
                fixture_write(orphan_stage_fd, first, artifacts[first])
            finally:
                os.close(orphan_stage_fd)
            fixture_write(orphan_conflict_fd, first, b"CONFLICT")
            try:
                publish_candidate_prefix_transaction(
                    orphan_conflict, orphan_conflict_fd, artifacts,
                )
            except PromotionBlocked:
                pass
            else:
                raise PromotionBlocked(
                    "CANDIDATE_PUBLISHER_SELFTEST_ORPHAN_CONFLICT_ACCEPTED"
                )
            need(
                (orphan_conflict / orphan_name / first).read_bytes()
                == artifacts[first],
                "CANDIDATE_PUBLISHER_SELFTEST_ORPHAN_MUTATED_BEFORE_PREFLIGHT",
            )
            outcomes["conflict_preflight_precedes_orphan_recovery"] = True
        finally:
            os.close(orphan_conflict_fd)

        nonprefix, nonprefix_fd = fixture_directory(sandbox, "nonprefix")
        try:
            marker = CANDIDATE_COMMIT_ORDER[-1]
            fixture_write(nonprefix_fd, marker, artifacts[marker])
            try:
                publish_candidate_prefix_transaction(
                    nonprefix, nonprefix_fd, artifacts,
                )
            except PromotionBlocked:
                outcomes["result_without_five_ledgers_rejected"] = True
            else:
                raise PromotionBlocked(
                    "CANDIDATE_PUBLISHER_SELFTEST_NONPREFIX_ACCEPTED"
                )
        finally:
            os.close(nonprefix_fd)

        symlinked, symlinked_fd = fixture_directory(sandbox, "symlink-target")
        try:
            fixture_write(symlinked_fd, "sentinel.bin", b"SENTINEL")
            first = CANDIDATE_COMMIT_ORDER[0]
            os.symlink("sentinel.bin", first, dir_fd=symlinked_fd)
            try:
                publish_candidate_prefix_transaction(
                    symlinked, symlinked_fd, artifacts,
                )
            except PromotionBlocked:
                outcomes["symlink_target_rejected"] = True
            else:
                raise PromotionBlocked(
                    "CANDIDATE_PUBLISHER_SELFTEST_SYMLINK_ACCEPTED"
                )
            need(
                (symlinked / "sentinel.bin").read_bytes() == b"SENTINEL",
                "CANDIDATE_PUBLISHER_SELFTEST_SYMLINK_OVERWROTE",
            )
        finally:
            os.close(symlinked_fd)

        orphan, orphan_fd = fixture_directory(sandbox, "exact-orphan")
        try:
            orphan_name = CANDIDATE_STAGE_PREFIX + ("0" * 32)
            os.mkdir(orphan_name, mode=0o700, dir_fd=orphan_fd)
            orphan_stage_fd = os.open(
                orphan_name,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=orphan_fd,
            )
            try:
                fixture_write(
                    orphan_stage_fd,
                    CANDIDATE_COMMIT_ORDER[0],
                    artifacts[CANDIDATE_COMMIT_ORDER[0]],
                )
            finally:
                os.close(orphan_stage_fd)
            recovered = publish_candidate_prefix_transaction(
                orphan, orphan_fd, artifacts,
            )
            need(
                recovered["recovered_exact_orphan_stage_count"] == 1,
                "CANDIDATE_PUBLISHER_SELFTEST_ORPHAN_NOT_RECOVERED",
            )
            outcomes["exact_owned_orphan_stage_recovered"] = True
        finally:
            os.close(orphan_fd)

        bad_orphan, bad_orphan_fd = fixture_directory(
            sandbox, "mismatched-orphan",
        )
        try:
            bad_name = CANDIDATE_STAGE_PREFIX + ("1" * 32)
            os.mkdir(bad_name, mode=0o700, dir_fd=bad_orphan_fd)
            bad_stage_fd = os.open(
                bad_name,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=bad_orphan_fd,
            )
            try:
                fixture_write(
                    bad_stage_fd, CANDIDATE_COMMIT_ORDER[0], b"WRONG",
                )
            finally:
                os.close(bad_stage_fd)
            try:
                publish_candidate_prefix_transaction(
                    bad_orphan, bad_orphan_fd, artifacts,
                )
            except PromotionBlocked:
                outcomes["mismatched_orphan_stage_blocks_fail_closed"] = True
            else:
                raise PromotionBlocked(
                    "CANDIDATE_PUBLISHER_SELFTEST_BAD_ORPHAN_ACCEPTED"
                )
            need(
                (bad_orphan / bad_name / CANDIDATE_COMMIT_ORDER[0]).read_bytes()
                == b"WRONG",
                "CANDIDATE_PUBLISHER_SELFTEST_BAD_ORPHAN_MUTATED",
            )
        finally:
            os.close(bad_orphan_fd)

        foreign_stage, foreign_stage_fd = fixture_directory(
            sandbox, "foreign-stage-name",
        )
        try:
            foreign_name = CANDIDATE_STAGE_PREFIX + "not-a-transaction-id"
            os.mkdir(foreign_name, mode=0o700, dir_fd=foreign_stage_fd)
            try:
                publish_candidate_prefix_transaction(
                    foreign_stage, foreign_stage_fd, artifacts,
                )
            except PromotionBlocked:
                pass
            else:
                raise PromotionBlocked(
                    "CANDIDATE_PUBLISHER_SELFTEST_FOREIGN_STAGE_ACCEPTED"
                )
            need(
                (foreign_stage / foreign_name).is_dir(),
                "CANDIDATE_PUBLISHER_SELFTEST_FOREIGN_STAGE_REMOVED",
            )
            outcomes["foreign_stage_name_preserved_and_rejected"] = True
        finally:
            os.close(foreign_stage_fd)

        rename_case, rename_fd = fixture_directory(sandbox, "rename-race")
        try:
            os.mkdir("source", mode=0o700, dir_fd=rename_fd)
            source_fd = os.open(
                "source",
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=rename_fd,
            )
            try:
                fixture_write(source_fd, "target.bin", b"NEW")
                fixture_write(rename_fd, "target.bin", b"OLD")
                try:
                    candidate_rename_noreplace(
                        source_fd, "target.bin", rename_fd, "target.bin",
                    )
                except FileExistsError:
                    outcomes["renameat2_noreplace_race_rejected"] = True
                else:
                    raise PromotionBlocked(
                        "CANDIDATE_PUBLISHER_SELFTEST_RENAME_REPLACED"
                    )
                need(
                    (rename_case / "target.bin").read_bytes() == b"OLD"
                    and (rename_case / "source" / "target.bin").read_bytes()
                    == b"NEW",
                    "CANDIDATE_PUBLISHER_SELFTEST_RENAME_CONTENT_DRIFT",
                )
            finally:
                os.close(source_fd)
        finally:
            os.close(rename_fd)

        real_parent = sandbox / "real-parent"
        real_parent.mkdir(mode=0o700)
        parent_link = sandbox / "parent-link"
        parent_link.symlink_to(real_parent.name, target_is_directory=True)
        try:
            escaped = open_bound_candidate_directory(parent_link)
        except (PromotionBlocked, OSError):
            outcomes["symlink_parent_chain_rejected"] = True
        else:
            os.close(escaped[0])
            raise PromotionBlocked(
                "CANDIDATE_PUBLISHER_SELFTEST_PARENT_SYMLINK_ACCEPTED"
            )

    need(
        not Path(temporary).exists(),
        "CANDIDATE_PUBLISHER_SELFTEST_TEMPORARY_TREE_NOT_REMOVED",
    )
    need(
        len(outcomes) == 17 and all(outcomes.values()),
        "CANDIDATE_PUBLISHER_SELFTEST_OUTCOME_CLOSURE",
    )
    return {
        "status": (
            "PASS_ROUND305B_ZERO_CREDIT_CANDIDATE_PREFIX_PUBLISHER_"
            "HOSTILE_SELFTEST__NO_FORMAL_OUTPUT__ZERO_CREDIT"
        ),
        "hostile_fixture_results": dict(sorted(outcomes.items())),
        "candidate_artifact_written_to_formal_deliverables": False,
        "independent_verification_performed": False,
        "officially_admitted_anchor_binding_credit": 0,
        "officially_admitted_physical_witness_credit": 0,
        "officially_admitted_component_edge_credit": 0,
        "official_key_merge_credit": 0,
        "D4_transfer_credit": 0,
        "owner_sidecar_credit": 0,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
    }


def project_official_keys(
    residual: list[dict[str, Any]], endpoints: set[str],
) -> dict[str, Any]:
    selected: dict[str, tuple[str, str]] = {}
    official_keys: set[str] = set()
    count = 0
    path = D / R304_MEMBER_LEDGER
    require_regular(path, R304_MEMBER_LEDGER)
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        for row in iter_json_array(stream, '"fresh_member_component_rows":['):
            count += 1
            occurrence = row.get("registry_occurrence_id")
            key = row.get("official_key_id")
            component = row.get("final_component_id")
            need(type(key) is str, "ROUND304_OFFICIAL_KEY")
            official_keys.add(key)
            if occurrence in endpoints:
                need(occurrence not in selected, "ROUND304_ENDPOINT_DUPLICATE")
                selected[occurrence] = (key, component)
    need(
        count == EXPECTED_R304_MEMBERS
        and len(official_keys) == EXPECTED_OFFICIAL_KEYS
        and set(selected) == endpoints,
        "ROUND304_COMPLETE_124_KEY_PROJECTION",
    )

    profiles: dict[tuple[str, str], Counter[tuple[str, str]]] = defaultdict(Counter)
    used_keys: set[str] = set()
    for row in residual:
        left, right = row["canonical_Round294_registry_occurrence_pair"]
        left_key, left_component = selected[left]
        right_key, right_component = selected[right]
        need(left_key != right_key, "RESIDUAL_PAIR_NOT_CROSS_OFFICIAL_KEY")
        need(
            sorted((left_component, right_component))
            == row["final_component_pair"],
            "ROUND304_COMPONENT_REPROJECTION",
        )
        used_keys.update((left_key, right_key))
        profiles[tuple(row["final_component_pair"])][
            tuple(sorted((left_key, right_key)))
        ] += 1
    need(
        len(used_keys) == EXPECTED_RESIDUAL_OFFICIAL_KEYS
        and len(profiles) == EXPECTED_CANONICAL_COMPONENT_EDGES,
        "RESIDUAL_16_KEY_8_EDGE_PROFILE",
    )
    for profile in profiles.values():
        need(
            len(profile) == 1
            and next(iter(profile.values()))
            == EXPECTED_WITNESSES_PER_COMPONENT_EDGE,
            "ONE_CROSS_KEY_PROFILE_PER_COMPONENT_EDGE",
        )
    return {
        "complete_Round304_member_count": count,
        "complete_Round304_official_key_count": len(official_keys),
        "residual_endpoint_count": len(selected),
        "residual_official_key_count": len(used_keys),
        "cross_official_key_pair_count": len(residual),
        "same_official_key_pair_count": 0,
        "canonical_component_edge_count": len(profiles),
        "official_key_profiles_per_component_edge": 1,
    }


def scope_preflight() -> dict[str, Any]:
    need(
        digest(SCHEMA_SNAPSHOT) == FROZEN_SCHEMA_SNAPSHOT_SHA256,
        "ROUND305B_SCHEMA_SNAPSHOT_DRIFT",
    )
    wire_files = admit_normative_wire_files()
    manifests = admit_sealed_inputs()
    residual, endpoints = read_r305a_scope()
    official = project_official_keys(residual, endpoints)
    need(D4_TRANSFER_ENABLED is False, "D4_UNSEALED_TRANSFER_ENABLED")
    need(D4_TRANSFER_CERTIFICATE_MANIFEST_SHA256 is None,
         "D4_UNCONSUMED_CERTIFICATE_SLOT_MUST_BE_NULL")
    return {
        "status": "PASS_SEALED_SCOPE_PREFLIGHT__ZERO_ROUND305B_CREDIT",
        "manifest_member_counts": {
            key: len(value) for key, value in manifests.items()
        },
        "physical_witness_obligation_count": len(residual),
        "anchor_obligation_count": len(endpoints),
        "closure_contact_obligation_count": EXPECTED_CLOSURE_CONTACTS,
        "owner_locus_obligation_count": EXPECTED_OWNER_LOCI,
        "canonical_component_edge_obligation_count":
            EXPECTED_CANONICAL_COMPONENT_EDGES,
        "maximum_later_fresh_DSU_rank_reductions":
            MAXIMUM_LATER_DSU_RANK_REDUCTIONS,
        "formal_DSU_rank_reduction_credit_in_Round305B": 0,
        "official_key_audit": official,
        "normative_wire_files": wire_files,
        "D4_transfer_enabled": False,
        "formal_geometry_kernel_implemented":
            FORMAL_GEOMETRY_KERNEL_IMPLEMENTED,
        "formal_Round305B_credit": 0,
    }


def cacheless_loader_selftest_report() -> dict[str, Any]:
    """Exercise the real six-module loader and the stale-pyc attack fixture."""

    _r174, _r179, _flint, attack = load_interval_runtime()
    need(
        attack["conventional_stale_pyc_attack_effective"] is True
        and attack["cacheless_source_compile_exec_returned_fresh_value"] is True
        and attack["stale_pyc_influenced_formal_runtime"] is False,
        "CACHELESS_LOADER_SELFTEST_REJECTED",
    )
    return {
        "status": (
            "PASS_PRIVATE_CACHELESS_SIX_MODULE_RUNTIME_AND_REAL_STALE_PYC_"
            "ATTACK_SELFTEST__NO_OUTPUT__ZERO_CREDIT"
        ),
        "runtime_closure": cacheless_runtime_closure(),
        "same_mtime_same_size_stale_pyc_attack": attack,
        "formal_Round305B_credit": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-schema-sha256", action="store_true")
    parser.add_argument("--print-wire-spec", action="store_true")
    parser.add_argument("--wire-contract-fixture", action="store_true")
    parser.add_argument("--wire-files-preflight", action="store_true")
    parser.add_argument("--scope-preflight", action="store_true")
    parser.add_argument("--cacheless-loader-selftest", action="store_true")
    parser.add_argument("--private-stage-writer-selftest", action="store_true")
    parser.add_argument("--publisher-hostile-selftest", action="store_true")
    parser.add_argument(
        "--publish-candidate",
        action="store_true",
        help=(
            "explicitly publish the exact zero-credit five-ledger-plus-result "
            "candidate prefix; this is not independent verification or formal "
            "mathematical promotion"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help=(
            "required with --publish-candidate and accepted only when it is "
            "this workspace's exact deliverables directory"
        ),
    )
    parser.add_argument(
        "--no-write",
        action="store_true",
        help=(
            "rebuild the complete five-ledger zero-credit candidate and exact "
            "byte commitments without writing artifacts"
        ),
    )
    parser.add_argument(
        "--bracket-preflight", action="store_true",
        help="run only the direct R292 single-cell/depth-1/2 p-bracket stage",
    )
    parser.add_argument(
        "--private-stage", type=Path,
        help=(
            "write the five candidate ledgers and result to a new, non-"
            "deliverables workspace directory; never emits a manifest"
        ),
    )
    arguments = parser.parse_args()
    modes = (
        arguments.print_schema_sha256,
        arguments.print_wire_spec,
        arguments.wire_contract_fixture,
        arguments.wire_files_preflight,
        arguments.scope_preflight,
        arguments.cacheless_loader_selftest,
        arguments.private_stage_writer_selftest,
        arguments.publisher_hostile_selftest,
        arguments.no_write,
        arguments.bracket_preflight,
        arguments.private_stage is not None,
        arguments.publish_candidate,
    )
    need(sum(bool(mode) for mode in modes) == 1, "EXACTLY_ONE_EXPLICIT_MODE_REQUIRED")
    need(
        (arguments.output_dir is not None) == arguments.publish_candidate,
        "OUTPUT_DIR_REQUIRES_AND_IS_REQUIRED_BY_PUBLISH_CANDIDATE",
    )
    if arguments.print_wire_spec:
        print(canonical(WIRE_SPEC).decode("utf-8"))
        return
    if arguments.wire_contract_fixture:
        print(canonical(wire_contract_fixture()).decode("utf-8"))
        return
    if arguments.wire_files_preflight:
        print(canonical(admit_normative_wire_files()).decode("utf-8"))
        return
    if arguments.print_schema_sha256:
        print("schema_snapshot_sha256=" + digest(SCHEMA_SNAPSHOT))
        return
    if arguments.cacheless_loader_selftest:
        print(canonical(cacheless_loader_selftest_report()).decode("utf-8"))
        return
    if arguments.private_stage_writer_selftest:
        print(canonical(private_stage_writer_selftest_report()).decode("utf-8"))
        return
    if arguments.publisher_hostile_selftest:
        print(
            canonical(candidate_publisher_hostile_selftest_report()).decode(
                "utf-8"
            )
        )
        return
    if arguments.bracket_preflight:
        print(canonical(no_write_geometry_preflight()).decode("utf-8"))
        return
    if arguments.no_write:
        _bundle, _raw, audit = build_full_candidate_bytes()
        print(canonical(audit).decode("utf-8"))
        return
    if arguments.private_stage is not None:
        print(canonical(emit_private_stage(arguments.private_stage)).decode("utf-8"))
        return
    if arguments.scope_preflight:
        print(canonical(scope_preflight()).decode("utf-8"))
        return
    if arguments.publish_candidate:
        need(arguments.output_dir is not None, "PUBLISH_CANDIDATE_OUTPUT_DIR")
        print(
            canonical(
                publish_zero_credit_candidate(arguments.output_dir)
            ).decode("utf-8")
        )
        return
    raise PromotionBlocked("UNREACHABLE_EXPLICIT_MODE_DISPATCH")


if __name__ == "__main__":
    try:
        main()
    except PromotionBlocked as error:
        print("BLOCKED_ROUND305B:" + str(error))
        raise SystemExit(2)
