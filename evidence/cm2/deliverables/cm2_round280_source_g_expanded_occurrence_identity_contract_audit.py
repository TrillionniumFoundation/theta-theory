#!/usr/bin/env python3
"""Zero-credit audit of the frozen expanded-occurrence identity contract.

This audit resolves a semantic ambiguity in the Round280 preview.  Frozen
Rounds174/179/204/208 define occurrences as materialized local positive-open
3D rows.  Rounds265/266 preserve those row identities while certified face
edges act only on the component DSU.  Consequently a connected class of
Round279 atoms is a local component-connectivity class, not an occurrence
identity class.

No occurrence, component, maximality, fibre, disposition, Gate5, D02 or CM2
credit is issued by this audit.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round280_source_g_expanded_occurrence_identity_contract_audit"
OUTPUT = HERE / f"{PREFIX}_result.json"
SCHEMA = "cm2.round280.source-g-expanded-occurrence-identity-contract-audit.v1"

FILES = {
    "R174_SOURCE": (
        "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py",
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    ),
    "R179_SOURCE": (
        "cm2_round179_source_g_residual_tube_arrangement.py",
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    ),
    "R204_SOURCE": (
        "cm2_round204_source_g_wall_return_signature_local_replacement.py",
        "7e4b81846155c1edad0807362c7086a290702da7ce6680d7c449b7193635da77",
    ),
    "R208_SOURCE": (
        "cm2_round208_source_g_outgoing_direct_signature_materialization.py",
        "c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913",
    ),
    "R265_SOURCE": (
        "cm2_round265_source_g_expanded_occurrence_safe_face_saturation.py",
        "ff32b033486d236d67532e7eef771983b32c8ca556d3fce06ddf3313ffb3f84d",
    ),
    "R266_SOURCE": (
        "cm2_round266_source_g_expanded_curved_face_closure.py",
        "22c2fa3555a69681f724088ad01d080e5f8925ae974f5e69307d72badd08a999",
    ),
    "R275_SOURCE": (
        "cm2_round275_source_g_complete_reverse_rechart_materialization.py",
        "4534a7000ddbc52933361f0d323ffc450e979ffc2b7ee891d3a0e770a216482f",
    ),
    "R279_SOURCE": (
        "cm2_round279_source_g_collar_atom_and_face_edge_freeze.py",
        "03a0c55a95d3f9bd2fcd3bf39060c9f3e2cb6799d321210375e1e793972bbda1",
    ),
    "R279_CERTIFICATE": (
        "cm2_round279_source_g_collar_atom_and_face_edge_freeze_certificate.json",
        "ef60a40cc05d47b3d899b73169017bee8e246583ce51a5b543f1b1a1047f064e",
    ),
    "R280_PREVIEW_SOURCE": (
        "cm2_round280_source_g_occurrence_materialization_and_dsu_preview_probe.py",
        "44eb9afa863b86e4dea0de081bcff323be4b7126c97c25f2b06e7398f6964e51",
    ),
    "R280_PREVIEW_RESULT": (
        "cm2_round280_source_g_occurrence_materialization_and_dsu_preview_probe_result.json",
        "93b0fc0ce798284120adb78e08f9c78ad33c67607dd40870483a5a1031388541",
    ),
}


class AuditError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise AuditError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def load_document(name: str) -> dict[str, Any]:
    value = json.loads((HERE / name).read_text())
    need(
        isinstance(value, dict)
        and set(value) == {"result", "result_sha256"}
        and value["result_sha256"] == digest(value["result"]),
        f"closed document:{name}",
    )
    return value


def require_snippets(name: str, snippets: tuple[str, ...]) -> None:
    text = (HERE / name).read_text()
    for snippet in snippets:
        need(snippet in text, f"missing frozen semantic snippet:{name}:{snippet}")


def stable_new_occurrence_id(atom: dict[str, Any]) -> str:
    """Deterministic ID rule for a future promoting producer.

    Calling this function does not promote the atom.  The producer may call it
    only after satisfying every condition in ``atom_promotion_preconditions``.
    """

    descriptor = [
        "ROUND279_CANONICAL_ATOM_LOCAL_OCCURRENCE_V1",
        atom["canonical_atom_id"],
        atom["row_sha256"],
        atom["Round182_leaf_row_id"],
        atom["complete_10_field_return_signature_sha256"],
        atom["source_signature_row_ids"],
        atom["frozen_true_support_boxes"],
    ]
    return "source-g-expanded-occurrence:" + digest(descriptor)


def build_result() -> dict[str, Any]:
    pins: dict[str, dict[str, str]] = {}
    for label, (name, expected) in FILES.items():
        actual = file_sha256(HERE / name)
        need(actual == expected, f"file pin:{label}")
        pins[label] = {"path": name, "sha256": actual}

    require_snippets(
        FILES["R174_SOURCE"][0],
        (
            "A positive\nthree-dimensional child is accepted only when",
            '"row_id": row_id("resolved-3d", payload)',
            '"physical_open_subset_positive": True',
        ),
    )
    require_snippets(
        FILES["R179_SOURCE"][0],
        (
            "one additional adaptive dyadic split releases strict regular occurrence",
            '"row_id": make_id("resolved-child", payload)',
        ),
    )
    require_snippets(
        FILES["R204_SOURCE"][0],
        (
            '"region_row_id":',
            '"strict_open_region": True',
            '"formal_local_signature_credit": 1',
        ),
    )
    require_snippets(
        FILES["R208_SOURCE"][0],
        (
            '"region_row_id": geometry["candidate_region_id"]',
            '"strict_open_3D_region_exists": True',
            '"formal_local_open_3D_signature_credit": 1',
        ),
    )
    require_snippets(
        FILES["R265_SOURCE"][0],
        (
            "adds those rows as initially separate seeds",
            'need(len(occurrences) == 126_468, "expanded occurrence universe")',
            "# Complete expanded occurrence frontier.",
        ),
    )
    require_snippets(
        FILES["R266_SOURCE"][0],
        (
            'len(occurrence_frontier_rows) == 126_468',
            '"member_identity_preserved": True',
            '"complete_full_signature_face_is_glue_but_not_maximality": True',
        ),
    )
    require_snippets(
        FILES["R275_SOURCE"][0],
        (
            '"total_materialized_connected_region_count": 13788',
            '"expanded_occurrence_credit": 0',
            '"Jx_Jy_same_point_glue_credit": 0',
        ),
    )
    require_snippets(
        FILES["R279_SOURCE"][0],
        (
            '"artificial_alias_contraction_count": 4',
            '"new_occurrence_region_atom_candidate_count": 295976',
            '"Round268_true_seam_edges_included": False',
        ),
    )
    require_snippets(
        FILES["R280_PREVIEW_SOURCE"][0],
        (
            '"atom_graph_quotient_precedes_occurrence_identity_assignment": True',
            "expanded-occurrence identity must be defined as a connected component of the certified positive-open support graph",
            '"multiple_existing_occurrence_ids_in_one_atom_class_are_not_automatically_collapsed": True',
        ),
    )

    r279 = load_document(FILES["R279_CERTIFICATE"][0])["result"]
    r280 = load_document(FILES["R280_PREVIEW_RESULT"][0])["result"]
    need(
        r279["census"]["canonical_atom_count"] == 332_016
        and r279["census"]["artificial_alias_contraction_count"] == 4
        and r279["census"]["existing_Round208_occurrence_backed_atom_count"]
        == 36_040
        and r279["census"]["new_occurrence_region_atom_candidate_count"]
        == 295_976
        and r279["census"]["formal_common_face_edge_witness_count"] == 330_724,
        "Round279 census",
    )
    need(
        r280["census"]["connected_atom_graph_class_count"] == 92_120
        and r280["census"]["unanchored_atom_graph_class_count"] == 75_588
        and r280["census"]["formal_new_expanded_occurrence_count"] == 0
        and r280["strict_nonpromotion"]["expanded_occurrence_credit"] == 0,
        "Round280 zero-credit preview census",
    )

    return {
        "schema": SCHEMA,
        "status": (
            "PASS_ZERO_CREDIT_IDENTITY_CONTRACT_AUDIT__"
            "ROUND280_CLASS_AS_OCCURRENCE_SEMANTICS_REJECTED"
        ),
        "verdict": {
            "Round280_numerical_atom_graph_census_reusable_as_component_preview":
                True,
            "Round280_atom_graph_quotient_precedes_occurrence_identity_claim":
                "REJECTED_BY_FROZEN_ROUND265_ROUND266_CONTRACT",
            "Round280_connected_class_is_one_occurrence_claim":
                "REJECTED_BY_FROZEN_ROUND265_ROUND266_CONTRACT",
            "reason": (
                "Frozen local occurrence row identities survive positive-area "
                "face glue. Face and seam witnesses generate component-DSU "
                "relations, not occurrence-identity aliases."
            ),
        },
        "frozen_evidence": {
            "input_file_pins": pins,
            "legacy_occurrence_sources": {
                "ROUND174_RESOLVED": 72_500,
                "ROUND179_RESOLVED": 17_192,
                "ROUND204_REGION": 736,
                "ROUND208_REGION": 36_040,
                "total_Round266_occurrence_frontier": 126_468,
            },
            "Round265_initially_separate_Round174_seed_count": 72_500,
            "Round265_Round266_face_glue_preserved_occurrence_identities":
                True,
            "Round279_source_signature_rows": 332_020,
            "Round279_canonical_atoms": 332_016,
            "Round279_only_proven_identity_alias_contractions": 4,
            "Round279_existing_occurrence_backed_atoms": 36_040,
            "Round279_new_local_occurrence_atom_candidates": 295_976,
            "Round279_local_component_face_edges": 330_724,
            "Round280_local_atom_graph_classes": 92_120,
        },
        "deterministic_identity_rule": {
            "identity_basis": (
                "one independently certified local positive-open 3D region "
                "row after exact duplicate-region alias normalization"
            ),
            "existing_anchor_rule": (
                "A Round279 atom with its unique Round208 anchor maps to that "
                "existing Round266 local_occurrence_row_id."
            ),
            "new_atom_rule": (
                "Each unbacked Round279 canonical atom is one distinct "
                "new-occurrence candidate; it is not absorbed by another atom "
                "merely because a certified face path connects them."
            ),
            "canonical_new_id_formula": (
                "source-g-expanded-occurrence:SHA256(canonical(["
                "'ROUND279_CANONICAL_ATOM_LOCAL_OCCURRENCE_V1',"
                "canonical_atom_id,row_sha256,Round182_leaf_row_id,"
                "signature_sha256,sorted_source_signature_row_ids,"
                "frozen_true_support_boxes]))"
            ),
            "identity_alias_rule": (
                "Collapse identities only under an explicit exact "
                "same-positive-open-region alias certificate. Ordinary "
                "positive-area common-face edges, true-seam patches and Jx/Jy "
                "are never identity aliases."
            ),
            "current_alias_universe": (
                "Exactly the four Round271 artificial W-tail t-split aliases, "
                "already contracted before the 332,016-atom ledger."
            ),
            "atom_graph_class_rule": (
                "A post-Round279 graph class is a component-connectivity "
                "class. It equals exactly one occurrence only when it has one "
                "canonical atom after identity-alias normalization. A "
                "multi-atom class remains a multi-occurrence component class."
            ),
            "multiple_anchor_rule": (
                "Distinct frozen occurrence anchors retain distinct identities; "
                "the class supplies component-union evidence only."
            ),
            "potential_count_if_all_Round279_candidates_later_pass": {
                "preexisting": 126_468,
                "new_atom_candidates": 295_976,
                "candidate_total": 422_444,
                "formal_credit_now": 0,
            },
        },
        "atom_promotion_preconditions": [
            "Pin and independently reconstruct the Round279 atom and every source signature row.",
            "Prove the atom carries a nonempty connected positive-open 3D physical support, not only a point witness or a nominal lineage.",
            "Prove the complete 10-field signature and immutable exact key are strict on the certified support.",
            "Prove exact source-chart ownership and a positive rational inner support; a frozen outer enclosure alone is insufficient.",
            "Bind every existing duplicate exactly: Round208-backed atoms preserve their old occurrence ID; every other overlap with the 126,468 frontier must be absent or explicitly alias-certified.",
            "Prove pairwise identity uniqueness of all new atoms; the four already frozen W-tail aliases are the only currently admitted contractions.",
            "Issue one deterministic ID per passing unbacked canonical atom and preserve all existing occurrence IDs.",
            "Have an independent cacheless verifier reconstruct the complete candidate/alias partition and reject forged occurrence, alias, face and Jx/Jy credits.",
        ],
        "component_DSU_rule_and_order": [
            "Materialize or preserve occurrence identity nodes first.",
            "Map every Round279 atom to exactly one occurrence identity node.",
            "Apply the 330,724 Round279 common-face witnesses as component edges; never rewrite occurrence IDs.",
            "Bind Round275 reverse-rechart transition regions to exact incident occurrence/atom nodes.",
            "Apply the 152 Round268 true-seam patches as same-point component edges after exact incidence is proved.",
            "Rebuild deterministic exact-key-pure component IDs, then audit maximality.",
            "Jx/Jy contributes no same-point identity or component edge.",
        ],
        "Round275_reverse_rechart_disposition": {
            "raw_connected_region_rows": 13_788,
            "raw_new_occurrence_seed_count_authorized": 0,
            "candidate_total_436232_authorized": False,
            "reason": (
                "Round275 rows are zero-credit adjacent-chart transition "
                "covers of the 880 rejected coordinate guards. Their raw row "
                "count cannot be added before exact same-physical overlap and "
                "cover-refinement deduplication against Round266 occurrences "
                "and Round279 atoms."
            ),
            "required_three_way_disposition_per_positive_open_piece": [
                "EXACT_ALIAS_OF_EXISTING_OCCURRENCE_OR_ROUND279_ATOM: bind as a representation witness; add no occurrence.",
                "STRICTLY_NEW_DISJOINT_POSITIVE_OPEN_SUPPORT: it may become one new occurrence after the atom promotion conditions pass.",
                "PARTIAL_OVERLAP_OR_OUTER_ENCLOSURE_ONLY: refine to an exact disjoint physical partition and remain fail-closed meanwhile.",
            ],
            "ordering_nuance": (
                "Positive-volume same-physical overlap normalization is an "
                "identity-deduplication step before counting new Round275 "
                "occurrences. The 2D Round268 true-seam quotient is component "
                "glue after occurrence identities are fixed."
            ),
        },
        "strict_nonpromotion": {
            "new_expanded_occurrence_credit": 0,
            "occurrence_identity_collapse_credit": 0,
            "component_edge_credit": 0,
            "DSU_rank_reduction_credit": 0,
            "maximality_credit": 0,
            "exact_key_fibre_credit": 0,
            "global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "expanded_occurrences": 126_468,
            "quotient_components": 63_224,
            "maximality": "0/63224",
            "fibres": "0/116",
            "dispositions": "0/224580",
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main() -> int:
    result = build_result()
    document = {"result": result, "result_sha256": digest(result)}
    atomic_write(
        OUTPUT,
        json.dumps(document, indent=2, sort_keys=True).encode() + b"\n",
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "result_sha256": document["result_sha256"],
                "Round279_new_local_occurrence_atom_candidates": result[
                    "frozen_evidence"
                ]["Round279_new_local_occurrence_atom_candidates"],
                "Round275_raw_new_occurrence_seed_count_authorized": result[
                    "Round275_reverse_rechart_disposition"
                ]["raw_new_occurrence_seed_count_authorized"],
                "formal_credit": 0,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
