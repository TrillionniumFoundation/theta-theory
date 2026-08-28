#!/usr/bin/env python3
"""Bind the selected QNL homoclinic occurrence to one positive word component.

The frozen Gate-2/5 maximal-word registry left this incidence deliberately
open.  Here a connected rational corridor containing both the original
positive seed and the selected QNL homoclinic point is replayed against the
complete retained first-hit candidate list, uniformly for |s|<=1/400.

This is a collision-section incidence theorem.  It does not construct a
stable-saturated carrier, a quotient density, reverse weights, PPE, or any
of the remaining full-key operator fields.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert


HERE = Path(__file__).resolve().parent
Q = Fraction
ctx.prec = 384

MAXIMAL_MANIFEST = (
    HERE / "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json"
)
IMMUTABLE_MANIFEST = (
    HERE / "cm2-gate1-immutable-homoclinic-plaque-entry-frontier-manifest-2026-07-16.json"
)

EXPECTED_HASHES = {
    MAXIMAL_MANIFEST.name: (
        "bb09f99519813ec49172f0bbbcc9015c1e0fcb2de07df7af734b81d2996a3f40"
    ),
    IMMUTABLE_MANIFEST.name: (
        "e583a7c0f43f291f92ffb7dc15a4888bda6702340f3209bfd7ec224101df841c"
    ),
    Path(core_cert.__file__).name: (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
}

PHYSICAL_KEY = ["G:E", "W[0,0]", [], 1]
CORRIDOR_T0 = Q(69, 100)
# This rational lies strictly below the E/N normal-chart seam 1/sqrt(2),
# while the selected homoclinic normal coordinate lies strictly below it.
CORRIDOR_T1 = Q(70710678118654, 10**14)
CORRIDOR_P0 = -Q(1, 50)
CORRIDOR_P1 = Q(1, 50)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_dependencies() -> tuple[dict[str, Any], dict[str, Any]]:
    for name, expected in EXPECTED_HASHES.items():
        if sha256_path(HERE / name) != expected:
            raise RuntimeError(f"frozen dependency hash changed: {name}")
    maximal = json.loads(MAXIMAL_MANIFEST.read_text(encoding="utf-8"))
    immutable = json.loads(IMMUTABLE_MANIFEST.read_text(encoding="utf-8"))
    assert maximal["schema"] == (
        "cm2.gate25.maximal-word-characteristic-frontier.manifest.v1"
    )
    assert immutable["schema"] == (
        "cm2.gate1.immutable-homoclinic-plaque-entry-frontier.manifest.v1"
    )
    assert maximal["verdict"]["positive_seeded_maximal_word_components"] == (
        "CERTIFIED_IMPLICIT"
    )
    assert immutable["result"]["scope_limits"][
        "selected_immutable_regular_phase_aligned_qnl_homoclinic_orbit"
    ] is True
    return maximal, immutable


def selected_point_physical_box(immutable: dict[str, Any]) -> dict[str, Any]:
    orbit = immutable["result"]["immutable_homoclinic_orbit"]
    assert orbit["q5_block_collision_keys"][0] == ["W", 0, 0]
    assert orbit["root_x_radius"] == "1e-50"
    assert orbit["actual_graph_ordinate_bound"] == (
        "|h_u(x)|<7e-29 on the root interval"
    )

    x = arb(orbit["root_x_center"], orbit["root_x_radius"])
    y = arb(0, "7e-29")
    radius_gray = arb(9) / 25
    sqrt_two = arb(2).sqrt()
    beta = (arb(859) - 550 * sqrt_two) / 100
    gamma = arb(625) * (25 - 4 * sqrt_two) / 324
    slope = (gamma / beta).sqrt()

    arclength = x + y
    theta = arb.pi() / 4 + arclength / radius_gray
    source_chart_t = theta.sin()
    momentum = slope * (x - y)

    assert bool(source_chart_t > core_cert.arbq(CORRIDOR_T0))
    assert bool(source_chart_t < core_cert.arbq(CORRIDOR_T1))
    assert 2 * CORRIDOR_T1 * CORRIDOR_T1 < 1
    assert bool(core_cert.arbq(CORRIDOR_T1) < 1 / arb(2).sqrt())
    assert bool(momentum > core_cert.arbq(CORRIDOR_P0))
    assert bool(momentum < core_cert.arbq(CORRIDOR_P1))
    assert bool(abs(arclength) < arb("1e-13"))
    assert bool(abs(momentum) < arb("1e-12"))

    return {
        "physical_source_obstacle": "G[0,0]",
        "physical_parameter": "s=0",
        "QNL_graph_coordinates": {
            "x_interval": str(x),
            "graph_ordinate_enclosure": str(y),
        },
        "coordinate_formula": {
            "boundary_arclength": "r=x+h_u(x)",
            "normal_angle": "theta=pi/4+(x+h_u(x))/(9/25)",
            "source_chart_coordinate": "t=sin(theta)",
            "collision_momentum": "p=kappa*(x-h_u(x))",
        },
        "strict_rational_enclosure": {
            "t": [str(CORRIDOR_T0), str(CORRIDOR_T1)],
            "p=sin(phi)": [str(CORRIDOR_P0), str(CORRIDOR_P1)],
            "abs_boundary_arclength_strict_upper": "1e-13",
            "abs_collision_momentum_strict_upper": "1e-12",
        },
        "first_Q5_collision_target": "W[0,0]",
    }


def corridor_certificate() -> dict[str, Any]:
    corridor = core_cert.Core(
        "G:E",
        CORRIDOR_T0,
        CORRIDOR_T1,
        CORRIDOR_P0,
        CORRIDOR_P1,
        "W[0,0]",
        (),
        "selected_QNL_incidence_corridor",
    )
    row = core_cert.certify_core(corridor)
    assert row["key"] == PHYSICAL_KEY
    assert row["strict_first_hit"] is True
    assert row["transparent_wall_record"] == []
    assert row["suffix_chart"]["target_lift"] == "W[0,0]"
    assert row["suffix_chart"]["open_semicircle_direction"] == [-1, -1]
    return {
        "parameter_window": ["-1/400", "1/400"],
        "connected_closed_corridor": {
            "source_chart": "G:E",
            "t": [str(CORRIDOR_T0), str(CORRIDOR_T1)],
            "p=sin(phi)": [str(CORRIDOR_P0), str(CORRIDOR_P1)],
        },
        "physical_key": PHYSICAL_KEY,
        "complete_retained_first_hit_replay": row,
        "corridor_uniformly_inside_exact_word_chart_homogeneity_predicate": True,
    }


def component_incidence(
    maximal: dict[str, Any], point: dict[str, Any], corridor: dict[str, Any]
) -> dict[str, Any]:
    registry = maximal["result"]["seeded_implicit_maximal_component_registry"]
    rows = [
        row for row in registry["rows"]
        if row["definition"]["physical_key"] == PHYSICAL_KEY
    ]
    assert len(rows) == 1
    row = rows[0]
    assert row["maximal_component_id"] == canonical_digest(row["definition"])
    seed = row["definition"]["seed_open_rectangle"]
    assert seed == {
        "t": ["69/100", "7/10"],
        "p=sin(phi)": ["-1/50", "1/50"],
    }
    assert CORRIDOR_T0 == Q(seed["t"][0])
    assert CORRIDOR_T1 > Q(seed["t"][1])
    assert [str(CORRIDOR_P0), str(CORRIDOR_P1)] == seed["p=sin(phi)"]
    assert corridor[
        "corridor_uniformly_inside_exact_word_chart_homogeneity_predicate"
    ] is True
    assert point["physical_parameter"] == "s=0"

    return {
        "physical_key": PHYSICAL_KEY,
        "maximal_component_id": row["maximal_component_id"],
        "original_positive_seed_is_contained_in_corridor": True,
        "selected_homoclinic_point_is_strictly_inside_corridor_at_s0": True,
        "corridor_is_connected": True,
        "corridor_stays_strictly_below_E_N_source_chart_seam": True,
        "corridor_stays_inside_defining_component_predicate": True,
        "selected_occurrence_membership_in_one_of_24_maximal_word_components_certified": True,
        "incidence_scope": (
            "the initial G[0,0] collision occurrence of the selected QNL "
            "homoclinic orbit at s=0"
        ),
    }


def build_result() -> dict[str, Any]:
    maximal, immutable = audit_dependencies()
    point = selected_point_physical_box(immutable)
    corridor = corridor_certificate()
    incidence = component_incidence(maximal, point, corridor)
    result: dict[str, Any] = {
        "schema": "cm2.gate25.selected-homoclinic-component-incidence-frontier.v1",
        "provenance": {
            "frozen_dependency_sha256": EXPECTED_HASHES,
            "maximal_registry_rows_sha256": maximal["result"][
                "seeded_implicit_maximal_component_registry"
            ]["rows_sha256"],
            "selected_homoclinic_full_word_sha256": immutable["result"][
                "immutable_homoclinic_orbit"
            ]["full_word_sha256"],
        },
        "selected_point_physical_enclosure": point,
        "connected_physical_corridor_replay": corridor,
        "selected_occurrence_component_incidence": incidence,
        "strict_nonpromotion": {
            "collision_occurrence_incidence_is_a_stable_quotient_branch_label": False,
            "stable_saturated_product_base": False,
            "stable_projection_pi_s": False,
            "quotient_density_rho": False,
            "physical_reverse_weight_p_a": False,
            "same_carrier_endpoint_maps_X_a_Y_a": False,
            "PPE": False,
            "full_key_characteristic_boundary_Z": False,
            "complete_18_field_operator_block_count": 0,
            "Gate2": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> int:
    result = build_result()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("SELECTED_QNL_HOMOCLINIC_PHYSICAL_COMPONENT_INCIDENCE: CERTIFIED")
    print("GATE2_STABLE_QUOTIENT_PPE: NOT_CERTIFIED")
    print("GATE5_COMPLETE_OPERATOR_BLOCKS: NOT_CERTIFIED")
    print("GATE2: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
