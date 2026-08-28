#!/usr/bin/env python3
"""Round-40 correction and C24 standard-family Growth frontier.

Round 39 correctly showed that the existing projective stable-test norm does
not control a pointwise transverse trace.  It overtyped that fact as a
necessary obstruction to initializing a positive canonical standard family.
The local no-trace model instead applies to moving inverse-branch face
currents.  Positive stopped atoms already have a certified standard-family
representation and finite initial boundary Z.

The Gate-4 base obstruction is therefore hereditary Growth under repeated
C24 characteristic restrictions.  This certificate freezes the correction,
an exact inverse-length boundary-moment criterion, and the precise C24
version of the 2026 leaky-billiard Growth Lemma that remains to be proved.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round40-c24-standard-family-growth-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round40-c24-standard-family-growth-frontier-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-round39-transverse-trace-z-bridge-frontier-manifest-2026-07-19.json": (
        "fa1839bb755028e3de46669780f3abf679400f3ade5c742a7ba3ba0a5dfd7bd5"
    ),
    "cm2-gate34-round38-sampled-projective-strong-tail-manifest-2026-07-19.json": (
        "6aab6003fecfb705c924cced3ca5eb0d64012b1bf4db4816a2a9ac7012b2f6bf"
    ),
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json": (
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183"
    ),
    "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json": (
        "ee1ac2acb72af04ac254e2f0a33981df478b022cde0dc08f9988762ff1c8bcc9"
    ),
    "cm2-gate45-density-regular-mesh-recovery-bridge-manifest-2026-07-16.json": (
        "cb5adf88c8b650786d5237e7d5b78296835851692e1159637da7111c6131e142"
    ),
    "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json": (
        "6ee5be1c2b60438043284c26837eef7681c94f95290abee33e52b7cab893e1d3"
    ),
    "cm2-gate45-round37-delayed-characteristic-block-manifest-2026-07-19.json": (
        "4166a72c603666a5ff2b5422dd167b5dd4fa1e4ab25fdd99b77af2e543cc33a8"
    ),
}

SURVIVAL = Q(111718729, 111718750)
WEIGHTED_SURVIVAL = Q(223437479, 223437500)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


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


def validate_dependencies() -> None:
    round39 = load(
        "cm2-gate34-round39-transverse-trace-z-bridge-frontier-manifest-2026-07-19.json"
    )["result"]
    audit = round39["canonical_parent_W_trace_type_audit"]
    if audit["typed_interface_status"] != "MISSING_EXACTLY_LOCATED":
        raise RuntimeError("round39 trace status")
    if "transverse trace/disintegration" not in audit["required_operator"]:
        raise RuntimeError("round39 claim to supersede")
    if round39["strict_nonpromotion"]["canonical_standard_family_Z_tail"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("round39 Z scope")

    strong = load(
        "cm2-gate34-round38-sampled-projective-strong-tail-manifest-2026-07-19.json"
    )["result"]
    tail = strong["sampled_C24_killed_strong_tail"]
    if tail["explicit_mass_survival_factor_r"] != qstr(SURVIVAL):
        raise RuntimeError("round38 survival")
    if tail["weighted_factor_w_times_r"] != qstr(WEIGHTED_SURVIVAL):
        raise RuntimeError("round38 weighted survival")
    if strong["strict_nonpromotion"]["standard_family_Z_or_Growth_tail"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("round38 Growth scope")

    geometry = load(
        "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json"
    )["result"]
    interface = geometry["sparse_opening_theorem_interface"]
    stable = geometry["stable_curve_open_hole_geometry"]
    inventory = geometry["frozen_core_inventory"]
    if interface["O1"] != "CERTIFIED_WITH_P0=49":
        raise RuntimeError("C24 O1")
    if interface["O1_prime"] != "CERTIFIED_WITH_P0=49":
        raise RuntimeError("C24 O1 prime")
    if interface["O2"] != "CERTIFIED_WITH_Ct=1493":
        raise RuntimeError("C24 O2")
    if stable["boundary_edges_on_each_collision_component"] != 48:
        raise RuntimeError("C24 edge geometry")
    if inventory["boundary_edge_count_per_collision_component"] != 48:
        raise RuntimeError("C24 edge inventory")

    growth = load(
        "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json"
    )["replay_summary"]
    if growth["true_continuity_component_upper"] != 153:
        raise RuntimeError("growth complexity")
    if growth["crude_global_one_step_Xi_upper"] != "137751561/901685":
        raise RuntimeError("growth coefficient")
    if growth["numeric_global_Growth_contraction"] is not False:
        raise RuntimeError("growth scope")

    initial = load(
        "cm2-gate45-density-regular-mesh-recovery-bridge-manifest-2026-07-16.json"
    )["result"]
    standard = initial["oriented_standard_family_contract"]
    scope = initial["scope_limits"]
    if standard["single_depth_K_atom_initial_standard_family_boundary"] != (
        "Z_fw(K,j),Z_rev(K,j)<=C_mesh*2^K"
    ):
        raise RuntimeError("initial standard family Z")
    if standard["same_restricted_measure_and_same_K_j_record_in_both_views"] is not True:
        raise RuntimeError("initial same-ID measure")
    if scope["controlled_s0_stopped_parent_recovery"] is not True:
        raise RuntimeError("controlled recovery")
    if scope["hereditary_recovery_under_repeated_arbitrary_indicators"] is not False:
        raise RuntimeError("hereditary scope")

    tube = load(
        "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json"
    )["result"]["fair_dyadic_boundary_tube_theorem"]
    if tube["uniform_parameter_averaged_normalized_collision_SRB_bound"] != (
        "mu(U_d)<(50/39)h_d for every fair frontier with d>=24"
    ):
        raise RuntimeError("tube law")

    delayed = load(
        "cm2-gate45-round37-delayed-characteristic-block-manifest-2026-07-19.json"
    )["result"]
    if delayed["two_component_exact_threshold"][
        "least_closed_steps_for_inherited_Z_contraction"
    ] != 697:
        raise RuntimeError("delayed threshold")
    if delayed["strict_nonpromotion"]["hereditary_C24_open_Growth"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("delayed scope")


def round39_correction_matrix() -> dict[str, Any]:
    return {
        "superseded_statement": (
            "a bounded C0 transverse trace is necessary to initialize the positive canonical parent-W standard family"
        ),
        "correction": (
            "positive stopped atoms already admit a measure-theoretic same-restriction standard-family disintegration with finite initial Z"
        ),
        "round39_local_countermodel_still_proves": (
            "stable-test control alone does not bound a pointwise transverse trace"
        ),
        "countermodel_correct_scope": (
            "moving inverse-branch face currents and other C0 transverse source terms"
        ),
        "countermodel_does_not_prove": (
            "failure of positive-measure standard-family initialization or boundary Growth"
        ),
        "round39_nonpromotion_remains_valid": True,
        "round39_exact_rate_thresholds_remain_valid_for_hypothetical_norm_bridge": True,
        "Gate4_actual_base_gap": (
            "hereditary C24 open standard-family Growth under repeated characteristic restrictions"
        ),
        "correction_status": "CERTIFIED_SUPERSEDING_ONLY_THE_OVERTYPED_NECESSITY_CLAIM",
    }


def existing_initial_standard_family() -> dict[str, Any]:
    return {
        "scope": "controlled s=0 stopped atoms in both orientations",
        "same_restricted_measure_and_depth_record": True,
        "initial_boundary_Z": "Z_fw(K,j),Z_rev(K,j)<=C_mesh*2^K",
        "uniform_unstable_cone": "25/9<dphi/dr<4108425/145348",
        "uniform_carrier_C2_upper": "4949",
        "uniform_log_Holder_constant": "52 at exponent 1/3",
        "closed_map_parent_recovery": "CERTIFIED_PREVIOUSLY",
        "repeated_C24_characteristic_restrictions": "NOT_COVERED",
        "finite_parameter_window_hereditary_recovery": "NOT_COVERED",
        "conclusion": (
            "initial canonical Z is not the first missing interface; inherited open Growth is"
        ),
    }


def inverse_length_boundary_moment() -> dict[str, Any]:
    finite_examples = []
    for alpha in (Q(2), Q(3), Q(4)):
        multiplier = Q(2) / (1 - Q(2) ** (1 - alpha))
        finite_examples.append(
            {
                "alpha": qstr(alpha),
                "dyadic_inverse_length_multiplier": qstr(multiplier),
            }
        )
    counter_rows = []
    for prefix in (1, 2, 4, 8, 16):
        counter_rows.append(
            {
                "shell_prefix_count": prefix,
                "prefix_mass": qstr(1 - Q(1, 1 << prefix)),
                "prefix_inverse_length_moment": qstr(Q(prefix, 2)),
            }
        )
    return {
        "normalized_boundary_length": "eta=ell/delta in (0,1]",
        "boundary_measure": "nu with total mass M",
        "tail_hypothesis": "nu{eta<=t}<=C_boundary*M*t^alpha for 0<t<=1",
        "dyadic_shell_bound": (
            "integral eta^(-1) dnu <= 2*C_boundary*M/(1-2^(1-alpha))"
        ),
        "strict_sufficient_condition": "alpha>1",
        "unnormalized_boundary_Z_bound": (
            "Z_boundary<=delta^(-1)*2*C_boundary*M/(1-2^(1-alpha))"
        ),
        "exact_rational_examples": finite_examples,
        "critical_alpha_one_countermodel": {
            "atoms": "eta_k=2^(-k), mass_k=2^(-(k+1))*M, k>=0",
            "tail": "nu{eta<=2^(-n)}=M*2^(-n)",
            "each_shell_inverse_length_contribution": "M/2",
            "inverse_length_moment": "infinite",
            "finite_prefix_rows_at_M_1": counter_rows,
        },
        "round26_tube_exponent": "alpha=1 in parameter-averaged physical width",
        "round26_tube_is_same_canonical_boundary_cell_law": False,
        "round26_tube_alone_closes_boundary_Z": False,
        "criterion_status": "CERTIFIED_EXACT_DYADIC_SUFFICIENCY_AND_CRITICAL_COUNTERMODEL",
    }


def latest_technology_match() -> dict[str, Any]:
    return {
        "official_version_snapshot_checked_2026_07_19": {
            "arXiv:2104.06947": "v3 revised 2022-11-18",
            "arXiv:2604.19671": "v2 revised 2026-05-21",
            "arXiv:2606.10155": "v1 submitted 2026-06-08",
        },
        "matched_2026_mechanism": {
            "source": "Canestrari, arXiv:2604.19671v2",
            "Proposition_4_4": (
                "regular standard families persist under the paper's conditional leaky evolution"
            ),
            "Lemma_6_14": (
                "Z(hat_F_t^((p+1)n_*)G)<=gamma*Z(hat_F_t^(p n_*)G)+Z_0 with gamma<1"
            ),
            "proof_mechanism": (
                "unstable expansion beats fragmentation and short descendants are chopped into a controlled family"
            ),
        },
        "available_C24_precursors": {
            "O1_and_O1_prime": "P0=49",
            "O2": "Ct=1493",
            "physical_boundary_edges_total": 96,
            "uniform_parameter_window": "|s|<=1/400",
        },
        "geometry_mismatch": (
            "the paper treats its own small boundary-strip hole and conditional evolution; no theorem row directly identifies that hole with the 96-edge C24 phase hole"
        ),
        "direct_theorem_import_status": "NOT_ALLOWED_WITHOUT_C24_EXPANSION_FRAGMENTATION_MATCH",
        "web_search_api_note": (
            "search endpoint was quota-limited; official arXiv pages were checked directly"
        ),
    }


def c24_growth_target() -> dict[str, Any]:
    crude = Q(137751561, 901685)
    if not crude > 1:
        raise RuntimeError("crude Growth arithmetic")
    return {
        "native_same_ID_target": (
            "Z(hat_F_C24^((p+1)n_*)G)<=gamma_C24*Z(hat_F_C24^(p n_*)G)+Z0_C24*mass(G)"
        ),
        "required_strict_coefficient": "0<gamma_C24<1",
        "operator_type": (
            "fixed-s conditional survivor evolution on the same canonical parent-W standard-family registry"
        ),
        "current_global_continuity_component_upper": 153,
        "current_crude_one_step_Xi_upper": qstr(crude),
        "current_crude_one_step_is_contractive": False,
        "existing_delayed_scalar_fallbacks": [
            "if C_N=4000/1999 uniformly on full Q_N, N=697 suffices",
            "if C_N=580000/1999 uniformly on full Q_N, N=5694 suffices",
        ],
        "exact_missing_physical_payload": [
            "C24-specific expansion-versus-fragmentation sum on every surviving standard curve",
            "proper-family density and curvature invariance after every C24 cut",
            "conditional survival normalization or an equivalent unnormalized killed-family estimate",
            "a fixed-s same-ID block constant gamma_C24<1 and finite Z0_C24",
        ],
        "why_this_route_is_shorter": (
            "it controls canonical Z natively and bypasses both a pointwise C0 trace and a cellwise retained-depth product moment"
        ),
        "hereditary_C24_open_Growth": "NOT_CERTIFIED",
    }


def retained_rate_budget() -> dict[str, Any]:
    return {
        "projective_survival_rate": qstr(SURVIVAL),
        "weighted_projective_rate": qstr(WEIGHTED_SURVIVAL),
        "hypothetical_norm_to_Z_root_loss_unweighted_upper": qstr(1 / SURVIVAL),
        "hypothetical_norm_to_Z_root_loss_weighted_upper": qstr(
            1 / WEIGHTED_SURVIVAL
        ),
        "fixed_or_polynomial_initial_disintegration_loss_root": "1",
        "fixed_or_polynomial_loss_preserves_both_rate_margins": True,
        "native_Growth_route_needs_projective_to_Z_trace": False,
        "native_Growth_route_needs_its_own_gamma_C24_below_one": True,
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "claim_type": (
                "Round39 correction, exact boundary inverse-length criterion, and native C24 Growth frontier"
            ),
        },
        "round39_trace_claim_correction": round39_correction_matrix(),
        "previously_certified_initial_standard_family": existing_initial_standard_family(),
        "canonical_boundary_inverse_length_moment": inverse_length_boundary_moment(),
        "latest_technology_geometry_match": latest_technology_match(),
        "native_C24_standard_family_Growth_target": c24_growth_target(),
        "retained_projective_rate_budget": retained_rate_budget(),
        "strict_nonpromotion": {
            "round39_C0_trace_necessity_for_positive_Z_initialization": "SUPERSEDED",
            "round39_moving_face_current_no_trace_obstruction": "REMAINS_VALID",
            "controlled_s0_initial_standard_family_Z": "CERTIFIED_PREVIOUSLY",
            "canonical_boundary_inverse_length_alpha_gt_1_criterion": "CERTIFIED",
            "C24_O1_O1prime_O2_geometry": "CERTIFIED_PREVIOUSLY",
            "hereditary_C24_open_Growth": "NOT_CERTIFIED",
            "physical_aggregate_Z_uniform_or_weighted_bound": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "final_same_ID_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5_maturity": "7/18_UNCHANGED",
            "Gate5": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
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
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=(
            HERE / "cm2_gate34_round40_c24_standard_family_growth_frontier_verifier.py"
        ),
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    print(
        "ROUND39_TRACE_NECESSITY_CLAIM:",
        result["strict_nonpromotion"][
            "round39_C0_trace_necessity_for_positive_Z_initialization"
        ],
    )
    print("HEREDITARY_C24_OPEN_GROWTH: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
