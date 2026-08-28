#!/usr/bin/env python3
"""Round-47 refined C24 crossing and post-cut recovery certificate.

This certificate makes two independent advances without assuming a numerical
covering time.  First, a transverse extended parent on a white-obstacle
diagonal C24 core has a much sharper geometrical hit fraction.  Second, the
one-step killed Growth bound, rather than the 9,148-step tiny-scale block,
gives a moderate dyadic post-cut recovery clock for each orientation
separately.

The forward and reverse killed survivors are not asserted to be the same
physical subset.  Consequently the certificate does not claim a joint
same-ID clock, a numerical H_cover/beta, a final q, or a strong cemetery
estimate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert as closed_growth


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round47-refined-crossing-postcut-recovery.v2"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round47-postcut-dyadic-recovery-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-round45-parent-bundle-cross-cell-frontier-manifest-2026-07-19.json": (
        "a616f9e2bd1ce44cb6c7aada76df8b25d55083899dc92ac42161f5f38a039bdf"
    ),
    "cm2-gate34-round46-extended-parent-density-frontier-manifest-2026-07-19.json": (
        "5144220fb226d0b00265d16e40cadde91ae2f4d2346f73ce31274b2b10b4c501"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json": (
        "9fe09f46e2201a54e000ea67ac09521ce73e1fe012b5205e12541805787683b3"
    ),
    "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json": (
        "fa654b2c852f2b89e6e85a457f7ec7689dc56b7ccc9582d994db6b2e269bfb74"
    ),
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json": (
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2_gate3_candidate_first_hit_cert.py": (
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py": (
        "01e32ca209818f4077443a7692622c4202ab7f1066e2f95802185e2be7a2cc9a"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
}

DENSITY_RATIO = Q(2000, 1999)
B0 = 49
THETA = Q(900337, 901685)
Z1 = Q(18367592526, 360493663)
R_EXT = Q(400000000, 399794003)
HIT_GAP = Q(21, 111718750)
CLOSED_CONTRACTION = Q(360134800, 360493663)
CLOSED_MARGIN = Q(358863, 360493663)
CLOSED_ADDITIVE = Q(2 * 10**90)
C_P = Q(4 * 10**90 * 360493663, 358863)
RECOVERY_HALF_BLOCK = 1005
POSTCUT_BASE = 318
NATIVE_ETA_ONE_ORIENTATION = Q(1, 6030)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


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
    old_geometry = load(
        "cm2-gate34-round45-parent-bundle-cross-cell-frontier-manifest-2026-07-19.json"
    )["result"]
    pair = old_geometry["extended_parent_bundle_minorization_interface"]
    old_length = pair["extended_pre_recut_pair_length_bound"]
    if old_length["monotone_unstable_graph"] is not True:
        raise RuntimeError("monotone extended parent")
    if old_length["phi_variation_strict_upper"] != "22/7":
        raise RuntimeError("phi variation")

    prior = load(
        "cm2-gate34-round46-extended-parent-density-frontier-manifest-2026-07-19.json"
    )["result"]
    density = prior["numeric_cross_cell_density_continuation"]
    registry = prior["extended_pre_recut_parent_bundle_registry"]
    frontier = prior["C24_covering_frontier_after_R_ext"]
    if density["extended_parent_density_ratio_strict_upper_R_ext"] != qstr(R_EXT):
        raise RuntimeError("R_ext")
    if registry["child_union"].startswith("the ordered half-open") is not True:
        raise RuntimeError("extended child union")
    if density["independent_child_weight_model_excluded"] is not True:
        raise RuntimeError("extended weights")
    if frontier["numeric_H_cover"] is not None or frontier["numeric_beta"] is not None:
        raise RuntimeError("covering overclaim")

    killed_manifest = load(
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    )["result"]
    killed = killed_manifest["numerical_C24_killed_Growth"]
    if killed["one_step_Z_multiplier_Z1"] != qstr(Z1):
        raise RuntimeError("one-step Z1")
    if killed["one_step_bound"] != "Z(O_s G)<=Z1*Z(G)":
        raise RuntimeError("one-step bound")
    if killed["uniform_parameter_scope"] != "every fixed |s|<=1/400":
        raise RuntimeError("parameter scope")

    q2 = load(
        "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json"
    )["result"]
    if q2["provenance"]["canonical_recut_policy"] != (
        "deterministic adapted-arclength branch rules producing cells of length at most 1e-90"
    ):
        raise RuntimeError("adapted recut policy")
    if q2["Q2_numeric_F5_F6_slot_registry"][
        "one_step_canonical_recut_log_variation_strict_upper"
    ] != "3/200000":
        raise RuntimeError("adapted recut F6")
    round31 = load(
        "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json"
    )["result"]
    parent31 = round31["Q2_parent_W_Borel_registry"]
    if not parent31["natural_short_cell_rule"].startswith(
        "oriented Euclidean arclength intervals"
    ):
        raise RuntimeError("Round31 metric audit")
    if round31["Q2_actual_recut_instance_schema"][
        "per_image_parent_natural_cell_count_formula"
    ] != "ceil(adapted_length(image-parent-W)/1e-90)":
        raise RuntimeError("Round31 image recut")

    hole = load(
        "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json"
    )["result"]["frozen_core_inventory"]
    if hole["core_count"] != 24 or hole["core_rows_sha256"] != (
        "c3042515b4a244b064f1aaef97ee236c5d3f6078a53fe3fb9e865a1976853b2f"
    ):
        raise RuntimeError("C24 core inventory")
    source = HERE / "cm2_gate25_physical_return_core_registry_cert.py"
    if sha(source) != DEPENDENCIES[source.name]:
        raise RuntimeError("core registry source")
    # The source cannot be imported in the minimal verifier environment
    # because its interval-arithmetic dependency is optional.  Its pinned
    # digest plus these exact registry tokens freeze the same rows without
    # executing that dependency.
    registry_source = source.read_text(encoding="utf-8")
    for token in (
        "DIAGONAL_P_HALF_WIDTH = Q(1, 50)",
        'for source in ("G", "W"):',
        'for direction in ("NE", "NW", "SE", "SW"):',
        'f"{source}:{cell}"',
    ):
        if token not in registry_source:
            raise RuntimeError(f"white diagonal registry token: {token}")
    first_hit_source = HERE / "cm2_gate3_candidate_first_hit_cert.py"
    if sha(first_hit_source) != DEPENDENCIES[first_hit_source.name]:
        raise RuntimeError("first-hit source hash")
    if 'RADIUS = {"G": Q(9, 25), "W": Q(4, 25)}' not in (
        first_hit_source.read_text(encoding="utf-8")
    ):
        raise RuntimeError("white radius")

    numeric = load(
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    )
    replay = numeric["replay_summary"]
    if replay["vartheta_p"] != qstr(CLOSED_CONTRACTION):
        raise RuntimeError("closed contraction")
    if replay["A1"] != RECOVERY_HALF_BLOCK:
        raise RuntimeError("closed recovery clock")
    closed_source = (
        HERE / "cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py"
    )
    if sha(closed_source) != DEPENDENCIES[closed_source.name]:
        raise RuntimeError("closed source hash")
    if "25/9<V=dphi/dr<4108425/145348<29" not in (
        closed_source.read_text(encoding="utf-8")
    ):
        raise RuntimeError("positive unstable slope")
    closed = closed_growth.certify()["numeric_growth_and_recovery"]
    recurrence = closed["adapted_boundary_Growth_recurrence"]
    constants = closed["numeric_Growth_Lemma_constants"]
    if recurrence["additive_mass_coefficient"] != qstr(CLOSED_ADDITIVE):
        raise RuntimeError("closed additive")
    if constants["adapted_C_p"] != qstr(C_P):
        raise RuntimeError("proper constant")

    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]["common_forward_reverse_carrier_pair"]
    if carrier["actual_parameterized_common_fw_rev_carrier_pair_registry"] != "CERTIFIED":
        raise RuntimeError("carrier registry")


def corrected_adapted_source_cell_registry() -> dict[str, Any]:
    return {
        "upstream_metric_mismatch": (
            "Round31 labels source cells as Euclidean-arclength 1e-90 intervals while also assigning the same 1e-90 adapted-length upper bound; the latter does not follow for slope V=4"
        ),
        "superseding_rule": (
            "on each canonical leaf define u_*(r)=integral_(r0)^r (kappa+4) dt and take oriented half-open u_* intervals [k*1e-90,(k+1)*1e-90), clipped at endpoints"
        ),
        "strict_monotonicity": "kappa+4>0, so u_* is a continuous strictly increasing leaf coordinate",
        "adapted_cell_length_upper": "1e-90",
        "Borel_parameter_dependence": (
            "kappa is constant on each circular obstacle chart and the clipped inverse u_* endpoints depend continuously on the leaf endpoint data"
        ),
        "same_parent_union": True,
        "artificial_recut_preserves_measure": True,
        "Round28_adapted_branch_rule_reused": True,
        "Round31_Euclidean_cell_bound_not_reused_as_adapted": True,
        "status": "CERTIFIED_CORRECTED_ADAPTED_SOURCE_CELL_SCHEMA",
    }


def refined_white_diagonal_crossing() -> dict[str, Any]:
    # R_ext controls density relative to the adapted line element
    # d ell_*=(kappa+V)|dr|.  On one monotone obstacle graph,
    # integral kappa dr<=2*pi and integral V dr=|Delta phi|<pi.
    # Thus ell_*(parent)<3*pi<66/7.  The diagonal crossing has
    # ell_*>=|Delta phi|=2*asin(1/50)>1/25.
    parent_length = Q(66, 7)
    crossing_length = Q(1, 25)
    arc_fraction = crossing_length / parent_length
    pair_hit = arc_fraction / R_EXT
    beta_threshold = HIT_GAP / pair_hit
    assert arc_fraction == Q(7, 1650)
    assert pair_hit == Q(2798558021, 660000000000)
    assert beta_threshold == Q(230400, 5197322039)
    assert Q(1, 22557) >= beta_threshold
    assert Q(1, 22558) < beta_threshold
    assert Q(1, 22557) * pair_hit - HIT_GAP == Q(
        1324673, 193539060000000000
    )
    return {
        "selected_component": "W",
        "selected_C24_core_type": "one W diagonal core with p in [-1/50,1/50]",
        "transverse_crossing_predicate": (
            "one connected extended-parent graph arc stays in the strict t-interior and joins p=-1/50 to p=1/50; deleting endpoints leaves the same arclength inside C24"
        ),
        "adapted_line_element": "dell_*=(kappa+V)*abs(dr)",
        "crossing_arc_adapted_length_strict_lower": "ell_*>=abs(Delta_phi)=2*asin(1/50)>1/25",
        "whole_parent_adapted_length_bound": "integral(kappa dr)<=2*pi and integral(V dr)=abs(Delta_phi)<pi",
        "extended_parent_adapted_length_strict_upper": qstr(parent_length),
        "crossing_adapted_length_fraction_strict_lower": qstr(arc_fraction),
        "extended_density_ratio_strict_upper_R_ext": qstr(R_EXT),
        "one_crossing_bundle_hit_fraction_strict_lower": qstr(pair_hit),
        "beta_Wdiag_definition": (
            "at one common terminal collision H_cover, total source-family weight of disjoint W-diagonal-crossing extended-parent bundle IDs divided by mass(G); artificial children of one bundle are counted once"
        ),
        "first-hit-stopping-time_beta_not_substituted": True,
        "sufficient_actual_crossing_family_weight": f"beta_Wdiag>={qstr(beta_threshold)}",
        "equality_is_sufficient_because_hit_fraction_is_strict": True,
        "safe_reciprocal_beta": "1/22557",
        "first_failing_reciprocal_beta": "1/22558",
        "safe_beta_hit_excess": "1324673/193539060000000000",
        "round45_46_metric_correction": (
            "the former Euclidean arc fraction cannot be multiplied by an adapted-density ratio without a line-element conversion; the old pair-hit number is not reused"
        ),
        "ratio_to_former_round46_numeric_pair_hit": "140/11 (comparison only; former metric interface superseded)",
        "numeric_H_cover_or_actual_beta_Wdiag_inferred": False,
        "status": "CERTIFIED_REFINED_CONDITIONAL_MINORISATION",
    }


def one_step_postcut_envelope() -> dict[str, Any]:
    replay_z1 = DENSITY_RATIO * B0 * THETA + 2
    envelope = Z1 * C_P
    assert replay_z1 == Z1
    assert envelope == Q(24490123368 * 10**90, 119621)
    assert 2**316 < envelope < 2**317
    return {
        "source": "one whole adapted canonical proper standard family G with every leaf length<=1e-90 and aggregate Z(G)<=C_p*mass(G)",
        "direct_one_step_replay": (
            "density_ratio*B0*theta+2=(2000/1999)*49*(900337/901685)+2=Z1"
        ),
        "recut_term_reason": (
            "natural 1e-90 recut contributes at most 2e90*mass(G)<=2*Z(G)"
        ),
        "killed_output": "H=O_s G, the whole positive post-C24-cut survivor family before normalization",
        "one_step_unnormalized_bound": "Z(H)<=Z1*Z(G)<=P*mass(G)",
        "Z1": qstr(Z1),
        "P_exact": qstr(envelope),
        "P_power_bracket": "2^316<P<2^317",
        "large_9148_step_Z0_not_used": True,
        "normalised_same-proper-class_return_inferred_directly": False,
        "status": "CERTIFIED_ONE_STEP_POSTCUT_ENVELOPE",
    }


def sample_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for k in (0, 1, 14, 64, 128):
        exponent = POSTCUT_BASE + k
        clock = RECOVERY_HALF_BLOCK * exponent
        rows.append(
            {
                "shell_k": k,
                "survivor_fraction": f"2^(-{k + 1})<x<=2^(-{k})",
                "normalized_Z_strict_upper": f"2^({exponent})",
                "closed_recovery_iterations": clock,
            }
        )
    return rows


def per_orientation_dyadic_return() -> dict[str, Any]:
    assert CLOSED_MARGIN == 1 - CLOSED_CONTRACTION
    assert C_P == 2 * CLOSED_ADDITIVE / CLOSED_MARGIN
    assert CLOSED_CONTRACTION**RECOVERY_HALF_BLOCK <= Q(1, 2)
    assert C_P > 2
    rows = sample_rows()
    return {
        "orientation_scope": "forward or reverse separately; the proof is applied to each whole positive survivor standard family",
        "zero_survivor_policy": "mass(H)=0 is absorbed and is never normalized",
        "positive_fraction": "x=mass(H)/mass(G) in (0,1]",
        "dyadic_shell": "unique k>=0 with 2^(-(k+1))<x<=2^(-k)",
        "normalized_postcut_bound": "Z(H)/mass(H)<2^(318+k)",
        "closed_recovery_recurrence": (
            "Z(T_s^r H)/mass(H)<=a^r*Z(H)/mass(H)+(2e90)/(1-a)"
        ),
        "per_orientation_postcut_clock": "R_post(k)=1005*(318+k)=319590+1005*k",
        "clock_origin": "closed iterations counted after the final C24 cut; a future full collision clock must add H_cover",
        "proof": (
            "a^1005<=1/2 makes the inherited normalized term <1, while the steady term is C_p/2 and 1+C_p/2<C_p"
        ),
        "restriction_preserves_regular_density_and_curvature_class": True,
        "single_short_leaf_assumed_proper": False,
        "same_proper_class_return": "CERTIFIED_PER_ORIENTATION_DYADIC_FAMILYWISE",
        "same_ID_forward_reverse_survivor_or_common_k_asserted": False,
        "sample_rows": rows,
        "sample_rows_sha256": digest(rows),
    }


def per_orientation_shell_moment() -> dict[str, Any]:
    assert NATIVE_ETA_ONE_ORIENTATION * RECOVERY_HALF_BLOCK == Q(1, 6)
    assert NATIVE_ETA_ONE_ORIENTATION * 319590 == 53
    assert Q(1, 2) * Q(6, 5) == Q(3, 5)
    return {
        "registry": (
            "for one orientation, assign each whole positive post-cut proper-family input its unique k and let m_k be the sum of its survivor-family masses"
        ),
        "shell_mass_bound": "m_k<=2^(-k)*sum_parent_mass",
        "index_scope": "an explicitly finite or countable discrete list of whole proper-family inputs",
        "clock_weight_eta": qstr(NATIVE_ETA_ONE_ORIENTATION),
        "base_exponent": "eta*319590=53=(318)/6",
        "slope_exponent": "eta*1005=1/6",
        "rational_exponential_bound": "exp(1/6)<1/(1-1/6)=6/5",
        "geometric_ratio_upper": "(1/2)*(6/5)=3/5",
        "aggregate_bound": (
            "sum_k m_k*exp(eta*R_post(k))<(5/2)*(6/5)^318*sum_parent_mass"
        ),
        "finite_or_countable_registry_extension": "finite sums directly; countable discrete sums by monotone convergence",
        "standard_Borel_mass_kernel_or_disintegration_claimed": False,
        "same_ID_joint_moment_claimed": False,
        "status": "CERTIFIED_CONDITIONAL_FINITE_OR_COUNTABLE_FAMILY_SHELL_LEMMA",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "every fixed |s|<=1/400",
            "claim_type": (
                "refined white-diagonal extended-parent crossing lower bound plus per-orientation dyadic post-cut recovery"
            ),
        },
        "corrected_adapted_source_cell_registry": corrected_adapted_source_cell_registry(),
        "refined_white_diagonal_crossing_minorisation": refined_white_diagonal_crossing(),
        "one_step_postcut_Z_envelope": one_step_postcut_envelope(),
        "per_orientation_dyadic_postcut_return": per_orientation_dyadic_return(),
        "per_orientation_postcut_shell_moment": per_orientation_shell_moment(),
        "corrected_frontier": {
            "numeric_H_cover": None,
            "numeric_actual_crossing_weight_beta_Wdiag": None,
            "crossing_weight_cannot_be_inferred_from_ambient_hit_gap": True,
            "uniform_normalized_postcut_clock": False,
            "same_ID_two_orientation_survivor_registry": "NOT_CERTIFIED",
            "same_ID_two_orientation_clock_or_joint_moment": "NOT_CERTIFIED",
            "standard_Borel_parent_survivor_mass_kernel": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
            "strong_cemetery_current_envelope": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "refined_conditional_one_crossing_hit_and_beta_threshold": "CERTIFIED",
            "adapted_source_cell_metric_correction": "CERTIFIED",
            "one_orientation_post_C24_cut_same_proper_class_return": "CERTIFIED_DYADIC_FAMILYWISE",
            "per_orientation_postcut_exponential_shell_moment": "CERTIFIED_CONDITIONAL_FINITE_OR_COUNTABLE",
            "same_ID_two_orientation_postcut_return": "NOT_CERTIFIED",
            "numeric_H_cover_and_actual_beta": "NOT_CERTIFIED",
            "numeric_proper_family_C24_minorization": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
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
        default=HERE / "cm2_gate34_round47_postcut_dyadic_recovery_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    strict = result["strict_nonpromotion"]
    print("REFINED_CROSSING_THRESHOLD:", strict["refined_conditional_one_crossing_hit_and_beta_threshold"])
    print("PER_ORIENTATION_POSTCUT_RETURN:", strict["one_orientation_post_C24_cut_same_proper_class_return"])
    print("NUMERIC_H_COVER_ACTUAL_BETA: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
