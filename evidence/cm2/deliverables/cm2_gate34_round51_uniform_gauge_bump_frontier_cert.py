#!/usr/bin/env python3
"""Round-51 Gate-4 fixed-gauge and uniform bump-minorisation frontier.

Round 50 used an abstract measure-trivialising diffeomorphism ``A_s`` and
therefore left its least singular value nonnumerical.  The frozen pilot is
much more special: the gray disk is fixed, the white disk is translated by
``(s,0)``, both radii are fixed, and every collision component uses intrinsic
boundary arclength and outgoing angle.  In that gauge the labelled coordinate
map is the identity, so its chart derivative is exactly ``I`` and the
Climenhaga--Day curve-length scale is unchanged.

The same fixed gauge also permits the uniform (but noneffective) memory-loss
theorem of Stenlund--Young--Zhang to be applied to the already frozen C1 bump
inside C24.  This gives one finite integer, common to the full parameter
window and all normalized canonical proper families, at which the C24 mass
is strictly larger than the required hit gap.  The theorem publishes no
values for its exponential constants, so this integer is not numerical.

Nothing here materialises the finite proper-crossing Cantor source cover,
an effective mixing time, a transverse crossing width, C_fw/C_rev, q, the
strong cemetery, Gate 4, or CM2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert as growth


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round51-uniform-gauge-bump-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round51-uniform-gauge-bump-frontier-manifest-2026-07-20.json"
)

DEPENDENCIES = {
    "cm2-gate34-round50-same-cover-target-adjunction-manifest-2026-07-19.json": (
        "03b9850b0dc3e2631b47e44ceb966cbf7b1b2b49263ca328662a03a0b8a7fc07"
    ),
    "cm2-gate34-round49-incidence-safe-long-leaf-atlas-manifest-2026-07-19.json": (
        "f8117b4d6b91c85597953366bc1eee26652a6ff7c3bd5486d3a3a38694550c18"
    ),
    "cm2-gate34-round44-proper-family-c24-minorization-frontier-manifest-2026-07-19.json": (
        "10952d4f27df11f6c5c9503999b8ba5795070f84d7cca455d697c7b962a65018"
    ),
    "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json": (
        "02277a2c10ea905fd8a4cf9998ae364a4b024087624fd3bea0a8a4175405727d"
    ),
    "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json": (
        "098f9f52580fbb71d2416b07330aefa4f67488115f000bb60d37eec521250625"
    ),
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json": (
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py": (
        "01e32ca209818f4077443a7692622c4202ab7f1066e2f95802185e2be7a2cc9a"
    ),
    "cm2_gate3_depth_one_fixed_gauge_dq_cert.py": (
        "8ce2490ee2b2bdfc251ac1892cb260e40f3eb5d87ce7f232c2076a10c4a9c066"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-bridge-note-v51.tex": (
        "da0f4ac7a6a914bef07d4e3b05d844803b251cc60f2486f943aca3abed4736bc"
    ),
}

ARXIV_1210_SOURCE_SHA256 = (
    "b705ed4fc89a42ac8e78957d65873211c71f9566599bfba90173812fe5ffe5c5"
)
ARXIV_1210_MAIN_TEX_SHA256 = (
    "921fe3477c2f3280a256a459c9e2a2bc6b719a971016a8320e6d0d5e9cd25f44"
)
ARXIV_2604_SOURCE_SHA256 = (
    "b8f79a99f5f98648f91848cd7b4e489846f4512d6ed35ebd042229da3c89ee94"
)
ARXIV_2604_ARCHIVE_SHA256 = (
    "bd03bb220ca4456e65a511669b76a903f2a1dba6629de70935490664104ce5b4"
)
ARXIV_1807_SOURCE_SHA256 = (
    "c1e0189b271fdd1303b425d096a9e1d8685a83f74d139b37a534a0530a6020aa"
)
ARXIV_1807_ARCHIVE_SHA256 = (
    "f360f57301e51d325e6ccd8e3095153cba5aa46985c9212af47eb4954bc3905d"
)

HIT_GAP = Q(21, 111718750)
BUMP_MASS = Q(21, 55859375)
BUMP_C1 = 2724
SAFE_FAMILY_MASS = Q(1999, 32000)
DIRECT_REQUIRED_FRACTION = Q(2688, 893303125)
R_G = Q(9, 25)
R_W = Q(4, 25)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate key: {key}")
        value[key] = item
    return value


def reject_json_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def load_json(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_json_constant,
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def checked_text(name: str, tokens: tuple[str, ...]) -> str:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe source dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"source dependency hash: {name}")
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            raise RuntimeError(f"source token {name}: {token}")
    return text


def validate_dependencies() -> dict[str, Any]:
    for name in DEPENDENCIES:
        path = HERE / name
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
            raise RuntimeError(f"unsafe dependency: {name}")
        if sha(path) != DEPENDENCIES[name]:
            raise RuntimeError(f"dependency hash: {name}")

    r50 = load_json(
        "cm2-gate34-round50-same-cover-target-adjunction-manifest-2026-07-19.json"
    )["result"]
    bridge50 = r50["fixed_parameter_enlarged_cover_target_adjunction"]
    if bridge50["status"] != "CERTIFIED_FIXED_S_QUALITATIVE_ENLARGED_COVER_ADJUNCTION":
        raise RuntimeError("Round50 bridge")
    if bridge50["numeric_m_s"] is not None or bridge50["numeric_N_s"] is not None:
        raise RuntimeError("Round50 numerical scope")
    delta_rect = Q(bridge50["numeric_input_delta_rect"])

    r49 = load_json(
        "cm2-gate34-round49-incidence-safe-long-leaf-atlas-manifest-2026-07-19.json"
    )["result"]
    core49 = r49["incidence_safe_long_leaf_compact_core"]
    threshold49 = r49["exact_remaining_cover_thresholds"]
    if Q(core49["incidence_safe_family_mass_strict_lower"]) != SAFE_FAMILY_MASS:
        raise RuntimeError("Round49 safe mass")
    if Q(threshold49["incidence_safe_required_direct_C24_fraction"]) != DIRECT_REQUIRED_FRACTION:
        raise RuntimeError("Round49 direct fraction")
    if Q(threshold49["direct_C24_hit_gap"]) != HIT_GAP:
        raise RuntimeError("Round49 hit gap")

    r44 = load_json(
        "cm2-gate34-round44-proper-family-c24-minorization-frontier-manifest-2026-07-19.json"
    )["result"]
    bump = r44["direct_smooth_bump_mixing_route"]["frozen_bump"]
    if Q(bump["mu_s_g_strict_lower"]) != BUMP_MASS:
        raise RuntimeError("Round44 bump mass")
    if int(bump["C1_norm_strict_upper"]) != BUMP_C1:
        raise RuntimeError("Round44 bump norm")
    if bump["support"] != "closure strictly inside one C24 core":
        raise RuntimeError("Round44 bump support")
    sparse_bump = load_json(
        "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json"
    )["result"]["explicit_C1_bump"]
    if sparse_bump["chart"] != "G:E":
        raise RuntimeError("bump chart")
    if sparse_bump["support_rectangle"] != {
        "t": ["11/1000", "19/1000"],
        "p": ["-3/2000", "3/2000"],
    }:
        raise RuntimeError("bump support rectangle")
    if sparse_bump["global_C1_on_collision_section"] is not True:
        raise RuntimeError("global C1 bump")

    mesh = load_json(
        "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
    )["result"]
    config = mesh["uniform_configuration_and_recovery"]
    compact = config["compact_configuration_path"]
    gauge = config["solid_section_typing"]
    if compact["path"] != "K_s: gray disk fixed, white disk translated by (s,0)":
        raise RuntimeError("physical path")
    if compact["scatterer_boundaries"] != "two fixed-radius circular C^infinity boundaries":
        raise RuntimeError("fixed radii")
    if compact["parameter_window"] != "|s|<=1/400":
        raise RuntimeError("parameter window")
    if gauge["common_gauge"] != "fixed obstacle labels and boundary arclength coordinates":
        raise RuntimeError("common arclength gauge")
    if gauge["map_used"] != "T_s=F_{K_s,K_s} in the canonical fixed-configuration gauge":
        raise RuntimeError("physical map gauge")

    hole = load_json(
        "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json"
    )["result"]
    if hole["frozen_core_inventory"]["core_count"] != 24:
        raise RuntimeError("C24 core count")
    if hole["collision_SRB_core_mass_interval"]["normalized_core_mass_strict_upper_simplification"] != "1/2500":
        raise RuntimeError("C24 mass upper")
    if hole["stable_curve_open_hole_geometry"]["common_collision_coordinates"] != "(r,phi)_on_N=G_disjoint_union_W":
        raise RuntimeError("C24 collision coordinates")

    growth_manifest = load_json(
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    )
    if growth_manifest["replay_summary"]["density_ratio"] != "2000/1999":
        raise RuntimeError("canonical density ratio")
    growth_result = growth.certify()
    density = growth_result["invariant_density_and_distortion"][
        "invariant_adapted_density_cone"
    ]
    if density["numeric_regular_density_invariance"] != "CERTIFIED":
        raise RuntimeError("numeric density invariance")
    if density["density_constant"] != "500000000000000000000000000":
        raise RuntimeError("density constant")
    if density["inverse_contraction_cube_root_strict_upper"] != "93/100":
        raise RuntimeError("density separation rate")
    growth_data = growth_result["numeric_growth_and_recovery"]
    growth_constants = growth_data["numeric_Growth_Lemma_constants"]
    if growth_constants["numeric_C_p_vartheta_p"] != "CERTIFIED":
        raise RuntimeError("numeric proper-family envelope")
    cp_euclidean = Q(growth_constants["euclidean_C_p"])
    if cp_euclidean <= 0:
        raise RuntimeError("euclidean C_p positivity")

    checked_text(
        "cm2_gate3_depth_one_fixed_gauge_dq_cert.py",
        (
            '"path": "horizontal center translation of W with both radii fixed"',
            '"collision_space": "N=G disjoint-union W in common arclength coordinates"',
            '"invariant_probability": "the same normalized cos(phi)dr dphi for every s"',
        ),
    )
    checked_text(
        "cm2_gate25_physical_return_core_registry_cert.py",
        (
            "AXIS_T_LOWER = Q(1, 100)",
            "AXIS_T_UPPER = Q(1, 50)",
            "AXIS_P_HALF_WIDTH = Q(1, 500)",
            'f"{source}:{cell}"',
        ),
    )
    checked_text(
        "cm2-bridge-note-v51.tex",
        (
            "Use arclength and outgoing angle on every component.",
            "spaces are the same disjoint union $M$",
            "measure-trivializing gauge may be taken to be the common arclength gauge",
        ),
    )
    return {
        "delta_rect": delta_rect,
        "euclidean_C_p": cp_euclidean,
        "density_constant": Q(density["density_constant"]),
        "dynamic_density_rate": Q(93, 100),
    }


def fixed_gauge_identity(delta_rect: Q) -> dict[str, Any]:
    rows = [
        {
            "component": "G",
            "physical_motion": "fixed",
            "label_map": "A_s(G,r,phi)=(G,r,phi)",
            "coordinate_derivative": "I_2",
            "least_singular_value": "1",
        },
        {
            "component": "W",
            "physical_motion": "ambient translation by (s,0)",
            "label_map": "A_s(W,r,phi)=(W_s,r,phi) in intrinsic boundary-arclength/outgoing-angle labels",
            "coordinate_derivative": "I_2",
            "least_singular_value": "1",
        },
    ]
    return {
        "parameter_window": "|s|<=1/400",
        "physical_path": "G fixed; W translated horizontally by (s,0); radii 9/25 and 4/25 fixed",
        "collision_metric": "Euclidean chart metric in intrinsic (r,phi) coordinates on each collision component",
        "literature_metric_match": (
            "Climenhaga--Day parameterize each boundary component by arclength and define admissible u-curves as graphs in (r,phi); Baladi--Demers explicitly use the Euclidean metric on each collision component"
        ),
        "rows": rows,
        "rows_sha256": digest(rows),
        "generic_measure_trivializing_interface_used_for_numeric_bound": False,
        "generic_interface_warning": (
            "the abstract C^{r+1} measure-trivializing A_s in bridge-note-v51 is an imposed interface and publishes no C1 or sigma_min bound; m_s=1 follows only from this fixed-radius translation pilot and its common arclength gauge"
        ),
        "uniform_numeric_m_s": "1",
        "numeric_reference_delta_rect": str(delta_rect),
        "numeric_physical_delta_hat": str(delta_rect),
        "length_loss_under_pullback": "1",
        "status": "CERTIFIED_INSTANCE_SPECIFIC_UNIFORM_ISOMETRIC_GAUGE",
    }


def explicit_open_target() -> dict[str, Any]:
    # The frozen bump support sits in one G:E axis C24 core with t in
    # (1/100,1/50) and p in (-1/500,1/500).
    t0, t1 = Q(11, 1000), Q(19, 1000)
    p0, p1 = -Q(3, 2000), Q(3, 2000)
    assert Q(1, 100) < t0 < t1 < Q(1, 50)
    assert -Q(1, 500) < p0 < p1 < Q(1, 500)
    unnormalized = R_G * (t1 - t0) * (p1 - p0)
    normalization_upper = 4 * Q(22, 7) * (R_G + R_W)
    normalized_lower = unnormalized / normalization_upper
    assert unnormalized == Q(27, 3125000)
    assert normalization_upper == Q(1144, 175)
    assert normalized_lower == Q(189, 143000000)
    assert normalized_lower == Q(225, 32) * HIT_GAP
    return {
        "chart": "G:E axis-translate C24 core and frozen bump support",
        "coordinates": "t=sin(boundary-normal angle), p=sin(outgoing phi)",
        "ambient_C24_core": {
            "t": ["1/100", "1/50"],
            "p": ["-1/500", "1/500"],
        },
        "open_box_O_star": {
            "t": [str(t0), str(t1)],
            "p": [str(p0), str(p1)],
        },
        "closure_strictly_inside_C24": True,
        "uniform_for_parameter_window": "|s|<=1/400",
        "measure_change_of_variables": "dr=R_G*dt/sqrt(1-t^2), cos(phi)dphi=dp",
        "unnormalized_mass_strict_lower": str(unnormalized),
        "normalization_strict_upper_using_pi_lt_22_over_7": str(normalization_upper),
        "normalized_collision_mass_strict_lower": str(normalized_lower),
        "ratio_to_required_hit_gap": "225/32",
        "is_a_dynamical_Cantor_rectangle": False,
        "status": "CERTIFIED_NUMERIC_UNIFORM_OPEN_C24_TARGET_NOT_CANTOR_RECTANGLE",
    }


def literature_rows() -> list[dict[str, Any]]:
    return [
        {
            "paper": "Climenhaga--Day, arXiv:2604.25881v1",
            "official_source_sha256": ARXIV_2604_SOURCE_SHA256,
            "official_source_sha256_scope": "source-archive member billiard-mme-arXiv-v1.tex",
            "official_source_archive_sha256": ARXIV_2604_ARCHIVE_SHA256,
            "source_anchor": "phase space/arclength source lines 219--240, admissible curves 1068--1086, Proposition 3.19 and sketch 1568--1586",
            "safe_quantifier": (
                "for one fixed billiard and delta>0, a finite proper-crossing source subcover and one target-crossing iterate exist; no numerical rows, time, or source width are published"
            ),
        },
        {
            "paper": "Baladi--Demers, arXiv:1807.02330v4",
            "official_source_sha256": ARXIV_1807_SOURCE_SHA256,
            "official_source_sha256_scope": "source-archive member maxentropypublished.tex",
            "official_source_archive_sha256": ARXIV_1807_ARCHIVE_SHA256,
            "source_anchor": "Euclidean collision-component metric source lines 780--790; Cantor rectangles/proper crossing 2430--2468; cover 3914--3944; open target 4067--4096",
            "safe_quantifier": (
                "the collision chart metric is Euclidean and an open target contains a positive Cantor rectangle, but its dynamical sides and quantitative density/mixing data are not constructed"
            ),
        },
        {
            "paper": "Stenlund--Young--Zhang, arXiv:1210.0011v4",
            "official_source_sha256": ARXIV_1210_SOURCE_SHA256,
            "official_source_sha256_scope": "whole source tar archive",
            "main_tex_member": "Moving_final.tex",
            "main_tex_member_sha256": ARXIV_1210_MAIN_TEX_SHA256,
            "source_anchor": "Theorems 1/1' and equilibrium mixing source lines 588--710 and 1360--1400; Growth/proper families 1120--1145 and 1316--1355; magnet Proposition 31 source lines 2340 onward",
            "safe_quantifier": (
                "on one compact finite-horizon configuration class, normalized regular measured unstable families with uniformly bounded density regularity and Z have uniform exponential memory loss; the constants C_gamma and theta_gamma exist but are not numerical"
            ),
        },
    ]


def uniform_bump_minorisation(
    euclidean_cp: Q, density_constant: Q, dynamic_rate: Q
) -> dict[str, Any]:
    assert BUMP_MASS == 2 * HIT_GAP
    # Climenhaga--Day give |V|<=pi/kappa_min=9*pi/25<198/175.
    # Since ell_*<(141/4)ell_E, every homogeneous image has adapted length
    # <40.  Pulling back n common homogeneous iterates and taking the one-third
    # power converts the spatial log-Hoelder cone into the SYZ separation-time
    # cone with constant <4*5e26=2e27 and rate 93/100.
    global_euclidean_curve_length_upper = Q(198, 175)
    global_adapted_curve_length_upper = Q(141, 4) * global_euclidean_curve_length_upper
    assert global_adapted_curve_length_upper < 40 < 4**3
    dynamic_constant_upper = 4 * density_constant
    assert dynamic_constant_upper == 2 * 10**27
    assert dynamic_rate == Q(93, 100)
    formula = (
        "H_bump=max(0,1+ceil(log(2724*C_bump/epsilon_hit)/(-log(theta_bump))))"
    )
    return {
        "family_scope": (
            "every normalized canonical regular standard family G in the frozen numeric cone, with Z_E(G)<C_p_E, and every |s|<=1/400"
        ),
        "numeric_uniform_Z_envelope_C_p_E": str(euclidean_cp),
        "uniform_SYZ_dynamic_density_bridge": {
            "spatial_log_Holder": "abs(log rho(x)-log rho(y))<=5e26*ell_*(x,y)^(1/3)",
            "global_Euclidean_u_curve_length_strict_upper": str(global_euclidean_curve_length_upper),
            "global_adapted_u_curve_length_strict_upper": "40",
            "inverse_contraction_cube_root_strict_upper": str(dynamic_rate),
            "separation_time_conclusion": "abs(log rho(x)-log rho(y))<2e27*(93/100)^s(x,y)",
            "uniform_dynamic_density_constant_upper": str(dynamic_constant_upper),
            "status": "CERTIFIED_SPATIAL_TO_SYZ_DYNAMIC_REGULARITY",
        },
        "observable": "the frozen C1 bump g with 0<=g<=1_C24",
        "uniform_bump_mass_strict_lower": str(BUMP_MASS),
        "uniform_bump_theorem_norm": "norm_infinity(g)+Lipschitz_1(g)<2724",
        "theorem_join": (
            "apply SYZ Theorem 1' to normalized G and the common invariant collision probability for the stationary sequence K_s,K_s,...; the displayed separation-time density bridge and numeric Z envelope uniformly type G, while Lemma 1'implies1 embeds the smooth comparison probability whose density is the common constant 1"
        ),
        "comparison_probability_typing": {
            "law": "the same normalized cos(phi)dr dphi for every s",
            "density_relative_to_common_collision_law": "1",
            "log_density_constant": "0",
            "SYZ_smooth_to_measured_unstable_embedding": "Lemma 1'implies1 / Theorem 1' generalizes Theorem 1",
            "uniform_finite_Z_and_density_regularity": True,
        },
        "uniform_exponential_constants_exist": True,
        "numeric_C_bump": None,
        "numeric_theta_bump": None,
        "safe_time_formula": formula,
        "one_uniform_finite_integer_H_bump_exists": True,
        "numeric_H_bump": None,
        "conclusion": "(T_s^H_bump)_*G(C24)>epsilon_hit",
        "actual_whole_family_C24_hit_fraction_strict_lower_at_H_bump": str(HIT_GAP),
        "cover_crossing_source_fraction_per_retained_leaf": None,
        "does_not_require_materialized_Cantor_source_cover": True,
        "status": "CERTIFIED_UNIFORM_EXISTENTIAL_TIME_WITH_NUMERIC_HIT_FRACTION",
    }


def non_effectivity_countermodel() -> dict[str, Any]:
    return {
        "purpose": "show that qualitative 0<theta<1 and finite C do not determine any numerical H; this is not a billiard counterexample",
        "for_each_proposed_integer_H0": (
            "choose C=1 and theta=1-1/(2*(H0+1)); Bernoulli gives theta^H0>=1-H0/(2*(H0+1))>1/2"
        ),
        "resulting_error_majorant": (
            "2724*C*theta^H0>1362>21/111718750, so the published existential range alone cannot validate H0"
        ),
        "numeric_H_requires": "numerical upper C_bump and numerical upper theta_bump<1, or a direct interval crossing proof",
        "logical_obstruction_certified": True,
    }


def cover_frontier() -> dict[str, Any]:
    missing = [
        {
            "id": "R_Cantor",
            "meaning": "stable/unstable boundary data and a positive dense subset for one dynamical Cantor rectangle inside the explicit C24 open box",
            "value": None,
        },
        {
            "id": "K_rect",
            "meaning": "cardinality and interval coordinates of a finite proper-crossing Cantor source subcover at delta_rect",
            "value": None,
        },
        {
            "id": "delta_density",
            "meaning": "quantitative leafwise density radius for the target Cantor subset",
            "value": None,
        },
        {
            "id": "C_mix_theta_mix",
            "meaning": "effective correlation constants for the actual source/target sets or numeric C_bump,theta_bump for the smooth-bump bypass",
            "value": None,
        },
        {
            "id": "N_mix",
            "meaning": "a numerical common target-hit iterate",
            "value": None,
        },
        {
            "id": "r_transverse",
            "meaning": "numerical margin for a target crossing component",
            "value": None,
        },
        {
            "id": "J_branch",
            "meaning": "inverse unstable-Jacobian/distortion conversion to a source-subcurve fraction",
            "value": None,
        },
        {
            "id": "omega_parameter_dynamic",
            "meaning": "persistence modulus for labelled Cantor sides, singularity avoidance, and crossing branches across the parameter window",
            "value": None,
        },
    ]
    return {
        "resolved_rows": {
            "uniform_conjugacy_length_factor": "1",
            "uniform_physical_input_scale": "delta_rect",
            "explicit_uniform_open_C24_target": "CERTIFIED",
            "uniform_open_target_mass_strict_lower": "189/143000000",
            "uniform_finite_bump_hit_time_exists": True,
            "actual_whole_family_hit_fraction_at_that_time_strict_lower": str(HIT_GAP),
        },
        "original_cover_route_missing_numeric_rows": missing,
        "missing_rows_sha256": digest(missing),
        "finite_registry_type_audit": {
            "twenty_four_C24_boxes_total_normalized_mass_strict_upper": "1/2500",
            "twenty_four_boxes_are_target_coordinate_boxes_not_proper_Cantor_source_rectangles": True,
            "candidate_key_universe_441280_is_a_branch_envelope_not_a_proper_crossing_Cantor_cover": True,
            "therefore_existing_finite_registries_do_not_supply_K_rect": True,
        },
        "numeric_H_cover": None,
        "numeric_H_bump": None,
        "actual_cover_crossing_source_fraction": None,
        "strict_inferable_uniform_cover_source_fraction_lower": "0",
        "status": "PARTIALLY_RESOLVED_GAUGE_AND_TARGET_NUMERIC_CLOCK_STILL_NONEFFECTIVE",
    }


def build_result() -> dict[str, Any]:
    data = validate_dependencies()
    rows = literature_rows()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "official_versions_rechecked_2026_07_20": [
                "arXiv:1210.0011v4",
                "arXiv:2604.25881v1",
                "arXiv:1807.02330v4",
                "arXiv:2104.06947v3",
            ],
            "claim_type": (
                "instance-specific exact translation gauge, explicit uniform C24 open target, uniform existential-time bump minorisation, and fail-closed numerical cover frontier"
            ),
        },
        "literature_quantifier_audit": {
            "rows": rows,
            "rows_sha256": digest(rows),
            "official_sources_publish_numeric_cover_or_mixing_constants": False,
        },
        "instance_specific_fixed_gauge": fixed_gauge_identity(data["delta_rect"]),
        "explicit_uniform_open_C24_target": explicit_open_target(),
        "uniform_standard_family_bump_minorisation": uniform_bump_minorisation(
            data["euclidean_C_p"],
            data["density_constant"],
            data["dynamic_density_rate"],
        ),
        "numerical_non_effectivity_countermodel": non_effectivity_countermodel(),
        "cover_effectivity_frontier": cover_frontier(),
        "corrected_frontier": {
            "uniform_numeric_conjugacy_factor_m_s": "CERTIFIED_EXACT_1",
            "uniform_numeric_open_C24_target": "CERTIFIED",
            "uniform_finite_bump_hit_time_exists_but_is_not_numerical": True,
            "numeric_whole_family_hit_fraction_at_existential_time": str(HIT_GAP),
            "numeric_H_cover": None,
            "numeric_H_bump": None,
            "numeric_proper_crossing_source_atlas": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "instance_specific_uniform_m_s_equals_1": "CERTIFIED",
            "explicit_uniform_open_C24_target": "CERTIFIED",
            "uniform_existential_time_numeric_hit_fraction": "CERTIFIED",
            "uniform_numeric_H_cover": "NOT_CERTIFIED",
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
        default=HERE / "cm2_gate34_round51_uniform_gauge_bump_frontier_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    if args.summary:
        gauge = result["instance_specific_fixed_gauge"]
        bump = result["uniform_standard_family_bump_minorisation"]
        print(f"UNIFORM_M_S: {gauge['uniform_numeric_m_s']}")
        print(f"UNIFORM_H_BUMP_EXISTS: {bump['one_uniform_finite_integer_H_bump_exists']}")
        print(f"NUMERIC_H_BUMP: {bump['numeric_H_bump']}")
        print(f"HIT_FRACTION: >{bump['actual_whole_family_C24_hit_fraction_strict_lower_at_H_bump']}")
        print("GATE4: NOT_CERTIFIED")
        print("CM2: NO-GO_FOR_CLAIM")
        return 0
    print("GATE4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
