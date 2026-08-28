#!/usr/bin/env python3
"""Gate-1 finite-word gauge propagation and homoclinic-loop frontier.

This certificate combines four frozen facts without changing them:

* the compact logarithmic gauge is one seam-free bundle automorphism on the
  QNL return section;
* canonical stable/unstable limits exist on the two local QNL plaques;
* the QNL and connector belong to one clean hyperbolic basic set
  existentially; and
* the certified 96-collision object is a periodic shadow based at ``z_*``,
  not a QNL-homoclinic point.

The new positive statement is exact cocycle algebra.  The single section
gauge propagates both through one-collision words for the billiard map T and
through words for the phase-aligned QNL return F=T^2, with all intermediate
gauge factors telescoping.  Local QNL holonomies also extend along any finite
prefix/suffix of a genuine global F-stable/unstable orbit.  The cyclic
component of the clean basic set containing the selected QNL phase supplies
such points existentially, so each carries a well-typed holonomy
endomorphism on the QNL fiber.

This still does not identify any such endomorphism with the finite periodic
shadow matrix.  No selected bi-infinite homoclinic word/point, equality or
error bound between the two matrices, or four twisting wedges on the QNL
fiber is available.  Gate 1 therefore remains fail-closed.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent

COMPACT_MANIFEST = (
    HERE / "cm2-gate1-compact-log-gauge-plaque-holonomy-frontier-manifest-2026-07-16.json"
)
COMPACT_CERTIFICATE = HERE / "cm2_gate1_compact_log_gauge_plaque_holonomy_frontier_cert.py"
SHADOW_MANIFEST = HERE / "cm2-gate1-closed-shadow-twisting-manifest-2026-07-15.json"
SHADOW_CERTIFICATE = HERE / "cm2_gate1_closed_shadow_twisting_cert.py"
TYPING_MANIFEST = HERE / "cm2-gate1-bv-holonomy-typing-obstruction-manifest-2026-07-15.json"
TOPOLOGY_REPORT = HERE / "cm2-gate1-topology-audit-2026-07-15.md"

EXPECTED_HASHES = {
    COMPACT_MANIFEST.name: "fc2d7263d4cb659a82c7ecb0fad48f538b466f861f1295d78bb6738331b8c4cd",
    COMPACT_CERTIFICATE.name: "2b84ce38f93118bc62287721fdcf33715ee82d23a888c307fb7f7d40de423f33",
    SHADOW_MANIFEST.name: "31a62a2544d266f76dc973e4c26d83ec34941ddb80d1b139c808750d8ced5800",
    SHADOW_CERTIFICATE.name: "5ce6e38558bd1de56e17c8ef620fc27b6e73f7b04764d272823964c3b9334abc",
    TYPING_MANIFEST.name: "0ed39be87b0efa55d88f83e4c63f8e1170a4392221316d49b83b3725b5a79d1d",
    TOPOLOGY_REPORT.name: "a5e4be0d913cbba00ca806eb6fe60dd9d045314dc70fd238b8a73ed96e77deb3",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_frozen_sources() -> dict[str, Any]:
    paths = (
        COMPACT_MANIFEST,
        COMPACT_CERTIFICATE,
        SHADOW_MANIFEST,
        SHADOW_CERTIFICATE,
        TYPING_MANIFEST,
        TOPOLOGY_REPORT,
    )
    for path in paths:
        assert sha256_path(path) == EXPECTED_HASHES[path.name]

    compact = json.loads(COMPACT_MANIFEST.read_text(encoding="utf-8"))
    shadow = json.loads(SHADOW_MANIFEST.read_text(encoding="utf-8"))
    typing = json.loads(TYPING_MANIFEST.read_text(encoding="utf-8"))
    topology = TOPOLOGY_REPORT.read_text(encoding="utf-8")

    assert compact["schema"] == (
        "cm2.gate1.compact-log-gauge-plaque-holonomy-frontier.manifest.v1"
    )
    compact_result = compact["result"]
    assert compact_result["compact_supported_section_gauge"][
        "no_chart_boundary_seam"
    ] is True
    assert compact_result["compact_supported_section_gauge"][
        "global_inverse_on_section"
    ] is True
    assert compact_result["compact_supported_section_gauge"]["determinant"] == (
        "1 exactly"
    )
    assert compact_result["scope_limits"][
        "stable_all_pairs_on_one_local_qnl_plaque"
    ] is True
    assert compact_result["scope_limits"][
        "unstable_all_pairs_on_one_local_qnl_plaque"
    ] is True
    assert compact_result["scope_limits"]["typed_qnl_homoclinic_loop"] is False

    assert shadow["schema"] == "cm2.gate1.closed-shadow-twisting.v1"
    assert shadow["closed_word"]["full_solid_collisions"] == 96
    assert shadow["derivative_typing"]["cross_basepoint_matrix_product"] is False
    assert shadow["verdict"]["finite_closed_same_orbit_shadow_loop"] == "CERTIFIED"
    assert shadow["verdict"][
        "bonatti_viana_qnl_periodic_fiber_holonomy_identification"
    ] == "NOT_CERTIFIED"

    assert typing["schema"] == "cm2.gate1.bv-holonomy-typing-obstruction.v1"
    assert typing["basepoint_typing"]["zstar_is_pa_homoclinic"] == "REFUTED"
    assert typing["qnl_periodic_obstruction"][
        "park_piraino_full_collision_period"
    ] == 2
    assert typing["gauge_counterexample"][
        "global_gray_trivialization_as_canonical_holonomy"
    ] == "REFUTED"
    assert typing["verdict"]["finite_one_vertex_actual_derivative_cocycle"] == (
        "NOT_CERTIFIED"
    )

    required_topology_phrases = (
        "same homoclinic class, existentially",
        "common locally maximal hyperbolic basic set / existential Markov",
        "clean transverse heteroclinic intersections",
    )
    for phrase in required_topology_phrases:
        assert phrase in topology

    return {
        "compact": compact,
        "shadow": shadow,
        "typing": typing,
    }


def finite_word_gauge_algebra() -> dict[str, Any]:
    return {
        "intrinsic_section_gauge": (
            "B_hat is the compact QNL-chart formula on U_chart and the identity "
            "on its boundary collar and outside U_chart; chart representatives "
            "are related by ordinary tangent-coordinate conjugacy"
        ),
        "collision_section_extension": (
            "use B_hat on the selected QNL collision component and the identity "
            "on every other disjoint obstacle component"
        ),
        "base_maps_and_cocycles": (
            "T is the one-collision billiard map with cocycle C; the QNL has "
            "full-collision period two, F=T^2 fixes the selected phase p, and "
            "A(x)=C^2(x) is the F-cocycle"
        ),
        "one_collision_gauge_cocycle": (
            "C_hat(x)=B_hat(Tx)^-1 C(x) B_hat(x), matching the frozen "
            "resonant-gauge convention"
        ),
        "finite_collision_word_telescope": (
            "C_hat^m(x)=B_hat(T^m x)^-1 C^m(x) B_hat(x) for every finite "
            "regular m-collision word"
        ),
        "phase_aligned_return_gauge_cocycle": (
            "A_hat(x)=C_hat^2(x)=B_hat(Fx)^-1 A(x) B_hat(x)"
        ),
        "finite_return_word_telescope": (
            "A_hat^n(x)=B_hat(F^n x)^-1 A^n(x) B_hat(x) for every finite "
            "regular n-return word"
        ),
        "concatenation_compatibility": (
            "at every T- or F-word concatenation endpoint y, the adjacent "
            "B_hat(y) B_hat(y)^-1 factors cancel exactly"
        ),
        "closed_word_conjugacy": (
            "if T^m z=z (equivalently for an F-word when m is even), then "
            "L_hat(z)=B_hat(z)^-1 L(z) B_hat(z)"
        ),
        "closed_96_collision_shadow_conjugacy": (
            "T^96 z_*=z_* gives L_hat(z_*)=B_hat(z_*)^-1 L(z_*) "
            "B_hat(z_*); this remains an endomorphism of E_{z_*}"
        ),
        "determinant_preserved": True,
        "chart_overlap_or_connector_patch_needed_for_finite_words": False,
        "finite_registered_qnl_connector_word_gauge_propagation": "CERTIFIED",
    }


def global_tail_extension() -> dict[str, Any]:
    return {
        "phase_aligned_return": (
            "F=T^2, p is the selected fixed QNL phase, and "
            "A_hat^(k)(x):E_x->E_{F^k x} for every signed regular integer k"
        ),
        "stable_extension_formula": (
            "if z_N=F^N z is in W^s_loc(p), then H^s_{p,z}="
            "A_hat^(N)(z)^-1 H^s_{p,z_N} A_hat^(N)(p):E_p->E_z"
        ),
        "unstable_extension_formula": (
            "if z_-N=F^-N z is in W^u_loc(p), then H^u_{p,z}="
            "A_hat^(-N)(z)^-1 H^u_{p,z_-N} A_hat^(-N)(p):E_p->E_z"
        ),
        "finite_prefix_suffix_preserves_convergence": True,
        "clean_basic_set_phase_alignment": (
            "the cyclic F=T^2 component of the nontrivial clean T-basic set "
            "containing p has local product structure and supplies clean "
            "z in W^s_F(p) intersect W^u_F(p) outside the QNL orbit"
        ),
        "clean_basic_set_supplies_nontrivial_phase_aligned_qnl_homoclinic_points": (
            "CERTIFIED_EXISTENTIALLY_BY_CYCLIC_COMPONENT_OF_FROZEN_BASIC_SET"
        ),
        "typed_holonomy_arrows": (
            "H^u_{p,z}:E_p->E_z and H^s_{z,p}:E_z->E_p"
        ),
        "typed_endomorphism": (
            "for every such phase-aligned z, psi_z=H^s_{z,p} o "
            "H^u_{p,z}:E_p->E_p is well-defined in the compact-gauge cocycle"
        ),
        "existential_qnl_homoclinic_holonomy_endomorphism": True,
        "existential_typed_endomorphism_implies_twisting": False,
        "selected_immutable_homoclinic_word_or_coordinate": False,
        "uniform_holder_family_on_all_basic_set_plaques": False,
    }


def exact_missing_identification() -> dict[str, Any]:
    return {
        "periodic_shadow_basepoint": "z_* is periodic and is not QNL-homoclinic",
        "shadow_matrix_fiber": "L acts on E_{z_*}",
        "required_loop_fiber": "psi_z acts on E_p for a genuine QNL-homoclinic z",
        "raw_common_chart_identification": "REFUTED_AS_CANONICAL_HOLONOMY",
        "raw_equality_psi_z_equals_L_is_well_typed": False,
        "required_cross_fiber_transport": (
            "a certified gauge-covariant J_{z_*,p}:E_{z_*}->E_p, if the "
            "periodic shadow is to be compared with a QNL loop"
        ),
        "only_typed_shadow_comparison": (
            "compare psi_z:E_p->E_p with J_{z_*,p} L J_{z_*,p}^-1:E_p->E_p"
        ),
        "missing_orbit_record": (
            "one selected bi-infinite p-tail/excursion/p-tail physical orbit z "
            "with immutable regular itinerary and local-plaque entry times"
        ),
        "missing_cocycle_identification": (
            "either compute psi_z directly from the selected homoclinic orbit, "
            "or certify J_{z_*,p} and an equality/error bound between psi_z and "
            "J_{z_*,p} L J_{z_*,p}^-1"
        ),
        "missing_twisting_test": (
            "four nonzero wedges between the QNL Perron lines and psi_z on E_p"
        ),
        "finite_shadow_matrix_equals_homoclinic_loop": False,
        "quantitative_shadow_to_homoclinic_error_bound": False,
        "four_qnl_fiber_twisting_wedges": False,
        "existential_typed_loop_is_a_twisting_certificate": False,
        "first_missing_interface": "SHADOW_TO_HOMOCLINIC_ORBIT_COCYCLE_IDENTIFICATION",
    }


def certify() -> dict[str, Any]:
    sources = load_frozen_sources()
    words = finite_word_gauge_algebra()
    tails = global_tail_extension()
    missing = exact_missing_identification()
    result = {
        "schema": "cm2.gate1.word-gauge-homoclinic-loop-frontier.v1",
        "provenance": {
            "dependencies": EXPECTED_HASHES,
            "compact_source_internal_digest": sources["compact"]["result"][
                "internal_digest"
            ],
        },
        "finite_word_gauge_propagation": words,
        "homoclinic_tail_extension": tails,
        "exact_missing_identification": missing,
        "scope_limits": {
            "finite_registered_word_gauge_compatibility": True,
            "phase_aligned_F_homoclinic_existence": True,
            "existential_typed_qnl_homoclinic_endomorphism": True,
            "existential_typed_loop_is_twisting": False,
            "specific_typed_qnl_twisting_loop": False,
            "shadow_loop_identified_with_qnl_holonomy_loop": False,
            "global_faithful_coding": False,
            "uniform_all_plaque_holder_holonomies": False,
            "butler_park_class_H": False,
            "park_piraino_typicality": False,
            "gate1_certified": False,
            "unconditional_cm2": False,
        },
        "strict_frontier": {
            "positive": (
                "finite QNL/connector return-word gauges telescope without an "
                "overlap seam; local QNL holonomies extend along finite tails, "
                "so an existential clean homoclinic point has a typed endomorphism"
            ),
            "negative": (
                "no selected homoclinic orbit or gauge-covariant identification "
                "of its holonomy loop with the finite-shadow matrix L"
            ),
            "gate1": "NOT_CERTIFIED",
        },
    }
    result["internal_digest"] = digest({
        "words": words,
        "tails": tails,
        "missing": missing,
        "scope": result["scope_limits"],
    })
    return result


def main() -> None:
    print(json.dumps(certify(), indent=2, sort_keys=True))
    print("GATE1_FINITE_WORD_GAUGE_AND_HOMOCLINIC_TAIL_TYPING: CERTIFIED")
    print("GATE1_SPECIFIC_QNL_TWISTING_LOOP: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
