#!/usr/bin/env python3
"""Independent verifier for the CM2 Round-58 Gate-1/2/3 frontier."""

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
    "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-"
    "manifest-2026-07-20.json"
)
Q = Fraction

EXPECTED_DEPENDENCIES = {
    "deliverables/cm2-gate123-round57-projective-holonomy-semialgebraic-dq-frontier-assault-2026-07-20.md":
        "7d012a962eb98f1b35fc988b9d011133148e874ff0dd0f6c3d8b5e8d64337207",
    "deliverables/cm2-gate123-round57-projective-holonomy-semialgebraic-dq-frontier-manifest-2026-07-20.json":
        "58bcb86cac43534a69604553cff6e46d92803af8d098a9b2e585333942b64d9f",
    "deliverables/cm2-gate1-numeric-holonomy-tail-twisting-frontier-assault-2026-07-16.md":
        "35f0632a29c93b639120cdffe5720b5d4ba282b02b3a247b476fcfb8f1ab4925",
    "deliverables/cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json":
        "4b9baaacaf7a315659448072d8d382bc90c4b41a9d98746b63c786f206ad449a",
    "deliverables/cm2-gate2-round25-product-base-assault-2026-07-18.md":
        "db75a6a8741d435182a1e0d0510e06d1b75b15eaba3d0c26e090e9c5990664e6",
    "deliverables/cm2-gate4-round57-unshifted-first-return-frontier-assault-2026-07-20.md":
        "a575bd78271a6581c232c3f37354dec75d3b3d73b9bf61474a2f6fbdae0d6fe3",
    "deliverables/cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-assault-2026-07-20.md":
        "b273290628c966465a3d0133661cfa511f7ec1ef18e98ee105b0f86bc7a2a0bc",
}


def fail(message: str) -> None:
    raise ValueError(message)


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate key: {key}")
        result[key] = value
    return result


def no_nonfinite(token: str) -> None:
    fail(f"non-finite token: {token}")


def strict_load_text(text: str) -> Any:
    return json.loads(text, object_pairs_hook=no_duplicates, parse_constant=no_nonfinite)


def load() -> dict[str, Any]:
    text = MANIFEST.read_text(encoding="utf-8")
    data = strict_load_text(text)
    if not isinstance(data, dict):
        fail("manifest root")
    if text != json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False) + "\n":
        fail("noncanonical manifest bytes")
    return data


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def dependency_check(data: dict[str, Any], check_files: bool) -> None:
    rows = data.get("dependencies")
    if not isinstance(rows, list) or len(rows) != len(EXPECTED_DEPENDENCIES):
        fail("dependency cardinality")
    observed: dict[str, str] = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "sha256"}:
            fail("dependency row shape")
        rel, digest = row["path"], row["sha256"]
        if not isinstance(rel, str) or rel in observed:
            fail("dependency path")
        if not isinstance(digest, str) or len(digest) != 64:
            fail("dependency digest")
        observed[rel] = digest
    if observed != EXPECTED_DEPENDENCIES:
        fail("dependency registry drift")
    if check_files:
        for rel, expected in EXPECTED_DEPENDENCIES.items():
            path = ROOT / rel
            if path.is_symlink() or not path.is_file() or sha256_path(path) != expected:
                fail(f"dependency integrity: {rel}")


