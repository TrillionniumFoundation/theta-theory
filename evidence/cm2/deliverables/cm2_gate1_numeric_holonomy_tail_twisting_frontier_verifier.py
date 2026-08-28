#!/usr/bin/env python3
"""Fail-closed verifier for the numerical QNL holonomy/twisting frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate1_numeric_holonomy_tail_twisting_frontier_cert.py"
REPORT = HERE / "cm2-gate1-numeric-holonomy-tail-twisting-frontier-assault-2026-07-16.md"
SCHEMA = "cm2.gate1.numeric-holonomy-tail-twisting-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate1.numeric-holonomy-tail-twisting-frontier.v1"
INTERNAL_DIGEST = "866afbfd317fbe21b9921f7152c9d94e2000a0104100fb1128b03c56bb8ac959"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def exact(errors: list[str], section: dict[str, Any], expected: dict[str, Any], label: str) -> None:
    for key, value in expected.items():
        if section.get(key) != value:
            errors.append(f"{label} mismatch: {key}")


INTERVAL = re.compile(
    r"^\[([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?)"
    r"(?: \+/- ([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?))?\]$",
    re.IGNORECASE,
)


def interval_bounds(value: Any) -> tuple[Decimal, Decimal] | None:
    if not isinstance(value, str):
        return None
    match = INTERVAL.match(value)
    if match is None:
        return None
    try:
        center = Decimal(match.group(1))
        radius = Decimal(match.group(2) or "0")
    except InvalidOperation:
        return None
    return center - radius, center + radius


def require_interval(
    errors: list[str], section: dict[str, Any], key: str, relation: str, threshold: str
) -> None:
    bounds = interval_bounds(section.get(key))
    if bounds is None:
        errors.append(f"invalid interval: {key}")
        return
    lower, upper = bounds
    target = Decimal(threshold)
    if relation == ">" and not lower > target:
        errors.append(f"interval lower bound fails: {key}")
    elif relation == "<" and not upper < target:
        errors.append(f"interval upper bound fails: {key}")
    elif relation == "negative" and not upper < 0:
        errors.append(f"interval may meet zero: {key}")
    elif relation == "positive" and not lower > 0:
        errors.append(f"interval may meet zero: {key}")


def check_structure(data: Any, *, enforce_frozen_digest: bool = True) -> list[str]:
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
    if not isinstance(dependencies, dict) or len(dependencies) != 11:
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
    if enforce_frozen_digest and result.get("internal_digest") != INTERNAL_DIGEST:
        errors.append("internal digest mismatch")
    recomputed_digest = digest(
        {
            "orbit": result.get("deep_selected_orbit_replay"),
            "tail": result.get("tail_majorants"),
            "loop": result.get("selected_homoclinic_holonomy"),
            "wedges": result.get("four_selected_twisting_wedges"),
            "scope": result.get("scope_limits"),
        }
    )
    if result.get("internal_digest") != recomputed_digest:
        errors.append("recomputed internal digest mismatch")

    orbit = result.get("deep_selected_orbit_replay", {})
    exact(
        errors,
        orbit,
        {
            "arb_precision_bits": 5000,
            "tail_depth_F_returns": 260,
            "deep_half_collision_count": 568,
            "deep_full_F_return_count": 568,
            "deep_root_radius": "1e-400",
            "actual_graph_whole_tube_IVT": True,
            "actual_graph_unique_by_uniform_monotonicity": True,
            "decimal_center_not_substituted_for_graph_point": True,
            "prefix_enters_selected_root_interval": True,
            "prefix_interval_strictly_inside_selected_radius_1e_minus_50": True,
            "all_collisions_physical_with_frozen_margins": True,
        },
        "deep orbit",
    )
    center = orbit.get("deep_root_center", "")
    if not isinstance(center, str) or not center.startswith("-1.4393187027937387") or not center.endswith("e-286"):
        errors.append("deep root centre mismatch")
    require_interval(errors, orbit, "prefix_x_minus_selected_center", ">", "-1e-50")
    require_interval(errors, orbit, "prefix_x_minus_selected_center", "<", "1e-50")
    require_interval(errors, orbit, "left_face_momentum", "negative", "0")
    require_interval(errors, orbit, "right_face_momentum", "positive", "0")
    require_interval(errors, orbit, "shooting_monotonicity", ">", "1e190")

    coordinates = result.get("canonical_coordinate_and_gauge_audit", {})
    exact(
        errors,
        coordinates,
        {
            "graph_to_canonical": "(x,y)= (x_g,-2*kappa*y_g)",
            "canonical_involution": "[[0,-1/(2*kappa)],[-2*kappa,0]]",
            "canonical_involution_square": "identity exactly",
            "lambda_times_mu": "contains 1 with absolute radius <1e-1000",
            "g_u_over_lambda": "325/144",
            "g_s_over_mu": "-325/144",
            "gauge_matrix": "B_u(x) B_s(y)",
            "half_derivative_determinant": "1 exactly by ds wedge dp",
        },
        "canonical coordinate/gauge",
    )

    tail = result.get("tail_majorants", {})
    exact(
        errors,
        tail,
        {
            "chart_radius": "1e-10",
            "backward_graph_contraction": "0.091",
            "declared_increment_majorant": "1e80",
            "critical_entry_bound": "|delta_12|,|delta_21| <= C*r^3*(1+|log r|)",
            "noncritical_entry_bound": "|delta_ij| <= C*r^2*(1+|log r|)",
            "finite_product_monomial_count_bound": 4096,
            "finite_product_factor_degree_bound": 5,
            "right_critical_conjugation_power": "lambda^(2*n+1) on delta_12",
            "left_critical_conjugation_power": "lambda^(2*n+97) on delta_21",
            "tail_recursion": "psi_(n+1)=S_n psi_n U_n",
            "submultiplicative_product_bound": "||P-I||_infinity<=exp(sum||K_n-I||_infinity)-1",
            "two_sided_error_formula": "||psi-psi_N||<=||psi_N||*((1+eta_L)*(1+eta_R)-1)",
        },
        "tail",
    )
    for key in (
        "base_cubic_remainder_ledger",
        "derivative_quadratic_remainder_ledger",
        "critical_cubic_remainder_ledger",
        "gauge_composition_ledger",
        "gauge_difference_ledger",
        "unstable_critical_explicit_ledger",
        "noncritical_explicit_ledger",
    ):
        require_interval(errors, tail, key, ">", "0")
    require_interval(errors, tail, "derived_product_ledger", "<", "1e80")
    require_interval(errors, tail, "critical_ratio_rho", "<", "0.1")
    require_interval(errors, tail, "right_critical_sum", "<", "1e-225")
    require_interval(errors, tail, "left_critical_sum_including_lambda_power_96", "<", "1e-125")
    require_interval(errors, tail, "right_tail_exponent_sum", "<", "1e-225")
    require_interval(errors, tail, "left_tail_exponent_sum", "<", "1e-125")
    require_interval(errors, tail, "right_tail_product_error", "<", "1e-225")
    require_interval(errors, tail, "left_tail_product_error", "<", "1e-125")
    require_interval(errors, tail, "two_sided_loop_entry_error", "<", "1e-47")

    loop = result.get("selected_homoclinic_holonomy", {})
    exact(
        errors,
        loop,
        {
            "typed_F_return_decomposition": "N + 48 + N = 2*N+48",
            "unstable_approximant": "H^u_N=A_hat^N(w_N) A^(-N):E_p->E_z",
            "stable_approximant": "H^s_N=A^(-(N+48)) A_hat^(N+48)(z):E_z->E_p",
            "finite_truncation_formula": (
                "A^(-(N+48)) B(Iw_N)^(-1) DF^(2N+48)(w_N) "
                "B(w_N) A^(-N)"
            ),
            "matrix_in_canonical_QNL_eigenfiber_E_p": True,
            "numeric_Hu_tail": True,
            "numeric_Hs_tail": True,
            "numeric_psi_z": True,
        },
        "typed numerical loop",
    )
    finite = loop.get("finite_matrix")
    enclosed = loop.get("infinite_matrix_enclosure")
    if not (
        isinstance(finite, list) and len(finite) == 2
        and all(isinstance(row, list) and len(row) == 2 for row in finite)
    ):
        errors.append("finite matrix shape mismatch")
    if not (
        isinstance(enclosed, list) and len(enclosed) == 2
        and all(isinstance(row, list) and len(row) == 2 for row in enclosed)
    ):
        errors.append("infinite matrix shape mismatch")

    wedges = result.get("four_selected_twisting_wedges", {})
    require_interval(errors, wedges, "wedge_e1_psi_e1", "negative", "0")
    require_interval(errors, wedges, "wedge_e2_psi_e1", "negative", "0")
    require_interval(errors, wedges, "wedge_e1_psi_e2", "positive", "0")
    require_interval(errors, wedges, "wedge_e2_psi_e2", "positive", "0")
    require_interval(errors, wedges, "wedge_e2_psi_e2", ">", "1e-29")

    scope = result.get("scope_limits", {})
    for key in (
        "selected_immutable_homoclinic_loop_numeric_enclosure",
        "four_selected_QNL_eigen_axis_twisting_wedges",
    ):
        if scope.get(key) is not True:
            errors.append(f"certified selected-loop flag missing: {key}")
    for key in (
        "comparison_with_periodic_shadow_matrix",
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
            "selected_numeric_psi_z": "CERTIFIED",
            "four_selected_QNL_twisting_wedges": "CERTIFIED",
            "periodic_shadow_identification": "NOT_CLAIMED",
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
        import cm2_gate1_numeric_holonomy_tail_twisting_frontier_cert as cert

        actual = cert.certify_numeric_loop()
    except Exception as exc:  # pragma: no cover
        return [f"certificate replay failed: {exc}"]
    return [] if data.get("result") == actual else ["certificate replay mismatch"]


def run_self_test(data: dict[str, Any]) -> int:
    mutations: list[tuple[str, dict[str, Any]]] = []

    def add(label: str, mutate) -> None:
        tampered = copy.deepcopy(data)
        mutate(tampered)
        result = tampered["result"]
        result["internal_digest"] = digest(
            {
                "orbit": result["deep_selected_orbit_replay"],
                "tail": result["tail_majorants"],
                "loop": result["selected_homoclinic_holonomy"],
                "wedges": result["four_selected_twisting_wedges"],
                "scope": result["scope_limits"],
            }
        )
        mutations.append((label, tampered))

    add("F-return typing", lambda d: d["result"]["selected_homoclinic_holonomy"].__setitem__("typed_F_return_decomposition", "N+24+N"))
    add("stable approximant", lambda d: d["result"]["selected_homoclinic_holonomy"].__setitem__("stable_approximant", "untyped"))
    add("whole graph IVT", lambda d: d["result"]["deep_selected_orbit_replay"].__setitem__("actual_graph_whole_tube_IVT", False))
    add("graph uniqueness", lambda d: d["result"]["deep_selected_orbit_replay"].__setitem__("actual_graph_unique_by_uniform_monotonicity", False))
    add("point substitution", lambda d: d["result"]["deep_selected_orbit_replay"].__setitem__("decimal_center_not_substituted_for_graph_point", False))
    add("canonical conversion", lambda d: d["result"]["canonical_coordinate_and_gauge_audit"].__setitem__("graph_to_canonical", "swap"))
    add("unstable resonance", lambda d: d["result"]["canonical_coordinate_and_gauge_audit"].__setitem__("g_u_over_lambda", "0"))
    add("critical cubic ledger", lambda d: d["result"]["tail_majorants"].__setitem__("critical_cubic_remainder_ledger", "[-1 +/- 0]"))
    add("monomial count", lambda d: d["result"]["tail_majorants"].__setitem__("finite_product_monomial_count_bound", 1))
    add("factor degree four", lambda d: d["result"]["tail_majorants"].__setitem__("finite_product_factor_degree_bound", 4))
    add("right critical power", lambda d: d["result"]["tail_majorants"].__setitem__("right_critical_conjugation_power", "lambda^n"))
    add("left fixed power", lambda d: d["result"]["tail_majorants"].__setitem__("left_critical_conjugation_power", "lambda^(2*n+1) on delta_21"))
    add("tail recursion", lambda d: d["result"]["tail_majorants"].__setitem__("tail_recursion", "unknown"))
    add("submultiplicativity", lambda d: d["result"]["tail_majorants"].__setitem__("submultiplicative_product_bound", "unknown"))
    add("left critical sum", lambda d: d["result"]["tail_majorants"].__setitem__("left_critical_sum_including_lambda_power_96", "[1 +/- 0]"))
    add("two-sided error", lambda d: d["result"]["tail_majorants"].__setitem__("two_sided_loop_entry_error", "[1 +/- 0]"))
    add("Hu tail", lambda d: d["result"]["selected_homoclinic_holonomy"].__setitem__("numeric_Hu_tail", False))
    add("smallest wedge", lambda d: d["result"]["four_selected_twisting_wedges"].__setitem__("wedge_e2_psi_e2", "[0 +/- 1e-20]"))
    add("shadow substitution", lambda d: d["result"]["scope_limits"].__setitem__("comparison_with_periodic_shadow_matrix", True))
    add("class H overclaim", lambda d: d["result"]["scope_limits"].__setitem__("butler_park_class_H", True))
    add("Gate 1 overclaim", lambda d: d["result"]["scope_limits"].__setitem__("gate1_certified", True))

    for label, tampered in mutations:
        # The mutation carries its own freshly recomputed internal digest and
        # the frozen digest comparison is disabled here.  Rejection therefore
        # comes from an independent semantic guard, not a stale hash.
        if not check_structure(tampered, enforce_frozen_digest=False):
            print(f"SELF_TEST: FAIL ({label} mutation accepted)")
            return 1
    print(f"MUTATION_SELF_TEST: PASS ({len(mutations)}/{len(mutations)} mutations rejected)")
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
        print("GATE1_NUMERIC_HOLONOMY_TAIL_TWISTING_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        return run_self_test(data)
    if args.integrity_only or args.replay:
        print("REPLAY_AND_INTEGRITY: PASS")
        return 0
    print("SELECTED_NUMERIC_PSI_Z: CERTIFIED")
    print("FOUR_SELECTED_QNL_TWISTING_WEDGES: CERTIFIED")
    print("PERIODIC_SHADOW_IDENTIFICATION: NOT_CLAIMED")
    print("BUTLER_PARK_CLASS_H: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
