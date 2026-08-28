#!/usr/bin/env python3
"""Round303-B unified two-sided attachment component-edge producer candidate.

This production candidate consumes no spike evidence or spike result.  Every
mathematical row is reconstructed from pinned formal packages and the
Round303-A package.

Round303-A is consumed only through its frozen ten-member verifier/manifest
seal.  Round303-B edge consumption remains disabled until this producer has
also passed dual-seed replay, an independent verifier and focused attacks,
cold replay, and an exact package manifest.
"""

from __future__ import annotations

import argparse
import ast
import gzip
import hashlib
import heapq
import json
import os
import re
import stat
import sys
import tempfile
import types
from collections import Counter, deque
from collections.abc import Iterable, Iterator
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, TextIO

HERE = Path(__file__).resolve().parent


def locate_workspace(here: Path) -> Path:
    """Locate the workspace both in staging and after delivery."""

    if here.name == "deliverables":
        return here.parent
    for ancestor in here.parents:
        if (ancestor / "deliverables").is_dir():
            return ancestor
    raise RuntimeError("cannot locate workspace deliverables directory")


WORKSPACE = locate_workspace(HERE)
DEFAULT_INPUT_DIR = WORKSPACE / "deliverables"

PREFIX = "cm2_round303b_source_g_unified_attachment_edge_promotion"
OUTPUT_NAMES = {
    "b1": f"{PREFIX}_b1_graph_attachment_lemma_ledger.json.gz",
    "b2a": f"{PREFIX}_b2a_analytic_sheet_lemma_ledger.json.gz",
    "b2b": f"{PREFIX}_b2b_physical_inclusion_lemma_ledger.json.gz",
    "edge": f"{PREFIX}_component_edge_ledger.json.gz",
    "unresolved": f"{PREFIX}_wtail_unresolved_ledger.json.gz",
    "result": f"{PREFIX}_result.json",
}

SCHEMA = "cm2.round303b.source-g-unified-attachment-edge-promotion.v1"
THEOREM_ID = "CM2_TWO_SIDED_INCLUDED_STRATUM_ATTACHMENT_GLUING_V1"
B1_THEOREM_ID = "ROUND303B_B1_MONOTONE_GRAPH_SIDE_ATTACHMENT_LEMMA_V1"
B2A_THEOREM_ID = "ROUND303B_B2A_R204_ANALYTIC_TARGET_SHEET_LEMMA_V1"
B2B_THEOREM_ID = "ROUND303B_B2B_R291_PHYSICAL_SHEET_INCLUSION_LEMMA_V1"
MONOTONE_LIMIT_THEOREM_ID = (
    "CM2_STRICT_T_MONOTONE_FULL_SIGN_SIDES_TWO_CLOSURE_LIMIT_V1"
)
WT_DISPOSITION = (
    "UNRESOLVED__ROUND271_W_TAIL_CONNECTED_SIDE_EXTENSION_MISSING"
)

R288_KIND = "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
PRESERVED_KIND = "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
B2A_FULL_2D_CERTIFICATION = "PINNED_ROUND182_FULL_2D_ENDPOINT_BRACKET"
B2A_FORBIDDEN_TAIL_CERTIFICATION = (
    "ROUND204_TAIL_T_BRACKET_MONOTONICITY_AND_P_OUTER_INTERVAL_NEWTON"
)
R182_TARGET_FACTOR_SHEET_THEOREM_ID = (
    "ROUND182_WALL_LEAF_IS_TARGET_FACTOR_GRAPH"
)
R182_PACKAGE_PREFIX = (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement"
)
R182_PACKAGE_MANIFEST = R182_PACKAGE_PREFIX + "_manifest.sha256"
R182_PACKAGE_MANIFEST_SHA256 = (
    "32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5"
)
R182_PACKAGE_MEMBER_PINS = {
    R182_PACKAGE_PREFIX + ".py":
        "8638f2722e68bd5c6e0eb5932dc76780728998f21a47b1d8c02c28449e984d56",
    R182_PACKAGE_PREFIX + "_certificate.json":
        "27491e3943e88772ec15cee110cd983b14ad82a2a56f8a07d605c3cd8fb49f08",
    R182_PACKAGE_PREFIX + "_rows.json":
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    R182_PACKAGE_PREFIX + "_verifier.py":
        "790b17cf6dadebc37b889fff63c6ecde985cccf53c95523cd6c2bc39d12db566",
    R182_PACKAGE_PREFIX + "_verification.json":
        "b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36",
    R182_PACKAGE_PREFIX + "_report.md":
        "708272e9425bef74f3f4639c76fd17078f509d3acc5d324325c224e743985f0c",
    R182_PACKAGE_PREFIX + "_cold_replay.md":
        "c0fd075a0ba56de5380c6cc89620dc82fa640c0466b118565cf1755aedf61f99",
}
R294B_PACKAGE_PREFIX = (
    "cm2_round294b_source_g_registry_builder_admission_closure"
)
R294B_MANIFEST = R294B_PACKAGE_PREFIX + "_manifest.sha256"
R294B_VERIFICATION = R294B_PACKAGE_PREFIX + "_verification.json"
R294B_MANIFEST_SHA256 = (
    "fc16aa2792a59dff922afcc8ec66b1ca015251af3c5f718d9d909439a2990d76"
)
R294B_VERIFICATION_FILE_SHA256 = (
    "b1440432a082b392de744bc6f4ca20e893122cb923a3236899357ccfb4fd6581"
)
R294B_VERIFICATION_OBJECT_SHA256 = (
    "1746adb7b71607909eae031da879671885deee8602fdb5685dc561ba9afa4179"
)
R294B_PACKAGE_MEMBER_PINS = {
    "cm2_round292_source_g_occurrence_registry_candidate_construction.py":
        "2c0b7e864839880f47cca2989b3f8d48fcec0399c0644c92f8aabab225402004",
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_verifier.py":
        "9efd78054cdde8172b016a684951395f1ca96958412122034dfc1971312ea010",
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_manifest.sha256":
        "4ea92e4112cae18aa0c13a6d2308816bafc19e4129c09d8b6be914268cfc4870",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256":
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    R294B_PACKAGE_PREFIX + ".py":
        "ed8346b550c461cea28a4a01393c4c5d1be802f9e6145537a0ae7fe5c2e13192",
    R294B_PACKAGE_PREFIX + "_result.json":
        "656676d6f5dd4accc7b9aa473a14d9c1326b83eff2fe8974e7b43694adb44ccc",
    R294B_PACKAGE_PREFIX + "_verifier.py":
        "f6aa9278de7a8c478b6c4d8b49bbf8517f54ba1fb2a2b15fda5ce8afae41cc92",
    R294B_VERIFICATION: R294B_VERIFICATION_FILE_SHA256,
    R294B_PACKAGE_PREFIX + "_attack_suite.json":
        "4d4f99615078062b0fbc544ff04245f6bd9055beb3ca8807480e0aff4aacdcff",
    R294B_PACKAGE_PREFIX + "_report.md":
        "358471a38a0c32c411179c373519fc426d3d32cbc56c3526c41392e0ed158ebe",
    R294B_PACKAGE_PREFIX + "_cold_replay.md":
        "502dd01eade98f5cd5e33c716ebd077b03257dc2f42f110919365662ce759944",
}

EXPECTED_R300D = 111_524
EXPECTED_CROSS = 44_108
EXPECTED_B1_SCOPE = 43_916
EXPECTED_B1 = 43_912
EXPECTED_B2 = 192
EXPECTED_WTAIL = 4
EXPECTED_EDGE = 44_104
EXPECTED_SELECTED_ENDPOINTS = 88_216

MAX_BASE_SPLIT_DEPTH = 24
MAX_CORRIDOR_DYADIC_DEPTH = 48
PIN_RE = re.compile(r"^[0-9a-f]{64}$")


GLUING_THEOREM = {
    "theorem_id": THEOREM_ID,
    "version": 1,
    "hypotheses": {
        "G0_exact_provenance_pins_and_row_closures": (
            "Every endpoint, bridge, chart, active equation, physical cell, "
            "included stratum, and source file is exactly pinned and row "
            "closed."
        ),
        "G1_endpoint_occurrence_connected_supports": (
            "Each endpoint has a nonempty occurrence anchor contained in one "
            "formal connected physical source side."
        ),
        "G2_nonempty_connected_included_lower_stratum": (
            "The common lower-dimensional patch Gamma is nonempty, connected, "
            "and included in the physical space."
        ),
        "G3_left_closure_attaches_to_included_patch": (
            "The closure of the left endpoint's connected side meets Gamma."
        ),
        "G4_right_closure_attaches_to_included_patch": (
            "The closure of the right endpoint's connected side meets Gamma."
        ),
        "G5_endpoint_patch_provenance_exactly_closed": (
            "Both occurrence IDs, connected sides, attachments, and Gamma "
            "close through one exact chart/equation/leaf provenance chain."
        ),
    },
    "conclusion": (
        "closure(A_left) union Gamma union closure(A_right) is connected, "
        "hence the two registry occurrences lie in one physical component."
    ),
    "credit_boundary": {
        "formal_component_edge_credit": 1,
        "formal_occurrence_identity_collapse_credit": 0,
        "formal_official_key_merge_credit": 0,
        "formal_component_union_credit": 0,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
        "formal_Jx_Jy_same_point_glue_credit": 0,
    },
}

MONOTONE_LIMIT_THEOREM = {
    "theorem_id": MONOTONE_LIMIT_THEOREM_ID,
    "version": 1,
    "hypotheses": {
        "L0_exact_relative_domain": (
            "D=I_t x U is an exact nondegenerate rational prism, U is a "
            "positive-area connected rational rectangle, and any excluded "
            "relative-open face is named and disjoint from Gamma."
        ),
        "L1_continuous_active_scalar": (
            "F is continuous on D; chart radicands/discriminants are strictly "
            "positive and every divisor is nonzero on the serialized domain."
        ),
        "L2_strict_t_monotonicity": (
            "The t derivative enclosure of F has one strict sign on D."
        ),
        "L3_uniform_opposite_face_signs": (
            "The two t faces of F have opposite uniform strict signs, each "
            "certified either by one direct interval enclosure or by an "
            "independently replayed transverse-monotonicity zero-absence "
            "status."
        ),
        "L4_exact_included_Gamma_binding": (
            "The unique zero graph Gamma is exactly the selected Round291 "
            "WHOLE_PHYSICAL_SUPPORT cell patch and closes through Round295A "
            "and Round300D."
        ),
        "L5_complete_connected_sign_sides": (
            "The two sealed Round303A A objects are included connected "
            "complete sign sides, and {F<0} in D and {F>0} in D are each "
            "symbolically contained in the corresponding A."
        ),
        "L6_endpoint_opposite_sign_bijection": (
            "The two endpoints biject to opposite signs and the "
            "Round294/Round303A/leaf/chart/owner/equation chain closes."
        ),
    },
    "conclusion": (
        "Gamma={F=0} in D is one nonempty continuous graph over U, and "
        "Gamma is contained in closure({F<0} in D) intersect "
        "closure({F>0} in D)."
    ),
    "proof_contract": (
        "Existence is IVT on every base fibre; uniqueness is strict "
        "monotonicity; continuity of the root map follows from continuity, "
        "the uniform strict face bracket, and uniqueness; approaching the "
        "root from either t direction supplies the two closure limits."
    ),
    "forbidden_shortcut": (
        "A strict nonzero corridor is disjoint from Gamma and is never an "
        "intersection or attachment witness."
    ),
}

B1_LAYER_THEOREM = {
    "theorem_id": B1_THEOREM_ID,
    "version": 1,
    "hypotheses": {
        "B1_0_exact_scope_and_sealed_bridges": (
            "The Round300D/Round301 pair and both opposite-sign Round303A "
            "connected-side bridges close through exact pinned rows."
        ),
        "B1_1_exact_monotone_graph": (
            "The pinned R179/R182 active scalar has one strict t derivative "
            "and opposite strict t-face signs on a positive-base prism."
        ),
        "B1_2_included_Gamma_identity": (
            "The unique zero graph is the selected included Round291 "
            "WHOLE_PHYSICAL_SUPPORT cell carried through R293/R295A."
        ),
        "B1_3_two_complete_side_attachments": (
            "The complete local sign sides lie in the two connected "
            "Round303A sides and Gamma lies in both closures."
        ),
    },
    "conclusion": (
        "The two endpoint connected supports attach to the same nonempty "
        "connected included Gamma."
    ),
    "kernel_theorem_id": MONOTONE_LIMIT_THEOREM_ID,
    "credit_boundary": {
        "formal_B1_attachment_lemma_credit": 1,
        "formal_component_edge_credit": 0,
        "all_downstream_credits": 0,
    },
}

B2A_LAYER_THEOREM = {
    "theorem_id": B2A_THEOREM_ID,
    "version": 1,
    "hypotheses": {
        "B2A_0_exact_FULL_2D_route": (
            "The selected R204 sheet is certified only by "
            "PINNED_ROUND182_FULL_2D_ENDPOINT_BRACKET; both incident regions "
            "are strict, positive-volume, non-tail FULL_2D graph cells."
        ),
        "B2A_1_strict_monotone_bracket": (
            "The exact continuous target factor has one strict t derivative "
            "and opposite uniform t-face signs over a connected positive-area "
            "rational base."
        ),
        "B2A_2_opposite_graph_cells": (
            "The two selected endpoint regions are exactly the negative and "
            "positive subgraph cells of the unique root graph."
        ),
    },
    "conclusion": (
        "Gamma is one nonempty connected unique graph; both strict graph "
        "cells are connected and Gamma lies in both analytic closures."
    ),
    "forbidden_route": B2A_FORBIDDEN_TAIL_CERTIFICATION,
    "credit_boundary": {
        "formal_B2a_analytic_lemma_credit": 1,
        "formal_component_edge_credit": 0,
        "physical_inclusion_claimed_at_B2a": False,
        "all_downstream_credits": 0,
    },
}

R182_TARGET_FACTOR_SHEET_THEOREM = {
    "theorem_id": R182_TARGET_FACTOR_SHEET_THEOREM_ID,
    "version": 1,
    "sealed_package": {
        "manifest_filename": R182_PACKAGE_MANIFEST,
        "manifest_sha256": R182_PACKAGE_MANIFEST_SHA256,
        "exact_member_count": 7,
        "exact_member_pins": dict(sorted(R182_PACKAGE_MEMBER_PINS.items())),
    },
    "hypotheses": {
        "T0_exact_sealed_Round182_package": (
            "The exact seven-member Round182 manifest, including producer, "
            "rows, independent verifier, and verification, is content pinned."
        ),
        "T1_WALL_geometry_value_is_target_selector": (
            "For kind WALL and axis X or Y, Round182 geometry_value evaluates "
            "subtract_wall(independent_geometry[hit_x or hit_y], "
            "integer_wall); it does not evaluate the source factor or the "
            "nominal product equation."
        ),
        "T2_FULL_2D_unique_target_graph": (
            "On the exact leaf box the target selector has a strict t "
            "derivative and opposite uniform lower/upper t-face signs.  Each "
            "face sign is certified either directly or by the independently "
            "replayed Round182 transverse-monotonicity zero-absence status, "
            "so the serialized FULL_2D leaf with sheet count one is the "
            "unique target factor graph over its positive-area base."
        ),
        "T3_exact_concrete_leaf_selector": (
            "Leaf id, collar id, retained child, chart, owner target, axis, "
            "integer wall, exact box, and exact base area all agree."
        ),
    },
    "conclusion": (
        "The selected Round182 WALL FULL_2D leaf carries exactly the unique "
        "target-factor graph target_axis-integer_wall=0 over that base."
    ),
    "nonclaims": {
        "nominal_product_equation_is_sheet_identity": False,
        "product_zero_iff_target_zero_on_closed_leaf": False,
        "closed_leaf_source_factor_strict_nonzero_required": False,
    },
}

B2B_LAYER_THEOREM = {
    "theorem_id": B2B_THEOREM_ID,
    "version": 1,
    "target_factor_sheet_theorem_id": R182_TARGET_FACTOR_SHEET_THEOREM_ID,
    "target_factor_sheet_theorem_sha256": None,
    "hypotheses": {
        "B2B_0_exact_physical_chain": (
            "One exact Round300D -> Round295A -> Round293 -> Round291 "
            "row-and-cell chain binds the same endpoint pair."
        ),
        "B2B_1_Round182_target_factor_sheet": (
            "The content-pinned ROUND182_WALL_LEAF_IS_TARGET_FACTOR_GRAPH "
            "theorem identifies the selected FULL_2D leaf as the unique target "
            "factor graph, independently of the nominal product equation."
        ),
        "B2B_2_R204_Gamma_is_R291_DIRECT_target_sheet": (
            "The R204 Gamma and the Round291 DIRECT_GRAPH_SHEET_WITNESS select "
            "that same concrete target sheet by identical leaf, collar, chart, "
            "owner, axis, wall, exact box, positive base, and target selector."
        ),
        "B2B_3_product_equation_is_nominal_lineage_only": (
            "The Round179/R291 product equation is checked only as nominal "
            "lineage compatibility; no product identity, product iff, or "
            "closed-leaf source-factor strictness is used as a logical bridge."
        ),
    },
    "conclusion": (
        "The B2a/R204 Gamma equals the target-factor graph sheet carried by the "
        "selected Round291 DIRECT witness and is therefore included in its "
        "WHOLE_PHYSICAL_SUPPORT ambient support."
    ),
    "credit_boundary": {
        "formal_B2b_physical_inclusion_lemma_credit": 1,
        "formal_component_edge_credit": 0,
        "all_downstream_credits": 0,
    },
}