def gate1_check(gate: dict[str, Any]) -> None:
    if set(gate) != {
        "official_status", "physical_weighted_projective_defect_convergence",
        "same_fibre_twisting_robustness", "same_representative_class_H_plus_twisting",
        "vanishing_increment_separator", "weighted_projective_critical_dini_theorem",
    }:
        fail("Gate1 shape")
    for key in (
        "official_status", "physical_weighted_projective_defect_convergence",
        "same_representative_class_H_plus_twisting",
    ):
        if gate[key] != "NOT_CERTIFIED":
            fail(f"Gate1 overpromotion: {key}")

    theorem = gate["weighted_projective_critical_dini_theorem"]
    critical = [Q(1) - Q(1, 2) ** n for n in range(10)]
    increments = [Q(1, 2) ** (n + 1) for n in range(9)]
    tails = [Q(1, 2) ** n for n in range(10)]
    if theorem != {
        "conclusion": (
            "both critical sequences converge uniformly with Holder tail "
            "d(x,y)^beta*sum_(k>=N)eta_k and limit modulus "
            "(H_0+sum eta_n)*d(x,y)^beta"
        ),
        "critical_sequences": [
            "C_n^+=(diagonal/projective weight)*(p_y,n-p_x,n)",
            "C_n^-=(diagonal/projective weight)*(q_y,n-q_x,n)",
        ],
        "exact_sample_C_n": [str(x) for x in critical],
        "exact_sample_increments": [str(x) for x in increments],
        "exact_sample_tails": [str(x) for x in tails],
        "hypothesis": (
            "abs(C_0^sigma)<=H_0*d(x,y)^beta and sup_plaque "
            "abs(C_(n+1)^sigma-C_n^sigma)"
            "<=eta_n*d(x,y)^beta for sigma in {+,-}, sum eta_n<infinity"
        ),
        "status": "CERTIFIED_CONDITIONAL_INTERFACE",
    }:
        fail("Gate1 Dini theorem")
    if any(critical[n + 1] - critical[n] != increments[n] for n in range(9)):
        fail("Gate1 Dini arithmetic")

    separator = gate["vanishing_increment_separator"]
    rows = separator["finite_replay_rows"]
    if [row["block"] for row in rows] != list(range(2, 8)):
        fail("Gate1 separator blocks")
    for row in rows:
        m = row["block"]
        if row != {
            "block": m, "high_value": "1", "step_absolute": str(Q(1, m)),
            "terminal_value": "0",
        }:
            fail("Gate1 separator row")
    if separator != {
        "conclusion": "vanishing_increment_without_Dini_summability_is_insufficient",
        "construction": (
            "block m rises 0->1 in m steps of 1/m and falls 1->0 "
            "in m steps of 1/m"
        ),
        "converges": False,
        "finite_replay_rows": rows,
        "increments_tend_to_zero": True,
    }:
        fail("Gate1 separator")

    robustness = gate["same_fibre_twisting_robustness"]
    margins = {
        "wedge_e1_psi_e1": str(Q(10) ** 77),
        "wedge_e1_psi_e2": str(Q(10) ** 47),
        "wedge_e2_psi_e1": "700",
        "wedge_e2_psi_e2": str(Q(1, 10**28)),
    }
    delta = Q(1, 10**29)
    if robustness != {
        "certified_delta": str(delta),
        "four_wedges_remain_nonzero": True,
        "physical_combined_gauge_loop_error_bound": "NOT_CERTIFIED",
        "required_comparison": (
            "same physical QNL fibre and same normalized eigenbasis; "
            "max-entry loop error <=delta"
        ),
        "strict_inward_wedge_margins": margins,
    }:
        fail("Gate1 robustness")
    if not all(Q(value) > delta for value in margins.values()):
        fail("Gate1 robustness arithmetic")


