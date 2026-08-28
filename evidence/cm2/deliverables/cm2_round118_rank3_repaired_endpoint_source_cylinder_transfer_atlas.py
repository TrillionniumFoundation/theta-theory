#!/usr/bin/env python3
"""Build the fail-closed Round118 repaired-endpoint transfer atlas.

This round uses only the combinatorial source-grazing incidence preserved by
Round111 from Round102.  The withdrawn Round102 endpoint identifiers are kept
as traceability aliases and are never used to mint the repaired identifiers.

The geometric payload is deliberately small: an eight-row identity crosswalk,
the exact radius ``R_G=9/25`` source-cylinder metric transfer, and the C1
``q <-> p`` transition inherited from Round115.  It installs no reach, collar,
whole-face transfer, physical-owner atlas, standard-curve child, or Gate5 field.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2-round118-rank3-repaired-endpoint-source-cylinder-transfer-atlas-2026-07-23.json"
SCHEMA = "cm2.round118.rank3-repaired-endpoint-source-cylinder-transfer-atlas.v1"

ROUND102 = HERE / "cm2-round102-rank3-corrected-face-quotient-2026-07-22.json"
ROUND111 = HERE / "cm2-round111-rank3-round101-zero-width-correction-impact-audit-2026-07-23.json"
ROUND112 = HERE / "cm2-round112-rank3-double-grazing-two-sided-root-sheet-2026-07-23.json"
ROUND113 = HERE / "cm2-round113-rank3-endpoint-sheet-owner-ordering-2026-07-23.json"
ROUND114 = HERE / "cm2-round114-rank3-seam-root-stitch-gap-atlas-2026-07-23.json"
ROUND115 = HERE / "cm2-round115-rank3-selected-lift-nofold-atlas-2026-07-23.json"

UPSTREAM_PINS = {
    ROUND102.name: "85069546fbc29f45af93eb65e2c2979bc83bfb5d744199771e234c2f7a1f0edb",
    ROUND111.name: "e343a15d5ad4838c2b9a808d64f9724e564e850cbdb13168c5e31e8f059794f1",
    ROUND112.name: "94a54ddbf31518cfc2a93b105d66337111f2b950be894f126e7b9c042e6b02e5",
    ROUND113.name: "d38d0fb159ea31ce430c1e2a27b88cc630d786921d3d4642f2bd3fe7c298e181",
    ROUND114.name: "945cbd96032544bdff449398715f173cabb9e034415a0ca5edb594715ce970d4",
    ROUND115.name: "bcaa3612fe6369b7a6a55e51cd7d345d3a7e4817906dd5998ad544d945035263",
    "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py": "ccdfeebfa14fdaa466a67b79269145b2a36076b7027f2bac0a9c5daa030b5e3f",
    "cm2_round76_r2_numeric_fields_generator.py": "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf",
}

UPSTREAM_SCHEMAS = {
    ROUND102.name: "cm2.round102.rank3-corrected-face-quotient.v1",
    ROUND111.name: "cm2.round111.rank3-round101-zero-width-correction-impact-audit.v1",
    ROUND112.name: "cm2.round112.rank3-double-grazing-two-sided-root-sheet.v1",
    ROUND113.name: "cm2.round113.rank3-endpoint-sheet-owner-ordering.v1",
    ROUND114.name: "cm2.round114.rank3-seam-root-stitch-gap-atlas.v1",
    ROUND115.name: "cm2.round115.rank3-selected-lift-nofold-atlas.v1",
}

ADJACENT_CHART_PAIRS = {
    frozenset(("E", "N")),
    frozenset(("N", "W")),
    frozenset(("W", "S")),
    frozenset(("S", "E")),
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_integer(token: str) -> int:
    digits = token[1:] if token.startswith("-") else token
    if token == "-0":
        raise ValueError("negative zero forbidden")
    if len(digits) > 256:
        raise ValueError("overlong JSON integer")
    return int(token)


def validate_json_tree(value: Any) -> None:
    if isinstance(value, str):
        if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            raise ValueError("unpaired Unicode surrogate forbidden")
        return
    if isinstance(value, list):
        for item in value:
            validate_json_tree(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            validate_json_tree(key)
            validate_json_tree(item)


def strict_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(),
        object_pairs_hook=strict_pairs,
        parse_int=strict_integer,
        parse_float=lambda token: (_ for _ in ()).throw(ValueError(f"floating JSON number forbidden: {token}")),
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    require(isinstance(value, dict), f"top-level object: {path.name}")
    validate_json_tree(value)
    return value


def load_documents() -> dict[str, dict[str, Any]]:
    for name, expected in UPSTREAM_PINS.items():
        require(sha256(HERE / name) == expected, f"upstream pin mismatch: {name}")
    documents: dict[str, dict[str, Any]] = {}
    for path in (ROUND102, ROUND111, ROUND112, ROUND113, ROUND114, ROUND115):
        document = strict_json(path)
        require(set(document) == {"schema", "result", "result_sha256"}, f"closed document: {path.name}")
        require(document["schema"] == UPSTREAM_SCHEMAS[path.name], f"schema: {path.name}")
        require(document["result_sha256"] == digest(document["result"]), f"result digest: {path.name}")
        documents[path.name] = document["result"]
    return documents


def repaired_endpoint_id(
    face_id: str,
    exterior_port_id: str,
    branch_key: list[Any],
    trace_id: str,
    hit_sheet_id: str,
    bypass_sheet_id: str,
) -> str:
    # Deliberately excludes the withdrawn Round102 endpoint ID.
    payload = [
        "cm2.round118.repaired-source-grazing-endpoint.v1",
        face_id,
        exterior_port_id,
        branch_key,
        trace_id,
        hit_sheet_id,
        bypass_sheet_id,
    ]
    return "physical-s0-rank3-repaired-source-grazing-endpoint:" + digest(payload)


def validate_round111_scope(audit: dict[str, Any]) -> None:
    rows = [row for row in audit["downstream_impact_rows"] if row["round"] == 102]
    require(len(rows) == 1, "one Round102 impact row")
    row = rows[0]
    require(row["status"] == "PARTIAL_COMBINATORIAL_FACE_LEDGER", "Round102 partial status")
    require(
        row["preserved"]
        == "12 face IDs, 120 registered ports, 108 internal links, and source-grazing event-type/candidate incidence",
        "Round102 preserved scope",
    )
    require("endpoint IDs" in row["affected"], "withdrawn endpoint IDs recorded")
    require("whole-domain physical completeness" in row["affected"], "withdrawn physical completeness recorded")


def build_rows(documents: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    r102 = documents[ROUND102.name]
    r112 = documents[ROUND112.name]
    r113 = documents[ROUND113.name]
    r114 = documents[ROUND114.name]
    r115 = documents[ROUND115.name]

    require(r102["corrected_rank3_physical_face_count"] == 12, "Round102 face count")
    require(r102["corrected_face_registered_port_count"] == 120, "Round102 port count")
    require(r102["corrected_face_interior_link_count"] == 108, "Round102 link count")
    source_incidence = [row for row in r102["endpoint_incidence_rows"] if row["endpoint_type"] == "SOURCE_GRAZING"]
    require(len(source_incidence) == 8, "Round102 source-grazing incidence count")
    require(r112["certified_hit_root_sheet_count"] == 8, "Round112 HIT count")
    require(r112["certified_bypass_root_sheet_count"] == 8, "Round112 BYPASS count")
    require(r113["natural_boundary_trace_row_count"] == 8, "Round113 natural trace count")
    require(r114["certified_source_chart_seam_bridge_count"] == 8, "Round114 seam count")
    require(r114["certified_selected_lift_root_edge_stitch_count"] == 8, "Round114 root stitch count")
    require(r115["certified_selected_lift_whole_trace_no_fold_atlas_count"] == 8, "Round115 nofold count")

    face_by_id = {row["face_id"]: row for row in r102["face_rows"]}
    incidence_by_port = {row["mated_registered_port_id"]: row for row in source_incidence}
    natural_by_port = {row["exterior_port_id"]: row for row in r113["natural_boundary_trace_rows"]}
    seam_by_port = {row["exterior_port_id"]: row for row in r114["source_chart_seam_bridge_rows"]}
    stitch_by_port = {row["exterior_port_id"]: row for row in r114["root_edge_stitch_rows"]}
    root_by_port = {row["exterior_port_id"]: row for row in r115["root_edge_rows"]}
    sheet_by_id = {row["sheet_id"]: row for row in r112["sheet_rows"]}
    for label, index in (
        ("incidence", incidence_by_port),
        ("natural", natural_by_port),
        ("seam", seam_by_port),
        ("stitch", stitch_by_port),
        ("root", root_by_port),
    ):
        require(len(index) == 8, f"unique {label} port index")

    rows: list[dict[str, Any]] = []
    for root in sorted(r115["root_edge_rows"], key=lambda row: row["ray_index"]):
        port = root["exterior_port_id"]
        incidence = incidence_by_port[port]
        face = face_by_id[incidence["face_id"]]
        natural = natural_by_port[port]
        seam = seam_by_port[port]
        stitch = stitch_by_port[port]
        hit = sheet_by_id[natural["incident_hit_sheet_id"]]
        bypass = sheet_by_id[natural["incident_bypass_sheet_id"]]
        branch = root["branch_key"]
        face_branch = [
            face["source_core_index"],
            face["second_selected_target_id"],
            face["third_candidate_id"],
            face["signed_transverse_tangency_factor_sign"],
        ]
        require(branch == face_branch, f"preserved face branch join: {port}")
        require(branch == natural["branch_key"] == seam["branch_key"] == stitch["branch_key"], f"branch join: {port}")
        require(branch == hit["branch_key"] == bypass["branch_key"], f"sheet branch join: {port}")
        require(hit["sheet_kind"] == "HIT" and bypass["sheet_kind"] == "BYPASS", f"sheet kinds: {port}")
        require(stitch["hit_sheet_id"] == hit["sheet_id"], f"HIT stitch: {port}")
        require(stitch["bypass_sheet_id"] == bypass["sheet_id"], f"BYPASS stitch: {port}")
        require(incidence["projective_end"] == seam["projective_end"] == stitch["projective_end"], f"projective end: {port}")
        require(incidence["adjacent_source_chart"] == seam["adjacent_source_chart"], f"adjacent chart: {port}")
        require(root["source_chart"] == f"G:{seam['adjacent_source_chart']}", f"root source chart: {port}")
        require(hit["source_chart"] == root["source_chart"] == bypass["source_chart"], f"sheet source chart: {port}")
        require(frozenset((seam["old_source_chart"], seam["adjacent_source_chart"])) in ADJACENT_CHART_PAIRS, f"adjacent chart pair: {port}")
        require(seam["physical_selected_owner_clearance_replayed"] is True, f"seam clearance: {port}")
        require(Q(seam["strict_positive_parameter_width"]) > 0, f"seam positive width: {port}")
        require(stitch["continuous_edge_image_covers_tail_and_reaches_unique_corner"] is True, f"root coverage: {port}")
        require(root["root_edge_q_injective"] is True, f"q injectivity: {port}")
        require(root["selected_lift_whole_trace_no_fold_atlas_installed"] is True, f"nofold: {port}")
        require(root["certified_uniform_q_prime_over_c0_abs_lower_bound"] == "1/1000", f"qprime/c: {port}")
        require(root["root_q_abs_second_derivative_upper_bound"] == "10", f"qsecond: {port}")
        require(root["corner_stationary_identity"] == "q_prime(0)=0_EXACT_BY_SOURCE_GRAZING_FLOW_SHIFT", f"stationary q: {port}")
        require(root["root_coordinate_interval"] == ["0", "1/16384"], f"root interval: {port}")
        for false_key in (
            "physical_owner_atlas_installed",
            "positive_reach_installed",
            "two_sided_physical_collar_installed",
            "uniform_other_singularity_separation_installed",
        ):
            require(root[false_key] is False, f"inherited nonclaim {false_key}: {port}")

        repaired_id = repaired_endpoint_id(
            face["face_id"], port, branch, natural["trace_id"], hit["sheet_id"], bypass["sheet_id"]
        )
        qprime_sign = root["q_prime_sign_for_c0_positive"]
        sigma0 = root["source_grazing_sign_sigma0"]
        require(qprime_sign in (-1, 1) and sigma0 in (-1, 1), f"transition signs: {port}")
        rows.append(
            {
                "ray_index": root["ray_index"],
                "face_id": face["face_id"],
                "exterior_port_id": port,
                "branch_key": branch,
                "projective_end": stitch["projective_end"],
                "round102_preserved_incidence_type": "SOURCE_GRAZING",
                "withdrawn_round102_endpoint_id": incidence["endpoint_id"],
                "withdrawn_round102_endpoint_id_status": "TRACEABILITY_ONLY_NOT_REUSED",
                "round102_endpoint_complete_claim_used": False,
                "round102_terminal_bracket_used": False,
                "repaired_endpoint_id": repaired_id,
                "repaired_id_payload_excludes_withdrawn_alias": True,
                "round113_natural_trace_id": natural["trace_id"],
                "round112_hit_sheet_id": hit["sheet_id"],
                "round112_bypass_sheet_id": bypass["sheet_id"],
                "round114_root_edge_stitch_joined": True,
                "round115_selected_lift_nofold_joined": True,
                "source_component": "G",
                "source_radius": "9/25",
                "old_source_chart": seam["old_source_chart"],
                "adjacent_source_chart": seam["adjacent_source_chart"],
                "adjacent_source_chart_id": root["source_chart"],
                "old_and_adjacent_chart_union_angular_span_upper_bound": "pi",
                "seam_selected_owner_clearance_replayed": True,
                "source_grazing_sign_sigma0": sigma0,
                "q_prime_sign_for_c0_positive": qprime_sign,
                "p_prime_sign_for_c0_positive": -sigma0,
                "q_as_function_of_p_derivative_sign_for_c0_positive": -qprime_sign * sigma0,
                "endpoint_c0_zero_kept_in_singularity_ledger": True,
                "physical_owner_whole_trace_atlas_installed": False,
                "whole_trace_positive_reach_installed": False,
                "two_sided_physical_collar_installed": False,
                "whole_face_source_cylinder_transfer_installed": False,
            }
        )

    repaired_ids = [row["repaired_endpoint_id"] for row in rows]
    withdrawn_ids = [row["withdrawn_round102_endpoint_id"] for row in rows]
    require(len(rows) == len(set(repaired_ids)) == len(set(withdrawn_ids)) == 8, "unique endpoint identities")
    require(set(repaired_ids).isdisjoint(withdrawn_ids), "repaired IDs disjoint from withdrawn aliases")
    require([row["ray_index"] for row in rows] == list(range(8)), "ray index sequence")
    return rows


def source_cylinder_transfer_theorem() -> dict[str, Any]:
    radius = Q(9, 25)
    # pi < 22/7 proves R*pi/2 < 1, hence R*Delta(theta) is no
    # larger than the unit-circle chord for Delta(theta) <= pi.
    require(radius * Q(22, 7) / 2 < 1, "rational chord/arc proof")
    return {
        "applies_only_within_each_repaired_old_adjacent_chart_union": True,
        "source_component": "G",
        "source_component_tag_is_mandatory": True,
        "source_radius": "9/25",
        "physical_unwrapped_coordinate": "(G,r=(9/25)*theta,p)",
        "physical_source_cylinder_metric": "d_phys^2=(9/25)^2*dtheta^2+dp^2",
        "unit_normal_reference_coordinate": "(G,n_x(theta),n_y(theta),p)",
        "unit_normal_reference_metric": "d_ref^2=||n(theta_1)-n(theta_2)||^2+|p_1-p_2|^2",
        "chart_union_unwrapped_angular_span_upper_bound": "pi",
        "distance_lower_factor_physical_over_reference": "9/25",
        "distance_upper_factor_physical_over_reference": "1",
        "inverse_distance_upper_factor_reference_over_physical": "25/9",
        "first_derivative_lower_factor_physical_over_reference": "9/25",
        "first_derivative_upper_factor_physical_over_reference": "1",
        "second_derivative_upper_factor_physical_over_reference": "1",
        "distance_identity": "(9/25)*d_ref <= d_phys <= d_ref",
        "first_derivative_identity": "(9/25)*|M_prime| <= |P_prime| <= |M_prime|",
        "second_derivative_identity": "|P_second| <= |M_second|",
        "chord_arc_proof": "for 0<=Delta_theta<=pi, chord<=Delta_theta and (9/25)*Delta_theta<=chord because (9/25)*pi/2<1, certified using pi<22/7",
        "second_derivative_proof": "||n_second||^2=theta_second^2+theta_prime^4, so |((9/25)*theta_second,p_second)|<=|(n_second,p_second)|",
        "physical_metric_is_not_the_unit_normal_reference_metric": True,
        "whole_face_transfer_installed": False,
    }


def q_to_p_transfer_theorem() -> dict[str, Any]:
    cmax = Q(1, 16384)
    require(1 - cmax * cmax > Q(1000, 1001) ** 2, "sqrt lower bound")
    return {
        "root_coordinate_interval": ["0", "1/16384"],
        "momentum_identity": "p(c0)=sigma0*sqrt(1-c0^2)",
        "momentum_derivative_identity_for_c0_positive": "dp/dc0=-sigma0*c0/sqrt(1-c0^2)",
        "projective_corner_stationary_identity": "q_prime(0)=0",
        "inherited_strict_q_prime_over_c0_abs_lower_bound": "1/1000",
        "inherited_strict_q_second_abs_upper_bound": "10",
        "derived_q_prime_over_c0_abs_upper_bound_for_c0_positive": "10",
        "derived_abs_dq_dp_identity_for_c0_positive": "|dq/dp|=|q_prime/c0|*sqrt(1-c0^2)",
        "sqrt_factor_strict_lower_bound": "1000/1001",
        "abs_dq_dp_strict_lower_bound": "1/1001",
        "abs_dq_dp_strict_upper_bound": "10",
        "closed_interval_finite_difference_bilipschitz_installed": True,
        "closed_interval_finite_difference_identity": "1/1001<|Delta_q/Delta_p|<10 for distinct c0 values, including one endpoint c0=0",
        "q_as_function_of_p_C1_endpoint_extension_installed": True,
        "q_as_function_of_p_C2_claim_installed": False,
        "C2_nonclaim_reason": "Round115 supplies q_second but not the q_third/odd-term control needed for a C2 q-to-p endpoint transfer",
        "positive_c0_overlap_only_for_derivative_formula": True,
        "endpoint_c0_zero_remains_source_grazing_singular": True,
        "closed_endpoint_positive_two_sided_collar_inferred": False,
    }


def build_result() -> dict[str, Any]:
    documents = load_documents()
    validate_round111_scope(documents[ROUND111.name])
    rows = build_rows(documents)
    return {
        "arithmetic": "exact rational structural replay; no floating-point acceptance predicate",
        "input_round102_source_grazing_incidence_count": 8,
        "input_round113_natural_boundary_trace_count": 8,
        "input_round114_source_chart_seam_bridge_count": 8,
        "input_round114_root_edge_stitch_count": 8,
        "input_round115_selected_lift_nofold_count": 8,
        "repaired_endpoint_identity_count": 8,
        "unique_face_port_trace_sheet_root_join_count": 8,
        "withdrawn_round102_endpoint_id_reuse_count": 0,
        "repaired_endpoint_rows": rows,
        "repaired_endpoint_rows_sha256": digest(rows),
        "source_cylinder_transfer_theorem": source_cylinder_transfer_theorem(),
        "q_to_p_transfer_theorem": q_to_p_transfer_theorem(),
        "round102_preserved_contract_used": "source-grazing event-type/candidate incidence plus preserved face IDs only",
        "round102_withdrawn_contract_not_used": "terminal brackets, endpoint IDs, endpoint completeness, whole-domain completeness, and zero-residual claims",
        "endpoint_identity_crosswalk_installed": True,
        "physical_owner_whole_trace_atlas_installed": False,
        "whole_trace_positive_reach_installed": False,
        "whole_trace_uniform_other_singularity_separation_installed": False,
        "whole_face_source_cylinder_transfer_installed": False,
        "whole_face_collar_installed": False,
        "two_sided_physical_collar_installed": False,
        "actual_standard_curve_child_count": 0,
        "canonical_curve_recut_instance_count": 0,
        "gate5_child_field_counts": {f"F{i}": 0 for i in range(1, 7)},
        "gate5_global_maturity": "10/18",
        "gate5_block_count": 0,
        "cm2_verdict": "NO-GO_FOR_CLAIM",
        "strict_scope": "eight repaired source-grazing endpoint identities, their exact upstream crosswalk, the local old/adjacent G-chart source-cylinder metric transfer, and the Round115 q-to-p C1 endpoint transition",
        "strict_nonclaims": [
            "withdrawn Round102 endpoint IDs are traceability aliases only and are not repaired by reuse",
            "the transfer is local to each audited old/adjacent source-chart union and is not a whole-face atlas",
            "the physical source-cylinder metric is (9/25)^2*dtheta^2+dp^2, not the unit-normal reference metric",
            "c0=0 remains a source-grazing singular endpoint and supplies no uniform positive closed-endpoint two-sided collar",
            "the q-to-p transition is C1/bi-Lipschitz at the endpoint; no C2 q-to-p transfer is installed",
            "no whole-trace physical-owner atlas, reach, other-singularity separation, collar, standard-curve child, canonical recut, or Gate5 field is installed",
        ],
        "upstream_and_formula_pins": dict(sorted(UPSTREAM_PINS.items())),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = build_result()
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "repaired_endpoint_identity_count": result["repaired_endpoint_identity_count"],
                "result_sha256": document["result_sha256"],
                "cm2_verdict": result["cm2_verdict"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