ZERO_FIELDS = (
    "formal_occurrence_identity_collapse_credit",
    "formal_official_key_merge_credit",
    "formal_component_union_credit",
    "formal_component_quotient_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_seam_edge_credit",
    "formal_Jx_Jy_same_point_glue_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)


# Base inputs are sealed.  The first four Round303-A pins below identify the
# raw candidate package only; formal consumption additionally requires the
# exact ten-member seal manifest closure declared below.
BASE_INPUT_PINS = {
    "cm2_round179_source_g_residual_tube_arrangement.py":
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round179_source_g_residual_tube_arrangement_manifest.sha256":
        "8fd5ae3a0cdd0c3321c0f8ffe6183ab57d31088b96523fa41ce0ebbe10d78b76",
    **R182_PACKAGE_MEMBER_PINS,
    R182_PACKAGE_MANIFEST: R182_PACKAGE_MANIFEST_SHA256,
    **R294B_PACKAGE_MEMBER_PINS,
    R294B_MANIFEST: R294B_MANIFEST_SHA256,
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json":
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "cm2_round204_source_g_wall_return_signature_local_replacement_manifest.sha256":
        "ae3310f8ae0a4c565a39153e268c09fcb983aa04cccce6e3d7dd72fb7803c213",
    "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_ledger.json.gz":
        "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab",
    "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_manifest.sha256":
        "d655907a45cfb7b47ebdc822d35a0e604fc27fa38547c300139c116d7a2191ce",
    "cm2_round293_source_g_r289_r291_witness_binding_canonical_closure_ledger.json.gz":
        "0e7395a69844734cc51563882f471987cc566db28a55ccae6e6d15d045f9e53c",
    "cm2_round293_source_g_r289_r291_witness_binding_canonical_closure_manifest.sha256":
        "14fef7e62be76cefaa2c331d7c6f72e50f732c7b5df17596759afe1a49406987",
    "cm2_round293b_source_g_r293_dual_producer_seed_replay_manifest.sha256":
        "4bca00a379bb2abb0e5d1dd2b2de7f750e77df32ad37d1c1bc2feab33f2354dd",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz":
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256":
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_physical_witness_incidence_binding_ledger.json.gz":
        "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_manifest.sha256":
        "b25f11c0090c56d2ad2d3b2cd0b172e7c089f044ae5722eb9e82ae04b129094a",
    "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_ledger.json.gz":
        "287d1382b25fd3d5cd0a52c6da8cabbb012040b8a6e35c9f887d7a425b812fa7",
    "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_manifest.sha256":
        "8dd3907a363ae0c4fe7d524061a02b4c70944ce870ded941d5d617911ea1124e",
    "cm2_round301_source_g_legal_component_dsu_application_member_component_ledger.json.gz":
        "88adb1ac6c9ee447fddb2ccd8e657a238827e9b31712d974a2a9abd2a3591b93",
    "cm2_round301_source_g_legal_component_dsu_application_ineligible_source_consumption_ledger.json.gz":
        "5fbc5a409eccd4e04954c7b63dab6739897efd8d9e327c47045cbfbbbaf7633e",
    "cm2_round301_source_g_legal_component_dsu_application_manifest.sha256":
        "5789b23e74b6e0db9a1b4e311fb22ebe5e3612e4972d2fc3547957230fda214c",
}

PROVISIONAL_R303A_PINS = {
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge.py":
        "b85d6a8f33e81feb613b2cdb04de648376a10c94635b23119bd7f70439ba461a",
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_bridge_ledger.json.gz":
        "efe0e4b71804848611f3702063698ee77bbdf9dc779bc473fba989fb5db7e465",
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_unresolved_bridge_ledger.json.gz":
        "a029eae97e1f35b87f9699adb0446f1b1329a55c5b4ee0887b03bd1f4a9db0b8",
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_result.json":
        "796b2167e2263108e3e2c373650e1d488152f7558bbc03fffe977d38e0e81d19",
}

R303A_MANIFEST = (
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_"
    "manifest.sha256"
)

# R303A FROZEN TEN-MEMBER SEAL PINS
#
# The member set is deliberately exact: adding, omitting, renaming, or
# changing any member keeps formal R303B writes disabled.
R303A_SEAL_MANIFEST_PIN: str | None = (
    "6f195f8325f107328f7e375411bb8a95146b0cfd65180f5cc9f85b3643d0b098"
)
R303A_MANIFEST_MEMBER_PINS: dict[str, str | None] = {
    **PROVISIONAL_R303A_PINS,
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_verifier.py":
        "f8ffa2080b6ccc51c48ce7a37dc6c80ae0a94187f19a744b3f46a03a144f45e3",
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_attack_suite.json":
        "ce29c15b9d685d9e863ab4534adc50302995131283f4dc03e68d34a18a678bf2",
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_verification.json":
        "ada33e5f1a780f92b228861f0e3606ff2c383665d056f1c83b38c0fda56a4549",
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_report.md":
        "190ed08b89be1fd8f719562b22898e860fbb3031d231ded0788bf68154c834fe",
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_cold_replay.md":
        "40fd98df494a4aba2c4c2697bf1c99e30b304cb62f295349ce0d12f8d93b2e9d",
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_attestation.json":
        "d46f8074761cdb5f4b9706d033665c2fc260be5a363cd96095ed350a2b125c10",
}

MANIFEST_MEMBERS = {
    "cm2_round179_source_g_residual_tube_arrangement_manifest.sha256": [
        "cm2_round179_source_g_residual_tube_arrangement.py",
        "cm2_round179_source_g_residual_tube_arrangement_rows.json",
    ],
    R182_PACKAGE_MANIFEST: list(R182_PACKAGE_MEMBER_PINS),
    R294B_MANIFEST: list(R294B_PACKAGE_MEMBER_PINS),
    "cm2_round204_source_g_wall_return_signature_local_replacement_manifest.sha256": [
        "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json",
    ],
    "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_manifest.sha256": [
        "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_ledger.json.gz",
    ],
    "cm2_round293_source_g_r289_r291_witness_binding_canonical_closure_manifest.sha256": [
        "cm2_round293_source_g_r289_r291_witness_binding_canonical_closure_ledger.json.gz",
    ],
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256": [
        "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz",
    ],
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_manifest.sha256": [
        "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_physical_witness_incidence_binding_ledger.json.gz",
    ],
    "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_manifest.sha256": [
        "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_ledger.json.gz",
    ],
    "cm2_round301_source_g_legal_component_dsu_application_manifest.sha256": [
        "cm2_round301_source_g_legal_component_dsu_application_member_component_ledger.json.gz",
        "cm2_round301_source_g_legal_component_dsu_application_ineligible_source_consumption_ledger.json.gz",
    ],
}