def gate2_check(gate: dict[str, Any]) -> None:
    if set(gate) != {
        "area_vs_shadow_separator", "gate2_to_gate4_landing_join",
        "official_immutable_fields", "official_status", "physical_projected_shadow_rows",
        "physical_stable_saturated_base_projection_holonomy",
        "projected_singularity_shadow_theorem",
    }:
        fail("Gate2 shape")
    if gate["official_immutable_fields"] != "0/17" or gate["physical_projected_shadow_rows"] != 0:
        fail("Gate2 field promotion")
    if gate["official_status"] != "NOT_CERTIFIED" or gate[
            "physical_stable_saturated_base_projection_holonomy"] != "NOT_CERTIFIED":
        fail("Gate2 physical promotion")

    theorem = gate["projected_singularity_shadow_theorem"]
    shadows = [Q(1, 2) ** (j + 2) for j in range(8)]
    if theorem != {
        "bad_shadow": (
            "B_j={u in I: W_u meets the depth-j singularity or "
            "the depth-j graph transform is undefined}"
        ),
        "candidate_fibres": "W_u over a reference base interval I",
        "conclusion": (
            "base measure of all-depth surviving plaques is at least "
            "|I|-sum_j b_j, and the graph-transform limit supplies stable plaques"
        ),
        "exact_sample_first_eight_b_j": [str(x) for x in shadows],
        "exact_sample_first_eight_sum": "255/512",
        "exact_sample_infinite_sum": "1/2",
        "exact_sample_survivor_lower": "1/2",
        "hypotheses": [
            "every bad shadow B_j is Borel",
            "Leb(B_j)<=b_j and sum_j b_j<|I|",
            "surviving finite graph transforms have a common cone/contraction/C1 compactness bound",
        ],
        "status": "CERTIFIED_CONDITIONAL_INTERFACE",
    }:
        fail("Gate2 shadow theorem")
    if sum(shadows, Q(0)) != Q(255, 512):
        fail("Gate2 shadow arithmetic")
    if gate["area_vs_shadow_separator"] != {
        "conclusion": "area_nullity_does_not_control_spanning_plaque_loss",
        "projected_bad_shadow": "the entire base I",
        "singular_set": "the line v=0 in the affine cone-product tile",
        "two_dimensional_area": "0",
    }:
        fail("Gate2 area-shadow separator")

    join = gate["gate2_to_gate4_landing_join"]
    c_p = Q(4 * 10**90 * 360493663, 358863)
    ell = Q(1) / (2 * c_p)
    interface = [
        "countable physical product-rectangle cover of the landing support",
        "immutable stable projection and two-sided Borel holonomy Jacobian bounds",
        "common landing restriction full-span or uniformly bounded fragmentation on physical unstable plaques",
        "same-measure Rokhlin unstable conditionals with density and log-distortion bounds",
        "average boundary charge sum p_W/|W| strictly below C_p",
        "Borel branch inverse retaining n/path/same-ID and half-open ownership",
        "strong restriction and assembly bounds for the resulting physical carrier",
    ]
    if join != {
        "actual_C_p": str(c_p),
        "isolated_physical_support_length": str(ell),
        "physical_same_support_Z_per_mass": str(2 * c_p),
        "projection_only_result": "proper_latent_graph_lift_with_endpoint_map",
        "reference_interval_Z_per_mass": "1",
        "same_point_positive_redisintegration_can_be_proper": False,
        "shortest_sufficient_physical_interface": interface,
        "stable_projection_preserves_physical_landing_point": False,
        "stable_projection_to_reference_can_be_proper": True,
        "status": "CONDITIONAL_JOIN_ONLY",
    }:
        fail("Gate2->4 join")
    if Q(join["physical_same_support_Z_per_mass"]) != 1 / ell:
        fail("Gate2->4 support arithmetic")


def cad_prefix(depth: int) -> dict[str, Any]:
    variables = 400 * depth + 20
    s_value, d_value = 2000 * depth + 100, 8
    rows = []
    product = 1
    for step in range(3):
        stack = 2 * s_value * d_value + 1
        product *= stack
        rows.append({
            "cell_product_prefix": str(product), "degree_majorant": str(d_value),
            "polynomial_count_majorant": str(s_value), "projection_step": step,
            "stack_factor": str(stack),
        })
        s_value = 2 * (s_value * d_value + 1) ** 2
        d_value = 2 * d_value**2
    return {
        "ambient_auxiliary_variables_k_n": variables,
        "depth": depth,
        "first_projection_rows": rows,
        "initial_degree_d": 8,
        "initial_polynomial_count_s_n": 2000 * depth + 100,
    }


