#!/usr/bin/env python3
"""Independent fail-closed verifier for the Round118 transfer atlas.

The verifier does not import the producer.  It reparses every pinned upstream
certificate with duplicate-key/NaN rejection, rebuilds all eight joins and
repaired identifiers, replays the exact rational transfer bounds, and executes
hostile signed-document mutations.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PRODUCER = HERE / "cm2_round118_rank3_repaired_endpoint_source_cylinder_transfer_atlas.py"
CERTIFICATE = HERE / "cm2-round118-rank3-repaired-endpoint-source-cylinder-transfer-atlas-2026-07-23.json"
OUTPUT = HERE / "cm2-round118-rank3-repaired-endpoint-source-cylinder-transfer-atlas-verification-2026-07-23.json"
SCHEMA = "cm2.round118.rank3-repaired-endpoint-source-cylinder-transfer-atlas.v1"
VERIFY_SCHEMA = "cm2.round118.rank3-repaired-endpoint-source-cylinder-transfer-atlas-verification.v1"
PRODUCER_SHA256 = "bfd517d6dd71aa923ed89400719302bd022945db9cce38e4b74f163ed0fa45f4"
CERTIFICATE_SHA256 = "91bd73445fd13eeb759e932b0626ba64acef1f10a061d6d416577dfd96feb34f"

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
    frozenset(("E", "N")), frozenset(("N", "W")),
    frozenset(("W", "S")), frozenset(("S", "E")),
}

STRICT_NONCLAIMS = [
    "withdrawn Round102 endpoint IDs are traceability aliases only and are not repaired by reuse",
    "the transfer is local to each audited old/adjacent source-chart union and is not a whole-face atlas",
    "the physical source-cylinder metric is (9/25)^2*dtheta^2+dp^2, not the unit-normal reference metric",
    "c0=0 remains a source-grazing singular endpoint and supplies no uniform positive closed-endpoint two-sided collar",
    "the q-to-p transition is C1/bi-Lipschitz at the endpoint; no C2 q-to-p transfer is installed",
    "no whole-trace physical-owner atlas, reach, other-singularity separation, collar, standard-curve child, canonical recut, or Gate5 field is installed",
]


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def require_exact_int(value: Any, expected: int, message: str) -> None:
    require(type(value) is int and value == expected, message)


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


def strict_json_text(text: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=strict_pairs,
        parse_int=strict_integer,
        parse_float=lambda token: (_ for _ in ()).throw(ValueError(f"floating JSON number forbidden: {token}")),
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    require(isinstance(value, dict), "top-level JSON object")
    validate_json_tree(value)
    return value


def strict_json(path: Path) -> dict[str, Any]:
    return strict_json_text(path.read_text())


def load_upstreams() -> dict[str, dict[str, Any]]:
    for name, expected in UPSTREAM_PINS.items():
        require(sha256(HERE / name) == expected, f"upstream pin mismatch: {name}")
    results: dict[str, dict[str, Any]] = {}
    for path in (ROUND102, ROUND111, ROUND112, ROUND113, ROUND114, ROUND115):
        document = strict_json(path)
        require(set(document) == {"schema", "result", "result_sha256"}, f"closed upstream: {path.name}")
        require(document["schema"] == UPSTREAM_SCHEMAS[path.name], f"upstream schema: {path.name}")
        require(document["result_sha256"] == digest(document["result"]), f"upstream result digest: {path.name}")
        results[path.name] = document["result"]
    return results


def endpoint_id(face: str, port: str, branch: list[Any], trace: str, hit: str, bypass: str) -> str:
    payload = [
        "cm2.round118.repaired-source-grazing-endpoint.v1",
        face, port, branch, trace, hit, bypass,
    ]
    return "physical-s0-rank3-repaired-source-grazing-endpoint:" + digest(payload)


def audit_withdrawal(upstreams: dict[str, dict[str, Any]]) -> None:
    audit = upstreams[ROUND111.name]
    selected = [row for row in audit["downstream_impact_rows"] if row.get("round") == 102]
    require(len(selected) == 1, "Round111 has exactly one Round102 impact row")
    impact = selected[0]
    require(impact["status"] == "PARTIAL_COMBINATORIAL_FACE_LEDGER", "Round102 partial-ledger status")
    require(
        impact["preserved"]
        == "12 face IDs, 120 registered ports, 108 internal links, and source-grazing event-type/candidate incidence",
        "preserved Round102 scope",
    )
    for phrase in ("endpoint IDs", "endpoint completeness", "whole-domain physical completeness", "zero-residual claims"):
        require(phrase in impact["affected"], f"withdrawn Round102 phrase: {phrase}")


def reconstruct_rows(upstreams: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    a = upstreams[ROUND102.name]
    b = upstreams[ROUND112.name]
    c = upstreams[ROUND113.name]
    d = upstreams[ROUND114.name]
    e = upstreams[ROUND115.name]
    require_exact_int(a["corrected_rank3_physical_face_count"], 12, "Round102 face count/type")
    require_exact_int(a["corrected_face_registered_port_count"], 120, "Round102 port count/type")
    require_exact_int(a["corrected_face_interior_link_count"], 108, "Round102 link count/type")
    incidences = [row for row in a["endpoint_incidence_rows"] if row.get("endpoint_type") == "SOURCE_GRAZING"]
    require(len(incidences) == 8, "eight source-grazing incidences")
    require_exact_int(b["certified_hit_root_sheet_count"], 8, "Round112 HIT count/type")
    require_exact_int(b["certified_bypass_root_sheet_count"], 8, "Round112 BYPASS count/type")
    require_exact_int(c["natural_boundary_trace_row_count"], 8, "Round113 trace count/type")
    require_exact_int(d["certified_source_chart_seam_bridge_count"], 8, "Round114 seam count/type")
    require_exact_int(d["certified_selected_lift_root_edge_stitch_count"], 8, "Round114 stitch count/type")
    require_exact_int(e["certified_selected_lift_whole_trace_no_fold_atlas_count"], 8, "Round115 nofold count/type")

    def unique(rows: list[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
        index = {row[key]: row for row in rows}
        require(len(index) == len(rows), f"unique {label}")
        return index

    incidence = unique(incidences, "mated_registered_port_id", "source incidence port")
    faces = unique(a["face_rows"], "face_id", "face ID")
    sheets = unique(b["sheet_rows"], "sheet_id", "sheet ID")
    natural = unique(c["natural_boundary_trace_rows"], "exterior_port_id", "natural trace port")
    seam = unique(d["source_chart_seam_bridge_rows"], "exterior_port_id", "seam port")
    stitch = unique(d["root_edge_stitch_rows"], "exterior_port_id", "stitch port")
    roots = unique(e["root_edge_rows"], "exterior_port_id", "root port")
    require(all(len(index) == 8 for index in (incidence, natural, seam, stitch, roots)), "eight-row join indices")

    rebuilt: list[dict[str, Any]] = []
    for ray, rr in enumerate(sorted(roots.values(), key=lambda row: row["ray_index"])):
        require_exact_int(rr["ray_index"], ray, "contiguous typed ray indices")
        port = rr["exterior_port_id"]
        inc = incidence[port]
        face = faces[inc["face_id"]]
        nt = natural[port]
        sb = seam[port]
        rs = stitch[port]
        hs = sheets[nt["incident_hit_sheet_id"]]
        bs = sheets[nt["incident_bypass_sheet_id"]]
        branch = rr["branch_key"]
        face_branch = [face["source_core_index"], face["second_selected_target_id"], face["third_candidate_id"], face["signed_transverse_tangency_factor_sign"]]
        require(branch == face_branch == nt["branch_key"] == sb["branch_key"] == rs["branch_key"] == hs["branch_key"] == bs["branch_key"], f"seven-way branch equality: ray {ray}")
        require(hs["sheet_kind"] == "HIT" and bs["sheet_kind"] == "BYPASS", f"sheet kind: ray {ray}")
        require((rs["hit_sheet_id"], rs["bypass_sheet_id"]) == (hs["sheet_id"], bs["sheet_id"]), f"sheet/stitch join: ray {ray}")
        require(inc["projective_end"] == sb["projective_end"] == rs["projective_end"], f"projective end: ray {ray}")
        require(inc["adjacent_source_chart"] == sb["adjacent_source_chart"], f"adjacent chart: ray {ray}")
        require(frozenset((sb["old_source_chart"], sb["adjacent_source_chart"])) in ADJACENT_CHART_PAIRS, f"chart adjacency: ray {ray}")
        expected_chart = "G:" + sb["adjacent_source_chart"]
        require(rr["source_chart"] == hs["source_chart"] == bs["source_chart"] == expected_chart, f"G chart equality: ray {ray}")
        require(sb["physical_selected_owner_clearance_replayed"] is True and Q(sb["strict_positive_parameter_width"]) > 0, f"seam evidence: ray {ray}")
        require(rs["continuous_edge_image_covers_tail_and_reaches_unique_corner"] is True, f"root coverage: ray {ray}")
        require(rr["root_edge_q_injective"] is True and rr["selected_lift_whole_trace_no_fold_atlas_installed"] is True, f"Round115 join: ray {ray}")
        require(rr["certified_uniform_q_prime_over_c0_abs_lower_bound"] == "1/1000", f"qprime/c bound: ray {ray}")
        require(rr["root_q_abs_second_derivative_upper_bound"] == "10", f"qsecond bound: ray {ray}")
        require(rr["corner_stationary_identity"] == "q_prime(0)=0_EXACT_BY_SOURCE_GRAZING_FLOW_SHIFT", f"q corner: ray {ray}")
        require(rr["root_coordinate_interval"] == ["0", "1/16384"], f"c interval: ray {ray}")
        for flag in ("physical_owner_atlas_installed", "positive_reach_installed", "two_sided_physical_collar_installed", "uniform_other_singularity_separation_installed"):
            require(rr[flag] is False, f"upstream nonclaim {flag}: ray {ray}")
        sigma = rr["source_grazing_sign_sigma0"]
        qsign = rr["q_prime_sign_for_c0_positive"]
        require(sigma in (-1, 1) and qsign in (-1, 1), f"transition signs: ray {ray}")
        repaired = endpoint_id(face["face_id"], port, branch, nt["trace_id"], hs["sheet_id"], bs["sheet_id"])
        rebuilt.append({
            "ray_index": ray,
            "face_id": face["face_id"],
            "exterior_port_id": port,
            "branch_key": branch,
            "projective_end": rs["projective_end"],
            "round102_preserved_incidence_type": "SOURCE_GRAZING",
            "withdrawn_round102_endpoint_id": inc["endpoint_id"],
            "withdrawn_round102_endpoint_id_status": "TRACEABILITY_ONLY_NOT_REUSED",
            "round102_endpoint_complete_claim_used": False,
            "round102_terminal_bracket_used": False,
            "repaired_endpoint_id": repaired,
            "repaired_id_payload_excludes_withdrawn_alias": True,
            "round113_natural_trace_id": nt["trace_id"],
            "round112_hit_sheet_id": hs["sheet_id"],
            "round112_bypass_sheet_id": bs["sheet_id"],
            "round114_root_edge_stitch_joined": True,
            "round115_selected_lift_nofold_joined": True,
            "source_component": "G",
            "source_radius": "9/25",
            "old_source_chart": sb["old_source_chart"],
            "adjacent_source_chart": sb["adjacent_source_chart"],
            "adjacent_source_chart_id": expected_chart,
            "old_and_adjacent_chart_union_angular_span_upper_bound": "pi",
            "seam_selected_owner_clearance_replayed": True,
            "source_grazing_sign_sigma0": sigma,
            "q_prime_sign_for_c0_positive": qsign,
            "p_prime_sign_for_c0_positive": -sigma,
            "q_as_function_of_p_derivative_sign_for_c0_positive": -qsign * sigma,
            "endpoint_c0_zero_kept_in_singularity_ledger": True,
            "physical_owner_whole_trace_atlas_installed": False,
            "whole_trace_positive_reach_installed": False,
            "two_sided_physical_collar_installed": False,
            "whole_face_source_cylinder_transfer_installed": False,
        })
    new_ids = [row["repaired_endpoint_id"] for row in rebuilt]
    old_ids = [row["withdrawn_round102_endpoint_id"] for row in rebuilt]
    require(len(set(new_ids)) == len(set(old_ids)) == 8 and set(new_ids).isdisjoint(old_ids), "new/old endpoint ID separation")
    return rebuilt


def expected_metric_theorem() -> dict[str, Any]:
    require(Q(9, 25) * Q(22, 7) / 2 < 1, "pi<22/7 chord/arc rational check")
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


def expected_qp_theorem() -> dict[str, Any]:
    cmax = Q(1, 16384)
    require(1 - cmax * cmax > Q(1000, 1001) ** 2, "exact sqrt-factor check")
    require(Q(1, 1000) * Q(1000, 1001) == Q(1, 1001), "exact dq/dp lower product")
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


def verify_contract(document: dict[str, Any], upstreams: dict[str, dict[str, Any]]) -> dict[str, Any]:
    require(set(document) == {"schema", "result", "result_sha256"}, "certificate document keys")
    require(document["schema"] == SCHEMA, "certificate schema")
    result = document["result"]
    require(isinstance(result, dict) and document["result_sha256"] == digest(result), "certificate result digest")
    expected_keys = {
        "arithmetic", "input_round102_source_grazing_incidence_count",
        "input_round113_natural_boundary_trace_count", "input_round114_source_chart_seam_bridge_count",
        "input_round114_root_edge_stitch_count", "input_round115_selected_lift_nofold_count",
        "repaired_endpoint_identity_count", "unique_face_port_trace_sheet_root_join_count",
        "withdrawn_round102_endpoint_id_reuse_count", "repaired_endpoint_rows",
        "repaired_endpoint_rows_sha256", "source_cylinder_transfer_theorem", "q_to_p_transfer_theorem",
        "round102_preserved_contract_used", "round102_withdrawn_contract_not_used",
        "endpoint_identity_crosswalk_installed", "physical_owner_whole_trace_atlas_installed",
        "whole_trace_positive_reach_installed", "whole_trace_uniform_other_singularity_separation_installed",
        "whole_face_source_cylinder_transfer_installed", "whole_face_collar_installed",
        "two_sided_physical_collar_installed", "actual_standard_curve_child_count",
        "canonical_curve_recut_instance_count", "gate5_child_field_counts", "gate5_global_maturity",
        "gate5_block_count", "cm2_verdict", "strict_scope", "strict_nonclaims",
        "upstream_and_formula_pins",
    }
    require(set(result) == expected_keys, "closed result key set")
    require(result["arithmetic"] == "exact rational structural replay; no floating-point acceptance predicate", "arithmetic mode")
    for key in (
        "input_round102_source_grazing_incidence_count",
        "input_round113_natural_boundary_trace_count",
        "input_round114_source_chart_seam_bridge_count",
        "input_round114_root_edge_stitch_count",
        "input_round115_selected_lift_nofold_count",
        "repaired_endpoint_identity_count",
        "unique_face_port_trace_sheet_root_join_count",
    ):
        require_exact_int(result[key], 8, f"typed eight-row count: {key}")
    require_exact_int(result["withdrawn_round102_endpoint_id_reuse_count"], 0, "typed zero withdrawn-ID reuse")
    audit_withdrawal(upstreams)
    rows = reconstruct_rows(upstreams)
    require(result["repaired_endpoint_rows"] == rows, "independent eight-row reconstruction")
    require(result["repaired_endpoint_rows_sha256"] == digest(rows), "row digest")
    require(result["source_cylinder_transfer_theorem"] == expected_metric_theorem(), "exact source-cylinder theorem")
    require(result["q_to_p_transfer_theorem"] == expected_qp_theorem(), "exact q-to-p theorem")
    require(result["round102_preserved_contract_used"] == "source-grazing event-type/candidate incidence plus preserved face IDs only", "Round102 allowed use")
    require(result["round102_withdrawn_contract_not_used"] == "terminal brackets, endpoint IDs, endpoint completeness, whole-domain completeness, and zero-residual claims", "Round102 disallowed use")
    require(result["endpoint_identity_crosswalk_installed"] is True, "identity crosswalk")
    for flag in (
        "physical_owner_whole_trace_atlas_installed", "whole_trace_positive_reach_installed",
        "whole_trace_uniform_other_singularity_separation_installed",
        "whole_face_source_cylinder_transfer_installed", "whole_face_collar_installed",
        "two_sided_physical_collar_installed",
    ):
        require(result[flag] is False, f"strict nonpromotion: {flag}")
    require_exact_int(result["actual_standard_curve_child_count"], 0, "typed actual child count")
    require_exact_int(result["canonical_curve_recut_instance_count"], 0, "typed recut count")
    require(set(result["gate5_child_field_counts"]) == {f"F{i}" for i in range(1, 7)}, "F1-F6 key set")
    for key, value in result["gate5_child_field_counts"].items():
        require_exact_int(value, 0, f"typed zero Gate5 field: {key}")
    require(result["gate5_global_maturity"] == "10/18", "Gate5 maturity unchanged")
    require_exact_int(result["gate5_block_count"], 0, "typed zero Gate5 blocks")
    require(result["cm2_verdict"] == "NO-GO_FOR_CLAIM", "CM2 no-go")
    require(result["strict_scope"] == "eight repaired source-grazing endpoint identities, their exact upstream crosswalk, the local old/adjacent G-chart source-cylinder metric transfer, and the Round115 q-to-p C1 endpoint transition", "strict scope")
    require(result["strict_nonclaims"] == STRICT_NONCLAIMS, "strict nonclaims")
    require(result["upstream_and_formula_pins"] == dict(sorted(UPSTREAM_PINS.items())), "pin map")
    return result


def hostile_tests(document: dict[str, Any], upstreams: dict[str, dict[str, Any]]) -> list[str]:
    passed: list[str] = []

    def reject(label: str, mutate: Callable[[dict[str, Any]], None], resign: bool = True) -> None:
        mutant = copy.deepcopy(document)
        mutate(mutant)
        if resign:
            mutant["result_sha256"] = digest(mutant["result"])
        try:
            verify_contract(mutant, upstreams)
        except (RuntimeError, KeyError, ValueError, TypeError, IndexError):
            passed.append(label)
            return
        raise RuntimeError(f"hostile mutation accepted: {label}")

    reject("schema substitution", lambda d: d.__setitem__("schema", "cm2.fake"), resign=False)
    reject("unsigned result mutation", lambda d: d["result"].__setitem__("cm2_verdict", "GO"), resign=False)
    reject("withdrawn endpoint ID reuse", lambda d: d["result"]["repaired_endpoint_rows"][0].__setitem__("repaired_endpoint_id", d["result"]["repaired_endpoint_rows"][0]["withdrawn_round102_endpoint_id"]))
    reject("repaired endpoint ID substitution", lambda d: d["result"]["repaired_endpoint_rows"][0].__setitem__("repaired_endpoint_id", "physical-s0-rank3-repaired-source-grazing-endpoint:" + "0" * 64))
    reject("face join substitution", lambda d: d["result"]["repaired_endpoint_rows"][0].__setitem__("face_id", d["result"]["repaired_endpoint_rows"][1]["face_id"]))
    reject("port join substitution", lambda d: d["result"]["repaired_endpoint_rows"][0].__setitem__("exterior_port_id", d["result"]["repaired_endpoint_rows"][1]["exterior_port_id"]))
    reject("trace join substitution", lambda d: d["result"]["repaired_endpoint_rows"][0].__setitem__("round113_natural_trace_id", d["result"]["repaired_endpoint_rows"][1]["round113_natural_trace_id"]))
    reject("chart adjacency collapse", lambda d: d["result"]["repaired_endpoint_rows"][0].__setitem__("old_source_chart", d["result"]["repaired_endpoint_rows"][0]["adjacent_source_chart"]))
    reject("source component substitution", lambda d: d["result"]["repaired_endpoint_rows"][0].__setitem__("source_component", "W"))
    reject("radius substitution", lambda d: d["result"]["source_cylinder_transfer_theorem"].__setitem__("source_radius", "4/25"))
    reject("physical metric substitution", lambda d: d["result"]["source_cylinder_transfer_theorem"].__setitem__("physical_source_cylinder_metric", "dtheta^2+dp^2"))
    reject("component tag removal", lambda d: d["result"]["source_cylinder_transfer_theorem"].__setitem__("source_component_tag_is_mandatory", False))
    reject("metric lower-bound inflation", lambda d: d["result"]["source_cylinder_transfer_theorem"].__setitem__("distance_lower_factor_physical_over_reference", "1/2"))
    reject("whole-face transfer promotion", lambda d: d["result"].__setitem__("whole_face_source_cylinder_transfer_installed", True))
    reject("q-to-p lower-bound inflation", lambda d: d["result"]["q_to_p_transfer_theorem"].__setitem__("abs_dq_dp_strict_lower_bound", "1/1000"))
    reject("q-to-p C2 promotion", lambda d: d["result"]["q_to_p_transfer_theorem"].__setitem__("q_as_function_of_p_C2_claim_installed", True))
    reject("endpoint collar promotion", lambda d: d["result"]["q_to_p_transfer_theorem"].__setitem__("closed_endpoint_positive_two_sided_collar_inferred", True))
    reject("singular ledger removal", lambda d: d["result"]["repaired_endpoint_rows"][0].__setitem__("endpoint_c0_zero_kept_in_singularity_ledger", False))
    reject("reach promotion", lambda d: d["result"].__setitem__("whole_trace_positive_reach_installed", True))
    reject("F1 promotion", lambda d: d["result"]["gate5_child_field_counts"].__setitem__("F1", 1))
    reject("boolean masquerading as zero reuse count", lambda d: d["result"].__setitem__("withdrawn_round102_endpoint_id_reuse_count", False))
    reject("boolean masquerading as zero child count", lambda d: d["result"].__setitem__("actual_standard_curve_child_count", False))
    reject("boolean masquerading as zero Gate5 field", lambda d: d["result"]["gate5_child_field_counts"].__setitem__("F2", False))
    reject("boolean masquerading as zero Gate5 block count", lambda d: d["result"].__setitem__("gate5_block_count", False))
    reject("Gate5 maturity inflation", lambda d: d["result"].__setitem__("gate5_global_maturity", "11/18"))
    reject("upstream pin substitution", lambda d: d["result"]["upstream_and_formula_pins"].__setitem__(ROUND111.name, "0" * 64))
    reject("row deletion", lambda d: d["result"]["repaired_endpoint_rows"].pop())
    reject("unknown row field", lambda d: d["result"]["repaired_endpoint_rows"][0].__setitem__("silent_row_promotion", True))
    reject("unknown result field", lambda d: d["result"].__setitem__("silent_promotion", True))

    for label, text in (
        ("duplicate JSON key rejection", '{"schema":1,"schema":2}'),
        ("deep duplicate JSON key rejection", '{"outer":{"inner":1,"inner":2}}'),
        ("floating JSON number rejection", '{"value":0.125}'),
        ("overflowing exponent JSON number rejection", '{"value":1e9999}'),
        ("NaN rejection", '{"value":NaN}'),
        ("Infinity rejection", '{"value":Infinity}'),
        ("negative Infinity rejection", '{"value":-Infinity}'),
        ("top-level array rejection", '[]'),
        ("top-level null rejection", 'null'),
        ("negative zero rejection", '{"value":-0}'),
        ("overlong integer rejection", '{"value":' + "9" * 257 + '}'),
        ("UTF-8 BOM rejection", '\ufeff{}'),
        ("unpaired surrogate rejection", r'{"value":"\ud800"}'),
    ):
        try:
            strict_json_text(text)
        except (RuntimeError, ValueError):
            passed.append(label)
        else:
            raise RuntimeError(f"hostile JSON accepted: {label}")
    return passed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    require(sha256(PRODUCER) == PRODUCER_SHA256, "producer byte pin")
    require(sha256(args.certificate) == CERTIFICATE_SHA256, "certificate byte pin")
    upstreams = load_upstreams()
    document = strict_json(args.certificate)
    result = verify_contract(document, upstreams)
    hostile = hostile_tests(document, upstreams)
    verification = {
        "status": "PASS",
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": document["result_sha256"],
        "upstream_and_formula_pin_count": len(UPSTREAM_PINS),
        "independent_verifier_imports_producer": False,
        "strict_json_duplicate_and_nonfinite_rejection": True,
        "independently_rebuilt_repaired_endpoint_identity_count": result["repaired_endpoint_identity_count"],
        "independently_replayed_unique_join_count": result["unique_face_port_trace_sheet_root_join_count"],
        "withdrawn_round102_endpoint_id_reuse_count": result["withdrawn_round102_endpoint_id_reuse_count"],
        "source_cylinder_exact_rational_transfer_replayed": True,
        "q_to_p_exact_rational_transition_replayed": True,
        "q_to_p_C2_nonclaim_preserved": True,
        "whole_face_reach_collar_and_owner_nonclaims_preserved": True,
        "gate5_child_field_counts": result["gate5_child_field_counts"],
        "gate5_global_maturity": result["gate5_global_maturity"],
        "cm2_verdict": result["cm2_verdict"],
        "hostile_mutation_test_count": len(hostile),
        "hostile_mutation_tests": hostile,
    }
    output_document = {
        "schema": VERIFY_SCHEMA,
        "result": verification,
        "result_sha256": digest(verification),
    }
    args.output.write_text(json.dumps(output_document, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(args.output), "status": "PASS", "hostile_tests": len(hostile)}, sort_keys=True))


if __name__ == "__main__":
    main()
