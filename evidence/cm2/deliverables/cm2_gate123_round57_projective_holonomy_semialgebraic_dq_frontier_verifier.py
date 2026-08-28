#!/usr/bin/env python3
"""Independent verifier for the CM2 Round-57 Gate-1/2/3 frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "deliverables" / (
    "cm2-gate123-round57-projective-holonomy-semialgebraic-dq-frontier-"
    "manifest-2026-07-20.json"
)
Q = Fraction

EXPECTED_DEPENDENCIES = {
    "deliverables/cm2-round56-independent-core-poles-and-r55-ledger-audit-2026-07-20.md":
        "d436a223f5aab4c719609ae8a1a87a254bdbd0f8eb8536463dc70f520ebaacdd",
    "deliverables/cm2-gate1-variable-diagonal-groupoid-frontier-assault-2026-07-17.md":
        "bbee54be4aea1df1d9b00a8a97145029ee68fd538aa44931dd2b21d1644c1fdd",
    "deliverables/cm2-gate1-round29-cross-term-rate-frontier-assault-2026-07-18.md":
        "9b1b52991640ec220c5296939cbf2c8d164242bbdc7d5fe90cea2eb683e1d61e",
    "deliverables/cm2-gate2-round25-product-base-assault-2026-07-18.md":
        "db75a6a8741d435182a1e0d0510e06d1b75b15eaba3d0c26e090e9c5990664e6",
    "deliverables/cm2-gate2-collision-key-stable-quotient-frontier-assault-2026-07-16.md":
        "1ca929145c53459a8e190b2b10a16a43a9d6e6b38c52b235c98af8e7b483112e",
    "deliverables/cm2-gate3-iterated-common-atlas-mt-dq-assault-2026-07-16.md":
        "235cf2c74ea3871a1d3862476d5e7d0ac506acc0e490ea5df12d8d2940c6b8f6",
    "deliverables/cm2-gate3-remaining-graph-complete-current-frontier-assault-2026-07-17.md":
        "51f046549b57ee7504399384e02ad2bd352260b15d503206fc7b82f8c3317a9e",
    "deliverables/cm2-gate3-common-graph-current-carrier-frontier-assault-2026-07-17.md":
        "cbe15f0535566c69c1e550a084d765fbac2a9e4c1aae01d54633d44dee506ae8",
    "deliverables/cm2-gate5-round53-trace-standard-family-graph-f17-frontier-assault-2026-07-20.md":
        "547a43c2b280e69544015056b367c118068318888e434520fe6b0b8acbfb83f8",
    "deliverables/cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
}


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def no_nonfinite(token: str) -> None:
    raise ValueError(f"non-finite token: {token}")


def strict_load_text(text: str) -> Any:
    return json.loads(text, object_pairs_hook=no_duplicates, parse_constant=no_nonfinite)


def load() -> dict[str, Any]:
    data = strict_load_text(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest root")
    return data


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def dependency_check(data: dict[str, Any]) -> None:
    rows = data.get("dependencies")
    if not isinstance(rows, list) or len(rows) != len(EXPECTED_DEPENDENCIES):
        raise ValueError("dependency cardinality")
    observed: dict[str, str] = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "sha256"}:
            raise ValueError("dependency row shape")
        rel, expected = row["path"], row["sha256"]
        if not isinstance(rel, str) or rel in observed:
            raise ValueError("dependency path")
        if not isinstance(expected, str) or len(expected) != 64:
            raise ValueError("dependency digest")
        observed[rel] = expected
    if observed != EXPECTED_DEPENDENCIES:
        raise ValueError("dependency registry drift")
    for rel, expected in EXPECTED_DEPENDENCIES.items():
        path = ROOT / rel
        if path.is_symlink() or not path.is_file() or sha256_path(path) != expected:
            raise ValueError(f"dependency integrity: {rel}")


def det(matrix: tuple[tuple[Q, Q], tuple[Q, Q]]) -> Q:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def inv(matrix: tuple[tuple[Q, Q], tuple[Q, Q]]) -> tuple[tuple[Q, Q], tuple[Q, Q]]:
    delta = det(matrix)
    if delta == 0:
        raise ValueError("singular replay matrix")
    return ((matrix[1][1] / delta, -matrix[0][1] / delta),
            (-matrix[1][0] / delta, matrix[0][0] / delta))


def mul(
    left: tuple[tuple[Q, Q], tuple[Q, Q]],
    right: tuple[tuple[Q, Q], tuple[Q, Q]],
) -> tuple[tuple[Q, Q], tuple[Q, Q]]:
    return tuple(tuple(sum(left[i][k] * right[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))  # type: ignore[return-value]


def gate1_replay(data: dict[str, Any]) -> None:
    gate = data["result"]["gate1"]
    if gate["physical_full_cross_common_vertex"] != "CERTIFIED":
        raise ValueError("Gate1 full-cross regression")
    if gate["weighted_projective_defect_compatibility_on_physical_combined_gauge"] != "NOT_CERTIFIED":
        raise ValueError("Gate1 weighted-defect promotion")
    if gate["same_representative_class_H_plus_twisting"] != "NOT_CERTIFIED":
        raise ValueError("Gate1 twisting promotion")
    if gate["official_status"] != "NOT_CERTIFIED":
        raise ValueError("Gate1 status")
    identity = gate["general_exact_identity"]
    if identity != {
        "D_x": "[[a_x,b_x],[c_x,e_x]]",
        "Delta_x": "a_x*e_x-b_x*c_x",
        "exact_rational_samples": 3,
        "p_x": "b_x/a_x",
        "pair_12": "a_y*a_x*(p_y-p_x)/Delta_x",
        "pair_21": "e_y*e_x*(q_y-q_x)/Delta_x",
        "q_x": "c_x/e_x",
    }:
        raise ValueError("Gate1 identity fields")

    # Independent rational rows, distinct from the producer's rows.
    rows = (
        (Q(7, 5), Q(-1, 4), Q(2, 9), Q(8, 7), Q(9, 8), Q(3, 10), Q(-2, 11), Q(5, 4)),
        (Q(11, 9), Q(2, 13), Q(-3, 14), Q(7, 6), Q(6, 5), Q(-1, 7), Q(4, 15), Q(10, 9)),
        (Q(5, 4), Q(-2, 17), Q(1, 12), Q(9, 8), Q(13, 11), Q(3, 16), Q(-1, 10), Q(7, 5)),
    )
    for ax, bx, cx, ex, ay, by, cy, ey in rows:
        dx, dy = ((ax, bx), (cx, ex)), ((ay, by), (cy, ey))
        pair = mul(dy, inv(dx))
        if pair[0][1] != ay * ax * (by / ay - bx / ax) / det(dx):
            raise ValueError("Gate1 independent upper identity")
        if pair[1][0] != ey * ex * (cy / ey - cx / ex) / det(dx):
            raise ValueError("Gate1 independent lower identity")

    gauges = gate["gauge_chart_replays"]
    if gauges != {
        "L_u_U_v": {"clean": "dv", "coupled": "du-u_y*u_x*dv"},
        "U_v_L_u": {"clean": "du", "coupled": "dv-v_y*du*v_x"},
        "additive": {"lower": "du/(1-u_x*v_x)", "upper": "dv/(1-u_x*v_x)"},
    }:
        raise ValueError("Gate1 gauge charts")
    counter = gate["uniformly_invertible_additive_countermodel"]
    if counter["normalized_lower_coordinate"] != ["1/10", "2/15"] * 4:
        raise ValueError("Gate1 additive oscillation")
    if counter["determinant_strict_lower"] != "29/40" or counter["converges"] is not False:
        raise ValueError("Gate1 additive guard")
    # Recompute the alternating normalized sequence and determinant lower.
    seq: list[Q] = []
    determinant_rows: list[Q] = []
    for n in range(8):
        rn = Q(1, 2) ** n
        ux, uy = Q(1, 2), Q(1, 2) + rn / 10
        vx = vy = Q(0) if n % 2 == 0 else Q(1, 2)
        dx, dy = ((1, vx), (ux, 1)), ((1, vy), (uy, 1))
        seq.append(mul(dy, inv(dx))[1][0] / rn)
        determinant_rows.extend((det(dx), det(dy)))
    if seq != [Q(1, 10), Q(2, 15)] * 4 or min(determinant_rows) != Q(29, 40):
        raise ValueError("Gate1 countermodel replay")


def gate2_replay(data: dict[str, Any]) -> None:
    gate = data["result"]["gate2"]
    if gate["candidate_cone_product_layers"] != "7/7_NON_OFFICIAL":
        raise ValueError("Gate2 candidate layers")
    if gate["official_immutable_fields"] != "0/17":
        raise ValueError("Gate2 field promotion")
    if gate["physical_stable_saturated_base_projection_holonomy"] != "NOT_CERTIFIED":
        raise ValueError("Gate2 physical promotion")
    if gate["official_status"] != "NOT_CERTIFIED":
        raise ValueError("Gate2 status")
    theorem = gate["conditional_holonomy_product_theorem"]
    if theorem["status"] != "CERTIFIED_CONDITIONAL_INTERFACE":
        raise ValueError("Gate2 theorem typing")
    full = Q(3) * Q(2) * Q(1, 8) / (1 - Q(1, 2))
    tails = [full * Q(1, 2) ** n for n in range(8)]
    if (full != Q(3, 2)
            or theorem["exact_sample_full_log_bound"] != "3/2"
            or theorem["exact_sample_tails"] != [str(x) for x in tails]):
        raise ValueError("Gate2 holonomy tail")
    separator = gate["finite_prefix_spanning_plaque_separator"]
    if separator["candidate_coordinate_tile_area"] != "1/163840000":
        raise ValueError("Gate2 tile area")
    rows = separator["rows"]
    if [row["agreed_regular_prefix_depth"] for row in rows] != [1, 2, 5, 17, 257]:
        raise ValueError("Gate2 separator depths")
    for row in rows:
        if row["future_cut_depth"] != row["agreed_regular_prefix_depth"] + 1:
            raise ValueError("Gate2 separator clock")
        if row["future_cut_two_dimensional_area"] != "0":
            raise ValueError("Gate2 separator area")
        if not row["intersects_every_candidate_fibre_u=constant"]:
            raise ValueError("Gate2 separator incidence")
        if row["cut_model_spanning_fibres"] is not False or row["good_model_spanning_fibres"] is not True:
            raise ValueError("Gate2 separator verdict")


def gate3_replay(data: dict[str, Any]) -> None:
    gate = data["result"]["gate3"]
    encoding = gate["pilot_semialgebraic_encoding"]
    if encoding["conservative_targets_per_step"] != 162 or encoding["source_chart_cells"] != 8:
        raise ValueError("Gate3 finite alphabet")
    expected_counts = {str(n): 8 * 162**n for n in range(1, 6)}
    if encoding["fixed_depth_branch_word_universe"] != expected_counts:
        raise ValueError("Gate3 word counts")
    if encoding["closure_tools"] != [
        "finite_boolean_operations",
        "Tarski_Seidenberg_projection",
        "finite_semialgebraic_connected_components",
        "Hardt_semialgebraic_triviality_over_parameter_strata",
    ]:
        raise ValueError("Gate3 semialgebraic closure chain")
    atlas = gate["fixed_depth_common_atlas"]
    if atlas != {
        "explicit_cell_enumeration_or_complexity_bound": "NOT_CERTIFIED",
        "finite_parameter_stratification": "CERTIFIED_QUALITATIVE_EXISTENCE",
        "fixed_slot_labels_with_empty_slots": "CERTIFIED_QUALITATIVE_EXISTENCE",
        "for_every_fixed_n": "CERTIFIED_QUALITATIVE_EXISTENCE",
        "regular_cells_real_analytic": True,
        "singular_and_grazing_cells_retained_as_cemetery": True,
    }:
        raise ValueError("Gate3 atlas typing")
    uniform = gate["uniform_component_theorem"]
    if uniform != {
        "artificial_homogeneity_cuts": (
            "allowed_only_as_one_fixed_finite_semialgebraic_family_absorbed_into_B"
        ),
        "conclusion": "there_exists_finite_N(n,B)_uniform_in_s_and_input_parameter",
        "gate4_J_cap_from_this_theorem_alone": "NOT_CERTIFIED",
        "input_scope": (
            "fixed_depth_n_and_compact_semialgebraic_regular_interval_"
            "family_of_uniform_format_degree_B"
        ),
        "properisation_Dbar_unbounded_gives_global_N_H": False,
        "terminal_predicates": "any_fixed_finite_family_including_two_C24_views",
        "unbounded_strip_indices": "NOT_COVERED",
    }:
        raise ValueError("Gate3 uniform-component theorem scope")
    lift = gate["weak_bulk_lift_assembly"]
    if lift["status"] != "CERTIFIED_FOR_EACH_FIXED_DEPTH_IN_WEAK_BOREL_TV_ONLY":
        raise ValueError("Gate3 weak map typing")
    if lift["R_s_l1_TV_norm"] != "1" or lift["Q_s_l1_TV_norm_upper"] != "1":
        raise ValueError("Gate3 weak map norms")
    source = (Q(1, 3), Q(-1, 6), Q(1, 2))
    source_tv = sum(abs(x) for x in source)
    target_tv = abs(source[0] + source[1]) + abs(source[2])
    if source_tv != 1 or target_tv != Q(2, 3):
        raise ValueError("Gate3 TV replay")
    if lift["sample_source_TV"] != "1" or lift["sample_assembled_TV"] != "2/3":
        raise ValueError("Gate3 TV manifest")
    if gate["fixed_free_graph_current_slots"] != 41508:
        raise ValueError("Gate3 slot count")
    if gate["complete_finite_s_future_side_owner_current_TV_upper"] != "518152320":
        raise ValueError("Gate3 current TV")
    for key in (
        "strong_physical_R_s_Q_s",
        "uniform_depth_boundary_Z_and_component_complexity",
        "directional_Piola_suffix_bound",
        "MT_DQ",
        "official_status",
    ):
        if gate[key] != "NOT_CERTIFIED":
            raise ValueError(f"Gate3 overpromotion: {key}")


def semantics(data: dict[str, Any]) -> None:
    if set(data) != {"artifact", "date", "dependencies", "result", "schema", "strict_verdict"}:
        raise ValueError("top-level shape")
    if data["artifact"] != "cm2-gate123-round57-projective-holonomy-semialgebraic-dq-frontier":
        raise ValueError("artifact")
    if data["date"] != "2026-07-20":
        raise ValueError("date")
    if data["schema"] != "cm2.gate123.round57.projective-holonomy-semialgebraic-dq-frontier.v1":
        raise ValueError("schema")
    if set(data["result"]) != {"gate1", "gate2", "gate3", "technology_recheck"}:
        raise ValueError("result shape")
    technology = data["result"]["technology_recheck"]
    if technology != {
        "latest_relevant_billiard_linear_response": "2604.19671v2",
        "latest_relevant_gate1": "2604.13401v1",
        "latest_relevant_gate2_gate3_review": "2606.10155v1",
        "new_direct_CM2_carrier_closure_found": False,
        "official_arxiv_api_checked_utc": "2026-07-20T08:17:40Z",
    }:
        raise ValueError("technology provenance")
    if data["strict_verdict"] != {
        "complete_composite_gates": "0/5",
        "gate1": "NOT_CERTIFIED",
        "gate2": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
        "overall": "NO-GO_FOR_CLAIM",
    }:
        raise ValueError("strict verdict")
    gate1_replay(data)
    gate2_replay(data)
    gate3_replay(data)


def validate(data: dict[str, Any], check_dependencies: bool = True) -> None:
    semantics(data)
    if check_dependencies:
        dependency_check(data)


def assign_path(data: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    target: Any = data
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def hostile_self_test() -> tuple[int, int]:
    original = load()
    mutations: list[tuple[tuple[Any, ...], Any]] = [
        (("schema",), "bad"),
        (("artifact",), "bad"),
        (("date",), "2026-07-19"),
        (("dependencies", 0, "sha256"), "0" * 64),
        (("dependencies", 0, "path"), "deliverables/missing"),
        (("strict_verdict", "gate1"), "CERTIFIED"),
        (("strict_verdict", "gate2"), "CERTIFIED"),
        (("strict_verdict", "gate3"), "CERTIFIED"),
        (("strict_verdict", "complete_composite_gates"), "1/5"),
        (("strict_verdict", "overall"), "GO"),
        (("result", "gate1", "physical_full_cross_common_vertex"), "NOT_CERTIFIED"),
        (("result", "gate1", "same_representative_class_H_plus_twisting"), "CERTIFIED"),
        (("result", "gate1", "weighted_projective_defect_compatibility_on_physical_combined_gauge"), "CERTIFIED"),
        (("result", "gate1", "general_exact_identity", "pair_12"), "dv"),
        (("result", "gate1", "general_exact_identity", "exact_rational_samples"), 2),
        (("result", "gate1", "gauge_chart_replays", "additive", "lower"), "du"),
        (("result", "gate1", "gauge_chart_replays", "U_v_L_u", "coupled"), "dv"),
        (("result", "gate1", "uniformly_invertible_additive_countermodel", "converges"), True),
        (("result", "gate1", "uniformly_invertible_additive_countermodel", "determinant_strict_lower"), "0"),
        (("result", "gate1", "uniformly_invertible_additive_countermodel", "normalized_lower_coordinate", 1), "1/10"),
        (("result", "gate2", "candidate_cone_product_layers"), "8/8"),
        (("result", "gate2", "official_immutable_fields"), "1/17"),
        (("result", "gate2", "physical_stable_saturated_base_projection_holonomy"), "CERTIFIED"),
        (("result", "gate2", "conditional_holonomy_product_theorem", "status"), "CERTIFIED_PHYSICAL"),
        (("result", "gate2", "conditional_holonomy_product_theorem", "exact_sample_full_log_bound"), "1"),
        (("result", "gate2", "conditional_holonomy_product_theorem", "exact_sample_tails", 7), "0"),
        (("result", "gate2", "finite_prefix_spanning_plaque_separator", "candidate_coordinate_tile_area"), "0"),
        (("result", "gate2", "finite_prefix_spanning_plaque_separator", "rows", 0, "future_cut_depth"), 1),
        (("result", "gate2", "finite_prefix_spanning_plaque_separator", "rows", 1, "future_cut_two_dimensional_area"), "1"),
        (("result", "gate2", "finite_prefix_spanning_plaque_separator", "rows", 2, "cut_model_spanning_fibres"), True),
        (("result", "gate3", "pilot_semialgebraic_encoding", "conservative_targets_per_step"), 161),
        (("result", "gate3", "pilot_semialgebraic_encoding", "source_chart_cells"), 7),
        (("result", "gate3", "pilot_semialgebraic_encoding", "fixed_depth_branch_word_universe", "3"), 1),
        (("result", "gate3", "pilot_semialgebraic_encoding", "closure_tools", 1), "projection"),
        (("result", "gate3", "fixed_depth_common_atlas", "for_every_fixed_n"), "NOT_CERTIFIED"),
        (("result", "gate3", "fixed_depth_common_atlas", "explicit_cell_enumeration_or_complexity_bound"), "CERTIFIED"),
        (("result", "gate3", "fixed_depth_common_atlas", "singular_and_grazing_cells_retained_as_cemetery"), False),
        (("result", "gate3", "uniform_component_theorem", "properisation_Dbar_unbounded_gives_global_N_H"), True),
        (("result", "gate3", "uniform_component_theorem", "gate4_J_cap_from_this_theorem_alone"), "CERTIFIED"),
        (("result", "gate3", "uniform_component_theorem", "unbounded_strip_indices"), "COVERED"),
        (("result", "gate3", "weak_bulk_lift_assembly", "R_s_l1_TV_norm"), "2"),
        (("result", "gate3", "weak_bulk_lift_assembly", "Q_s_l1_TV_norm_upper"), "2"),
        (("result", "gate3", "weak_bulk_lift_assembly", "status"), "CERTIFIED_STRONG"),
        (("result", "gate3", "weak_bulk_lift_assembly", "sample_assembled_TV"), "1"),
        (("result", "gate3", "fixed_free_graph_current_slots"), 41507),
        (("result", "gate3", "complete_finite_s_future_side_owner_current_TV_upper"), "0"),
        (("result", "gate3", "strong_physical_R_s_Q_s"), "CERTIFIED"),
        (("result", "gate3", "uniform_depth_boundary_Z_and_component_complexity"), "CERTIFIED"),
        (("result", "gate3", "directional_Piola_suffix_bound"), "CERTIFIED"),
        (("result", "gate3", "MT_DQ"), "CERTIFIED"),
        (("result", "technology_recheck", "new_direct_CM2_carrier_closure_found"), True),
        (("result", "technology_recheck", "latest_relevant_gate1"), "2607.99999v1"),
    ]
    rejected = 0
    accepted_paths: list[tuple[Any, ...]] = []
    for path, value in mutations:
        candidate = copy.deepcopy(original)
        assign_path(candidate, path, value)
        try:
            validate(candidate, check_dependencies=True)
        except (OSError, ValueError, KeyError, TypeError):
            rejected += 1
        else:
            accepted_paths.append(path)
    strict_cases = ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '[1,2,3]')
    for payload in strict_cases:
        try:
            parsed = strict_load_text(payload)
            if not isinstance(parsed, dict):
                raise ValueError("root")
        except ValueError:
            rejected += 1
    if accepted_paths:
        raise ValueError(f"hostile mutations accepted: {accepted_paths}")
    return rejected, len(mutations) + len(strict_cases)


def encoded(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        data = load()
        if args.self_test:
            rejected, total = hostile_self_test()
            if rejected != total:
                raise ValueError(f"hostile rejection shortfall {rejected}/{total}")
            print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
            return 0
        validate(data, check_dependencies=True)
        if args.reemit is not None:
            args.reemit.write_text(encoded(data), encoding="utf-8")
            print(f"REEMIT: {args.reemit}")
            return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ROUND57_GATE123_VERIFIER_FAILURE: {exc}", file=sys.stderr)
        return 1

    if args.integrity_only or args.replay:
        print("ROUND57_GATE123_INTEGRITY: PASS")
        print("PROJECTIVE_HOLONOMY_SEMIALGEBRAIC_REPLAY: PASS")
        print("NO_GATE_PROMOTION: PASS")
        return 0

    print("ROUND57_GATE123_FRONTIER: VALID_FAIL_CLOSED")
    print("GATE1_GATE2_GATE3: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
