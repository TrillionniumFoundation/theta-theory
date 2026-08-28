#!/usr/bin/env python3
"""C24 open-hole geometry and sparse-opening theorem interface.

This append-only certificate replays the twenty-four compact collision cores
and proves three inputs that were still missing after Round 24:

* a strict normalized collision-SRB upper bound for their union;
* Demers--Liverani assumptions (O1), (O1') and (O2), with explicit uniform
  constants, in the common ``(r, phi)`` collision gauge;
* an exact match to the qualitative sparse-opening cone-recovery theorem.

The cited theorem controls normalized cone recovery/loss of memory when the
hole is opened only after sufficiently long mixing blocks.  This certificate
does not manufacture an unnormalised mass-loss gap, a numerical block length,
an every-collision exponential survivor tail, or a branchwise strong ``q``
tail.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json": (
        "098f9f52580fbb71d2416b07330aefa4f67488115f000bb60d37eec521250625"
    ),
    "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json": (
        "173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9"
    ),
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json": (
        "1213a6b66fca6d3a776a75244c334dacfeb822240f7c7eeadcb565553e62a53a"
    ),
}


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def parse_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else (
        f"{value.numerator}/{value.denominator}"
    )


def load_dependencies() -> dict[str, dict[str, Any] | str]:
    loaded: dict[str, dict[str, Any] | str] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        if path.suffix == ".json":
            value = parse_json_text(path.read_text(encoding="utf-8"))
            require(isinstance(value, dict), f"dependency JSON type: {name}")
            loaded[name] = value
        else:
            loaded[name] = expected

    registry = loaded[
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ]
    require(isinstance(registry, dict), "registry manifest")
    physical = registry["result"]["physical_return_core_registry"]
    require(physical["physical_compact_homogeneous_core_count"] == 24, "core count")
    require(
        physical["rows_sha256"]
        == "c3042515b4a244b064f1aaef97ee236c5d3f6078a53fe3fb9e865a1976853b2f",
        "core rows",
    )
    require(
        physical[
            "collision_SRB_normalized_mass_strict_lower_using_pi_lt_22_over_7"
        ]
        == "147/550000",
        "mass lower",
    )

    family_manifest = loaded[
        "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
    ]
    require(isinstance(family_manifest, dict), "family manifest")
    family = family_manifest["result"]["uniform_configuration_and_recovery"]
    require(family["compact_configuration_path"]["parameter_window"] == "|s|<=1/400", "parameter")
    require(family["compact_configuration_path"]["uniform_curvature_interval"] == "[25/9,25/4]", "curvature")
    require(family["compact_configuration_path"]["declared_SYZ_tau_bar_min"] == "1/25", "flight")
    require(family["compact_configuration_path"]["one_compact_SYZ_configuration_class"] is True, "compact family")
    require(
        family["solid_section_typing"]["common_gauge"]
        == "fixed obstacle labels and boundary arclength coordinates",
        "common gauge",
    )

    cone_manifest = loaded[
        "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json"
    ]
    require(isinstance(cone_manifest, dict), "cone manifest")
    cone = cone_manifest["result"]["global_invariant_geometric_cone"]
    require(cone["curvature_lower"] == "25/9", "cone lower")
    require(cone["cone_upper"] == "4108425/145348", "cone upper")
    require(cone["strict_forward_invariance"] is True, "cone invariance")

    kac_manifest = loaded[
        "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json"
    ]
    require(isinstance(kac_manifest, dict), "Kac manifest")
    require(
        kac_manifest["verdict"]["q_weighted_exponential_excursion_cemetery_tail"]
        == "NOT_CERTIFIED",
        "Kac scope",
    )
    return loaded


def replay_core_geometry() -> tuple[list[Any], dict[str, Any]]:
    cores = list(core_cert.physical_cores())
    require(len(cores) == 24, "replayed core count")
    require(sum(row.family == "axis_translate" for row in cores) == 8, "axis count")
    require(sum(row.family.startswith("diagonal_") for row in cores) == 16, "diagonal count")
    per_source = {
        source: sum(row.source == source for row in cores) for source in ("G", "W")
    }
    require(per_source == {"G": 12, "W": 12}, "per-source rectangle count")

    for row in cores:
        require(row.p0 < row.p1 and row.t0 < row.t1, "positive rectangle")
        if row.family == "axis_translate":
            require((row.t0, row.t1, row.p0, row.p1) == (
                Q(1, 100), Q(1, 50), -Q(1, 500), Q(1, 500)
            ), "axis geometry")
        else:
            require((row.t1 - row.t0) == Q(1, 100), "diagonal t width")
            require((row.p0, row.p1) == (-Q(1, 50), Q(1, 50)), "diagonal p")
            require(max(abs(row.t0), abs(row.t1)) == Q(7, 10), "diagonal t range")

    rows = [
        {
            "chart_id": row.chart_id,
            "family": row.family,
            "source": row.source,
            "t": [qstr(row.t0), qstr(row.t1)],
            "p": [qstr(row.p0), qstr(row.p1)],
            "target_id": row.target_id,
        }
        for row in cores
    ]
    rows.sort(key=canonical_json)
    return cores, {
        "core_count": 24,
        "rectangle_count_per_collision_component": per_source,
        "boundary_edge_count_per_collision_component": 48,
        "vertical_edge_count_per_collision_component": 24,
        "horizontal_edge_count_per_collision_component": 24,
        "core_rows_sha256": (
            "c3042515b4a244b064f1aaef97ee236c5d3f6078a53fe3fb9e865a1976853b2f"
        ),
        "open_hole_geometry_rows_sha256": canonical_digest(rows),
    }


def mass_upper(cores: list[Any]) -> dict[str, Any]:
    radius = core_cert.first_hit.RADIUS
    axis_base = sum(
        radius[row.source] * (row.t1 - row.t0) * (row.p1 - row.p0)
        for row in cores if row.family == "axis_translate"
    )
    diagonal_base = sum(
        radius[row.source] * (row.t1 - row.t0) * (row.p1 - row.p0)
        for row in cores if row.family.startswith("diagonal_")
    )
    require(axis_base == Q(13, 156250), "axis mass base")
    require(diagonal_base == Q(26, 15625), "diagonal mass base")

    axis_derivative_upper = Q(1001, 1000)
    diagonal_derivative_upper = Q(1401, 1000)
    require(
        axis_derivative_upper**2 > 1 / (1 - Q(1, 50) ** 2),
        "axis dtheta/dt upper",
    )
    require(
        diagonal_derivative_upper**2 > 1 / (1 - Q(7, 10) ** 2),
        "diagonal dtheta/dt upper",
    )
    raw_upper = (
        axis_base * axis_derivative_upper
        + diagonal_base * diagonal_derivative_upper
    )
    require(raw_upper == Q(377273, 156250000), "raw upper")

    radii_sum = radius["G"] + radius["W"]
    require(radii_sum == Q(13, 25), "radii sum")
    # Total collision volume is 4*pi*(R_G+R_W), and pi>3.
    normalized_upper = raw_upper / (4 * Q(3) * radii_sum)
    require(normalized_upper == Q(29021, 75000000), "normalized upper")
    require(normalized_upper < Q(1, 2500) < Q(1, 2), "small mass upper")
    require(Q(147, 550000) < normalized_upper, "consistent mass interval")
    return {
        "collision_SRB_axis_unnormalized_base": qstr(axis_base),
        "collision_SRB_diagonal_unnormalized_base": qstr(diagonal_base),
        "axis_dtheta_dt_strict_upper": qstr(axis_derivative_upper),
        "diagonal_dtheta_dt_strict_upper": qstr(diagonal_derivative_upper),
        "collision_SRB_unnormalized_strict_upper": qstr(raw_upper),
        "normalization_denominator_strict_lower_using_pi_gt_3": qstr(
            4 * Q(3) * radii_sum
        ),
        "normalized_core_mass_strict_lower": "147/550000",
        "normalized_core_mass_strict_upper": qstr(normalized_upper),
        "normalized_core_mass_strict_upper_simplification": "1/2500",
        "normalized_core_mass_at_most_one_half": True,
        "same_bounds_for_every_|s|<=1/400": True,
    }


def stable_geometry() -> dict[str, Any]:
    slope_lower = Q(25, 9)
    slope_upper = Q(4108425, 145348)
    require(slope_upper < 29, "stable slope upper")

    # Each stable curve is a graph phi(r).  Every vertical or horizontal
    # boundary segment is met at most once.  There are 48 segments on the
    # collision component containing W, so at most 49 cut pieces.
    p0 = 49
    vertical_edge_count = 24
    horizontal_edge_count = 24
    require(1 + vertical_edge_count + horizontal_edge_count == p0, "P0")

    # In an epsilon strip around r=constant, ds/dr<sqrt(1+29^2)<30,
    # hence one vertical edge contributes <60 epsilon.  Around phi=constant,
    # |dr/dphi|<9/25 and ds/dphi<11/10, hence one horizontal edge contributes
    # <(11/5) epsilon.
    require(1 + Q(29) ** 2 < Q(30) ** 2, "vertical arclength factor")
    require(1 + (1 / slope_lower) ** 2 < Q(11, 10) ** 2, "horizontal factor")
    vertical_o2 = vertical_edge_count * Q(60)
    horizontal_o2 = horizontal_edge_count * Q(11, 5)
    exact_o2_upper = vertical_o2 + horizontal_o2
    require(exact_o2_upper == Q(7464, 5) < 1493, "O2 constant")

    # Stable diameter: a stable graph inside the disconnected hole lies in
    # one rectangle.  Its length is at most total r and phi variation.
    axis_t_factor = Q(1001, 1000)
    diagonal_t_factor = Q(1401, 1000)
    p_factor = Q(1001, 1000)
    max_radius = Q(9, 25)
    axis_length_upper = (
        max_radius * Q(1, 100) * axis_t_factor
        + Q(1, 250) * p_factor
    )
    diagonal_length_upper = (
        max_radius * Q(1, 100) * diagonal_t_factor
        + Q(1, 25) * p_factor
    )
    require(axis_length_upper == Q(19019, 2500000) < Q(1, 100), "axis diameter")
    require(diagonal_length_upper == Q(112709, 2500000) < Q(1, 20), "diagonal diameter")

    return {
        "common_collision_coordinates": "(r,phi)_on_N=G_disjoint_union_W",
        "stable_curve_form": "C2_graph_phi(r)_with_strictly_negative_slope",
        "stable_slope_interval": (
            "-4108425/145348<dphi/dr<-25/9"
        ),
        "time_reversal_of_frozen_invariant_unstable_cone": True,
        "rectangles_on_each_collision_component": 12,
        "boundary_edges_on_each_collision_component": 48,
        "each_vertical_edge_meets_a_stable_graph_at_most_once": True,
        "each_horizontal_edge_meets_a_stable_graph_at_most_once": True,
        "O1_complexity_P0": p0,
        "O1_prime_complexity_P0": p0,
        "vertical_edge_O2_coefficient_strict_upper": "60",
        "horizontal_edge_O2_coefficient_strict_upper": "11/5",
        "summed_O2_coefficient_strict_upper": qstr(exact_o2_upper),
        "certified_O2_constant_Ct": 1493,
        "O2_statement": "m_W(N_epsilon(boundary_C24))<=1493*epsilon",
        "large_epsilon_guard": (
            "for_epsilon>=1/(2*1493),_|W|<delta0<1/2<=1493*epsilon"
        ),
        "axis_component_stable_diameter_strict_upper": qstr(axis_length_upper),
        "diagonal_component_stable_diameter_strict_upper": qstr(
            diagonal_length_upper
        ),
        "C24_stable_diameter_strict_upper": "1/20",
        "all_constants_uniform_for_|s|<=1/400": True,
    }


def theorem_interface() -> dict[str, Any]:
    return {
        "source": (
            "Demers--Liverani,_Projective_cones_for_sequential_dispersing_"
            "billiards,_arXiv:2104.06947v3"
        ),
        "checked_sections": [
            "Section_8_definition_(O1)/(O2)",
            "Section_8.2_definition_(O1_prime)",
            "Proposition_8.7",
            "Theorem_8.9_and_footnote_25",
        ],
        "hole": "H=C24_in_the_common_solid_collision_section",
        "O1": "CERTIFIED_WITH_P0=49",
        "O1_prime": "CERTIFIED_WITH_P0=49",
        "O2": "CERTIFIED_WITH_Ct=1493",
        "mu_SRB_H_at_most_one_half": True,
        "compact_uniform_table_family": True,
        "fixed_s_sequence_is_admissible": (
            "constant_configuration_sequence_K_s,K_s,..."
        ),
        "large_hole_sparse_opening_cone_recovery": (
            "CERTIFIED_THEOREM_MATCH_WITH_EXISTENTIAL_DELTA_CHI_J_NSTAR"
        ),
        "theorem_supplied_sparse_constants_uniform_over_parameter_window": True,
        "numeric_delta": None,
        "numeric_sparse_block_n_star": None,
        "numeric_cone_contraction_chi": None,
        "small_hole_Lemma_8_3_threshold": (
            "NOT_CERTIFIED:_diam_s(C24)<1/20_is_not_compared_to_"
            "delta*(1/(4*P0*A))^(1/q)"
        ),
        "normalized_sparse_open_loss_of_memory": "THEOREM_INTERFACE_INSTALLED",
        "stationary_unnormalized_mass_loss_gap": "NOT_CERTIFIED",
        "sampled_survivor_exponential_mass_bound": "NOT_CERTIFIED",
        "every_collision_survivor_exponential_mass_bound": "NOT_CERTIFIED",
        "why_subset_argument_stops": (
            "every-collision_avoidance_is_a_subset_of_sparse-sample_avoidance,_"
            "but_Proposition_8.7/Theorem_8.9_cone_recovery_and_normalized_"
            "memory_loss_do_not_by_themselves_install_an_unnormalized_escape_"
            "eigenvalue_gap_for_this_C24_killed_operator"
        ),
    }


def strict_scope() -> dict[str, Any]:
    return {
        "C24_exact_normalized_mass_upper": "CERTIFIED",
        "C24_O1_O1prime_O2_geometry": "CERTIFIED",
        "C24_sparse_opening_theorem_admission": "CERTIFIED_QUALITATIVE",
        "C24_numeric_sparse_block": "NOT_CERTIFIED",
        "unweighted_every_collision_exponential_return_tail": "NOT_CERTIFIED",
        "q_weighted_exponential_excursion_cemetery_tail": "NOT_CERTIFIED",
        "full_2d_Rn_Qn_partition": "NOT_CERTIFIED",
        "branch_Jacobian_distortion_mass_q_payload": "NOT_CERTIFIED",
        "induced_common_strong_Lasota_Yorke_coefficient": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }


def certify() -> dict[str, Any]:
    load_dependencies()
    cores, inventory = replay_core_geometry()
    result = {
        "schema": "cm2.gate34.c24-open-hole-geometry.v1",
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "parameter_quantifier": "for_every_fixed_s_with_|s|<=1/400",
            "old_artifacts_modified": False,
            "literature_checked_through": "2026-07-18",
        },
        "frozen_core_inventory": inventory,
        "collision_SRB_core_mass_interval": mass_upper(cores),
        "stable_curve_open_hole_geometry": stable_geometry(),
        "sparse_opening_theorem_interface": theorem_interface(),
        "strict_scope": strict_scope(),
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("C24_NORMALIZED_COLLISION_SRB_MASS_STRICT_UPPER_1_OVER_2500: CERTIFIED")
    print("C24_OPEN_HOLE_O1_O1PRIME_O2: CERTIFIED")
    print("C24_SPARSE_OPENING_THEOREM_ADMISSION: CERTIFIED_QUALITATIVE")
    print("C24_EVERY_COLLISION_EXPONENTIAL_SURVIVOR_TAIL: NOT_CERTIFIED")
    print("GATE3_GATE4_GATE5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
