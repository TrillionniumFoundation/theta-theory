#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-1 coding/class-H separation frontier."""

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
    HERE
    / "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate1_global_coding_class_h_frontier_cert.py"
REPORT = HERE / "cm2-gate1-global-coding-class-h-separation-frontier-assault-2026-07-16.md"
SCHEMA = "cm2.gate1.global-coding-class-h-separation-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate1.global-coding-class-h-separation-frontier.v1"
INTERNAL_DIGEST = "3849c2037d34b17c4a3196896294cdc9d650e802f87585376b5368c8b20ebeb6"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def exact(
    errors: list[str], section: dict[str, Any], expected: dict[str, Any], label: str
) -> None:
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
    errors: list[str],
    section: dict[str, Any],
    key: str,
    relation: str,
    threshold: str,
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
    elif relation == "positive" and not lower > 0:
        errors.append(f"interval may meet zero: {key}")
    elif relation == "negative" and not upper < 0:
        errors.append(f"interval may meet zero: {key}")


def recompute_internal(result: dict[str, Any]) -> str:
    return digest(
        {
            "transverse": result.get("selected_transverse_homoclinic"),
            "connector": result.get("connector_compact_gauge_obstruction"),
            "symbolic": result.get("symbolic_and_class_h_frontier"),
            "scope": result.get("scope_limits"),
        }
    )


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
    if result.get("internal_digest") != recompute_internal(result):
        errors.append("recomputed internal digest mismatch")

    provenance = result.get("provenance", {})
    exact(
        errors,
        provenance,
        {
            "immutable_internal_digest": "95c274e761c08ad9768e98040aa46663e113f70c6167e556faea659b535ef000",
            "numeric_internal_digest": "866afbfd317fbe21b9921f7152c9d94e2000a0104100fb1128b03c56bb8ac959",
            "compact_internal_digest": "4d2780a1ae29a170403576efe8890236199656c33848c7d2736d86e3e5c95251",
            "butler_park_arxiv": "1909.11548v2",
            "audited_pdf_sha256": "63c186b1a09db9db50882ba29c32b6395d868596138011f97d5284a484a590ca",
        },
        "provenance",
    )

    transverse = result.get("selected_transverse_homoclinic", {})
    exact(
        errors,
        transverse,
        {
            "arb_precision_bits": 1000,
            "selected_half_collision_count": 48,
            "symmetric_full_collision_count": 96,
            "actual_unstable_graph_tangent_cone": "(1,h'(x)), |h'(x)|<=1e-4",
            "reflection_tangent_determinant_formula": "det((a,b),(a,-b))=-2*a*b",
            "absolute_reflection_tangent_determinant_gt_3e54": True,
            "selected_qnl_homoclinic_is_transverse": True,
            "clean_physical_half_word_replayed": True,
            "birkhoff_smale_clean_horseshoe_exists": True,
            "finite_markov_partition_for_a_clean_return_iterate_exists": True,
        },
        "transverse homoclinic",
    )
    require_interval(errors, transverse, "terminal_theta_tangent_component_lower", ">", "9e26")
    require_interval(errors, transverse, "terminal_momentum_tangent_component_lower", ">", "2e27")
    require_interval(errors, transverse, "absolute_reflection_tangent_determinant_lower", ">", "3e54")

    connector = result.get("connector_compact_gauge_obstruction", {})
    exact(
        errors,
        connector,
        {
            "arb_precision_bits": 1000,
            "connector_return": "G=T^14 at the certified symmetric connector fixed point",
            "symplectic_multiplier_identity": "Lambda*nu=1 exactly",
            "stable_mixed_jet_in_minus_1_over_20_minus_1_over_25": True,
            "compact_qnl_gauge_chart_radius": "1e-10",
            "connector_has_neighbourhood_where_compact_qnl_gauge_is_identity": True,
            "stable_graph_form": "x=h(y), h(0)=h'(0)=0",
            "canonical_increment_formula": (
                "(K_n)_21=-Lambda*(Lambda/nu)^n*b_21(y_n), "
                "b_21(y)=c*y+O(y^2)"
            ),
            "canonical_increment_asymptotic": (
                "(K_n)_21~ -Lambda*c*d*Lambda^n for y_n~d*nu^n, d!=0"
            ),
            "compact_qnl_gauge_connector_stable_limit_converges": False,
            "compact_qnl_gauge_class_H_on_common_basic_set_with_connector": False,
        },
        "connector obstruction",
    )
    require_interval(errors, connector, "connector_unstable_multiplier", ">", "1e8")
    require_interval(errors, connector, "connector_stable_multiplier", "positive", "0")
    require_interval(errors, connector, "connector_stable_multiplier", "<", "1e-8")
    require_interval(errors, connector, "stable_mixed_jet_partial_xy_G2", "negative", "0")
    require_interval(errors, connector, "stable_mixed_jet_partial_xy_G2", ">", "-0.05")
    require_interval(errors, connector, "stable_mixed_jet_partial_xy_G2", "<", "-0.04")
    require_interval(errors, connector, "connector_qnl_eigen_coordinate", "<", "-1e-4")

    symbolic = result.get("symbolic_and_class_h_frontier", {})
    coding = symbolic.get("clean_symbolic_coding", {})
    exact(
        errors,
        coding,
        {
            "base": "a finite SFT coding of a clean Birkhoff-Smale horseshoe for a return iterate",
            "selected_qnl_periodic_code": True,
            "selected_transverse_homoclinic_code": True,
            "coding_map": "pi:Sigma_A->Lambda, G o pi=pi o sigma",
            "faithful_actual_cocycle": (
                "A_log(x)=E(sigma*x)^-1 D_{pi(x)}G E(x); no frozen word matrix substitution"
            ),
            "finite_clean_horseshoe_coding_certified": True,
            "full_collision_srb_mass_coding_certified": False,
            "global_singular_billiard_coding_certified": False,
        },
        "clean coding",
    )

    diagonal = symbolic.get("invariant_frame_class_H", {})
    exact(
        errors,
        diagonal,
        {
            "higher_block_sign_recode": True,
            "faithful_diagonal_formula": (
                "A_diag(x)=C(sigma*x)^-1 A_log(x) C(x)=diag(a_u(x),a_s(x))"
            ),
            "canonical_stable_and_unstable_holonomies_converge": True,
            "canonical_holonomies_are_holder": True,
            "diagonal_representative_belongs_to_butler_park_class_H": True,
            "all_canonical_holonomy_loops_are_diagonal": True,
            "same_axis_twisting_wedges_are_exactly_zero": True,
            "diagonal_representative_is_weakly_typical": False,
        },
        "diagonal class H",
    )

    frontier = symbolic.get("same_representative_frontier", {})
    exact(
        errors,
        frontier,
        {
            "selected_compact_gauge_four_wedges": True,
            "selected_compact_gauge_all_plaque_holder_holonomies": False,
            "selected_compact_gauge_class_H_on_selected_horseshoe": False,
            "selected_compact_gauge_class_H_on_selected_horseshoe_status": "NOT_CERTIFIED",
            "diagonal_gauge_global_class_H": True,
            "diagonal_gauge_selected_same_axis_twisting": False,
            "cohomology_does_not_identify_non_fiber_bunched_canonical_holonomies": True,
            "one_representative_with_both_class_H_and_weak_typicality": False,
            "one_representative_with_both_status": "NOT_CERTIFIED",
        },
        "same representative frontier",
    )

    scope = result.get("scope_limits", {})
    for key in (
        "selected_transverse_qnl_homoclinic",
        "finite_faithful_clean_horseshoe_coding",
        "faithful_diagonal_class_H_representative_on_clean_horseshoe",
    ):
        if scope.get(key) is not True:
            errors.append(f"certified positive scope flag missing: {key}")
    for key in (
        "global_full_mass_physical_coding",
        "diagonal_representative_weakly_typical",
        "compact_twisting_gauge_uniform_all_plaque_holder_holonomies",
        "compact_twisting_gauge_butler_park_class_H",
        "single_representative_class_H_and_weak_typicality",
        "physical_projective_PPE",
        "gate1_certified",
        "unconditional_cm2",
    ):
        if scope.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    exact(
        errors,
        data.get("verdict", {}),
        {
            "selected_transverse_qnl_homoclinic": "CERTIFIED",
            "finite_faithful_clean_horseshoe_coding": "CERTIFIED",
            "diagonal_invariant_frame_class_H": "CERTIFIED",
            "diagonal_invariant_frame_weak_typicality": "REFUTED",
            "compact_twisting_gauge_global_class_H": "NOT_CERTIFIED",
            "single_representative_class_H_plus_twisting": "NOT_CERTIFIED",
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
        import cm2_gate1_global_coding_class_h_frontier_cert as cert

        actual = cert.certify_frontier()
    except Exception as exc:  # pragma: no cover
        return [f"certificate replay failed: {exc}"]
    return [] if data.get("result") == actual else ["certificate replay mismatch"]


def run_self_test(data: dict[str, Any]) -> int:
    mutations: list[tuple[str, dict[str, Any]]] = []

    def add(label: str, mutate) -> None:
        tampered = copy.deepcopy(data)
        mutate(tampered)
        tampered["result"]["internal_digest"] = recompute_internal(tampered["result"])
        mutations.append((label, tampered))

    add("transversality", lambda d: d["result"]["selected_transverse_homoclinic"].__setitem__("selected_qnl_homoclinic_is_transverse", False))
    add("reflection determinant", lambda d: d["result"]["selected_transverse_homoclinic"].__setitem__("absolute_reflection_tangent_determinant_lower", "[0 +/- 1]"))
    add("clean replay", lambda d: d["result"]["selected_transverse_homoclinic"].__setitem__("clean_physical_half_word_replayed", False))
    add("finite coding", lambda d: d["result"]["symbolic_and_class_h_frontier"]["clean_symbolic_coding"].__setitem__("finite_clean_horseshoe_coding_certified", False))
    add("matrix substitution", lambda d: d["result"]["symbolic_and_class_h_frontier"]["clean_symbolic_coding"].__setitem__("faithful_actual_cocycle", "periodic matrices"))
    add("full-mass overclaim", lambda d: d["result"]["symbolic_and_class_h_frontier"]["clean_symbolic_coding"].__setitem__("full_collision_srb_mass_coding_certified", True))
    add("diagonal formula", lambda d: d["result"]["symbolic_and_class_h_frontier"]["invariant_frame_class_H"].__setitem__("faithful_diagonal_formula", "approximate"))
    add("class H", lambda d: d["result"]["symbolic_and_class_h_frontier"]["invariant_frame_class_H"].__setitem__("diagonal_representative_belongs_to_butler_park_class_H", False))
    add("Holder holonomy", lambda d: d["result"]["symbolic_and_class_h_frontier"]["invariant_frame_class_H"].__setitem__("canonical_holonomies_are_holder", False))
    add("zero diagonal wedge", lambda d: d["result"]["symbolic_and_class_h_frontier"]["invariant_frame_class_H"].__setitem__("same_axis_twisting_wedges_are_exactly_zero", False))
    add("diagonal typicality", lambda d: d["result"]["symbolic_and_class_h_frontier"]["invariant_frame_class_H"].__setitem__("diagonal_representative_is_weakly_typical", True))
    add("same representative", lambda d: d["result"]["symbolic_and_class_h_frontier"]["same_representative_frontier"].__setitem__("one_representative_with_both_class_H_and_weak_typicality", True))
    add("compact H overclaim", lambda d: d["result"]["symbolic_and_class_h_frontier"]["same_representative_frontier"].__setitem__("selected_compact_gauge_class_H_on_selected_horseshoe", True))
    add("connector mixed jet", lambda d: d["result"]["connector_compact_gauge_obstruction"].__setitem__("stable_mixed_jet_partial_xy_G2", "[0 +/- 1]"))
    add("connector convergence", lambda d: d["result"]["connector_compact_gauge_obstruction"].__setitem__("compact_qnl_gauge_connector_stable_limit_converges", True))
    add("connector support", lambda d: d["result"]["connector_compact_gauge_obstruction"].__setitem__("connector_has_neighbourhood_where_compact_qnl_gauge_is_identity", False))
    add("PPE overclaim", lambda d: d["result"]["scope_limits"].__setitem__("physical_projective_PPE", True))
    add("Gate1 overclaim", lambda d: d["result"]["scope_limits"].__setitem__("gate1_certified", True))

    for label, tampered in mutations:
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
        print("GATE1_GLOBAL_CODING_CLASS_H_FRONTIER_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        return run_self_test(data)
    if args.integrity_only or args.replay:
        print("REPLAY_AND_INTEGRITY: PASS")
        return 0
    print("SELECTED_TRANSVERSE_QNL_HOMOCLINIC: CERTIFIED")
    print("FINITE_FAITHFUL_CLEAN_HORSESHOE_CODING: CERTIFIED")
    print("DIAGONAL_INVARIANT_FRAME_CLASS_H: CERTIFIED")
    print("DIAGONAL_INVARIANT_FRAME_WEAK_TYPICALITY: REFUTED")
    print("COMPACT_TWISTING_GAUGE_GLOBAL_CLASS_H: NOT_CERTIFIED")
    print("SINGLE_REPRESENTATIVE_CLASS_H_PLUS_TWISTING: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
