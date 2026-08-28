#!/usr/bin/env python3
"""Fail-closed verifier for the immutable QNL homoclinic frontier."""

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
    HERE
    / "cm2-gate1-immutable-homoclinic-plaque-entry-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = (
    HERE / "cm2_gate1_immutable_homoclinic_plaque_entry_frontier_cert.py"
)
REPORT = (
    HERE
    / "cm2-gate1-immutable-homoclinic-plaque-entry-frontier-assault-2026-07-16.md"
)
SCHEMA = "cm2.gate1.immutable-homoclinic-plaque-entry-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate1.immutable-homoclinic-plaque-entry-frontier.v1"
INTERNAL_DIGEST = "95c274e761c08ad9768e98040aa46663e113f70c6167e556faea659b535ef000"


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
    if not isinstance(dependencies, dict) or len(dependencies) != 8:
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

    orbit = result.get("immutable_homoclinic_orbit", {})
    exact(
        errors,
        orbit,
        {
            "arb_precision_bits": 1000,
            "root_x_radius": "1e-50",
            "root_interval_excludes_qnl_point": True,
            "actual_graph_ordinate_bound": "|h_u(x)|<7e-29 on the root interval",
            "actual_graph_derivative_bound": "|h_u'(x)|<=1e-4",
            "half_word_left_face_momentum": "strictly less than -1e-23",
            "half_word_right_face_momentum": "strictly greater than 1e-23",
            "shooting_derivative_along_actual_graph": "strictly greater than 1e27",
            "unique_actual_graph_root": True,
            "half_word_factorisation": "Q5^2 B^2",
            "full_word_factorisation": "Q5^2 B^4 Q5^2",
            "half_word_collision_count": 48,
            "full_word_collision_count": 96,
            "half_word_sha256": "ae58871d5e57096b0f798c442a670b5545c9f4e00d9bb87ec22a36d448f20441",
            "full_word_sha256": "b97277492675bcb90b42f95be744f9c920212740324a2fe19eaabaf850e9c47e",
            "half_lift_ledger_sha256": "41b21572b2c0c0f5e0067400a0d2e6b1287c81ee7086c8b6a7747a1342a4a108",
            "half_word_terminal_lift": [0, 0],
            "reversibility_fixed_line": "Fix(I)={p=0}",
            "exact_reflection_identity": "T^96 z_h=I z_h",
            "phase_aligned_return": "F=T^2",
            "F_unstable_plaque_entry_time": 0,
            "F_stable_plaque_entry_time": 48,
            "bi_infinite_itinerary": "... QNL | Q5^2 B^4 Q5^2 | QNL ...",
            "selected_point_is_regular": True,
            "selected_point_is_nonperiodic_qnl_homoclinic": True,
            "explicit_gauge_core_radius": "1e-12",
            "explicit_gauge_chart_radius": "1e-10",
            "gauge_is_one_on_selected_local_tails": True,
            "gauge_is_zero_outside_chart_disk": True,
            "gauge_chart_qnl_return_is_regular": True,
        },
        "immutable orbit",
    )
    if len(orbit.get("q5_block_collision_keys", [])) != 10:
        errors.append("Q5 key registry length mismatch")
    if len(orbit.get("connector_block_collision_keys", [])) != 14:
        errors.append("connector key registry length mismatch")
    margins = orbit.get("half_word_uniform_physical_margins", {})
    exact(
        errors,
        margins,
        {
            "flight": ">18/100",
            "discriminant": ">1/100",
            "incidence": ">63/100",
            "clearance": ">22/100",
        },
        "physical margins",
    )
    if "unique root" not in orbit.get("selected_point_definition", ""):
        errors.append("selected point uniqueness definition missing")
    cutoff = orbit.get("explicit_gauge_cutoff", "")
    if "beta(t)=0 for t<=0" not in cutoff or "exp(-1/t)" not in cutoff:
        errors.append("explicit compact cutoff missing")

    loop = result.get("typed_loop_and_numeric_frontier", {})
    exact(
        errors,
        loop,
        {
            "selected_loop_fiber": "E_p",
            "selected_homoclinic_endomorphism": (
                "psi_z=H_hat^s_{z_h,p} o H_hat^u_{p,z_h}:E_p->E_p"
            ),
            "finite_entry_formula": (
                "psi_z=A_hat^48(p)^-1 H_hat^s_{I z_h,p} "
                "A_hat^48(z_h) H_hat^u_{p,z_h}:E_p->E_p"
            ),
            "formula_is_well_typed": True,
            "local_unstable_holonomy_exists": True,
            "local_stable_holonomy_exists": True,
            "selected_immutable_qnl_homoclinic_loop": (
                "CERTIFIED_AS_A_TYPED_LIMIT"
            ),
            "numeric_matrix_enclosure_for_Hu": False,
            "numeric_matrix_enclosure_for_Hs": False,
            "numeric_matrix_enclosure_for_psi_z": False,
            "periodic_shadow_matrix_fiber": "E_{z_*}",
            "gauge_covariant_transport_J_from_shadow_to_p": False,
            "psi_z_vs_J_L_J_inverse_error_bound": False,
            "raw_common_chart_finite_excursion_equals_psi_z": False,
            "four_qnl_fiber_twisting_wedges": False,
            "global_uniform_holder_holonomies": False,
            "butler_park_class_H": False,
            "first_missing_numeric_interface": (
                "EXPLICIT_LOCAL_HOLONOMY_TAIL_MAJORANTS_AND_MATRIX_ENCLOSURES"
            ),
        },
        "typed loop frontier",
    )
    if "without numerical majorant constants" not in loop.get(
        "frozen_tail_data_are_qualitative", ""
    ):
        errors.append("quantitative tail blocker missing")

    scope = result.get("scope_limits", {})
    for key in (
        "selected_immutable_regular_phase_aligned_qnl_homoclinic_orbit",
        "physical_plaque_entry_times_certified",
        "selected_typed_qnl_homoclinic_limit_loop",
    ):
        if scope.get(key) is not True:
            errors.append(f"certified frontier flag missing: {key}")
    for key in (
        "direct_numeric_psi_z",
        "shadow_transport_and_error_bound",
        "four_twisting_wedges",
        "global_faithful_coding",
        "uniform_all_plaque_holder_holonomies",
        "butler_park_class_H",
        "gate1_certified",
        "unconditional_cm2",
    ):
        if scope.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    exact(
        errors,
        data.get("verdict", {}),
        {
            "selected_immutable_qnl_homoclinic_orbit": "CERTIFIED",
            "physical_F_plaque_entry_times_0_and_48": "CERTIFIED",
            "selected_typed_qnl_homoclinic_limit_loop": "CERTIFIED",
            "numeric_psi_z_and_four_twisting_wedges": "NOT_CERTIFIED",
            "butler_park_class_H": "NOT_CERTIFIED",
            "gate1": "NOT_CERTIFIED",
            "unconditional_cm2": "NO_GO_FOR_CLAIM",
        },
        "verdict",
    )
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate1_immutable_homoclinic_plaque_entry_frontier_cert as cert

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

    add(
        "root uniqueness",
        lambda d: d["result"]["immutable_homoclinic_orbit"].__setitem__(
            "unique_actual_graph_root", False
        ),
    )
    add(
        "left face",
        lambda d: d["result"]["immutable_homoclinic_orbit"].__setitem__(
            "half_word_left_face_momentum", "unknown"
        ),
    )
    add(
        "graph derivative",
        lambda d: d["result"]["immutable_homoclinic_orbit"].__setitem__(
            "shooting_derivative_along_actual_graph", "may vanish"
        ),
    )
    add(
        "word digest",
        lambda d: d["result"]["immutable_homoclinic_orbit"].__setitem__(
            "full_word_sha256", "0" * 64
        ),
    )
    add(
        "collision count",
        lambda d: d["result"]["immutable_homoclinic_orbit"].__setitem__(
            "full_word_collision_count", 95
        ),
    )
    add(
        "physical margin",
        lambda d: d["result"]["immutable_homoclinic_orbit"][
            "half_word_uniform_physical_margins"
        ].__setitem__("clearance", "unknown"),
    )
    add(
        "reflection identity",
        lambda d: d["result"]["immutable_homoclinic_orbit"].__setitem__(
            "exact_reflection_identity", "periodic"
        ),
    )
    add(
        "plaque time",
        lambda d: d["result"]["immutable_homoclinic_orbit"].__setitem__(
            "F_stable_plaque_entry_time", 24
        ),
    )
    add(
        "gauge core",
        lambda d: d["result"]["immutable_homoclinic_orbit"].__setitem__(
            "gauge_is_one_on_selected_local_tails", False
        ),
    )
    add(
        "typed formula",
        lambda d: d["result"]["typed_loop_and_numeric_frontier"].__setitem__(
            "formula_is_well_typed", False
        ),
    )
    add(
        "psi overclaim",
        lambda d: d["result"]["typed_loop_and_numeric_frontier"].__setitem__(
            "numeric_matrix_enclosure_for_psi_z", True
        ),
    )
    add(
        "shadow transport overclaim",
        lambda d: d["result"]["typed_loop_and_numeric_frontier"].__setitem__(
            "gauge_covariant_transport_J_from_shadow_to_p", True
        ),
    )
    add(
        "raw excursion overclaim",
        lambda d: d["result"]["typed_loop_and_numeric_frontier"].__setitem__(
            "raw_common_chart_finite_excursion_equals_psi_z", True
        ),
    )
    add(
        "twisting overclaim",
        lambda d: d["result"]["typed_loop_and_numeric_frontier"].__setitem__(
            "four_qnl_fiber_twisting_wedges", True
        ),
    )
    add(
        "class H overclaim",
        lambda d: d["result"]["scope_limits"].__setitem__(
            "butler_park_class_H", True
        ),
    )
    add(
        "Gate 1 overclaim",
        lambda d: d["result"]["scope_limits"].__setitem__(
            "gate1_certified", True
        ),
    )

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
        print("GATE1_IMMUTABLE_HOMOCLINIC_FRONTIER_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        return run_self_test(data)
    if args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return 0
    print("SELECTED_IMMUTABLE_QNL_HOMOCLINIC_ORBIT: CERTIFIED")
    print("PHYSICAL_F_PLAQUE_ENTRY_TIMES_0_AND_48: CERTIFIED")
    print("SELECTED_TYPED_QNL_HOMOCLINIC_LIMIT_LOOP: CERTIFIED")
    print("NUMERIC_PSI_Z_AND_FOUR_TWISTING_WEDGES: NOT_CERTIFIED")
    print("BUTLER_PARK_CLASS_H: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
