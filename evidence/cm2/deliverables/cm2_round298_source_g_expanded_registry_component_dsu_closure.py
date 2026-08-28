#!/usr/bin/env python3
"""Parameterized, fail-closed framework for the future Round298 DSU.

The ordinary-face, true-seam, and Round291 lower physical-incidence inputs
form a sealed *prefix*, not a complete FULL-face inventory.  This module
defines the future channel and ledger contracts, but refuses to emit any
candidate while:

* the Round292 internal-refinement-face channel is not formally mapped;
* FULL-face channel exhaustion is not independently sealed; or
* 9,404 refined occurrences lack append-only official-key bindings,
  including a transport-equivalence disposition for eight new raw keys.

All counts below that are labelled as diagnostics remain non-promoted.
Witness nodes are proof devices and can never become registry members.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round298_source_g_expanded_registry_component_dsu_closure"
SCHEMA = "cm2.round298.source-g-expanded-registry-component-dsu-closure.v1"

MEMBER_ASSIGNMENTS = HERE / f"{PREFIX}_member_assignment_ledger.json.gz"
EDGE_APPLICATIONS = HERE / f"{PREFIX}_edge_application_ledger.json.gz"
CANONICAL_PAIRS = (
    HERE / f"{PREFIX}_canonical_pair_projection_ledger.json.gz"
)
COMPONENTS = HERE / f"{PREFIX}_component_ledger.json.gz"
COMPONENT_KEY_INCIDENCE = (
    HERE / f"{PREFIX}_component_key_incidence_ledger.json.gz"
)
REFINED_KEY_BINDINGS = (
    HERE / f"{PREFIX}_refined_occurrence_key_binding_ledger.json.gz"
)
PHYSICAL_ASSIGNMENTS = (
    HERE / f"{PREFIX}_physical_witness_component_assignment_ledger.json.gz"
)
REPRESENTATION_ASSIGNMENTS = (
    HERE / f"{PREFIX}_representation_component_assignment_ledger.json.gz"
)
NO_BINDING_EXCLUSIONS = (
    HERE / f"{PREFIX}_no_binding_exclusion_ledger.json.gz"
)
RESULT = HERE / f"{PREFIX}_result.json"

LEDGER_PATHS = {
    "member_assignment": MEMBER_ASSIGNMENTS,
    "edge_application": EDGE_APPLICATIONS,
    "canonical_pair_projection": CANONICAL_PAIRS,
    "component": COMPONENTS,
    "component_key_incidence": COMPONENT_KEY_INCIDENCE,
    "refined_occurrence_key_binding": REFINED_KEY_BINDINGS,
    "physical_witness_component_assignment": PHYSICAL_ASSIGNMENTS,
    "representation_component_assignment": REPRESENTATION_ASSIGNMENTS,
    "no_binding_exclusion": NO_BINDING_EXCLUSIONS,
}

LEDGER_SCHEMAS = {
    name: f"{SCHEMA}.{name.replace('_', '-')}-ledger.v1"
    for name in LEDGER_PATHS
}

# These field sets are contracts for the future deterministic producer and
# independent verifier.  They are deliberately explicit so a raw witness,
# its canonical-pair projection, and its DSU rank effect cannot be conflated.
ROW_FIELD_SCHEMAS = {
    "member_assignment": {
        "required": (
            "row_id",
            "member_id",
            "member_kind",
            "formal_occurrence_id",
            "base_root_id",
            "inherited_round266_component_id",
            "source_package_id",
            "source_ledger_id",
            "source_row_id",
            "official_key_ids",
            "official_key_ids_digest",
            "assignment_disposition",
        ),
        "forbidden": (
            "witness_node_id_as_member",
            "single_official_key_id",
            "key_pure_component_id",
        ),
    },
    "edge_application": {
        "required": (
            "row_id",
            "application_ordinal",
            "channel_id",
            "raw_source_package_id",
            "raw_source_ledger_id",
            "raw_source_row_id",
            "raw_witness_id",
            "raw_witness_kind",
            "endpoint_a_formal_occurrence_id",
            "endpoint_b_formal_occurrence_id",
            "canonical_pair_row_id",
            "rank_effect",
            "pre_union_root_a",
            "pre_union_root_b",
            "post_union_root",
        ),
        "forbidden": (
            "witness_node_member_id",
            "maximality_credit",
            "fibre_credit",
            "disposition_credit",
        ),
    },
    "canonical_pair_projection": {
        "required": (
            "row_id",
            "canonical_pair_id",
            "endpoint_lo_formal_occurrence_id",
            "endpoint_hi_formal_occurrence_id",
            "endpoint_pair_digest",
            "channel_ids",
            "raw_edge_application_row_ids",
            "raw_witness_count",
            "cross_channel_multiplicity",
            "projection_disposition",
        ),
        "forbidden": (
            "rank_reduction_credit",
            "witness_node_member_id",
        ),
    },
    "component": {
        "required": (
            "row_id",
            "component_id",
            "canonical_representative_member_id",
            "member_ids",
            "member_ids_digest",
            "member_count",
            "base_root_ids",
            "base_root_ids_digest",
            "base_root_count",
            "official_key_ids",
            "official_key_ids_digest",
            "official_key_count",
            "unkeyed_member_count_before_refined_binding",
            "component_key_incidence_row_ids",
        ),
        "forbidden": (
            "official_key_id",
            "single_official_key_id",
            "key_pure",
            "maximality_credit",
            "fibre_credit",
            "disposition_credit",
        ),
    },
    "component_key_incidence": {
        "required": (
            "row_id",
            "component_id",
            "official_key_id",
            "member_ids",
            "member_ids_digest",
            "member_count",
            "binding_row_ids",
            "binding_row_ids_digest",
            "incidence_disposition",
        ),
        "forbidden": (
            "component_is_key_pure",
            "identity_alias_credit",
        ),
    },
    "refined_occurrence_key_binding": {
        "required": (
            "row_id",
            "refined_occurrence_id",
            "round294_registry_row_id",
            "round294_member_reference_digest",
            "round292_refinement_component_id",
            "round275_local_return_signature_row_id",
            "round275_local_return_signature_digest",
            "raw_official_key_id",
            "raw_official_key_ordinal",
            "seen_in_prior_116_key_universe",
            "transport_equivalence_target_key_id",
            "transport_equivalence_disposition",
            "binding_proof_digest",
            "append_only_identity_preserved",
        ),
        "forbidden": (
            "replacement_occurrence_id",
            "identity_collapse_target",
            "permanent_null_key",
        ),
    },
    "physical_witness_component_assignment": {
        "required": (
            "row_id",
            "physical_assignment_class",
            "source_package_id",
            "source_ledger_id",
            "source_row_id",
            "physical_witness_id",
            "physical_child_id",
            "canonical_target_occurrence_ids",
            "canonical_target_count",
            "assigned_component_ids",
            "connectivity_requirement",
            "edge_application_row_ids",
            "assignment_disposition",
        ),
        "forbidden": (
            "relation_group_component_requirement",
            "witness_node_member_id",
        ),
    },
    "representation_component_assignment": {
        "required": (
            "row_id",
            "source_package_id",
            "source_ledger_id",
            "source_row_id",
            "representation_id",
            "canonical_target_occurrence_id",
            "assigned_component_id",
            "assignment_disposition",
        ),
        "forbidden": (
            "new_component_edge_credit",
            "identity_alias_credit",
        ),
    },
    "no_binding_exclusion": {
        "required": (
            "row_id",
            "source_package_id",
            "source_ledger_id",
            "source_row_id",
            "physical_witness_id",
            "no_binding_reason",
            "excluded_member_ids",
            "excluded_edge_application_row_ids",
            "exclusion_proof_digest",
        ),
        "forbidden": (
            "assigned_component_id",
            "new_component_edge_credit",
        ),
    },
}

R295C_MANIFEST = (
    "cm2_round295c_source_g_all_stratum_scope_composition_closure_"
    "manifest.sha256"
)
R296_MANIFEST = (
    "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_"
    "manifest.sha256"
)
R297_MANIFEST = (
    "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_"
    "manifest.sha256"
)

PACKAGE_MANIFEST_PINS = {
    R295C_MANIFEST:
        "a9499856148480b9ddd5b0dd9ea8de28b989b592477c9a3b7ea43541772180c1",
    R296_MANIFEST:
        "f7786b9cdec45cb381ec46489eb44b0365b8ee43d81ae9a9611cb2dcdee7fb59",
    R297_MANIFEST:
        "1feecefa897c5320eadc006509ba6bde84cdbf692dfaddd024472b93c13c38c0",
}

# No filename is invented for an upstream package that has not been sealed.
# A future patch must replace every ``None`` with an exact manifest filename
# and digest supplied by the inventory closure.
PENDING_REQUIRED_PACKAGES = {
    "round299_full_face_and_refined_key_inventory": {
        "manifest_filename": None,
        "manifest_sha256": None,
        "status": (
            "PENDING_FAIL_CLOSED__UPSTREAM_PACKAGE_NOT_YET_SEALED"
        ),
        "required_for": (
            "full_face_channel_exhaustion",
            "round292_internal_refinement_face_formal_mapping",
            "refined_occurrence_key_binding",
            "eight_new_raw_key_transport_equivalence",
        ),
    },
}

THREE_CHANNEL_PREFIX_DIAGNOSTIC = {
    "status": "NONPROMOTED_PREFIX_ONLY",
    "full_member_count": 564_492,
    "occurrence_member_count": 431_208,
    "virtual_member_count": 133_284,
    "base_root_count": 367_964,
    "raw_edge_witness_count": 491_020,
    "canonical_pair_count": 457_564,
    "ordinary_rank_reduction": 221_916,
    "true_seam_incremental_rank_reduction": 5_212,
    "lower_incremental_rank_reduction": 29_984,
    "prefix_rank_reduction": 257_112,
    "prefix_component_count": 110_852,
}

CHANNEL_SCHEMA_FIELDS = (
    "channel_id",
    "source_kind",
    "source_manifest",
    "sealed_prefix_status",
    "final_inventory_status",
    "raw_witness_count",
    "canonical_pair_count",
    "formal_occurrence_mapping_status",
    "connectivity_semantics",
    "rank_reduction",
)

CHANNEL_SPECS = {
    "O_ordinary_face": {
        "channel_id": "O_ordinary_face",
        "source_kind": "ordinary_face_occurrence_edge",
        "source_manifest": R297_MANIFEST,
        "sealed_prefix_status": "SEALED_PREFIX_INPUT",
        "final_inventory_status": (
            "PENDING_FULL_FACE_INVENTORY_CLOSURE"
        ),
        "raw_witness_count": 330_724,
        "canonical_pair_count": 330_724,
        "formal_occurrence_mapping_status": "SEALED",
        "connectivity_semantics": "TWO_ENDPOINT_FORMAL_EDGE",
        "rank_reduction": None,
        "prefix_diagnostic_rank_reduction": 221_916,
    },
    "S_true_seam": {
        "channel_id": "S_true_seam",
        "source_kind": "true_seam_occurrence_edge",
        "source_manifest": R296_MANIFEST,
        "sealed_prefix_status": "SEALED_PREFIX_INPUT",
        "final_inventory_status": (
            "PENDING_FULL_FACE_INVENTORY_CLOSURE"
        ),
        "raw_witness_count": 48_444,
        "canonical_pair_count": 15_316,
        "formal_occurrence_mapping_status": "SEALED",
        "connectivity_semantics": "TWO_ENDPOINT_FORMAL_EDGE",
        "rank_reduction": None,
        "prefix_diagnostic_rank_reduction_after_O": 5_212,
    },
    "L_round291_lower_physical_incidence": {
        "channel_id": "L_round291_lower_physical_incidence",
        "source_kind": "round291_lower_physical_incidence",
        "source_manifest": R295C_MANIFEST,
        "sealed_prefix_status": "SEALED_PREFIX_INPUT",
        "final_inventory_status": (
            "PENDING_FULL_FACE_INVENTORY_CLOSURE"
        ),
        "raw_witness_count": 111_852,
        "canonical_pair_count": 111_524,
        "formal_occurrence_mapping_status": "SEALED_PREFIX_MAPPING",
        "connectivity_semantics": (
            "ROUND291_A_TWO_TARGET_ONLY__WITNESS_NODE_PROOF_DEVICE"
        ),
        "rank_reduction": None,
        "prefix_diagnostic_rank_reduction_after_O_S": 29_984,
    },
    "F_round292_internal_refinement_face": {
        "channel_id": "F_round292_internal_refinement_face",
        "source_kind": "round292_positive_area_internal_refinement_face",
        "source_manifest": None,
        "sealed_prefix_status": "NOT_IN_THREE_CHANNEL_PREFIX",
        "final_inventory_status": (
            "PENDING_FAIL_CLOSED__CHANNEL_NOT_FORMALLY_SEALED"
        ),
        "raw_witness_count": None,
        "diagnostic_raw_contact_count": 464,
        "canonical_pair_count": None,
        "diagnostic_candidate_distinct_pair_count": 416,
        "formal_occurrence_mapping_status": (
            "PENDING_FAIL_CLOSED__FORMAL_OCCURRENCE_MAPPING"
        ),
        "connectivity_semantics": (
            "PENDING_FAIL_CLOSED__POSITIVE_AREA_CONTACT_PROOF"
        ),
        "rank_reduction": None,
    },
}

FULL_FACE_INVENTORY_STATUS = (
    "PENDING_FAIL_CLOSED__ALL_FULL_FACE_CHANNELS_NOT_YET_EXHAUSTED"
)
FULL_FACE_CHANNEL_IDS = None
FULL_FACE_INVENTORY_DIGEST = None

REFINED_OCCURRENCE_KEY_BINDING_STATUS = (
    "PENDING_FAIL_CLOSED__9404_NULL_KEYS_REQUIRE_APPEND_ONLY_BINDINGS__"
    "8212_TO_EXISTING36__1192_TO_EIGHT_NEW_RAW_KEYS__"
    "GLOBAL_TRANSPORT_EQUIVALENCE_NOT_YET_SEALED"
)

PHYSICAL_ASSIGNMENT_CONTRACT = {
    "total_assignment_row_count": 124_900,
    "round291_A_assignment_row_count": 113_452,
    "round291_A_single_target_assignment_only_count": 1_600,
    "round291_A_two_target_connectivity_count": 111_852,
    "round291_B_child_assignment_row_count": 11_448,
    "round291_B_target_count_per_child": 1,
    "round291_B_relation_grouping_implies_connectivity": False,
    "no_binding_exclusion_row_count": 28_772,
    "representation_assignment_row_count": 46_564,
    "witness_nodes_are_registry_members": False,
}

REFINED_KEY_BINDING_DIAGNOSTIC = {
    "status": "NONPROMOTED_BINDING_DIAGNOSTIC_ONLY",
    "refined_occurrence_count": 9_404,
    "mapped_to_existing_36_raw_keys": 8_212,
    "mapped_to_eight_new_raw_keys": 1_192,
    "new_raw_key_count": 8,
    "rows_per_new_raw_key": 149,
    "candidate_raw_key_universe_count": 124,
}

FINAL_COUNTS = {
    "raw_edge_witness_count": None,
    "canonical_pair_count": None,
    "rank_reducing_edge_count": None,
    "redundant_edge_application_count": None,
    "base_root_rank_reduction": None,
    "component_count": None,
    "component_key_incidence_count": None,
}

ATTACK_GATE_REQUIREMENTS = {
    "channel_inventory": (
        "MISSING_CHANNEL_RAW_ROW",
        "MISSING_R292_INTERNAL_REFINEMENT_FACE_CHANNEL",
        "FULL_FACE_INVENTORY_OMISSION",
        "UNSEALED_CHANNEL_MANIFEST",
        "CHANNEL_COUNT_OR_DIGEST_FORGERY",
    ),
    "edge_projection_and_rank": (
        "RAW_CANONICAL_RANK_CONFLATION",
        "CANONICAL_PAIR_ENDPOINT_ORDER_FORGERY",
        "CANONICAL_PAIR_OVERLAP_FORGERY",
        "CROSS_CHANNEL_PAIR_MULTIPLICITY_FORGERY",
        "RANK_REDUCTION_COUNT_FORGERY",
        "DSU_PARTITION_FORGERY",
        "CHANNEL_ORDER_DEPENDENT_FINAL_PARTITION",
    ),
    "physical_assignment_semantics": (
        "WITNESS_NODE_COUNTED_AS_MEMBER",
        "ROUND291_A_SINGLE_TARGET_PROMOTED_TO_EDGE",
        "ROUND291_A_TWO_TARGET_LEFT_IN_DIFFERENT_COMPONENTS",
        "ROUND291_B_RELATION_GROUP_PROMOTED_TO_EDGE",
        "ROUND291_B_CHILD_TARGET_CARDINALITY_FORGERY",
        "NO_BINDING_ROW_PROMOTED_TO_MEMBER_OR_EDGE",
        "REPRESENTATION_BINDING_PROMOTED_TO_EDGE",
    ),
    "key_binding_and_identity": (
        "PERMANENT_NULL_REFINED_KEY",
        "UNSEALED_EIGHT_NEW_RAW_KEY_TRANSPORT",
        "REFINED_BINDING_NOT_APPEND_ONLY",
        "REFINED_BINDING_SOURCE_REFERENCE_FORGERY",
        "OCCURRENCE_IDENTITY_COLLAPSE",
        "SINGLE_COMPONENT_KEY_FIELD_RESURRECTION",
        "EXACT_KEY_PURITY_RESURRECTION",
        "COMPONENT_KEY_INCIDENCE_OMISSION_OR_FORGERY",
    ),
    "forbidden_credit": (
        "MAXIMALITY_CREDIT_FORGERY",
        "FIBRE_CREDIT_FORGERY",
        "DISPOSITION_CREDIT_FORGERY",
        "IDENTITY_OR_ALIAS_CREDIT_FORGERY",
    ),
    "strict_serialization": (
        "JSON_DUPLICATE_KEY",
        "JSON_TRAILING_GARBAGE",
        "JSON_NON_UTF8",
        "GZIP_TRUNCATED_MEMBER",
        "GZIP_CONCATENATED_MEMBER",
        "GZIP_NONDETERMINISTIC_HEADER",
    ),
    "path_and_boundary": (
        "MANIFEST_PIN_FORGERY",
        "SYMLINK_INPUT_SUBSTITUTION",
        "HARDLINK_INPUT_SUBSTITUTION",
        "PATH_TRAVERSAL_INPUT_SUBSTITUTION",
    ),
}

PIN_RE = re.compile(r"^[0-9a-f]{64}$")


class ClosureError(RuntimeError):
    """Fail-closed Round298 construction error."""


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1 << 20), b""):
            state.update(piece)
    return state.hexdigest()


def _is_pending(value: object) -> bool:
    return value is None or (
        isinstance(value, str) and value.startswith("PENDING_")
    )


def validate_parameterized_framework() -> None:
    """Check the static contract before considering any final inputs."""
    if set(LEDGER_PATHS) != set(LEDGER_SCHEMAS):
        raise ClosureError("FRAMEWORK_LEDGER_SCHEMA_PATH_SET_MISMATCH")
    if set(LEDGER_PATHS) != set(ROW_FIELD_SCHEMAS):
        raise ClosureError("FRAMEWORK_LEDGER_ROW_SCHEMA_SET_MISMATCH")
    if len(set(LEDGER_PATHS.values())) != len(LEDGER_PATHS):
        raise ClosureError("FRAMEWORK_DUPLICATE_LEDGER_PATH")
    if len(set(LEDGER_SCHEMAS.values())) != len(LEDGER_SCHEMAS):
        raise ClosureError("FRAMEWORK_DUPLICATE_LEDGER_SCHEMA")
    for name, path in LEDGER_PATHS.items():
        if path.parent != HERE or path.suffix != ".gz":
            raise ClosureError("FRAMEWORK_UNSAFE_LEDGER_PATH:" + name)
        fields = ROW_FIELD_SCHEMAS[name]
        required = fields["required"]
        forbidden = fields["forbidden"]
        if (
            not required
            or len(required) != len(set(required))
            or set(required) & set(forbidden)
        ):
            raise ClosureError("FRAMEWORK_INVALID_ROW_FIELDS:" + name)

    if set(CHANNEL_SPECS) != {
        value["channel_id"] for value in CHANNEL_SPECS.values()
    }:
        raise ClosureError("FRAMEWORK_CHANNEL_ID_MISMATCH")
    for channel_id, spec in CHANNEL_SPECS.items():
        missing = set(CHANNEL_SCHEMA_FIELDS) - set(spec)
        if missing:
            raise ClosureError(
                "FRAMEWORK_CHANNEL_SCHEMA_MISSING:"
                + channel_id
                + ":"
                + ",".join(sorted(missing))
            )

    prefix = THREE_CHANNEL_PREFIX_DIAGNOSTIC
    if (
        prefix["occurrence_member_count"]
        + prefix["virtual_member_count"]
        != prefix["full_member_count"]
        or 330_724 + 48_444 + 111_852
        != prefix["raw_edge_witness_count"]
        or 330_724 + 15_316 + 111_524
        != prefix["canonical_pair_count"]
        or 221_916 + 5_212 + 29_984
        != prefix["prefix_rank_reduction"]
        or prefix["base_root_count"] - prefix["prefix_rank_reduction"]
        != prefix["prefix_component_count"]
    ):
        raise ClosureError("FRAMEWORK_PREFIX_DIAGNOSTIC_ARITHMETIC")

    physical = PHYSICAL_ASSIGNMENT_CONTRACT
    if (
        physical["round291_A_assignment_row_count"]
        + physical["round291_B_child_assignment_row_count"]
        != physical["total_assignment_row_count"]
        or physical["round291_A_single_target_assignment_only_count"]
        + physical["round291_A_two_target_connectivity_count"]
        != physical["round291_A_assignment_row_count"]
        or physical["round291_B_relation_grouping_implies_connectivity"]
        or physical["witness_nodes_are_registry_members"]
    ):
        raise ClosureError("FRAMEWORK_PHYSICAL_ASSIGNMENT_CONTRACT")

    attack_names = [
        name
        for group in ATTACK_GATE_REQUIREMENTS.values()
        for name in group
    ]
    if len(attack_names) != len(set(attack_names)):
        raise ClosureError("FRAMEWORK_DUPLICATE_ATTACK_GATE")


def verify_sealed_manifest_boundary() -> None:
    """Verify only already sealed packages; pending packages stay symbolic."""
    for filename, expected in PACKAGE_MANIFEST_PINS.items():
        if PIN_RE.fullmatch(expected) is None:
            raise ClosureError("UNSEALED_PACKAGE_MANIFEST_PIN:" + filename)
        path = HERE / filename
        if (
            path.parent != HERE
            or not path.is_file()
            or path.is_symlink()
            or file_sha256(path) != expected
        ):
            raise ClosureError("PACKAGE_MANIFEST_PIN_MISMATCH:" + filename)


def validate_final_configuration() -> None:
    """Refuse construction until every upstream and semantic gate is sealed."""
    validate_parameterized_framework()
    verify_sealed_manifest_boundary()
    blockers = []

    for logical_name, package in PENDING_REQUIRED_PACKAGES.items():
        filename = package["manifest_filename"]
        digest = package["manifest_sha256"]
        status = package["status"]
        if (
            _is_pending(filename)
            or not isinstance(filename, str)
            or Path(filename).name != filename
            or _is_pending(digest)
            or not isinstance(digest, str)
            or PIN_RE.fullmatch(digest) is None
            or _is_pending(status)
        ):
            blockers.append("UPSTREAM_PACKAGE:" + logical_name)

    if _is_pending(FULL_FACE_INVENTORY_STATUS):
        blockers.append("FULL_FACE_INVENTORY_STATUS")
    if (
        FULL_FACE_CHANNEL_IDS is None
        or FULL_FACE_INVENTORY_DIGEST is None
    ):
        blockers.append("FULL_FACE_INVENTORY_CONFIGURATION")
    elif PIN_RE.fullmatch(FULL_FACE_INVENTORY_DIGEST) is None:
        blockers.append("FULL_FACE_INVENTORY_DIGEST")

    for channel_id, spec in CHANNEL_SPECS.items():
        if (
            spec["final_inventory_status"] != "SEALED_FINAL_CHANNEL"
            or spec["raw_witness_count"] is None
            or spec["canonical_pair_count"] is None
            or spec["rank_reduction"] is None
            or _is_pending(spec["formal_occurrence_mapping_status"])
            or _is_pending(spec["connectivity_semantics"])
        ):
            blockers.append("CHANNEL:" + channel_id)

    if _is_pending(REFINED_OCCURRENCE_KEY_BINDING_STATUS):
        blockers.append("REFINED_OCCURRENCE_KEY_BINDING_STATUS")
    for name, value in FINAL_COUNTS.items():
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append("FINAL_COUNT:" + name)

    if blockers:
        raise ClosureError(
            "ROUND298_FAIL_CLOSED__" + "__".join(sorted(blockers))
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=298_001)
    parser.parse_args()
    validate_final_configuration()
    raise ClosureError(
        "ROUND298_PARAMETERIZED_FRAMEWORK_ONLY__BUILDER_NOT_INSTALLED"
    )


if __name__ == "__main__":
    main()