def gate3_check(gate: dict[str, Any]) -> None:
    if set(gate) != {
        "directional_Piola_suffix_bound", "directional_piola_separator",
        "explicit_fixed_depth_cad_majorant", "MT_DQ", "official_status",
        "physical_formula_budget_instantiation", "strong_physical_R_s_Q_s",
        "unbounded_depth_moment_separator",
    }:
        fail("Gate3 shape")
    for key in ("directional_Piola_suffix_bound", "MT_DQ", "official_status",
                "physical_formula_budget_instantiation", "strong_physical_R_s_Q_s"):
        if gate[key] != "NOT_CERTIFIED":
            fail(f"Gate3 overpromotion: {key}")
    cad = gate["explicit_fixed_depth_cad_majorant"]
    words = {str(n): 8 * 162**n for n in range(1, 6)}
    if cad != {
        "budget_scope": (
            "conditional on an explicit branch formula fitting the declared "
            "k_n,s_n,degree envelope; physical formula enumeration is not claimed"
        ),
        "cad_recurrence": {
            "D_(r+1)": "2*D_r^2", "S_(r+1)": "2*(S_r*D_r+1)^2",
            "lift_stack_factor": "2*S_r*D_r+1", "projection_steps": "k_n",
            "total_component_majorant": (
                "8*162^n times product_(r=0)^(k_n-1)(2*S_r*D_r+1)"
            ),
        },
        "encoding_budget": {
            "auxiliary_variables_k_n": "400*n+20", "branch_words": "8*162^n",
            "degree": 8, "polynomial_count_s_n": "2000*n+100",
        },
        "exact_first_projection_replays": [cad_prefix(n) for n in (1, 2, 3)],
        "fixed_depth_branch_word_universe": words,
        "projection_component_rule": (
            "a continuous coordinate projection cannot split a connected component"
        ),
        "status": "CERTIFIED_FOR_DECLARED_ENCODING_BUDGET",
    }:
        fail("Gate3 CAD majorant")

    separator = gate["unbounded_depth_moment_separator"]
    values = [str(Q(d, 2) ** d) for d in range(1, 9)]
    if separator != {
        "exp_d_over_6_moment_upper_using_exp_1_over_6_lt_3_over_2": "3",
        "law": "p_d=2^-d for d>=1",
        "p_d_G_d_first_eight": values,
        "scope": (
            "the installed exponential Dbar moment alone cannot integrate "
            "the CAD majorant; no lower bound on actual component growth is claimed"
        ),
        "superexponential_integral_finite": False,
        "superexponential_test": "G(d)=d^d",
        "total_mass": "1",
    }:
        fail("Gate3 moment separator")
    if Q(values[-1]) != 65536:
        fail("Gate3 moment arithmetic")

    piola = gate["directional_piola_separator"]
    rows = [{
        "S_n": f"diag({2**n},1/{2**n})", "determinant": "1", "n": n,
        "norm_of_S_n_e1": str(2**n),
    } for n in range(1, 9)]
    if piola != {
        "conclusion": "determinant_one_does_not_bound_directional_current_amplification",
        "current_direction": "K=e1", "maps": "S_n=diag(2^n,2^-n)",
        "rows": rows,
    }:
        fail("Gate3 Piola separator")
    if any(Q(2**row["n"]) * Q(1, 2**row["n"]) != 1 for row in rows):
        fail("Gate3 Piola determinant")


def semantics(data: dict[str, Any], check_files: bool = True) -> None:
    if set(data) != {"artifact", "date", "dependencies", "result", "schema", "strict_verdict"}:
        fail("top-level shape")
    if data["artifact"] != "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier":
        fail("artifact")
    if data["date"] != "2026-07-20":
        fail("date")
    if data["schema"] != "cm2.gate123.round58.dini-shadow-cad-landing-join-frontier.v1":
        fail("schema")
    if data["strict_verdict"] != {
        "complete_composite_gates": "0/5", "gate1": "NOT_CERTIFIED",
        "gate2": "NOT_CERTIFIED", "gate3": "NOT_CERTIFIED",
        "overall": "NO-GO_FOR_CLAIM",
    }:
        fail("strict verdict")
    result = data["result"]
    if not isinstance(result, dict) or set(result) != {"gate1", "gate2", "gate3", "technology_recheck"}:
        fail("result shape")
    technology = result["technology_recheck"]
    if technology != {
        "checked_utc": "2026-07-20T11:45:20Z",
        "demers_liverani_2606_10155v1_pdf_sha256":
            "3330b5467c5c7107e58ba7966a0386f2ab51415990399b387ad2f7e571f61798",
        "new_direct_CM2_carrier_closure_found": False,
        "official_arxiv_api_queries": {
            "billiard_holonomy_young_tower": {
                "latest_relevant": "2509.07657v2",
                "response_sha256": "52a696a784ac85a2d61fb5b35b2300aa4658d2245460fa08c28fac6c79d84067",
            },
            "billiard_transfer_perturbation": {
                "latest_relevant": "2606.10155v1",
                "response_sha256": "e8c5429717c3522177ca15b601a2d66e0a91c64efd6092a41a4063ac4cc4d99f",
            },
            "cocycle_holonomy_twisting_cohomology": {
                "latest_relevant": "2604.13401v1",
                "response_sha256": "3349f389ad2b540e6a7edb309677334d81a90999d50cbf1b4b3ab160801e17a2",
            },
        },
    }:
        fail("technology provenance")
    dependency_check(data, check_files)
    gate1_check(result["gate1"])
    gate2_check(result["gate2"])
    gate3_check(result["gate3"])


