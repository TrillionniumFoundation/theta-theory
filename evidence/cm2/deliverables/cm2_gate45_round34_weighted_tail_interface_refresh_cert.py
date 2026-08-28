#!/usr/bin/env python3
"""Corrected strong-q tail interface ledger after rounds 31--34."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate45.round34-weighted-tail-interface-refresh.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate45-round34-weighted-tail-interface-refresh-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json": (
        "02277a2c10ea905fd8a4cf9998ae364a4b024087624fd3bea0a8a4175405727d"
    ),
    "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json": (
        "eef1071c1f4973892bf5e450421f3b91de7a2b426165e6a8c6f8bb4404eeac57"
    ),
    "cm2-gate45-round29-same-id-weighted-induced-frontier-manifest-2026-07-18.json": (
        "f2725815d6f995b8d6055255bd50ba60619f06a7904409177a227ff247a2f659"
    ),
    "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json": (
        "fa654b2c852f2b89e6e85a457f7ec7689dc56b7ccc9582d994db6b2e269bfb74"
    ),
    "cm2-gate45-round32-actual-instance-f7-join-manifest-2026-07-19.json": (
        "81e59b1ca2ff8b2aeac1c2eba36592e0e788618a33ef97c7a7d65faa94c2c310"
    ),
    "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json": (
        "f9c4eca78065001e65381880deef8681b3a626c2bd419e4ecfe3b02f37a7b53e"
    ),
    "cm2-gate5-round33-safe-f9-f10-subatlas-manifest-2026-07-19.json": (
        "75871f5e0bad0d504ecfe3a796bff05318f56f7044041c35b25918701adc6afc"
    ),
    "cm2-gate5-round34-rank-path-core-preimage-f9-manifest-2026-07-19.json": (
        "323cdeb40a78d29e0e767b438ef1e6fe0c28d8da80a10e0b4f4d717d4f308515"
    ),
    "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json": (
        "7594afb9fc37660e8ce7c47d57bfd385dde65bcedfbdab5872f52699f5a4e72d"
    ),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def endpoint_lthreehalves_seed() -> dict[str, Any]:
    mass_upper = Q(8064, 5)
    tail_constant = Q(9158592, 6875)
    rank_moment_upper = (1 << 21) * mass_upper + Q(7, 128) * tail_constant
    cost_power_upper = 1963 * rank_moment_upper
    return {
        "endpoint_coarea_measure_symbol": "dm_e",
        "minimum_rank": 14,
        "tail_input": "m_e{B>b}<=(9158592/6875)*4^-b for b>=14",
        "positive_mass_upper": str(mass_upper),
        "one_collision_density_symbol": "c_e^(1)=151*2^B",
        "chosen_exponent": "p=3/2",
        "rank_moment_identity_start": (
            "integral a^B dm <= a^14*m(total)+sum_{b>=14}(a^(b+1)-a^b)m{B>b}"
        ),
        "a": "2^(3/2)=2*sqrt(2)",
        "exact_a_power_at_base_rank": "a^14=2^21",
        "rational_tail_majorants": [
            "a-1<2",
            "a/4=1/sqrt(2)<5/7",
            "(a/4)^14=1/128",
            "sum_{b>=14}(a/4)^b<7/256",
        ],
        "integral_2^(3B/2)_dm_strict_upper": str(rank_moment_upper),
        "151^(3/2)_strict_upper": "1963",
        "integral_(151*2^B)^(3/2)_dm_strict_upper": str(cost_power_upper),
        "one_collision_endpoint_coarea_L3over2_seed": "CERTIFIED",
        "same_measure_as_fixed_s_first_return_component_mass": False,
        "physical_first_return_Lp_transfer_hypothesis_filled": False,
    }


def build_result() -> dict[str, Any]:
    sparse = load(
        "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json"
    )
    transfer = load(
        "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json"
    )["result"]
    old_interface = load(
        "cm2-gate45-round29-same-id-weighted-induced-frontier-manifest-2026-07-18.json"
    )["result"]
    parent = load(
        "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json"
    )["result"]
    f7 = load(
        "cm2-gate45-round32-actual-instance-f7-join-manifest-2026-07-19.json"
    )["result"]
    f8 = load(
        "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json"
    )["result"]
    f10 = load(
        "cm2-gate5-round33-safe-f9-f10-subatlas-manifest-2026-07-19.json"
    )["result"]
    f9 = load(
        "cm2-gate5-round34-rank-path-core-preimage-f9-manifest-2026-07-19.json"
    )["result"]
    endpoint = load(
        "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
    )["result"]["endpoint_rank_tail_and_first_order_cost"]

    sparse_verdict = sparse["verdict"]
    sparse_result = sparse["result"]
    if sparse_verdict["C24_recovered_cone_hit_gap_21_over_111718750"] != "CERTIFIED":
        raise RuntimeError("hit gap")
    if sparse_verdict["C24_uniform_unweighted_exponential_return_tail"] != "CERTIFIED":
        raise RuntimeError("unweighted tail")
    if sparse_result["uniform_recovered_cone_hit_gap"][
        "explicit_per_block_survival_factor"
    ] != "111718729/111718750":
        raise RuntimeError("survival factor")
    if transfer["weighted_tail_transfer_theorem"]["survivor_conditioned_Lp_transfer"][
        "status"
    ] != "CERTIFIED_CONDITIONAL_TRANSFER_THEOREM":
        raise RuntimeError("conditional transfer")
    old_rows = old_interface["weighted_tail_connectability"]["required_interfaces"]
    if len(old_rows) != 6:
        raise RuntimeError("old six-interface ledger")
    if parent["Q2_parent_W_Borel_registry"]["actual_parent_W_registry"] != (
        "CERTIFIED_PARAMETERIZED"
    ):
        raise RuntimeError("actual parent W")
    if parent["Q2_actual_recut_instance_schema"]["actual_recut_instance_registry"] != (
        "CERTIFIED_PARAMETERIZED_SCHEMA"
    ):
        raise RuntimeError("actual recuts")
    if f7["same_ID_actual_instance_F7_join"]["numeric_F7_actual_instance_slots"] != (
        "CERTIFIED_PARAMETERIZED_228012_BASE_RULES"
    ):
        raise RuntimeError("F7")
    if f7["same_ID_actual_instance_F7_join"][
        "one_step_numeric_F7_strict_upper"
    ] != "360134800/360493663":
        raise RuntimeError("F7 coefficient")
    if f8["same_ID_numeric_F8"]["numeric_F8_actual_face_slots"] != (
        "CERTIFIED_PARAMETERIZED"
    ):
        raise RuntimeError("F8")
    if f10["moving_occurrence_F10_subatlas"]["F10_slots"] != (
        "CERTIFIED_PARAMETERIZED_64_OCCURRENCE_SEEDS"
    ):
        raise RuntimeError("F10 seed")
    if f9["five_face_kind_matrix"]["terminal_core_preimage_face"]["F9"] != (
        "CERTIFIED_RANK_PATH_TEMPLATE_ON_EACH_REGULAR_COMPONENT"
    ):
        raise RuntimeError("F9 rank path")
    rank = endpoint["endpoint_tail"]
    if rank["global_tail_constant"] != "9158592/6875":
        raise RuntimeError("rank tail")
    if endpoint["raw_rank_moment"][
        "positive_coarea_mass_upper_before_Z_N_inverse"
    ] != "8064/5":
        raise RuntimeError("rank mass")

    interfaces = [
        {
            "index": 1,
            "record": "positive_mass_fixed_s_Rn_component_rows",
            "round29_state": "4216_FINITE_R1_ANCHORS_ONLY",
            "round34_state": "UNCHANGED_PARTIAL",
            "remaining": (
                "complete arbitrary-depth nonempty fixed-s first-return component "
                "registry with physical masses"
            ),
        },
        {
            "index": 2,
            "record": "actual_parent_recuts_and_common_fw_rev_recovery_carrier",
            "round29_state": "ACTUAL_RECUTS_0_COMMON_CARRIER_0",
            "round34_state": "ACTUAL_RECUTS_CERTIFIED_PARAMETERIZED_COMMON_CARRIER_ABSENT",
            "remaining": "one same-ID standard-family recovery carrier shared by fw and rev",
        },
        {
            "index": 3,
            "record": "numeric_once_charged_C_fw_C_rev_c_equals_q_over_m",
            "round29_state": "COUNT_0",
            "round34_state": "COUNT_0",
            "remaining": "numeric fixed-s rows on physical Rn component masses",
        },
        {
            "index": 4,
            "record": "physical_first_return_tail_transfer_envelope",
            "round29_state": "COUNT_0",
            "round34_state": "COUNT_0_ONE_COLLISION_COAREA_L3OVER2_SEED_ONLY",
            "remaining": "survivor-conditioned or global fixed-s physical Rn Lp envelope",
        },
        {
            "index": 5,
            "record": "strong_singular_cemetery_charge",
            "round29_state": "COUNT_0",
            "round34_state": "COUNT_0",
            "remaining": "summable strong Z/trace/current estimate on the same carrier",
        },
        {
            "index": 6,
            "record": "induced_common_space_F14_through_F18_assembly",
            "round29_state": "NOT_CERTIFIED",
            "round34_state": "NOT_CERTIFIED",
            "remaining": "complete F14-F18 and a common induced contraction coefficient",
        },
    ]
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "old_artifacts_modified": False,
            "audit_date": "2026-07-19",
            "parameter_quantifier": "uniformly for every fixed |s|<=1/400 where stated",
        },
        "corrected_C24_tail_baseline": {
            "round33_missing_hit_lower_label_was_stale": True,
            "recovered_cone_explicit_per_block_hit_gap": "21/111718750",
            "per_block_survival_factor": "111718729/111718750",
            "uniform_theorem_supplied_block_length": "N_open>=1_non_numeric",
            "normalized_unweighted_return_tail": (
                "P(tau_C24_plus>n)<(550000/147)*"
                "(111718729/111718750)^floor(n/N_open)"
            ),
            "uniform_unweighted_exponential_return_tail": "CERTIFIED",
            "q_weighted_exponential_return_cemetery_tail": "NOT_CERTIFIED",
            "correction_is_append_only_prior_reports_unchanged": True,
        },
        "post_round31_to_round34_interface_refresh": {
            "required_interface_count": 6,
            "fully_completed_interface_count": 0,
            "partially_advanced_interface_indices": [2, 4],
            "rows": interfaces,
            "rows_sha256": digest(interfaces),
            "first_true_missing_strong_tail_interface": (
                "same-ID common fw/rev standard-family recovery carrier and numeric c=q/m rows"
            ),
            "recovered_cone_hit_lower_is_first_missing_interface": False,
        },
        "current_F7_to_F10_payload": {
            "F7_actual_parameterized_recut_instance_schema": "CERTIFIED",
            "F7_Q2_actual_parameterized_instance_slots": (
                "CERTIFIED_PARAMETERIZED_228012_BASE_RULES"
            ),
            "F7_Q2_one_step_numeric_strict_upper": "360134800/360493663",
            "F7_arbitrary_depth_Rn_same_ID_numeric_charge": "NOT_CERTIFIED",
            "F8_all_five_face_grammars_common_transversality_lower": "CERTIFIED_1/5",
            "F9_source_core_faces": "CERTIFIED_96_LEVEL_ZERO",
            "F9_intermediate_and_terminal_core_preimages": (
                "CERTIFIED_RANK_PATH_TEMPLATE_ON_REGULAR_COMPONENTS"
            ),
            "F9_owner_change_singularity_and_moving_occurrence": "NOT_CERTIFIED",
            "F10_stationary_source_core": "CERTIFIED_ZERO_PARAMETER_CURRENT",
            "F10_moving_occurrence": "CERTIFIED_64_SEED_LEVEL_PARAMETERIZED",
            "F10_other_face_kinds": "NOT_CERTIFIED",
            "global_Gate5_maturity": "6/18_UNCHANGED",
        },
        "one_collision_endpoint_coarea_L3over2_seed": endpoint_lthreehalves_seed(),
        "latest_technology_audit": {
            "official_pages_checked_on": "2026-07-19",
            "sources": [
                {
                    "id": "arXiv:2604.19671v2",
                    "title": "Linear response for Sinai billiards with small holes",
                    "scope_match": (
                        "special boundary-position holes whose images admit long-standard-pair foliations"
                    ),
                    "closes_C24_phase_rectangle_strong_q_interface": False,
                },
                {
                    "id": "arXiv:2606.10155v1",
                    "title": "Recent Progress in the Application of Transfer Operators to Dispersing Billiards",
                    "scope_match": "review and cone/Banach-space blueprint",
                    "closes_C24_branchwise_numeric_q_cemetery_F14_F18": False,
                },
                {
                    "id": "arXiv:2104.06947v3",
                    "title": "Projective Cones for Sequential Dispersing Billiards",
                    "scope_match": "already instantiated recovered-cone sparse-hit theorem source",
                    "closes_weighted_induced_strong_tail": False,
                },
            ],
            "new_external_theorem_promoted": False,
        },
        "shortest_remaining_route": [
            "bind one common fw/rev standard-family recovery carrier to actual parent-W and physical Rn IDs",
            "materialize numeric fixed-s C_fw,C_rev,c=q/m rows including F7,F9,F10 charges",
            "upgrade the one-collision coarea moment to a survivor-conditioned physical Rn Lp envelope",
            "charge the strong singular/corner cemetery on the same carrier",
            "assemble F14-F18 and prove the induced common-space contraction",
        ],
        "strict_nonpromotion": {
            "unweighted_tail_reproved_as_new_round34_result": False,
            "one_collision_coarea_L3over2_seed_is_physical_Rn_Lp_envelope": False,
            "rank_path_F9_template_is_complete_F9_atlas": False,
            "q_weighted_exponential_excursion_cemetery_tail": "NOT_CERTIFIED",
            "induced_common_strong_Lasota_Yorke": "NOT_CERTIFIED",
            "complete_18_field_operator_block_count": 0,
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def write_manifest(path: Path, verifier: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate45_round34_weighted_tail_interface_refresh_verifier.py",
    )
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        return 0
    result = build_result()
    print(result["corrected_C24_tail_baseline"]["uniform_unweighted_exponential_return_tail"])
    print(result["strict_nonpromotion"]["q_weighted_exponential_excursion_cemetery_tail"])
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