class PromotionError(RuntimeError):
    """Any missing proof predicate aborts before an atomic commit."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise PromotionError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=True,
    allow_nan=False,
)


def pieces(value: Any) -> Iterable[bytes]:
    for part in ENCODER.iterencode(value):
        yield part.encode("ascii")


def canonical(value: Any) -> bytes:
    return b"".join(pieces(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for part in pieces(value):
        state.update(part)
    return state.hexdigest()


THEOREM_SHA256 = digest(GLUING_THEOREM)
MONOTONE_LIMIT_THEOREM_SHA256 = digest(MONOTONE_LIMIT_THEOREM)
B1_LAYER_THEOREM_SHA256 = digest(B1_LAYER_THEOREM)
B2A_LAYER_THEOREM_SHA256 = digest(B2A_LAYER_THEOREM)
R182_TARGET_FACTOR_SHEET_THEOREM_SHA256 = digest(
    R182_TARGET_FACTOR_SHEET_THEOREM
)
B2B_LAYER_THEOREM["target_factor_sheet_theorem_sha256"] = (
    R182_TARGET_FACTOR_SHEET_THEOREM_SHA256
)
B2B_LAYER_THEOREM_SHA256 = digest(B2B_LAYER_THEOREM)


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in output, "duplicate JSON key:" + key)
        output[key] = value
    return output


def reject_number(token: str) -> Any:
    raise PromotionError("noninteger JSON number:" + token)


def decoder() -> json.JSONDecoder:
    return json.JSONDecoder(
        object_pairs_hook=strict_object,
        parse_float=reject_number,
        parse_constant=reject_number,
    )


def read_json(path: Path) -> dict[str, Any]:
    raw = path.read_text("utf-8")
    value, end = decoder().raw_decode(raw)
    need(not raw[end:].strip() and type(value) is dict, "strict JSON:" + path.name)
    return value


def verify_row(row: dict[str, Any], label: str) -> None:
    claimed = row.get("row_sha256")
    payload = dict(row)
    payload.pop("row_sha256", None)
    need(
        type(claimed) is str
        and PIN_RE.fullmatch(claimed) is not None
        and digest(payload) == claimed,
        "row closure:" + label,
    )


def close_row(
    id_field: str,
    prefix: str,
    context: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    row = dict(payload)
    row[id_field] = prefix + digest([context, payload])
    row["row_sha256"] = digest(row)
    return row


def require_diagnostic_zero_credit(row: dict[str, Any], label: str) -> None:
    for field, value in row.items():
        if field.startswith("formal_"):
            need(value == 0, "diagnostic formal credit:" + label + ":" + field)
    if "eligible_for_later_fresh_DSU_application" in row:
        need(
            row["eligible_for_later_fresh_DSU_application"] is False,
            "diagnostic DSU eligibility:" + label,
        )
    for field in ("nonedge_credit", "exclusion_credit"):
        if field in row:
            need(row[field] == 0, "diagnostic credit:" + label + ":" + field)


def open_text(path: Path) -> TextIO:
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="ascii", newline="")
    return path.open("rt", encoding="ascii", newline="")


def iter_array(
    path: Path,
    marker: str,
    *,
    after_marker: str | None = None,
) -> Iterator[Any]:
    """Strictly stream one uniquely named JSON array without loading its file."""

    with open_text(path) as stream:
        buffer = ""
        if after_marker is not None:
            while after_marker not in buffer:
                part = stream.read(1 << 20)
                need(bool(part), "array anchor:" + path.name + ":" + after_marker)
                buffer += part
                if len(buffer) > len(after_marker) + (1 << 21):
                    buffer = buffer[-(len(after_marker) + (1 << 21)):]
            buffer = buffer.split(after_marker, 1)[1]
        while marker not in buffer:
            part = stream.read(1 << 20)
            need(bool(part), "array marker:" + path.name + ":" + marker)
            buffer += part
            if len(buffer) > len(marker) + (1 << 21):
                buffer = buffer[-(len(marker) + (1 << 21)):]
        buffer = buffer.split(marker, 1)[1]
        dec = decoder()
        while True:
            buffer = buffer.lstrip()
            if not buffer:
                part = stream.read(1 << 20)
                need(bool(part), "array EOF:" + path.name)
                buffer = part
                continue
            if buffer[0] == ",":
                buffer = buffer[1:]
                continue
            if buffer[0] == "]":
                return
            while True:
                try:
                    value, end = dec.raw_decode(buffer)
                    break
                except json.JSONDecodeError:
                    part = stream.read(1 << 20)
                    need(bool(part), "truncated array row:" + path.name)
                    buffer += part
            yield value
            buffer = buffer[end:]


def iter_nested_rows(path: Path, ledger_name: str) -> Iterator[dict[str, Any]]:
    token = json.dumps(ledger_name, separators=(",", ":")) + ":{"
    with open_text(path) as stream:
        buffer = ""
        while token not in buffer:
            part = stream.read(1 << 20)
            need(bool(part), "nested ledger token:" + ledger_name)
            buffer += part
            if len(buffer) > len(token) + (1 << 21):
                buffer = buffer[-(len(token) + (1 << 21)):]
        buffer = buffer.split(token, 1)[1]
        marker = '"rows":['
        while marker not in buffer:
            part = stream.read(1 << 20)
            need(bool(part), "nested rows token:" + ledger_name)
            buffer += part
        buffer = buffer.split(marker, 1)[1]
        dec = decoder()
        while True:
            buffer = buffer.lstrip()
            if not buffer:
                part = stream.read(1 << 20)
                need(bool(part), "nested array EOF:" + ledger_name)
                buffer = part
                continue
            if buffer[0] == ",":
                buffer = buffer[1:]
                continue
            if buffer[0] == "]":
                return
            while True:
                try:
                    value, end = dec.raw_decode(buffer)
                    break
                except json.JSONDecodeError:
                    part = stream.read(1 << 20)
                    need(bool(part), "nested row truncation:" + ledger_name)
                    buffer += part
            need(type(value) is dict, "nested row object:" + ledger_name)
            yield value
            buffer = buffer[end:]


def parse_manifest(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text("utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = line.split()
        need(len(parts) >= 2 and PIN_RE.fullmatch(parts[0]) is not None,
             "manifest syntax:" + path.name)
        name = parts[-1].removeprefix("*").removeprefix("./")
        need(name not in values, "manifest duplicate:" + name)
        values[name] = parts[0]
    return values


def is_pin(value: object) -> bool:
    return type(value) is str and PIN_RE.fullmatch(value) is not None


def r303a_seal_complete() -> bool:
    return (
        is_pin(R303A_SEAL_MANIFEST_PIN)
        and len(R303A_MANIFEST_MEMBER_PINS) == 10
        and all(is_pin(value) for value in R303A_MANIFEST_MEMBER_PINS.values())
    )


def validate_regular_pinned_file(
    path: Path,
    expected: str,
    label: str,
) -> None:
    need(path.exists() and not path.is_symlink(), label)
    info = path.stat()
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and info.st_size > 0,
        label + ":regular-single-link",
    )
    need(file_sha256(path) == expected, label + ":sha256")


def validate_r294b_admission(input_dir: Path) -> None:
    """Require the sealed builder-admission closure before using Round294."""

    manifest = parse_manifest(input_dir / R294B_MANIFEST)
    need(
        set(manifest) == set(R294B_PACKAGE_MEMBER_PINS)
        and len(manifest) == 11,
        "Round294B exact eleven-member manifest",
    )
    for name, expected in R294B_PACKAGE_MEMBER_PINS.items():
        need(
            manifest.get(name) == expected,
            "Round294B manifest member:" + name,
        )

    verification = read_json(input_dir / R294B_VERIFICATION)
    claimed = verification.get("verification_sha256")
    payload = dict(verification)
    payload.pop("verification_sha256", None)
    census = verification["independent_registry_census"]
    direct = verification["direct_actual_file_audit"]
    independence = verification["independence_contract"]
    manifest_audit = verification["manifest_exact_set_audit"]
    nonpromotion = verification["strict_nonpromotion"]
    credits = verification["formal_credit_transition"]
    need(
        claimed == R294B_VERIFICATION_OBJECT_SHA256
        and digest(payload) == claimed
        and verification["status"] == (
            "PASS_INDEPENDENT_ROUND294B_ZERO_CREDIT_ADMISSION__"
            "ACTUAL_R292A_VERIFIER_DIRECT_PIN__7_PLUS_9_EXACT_MANIFESTS__"
            "431208_REGISTRY_ROWS__46288_BINDINGS__"
            "38_OF_38_ATTACKS_REJECTED"
        )
        and verification["attack_audit"]["attack_count"] == 38
        and verification["attack_audit"]["rejected_attack_count"] == 38
        and verification["attack_audit"]["accepted_attack_count"] == 0
        and verification["attack_audit"]["all_attacks_rejected"] is True
        and census["formal_occurrence_registry_row_count"] == 431_208
        and census["formal_representation_binding_count"] == 46_288
        and census["binding_rows_issuing_occurrence_ID_count"] == 0
        and census["direct_Round287_union_issuance_count_rejected"] == 10_020
        and census["legacy_63224_as_current_quotient_rejected"] is True
        and census["superseded_registry_row_count_rejected"] == 431_824
        and direct["Round294_manifest_sha256"]
        == BASE_INPUT_PINS[
            "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
            "manifest.sha256"
        ]
        and direct["Round292_builder_sha256"]
        == R294B_PACKAGE_MEMBER_PINS[
            "cm2_round292_source_g_occurrence_registry_"
            "candidate_construction.py"
        ]
        and verification["candidate_artifacts"]["producer_sha256"]
        == R294B_PACKAGE_MEMBER_PINS[R294B_PACKAGE_PREFIX + ".py"]
        and verification["candidate_artifacts"]["verifier_sha256"]
        == R294B_PACKAGE_MEMBER_PINS[
            R294B_PACKAGE_PREFIX + "_verifier.py"
        ]
        and manifest_audit["Round292A_member_count"] == 7
        and manifest_audit["Round294_member_count"] == 9
        and manifest_audit["all_16_members_actual_hash_match"] is True
        and manifest_audit["extra_or_missing_member_count"] == 0
        and independence[
            "Round292A_or_Round294_producer_imported_or_executed"
        ] is False
        and independence["Round294B_producer_imported_or_executed"] is False
        and independence["candidate_used_as_expected_oracle"] is False
        and nonpromotion["post_Round294_expanded_registry_component_DSU_status"]
        == "NOT_REBUILT"
        and nonpromotion["post_Round294_quotient_component_count"] is None
        and all(value == 0 for value in credits.values()),
        "Round294B sealed admission verification closure",
    )


def validate_inputs(input_dir: Path, allow_provisional: bool) -> None:
    need(input_dir.resolve() == DEFAULT_INPUT_DIR.resolve(),
         "input directory must be formal deliverables")
    for name, expected in BASE_INPUT_PINS.items():
        validate_regular_pinned_file(
            input_dir / name,
            expected,
            "base input:" + name,
        )
    for name, expected in EXECUTABLE_TRANSITIVE_CLOSURE_PINS.items():
        validate_regular_pinned_file(
            input_dir / name,
            expected,
            "executable transitive closure:" + name,
        )
    need(
        EXECUTABLE_TRANSITIVE_CLOSURE_PINS[R179_KERNEL]
        == BASE_INPUT_PINS[R179_KERNEL],
        "Round179 executable pin agrees with base pin",
    )
    for manifest_name, members in MANIFEST_MEMBERS.items():
        manifest = parse_manifest(input_dir / manifest_name)
        if manifest_name in {R182_PACKAGE_MANIFEST, R294B_MANIFEST}:
            need(
                set(manifest) == set(members),
                "exact sealed manifest member set:" + manifest_name,
            )
        for member in members:
            need(
                manifest.get(member) == BASE_INPUT_PINS[member],
                "manifest member:" + manifest_name + ":" + member,
            )
    validate_r294b_admission(input_dir)

    need(
        R303A_SEAL_MANIFEST_PIN is None
        or is_pin(R303A_SEAL_MANIFEST_PIN),
        "Round303A seal manifest replacement pin format",
    )
    need(
        all(value is None or is_pin(value)
            for value in R303A_MANIFEST_MEMBER_PINS.values()),
        "Round303A seal member replacement pin format",
    )
    sealed = r303a_seal_complete()
    if not sealed:
        need(allow_provisional, "Round303-A is not sealed")
    for name, expected in PROVISIONAL_R303A_PINS.items():
        validate_regular_pinned_file(
            input_dir / name,
            expected,
            "Round303A raw:" + name,
        )
    if sealed:
        need(
            type(R303A_SEAL_MANIFEST_PIN) is str,
            "Round303A sealed manifest pin type",
        )
        validate_regular_pinned_file(
            input_dir / R303A_MANIFEST,
            R303A_SEAL_MANIFEST_PIN,
            "Round303A seal manifest:" + R303A_MANIFEST,
        )
        manifest = parse_manifest(input_dir / R303A_MANIFEST)
        need(
            set(manifest) == set(R303A_MANIFEST_MEMBER_PINS),
            "Round303A seal manifest exact ten-member set",
        )
        for name, expected in R303A_MANIFEST_MEMBER_PINS.items():
            need(
                type(expected) is str,
                "Round303A sealed member pin type:" + name,
            )
            validate_regular_pinned_file(
                input_dir / name,
                expected,
                "Round303A sealed member:" + name,
            )
            need(
                manifest.get(name) == expected,
                "Round303A seal manifest member:" + name,
            )


class ListHasher:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        self.add_canonical(canonical(value))

    def add_canonical(self, value: bytes) -> None:
        if self.count:
            self.state.update(b",")
        self.state.update(value)
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


class RowSpool:
    CHUNK_ROWS = 512

    def __init__(self, path: Path, id_field: str) -> None:
        self.path = path
        self.id_field = id_field
        self.seen: set[str] = set()
        self.pending: list[tuple[str, str, bytes]] = []
        self.chunks: list[Path] = []

    def add(self, row: dict[str, Any]) -> None:
        row_id = row[self.id_field]
        need(row_id not in self.seen, "duplicate output row:" + row_id)
        self.seen.add(row_id)
        self.pending.append((row_id, row["row_sha256"], canonical(row)))
        if len(self.pending) >= self.CHUNK_ROWS:
            self.flush_chunk()

    def flush_chunk(self) -> None:
        if not self.pending:
            return
        self.pending.sort(key=lambda item: item[0])
        chunk = self.path.with_name(
            self.path.name + f".chunk.{len(self.chunks):06d}"
        )
        with chunk.open("wb") as stream:
            for row_id, row_sha256, encoded in self.pending:
                stream.write(
                    row_id.encode("ascii")
                    + b"\t"
                    + row_sha256.encode("ascii")
                    + b"\t"
                    + encoded
                    + b"\n"
                )
            stream.flush()
            os.fsync(stream.fileno())
        self.chunks.append(chunk)
        self.pending.clear()

    def close(self) -> dict[str, Any]:
        self.flush_chunk()
        rows = ListHasher()
        ids = ListHasher()
        hashes = ListHasher()
        streams = [chunk.open("rb") for chunk in self.chunks]
        try:
            merged = heapq.merge(
                *streams,
                key=lambda line: line.split(b"\t", 1)[0],
            )
            last_id: str | None = None
            with self.path.open("wb") as output:
                for line in merged:
                    raw_id, raw_hash, encoded = line.rstrip(b"\n").split(
                        b"\t", 2
                    )
                    row_id = raw_id.decode("ascii")
                    row_hash = raw_hash.decode("ascii")
                    need(
                        last_id is None or last_id < row_id,
                        "strict output row-id order:" + self.id_field,
                    )
                    last_id = row_id
                    output.write(encoded + b"\n")
                    rows.add_canonical(encoded)
                    ids.add(row_id)
                    hashes.add(row_hash)
                output.flush()
                os.fsync(output.fileno())
        finally:
            for stream in streams:
                stream.close()
        need(rows.count == len(self.seen), "sorted spool row census")
        return {
            "row_count": rows.count,
            "row_ids_sha256": ids.finish(),
            "row_hashes_sha256": hashes.finish(),
            "rows_sha256": rows.finish(),
        }


def canonical_pair(value: Any, label: str) -> tuple[str, str]:
    need(
        type(value) is list
        and len(value) == 2
        and all(type(item) is str and item for item in value)
        and value[0] < value[1],
        "canonical pair:" + label,
    )
    return value[0], value[1]


R300D = (
    "cm2_round300d_source_g_lower_physical_witness_component_edge_"
    "promotion_ledger.json.gz"
)
R301_MEMBERS = (
    "cm2_round301_source_g_legal_component_dsu_application_"
    "member_component_ledger.json.gz"
)
R301_INELIGIBLE = (
    "cm2_round301_source_g_legal_component_dsu_application_"
    "ineligible_source_consumption_ledger.json.gz"
)
R294 = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)
R295A = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_"
    "closure_physical_witness_incidence_binding_ledger.json.gz"
)
R293 = (
    "cm2_round293_source_g_r289_r291_witness_binding_canonical_"
    "closure_ledger.json.gz"
)
R291 = (
    "cm2_round291_source_g_complete_lower_stratum_local_disposition_"
    "freeze_ledger.json.gz"
)
R303A_BRIDGES = (
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_"
    "bridge_ledger.json.gz"
)
R303A_UNRESOLVED = (
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_"
    "unresolved_bridge_ledger.json.gz"
)
R303A_RESULT = (
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_"
    "result.json"
)
R204 = (
    "cm2_round204_source_g_wall_return_signature_local_replacement_"
    "certificate.json"
)
R182 = "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
R179 = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R179_KERNEL = "cm2_round179_source_g_residual_tube_arrangement.py"
R174_KERNEL = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_"
    "materialization_verifier.py"
)
FIRST_HIT_KERNEL = "cm2_gate3_candidate_first_hit_cert.py"
INTERVAL_ATLAS_KERNEL = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
GE_KERNEL = "cm2_gate3_ge_interval_atlas_cert.py"
EXECUTABLE_TRANSITIVE_CLOSURE_PINS = {
    R179_KERNEL:
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    R174_KERNEL:
        "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
    FIRST_HIT_KERNEL:
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    INTERVAL_ATLAS_KERNEL:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    GE_KERNEL:
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
}
EXECUTABLE_IMPORT_GRAPH = {
    R179_KERNEL: [R174_KERNEL],
    R174_KERNEL: [FIRST_HIT_KERNEL, INTERVAL_ATLAS_KERNEL],
    INTERVAL_ATLAS_KERNEL: [FIRST_HIT_KERNEL, GE_KERNEL],
    GE_KERNEL: [FIRST_HIT_KERNEL],
    FIRST_HIT_KERNEL: [],
}
EXECUTABLE_LOAD_ORDER = (
    FIRST_HIT_KERNEL,
    GE_KERNEL,
    INTERVAL_ATLAS_KERNEL,
    R174_KERNEL,
)


def collect_scope(input_dir: Path) -> tuple[
    list[dict[str, Any]], dict[str, dict[str, Any]]
]:
    records: dict[str, dict[str, Any]] = {}
    endpoints: set[str] = set()
    canonical_pairs: set[tuple[str, str]] = set()
    tranche_histogram: Counter[str] = Counter()
    for row in iter_array(input_dir / R300D, '"canonical_incidence_edge_rows":['):
        need(type(row) is dict, "R300D row")
        row_id = row["Round300D_lower_physical_witness_incidence_edge_row_id"]
        need(row_id not in records, "duplicate R300D row")
        verify_row(row, row_id)
        pair = canonical_pair(
            row["canonical_unordered_Round294_registry_occurrence_ids"],
            row_id,
        )
        need(pair not in canonical_pairs, "duplicate R300D canonical pair")
        canonical_pairs.add(pair)
        left, right = row["left_endpoint"], row["right_endpoint"]
        need(
            [left["registry_occurrence_id"], right["registry_occurrence_id"]]
            == list(pair)
            and row["shared_lower_witness_incidence_proved"] is True
            and row["formal_component_edge_credit"] == 0
            and row["included_stratum_gluing_lemma_pinned"] is False
            and row["eligible_for_component_DSU_application"] is False,
            "R300D fail-closed row:" + row_id,
        )
        tranche = (
            left["registry_entry_kind"] + "|" + right["registry_entry_kind"]
        )
        tranche_histogram[tranche] += 1
        records[row_id] = {
            "source_id": row_id,
            "source_sha256": row["row_sha256"],
            "pair": pair,
            "tranche": tranche,
            "endpoint_refs": {
                left["registry_occurrence_id"]: {
                    "row_id": left["Round294_occurrence_registry_row_id"],
                    "row_sha256": left["Round294_occurrence_registry_row_sha256"],
                    "kind": left["registry_entry_kind"],
                    "chart": left["physical_support_chart"],
                    "official_key_id": left["final_Round299A_official_key_id"],
                    "official_key_ordinal":
                        left["final_Round299A_official_key_ordinal"],
                    "signature_sha256":
                        left["complete_10_field_return_signature_sha256"],
                },
                right["registry_occurrence_id"]: {
                    "row_id": right["Round294_occurrence_registry_row_id"],
                    "row_sha256": right["Round294_occurrence_registry_row_sha256"],
                    "kind": right["registry_entry_kind"],
                    "chart": right["physical_support_chart"],
                    "official_key_id": right["final_Round299A_official_key_id"],
                    "official_key_ordinal":
                        right["final_Round299A_official_key_ordinal"],
                    "signature_sha256":
                        right["complete_10_field_return_signature_sha256"],
                },
            },
            "r295_ids":
                row["source_Round295A_physical_incidence_binding_row_ids"],
            "r295_hashes":
                row["source_Round295A_physical_incidence_binding_row_sha256s"],
            "r291_ids": row["source_Round291_local_disposition_row_ids"],
            "cell_indices": row["physical_witness_cell_indices"],
            "source_charts": row["source_charts"],
            "witness_kind_histogram": row["witness_kind_histogram"],
            "witness_multiplicity": row["witness_multiplicity"],
        }
        endpoints.update(pair)
    need(len(records) == EXPECTED_R300D, "R300D census")
    need(
        len(canonical_pairs) == EXPECTED_R300D,
        "R300D canonical-pair uniqueness census",
    )
    need(
        tranche_histogram == {
            R288_KIND + "|" + R288_KIND: 111_332,
            PRESERVED_KIND + "|" + PRESERVED_KIND: 192,
        },
        "R300D tranche census",
    )

    residual_disposition = (
        "INELIGIBLE_INCIDENCE_ONLY__NO_STRONGER_GATE_PROOF"
    )
    disposition_histogram: Counter[str] = Counter()
    all_seen: set[str] = set()
    residual_ids: set[str] = set()
    for row in iter_array(input_dir / R301_INELIGIBLE, '"rows":['):
        if row.get("source_relation") != (
            "R300D_CANONICAL_TWO_TARGET_LOWER_PHYSICAL_WITNESS_INCIDENCE_EDGE"
        ):
            continue
        source_id = row["source_row_id"]
        verify_row(row, source_id)
        need(source_id in records and source_id not in all_seen,
             "R301/R300D row")
        all_seen.add(source_id)
        need(
            row["source_row_sha256"] == records[source_id]["source_sha256"]
            and canonical_pair(
                row["canonical_occurrence_endpoint_pair"], source_id
            ) == records[source_id]["pair"]
            and row["source_row_fed_to_DSU"] is False
            and row["eligible_for_component_DSU_application"] is False
            and row["formal_DSU_rank_reduction_credit"] == 0
            and row["formal_component_edge_application_credit"] == 0
            and row["formal_component_union_credit"] == 0,
            "R301 fail-closed source:" + source_id,
        )
        disposition = row["disposition"]
        disposition_histogram[disposition] += 1
        if disposition == residual_disposition:
            need(
                row["stronger_gate_names"] == []
                and row["legal_stronger_edge_references"] == []
                and row["exact_gate_provenance_references"] == [],
                "R301 residual incidence-only row:" + source_id,
            )
            residual_ids.add(source_id)
        elif disposition.endswith("PAIR_RECLOSED_BY_STRONGER_LEGAL_EDGE"):
            need(
                row["stronger_gate_names"] != []
                and row["legal_stronger_edge_references"] != []
                and row["exact_gate_provenance_references"] != [],
                "R301 stronger-edge reclosure:" + source_id,
            )
        elif disposition.endswith("AUDITED_FAIL_CLOSED_NO_EDGE"):
            need(
                row["stronger_gate_names"] != []
                and row["legal_stronger_edge_references"] == []
                and row["exact_gate_provenance_references"] != [],
                "R301 audited fail-closed row:" + source_id,
            )
        else:
            raise PromotionError("unexpected R301 disposition:" + disposition)
        records[source_id]["r301_ineligible_ref"] = {
            "row_id": row["Round301_ineligible_source_consumption_row_id"],
            "row_sha256": row["row_sha256"],
            "disposition": disposition,
        }
    need(all_seen == set(records), "complete R301/R300D consumption")
    need(
        disposition_histogram == {
            residual_disposition: 110_516,
            (
                "INELIGIBLE_SOURCE_ROW_NOT_CONSUMED__"
                "PAIR_RECLOSED_BY_STRONGER_LEGAL_EDGE"
            ): 736,
            (
                "INELIGIBLE_SOURCE_ROW_NOT_CONSUMED__"
                "AUDITED_FAIL_CLOSED_NO_EDGE"
            ): 272,
        }
        and len(residual_ids) == 110_516,
        "R301/R300D residual partition census",
    )
    residual_records = [
        records[source_id] for source_id in sorted(residual_ids)
    ]
    residual_endpoints = {
        endpoint
        for record in residual_records
        for endpoint in record["pair"]
    }

    members: dict[str, dict[str, Any]] = {}
    for row in iter_array(input_dir / R301_MEMBERS, '"rows":['):
        endpoint = row.get("registry_or_frontier_member_id")
        if endpoint not in residual_endpoints:
            continue
        verify_row(row, str(endpoint))
        need(
            endpoint not in members
            and row["member_kind"] in {
                "EXPANDED_OCCURRENCE", R288_KIND, PRESERVED_KIND
            }
            and row["formal_component_membership_credit"] == 1
            and row["member_identity_preserved"] is True
            and row["formal_occurrence_identity_collapse_credit"] == 0,
            "R301 selected member:" + str(endpoint),
        )
        members[endpoint] = {
            "row_id": row["Round301_member_to_component_row_id"],
            "row_sha256": row["row_sha256"],
            "component_id": row["final_Round301_component_id"],
            "base_root_id": row["base_component_root_id"],
            "official_key_id": row["official_key_id"],
            "member_kind": row["member_kind"],
        }
    need(set(members) == residual_endpoints, "R301 residual endpoint coverage")

    cross: list[dict[str, Any]] = []
    for record in residual_records:
        left, right = record["pair"]
        if members[left]["component_id"] == members[right]["component_id"]:
            continue
        record["member_refs"] = {left: members[left], right: members[right]}
        cross.append(record)
    cross.sort(key=lambda item: item["source_id"])
    cross_histogram = Counter(item["tranche"] for item in cross)
    cross_pairs = {record["pair"] for record in cross}
    cross_endpoints = {
        endpoint for record in cross for endpoint in record["pair"]
    }
    need(
        len(cross) == EXPECTED_CROSS
        and len(cross_pairs) == EXPECTED_CROSS
        and len(cross_endpoints) == EXPECTED_SELECTED_ENDPOINTS
        and cross_histogram == {
            R288_KIND + "|" + R288_KIND: EXPECTED_B1_SCOPE,
            PRESERVED_KIND + "|" + PRESERVED_KIND: EXPECTED_B2,
        },
        "cross-R301 exact scope:"
        + str(len(cross))
        + ":"
        + json.dumps(dict(sorted(cross_histogram.items())), sort_keys=True),
    )

    need(
        all(
            record["r301_ineligible_ref"]["disposition"]
            == residual_disposition
            for record in cross
        ),
        "cross R301 pairs are residual incidence-only",
    )
    return cross, members


def validate_r303a_result(input_dir: Path) -> dict[str, Any]:
    result = read_json(input_dir / R303A_RESULT)
    claimed = result.get("result_sha256")
    payload = dict(result)
    payload.pop("result_sha256", None)
    need(
        digest(payload) == claimed
        and result["complete_formal_run"] is True
        and result["theorem_sha256"]
        == "41141dbd0fbc9d501c5714ab61b7907711f1a6fdcee1796a6cbc602e9aab138f"
        and result["bridge_census"]["bridge_count"] == 87_824
        and result["bridge_census"]["unresolved_count"] == 8
        and result["formal_credit_transition"][
            "formal_component_edge_credit"
        ] == 0,
        "Round303A result closure/provisional census",
    )
    need(
        result["materialized_bridge_ledger"]["file_sha256"]
        == PROVISIONAL_R303A_PINS[R303A_BRIDGES]
        and result["unresolved_bridge_ledger"]["file_sha256"]
        == PROVISIONAL_R303A_PINS[R303A_UNRESOLVED],
        "Round303A raw ledger/result binding",
    )
    return result


def compact_bridge(row: dict[str, Any]) -> dict[str, Any]:
    endpoint = row["registry_occurrence_id"]
    scope = row["Round300D_Round301_scope_reference"]
    witness = row["connected_source_side_witness"]
    leaf = row["Round182_leaf_reference"]
    active = row["Round179_active_geometry_reference"]
    need(
        row["A0_exact_provenance_pins_and_row_closures"] is True
        and row["A1_Round294_issued_occurrence_has_nonempty_inner_anchor"] is True
        and row["A2_strict_anchor_subbox_inside_issued_inner_support"] is True
        and row["A3_occurrence_atom_source_side_provenance_exactly_closed"] is True
        and row["A4_unique_formal_connected_source_signed_region_materialized"]
        is True
        and row["eligible_as_R303B_G1_bridge_input"] is True
        and row["formal_occurrence_anchor_connected_side_bridge_credit"] == 1
        and row["formal_component_edge_credit"] == 0
        and row["full_occurrence_support_equality_claimed"] is False
        and witness["connected"] is True
        and witness["strict_anchor_subbox_has_same_active_factor_sign"] is True
        and row["active_factor_strict_sign"] in STRICT_SIGNS,
        "Round303A bridge contract:" + endpoint,
    )
    return {
        "endpoint": endpoint,
        "row_id":
            row["Round303A_occurrence_anchor_source_side_bridge_row_id"],
        "row_sha256": row["row_sha256"],
        "source_R300D_row_id": scope["source_Round300D_row_id"],
        "source_R300D_row_sha256": scope["source_Round300D_row_sha256"],
        "source_R301_row_id": scope["source_Round301_ineligible_row_id"],
        "source_R301_row_sha256":
            scope["source_Round301_ineligible_row_sha256"],
        "opposite_endpoint": scope["opposite_endpoint"],
        "Round301_member_row": scope["this_Round301_member_row"],
        "Round294_registry_reference": row["Round294_registry_reference"],
        "active_factor_strict_sign": row["active_factor_strict_sign"],
        "active_factor_equation": row["active_factor_equation"],
        "anchor_box": row["exact_strict_anchor_subbox"],
        "issued_inner_support_box": row["exact_issued_inner_support_box"],
        "connected_source_side_witness": witness,
        "source_side_row_references": row["source_side_row_references"],
        "Round182_leaf_reference": leaf,
        "Round179_active_geometry_reference": active,
        "theorem_id": row["theorem_id"],
        "theorem_sha256": row["theorem_sha256"],
    }


def compact_unresolved(row: dict[str, Any]) -> dict[str, Any]:
    endpoint = row["registry_occurrence_id"]
    scope = row["Round300D_Round301_scope_reference"]
    need(
        row["A0_exact_provenance_pins_and_row_closures"] is True
        and row["A1_Round294_issued_occurrence_has_nonempty_inner_anchor"] is True
        and row["A2_strict_anchor_subbox_inside_issued_inner_support"] is True
        and row["A3_occurrence_atom_source_side_provenance_exactly_closed"] is True
        and row["A4_unique_formal_connected_source_signed_region_materialized"]
        is False
        and row["eligible_as_R303B_G1_bridge_input"] is False
        and row["formal_occurrence_anchor_connected_side_bridge_credit"] == 0
        and row["formal_component_edge_credit"] == 0
        and row["nonedge_or_exclusion_claimed"] is False
        and row["disposition"]
        == "UNRESOLVED__W_TAIL_CONNECTED_SOURCE_SIDE_EXTENSION_MISSING",
        "Round303A unresolved contract:" + endpoint,
    )
    return {
        "endpoint": endpoint,
        "row_id":
            row["Round303A_unresolved_occurrence_anchor_bridge_row_id"],
        "row_sha256": row["row_sha256"],
        "source_R300D_row_id": scope["source_Round300D_row_id"],
        "source_R300D_row_sha256": scope["source_Round300D_row_sha256"],
        "source_R301_row_id": scope["source_Round301_ineligible_row_id"],
        "source_R301_row_sha256":
            scope["source_Round301_ineligible_row_sha256"],
        "opposite_endpoint": scope["opposite_endpoint"],
        "missing_obligation": row["missing_obligation"],
        "disposition": row["disposition"],
    }


def collect_r303a_partition(
    input_dir: Path,
    cross: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    result = validate_r303a_result(input_dir)
    bridge_hasher = ListHasher()
    bridge_ids = ListHasher()
    bridge_hashes = ListHasher()
    bridges: dict[str, dict[str, Any]] = {}
    for row in iter_array(
        input_dir / R303A_BRIDGES, '"materialized_bridge_rows":['
    ):
        need(type(row) is dict, "Round303A bridge row")
        endpoint = row["registry_occurrence_id"]
        verify_row(row, endpoint)
        need(endpoint not in bridges, "duplicate Round303A bridge endpoint")
        bridges[endpoint] = compact_bridge(row)
        bridge_hasher.add(row)
        bridge_ids.add(row["Round303A_occurrence_anchor_source_side_bridge_row_id"])
        bridge_hashes.add(row["row_sha256"])
    expected = result["materialized_bridge_ledger"]
    need(
        bridge_hasher.count == expected["row_count"] == 87_824
        and bridge_hasher.finish() == expected["rows_sha256"]
        and bridge_ids.finish() == expected["row_ids_sha256"]
        and bridge_hashes.finish() == expected["row_hashes_sha256"],
        "Round303A complete bridge ledger commitments",
    )

    unresolved_hasher = ListHasher()
    unresolved_ids = ListHasher()
    unresolved_hashes = ListHasher()
    unresolved: dict[str, dict[str, Any]] = {}
    for row in iter_array(
        input_dir / R303A_UNRESOLVED, '"unresolved_bridge_rows":['
    ):
        need(type(row) is dict, "Round303A unresolved row")
        endpoint = row["registry_occurrence_id"]
        verify_row(row, endpoint)
        need(endpoint not in unresolved, "duplicate Round303A unresolved endpoint")
        unresolved[endpoint] = compact_unresolved(row)
        unresolved_hasher.add(row)
        unresolved_ids.add(
            row["Round303A_unresolved_occurrence_anchor_bridge_row_id"]
        )
        unresolved_hashes.add(row["row_sha256"])
    expected = result["unresolved_bridge_ledger"]
    need(
        unresolved_hasher.count == expected["row_count"] == 8
        and unresolved_hasher.finish() == expected["rows_sha256"]
        and unresolved_ids.finish() == expected["row_ids_sha256"]
        and unresolved_hashes.finish() == expected["row_hashes_sha256"],
        "Round303A complete unresolved ledger commitments",
    )
    need(set(bridges).isdisjoint(unresolved), "Round303A bridge partition disjoint")

    b1_records = [
        item for item in cross
        if item["tranche"] == R288_KIND + "|" + R288_KIND
    ]
    b2_records = [
        item for item in cross
        if item["tranche"] == PRESERVED_KIND + "|" + PRESERVED_KIND
    ]
    accepted_b1: list[dict[str, Any]] = []
    unresolved_b1: list[dict[str, Any]] = []
    all_r288_endpoints: set[str] = set()
    bridge_endpoints = set(bridges)
    unresolved_endpoints = set(unresolved)
    for record in b1_records:
        pair = set(record["pair"])
        all_r288_endpoints.update(pair)
        in_bridge = pair <= bridge_endpoints
        in_unresolved = pair <= unresolved_endpoints
        need(in_bridge ^ in_unresolved,
             "Round303A whole-pair accepted/unresolved partition:"
             + record["source_id"])
        if in_bridge:
            for endpoint in record["pair"]:
                bridge = bridges[endpoint]
                need(
                    bridge["source_R300D_row_id"] == record["source_id"]
                    and bridge["source_R300D_row_sha256"]
                    == record["source_sha256"]
                    and bridge["opposite_endpoint"]
                    == next(value for value in record["pair"] if value != endpoint)
                    and bridge["source_R301_row_id"]
                    == record["r301_ineligible_ref"]["row_id"]
                    and bridge["source_R301_row_sha256"]
                    == record["r301_ineligible_ref"]["row_sha256"],
                    "Round303A/R300D/R301 bridge scope:" + endpoint,
                )
            record["bridge_refs"] = {
                endpoint: bridges[endpoint] for endpoint in record["pair"]
            }
            accepted_b1.append(record)
        else:
            for endpoint in record["pair"]:
                gap = unresolved[endpoint]
                need(
                    gap["source_R300D_row_id"] == record["source_id"]
                    and gap["source_R300D_row_sha256"]
                    == record["source_sha256"]
                    and gap["source_R301_row_id"]
                    == record["r301_ineligible_ref"]["row_id"],
                    "Round303A W-tail scope:" + endpoint,
                )
            record["unresolved_refs"] = {
                endpoint: unresolved[endpoint] for endpoint in record["pair"]
            }
            unresolved_b1.append(record)
    need(
        bridge_endpoints | unresolved_endpoints == all_r288_endpoints
        and len(accepted_b1) == EXPECTED_B1
        and len(unresolved_b1) == EXPECTED_WTAIL
        and len(b2_records) == EXPECTED_B2
        and len(accepted_b1) + len(b2_records) + len(unresolved_b1)
        == EXPECTED_CROSS,
        "Round303B B1/B2/W-tail partition census",
    )
    route_pairs = {
        "B1": {record["pair"] for record in accepted_b1},
        "B2": {record["pair"] for record in b2_records},
        "W_tail": {record["pair"] for record in unresolved_b1},
    }
    route_endpoints = {
        route: {
            endpoint
            for record in records
            for endpoint in record["pair"]
        }
        for route, records in (
            ("B1", accepted_b1),
            ("B2", b2_records),
            ("W_tail", unresolved_b1),
        )
    }
    need(
        len(route_pairs["B1"]) == EXPECTED_B1
        and len(route_pairs["B2"]) == EXPECTED_B2
        and len(route_pairs["W_tail"]) == EXPECTED_WTAIL
        and route_pairs["B1"].isdisjoint(route_pairs["B2"])
        and route_pairs["B1"].isdisjoint(route_pairs["W_tail"])
        and route_pairs["B2"].isdisjoint(route_pairs["W_tail"])
        and set().union(*route_pairs.values())
        == {record["pair"] for record in cross}
        and len(route_endpoints["B1"]) == 2 * EXPECTED_B1
        and len(route_endpoints["B2"]) == 2 * EXPECTED_B2
        and len(route_endpoints["W_tail"]) == 2 * EXPECTED_WTAIL
        and route_endpoints["B1"].isdisjoint(route_endpoints["B2"])
        and route_endpoints["B1"].isdisjoint(route_endpoints["W_tail"])
        and route_endpoints["B2"].isdisjoint(route_endpoints["W_tail"])
        and len(set().union(*route_endpoints.values()))
        == EXPECTED_SELECTED_ENDPOINTS,
        "Round303B exact pair/endpoint route partition",
    )
    return accepted_b1, b2_records, unresolved_b1


def collect_r294(
    input_dir: Path,
    records: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    wanted = {
        endpoint
        for record in records
        for endpoint in record["pair"]
    }
    expected = {
        endpoint: record["endpoint_refs"][endpoint]
        for record in records
        for endpoint in record["pair"]
    }
    selected: dict[str, dict[str, Any]] = {}
    for row in iter_array(input_dir / R294, '"rows":['):
        endpoint = row.get("registry_occurrence_id")
        if endpoint not in wanted:
            continue
        verify_row(row, str(endpoint))
        ref = expected[endpoint]
        need(
            endpoint not in selected
            and row["Round294_occurrence_registry_row_id"] == ref["row_id"]
            and row["row_sha256"] == ref["row_sha256"]
            and row["registry_entry_kind"] == ref["kind"]
            and row["physical_support_chart"] == ref["chart"]
            and row["official_key_id"] == ref["official_key_id"]
            and row["official_key_ordinal"] == ref["official_key_ordinal"]
            and row["complete_10_field_return_signature_sha256"]
            == ref["signature_sha256"],
            "R300D/R294 endpoint:" + str(endpoint),
        )
        selected[endpoint] = row
    need(set(selected) == wanted, "R294 sample endpoint coverage")
    return selected


def collect_physical_chain(
    input_dir: Path,
    records: list[dict[str, Any]],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    wanted_295: dict[str, str] = {}
    for record in records:
        need(
            len(record["r295_ids"]) == len(record["r295_hashes"]) == 1
            and len(record["r291_ids"]) == len(record["cell_indices"]) == 1
            and record["witness_kind_histogram"]
            == {"ROUND182_GRAPH_SHEET_LEAF": 1}
            and record["witness_multiplicity"] == 1,
            "single physical graph witness:" + record["source_id"],
        )
        wanted_295[record["r295_ids"][0]] = record["r295_hashes"][0]
    r295: dict[str, dict[str, Any]] = {}
    for row in iter_array(input_dir / R295A, '"rows":['):
        row_id = row.get("Round295A_R291_physical_incidence_binding_row_id")
        if row_id not in wanted_295:
            continue
        verify_row(row, str(row_id))
        need(
            row_id not in r295
            and row["row_sha256"] == wanted_295[row_id]
            and row["Round295A_binding_classification"] == (
                "FORMAL_ROUND294_REGISTRY_REBIND__"
                "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            )
            and row["source_Round293_binding_classification"]
            == "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            and row["exact_witness_covered_by_named_registry_supports"] is True
            and row["formal_target_reference_credit"] == 2
            and row["formal_DSU_rank_reduction_credit"] == 0,
            "R295A selected binding:" + str(row_id),
        )
        r295[row_id] = row
    need(set(r295) == set(wanted_295), "R295A sample coverage")

    wanted_293 = {
        row["source_Round293_R291_physical_witness_binding_row_id"]:
            row["source_Round293_R291_physical_witness_binding_row_sha256"]
        for row in r295.values()
    }
    r293: dict[str, dict[str, Any]] = {}
    for row in iter_array(
        input_dir / R293, '"Round291_physical_witness_binding_rows":['
    ):
        row_id = row.get("Round292_R291_physical_witness_binding_row_id")
        if row_id not in wanted_293:
            continue
        verify_row(row, str(row_id))
        need(
            row_id not in r293
            and row["row_sha256"] == wanted_293[row_id]
            and row["binding_classification"]
            == "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            and row["exact_witness_covered_by_named_registry_supports"] is True
            and row["component_edge_credit"] == 0,
            "R293 selected binding:" + str(row_id),
        )
        r293[row_id] = row
    need(set(r293) == set(wanted_293), "R293 sample coverage")

    requested_291: dict[str, set[int]] = {}
    for record in records:
        requested_291.setdefault(record["r291_ids"][0], set()).add(
            record["cell_indices"][0]
        )
    r291: dict[str, dict[str, Any]] = {}
    for row in iter_array(input_dir / R291, '"rows":['):
        row_id = row.get("complete_lower_stratum_local_disposition_row_id")
        if row_id not in requested_291:
            continue
        verify_row(row, str(row_id))
        need(
            row_id not in r291
            and row["local_disposition"] == "WHOLE_PHYSICAL_SUPPORT"
            and row["representation_role"] == "DIRECT_GRAPH_SHEET_WITNESS"
            and row["component_edge_credit"] == 0
            and row["occurrence_binding_status"]
            == "PENDING_FINAL_OCCURRENCE_REGISTRY",
            "R291 physical row:" + str(row_id),
        )
        cells: dict[int, dict[str, Any]] = {}
        for index in requested_291[row_id]:
            need(0 <= index < len(row["physical_witness_cells"]),
                 "R291 cell index")
            cell = row["physical_witness_cells"][index]
            need(
                cell["witness_kind"] == "ROUND182_GRAPH_SHEET_LEAF"
                and Q(cell["base_coordinate_area"]) > 0,
                "R291 positive graph cell",
            )
            cells[index] = cell
        r291[row_id] = {"row": row, "cells": cells}
    need(set(r291) == set(requested_291), "R291 sample coverage")

    for record in records:
        a = r295[record["r295_ids"][0]]
        b = r293[a["source_Round293_R291_physical_witness_binding_row_id"]]
        need(
            a["Round291_local_disposition_row_id"]
            == b["Round291_local_disposition_row_id"]
            == record["r291_ids"][0]
            and a["physical_witness_cell_index"]
            == b["physical_witness_cell_index"]
            == record["cell_indices"][0]
            and sorted(a["target_Round294_registry_occurrence_ids"])
            == sorted(b["terminal_registry_target_references"])
            == list(record["pair"])
            and a["source_Round293_R291_physical_witness_binding_row_sha256"]
            == b["row_sha256"],
            "R300D/R295A/R293/R291 chain:" + record["source_id"],
        )
    return r295, r293, r291


R182_LEAF_COLUMNS = [
    "row_id", "occurrence_row_id", "retained_child_row_id",
    "base_refinement_path", "box", "coordinate_volume",
    "base_coordinate_area", "lower_t_face_status", "upper_t_face_status",
    "graph_classification", "two_dimensional_graph_sheet_count",
    "one_dimensional_clipping_curve_segment_count",
    "zero_dimensional_boundary_endpoint_incidence_count",
    "closed_3d_side_union_volume", "residual_3d_collar_volume",
]
R182_COLLAR_COLUMNS = [
    "row_id", "Round179_occurrence_row_id", "origin_row_id", "parent_id",
    "chart", "owner_target", "kind", "reason_label", "equation",
    "target_obstacle", "strict_t_derivative_sign",
    "Round179_origin_already_fully_replaced",
    "Round179_retained_child_count", "Round179_retained_coordinate_volume",
    "bounded_base_split_axis", "bounded_base_split_depth",
    "closed_leaf_count", "closed_coordinate_volume", "residual_leaf_count",
    "residual_coordinate_volume", "full_base_graph_leaf_count",
    "absent_graph_leaf_count", "clipped_graph_leaf_count",
    "two_dimensional_graph_sheet_count",
    "one_dimensional_clipping_curve_segment_count",
    "zero_dimensional_boundary_endpoint_incidence_count",
    "fully_clipped_over_Round179_retained_children", "leaf_rows_sha256",
    "whole_original_tube_credit", "global_exact_key_disposition_credit",
    "provenance",
]
R179_ORIGIN_COLUMNS = [
    "origin_row_id", "parent_id", "chart", "owner_target",
    "original_refinement_path", "original_box",
    "original_coordinate_volume", "original_reason_labels", "reason_count",
    "chosen_split_axis", "resolved_child_count",
    "resolved_child_coordinate_volume", "guard_child_count",
    "guard_child_coordinate_volume", "retained_child_count",
    "retained_child_coordinate_volume", "fully_replaced_by_bounded_children",
    "released_exact_key_count", "released_exact_key_ordinals_sha256",
    "provenance",
]
R179_RETAINED_COLUMNS = [
    "row_id", "origin_row_id", "parent_id", "chart", "child_index",
    "refinement_path", "box", "coordinate_volume", "reason_labels",
    "ambient_dimension", "whole_origin_credit",
    "global_geometric_disposition_credit", "provenance",
]
R179_OUTGOING_COLUMNS = [
    "row_id", "origin_row_id", "parent_id", "chart", "equation",
    "gradient_axis", "gradient_sign", "regularity_certification",
    "lower_t_face_sign", "upper_t_face_sign", "face_classification",
    "zero_set_dimension_account", "existence_over_full_base",
    "two_open_3d_sides_retained", "whole_origin_credit",
    "global_geometric_disposition_credit", "provenance",
]
R179_WALL_COLUMNS = [
    "row_id", "origin_row_id", "parent_id", "chart", "reason_label",
    "axis", "integer_wall", "zero_equation",
    "source_factor_classification", "source_gradient_axis",
    "source_gradient_sign", "target_factor_classification",
    "target_gradient_axis", "target_gradient_sign",
    "target_lower_face_sign", "target_upper_face_sign",
    "target_face_classification", "zero_set_dimension_account",
    "crossing_time_dependency_overwrap_discharged", "whole_origin_credit",
    "global_geometric_disposition_credit", "provenance",
]


def unpack_selected(
    path: Path,
    table_name: str,
    columns: list[str],
    id_field: str,
    wanted: set[str],
    *,
    after_marker: str | None = None,
) -> dict[str, dict[str, Any]]:
    selected: dict[str, dict[str, Any]] = {}
    marker = json.dumps(table_name, separators=(",", ":")) + ":["
    for packed in iter_array(path, marker, after_marker=after_marker):
        need(type(packed) is list and len(packed) == len(columns),
             "packed row arity:" + table_name)
        row = dict(zip(columns, packed, strict=True))
        row_id = row[id_field]
        if row_id not in wanted:
            continue
        need(row_id not in selected, "duplicate packed row:" + str(row_id))
        selected[row_id] = row
    need(set(selected) == wanted, "packed selected coverage:" + table_name)
    return selected


def load_geometry(
    input_dir: Path,
    records: list[dict[str, Any]],
    r291: dict[str, dict[str, Any]],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    leaf_ids = {
        r291[record["r291_ids"][0]]["cells"][
            record["cell_indices"][0]
        ]["leaf_row_id"]
        for record in records
    }
    leaves = unpack_selected(
        input_dir / R182,
        "collar_leaf_rows",
        R182_LEAF_COLUMNS,
        "row_id",
        leaf_ids,
    )
    occurrence_ids = {leaf["occurrence_row_id"] for leaf in leaves.values()}
    collars = unpack_selected(
        input_dir / R182,
        "collar_occurrence_rows",
        R182_COLLAR_COLUMNS,
        "Round179_occurrence_row_id",
        occurrence_ids,
    )
    origin_ids = {collar["origin_row_id"] for collar in collars.values()}
    origins = unpack_selected(
        input_dir / R179,
        "origin_tube_rows",
        R179_ORIGIN_COLUMNS,
        "origin_row_id",
        origin_ids,
    )
    retained_ids = {leaf["retained_child_row_id"] for leaf in leaves.values()}
    retained = unpack_selected(
        input_dir / R179,
        "retained_3d_child_rows",
        R179_RETAINED_COLUMNS,
        "row_id",
        retained_ids,
    )
    outgoing_ids = {
        occurrence_id
        for occurrence_id, collar in collars.items()
        if collar["kind"] == "OUTGOING"
    }
    wall_ids = occurrence_ids - outgoing_ids
    outgoing = (
        unpack_selected(
            input_dir / R179,
            "outgoing_normal_form_rows",
            R179_OUTGOING_COLUMNS,
            "row_id",
            outgoing_ids,
        )
        if outgoing_ids else {}
    )
    walls = (
        unpack_selected(
            input_dir / R179,
            "wall_normal_form_rows",
            R179_WALL_COLUMNS,
            "row_id",
            wall_ids,
            after_marker='"table_census_and_sha256":{',
        )
        if wall_ids else {}
    )
    active = {**outgoing, **walls}
    need(set(active) == occurrence_ids, "active metadata coverage")

    for record in records:
        local = r291[record["r291_ids"][0]]
        cell = local["cells"][record["cell_indices"][0]]
        leaf = leaves[cell["leaf_row_id"]]
        collar = collars[leaf["occurrence_row_id"]]
        origin = origins[collar["origin_row_id"]]
        child = retained[leaf["retained_child_row_id"]]
        need(
            leaf["box"] == cell["exact_box"]
            and leaf["base_coordinate_area"] == cell["base_coordinate_area"]
            and leaf["graph_classification"] == cell["graph_classification"]
            and leaf["retained_child_row_id"] == cell["retained_child_row_id"]
            and leaf["occurrence_row_id"]
            == local["row"]["canonical_support_row_id"]
            and collar["chart"] == local["row"]["source_chart"]
            and collar["equation"] == local["row"]["predicate_equation"]
            and origin["chart"] == collar["chart"]
            and origin["owner_target"] == collar["owner_target"]
            and child["origin_row_id"] == origin["origin_row_id"]
            and leaf["two_dimensional_graph_sheet_count"] == 1
            and Q(leaf["base_coordinate_area"]) > 0
            and Q(leaf["residual_3d_collar_volume"]) == 0
            and Q(leaf["closed_3d_side_union_volume"])
            == Q(leaf["coordinate_volume"]),
            "R179/R182/R291 graph lineage:" + record["source_id"],
        )
        record["leaf_id"] = leaf["row_id"]
        record["occurrence_row_id"] = leaf["occurrence_row_id"]
        record["origin_row_id"] = collar["origin_row_id"]
        record["retained_child_row_id"] = leaf["retained_child_row_id"]
        record["collar_kind"] = collar["kind"]
        record["source_chart"] = collar["chart"]
        record["owner_target"] = collar["owner_target"]
        record["active_equation"] = collar["equation"]
    return leaves, collars, origins, active


def read_pinned_executable(
    path: Path,
    expected_sha256: str,
    label: str,
) -> bytes:
    """Read one executable through a no-follow descriptor and reclose it."""

    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags)
    try:
        info = os.fstat(descriptor)
        need(
            stat.S_ISREG(info.st_mode)
            and info.st_nlink == 1
            and info.st_size > 0,
            label + ":regular-single-link-descriptor",
        )
        chunks: list[bytes] = []
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            chunks.append(block)
    finally:
        os.close(descriptor)
    source = b"".join(chunks)
    need(
        len(source) == info.st_size
        and hashlib.sha256(source).hexdigest() == expected_sha256,
        label + ":descriptor-sha256",
    )
    return source


def local_imports(source: bytes, filename: str) -> set[str]:
    """Return every local cm2 Python dependency named by actual AST imports."""

    try:
        tree = ast.parse(source, filename=filename)
    except (SyntaxError, ValueError) as exc:
        raise PromotionError("executable AST:" + filename) from exc
    local: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            need(node.level == 0, "no relative executable import:" + filename)
            names = [node.module] if node.module is not None else []
        else:
            if isinstance(node, ast.Call):
                function = node.func
                dynamic = (
                    isinstance(function, ast.Name)
                    and function.id == "__import__"
                ) or (
                    isinstance(function, ast.Attribute)
                    and function.attr == "import_module"
                )
                need(not dynamic, "no dynamic executable import:" + filename)
            continue
        for name in names:
            top = name.split(".", 1)[0]
            if top.startswith("cm2_"):
                local.add(top + ".py")
    return local


def pinned_executable_sources(input_dir: Path) -> dict[str, bytes]:
    """Close the complete recursive local import graph before any exec."""

    sources = {
        name: read_pinned_executable(
            input_dir / name,
            expected,
            "pinned executable:" + name,
        )
        for name, expected in EXECUTABLE_TRANSITIVE_CLOSURE_PINS.items()
    }
    actual_graph = {
        name: sorted(local_imports(source, name))
        for name, source in sources.items()
    }
    need(
        actual_graph
        == {
            name: sorted(children)
            for name, children in EXECUTABLE_IMPORT_GRAPH.items()
        },
        "exact recursive executable import graph:"
        + json.dumps(actual_graph, sort_keys=True),
    )
    discovered = {R179_KERNEL}
    queue = [R179_KERNEL]
    while queue:
        current = queue.pop()
        for child in actual_graph[current]:
            if child not in discovered:
                discovered.add(child)
                queue.append(child)
    need(
        discovered == set(EXECUTABLE_TRANSITIVE_CLOSURE_PINS),
        "complete executable transitive closure",
    )
    return sources


def execute_pinned_module(
    *,
    module_name: str,
    filename: str,
    source: bytes,
    input_dir: Path,
) -> Any:
    """Execute already-hashed bytes under one exact, canonical module name."""

    path = (input_dir / filename).resolve()
    module = types.ModuleType(module_name)
    module.__file__ = str(path)
    module.__package__ = ""
    sys.modules[module_name] = module
    try:
        code = compile(source, str(path), "exec", dont_inherit=True)
        # The bytes were O_NOFOLLOW-read, SHA-closed, and AST-audited above.
        exec(code, module.__dict__)  # noqa: S102
    except BaseException:
        if sys.modules.get(module_name) is module:
            del sys.modules[module_name]
        raise
    need(
        sys.modules.get(module_name) is module
        and Path(module.__file__).resolve() == path,
        "pinned module identity:" + module_name,
    )
    return module


def import_kernel(input_dir: Path) -> Any:
    sources = pinned_executable_sources(input_dir)
    canonical_names = {
        filename: Path(filename).stem
        for filename in EXECUTABLE_TRANSITIVE_CLOSURE_PINS
    }
    root_name = "_r303b_producer_pinned_round179_kernel"
    for module_name in [*canonical_names.values(), root_name]:
        sys.modules.pop(module_name, None)

    loaded: dict[str, Any] = {}
    for filename in EXECUTABLE_LOAD_ORDER:
        module_name = canonical_names[filename]
        loaded[filename] = execute_pinned_module(
            module_name=module_name,
            filename=filename,
            source=sources[filename],
            input_dir=input_dir,
        )
    module = execute_pinned_module(
        module_name=root_name,
        filename=R179_KERNEL,
        source=sources[R179_KERNEL],
        input_dir=input_dir,
    )
    for filename in EXECUTABLE_LOAD_ORDER:
        dependency = loaded[filename]
        module_name = canonical_names[filename]
        need(
            sys.modules.get(module_name) is dependency
            and Path(dependency.__file__).resolve()
            == (input_dir / filename).resolve(),
            "dependency module path:" + filename,
        )
    need(
        Path(module.__file__).resolve()
        == (input_dir / R179_KERNEL).resolve()
        and module.FLINT_VERSION == "0.9.0"
        and module.PRECISION_BITS == 256,
        "pinned Round179 interval runtime",
    )
    module.ctx.prec = module.PRECISION_BITS
    return module


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else (
        f"{value.numerator}/{value.denominator}"
    )


def box_values(box: Any) -> list[str]:
    return [
        qstr(box.t0), qstr(box.t1),
        qstr(box.p0), qstr(box.p1),
        qstr(box.s0), qstr(box.s1),
    ]


def exact_volume(values: list[str]) -> Q:
    need(type(values) is list and len(values) == 6, "box arity")
    q = [Q(value) for value in values]
    return (q[1] - q[0]) * (q[3] - q[2]) * (q[5] - q[4])


def volume(box: Any) -> Q:
    return (
        (box.t1 - box.t0)
        * (box.p1 - box.p0)
        * (box.s1 - box.s0)
    )


def base_area(box: Any) -> Q:
    return (box.p1 - box.p0) * (box.s1 - box.s0)


def contains(outer: Any, inner: Any) -> bool:
    return (
        outer.t0 <= inner.t0 <= inner.t1 <= outer.t1
        and outer.p0 <= inner.p0 <= inner.p1 <= outer.p1
        and outer.s0 <= inner.s0 <= inner.s1 <= outer.s1
    )


def rational_domain_margin(box: Any, axis: str) -> Q:
    need(axis in {"t", "p"}, "chart radicand axis")
    bounds = (
        (box.t0, box.t1) if axis == "t" else (box.p0, box.p1)
    )
    return 1 - max(abs(bounds[0]), abs(bounds[1])) ** 2


def active_dual(
    kernel: Any,
    origin: dict[str, Any],
    kind: str,
    metadata: dict[str, Any],
    box: Any,
) -> tuple[Any, tuple[Any, ...]]:
    geometry = kernel.interval_geometry(
        origin["chart"], origin["owner_target"], box
    )
    if kind == "OUTGOING":
        return geometry["outgoing_equality"]
    need(kind == "WALL", "known collar kind")
    target = "hit_x" if metadata["axis"] == "X" else "hit_y"
    return kernel.subtract_wall(
        geometry[target], metadata["integer_wall"]
    )


def inactive_wall_dual(
    kernel: Any,
    origin: dict[str, Any],
    metadata: dict[str, Any],
    box: Any,
) -> tuple[Any, tuple[Any, ...]]:
    geometry = kernel.interval_geometry(
        origin["chart"], origin["owner_target"], box
    )
    source = "source_x" if metadata["axis"] == "X" else "source_y"
    return kernel.subtract_wall(
        geometry[source], metadata["integer_wall"]
    )


def face_signs(
    kernel: Any,
    origin: dict[str, Any],
    kind: str,
    metadata: dict[str, Any],
    box: Any,
) -> tuple[str, str]:
    lower = kernel.fixed_axis_face(box, "t", False)
    upper = kernel.fixed_axis_face(box, "t", True)
    return (
        kernel.sign(active_dual(kernel, origin, kind, metadata, lower)[0]),
        kernel.sign(active_dual(kernel, origin, kind, metadata, upper)[0]),
    )


def round182_interval_newton_image(
    kernel: Any,
    origin: dict[str, Any],
    metadata: dict[str, Any],
    face: Any,
    axis: str,
) -> tuple[bool, str]:
    """Replay the Round182 one-dimensional face interval-Newton test."""

    need(axis in {"p", "s"}, "Round182 face Newton axis")
    axis_index = "tps".index(axis)
    lower = getattr(face, axis + "0")
    upper = getattr(face, axis + "1")
    midpoint = (lower + upper) / 2
    if axis == "p":
        midpoint_box = kernel.r174.atlas.AtlasBox(
            face.t0, face.t1, midpoint, midpoint,
            face.s0, face.s1, face.depth, face.path,
        )
    else:
        midpoint_box = kernel.r174.atlas.AtlasBox(
            face.t0, face.t1, face.p0, face.p1,
            midpoint, midpoint, face.depth, face.path,
        )
    midpoint_value = active_dual(
        kernel, origin, "WALL", metadata, midpoint_box
    )[0]
    derivative = active_dual(
        kernel, origin, "WALL", metadata, face
    )[1][axis_index]
    need(
        derivative is not None
        and kernel.sign(derivative) in STRICT_SIGNS,
        "Round182 face Newton strict derivative",
    )
    domain = kernel.r174.first_hit.arb_interval(lower, upper)
    midpoint_arb = (
        kernel.arb(midpoint.numerator) / midpoint.denominator
    )
    newton = midpoint_arb - midpoint_value / derivative
    return domain.contains_interior(newton), newton.str(40)


def round182_face_status(
    kernel: Any,
    origin: dict[str, Any],
    metadata: dict[str, Any],
    box: Any,
    upper: bool,
) -> dict[str, Any]:
    """Independently replay one Round182 target-selector t-face status."""

    face = kernel.fixed_axis_face(box, "t", upper)
    value = active_dual(kernel, origin, "WALL", metadata, face)
    raw_sign = kernel.sign(value[0])
    if raw_sign in STRICT_SIGNS:
        return {
            "kind": "STRICT",
            "raw_interval_sign": raw_sign,
            "resolved_sign": raw_sign,
            "axis": None,
            "derivative_sign": None,
            "axis_lower_sign": None,
            "axis_upper_sign": None,
            "newton_interior": None,
            "newton_image": None,
        }

    curves: list[dict[str, Any]] = []
    absences: list[dict[str, Any]] = []
    for axis in ("p", "s"):
        axis_index = "tps".index(axis)
        derivative = value[1][axis_index]
        if derivative is None:
            continue
        derivative_sign = kernel.sign(derivative)
        if derivative_sign not in STRICT_SIGNS:
            continue
        lower_face = kernel.fixed_axis_face(face, axis, False)
        upper_face = kernel.fixed_axis_face(face, axis, True)
        lower_value = active_dual(
            kernel, origin, "WALL", metadata, lower_face
        )[0]
        upper_value = active_dual(
            kernel, origin, "WALL", metadata, upper_face
        )[0]
        lower_sign = kernel.sign(lower_value)
        upper_sign = kernel.sign(upper_value)
        classification = kernel.face_classification(
            lower_value, upper_value
        )
        record = {
            "kind": (
                "CURVE"
                if classification == "FULL_BASE_UNIQUE_GRAPH"
                else "ABSENT"
            ),
            "raw_interval_sign": raw_sign,
            "resolved_sign": (
                None
                if classification == "FULL_BASE_UNIQUE_GRAPH"
                else lower_sign
            ),
            "axis": axis,
            "derivative_sign": derivative_sign,
            "axis_lower_sign": lower_sign,
            "axis_upper_sign": upper_sign,
            "newton_interior": None,
            "newton_image": None,
        }
        if classification == "FULL_BASE_UNIQUE_GRAPH":
            inside, image = round182_interval_newton_image(
                kernel, origin, metadata, face, axis
            )
            record["newton_interior"] = inside
            record["newton_image"] = image
            curves.append(record)
        elif classification == "STRICT_ZERO_ABSENT":
            need(
                lower_sign == upper_sign
                and lower_sign in STRICT_SIGNS,
                "Round182 absence resolved sign",
            )
            absences.append(record)
    need(not (curves and absences), "Round182 conflicting face normal forms")
    if curves:
        return curves[0]
    if absences:
        return absences[0]
    return {
        "kind": "UNRESOLVED",
        "raw_interval_sign": raw_sign,
        "resolved_sign": None,
        "axis": None,
        "derivative_sign": None,
        "axis_lower_sign": None,
        "axis_upper_sign": None,
        "newton_interior": None,
        "newton_image": None,
    }


def encode_round182_face_status(status: dict[str, Any]) -> str:
    """Encode a replayed face status exactly as the sealed Round182 package."""

    signs = {
        "STRICT_POSITIVE": "+",
        "STRICT_NEGATIVE": "-",
        None: "_",
    }
    kind = status["kind"]
    if kind == "STRICT":
        return "S" + signs[status["resolved_sign"]]
    if kind == "UNRESOLVED":
        return "U"
    need(kind in {"CURVE", "ABSENT"}, "known Round182 face status kind")
    return "".join([
        "C" if kind == "CURVE" else "A",
        status["axis"],
        signs[status["derivative_sign"]],
        signs[status["axis_lower_sign"]],
        signs[status["axis_upper_sign"]],
        signs[status["resolved_sign"]],
        (
            "1" if status["newton_interior"] is True
            else "0" if status["newton_interior"] is False
            else "_"
        ),
    ])


def compact_round182_face_status(status: dict[str, Any]) -> dict[str, Any]:
    return {
        field: status[field]
        for field in (
            "kind",
            "raw_interval_sign",
            "resolved_sign",
            "axis",
            "derivative_sign",
            "axis_lower_sign",
            "axis_upper_sign",
            "newton_interior",
        )
    }


def split_base(kernel: Any, box: Any, axis: str, bit: int) -> Any:
    need(axis in {"p", "s"} and bit in {0, 1}, "base split")
    if axis == "p":
        middle = (box.p0 + box.p1) / 2
        values = (
            (box.t0, box.t1, box.p0, middle, box.s0, box.s1)
            if bit == 0
            else (box.t0, box.t1, middle, box.p1, box.s0, box.s1)
        )
    else:
        middle = (box.s0 + box.s1) / 2
        values = (
            (box.t0, box.t1, box.p0, box.p1, box.s0, middle)
            if bit == 0
            else (box.t0, box.t1, box.p0, box.p1, middle, box.s1)
        )
    return kernel.r174.atlas.AtlasBox(
        *values, box.depth + 1, f"{box.path}:{axis}{bit}"
    )


def t_subbox(
    kernel: Any,
    box: Any,
    lower: Q,
    upper: Q,
    label: str,
) -> Any:
    return kernel.r174.atlas.AtlasBox(
        lower, upper, box.p0, box.p1, box.s0, box.s1,
        box.depth + 1, f"{box.path}:{label}",
    )


def base_schedule(
    kernel: Any,
    origin: dict[str, Any],
    kind: str,
    metadata: dict[str, Any],
    root: Any,
) -> tuple[str, ...]:
    strict_axes = kernel.strict_derivative_axes(
        active_dual(kernel, origin, kind, metadata, root)
    )
    axes = [axis for axis in ("p", "s") if axis in strict_axes]
    if kind == "OUTGOING" and origin["owner_target"].startswith("W["):
        axes.sort(key=lambda axis: 0 if axis == "s" else 1)
    return tuple(axes or ["p", "s"])


def find_graph_patch(
    kernel: Any,
    origin: dict[str, Any],
    kind: str,
    metadata: dict[str, Any],
    root: Any,
) -> dict[str, Any]:
    schedule = base_schedule(kernel, origin, kind, metadata, root)
    queue = deque([(root, 0, "")])
    visited = 0
    while queue:
        candidate, depth, path = queue.popleft()
        visited += 1
        lower, upper = face_signs(
            kernel, origin, kind, metadata, candidate
        )
        if {lower, upper} == STRICT_SIGNS:
            need(base_area(candidate) > 0, "positive graph base")
            return {
                "box": candidate,
                "split_depth": depth,
                "split_path": path,
                "schedule": schedule,
                "lower_sign": lower,
                "upper_sign": upper,
                "visited": visited,
            }
        if lower == upper and lower in STRICT_SIGNS:
            continue
        if depth == MAX_BASE_SPLIT_DEPTH:
            continue
        axis = schedule[depth % len(schedule)]
        for bit in (0, 1):
            queue.append((
                split_base(kernel, candidate, axis, bit),
                depth + 1,
                path + axis + str(bit),
            ))
    raise PromotionError("no positive-area monotone graph patch")


def find_corridor(
    kernel: Any,
    origin: dict[str, Any],
    kind: str,
    metadata: dict[str, Any],
    graph_box: Any,
    side: str,
    expected_sign: str,
) -> tuple[Any, int]:
    need(side in {"LOWER", "UPPER"}, "corridor side")
    width = graph_box.t1 - graph_box.t0
    for depth in range(2, MAX_CORRIDOR_DYADIC_DEPTH + 1):
        lane = width / (2 ** depth)
        lower, upper = (
            (graph_box.t0, graph_box.t0 + lane)
            if side == "LOWER"
            else (graph_box.t1 - lane, graph_box.t1)
        )
        candidate = t_subbox(
            kernel, graph_box, lower, upper,
            side.lower() + f"-corridor-{depth}",
        )
        sign = kernel.sign(
            active_dual(kernel, origin, kind, metadata, candidate)[0]
        )
        if sign == expected_sign:
            need(volume(candidate) > 0, "positive corridor")
            return candidate, depth
    raise PromotionError("graph-facing corridor search cap:" + side)


def load_r204_lineage(
    input_dir: Path,
    records: list[dict[str, Any]],
    r294: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    wanted_regions = {
        endpoint for record in records for endpoint in record["pair"]
    }
    document = read_json(input_dir / R204)
    need(
        document.get("schema")
        == "cm2.round204.source-g-wall-return-signature-local-replacement.v1"
        and document.get("result_sha256") == digest(document["result"]),
        "R204 certificate envelope",
    )
    result = document["result"]
    region_ledger = result["formal_local_open_3D_region_ledger"]
    sheet_ledger = result["formal_2D_sheet_lineage"]
    all_regions = region_ledger["rows"]
    all_sheets = sheet_ledger["target_sheet_rows"]
    need(
        region_ledger["row_count"] == len(all_regions) == 736
        and region_ledger["rows_sha256"] == digest(all_regions)
        and sheet_ledger["target_sheet_row_count"] == len(all_sheets) == 224
        and sheet_ledger["target_sheet_rows_sha256"] == digest(all_sheets),
        "R204 embedded ledger commitments",
    )
    regions: dict[str, dict[str, Any]] = {}
    for row in all_regions:
        endpoint = row["region_row_id"]
        if endpoint not in wanted_regions:
            continue
        verify_row(row, endpoint)
        registry = r294[endpoint]
        need(
            endpoint not in regions
            and registry["registry_entry_kind"] == PRESERVED_KIND
            and registry["source_occurrence_round"] == 266
            and registry["source_geometry_row_id"] == endpoint
            and registry["source_geometry_row_sha256"] == row["row_sha256"]
            and registry["support_geometry_status"]
            == "RECONSTRUCT_FROM_PINNED_SOURCE_GEOMETRY_ROW"
            and row["ambient_dimension"] == 3
            and row["strict_open_region"] is True
            and row["positive_coordinate_volume"] is True
            and row["target_graph_sheet_incident"] is True
            and row["tail_region"] is False
            and row["graph_classification"] == "FULL_2D"
            and row["target_factor_sign"] in {"NEGATIVE", "POSITIVE"}
            and row["formal_local_signature_credit"] == 1
            and row["missing_signature_field_count"] == 0
            and row["conflicting_signature_count"] == 0,
            "R204 preserved region:" + endpoint,
        )
        regions[endpoint] = row
    need(set(regions) == wanted_regions, "R204 selected region coverage")

    sheets_by_pair: dict[tuple[str, str], dict[str, Any]] = {}
    for row in all_sheets:
        pair = tuple(sorted([
            row["negative_side_region_row_id"],
            row["positive_side_region_row_id"],
        ]))
        if not set(pair) <= wanted_regions:
            continue
        verify_row(row, row["sheet_row_id"])
        need(
            pair not in sheets_by_pair
            and row["ambient_dimension"] == 2
            and row["sheet_kind"] == "TARGET_REGULAR_GRAPH_SHEET_CELL"
            and row["local_dimension_lineage_materialized"] is True
            and row["target_factor_graph_axis"] == "t"
            and row["target_t_derivative_sign"] in STRICT_SIGNS
            and row["existence_certification"]
            == B2A_FULL_2D_CERTIFICATION
            and row["existence_certification"]
            != B2A_FORBIDDEN_TAIL_CERTIFICATION
            and row["source_sign_on_leaf"] in {"NEGATIVE", "POSITIVE"}
            and Q(row["base_p_s_exact_bounds"][1])
            > Q(row["base_p_s_exact_bounds"][0])
            and Q(row["base_p_s_exact_bounds"][3])
            > Q(row["base_p_s_exact_bounds"][2])
            and row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0,
            "R204 target sheet:" + row["sheet_row_id"],
        )
        sheets_by_pair[pair] = row

    output: dict[str, dict[str, Any]] = {}
    for record in records:
        pair = record["pair"]
        need(pair in sheets_by_pair, "R300D/R204 sheet pair")
        sheet = sheets_by_pair[pair]
        negative = regions[sheet["negative_side_region_row_id"]]
        positive = regions[sheet["positive_side_region_row_id"]]
        need(
            negative["target_factor_sign"] == "NEGATIVE"
            and positive["target_factor_sign"] == "POSITIVE"
            and negative["target_sheet_row_id"]
            == positive["target_sheet_row_id"]
            == sheet["sheet_row_id"]
            and negative["leaf_row_id"]
            == positive["leaf_row_id"]
            == sheet["leaf_row_id"]
            and negative["chart"] == positive["chart"] == sheet["chart"]
            and negative["owner_target"]
            == positive["owner_target"]
            == sheet["owner_target"]
            and negative["leaf_exact_box"]
            == positive["leaf_exact_box"]
            == [
                *sheet["leaf_t_exact_bounds"],
                *sheet["base_p_s_exact_bounds"],
            ],
            "R204 negative/sheet/positive lineage:" + record["source_id"],
        )
        output[record["source_id"]] = {
            "sheet": sheet,
            "negative": negative,
            "positive": positive,
        }
    need(len(output) == len(records), "R204 sample lineage coverage")
    return output


def source_refs(
    record: dict[str, Any],
    r295: dict[str, dict[str, Any]],
    r293: dict[str, dict[str, Any]],
    r291: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    row295 = r295[record["r295_ids"][0]]
    row293 = r293[
        row295["source_Round293_R291_physical_witness_binding_row_id"]
    ]
    local = r291[record["r291_ids"][0]]
    cell = local["cells"][record["cell_indices"][0]]
    return {
        "Round291": {
            "row_id": local["row"][
                "complete_lower_stratum_local_disposition_row_id"
            ],
            "row_sha256": local["row"]["row_sha256"],
            "physical_witness_cell_index": record["cell_indices"][0],
            "physical_witness_cell": cell,
        },
        "Round293": {
            "row_id": row293[
                "Round292_R291_physical_witness_binding_row_id"
            ],
            "row_sha256": row293["row_sha256"],
            "binding_classification": row293["binding_classification"],
        },
        "Round295A": {
            "row_id": row295[
                "Round295A_R291_physical_incidence_binding_row_id"
            ],
            "row_sha256": row295["row_sha256"],
            "binding_classification":
                row295["Round295A_binding_classification"],
        },
    }


def normalized_A_definition(contract: str, sign: str) -> str:
    if contract in {
        "ROUND269_DIRECT_WHOLE_LEAF_F_SIGN_SIDE",
        "ROUND270_DIRECT_WHOLE_LEAF_F_SIGN_SIDE",
    }:
        return (
            "{x in exact pinned Round182 leaf: active_F(x) has "
            + sign + "}"
        )
    if contract == (
        "ROUND271_SINGLE_ACTIVE_FACTOR_STRICT_T_MONOTONE_WHOLE_F_SIGN_SIDE"
    ):
        return (
            "{x in exact pinned Round182 wall leaf: active target_F(x) has "
            + sign + "}"
        )
    need(
        contract == (
            "ROUND272_ONE_SIDED_SOURCE_FACTOR_TARGET_ONLY_ACTIVE_"
            "WHOLE_F_SIGN_SIDE"
        ),
        "known normalized A contract",
    )
    return (
        "{x in relative-open pinned Round182 wall leaf excluding t=0: "
        "active target_F(x) has " + sign + "}"
    )


def build_b1_row(
    *,
    record: dict[str, Any],
    r294: dict[str, dict[str, Any]],
    r295: dict[str, dict[str, Any]],
    r293: dict[str, dict[str, Any]],
    r291: dict[str, dict[str, Any]],
    leaves: dict[str, dict[str, Any]],
    collars: dict[str, dict[str, Any]],
    origins: dict[str, dict[str, Any]],
    active: dict[str, dict[str, Any]],
    kernel: Any,
    formal: bool,
) -> dict[str, Any]:
    local = r291[record["r291_ids"][0]]
    cell = local["cells"][record["cell_indices"][0]]
    leaf = leaves[record["leaf_id"]]
    origin = origins[record["origin_row_id"]]
    metadata = active[record["occurrence_row_id"]]
    root = kernel.box_from(
        cell["exact_box"],
        len(leaf["base_refinement_path"]),
        cell["leaf_row_id"],
    )
    scalar = active_dual(
        kernel, origin, record["collar_kind"], metadata, root
    )
    derivative_sign = kernel.sign(scalar[1][0])
    need(derivative_sign in STRICT_SIGNS,
         "B1 strict t derivative:" + record["source_id"])
    graph = find_graph_patch(
        kernel, origin, record["collar_kind"], metadata, root
    )
    graph_box = graph["box"]
    graph_dual = active_dual(
        kernel, origin, record["collar_kind"], metadata, graph_box
    )
    restricted_derivative_enclosure = graph_dual[1][0]
    restricted_derivative = kernel.sign(restricted_derivative_enclosure)
    lower_face = kernel.fixed_axis_face(graph_box, "t", False)
    upper_face = kernel.fixed_axis_face(graph_box, "t", True)
    lower_face_enclosure = active_dual(
        kernel, origin, record["collar_kind"], metadata, lower_face
    )[0]
    upper_face_enclosure = active_dual(
        kernel, origin, record["collar_kind"], metadata, upper_face
    )[0]
    need(restricted_derivative == derivative_sign,
         "B1 derivative restriction:" + record["source_id"])
    expected_faces = (
        ("STRICT_NEGATIVE", "STRICT_POSITIVE")
        if derivative_sign == "STRICT_POSITIVE"
        else ("STRICT_POSITIVE", "STRICT_NEGATIVE")
    )
    need(
        (graph["lower_sign"], graph["upper_sign"]) == expected_faces,
        "B1 oriented face bracket:" + record["source_id"],
    )
    t_margin = rational_domain_margin(graph_box, "t")
    p_margin = rational_domain_margin(graph_box, "p")
    need(
        t_margin > 0 and p_margin > 0,
        "B1 strict chart radicand margins:" + record["source_id"],
    )
    lower_corridor, lower_depth = find_corridor(
        kernel, origin, record["collar_kind"], metadata, graph_box,
        "LOWER", graph["lower_sign"],
    )
    upper_corridor, upper_depth = find_corridor(
        kernel, origin, record["collar_kind"], metadata, graph_box,
        "UPPER", graph["upper_sign"],
    )
    need(
        lower_corridor.t1 < upper_corridor.t0
        and volume(lower_corridor) > 0
        and volume(upper_corridor) > 0,
        "B1 disjoint positive corridors:" + record["source_id"],
    )

    round272 = any(
        bridge["connected_source_side_witness"]["connected_contract"].startswith(
            "ROUND272_"
        )
        for bridge in record["bridge_refs"].values()
    )
    inactive_source_factor: dict[str, Any] | None = None
    if record["collar_kind"] == "WALL":
        source_sign = kernel.sign(
            inactive_wall_dual(kernel, origin, metadata, root)[0]
        )
        checked_root = root
        domain = "CLOSED_R291_PHYSICAL_LEAF"
        if source_sign not in STRICT_SIGNS:
            need(
                round272 and ((root.t0 == 0) + (root.t1 == 0)) == 1,
                "only Round272 may touch source-factor zero face",
            )
            middle = (root.t0 + root.t1) / 2
            checked_root = t_subbox(
                kernel,
                root,
                middle if root.t0 == 0 else root.t0,
                root.t1 if root.t0 == 0 else middle,
                "round272-relative-open-source-check",
            )
            source_sign = kernel.sign(
                inactive_wall_dual(
                    kernel, origin, metadata, checked_root
                )[0]
            )
            domain = (
                "ROUND272_RELATIVE_OPEN_INTERIOR__EXCLUDED_t_EQUALS_0_FACE"
            )
        need(source_sign in STRICT_SIGNS,
             "B1 strict inactive wall source factor")
        corridor_checks: list[dict[str, Any]] = []
        for corridor in (lower_corridor, upper_corridor):
            checked = corridor
            sign = kernel.sign(
                inactive_wall_dual(kernel, origin, metadata, checked)[0]
            )
            check_domain = "CLOSED_CORRIDOR"
            if sign != source_sign and round272:
                need(
                    ((corridor.t0 == 0) + (corridor.t1 == 0)) == 1,
                    "Round272 corridor only zero on excluded face",
                )
                middle = (corridor.t0 + corridor.t1) / 2
                checked = t_subbox(
                    kernel,
                    corridor,
                    middle if corridor.t0 == 0 else corridor.t0,
                    corridor.t1 if corridor.t0 == 0 else middle,
                    "round272-relative-open-corridor-check",
                )
                sign = kernel.sign(
                    inactive_wall_dual(kernel, origin, metadata, checked)[0]
                )
                check_domain = "RELATIVE_OPEN_POSITIVE_VOLUME_SUBBOX"
            need(sign == source_sign,
                 "B1 corridor inactive source factor")
            corridor_checks.append({
                "checked_box": box_values(checked),
                "domain": check_domain,
                "strict_sign": sign,
            })
        inactive_source_factor = {
            "root_checked_box": box_values(checked_root),
            "domain": domain,
            "strict_sign": source_sign,
            "corridor_checks": corridor_checks,
        }

    endpoint_rows: list[dict[str, Any]] = []
    matched_sides: set[str] = set()
    normalized_contracts: list[str] = []
    for endpoint in record["pair"]:
        bridge = record["bridge_refs"][endpoint]
        registry = r294[endpoint]
        leaf_ref = bridge["Round182_leaf_reference"]
        active_ref = bridge["Round179_active_geometry_reference"]
        member_ref = record["member_refs"][endpoint]
        connected = bridge["connected_source_side_witness"]
        contract = connected["connected_contract"]
        sign = bridge["active_factor_strict_sign"]
        need(
            bridge["Round294_registry_reference"][
                "Round294_occurrence_registry_row_id"
            ] == registry["Round294_occurrence_registry_row_id"]
            and bridge["Round294_registry_reference"]["row_sha256"]
            == registry["row_sha256"]
            and bridge["Round301_member_row"]["row_id"]
            == member_ref["row_id"]
            and bridge["Round301_member_row"]["row_sha256"]
            == member_ref["row_sha256"]
            and bridge["Round301_member_row"]["component_id"]
            == member_ref["component_id"]
            and leaf_ref["Round182_leaf_row_id"] == record["leaf_id"]
            and leaf_ref["exact_leaf_box"] == leaf["box"]
            and active_ref["Round179_active_normal_form_row_id"]
            == record["occurrence_row_id"]
            and active_ref["Round179_origin_row_id"] == record["origin_row_id"]
            and active_ref["source_chart"] == record["source_chart"]
            and active_ref["owner_target"] == record["owner_target"]
            and bridge["active_factor_equation"] == record["active_equation"]
            and connected["formal_connected_source_signed_region_definition"]
            == normalized_A_definition(contract, sign)
            and (
                connected["relative_open_excluded_face"] == "t=0"
                if contract.startswith("ROUND272_")
                else connected["relative_open_excluded_face"] is None
            )
            and all(
                reference["connected_contract"] == contract
                and reference["active_factor_strict_sign"] == sign
                and reference["connected_side_extension_materialized"] is True
                and reference["formal_connected_source_signed_region_id"]
                == connected["formal_connected_source_signed_region_id"]
                for reference in bridge["source_side_row_references"]
            ),
            "B1 endpoint provenance:" + endpoint,
        )
        anchor = kernel.box_from(
            bridge["anchor_box"], 0, "Round303A-anchor:" + endpoint
        )
        need(
            volume(anchor) > 0
            and contains(root, anchor)
            and kernel.sign(
                active_dual(
                    kernel, origin, record["collar_kind"], metadata, anchor
                )[0]
            ) == sign,
            "B1 bridge anchor replay:" + endpoint,
        )
        matched = (
            "LOWER_GRAPH_SIDE"
            if sign == graph["lower_sign"]
            else "UPPER_GRAPH_SIDE"
            if sign == graph["upper_sign"]
            else "NO_MATCH"
        )
        need(matched != "NO_MATCH", "B1 bridge/corridor sign:" + endpoint)
        matched_sides.add(matched)
        normalized_contracts.append(contract)
        endpoint_rows.append({
            "registry_occurrence_id": endpoint,
            "Round294_registry_row_id":
                registry["Round294_occurrence_registry_row_id"],
            "Round294_registry_row_sha256": registry["row_sha256"],
            "Round301_member_reference": member_ref,
            "Round303A_bridge_row_id": bridge["row_id"],
            "Round303A_bridge_row_sha256": bridge["row_sha256"],
            "Round303A_theorem_id": bridge["theorem_id"],
            "Round303A_theorem_sha256": bridge["theorem_sha256"],
            "strict_anchor_box": bridge["anchor_box"],
            "active_factor_strict_sign": sign,
            "normalized_A_contract": contract,
            "normalized_A_definition":
                normalized_A_definition(contract, sign),
            "connected_source_side_witness": connected,
            "matched_graph_side": matched,
            "local_graph_sign_side_subset_normalized_A": True,
            "closure_attachment_to_Gamma": {
                "theorem_id": MONOTONE_LIMIT_THEOREM_ID,
                "theorem_sha256": MONOTONE_LIMIT_THEOREM_SHA256,
                "Gamma_subset_closure_of_this_local_sign_side": True,
                "local_sign_side_subset_normalized_A": True,
                "therefore_Gamma_subset_closure_of_normalized_A": True,
            },
        })
    need(
        matched_sides == {"LOWER_GRAPH_SIDE", "UPPER_GRAPH_SIDE"},
        "B1 endpoints occupy opposite sides:" + record["source_id"],
    )
    if round272:
        need(
            all(contract.startswith("ROUND272_")
                for contract in normalized_contracts)
            and ((root.t0 == 0) + (root.t1 == 0)) == 1,
            "B1 Round272 one-sided normalized domains",
        )
        excluded_face_sign = (
            graph["lower_sign"] if graph_box.t0 == 0
            else graph["upper_sign"]
        )
        need(
            excluded_face_sign in STRICT_SIGNS,
            "B1 Round272 Gamma misses excluded t=0 face",
        )
    else:
        excluded_face_sign = None

    payload = {
        "schema": SCHEMA + ".b1-lemma-row.v1",
        "proof_path": "B1_MONOTONE_GRAPH_TWO_CONNECTED_SIDE_ATTACHMENTS",
        "theorem_id": B1_THEOREM_ID,
        "theorem_sha256": B1_LAYER_THEOREM_SHA256,
        "gluing_theorem_id": THEOREM_ID,
        "gluing_theorem_sha256": THEOREM_SHA256,
        "monotone_limit_theorem": MONOTONE_LIMIT_THEOREM,
        "monotone_limit_theorem_sha256":
            MONOTONE_LIMIT_THEOREM_SHA256,
        "source_Round300D_row_id": record["source_id"],
        "source_Round300D_row_sha256": record["source_sha256"],
        "source_Round301_ineligible_reference":
            record["r301_ineligible_ref"],
        "canonical_endpoint_pair": list(record["pair"]),
        "endpoint_connected_side_rows": endpoint_rows,
        "physical_inclusion_chain": source_refs(
            record, r295, r293, r291
        ),
        "Gamma": {
            "kind": "UNIQUE_MONOTONE_TARGET_GRAPH_OVER_POSITIVE_RATIONAL_BASE",
            "exact_active_scalar_equation": record["active_equation"],
            "Round182_leaf_row_id": record["leaf_id"],
            "root_physical_leaf_box": box_values(root),
            "positive_base_graph_prism": box_values(graph_box),
            "exact_positive_base_area": qstr(base_area(graph_box)),
            "base_split_schedule": list(graph["schedule"]),
            "base_split_path": graph["split_path"],
            "base_split_depth": graph["split_depth"],
            "strict_t_derivative_sign": derivative_sign,
            "strict_t_derivative_enclosure":
                str(restricted_derivative_enclosure),
            "lower_face_active_sign": graph["lower_sign"],
            "lower_face_active_enclosure": str(lower_face_enclosure),
            "upper_face_active_sign": graph["upper_sign"],
            "upper_face_active_enclosure": str(upper_face_enclosure),
            "exact_chart_radicand_margins": {
                "one_minus_t_squared_margin": qstr(t_margin),
                "one_minus_p_squared_margin": qstr(p_margin),
                "both_strictly_positive": True,
            },
            "active_scalar_continuous_on_D": True,
            "unique_zero_graph_by_strict_monotonicity_and_IVT": True,
            "connected": True,
            "nonempty": True,
            "included_by_R291_R293_R295A_physical_chain": True,
            "Round272_excluded_t0_face_active_sign":
                excluded_face_sign,
            "Round272_Gamma_misses_excluded_t0_face":
                True if round272 else None,
            "relative_domain": (
                "ROUND272_RELATIVE_OPEN_LEAF_EXCLUDING_t=0"
                if round272 else "CLOSED_EXACT_GRAPH_PRISM"
            ),
        },
        "local_side_nonempty_witnesses": {
            "lower_graph_facing_corridor_box":
                box_values(lower_corridor),
            "lower_corridor_dyadic_depth": lower_depth,
            "lower_corridor_active_sign": graph["lower_sign"],
            "upper_graph_facing_corridor_box":
                box_values(upper_corridor),
            "upper_corridor_dyadic_depth": upper_depth,
            "upper_corridor_active_sign": graph["upper_sign"],
            "both_positive_volume": True,
            "corridor_intersects_Gamma_claimed": False,
            "corridor_used_as_attachment_witness": False,
        },
        "two_sided_limit_attachment": {
            "left_local_sign_side_subset_normalized_A": True,
            "right_local_sign_side_subset_normalized_A": True,
            "Gamma_subset_closure_of_left_local_sign_side": True,
            "Gamma_subset_closure_of_right_local_sign_side": True,
            "Gamma_subset_closure_of_both_normalized_A_sides": True,
            "proof_source": MONOTONE_LIMIT_THEOREM_ID,
            "corridor_box_closure_meets_Gamma": False,
        },
        "inactive_wall_source_factor_replay": inactive_source_factor,
        "B1_predicates": {
            "B1_P0_exact_scope_and_physical_binding_join": True,
            "B1_P1_two_complete_connected_A_bridges": True,
            "B1_P2_exact_chart_and_inactive_factor_domain": True,
            "B1_P3_positive_base_strict_monotone_bracket": True,
            "B1_P4_Gamma_same_included_R291_sheet_patch": True,
            "B1_P5_left_local_side_subset_A_and_limit_attachment": True,
            "B1_P6_right_local_side_subset_A_and_limit_attachment": True,
            "B1_P7_endpoint_patch_provenance_exactly_closed": True,
        },
        "limit_theorem_predicates": {
            "L0_exact_relative_domain": True,
            "L1_continuous_active_scalar": True,
            "L2_strict_t_monotonicity": True,
            "L3_uniform_opposite_face_signs": True,
            "L4_exact_included_Gamma_binding": True,
            "L5_complete_connected_sign_sides": True,
            "L6_endpoint_opposite_sign_bijection": True,
        },
        "G0_exact_provenance_pins_and_row_closures": True,
        "G1_endpoint_occurrence_connected_supports": True,
        "G2_nonempty_connected_included_lower_stratum": True,
        "G3_left_closure_attaches_to_included_patch": True,
        "G4_right_closure_attaches_to_included_patch": True,
        "G5_endpoint_patch_provenance_exactly_closed": True,
        "candidate_B1_lemma_conclusion": True,
        "formal_B1_attachment_lemma_credit": 1 if formal else 0,
        "formal_component_edge_credit": 0,
        **{field: 0 for field in ZERO_FIELDS},
    }
    return close_row(
        "Round303B_B1_attachment_lemma_row_id",
        "round303b-b1-attachment-lemma:",
        B1_THEOREM_ID,
        payload,
    )


def b2_exact_join_payloads(
    *,
    record: dict[str, Any],
    lineage: dict[str, Any],
    r291: dict[str, dict[str, Any]],
    leaves: dict[str, dict[str, Any]],
    collars: dict[str, dict[str, Any]],
    origins: dict[str, dict[str, Any]],
    active: dict[str, dict[str, Any]],
    kernel: Any,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Prove the concrete R182 target-sheet/R204/R291 identity join."""

    sheet = lineage["sheet"]
    negative = lineage["negative"]
    positive = lineage["positive"]
    local = r291[record["r291_ids"][0]]
    cell_index = record["cell_indices"][0]
    cell = local["cells"][cell_index]
    leaf = leaves[cell["leaf_row_id"]]
    collar = collars[leaf["occurrence_row_id"]]
    origin = origins[collar["origin_row_id"]]
    active_row = active[leaf["occurrence_row_id"]]
    sheet_box = [
        *sheet["leaf_t_exact_bounds"],
        *sheet["base_p_s_exact_bounds"],
    ]
    sheet_base_area = (
        (
            Q(sheet["base_p_s_exact_bounds"][1])
            - Q(sheet["base_p_s_exact_bounds"][0])
        )
        * (
            Q(sheet["base_p_s_exact_bounds"][3])
            - Q(sheet["base_p_s_exact_bounds"][2])
        )
    )
    wall_axis = sheet["wall_axis"]
    integer_wall = sheet["integer_wall"]
    coordinate = wall_axis.lower()
    source_factor_scalar = f"source_{coordinate}-{integer_wall}"
    target_factor_scalar = f"target_{coordinate}-{integer_wall}"
    source_factor_equation = f"({source_factor_scalar})=0"
    target_factor_equation = f"({target_factor_scalar})=0"
    product_equation = (
        f"({source_factor_scalar})*({target_factor_scalar})=0"
    )
    selector_coordinate = "hit_x" if wall_axis == "X" else "hit_y"
    target_selector_scalar = f"{selector_coordinate}-{integer_wall}"
    root = kernel.box_from(
        sheet_box,
        len(leaf["base_refinement_path"]),
        leaf["row_id"],
    )
    selector_dual = active_dual(
        kernel, origin, "WALL", active_row, root
    )
    replayed_derivative_sign = kernel.sign(selector_dual[1][0])
    lower_face_status = round182_face_status(
        kernel, origin, active_row, root, False
    )
    upper_face_status = round182_face_status(
        kernel, origin, active_row, root, True
    )
    encoded_face_statuses = (
        encode_round182_face_status(lower_face_status),
        encode_round182_face_status(upper_face_status),
    )
    raw_face_interval_signs = (
        lower_face_status["raw_interval_sign"],
        upper_face_status["raw_interval_sign"],
    )
    replayed_face_signs = (
        lower_face_status["resolved_sign"],
        upper_face_status["resolved_sign"],
    )
    expected_face_signs = (
        ("STRICT_NEGATIVE", "STRICT_POSITIVE")
        if replayed_derivative_sign == "STRICT_POSITIVE"
        else ("STRICT_POSITIVE", "STRICT_NEGATIVE")
    )
    need(
        local["row"]["local_disposition"] == "WHOLE_PHYSICAL_SUPPORT"
        and local["row"]["representation_role"]
        == "DIRECT_GRAPH_SHEET_WITNESS"
        and local["row"]["absence_witness_cell_count"] == 0
        and local["row"]["absence_witness_cells"] == []
        and cell["witness_kind"] == "ROUND182_GRAPH_SHEET_LEAF"
        and cell["graph_classification"] == "FULL_2D"
        and leaf["graph_classification"] == "FULL_2D"
        and negative["graph_classification"] == "FULL_2D"
        and positive["graph_classification"] == "FULL_2D"
        and cell["leaf_row_id"] == sheet["leaf_row_id"] == leaf["row_id"]
        and cell["retained_child_row_id"]
        == leaf["retained_child_row_id"]
        == negative["retained_child_row_id"]
        == positive["retained_child_row_id"]
        and cell["exact_box"]
        == sheet_box
        == leaf["box"]
        == negative["leaf_exact_box"]
        == positive["leaf_exact_box"]
        and Q(cell["base_coordinate_area"])
        == Q(leaf["base_coordinate_area"])
        == sheet_base_area > 0
        and local["row"]["source_chart"]
        == sheet["chart"]
        == negative["chart"]
        == positive["chart"]
        == collar["chart"]
        == origin["chart"]
        == active_row["chart"]
        and sheet["owner_target"]
        == negative["owner_target"]
        == positive["owner_target"]
        == collar["owner_target"]
        == origin["owner_target"]
        and sheet["origin_row_id"]
        == negative["origin_row_id"]
        == positive["origin_row_id"]
        == collar["origin_row_id"]
        == origin["origin_row_id"]
        == active_row["origin_row_id"]
        and sheet["parent_id"]
        == negative["parent_id"]
        == positive["parent_id"]
        == collar["parent_id"]
        == origin["parent_id"]
        == active_row["parent_id"]
        == local["row"]["parent_id"]
        and negative["occurrence_row_id"]
        == positive["occurrence_row_id"]
        == leaf["occurrence_row_id"]
        == collar["Round179_occurrence_row_id"]
        == active_row["row_id"]
        == local["row"]["canonical_support_row_id"]
        and negative["Round182_leaf_packed_sha256"]
        == positive["Round182_leaf_packed_sha256"]
        and sheet["wall_axis"]
        == negative["wall_axis"]
        == positive["wall_axis"]
        == active_row["axis"]
        and sheet["integer_wall"]
        == negative["integer_wall"]
        == positive["integer_wall"]
        == active_row["integer_wall"]
        and local["row"]["predicate_equation"]
        == collar["equation"]
        == active_row["zero_equation"]
        == product_equation
        and collar["reason_label"] == active_row["reason_label"]
        and collar["kind"] == "WALL"
        and active_row["target_factor_classification"] == "REGULAR_GRAPH"
        and active_row["target_gradient_axis"]
        == sheet["target_factor_graph_axis"]
        == "t"
        and active_row["target_gradient_sign"]
        == collar["strict_t_derivative_sign"]
        == sheet["target_t_derivative_sign"]
        == replayed_derivative_sign
        and replayed_derivative_sign in STRICT_SIGNS
        and all(sign in STRICT_SIGNS for sign in replayed_face_signs)
        and replayed_face_signs == expected_face_signs
        and leaf["lower_t_face_status"]
        == encoded_face_statuses[0]
        and leaf["upper_t_face_status"]
        == encoded_face_statuses[1]
        and leaf["two_dimensional_graph_sheet_count"] == 1
        and sheet["source_sign_on_leaf"] in {"NEGATIVE", "POSITIVE"},
        "B2 exact target-selector/owner/leaf provenance:"
        + record["source_id"],
    )
    common = {
        "Round182_target_factor_sheet_theorem_id":
            R182_TARGET_FACTOR_SHEET_THEOREM_ID,
        "Round182_target_factor_sheet_theorem_sha256":
            R182_TARGET_FACTOR_SHEET_THEOREM_SHA256,
        "Round204_sheet_leaf_row_id": sheet["leaf_row_id"],
        "Round204_sheet_chart": sheet["chart"],
        "Round204_sheet_owner_target": sheet["owner_target"],
        "Round204_sheet_origin_row_id": sheet["origin_row_id"],
        "Round204_sheet_exact_box": sheet_box,
        "Round204_sheet_base_coordinate_area": qstr(sheet_base_area),
        "Round204_target_factor_equation": target_factor_equation,
        "Round182_collar_row_id": collar["row_id"],
        "Round182_leaf_row_id": leaf["row_id"],
        "Round182_leaf_graph_classification":
            leaf["graph_classification"],
        "Round182_leaf_base_coordinate_area":
            leaf["base_coordinate_area"],
        "Round182_WALL_geometry_selector": target_selector_scalar,
        "Round182_WALL_geometry_selector_source":
            "independent_geometry." + selector_coordinate,
        "Round182_replayed_target_t_derivative_sign":
            replayed_derivative_sign,
        "Round182_raw_lower_t_face_interval_sign":
            raw_face_interval_signs[0],
        "Round182_raw_upper_t_face_interval_sign":
            raw_face_interval_signs[1],
        "Round182_replayed_lower_t_face_encoded_status":
            encoded_face_statuses[0],
        "Round182_replayed_upper_t_face_encoded_status":
            encoded_face_statuses[1],
        "Round182_replayed_lower_t_face_certificate":
            compact_round182_face_status(lower_face_status),
        "Round182_replayed_upper_t_face_certificate":
            compact_round182_face_status(upper_face_status),
        "Round182_serialized_lower_t_face_status":
            leaf["lower_t_face_status"],
        "Round182_serialized_upper_t_face_status":
            leaf["upper_t_face_status"],
        "Round182_replayed_lower_t_face_sign":
            replayed_face_signs[0],
        "Round182_replayed_upper_t_face_sign":
            replayed_face_signs[1],
        "Round182_FULL_2D_unique_target_graph_checked": True,
        "Round179_active_row_id": active_row["row_id"],
        "Round179_nominal_product_lineage_equation": product_equation,
        "Round179_source_factor_equation": source_factor_equation,
        "Round179_target_factor_equation": target_factor_equation,
        "Round179_target_factor_classification":
            active_row["target_factor_classification"],
        "Round179_target_gradient_axis":
            active_row["target_gradient_axis"],
        "Round179_target_gradient_sign":
            active_row["target_gradient_sign"],
        "active_factor_semantic_mapping":
            "ROUND204_TARGET_FACTOR_IS_ROUND182_WALL_TARGET_SELECTOR",
        "Round204_half_open_source_sign_on_leaf":
            sheet["source_sign_on_leaf"],
        "source_sign_join_role":
            "INFORMATIONAL_HALF_OPEN_STRENGTHENING_NOT_LOGICAL_BRIDGE",
        "nominal_product_lineage_compatibility_checked": True,
        "nominal_product_equation_used_as_sheet_identity": False,
        "product_zero_iff_target_zero_claimed": False,
        "closed_leaf_source_factor_strict_nonzero_required": False,
        "exact_owner_leaf_chart_box_base_area_join_checked": True,
        "exact_active_factor_provenance_mapping_checked": True,
    }
    b2b = {
        **common,
        "Round291_local_disposition_row_id": local["row"][
            "complete_lower_stratum_local_disposition_row_id"
        ],
        "Round291_local_disposition_row_sha256":
            local["row"]["row_sha256"],
        "Round291_physical_witness_cell_index": cell_index,
        "Round291_physical_witness_leaf_row_id": cell["leaf_row_id"],
        "Round291_physical_witness_graph_classification":
            cell["graph_classification"],
        "Round291_physical_witness_exact_box": cell["exact_box"],
        "Round291_physical_witness_base_coordinate_area":
            cell["base_coordinate_area"],
        "Round291_nominal_predicate_product_equation":
            local["row"]["predicate_equation"],
        "Round291_representation_role":
            local["row"]["representation_role"],
        "Round291_local_disposition":
            local["row"]["local_disposition"],
        "Round204_sheet_and_R291_witness_same_leaf": True,
        "Round204_sheet_and_R291_witness_same_exact_box": True,
        "Round204_sheet_and_R291_witness_same_chart": True,
        "Round204_sheet_and_R291_witness_same_owner_target": True,
        "Round204_sheet_and_R291_witness_same_base_area": True,
        "Round204_Gamma_equals_Round182_target_factor_graph": True,
        "Round291_DIRECT_witness_carries_same_Round182_target_sheet": True,
        "Round293_and_Round295A_bind_same_two_Round294_occurrences": True,
        "Gamma_included_via_R291_DIRECT_target_sheet_witness": True,
    }
    return common, b2b


