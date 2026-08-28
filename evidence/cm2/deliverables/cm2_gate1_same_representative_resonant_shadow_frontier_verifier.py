#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-1 same-representative frontier."""

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
    / "cm2-gate1-same-representative-resonant-shadow-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate1_same_representative_resonant_shadow_frontier_cert.py"
REPORT = HERE / "cm2-gate1-same-representative-resonant-shadow-frontier-assault-2026-07-16.md"
SCHEMA = "cm2.gate1.same-representative-resonant-shadow-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate1.same-representative-resonant-shadow-frontier.v1"
INTERNAL_DIGEST = "d3919cc092e1857f24609ec871ad8b783af6c808a7b3953ca6297a863be846e5"


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
    elif relation == "positive" and not lower > 0:
        errors.append(f"interval may meet zero: {key}")
    elif relation == "negative" and not upper < 0:
        errors.append(f"interval may meet zero: {key}")


def recompute_internal(result: dict[str, Any]) -> str:
    return digest(
        {
            "transport": result.get("cohomology_transport_frontier"),
            "shadow": result.get("compact_gauge_periodic_shadow_obstruction"),
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
    if not isinstance(dependencies, dict) or len(dependencies) != 7:
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
            "global_internal_digest": "3849c2037d34b17c4a3196896294cdc9d650e802f87585376b5368c8b20ebeb6",
            "numeric_internal_digest": "866afbfd317fbe21b9921f7152c9d94e2000a0104100fb1128b03c56bb8ac959",
            "compact_internal_digest": "4d2780a1ae29a170403576efe8890236199656c33848c7d2736d86e3e5c95251",
            "shadow_schema": "cm2.gate1.closed-shadow-twisting.v1",
        },
        "provenance",
    )

    transport = result.get("cohomology_transport_frontier", {})
    exact(
        errors,
        transport,
        {
            "cohomology_convention": "B(x)=D(fx)^-1 A(x) D(x)",
            "finite_n_identity": (
                "H^s_B(x,y;n)=D(y)^-1 A^n(y)^-1 "
                "[D(f^n y)D(f^n x)^-1] A^n(x)D(x)"
            ),
            "right_factored_defect": (
                "L^s_D(x,y;n)=A^n(x)^-1[D(f^n y)D(f^n x)^-1]A^n(x)"
            ),
            "transport_if_and_only_if_defect_limit_is_identity": True,
            "holder_transfer_alone_forces_identity_defect": False,
            "diagonal_loop_same_axis_wedges": "both exactly zero",
            "compact_loop_four_wedges": "all four strictly nonzero",
            "all_selected_stable_unstable_defects_can_be_identity": False,
        },
        "cohomology transport",
    )

    shadow = result.get("compact_gauge_periodic_shadow_obstruction", {})
    exact(
        errors,
        shadow,
        {
            "arb_precision_bits": 5000,
            "refined_shadow_root_radius": "1e-800",
            "periodic_shadow_collision_count": 96,
            "periodic_shadow_half_word": "Q^10 B^2",
            "periodic_shadow_full_word": "Q^10 B^4 Q^10",
            "same_selected_homoclinic_excursion_word": True,
            "compact_gauge_cutoff_is_one_near_shadow": True,
            "compact_gauge_is_C_infinity_near_shadow": True,
            "return_determinant_contains_one": True,
            "return_trace_gt_1e53": True,
            "gauged_stable_direction_lower_left_derivative_excludes_zero": True,
            "stable_increment_asymptotic": (
                "(K_n)_21 ~ -Lambda*c*d*Lambda^n for a nontrivial stable tail"
            ),
            "compact_gauge_stable_canonical_limit_at_shadow": "DIVERGENT",
            "nontrivial_local_stable_tail_required": True,
            "compact_gauge_class_H_on_clean_horseshoe_containing_shadow_and_nontrivial_stable_tail": False,
            "shadow_membership_in_predecessor_existential_horseshoe": "NOT_CERTIFIED",
        },
        "shadow obstruction",
    )
    require_interval(errors, shadow, "shadow_qnl_x_coordinate", "<", "-1e-15")
    require_interval(errors, shadow, "shadow_qnl_y_coordinate", ">", "1e-14")
    require_interval(errors, shadow, "return_unstable_multiplier", ">", "1e53")
    require_interval(errors, shadow, "return_stable_multiplier", "positive", "0")
    require_interval(errors, shadow, "return_stable_multiplier", "<", "1e-53")
    require_interval(errors, shadow, "compact_gauge_coefficient", "positive", "0")
    require_interval(
        errors,
        shadow,
        "gauged_stable_direction_lower_left_derivative",
        "negative",
        "0",
    )

    scope = result.get("scope_limits", {})
    for key in (
        "finite_faithful_clean_coding_from_predecessor",
        "diagonal_representative_class_H_from_predecessor",
        "compact_gauge_selected_four_wedges_from_predecessor",
    ):
        if scope.get(key) is not True:
            errors.append(f"certified positive scope flag missing: {key}")
    for key in (
        "diagonal_representative_weak_typicality",
        "formal_cohomology_transport_merges_the_two_representatives",
        "compact_gauge_class_H_on_clean_horseshoe_containing_shadow_and_nontrivial_stable_tail",
        "shadow_membership_in_predecessor_existential_horseshoe",
        "every_possible_third_representative_obstructed",
        "single_representative_class_H_and_twisting_certified",
        "full_mass_global_singular_coding",
        "physical_projective_PPE",
        "gate1_certified",
        "unconditional_cm2",
    ):
        if scope.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")
    if scope.get("nontrivial_local_stable_tail_required") is not True:
        errors.append("nontrivial stable-tail scope qualifier missing")

    exact(
        errors,
        data.get("verdict", {}),
        {
            "cohomology_transport_defect": "CERTIFIED",
            "formal_merge_of_diagonal_H_and_compact_twisting": "REFUTED",
            "compact_gauge_shadow_stable_canonical_limit": "DIVERGENT",
            "compact_gauge_class_H_on_shadow_horseshoe_with_nontrivial_stable_tail": "REFUTED",
            "third_representative_class_H_plus_twisting": "NOT_CERTIFIED",
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
        import cm2_gate1_same_representative_resonant_shadow_frontier_cert as cert

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

    add("defect identity", lambda d: d["result"]["cohomology_transport_frontier"].__setitem__("finite_n_identity", "formal conjugacy"))
    add("Holder transport overclaim", lambda d: d["result"]["cohomology_transport_frontier"].__setitem__("holder_transfer_alone_forces_identity_defect", True))
    add("identity defects", lambda d: d["result"]["cohomology_transport_frontier"].__setitem__("all_selected_stable_unstable_defects_can_be_identity", True))
    add("word", lambda d: d["result"]["compact_gauge_periodic_shadow_obstruction"].__setitem__("periodic_shadow_full_word", "Q^10 B^2"))
    add("precision", lambda d: d["result"]["compact_gauge_periodic_shadow_obstruction"].__setitem__("arb_precision_bits", 1000))
    add("root radius", lambda d: d["result"]["compact_gauge_periodic_shadow_obstruction"].__setitem__("refined_shadow_root_radius", "1e-200"))
    add("determinant", lambda d: d["result"]["compact_gauge_periodic_shadow_obstruction"].__setitem__("return_determinant_contains_one", False))
    add("mixed coefficient", lambda d: d["result"]["compact_gauge_periodic_shadow_obstruction"].__setitem__("gauged_stable_direction_lower_left_derivative", "[0 +/- 1]"))
    add("mixed separation", lambda d: d["result"]["compact_gauge_periodic_shadow_obstruction"].__setitem__("gauged_stable_direction_lower_left_derivative_excludes_zero", False))
    add("convergence", lambda d: d["result"]["compact_gauge_periodic_shadow_obstruction"].__setitem__("compact_gauge_stable_canonical_limit_at_shadow", "CONVERGENT"))
    add("compact H", lambda d: d["result"]["compact_gauge_periodic_shadow_obstruction"].__setitem__("compact_gauge_class_H_on_clean_horseshoe_containing_shadow_and_nontrivial_stable_tail", True))
    add("membership overclaim", lambda d: d["result"]["compact_gauge_periodic_shadow_obstruction"].__setitem__("shadow_membership_in_predecessor_existential_horseshoe", "CERTIFIED"))
    add("scope membership", lambda d: d["result"]["scope_limits"].__setitem__("shadow_membership_in_predecessor_existential_horseshoe", True))
    add("all gauges no-go", lambda d: d["result"]["scope_limits"].__setitem__("every_possible_third_representative_obstructed", True))
    add("same representative overclaim", lambda d: d["result"]["scope_limits"].__setitem__("single_representative_class_H_and_twisting_certified", True))
    add("full-mass overclaim", lambda d: d["result"]["scope_limits"].__setitem__("full_mass_global_singular_coding", True))
    add("PPE overclaim", lambda d: d["result"]["scope_limits"].__setitem__("physical_projective_PPE", True))
    add("Gate1 overclaim", lambda d: d["result"]["scope_limits"].__setitem__("gate1_certified", True))
    add("verdict Gate1", lambda d: d["verdict"].__setitem__("gate1", "CERTIFIED"))
    add("verdict CM2", lambda d: d["verdict"].__setitem__("unconditional_cm2", "GO"))

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
        print("GATE1_SAME_REPRESENTATIVE_RESONANT_SHADOW_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        return run_self_test(data)
    if args.integrity_only or args.replay:
        print("REPLAY_AND_INTEGRITY: PASS")
        return 0
    print("COHOMOLOGY_TRANSPORT_DEFECT: CERTIFIED")
    print("FORMAL_MERGE_OF_DIAGONAL_H_AND_COMPACT_TWISTING: REFUTED")
    print("COMPACT_GAUGE_SHADOW_STABLE_CANONICAL_LIMIT: DIVERGENT")
    print("COMPACT_GAUGE_CLASS_H_ON_SHADOW_HORSESHOE_WITH_NONTRIVIAL_STABLE_TAIL: REFUTED")
    print("THIRD_REPRESENTATIVE_CLASS_H_PLUS_TWISTING: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
