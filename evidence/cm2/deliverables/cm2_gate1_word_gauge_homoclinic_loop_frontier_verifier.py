#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-1 word-gauge/loop frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate1-word-gauge-homoclinic-loop-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate1_word_gauge_homoclinic_loop_frontier_cert.py"
REPORT = HERE / "cm2-gate1-word-gauge-homoclinic-loop-frontier-assault-2026-07-16.md"
SCHEMA = "cm2.gate1.word-gauge-homoclinic-loop-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate1.word-gauge-homoclinic-loop-frontier.v1"
INTERNAL_DIGEST = "06486980569fcf6cd5a2707f72d64c6d277718751dc02aee8b22e17599fa6d83"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact(
    errors: list[str], section: dict[str, Any], expected: dict[str, Any], label: str
) -> None:
    for key, value in expected.items():
        if section.get(key) != value:
            errors.append(f"{label} mismatch: {key}")


def check_structure(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("manifest schema mismatch")
    if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash mismatch")
    if data.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash mismatch")
    if data.get("report_sha256") != sha256_path(REPORT):
        errors.append("report hash mismatch")

    dependencies = data.get("dependencies")
    if not isinstance(dependencies, dict) or len(dependencies) != 6:
        errors.append("dependency ledger mismatch")
    else:
        for name, expected_hash in dependencies.items():
            path = HERE / name
            if not path.is_file():
                errors.append(f"dependency missing: {name}")
            elif sha256_path(path) != expected_hash:
                errors.append(f"dependency hash mismatch: {name}")

    result = data.get("result")
    if not isinstance(result, dict):
        return errors + ["result missing"]
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")
    if result.get("internal_digest") != INTERNAL_DIGEST:
        errors.append("internal digest mismatch")

    words = result.get("finite_word_gauge_propagation", {})
    exact(errors, words, {
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
    }, "finite-word gauge")

    tails = result.get("homoclinic_tail_extension", {})
    exact(errors, tails, {
        "phase_aligned_return": (
            "F=T^2, p is the selected fixed QNL phase, and "
            "A_hat^(k)(x):E_x->E_{F^k x} for every signed regular integer k"
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
        "existential_qnl_homoclinic_holonomy_endomorphism": True,
        "existential_typed_endomorphism_implies_twisting": False,
        "selected_immutable_homoclinic_word_or_coordinate": False,
        "uniform_holder_family_on_all_basic_set_plaques": False,
    }, "tail extension")
    if "A_hat^(N)(z)^-1" not in tails.get("stable_extension_formula", ""):
        errors.append("stable extension formula missing")
    if "A_hat^(-N)(z)^-1" not in tails.get("unstable_extension_formula", ""):
        errors.append("unstable extension formula missing")
    typed = tails.get("typed_endomorphism", "")
    if "psi_z=H^s_{z,p} o H^u_{p,z}:E_p->E_p" not in typed:
        errors.append("typed QNL-fiber endomorphism missing")

    missing = result.get("exact_missing_identification", {})
    exact(errors, missing, {
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
        "finite_shadow_matrix_equals_homoclinic_loop": False,
        "quantitative_shadow_to_homoclinic_error_bound": False,
        "four_qnl_fiber_twisting_wedges": False,
        "existential_typed_loop_is_a_twisting_certificate": False,
        "first_missing_interface": "SHADOW_TO_HOMOCLINIC_ORBIT_COCYCLE_IDENTIFICATION",
    }, "missing identification")

    scope = result.get("scope_limits", {})
    for key in (
        "finite_registered_word_gauge_compatibility",
        "phase_aligned_F_homoclinic_existence",
        "existential_typed_qnl_homoclinic_endomorphism",
    ):
        if scope.get(key) is not True:
            errors.append(f"certified frontier flag missing: {key}")
    for key in (
        "specific_typed_qnl_twisting_loop",
        "existential_typed_loop_is_twisting",
        "shadow_loop_identified_with_qnl_holonomy_loop",
        "global_faithful_coding",
        "uniform_all_plaque_holder_holonomies",
        "butler_park_class_H",
        "park_piraino_typicality",
        "gate1_certified",
        "unconditional_cm2",
    ):
        if scope.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    exact(errors, data.get("verdict", {}), {
        "finite_registered_word_gauge_compatibility": "CERTIFIED",
        "existential_qnl_homoclinic_holonomy_endomorphism": "CERTIFIED",
        "specific_qnl_twisting_loop": "NOT_CERTIFIED",
        "butler_park_class_H": "NOT_CERTIFIED",
        "gate1": "NOT_CERTIFIED",
        "unconditional_cm2": "NO_GO_FOR_CLAIM",
    }, "verdict")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate1_word_gauge_homoclinic_loop_frontier_cert as cert

        actual = cert.certify()
    except Exception as exc:  # pragma: no cover
        return [f"certificate replay failed: {exc}"]
    return [] if data.get("result") == actual else ["certificate replay mismatch"]


def run_self_test(data: dict[str, Any]) -> int:
    mutations: list[tuple[str, dict[str, Any]]] = []

    def add(label: str, mutate) -> None:
        tampered = copy.deepcopy(data)
        mutate(tampered)
        mutations.append((label, tampered))

    add("collision map typing", lambda d: d["result"]["finite_word_gauge_propagation"].__setitem__("base_maps_and_cocycles", "unknown"))
    add("gauge inverse convention", lambda d: d["result"]["finite_word_gauge_propagation"].__setitem__("one_collision_gauge_cocycle", "C_hat=B(Tx) C B(x)^-1"))
    add("finite collision telescope", lambda d: d["result"]["finite_word_gauge_propagation"].__setitem__("finite_collision_word_telescope", "unknown"))
    add("finite return telescope", lambda d: d["result"]["finite_word_gauge_propagation"].__setitem__("finite_return_word_telescope", "unknown"))
    add("concatenation", lambda d: d["result"]["finite_word_gauge_propagation"].__setitem__("concatenation_compatibility", "unknown"))
    add("closed conjugacy", lambda d: d["result"]["finite_word_gauge_propagation"].__setitem__("closed_word_conjugacy", "equality"))
    add("stable tail", lambda d: d["result"]["homoclinic_tail_extension"].__setitem__("stable_extension_formula", "missing"))
    add("existential typing", lambda d: d["result"]["homoclinic_tail_extension"].__setitem__("existential_qnl_homoclinic_holonomy_endomorphism", False))
    add("phase alignment", lambda d: d["result"]["homoclinic_tail_extension"].__setitem__("clean_basic_set_phase_alignment", "unknown"))
    add("existential twisting overclaim", lambda d: d["result"]["homoclinic_tail_extension"].__setitem__("existential_typed_endomorphism_implies_twisting", True))
    add("selected orbit overclaim", lambda d: d["result"]["homoclinic_tail_extension"].__setitem__("selected_immutable_homoclinic_word_or_coordinate", True))
    add("shadow equality overclaim", lambda d: d["result"]["exact_missing_identification"].__setitem__("finite_shadow_matrix_equals_homoclinic_loop", True))
    add("raw equality typing overclaim", lambda d: d["result"]["exact_missing_identification"].__setitem__("raw_equality_psi_z_equals_L_is_well_typed", True))
    add("transport deletion", lambda d: d["result"]["exact_missing_identification"].__setitem__("required_cross_fiber_transport", "missing"))
    add("error bound overclaim", lambda d: d["result"]["exact_missing_identification"].__setitem__("quantitative_shadow_to_homoclinic_error_bound", True))
    add("twisting overclaim", lambda d: d["result"]["exact_missing_identification"].__setitem__("four_qnl_fiber_twisting_wedges", True))
    add("class H overclaim", lambda d: d["result"]["scope_limits"].__setitem__("butler_park_class_H", True))
    add("Gate 1 overclaim", lambda d: d["result"]["scope_limits"].__setitem__("gate1_certified", True))

    rejected = 0
    for label, tampered in mutations:
        if check_structure(tampered):
            rejected += 1
        else:
            print(f"SELF_TEST: FAIL ({label} mutation accepted)")
            return 1
    print(f"MUTATION_SELF_TEST: PASS ({rejected}/{len(mutations)} mutations rejected)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"MANIFEST_READ_ERROR: {exc}", file=sys.stderr)
        return 1
    errors = check_structure(data)
    if args.replay and not errors:
        errors.extend(check_replay(data))
    if errors:
        print("GATE1_WORD_GAUGE_HOMOCLINIC_LOOP_FRONTIER_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        return run_self_test(data)
    if args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return 0
    print("GATE1_FINITE_WORD_GAUGE_AND_HOMOCLINIC_TAIL_TYPING: CERTIFIED")
    print("GATE1_SPECIFIC_QNL_TWISTING_LOOP: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