def assign_path(data: Any, path: tuple[Any, ...], value: Any) -> None:
    target = data
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def hostile_self_test() -> tuple[int, int]:
    original = load()
    mutations: list[tuple[tuple[Any, ...], Any]] = [
        (("artifact",), "bad"), (("date",), "2026-07-19"), (("schema",), "bad"),
        (("dependencies", 0, "path"), "deliverables/missing"),
        (("dependencies", 0, "sha256"), "0" * 64),
        (("strict_verdict", "gate1"), "CERTIFIED"),
        (("strict_verdict", "gate2"), "CERTIFIED"),
        (("strict_verdict", "gate3"), "CERTIFIED"),
        (("strict_verdict", "complete_composite_gates"), "1/5"),
        (("strict_verdict", "overall"), "GO"),
        (("result", "gate1", "official_status"), "CERTIFIED"),
        (("result", "gate1", "physical_weighted_projective_defect_convergence"), "CERTIFIED"),
        (("result", "gate1", "same_representative_class_H_plus_twisting"), "CERTIFIED"),
        (("result", "gate1", "weighted_projective_critical_dini_theorem", "status"), "CERTIFIED_PHYSICAL"),
        (("result", "gate1", "weighted_projective_critical_dini_theorem", "exact_sample_C_n", 3), "0"),
        (("result", "gate1", "weighted_projective_critical_dini_theorem", "exact_sample_increments", 2), "0"),
        (("result", "gate1", "weighted_projective_critical_dini_theorem", "exact_sample_tails", 2), "0"),
        (("result", "gate1", "weighted_projective_critical_dini_theorem", "hypothesis"), "weaker"),
        (("result", "gate1", "vanishing_increment_separator", "increments_tend_to_zero"), False),
        (("result", "gate1", "vanishing_increment_separator", "converges"), True),
        (("result", "gate1", "vanishing_increment_separator", "finite_replay_rows", 0, "high_value"), "0"),
        (("result", "gate1", "vanishing_increment_separator", "finite_replay_rows", 1, "step_absolute"), "1"),
        (("result", "gate1", "same_fibre_twisting_robustness", "certified_delta"), "1"),
        (("result", "gate1", "same_fibre_twisting_robustness", "four_wedges_remain_nonzero"), False),
        (("result", "gate1", "same_fibre_twisting_robustness", "physical_combined_gauge_loop_error_bound"), "CERTIFIED"),
        (("result", "gate1", "same_fibre_twisting_robustness", "strict_inward_wedge_margins", "wedge_e2_psi_e2"), "0"),
        (("result", "gate2", "official_status"), "CERTIFIED"),
        (("result", "gate2", "official_immutable_fields"), "1/17"),
        (("result", "gate2", "physical_projected_shadow_rows"), 1),
        (("result", "gate2", "physical_stable_saturated_base_projection_holonomy"), "CERTIFIED"),
        (("result", "gate2", "projected_singularity_shadow_theorem", "status"), "CERTIFIED_PHYSICAL"),
        (("result", "gate2", "projected_singularity_shadow_theorem", "exact_sample_first_eight_b_j", 0), "0"),
        (("result", "gate2", "projected_singularity_shadow_theorem", "exact_sample_first_eight_sum"), "1/2"),
        (("result", "gate2", "projected_singularity_shadow_theorem", "exact_sample_survivor_lower"), "0"),
        (("result", "gate2", "area_vs_shadow_separator", "two_dimensional_area"), "1"),
        (("result", "gate2", "area_vs_shadow_separator", "projected_bad_shadow"), "empty"),
        (("result", "gate2", "gate2_to_gate4_landing_join", "same_point_positive_redisintegration_can_be_proper"), True),
        (("result", "gate2", "gate2_to_gate4_landing_join", "stable_projection_preserves_physical_landing_point"), True),
        (("result", "gate2", "gate2_to_gate4_landing_join", "physical_same_support_Z_per_mass"), "1"),
        (("result", "gate2", "gate2_to_gate4_landing_join", "reference_interval_Z_per_mass"), "2"),
        (("result", "gate2", "gate2_to_gate4_landing_join", "shortest_sufficient_physical_interface", 0), "missing"),
        (("result", "gate2", "gate2_to_gate4_landing_join", "status"), "CERTIFIED"),
        (("result", "gate3", "official_status"), "CERTIFIED"),
        (("result", "gate3", "strong_physical_R_s_Q_s"), "CERTIFIED"),
        (("result", "gate3", "physical_formula_budget_instantiation"), "CERTIFIED"),
        (("result", "gate3", "directional_Piola_suffix_bound"), "CERTIFIED"),
        (("result", "gate3", "MT_DQ"), "CERTIFIED"),
        (("result", "gate3", "explicit_fixed_depth_cad_majorant", "status"), "NOT_CERTIFIED"),
        (("result", "gate3", "explicit_fixed_depth_cad_majorant", "encoding_budget", "degree"), 7),
        (("result", "gate3", "explicit_fixed_depth_cad_majorant", "fixed_depth_branch_word_universe", "2"), 1),
        (("result", "gate3", "explicit_fixed_depth_cad_majorant", "cad_recurrence", "D_(r+1)"), "D_r"),
        (("result", "gate3", "explicit_fixed_depth_cad_majorant", "exact_first_projection_replays", 0, "ambient_auxiliary_variables_k_n"), 1),
        (("result", "gate3", "explicit_fixed_depth_cad_majorant", "exact_first_projection_replays", 0, "first_projection_rows", 0, "stack_factor"), "1"),
        (("result", "gate3", "unbounded_depth_moment_separator", "superexponential_integral_finite"), True),
        (("result", "gate3", "unbounded_depth_moment_separator", "p_d_G_d_first_eight", 7), "0"),
        (("result", "gate3", "unbounded_depth_moment_separator", "scope"), "actual lower bound"),
        (("result", "gate3", "directional_piola_separator", "rows", 0, "determinant"), "2"),
        (("result", "gate3", "directional_piola_separator", "rows", 7, "norm_of_S_n_e1"), "1"),
        (("result", "technology_recheck", "checked_utc"), "bad"),
        (("result", "technology_recheck", "new_direct_CM2_carrier_closure_found"), True),
        (("result", "technology_recheck", "demers_liverani_2606_10155v1_pdf_sha256"), "0" * 64),
        (("result", "technology_recheck", "official_arxiv_api_queries", "billiard_holonomy_young_tower", "response_sha256"), "0" * 64),
        (("result", "technology_recheck", "official_arxiv_api_queries", "cocycle_holonomy_twisting_cohomology", "latest_relevant"), "bad"),
        (("result", "technology_recheck", "official_arxiv_api_queries", "billiard_transfer_perturbation", "latest_relevant"), "bad"),
    ]
    rejected = 0
    for path, replacement in mutations:
        mutant = copy.deepcopy(original)
        assign_path(mutant, path, replacement)
        try:
            semantics(mutant, check_files=False)
        except (ValueError, KeyError, TypeError, IndexError):
            rejected += 1
    text = MANIFEST.read_text(encoding="utf-8")
    hostile_texts = [
        text.replace('"artifact":', '"artifact":"duplicate","artifact":', 1),
        text.replace('"date": "2026-07-20"', '"date": NaN', 1),
        text + " {}",
    ]
    for hostile in hostile_texts:
        try:
            strict_load_text(hostile)
        except (ValueError, json.JSONDecodeError):
            rejected += 1
    total = len(mutations) + len(hostile_texts)
    if rejected != total:
        fail(f"hostile suite accepted {total - rejected}/{total}")
    return rejected, total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = load()
        semantics(data, check_files=True)
        if args.self_test:
            rejected, total = hostile_self_test()
            print(f"ROUND58_GATE123_HOSTILE_MUTATIONS: {rejected}/{total} REJECTED")
        if args.integrity_only:
            print(f"ROUND58_GATE123_DEPENDENCIES: {len(EXPECTED_DEPENDENCIES)}/{len(EXPECTED_DEPENDENCIES)} PASS")
        if args.replay or args.integrity_only or args.self_test:
            print("ROUND58_GATE123_INDEPENDENT_REPLAY: PASS")
            return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, json.JSONDecodeError) as exc:
        print(f"ROUND58_GATE123_VERIFIER_FAILURE: {exc}", file=sys.stderr)
        return 1

    print("GATE1_GATE2_GATE3: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