def build_b2_rows(
    *,
    record: dict[str, Any],
    lineage: dict[str, Any],
    r294: dict[str, dict[str, Any]],
    r295: dict[str, dict[str, Any]],
    r293: dict[str, dict[str, Any]],
    r291: dict[str, dict[str, Any]],
    leaves: dict[str, dict[str, Any]],
    collars: dict[str, dict[str, Any]],
    origins: dict[str, dict[str, Any]],
    active: dict[str, dict[str, Any]],
    kernel: Any,
    formal: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    sheet = lineage["sheet"]
    negative = lineage["negative"]
    positive = lineage["positive"]
    local = r291[record["r291_ids"][0]]
    cell = local["cells"][record["cell_indices"][0]]
    leaf = leaves[cell["leaf_row_id"]]
    sheet_leaf_box = [
        *sheet["leaf_t_exact_bounds"],
        *sheet["base_p_s_exact_bounds"],
    ]
    need(
        cell["graph_classification"] == "FULL_2D"
        and leaf["graph_classification"] == "FULL_2D"
        and cell["leaf_row_id"] == sheet["leaf_row_id"] == leaf["row_id"]
        and cell["exact_box"] == sheet_leaf_box == leaf["box"]
        and local["row"]["source_chart"] == sheet["chart"]
        and Q(cell["base_coordinate_area"])
        == (
            (Q(sheet["base_p_s_exact_bounds"][1])
             - Q(sheet["base_p_s_exact_bounds"][0]))
            * (Q(sheet["base_p_s_exact_bounds"][3])
               - Q(sheet["base_p_s_exact_bounds"][2]))
        ) > 0,
        "B2 R204/R291 exact physical sheet join:" + record["source_id"],
    )
    b2a_exact_join, b2b_exact_join = b2_exact_join_payloads(
        record=record,
        lineage=lineage,
        r291=r291,
        leaves=leaves,
        collars=collars,
        origins=origins,
        active=active,
        kernel=kernel,
    )
    endpoint_rows = []
    for endpoint in record["pair"]:
        region = (
            negative if endpoint == negative["region_row_id"] else positive
        )
        registry = r294[endpoint]
        member = record["member_refs"][endpoint]
        need(
            region["region_row_id"] == endpoint
            and registry["source_geometry_row_id"] == endpoint
            and registry["source_geometry_row_sha256"] == region["row_sha256"]
            and member["official_key_id"] == registry["official_key_id"],
            "B2 endpoint/R204/R294/R301 join:" + endpoint,
        )
        endpoint_rows.append({
            "registry_occurrence_id": endpoint,
            "Round204_region_row_id": region["region_row_id"],
            "Round204_region_row_sha256": region["row_sha256"],
            "target_factor_sign": region["target_factor_sign"],
            "Round294_registry_row_id":
                registry["Round294_occurrence_registry_row_id"],
            "Round294_registry_row_sha256": registry["row_sha256"],
            "Round301_member_reference": member,
        })

    b2a_payload = {
        "schema": SCHEMA + ".b2a-analytic-lemma-row.v1",
        "proof_path": "B2A_R204_ANALYTIC_TARGET_GRAPH_SHEET",
        "theorem_id": B2A_THEOREM_ID,
        "theorem_sha256": B2A_LAYER_THEOREM_SHA256,
        "source_Round300D_row_id": record["source_id"],
        "source_Round300D_row_sha256": record["source_sha256"],
        "canonical_endpoint_pair": list(record["pair"]),
        "Round204_target_sheet_reference": {
            "sheet_row_id": sheet["sheet_row_id"],
            "row_sha256": sheet["row_sha256"],
            "leaf_row_id": sheet["leaf_row_id"],
            "chart": sheet["chart"],
            "owner_target": sheet["owner_target"],
            "leaf_t_exact_bounds": sheet["leaf_t_exact_bounds"],
            "base_p_s_exact_bounds": sheet["base_p_s_exact_bounds"],
            "target_t_derivative_sign":
                sheet["target_t_derivative_sign"],
            "existence_certification": sheet["existence_certification"],
        },
        "endpoint_open_region_references": endpoint_rows,
        "exact_join": b2a_exact_join,
        "analytic_conclusion": {
            "Gamma_nonempty": True,
            "Gamma_unique_graph_over_connected_positive_area_base": True,
            "Gamma_connected": True,
            "physical_inclusion_claimed_at_B2a": False,
        },
        "candidate_B2a_analytic_lemma_conclusion": True,
        "formal_B2a_analytic_lemma_credit": 1 if formal else 0,
        "formal_component_edge_credit": 0,
        **{field: 0 for field in ZERO_FIELDS},
    }
    b2a = close_row(
        "Round303B_B2a_analytic_sheet_lemma_row_id",
        "round303b-b2a-analytic-sheet-lemma:",
        B2A_THEOREM_ID,
        b2a_payload,
    )
    b2b_payload = {
        "schema": SCHEMA + ".b2b-inclusion-lemma-row.v1",
        "proof_path": "B2B_R291_R293_R295A_PHYSICAL_SHEET_INCLUSION",
        "theorem_id": B2B_THEOREM_ID,
        "theorem_sha256": B2B_LAYER_THEOREM_SHA256,
        "Round182_target_factor_sheet_theorem_id":
            R182_TARGET_FACTOR_SHEET_THEOREM_ID,
        "Round182_target_factor_sheet_theorem_sha256":
            R182_TARGET_FACTOR_SHEET_THEOREM_SHA256,
        "source_B2a_row_id":
            b2a["Round303B_B2a_analytic_sheet_lemma_row_id"],
        "source_B2a_row_sha256": b2a["row_sha256"],
        "source_Round300D_row_id": record["source_id"],
        "source_Round300D_row_sha256": record["source_sha256"],
        "canonical_endpoint_pair": list(record["pair"]),
        "Round204_target_sheet_row_id": sheet["sheet_row_id"],
        "Round204_target_sheet_row_sha256": sheet["row_sha256"],
        "physical_inclusion_chain": source_refs(
            record, r295, r293, r291
        ),
        "exact_join": b2b_exact_join,
        "candidate_B2b_inclusion_lemma_conclusion": True,
        "formal_B2b_physical_inclusion_lemma_credit": 1 if formal else 0,
        "formal_component_edge_credit": 0,
        **{field: 0 for field in ZERO_FIELDS},
    }
    b2b = close_row(
        "Round303B_B2b_physical_inclusion_lemma_row_id",
        "round303b-b2b-physical-inclusion-lemma:",
        B2B_THEOREM_ID,
        b2b_payload,
    )
    return b2a, b2b


def build_edge_row(
    *,
    record: dict[str, Any],
    proof_path: str,
    lemma_rows: list[dict[str, Any]],
    formal: bool,
) -> dict[str, Any]:
    need(proof_path in {"B1", "B2"}, "edge proof path")
    expected_fields = (
        ["Round303B_B1_attachment_lemma_row_id"]
        if proof_path == "B1"
        else [
            "Round303B_B2a_analytic_sheet_lemma_row_id",
            "Round303B_B2b_physical_inclusion_lemma_row_id",
        ]
    )
    need(
        len(lemma_rows) == len(expected_fields)
        and all(field in row for field, row in zip(expected_fields, lemma_rows)),
        "edge lemma arity",
    )
    refs = [
        {
            "row_id": row[field],
            "row_sha256": row["row_sha256"],
        }
        for field, row in zip(expected_fields, lemma_rows)
    ]
    payload = {
        "schema": SCHEMA + ".component-edge-row.v1",
        "theorem_id": THEOREM_ID,
        "theorem_sha256": THEOREM_SHA256,
        "proof_path": (
            "B1_MONOTONE_GRAPH_SIDE_ATTACHMENT"
            if proof_path == "B1"
            else "B2_R204_ANALYTIC_PLUS_R291_PHYSICAL_INCLUSION"
        ),
        "source_Round300D_row_id": record["source_id"],
        "source_Round300D_row_sha256": record["source_sha256"],
        "source_Round301_ineligible_reference":
            record["r301_ineligible_ref"],
        "canonical_unordered_registry_occurrence_ids":
            list(record["pair"]),
        "source_lemma_references": refs,
        "Round301_pre_edge_components": {
            endpoint: record["member_refs"][endpoint]["component_id"]
            for endpoint in record["pair"]
        },
        "official_key_metadata": {
            endpoint: record["endpoint_refs"][endpoint]["official_key_id"]
            for endpoint in record["pair"]
        },
        "G0_exact_provenance_pins_and_row_closures": True,
        "G1_endpoint_occurrence_connected_supports": True,
        "G2_nonempty_connected_included_lower_stratum": True,
        "G3_left_closure_attaches_to_included_patch": True,
        "G4_right_closure_attaches_to_included_patch": True,
        "G5_endpoint_patch_provenance_exactly_closed": True,
        "candidate_component_connectivity_conclusion": True,
        "formal_component_edge_credit": 1 if formal else 0,
        "eligible_for_later_fresh_DSU_application": formal,
        "old_63224_component_result_reused": False,
        "Round301_DSU_mutated_here": False,
        **{field: 0 for field in ZERO_FIELDS},
    }
    return close_row(
        "Round303B_component_connectivity_edge_row_id",
        "round303b-component-connectivity-edge:",
        THEOREM_ID,
        payload,
    )


def build_unresolved_row(record: dict[str, Any]) -> dict[str, Any]:
    refs = [
        record["unresolved_refs"][endpoint]
        for endpoint in record["pair"]
    ]
    need(
        all(ref["disposition"]
            == "UNRESOLVED__W_TAIL_CONNECTED_SOURCE_SIDE_EXTENSION_MISSING"
            for ref in refs),
        "W-tail unresolved-only input",
    )
    payload = {
        "schema": SCHEMA + ".wtail-unresolved-row.v1",
        "source_Round300D_row_id": record["source_id"],
        "source_Round300D_row_sha256": record["source_sha256"],
        "source_Round301_ineligible_reference":
            record["r301_ineligible_ref"],
        "canonical_unordered_registry_occurrence_ids":
            list(record["pair"]),
        "Round303A_unresolved_endpoint_references": [
            {
                "endpoint": ref["endpoint"],
                "row_id": ref["row_id"],
                "row_sha256": ref["row_sha256"],
                "missing_obligation": ref["missing_obligation"],
            }
            for ref in refs
        ],
        "disposition": WT_DISPOSITION,
        "formal_component_edge_credit": 0,
        "nonedge_credit": 0,
        "exclusion_credit": 0,
        "eligible_for_later_fresh_DSU_application": False,
        **{field: 0 for field in ZERO_FIELDS},
    }
    return close_row(
        "Round303B_W_tail_unresolved_row_id",
        "round303b-wtail-unresolved:",
        "ROUND303B_WTAIL_UNRESOLVED_V1",
        payload,
    )


def write_ledger(
    path: Path,
    rows_path: Path,
    table_name: str,
    schema: str,
    commitment: dict[str, Any],
    status: str,
) -> None:
    document: dict[str, Any] = {
        "every_row_closed_by_own_SHA256": True,
        "row_count": commitment["row_count"],
        "row_hashes_sha256": commitment["row_hashes_sha256"],
        "row_ids_sha256": commitment["row_ids_sha256"],
        "rows_sha256": commitment["rows_sha256"],
        "schema": schema,
        "status": status,
        table_name: None,
    }
    with path.open("wb") as raw:
        with gzip.GzipFile(
            filename="", fileobj=raw, mode="wb", mtime=0, compresslevel=9
        ) as stream:
            stream.write(b"{")
            first = True
            for key in sorted(document):
                if not first:
                    stream.write(b",")
                first = False
                stream.write(canonical(key) + b":")
                if key != table_name:
                    stream.write(canonical(document[key]))
                    continue
                stream.write(b"[")
                first_row = True
                with rows_path.open("rb") as rows:
                    for raw_row in rows:
                        if not first_row:
                            stream.write(b",")
                        first_row = False
                        stream.write(raw_row.rstrip(b"\n"))
                stream.write(b"]")
            stream.write(b"}")
        raw.flush()
        os.fsync(raw.fileno())


def finalize_result(result: dict[str, Any]) -> bytes:
    value = dict(result)
    value["result_sha256"] = ""
    payload = dict(value)
    payload.pop("result_sha256")
    value["result_sha256"] = digest(payload)
    return canonical(value) + b"\n"


def publish_exclusive(staged: Path, target: Path) -> None:
    """Publish one staged file without ever replacing an existing path."""

    with staged.open("rb") as stream:
        os.fsync(stream.fileno())
    try:
        os.link(staged, target, follow_symlinks=False)
    except FileExistsError as exc:
        raise PromotionError(
            "formal output target raced or already exists:" + target.name
        ) from exc
    staged.unlink()


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def confined_output_target(target: Path) -> None:
    need(
        target.parent.resolve() == HERE.resolve(),
        "output confinement:" + target.name,
    )


def read_existing_output(
    target: Path,
    label: str,
) -> tuple[str, int, tuple[int, ...]]:
    """O_NOFOLLOW-read and snapshot one pre-existing formal output."""

    confined_output_target(target)
    need(os.path.lexists(target), "existing output missing:" + label)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(target, flags)
    except OSError as exc:
        raise PromotionError("unsafe existing output:" + label) from exc
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode)
            and before.st_nlink == 1
            and before.st_size > 0,
            "existing output regular-single-link:" + label,
        )
        state = hashlib.sha256()
        size = 0
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            state.update(block)
            size += len(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    snapshot = (
        after.st_dev,
        after.st_ino,
        after.st_mode,
        after.st_nlink,
        after.st_uid,
        after.st_gid,
        after.st_size,
        after.st_mtime_ns,
        after.st_ctime_ns,
    )
    path_info = os.stat(target, follow_symlinks=False)
    need(
        before.st_dev == after.st_dev == path_info.st_dev
        and before.st_ino == after.st_ino == path_info.st_ino
        and before.st_size == after.st_size == path_info.st_size == size
        and after.st_nlink == path_info.st_nlink == 1,
        "existing output stable snapshot:" + label,
    )
    return state.hexdigest(), size, snapshot


def existing_output_equals_stage(
    target: Path,
    staged: Path,
    label: str,
) -> tuple[int, ...]:
    expected_hash = file_sha256(staged)
    expected_size = staged.stat().st_size
    actual_hash, actual_size, snapshot = read_existing_output(target, label)
    need(
        actual_hash == expected_hash and actual_size == expected_size,
        "existing output exact hash/size:" + label,
    )
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(target, flags)
    try:
        with staged.open("rb") as expected:
            while True:
                actual_block = os.read(descriptor, 1 << 20)
                expected_block = expected.read(1 << 20)
                need(
                    actual_block == expected_block,
                    "existing output exact bytes:" + label,
                )
                if not actual_block:
                    break
    finally:
        os.close(descriptor)
    return snapshot


def commit_formal_package(
    staged_ledgers: dict[str, Path],
    staged_result: Path,
) -> None:
    """No-clobber publication with result as the sole commit marker."""

    ledger_targets = {
        key: HERE / OUTPUT_NAMES[key]
        for key in staged_ledgers
    }
    result_target = HERE / OUTPUT_NAMES["result"]
    for target in [*ledger_targets.values(), result_target]:
        confined_output_target(target)

    if os.path.lexists(result_target):
        existing_output_equals_stage(
            result_target, staged_result, "idempotent-result"
        )
        for key, target in ledger_targets.items():
            need(
                os.path.lexists(target),
                "committed package ledger missing:" + target.name,
            )
            existing_output_equals_stage(
                target, staged_ledgers[key], "idempotent-" + key
            )
        return

    reusable: set[str] = set()
    for key, target in ledger_targets.items():
        if not os.path.lexists(target):
            continue
        existing_output_equals_stage(
            target, staged_ledgers[key], "crash-recovery-" + key
        )
        reusable.add(key)

    fsync_directory(staged_result.parent)
    expected = {
        key: (
            file_sha256(staged_ledgers[key]),
            staged_ledgers[key].stat().st_size,
        )
        for key in staged_ledgers
    }
    for key, target in ledger_targets.items():
        if key in reusable:
            continue
        publish_exclusive(staged_ledgers[key], target)

    snapshots: dict[str, tuple[int, ...]] = {}
    for key, target in ledger_targets.items():
        actual_hash, actual_size, snapshot = read_existing_output(
            target, "precommit-" + key
        )
        need(
            (actual_hash, actual_size) == expected[key],
            "precommit ledger rehash:" + key,
        )
        snapshots[key] = snapshot
    fsync_directory(HERE)
    for key, target in ledger_targets.items():
        actual_hash, actual_size, snapshot = read_existing_output(
            target, "post-fsync-" + key
        )
        need(
            (actual_hash, actual_size) == expected[key]
            and snapshot == snapshots[key],
            "pre-result stable ledger snapshot:" + key,
        )
    need(
        not os.path.lexists(result_target),
        "result commit marker raced before publication",
    )
    expected_result = (
        file_sha256(staged_result),
        staged_result.stat().st_size,
    )
    publish_exclusive(staged_result, result_target)
    fsync_directory(HERE)
    actual_result_hash, actual_result_size, _ = read_existing_output(
        result_target, "committed-result"
    )
    need(
        (actual_result_hash, actual_result_size) == expected_result,
        "committed result rehash",
    )


def run(
    *,
    input_dir: Path,
    no_write: bool,
    allow_provisional_r303a: bool,
    sample_b1: int | None,
    sample_b2: int | None,
) -> dict[str, Any]:
    complete = sample_b1 is None and sample_b2 is None
    sealed_r303a = r303a_seal_complete()
    formal = complete and sealed_r303a
    need(no_write or formal,
         "formal write requires complete run and sealed Round303A")
    if not no_write:
        need(
            HERE.resolve() == DEFAULT_INPUT_DIR.resolve(),
            "formal producer must run from deliverables",
        )
    need(
        complete or no_write,
        "sample runs are diagnostic no-write only",
    )
    if allow_provisional_r303a:
        need(no_write, "provisional Round303A may only be used no-write")
    if sample_b1 is not None:
        need(0 < sample_b1 <= EXPECTED_B1, "sample-b1 range")
    if sample_b2 is not None:
        need(0 < sample_b2 <= EXPECTED_B2, "sample-b2 range")
    need(
        complete
        or (sample_b1 is not None and sample_b2 is not None),
        "diagnostic route requires explicit B1 and B2 sample counts",
    )

    validate_inputs(input_dir, allow_provisional_r303a)
    print("R303B input pins and sealed-base manifests PASS", flush=True)
    cross, _members = collect_scope(input_dir)
    print("R303B exact cross-Round301 scope 44108 PASS", flush=True)
    accepted_b1, b2_scope, unresolved_scope = collect_r303a_partition(
        input_dir, cross
    )
    print(
        "R303B partition B1=43912 B2=192 W-tail=4 PASS",
        flush=True,
    )
    chosen_b1 = (
        accepted_b1 if sample_b1 is None else accepted_b1[:sample_b1]
    )
    chosen_b2 = (
        b2_scope if sample_b2 is None else b2_scope[:sample_b2]
    )
    selected = chosen_b1 + chosen_b2
    r294 = collect_r294(input_dir, selected)
    print("R303B selected Round294 endpoints PASS", flush=True)
    r295, r293, r291 = collect_physical_chain(input_dir, selected)
    print("R303B selected R291->R293->R295A physical chains PASS", flush=True)
    leaves, collars, origins, active = load_geometry(
        input_dir, selected, r291
    )
    print("R303B selected R179/R182 geometry lineages PASS", flush=True)
    kernel = import_kernel(input_dir)
    r204 = load_r204_lineage(input_dir, chosen_b2, r294)
    print("R303B selected R204 analytic lineages PASS", flush=True)

    id_fields = {
        "b1": "Round303B_B1_attachment_lemma_row_id",
        "b2a": "Round303B_B2a_analytic_sheet_lemma_row_id",
        "b2b": "Round303B_B2b_physical_inclusion_lemma_row_id",
        "edge": "Round303B_component_connectivity_edge_row_id",
        "unresolved": "Round303B_W_tail_unresolved_row_id",
    }
    table_names = {
        "b1": "B1_graph_attachment_lemma_rows",
        "b2a": "B2a_analytic_sheet_lemma_rows",
        "b2b": "B2b_physical_inclusion_lemma_rows",
        "edge": "component_connectivity_edge_rows",
        "unresolved": "W_tail_unresolved_rows",
    }
    schemas = {
        key: SCHEMA + "." + key + "-ledger.v1"
        for key in id_fields
    }
    producer_sha256 = file_sha256(Path(__file__).resolve())

    with tempfile.TemporaryDirectory(
        dir=HERE, prefix=f".{PREFIX}.stage."
    ) as stage_text:
        stage = Path(stage_text)
        spools = {
            key: RowSpool(stage / (key + ".rows"), id_field)
            for key, id_field in id_fields.items()
        }
        for ordinal, record in enumerate(chosen_b1, start=1):
            lemma = build_b1_row(
                record=record,
                r294=r294,
                r295=r295,
                r293=r293,
                r291=r291,
                leaves=leaves,
                collars=collars,
                origins=origins,
                active=active,
                kernel=kernel,
                formal=formal,
            )
            edge = build_edge_row(
                record=record,
                proof_path="B1",
                lemma_rows=[lemma],
                formal=formal,
            )
            if not formal:
                require_diagnostic_zero_credit(lemma, "B1")
                require_diagnostic_zero_credit(edge, "edge-B1")
            spools["b1"].add(lemma)
            spools["edge"].add(edge)
            if ordinal % 4_000 == 0:
                print(
                    f"R303B B1 replay {ordinal}/{len(chosen_b1)}",
                    flush=True,
                )
        for record in chosen_b2:
            b2a, b2b = build_b2_rows(
                record=record,
                lineage=r204[record["source_id"]],
                r294=r294,
                r295=r295,
                r293=r293,
                r291=r291,
                leaves=leaves,
                collars=collars,
                origins=origins,
                active=active,
                kernel=kernel,
                formal=formal,
            )
            edge = build_edge_row(
                record=record,
                proof_path="B2",
                lemma_rows=[b2a, b2b],
                formal=formal,
            )
            if not formal:
                require_diagnostic_zero_credit(b2a, "B2a")
                require_diagnostic_zero_credit(b2b, "B2b")
                require_diagnostic_zero_credit(edge, "edge-B2")
            spools["b2a"].add(b2a)
            spools["b2b"].add(b2b)
            spools["edge"].add(edge)
        for record in unresolved_scope:
            unresolved = build_unresolved_row(record)
            require_diagnostic_zero_credit(unresolved, "W-tail")
            spools["unresolved"].add(unresolved)

        commitments = {
            key: spool.close() for key, spool in spools.items()
        }
        if complete:
            need(
                commitments["b1"]["row_count"] == EXPECTED_B1
                and commitments["b2a"]["row_count"] == EXPECTED_B2
                and commitments["b2b"]["row_count"] == EXPECTED_B2
                and commitments["edge"]["row_count"] == EXPECTED_EDGE
                and commitments["unresolved"]["row_count"] == EXPECTED_WTAIL
                and commitments["edge"]["row_count"]
                + commitments["unresolved"]["row_count"] == EXPECTED_CROSS,
                "complete R303B output census",
            )
        staged_ledgers: dict[str, Path] = {}
        file_hashes: dict[str, str] = {}
        status = (
            "FORMAL_COMPLETE__ROUND303A_SEALED__G0_G5_REPLAYED"
            if formal
            else (
                "DIAGNOSTIC_SAMPLE__SEALED_ROUND303A__ZERO_FORMAL_CREDIT"
                if sealed_r303a
                else (
                    "DIAGNOSTIC_SAMPLE__PROVISIONAL_ROUND303A__"
                    "ZERO_FORMAL_CREDIT"
                )
            )
        )
        for key in id_fields:
            path = stage / OUTPUT_NAMES[key]
            write_ledger(
                path,
                spools[key].path,
                table_names[key],
                schemas[key],
                commitments[key],
                status,
            )
            staged_ledgers[key] = path
            file_hashes[key] = file_sha256(path)
        consumed_input_pins = {
            **dict(sorted(BASE_INPUT_PINS.items())),
            **dict(sorted(EXECUTABLE_TRANSITIVE_CLOSURE_PINS.items())),
            **dict(sorted(PROVISIONAL_R303A_PINS.items())),
        }
        if sealed_r303a:
            need(
                type(R303A_SEAL_MANIFEST_PIN) is str,
                "sealed Round303A manifest pin type",
            )
            consumed_input_pins.update({
                R303A_MANIFEST: R303A_SEAL_MANIFEST_PIN,
                **{
                    name: value
                    for name, value in R303A_MANIFEST_MEMBER_PINS.items()
                    if type(value) is str
                },
            })
        result = {
            "schema": SCHEMA,
            "status": (
                "PASS_ROUND303B_43912_B1_192_B2_COMPONENT_EDGES__"
                "4_WTAIL_UNRESOLVED__ZERO_DSU_AND_DOWNSTREAM_CREDIT"
                if formal
                else (
                    "DIAGNOSTIC_ROUND303B_B1_B2_SAMPLE__"
                    "SEALED_R303A__ZERO_FORMAL_PROMOTION"
                    if sealed_r303a
                    else (
                        "DIAGNOSTIC_ROUND303B_B1_B2_SAMPLE__"
                        "PROVISIONAL_R303A__ZERO_FORMAL_PROMOTION"
                    )
                )
            ),
            "producer_sha256": producer_sha256,
            "seed_affects_output": False,
            "complete_formal_run": formal,
            "provisional_Round303A_consumed": not sealed_r303a,
            "input_file_pins": dict(sorted(consumed_input_pins.items())),
            "executable_runtime_closure": {
                "entrypoint": R179_KERNEL,
                "transitive_file_pins": dict(sorted(
                    EXECUTABLE_TRANSITIVE_CLOSURE_PINS.items()
                )),
                "recursive_import_graph": {
                    name: sorted(children)
                    for name, children in sorted(
                        EXECUTABLE_IMPORT_GRAPH.items()
                    )
                },
                "module_files_exactly_pinned": True,
                "sys_modules_alternates_cleared": True,
                "python_flint_version": "0.9.0",
                "interval_precision_bits": 256,
            },
            "Round303A_seal": {
                "manifest_filename": R303A_MANIFEST,
                "manifest_file_sha256": R303A_SEAL_MANIFEST_PIN,
                "manifest_member_count": 10,
                "manifest_members":
                    dict(sorted(R303A_MANIFEST_MEMBER_PINS.items())),
                "manifest_exact_member_set_checked": sealed_r303a,
                "manifest_member_hashes_checked": sealed_r303a,
            },
            "Round294B_registry_builder_admission": {
                "manifest_filename": R294B_MANIFEST,
                "manifest_file_sha256": R294B_MANIFEST_SHA256,
                "manifest_member_count": 11,
                "verification_filename": R294B_VERIFICATION,
                "verification_file_sha256":
                    R294B_VERIFICATION_FILE_SHA256,
                "verification_object_sha256":
                    R294B_VERIFICATION_OBJECT_SHA256,
                "formal_occurrence_registry_row_count": 431_208,
                "formal_representation_binding_count": 46_288,
                "direct_Round287_union_issuance_count_rejected": 10_020,
                "binding_rows_issuing_occurrence_ID_count": 0,
                "admission_checked_before_Round294_consumption": True,
                "bypass_permitted": False,
            },
            "theorem": GLUING_THEOREM,
            "theorem_sha256": THEOREM_SHA256,
            "theorem_objects": {
                "B1_monotone_closure": {
                    "theorem": B1_LAYER_THEOREM,
                    "theorem_sha256": B1_LAYER_THEOREM_SHA256,
                    "kernel_theorem": MONOTONE_LIMIT_THEOREM,
                    "kernel_theorem_sha256":
                        MONOTONE_LIMIT_THEOREM_SHA256,
                },
                "B2a_FULL_2D_analytic_closure": {
                    "theorem": B2A_LAYER_THEOREM,
                    "theorem_sha256": B2A_LAYER_THEOREM_SHA256,
                },
                "B2b_target_factor_sheet_inclusion": {
                    "theorem": B2B_LAYER_THEOREM,
                    "theorem_sha256": B2B_LAYER_THEOREM_SHA256,
                    "target_factor_sheet_theorem":
                        R182_TARGET_FACTOR_SHEET_THEOREM,
                    "target_factor_sheet_theorem_sha256":
                        R182_TARGET_FACTOR_SHEET_THEOREM_SHA256,
                },
                "G0_G5_final_gluing": {
                    "theorem": GLUING_THEOREM,
                    "theorem_sha256": THEOREM_SHA256,
                },
            },
            "scope_census": {
                "Round300D_rows": EXPECTED_R300D,
                "cross_Round301_pairs": EXPECTED_CROSS,
                "B1_scope_pairs": EXPECTED_B1_SCOPE,
                "B1_accepted_pairs": EXPECTED_B1,
                "B2_accepted_pairs": EXPECTED_B2,
                "W_tail_unresolved_pairs": EXPECTED_WTAIL,
                "accepted_plus_unresolved": EXPECTED_CROSS,
                "selected_distinct_endpoint_count":
                    EXPECTED_SELECTED_ENDPOINTS,
                "old_63224_component_result_reused": False,
                "conditional_DSU_result_consumed": False,
            },
            "run_census": {
                "B1_rows": commitments["b1"]["row_count"],
                "B2a_rows": commitments["b2a"]["row_count"],
                "B2b_rows": commitments["b2b"]["row_count"],
                "candidate_edge_rows": commitments["edge"]["row_count"],
                "W_tail_unresolved_rows":
                    commitments["unresolved"]["row_count"],
            },
            "output_ledgers": {
                key: {
                    "filename": OUTPUT_NAMES[key],
                    "schema": schemas[key],
                    **commitments[key],
                    "file_sha256": file_hashes[key],
                }
                for key in id_fields
            },
            "formal_credit_transition": {
                "formal_component_edge_credit":
                    EXPECTED_EDGE if formal else 0,
                **{field: 0 for field in ZERO_FIELDS},
            },
            "strict_nonclaims": {
                "occurrence_identity_collapsed": False,
                "official_key_identity_merged": False,
                "Round301_DSU_mutated_or_reused": False,
                "old_63224_partition_used": False,
                "conditional_92696_partition_used": False,
                "maximality_claimed": False,
                "fibre_exhaustion_claimed": False,
                "global_disposition_claimed": False,
                "W_tail_rows_are_nonedges_or_exclusions": False,
            },
            "atomicity_contract": {
                "five_ledgers_staged_before_any_publication": True,
                "result_staged_before_any_publication": True,
                "ledger_batch_directory_fsynced_before_result": True,
                "result_published_no_replace_last_as_commit_marker": True,
                "output_directory_fsynced_after_result_commit": True,
                "all_six_targets_no_clobber": True,
                "result_absent_reuses_only_exact_prior_crash_ledgers": True,
                "result_present_idempotence_requires_all_six_exact": True,
                "mismatched_existing_target_left_untouched_and_rejected":
                    True,
                "nlink2_crash_orphan_requires_manual_recovery": True,
                "partial_formal_promotion_permitted": False,
                "sample_run_writes_formal_outputs": False,
            },
            "required_before_edge_consumption": [
                (
                    "Run this producer under two distinct nonempty seeds and "
                    "confirm exact byte-identical outputs."
                ),
                (
                    "Run a separately implemented cacheless verifier and its "
                    "focused re-sign, schema, semantic, and path attacks."
                ),
                (
                    "Seal the producer, five ledgers, result, verifier, "
                    "verification, attack suite, dual-seed replay, and cold "
                    "replay in one exact manifest before edge consumption."
                ),
            ],
            "result_sha256": "",
        }
        result_bytes = finalize_result(result)
        staged_result = stage / OUTPUT_NAMES["result"]
        with staged_result.open("wb") as stream:
            stream.write(result_bytes)
            stream.flush()
            os.fsync(stream.fileno())
        if not no_write:
            commit_formal_package(staged_ledgers, staged_result)
        printed = json.loads(result_bytes)
        printed["result_file_sha256"] = hashlib.sha256(result_bytes).hexdigest()
        return printed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--allow-provisional-r303a", action="store_true")
    parser.add_argument("--sample-b1", type=int)
    parser.add_argument("--sample-b2", type=int)
    parser.add_argument("--seed", default="303201")
    args = parser.parse_args()
    need(bool(args.seed), "nonempty seed bookkeeping")
    result = run(
        input_dir=args.input_dir,
        no_write=args.no_write,
        allow_provisional_r303a=args.allow_provisional_r303a,
        sample_b1=args.sample_b1,
        sample_b2=args.sample_b2,
    )
    print("invocation_seed=" + args.seed)
    print(result["status"])
    print(json.dumps(result["scope_census"], sort_keys=True))
    print(json.dumps(result["run_census"], sort_keys=True))
    print("producer_sha256=" + result["producer_sha256"])
    print("result_sha256=" + result["result_sha256"])
    print("result_file_sha256=" + result["result_file_sha256"])


if __name__ == "__main__":
    main()
