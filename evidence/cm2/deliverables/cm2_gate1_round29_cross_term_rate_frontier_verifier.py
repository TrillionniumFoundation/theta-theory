#!/usr/bin/env python3
"""Independent verifier for the round-29 Gate-1 cross-term rate leaf."""

from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2_gate1_round29_cross_term_rate_frontier_cert.py"
MANIFEST = HERE / "cm2-gate1-round29-cross-term-rate-frontier-manifest-2026-07-18.json"
REPORT = HERE / "cm2-gate1-round29-cross-term-rate-frontier-assault-2026-07-18.md"
EXPECTED_CERTIFICATE_SHA256 = "2ab53804b7287e5ac764d3b3109526a8e936bfc523966fbfd4b0b60053f1d52b"
EXPECTED_DEPENDENCIES = {
    "cm2-twenty-eighth-direct-assault-manifest-2026-07-18.sha256":
        "a281274b76fc81401ec7fbf574fae0df7fa67c9b8b5146c583c88a9c73b95e80",
    "cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.json":
        "dacbae6255707086bc7486e4933d8c890ede1547a9e545995800a5fc18698f83",
    "cm2-gate1-round25-common-frame-manifest-2026-07-18.json":
        "66d4b207a0155ee98a7632154c81caebd567f43aa1a449ffc28b421b175cd436",
}
VARIABLE = "cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.json"
COMMON = "cm2-gate1-round25-common-frame-manifest-2026-07-18.json"


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise VerificationError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def parse_json(text: str) -> Any:
    try:
        return json.loads(
            text,
            object_pairs_hook=reject_pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(
                VerificationError(f"non-finite JSON token: {token}")
            ),
        )
    except VerificationError:
        raise
    except Exception as exc:
        raise VerificationError(f"malformed JSON: {exc}") from exc


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def qstr(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def safe_file(path: Path) -> None:
    require(path.parent.resolve() == HERE, f"escaped path: {path.name}")
    require(not path.is_symlink(), f"symlink rejected: {path.name}")
    require(path.is_file(), f"missing file: {path.name}")


def load_dependencies() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name, expected in EXPECTED_DEPENDENCIES.items():
        path = HERE / name
        safe_file(path)
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        if path.suffix == ".json":
            out[name] = parse_json(path.read_text(encoding="utf-8"))
    return out


def independent_samples() -> dict[str, Any]:
    m, omega = Fraction(3, 5), Fraction(1, 3)
    delta, vx, vy = Fraction(7, 11), Fraction(2), Fraction(3)
    ratio = omega / m
    require(ratio == Fraction(5, 9) and ratio < 1, "decay ratio")
    decay = [vx * vy * delta * ratio**n for n in range(6)]
    require(all(decay[n + 1] == ratio * decay[n] for n in range(5)),
            "decay recurrence")
    bad_m, bad_omega = Fraction(1, 3), Fraction(1, 2)
    epsilon = Fraction(1, 10**12)
    bad_ratio = bad_omega / bad_m
    growth = [epsilon**2 * bad_ratio**n for n in range(6)]
    require(bad_ratio == Fraction(3, 2), "growth ratio")
    require(all(growth[n + 1] == bad_ratio * growth[n] for n in range(5)),
            "growth recurrence")
    memory = [Fraction(5, 7), Fraction(2, 7), Fraction(1, 7),
              Fraction(1, 14), Fraction(1, 28), Fraction(0), Fraction(0)]
    require(memory[5:] == [0, 0], "finite memory")
    return {
        "decay_sample": {
            "m": qstr(m), "omega": qstr(omega), "omega_over_m": qstr(ratio),
            "Vx": qstr(vx), "Vy": qstr(vy), "delta": qstr(delta),
            "Z_n_n0_to_5": [qstr(x) for x in decay],
        },
        "amplitude_only_countermodel": {
            "m": qstr(bad_m), "omega": qstr(bad_omega),
            "omega_over_m": qstr(bad_ratio), "epsilon": qstr(epsilon),
            "Z_n_n0_to_5": [qstr(x) for x in growth],
            "every_nonzero_fixed_amplitude_preserves_bad_exponential_ratio": True,
        },
        "finite_memory_sample": {
            "last_possible_nonzero_depth_L": 4,
            "defect_n0_to_6": [qstr(x) for x in memory],
            "renormalised_cross_term_identically_zero_for_n_gt_L": True,
        },
    }


def expected_result() -> dict[str, Any]:
    deps = load_dependencies()
    variable = deps[VARIABLE]["result"]
    common = deps[COMMON]["result"]
    frontier = variable["nonlinear_third_gauge_compatibility_frontier"]
    green = variable["one_sided_all_plaque_green_theorems"]
    require(frontier["chosen_order"] == "D=U_v L_u", "gauge order")
    require(frontier["actual_cross_term_limit_computed_on_all_physical_plaques"]
            is False, "predecessor promotion")
    require(green["former_two_variable_diagonal_linear_groupoid_equations"]
            == "SOLVED_SEPARATELY", "Green equations")
    require(variable["strict_scope"]["combined_all_plaque_third_gauge"]
            == "NOT_CERTIFIED", "combined predecessor")
    require(common["strict_nonpromotion"]["Gate1"] == "NOT_CERTIFIED",
            "Gate1 predecessor")
    require(common["uniform_big_cell_certificate"]["uniform_q_lower_bound_certified"]
            is True, "common frame")

    core: dict[str, Any] = {
        "schema": "cm2.gate1.round29-cross-term-rate-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(EXPECTED_DEPENDENCIES),
            "old_artifacts_modified": False,
            "arithmetic": "exact rational inequalities and symbolic groupoid algebra",
        },
        "frozen_cross_term_interface": {
            "combined_candidate_gauge": "D=U_v L_u",
            "local_unstable_pair": "x,y with the same past",
            "backward_ratio_product": "R_minus_n(x)>0",
            "lower_green_unstable_defect":
                "du_n=u(sigma^-n y)-u(sigma^-n x)",
            "bounded_upper_coordinates": "abs(v(sigma^-n x)),abs(v(sigma^-n y))<=V",
            "renormalised_cross_term":
                "Z_n=R_minus_n(x)^(-1)*v(sigma^-n y)*du_n*v(sigma^-n x)",
            "predecessor_certifies_this_is_the_only_remaining_combined_limit": True,
        },
        "uniform_rate_gap_theorem": {
            "hypotheses": [
                "R_minus_n(x)>=m^n for one uniform 0<m<1",
                "abs(du_n)<=H*omega^n*d(x,y)^beta for one 0<=omega<m",
                "abs(v(sigma^-n x)),abs(v(sigma^-n y))<=V",
            ],
            "exact_bound":
                "abs(Z_n)<=V^2*H*(omega/m)^n*d(x,y)^beta",
            "uniform_limit": "Z_n->0 with Holder-beta modulus",
            "combined_unstable_holonomy_equals_clean_upper-Green limit": True,
            "combined_stable_holonomy_remains_the_clean lower-Green limit": True,
            "conclusion":
                "the combined gauge belongs to class H under these same-registry hypotheses",
            "amplitude_size_enters_only_the_prefactor_not_the_rate": True,
        },
        "finite_memory_exact_route": {
            "hypothesis":
                "du_n=0 for every local unstable pair once n exceeds one uniform L",
            "conclusion":
                "Z_n=0 eventually; no comparison between omega and m is needed",
            "finite_future_memory_of_actual_normalised_ratio_and_marker": "NOT_CERTIFIED",
        },
        "amplitude_only_no_repair": {
            "countermodel":
                "R_minus_n=m^n, du_n=omega^n, v_x=v_y=epsilon>0, omega/m>1",
            "cross_term": "Z_n=epsilon^2*(omega/m)^n",
            "conclusion":
                "every fixed nonzero amplitude retains divergence when the rate is adverse",
            "epsilon_zero_would_remove_the_selected_upper twisting mechanism": True,
        },
        "exact_rational_replay": independent_samples(),
        "current_physical_instantiation": {
            "same_combined_third_gauge_rows": 0,
            "uniform_backward_ratio_lower_rows": 0,
            "numeric_lower_green_unstable_defect_rate_rows": 0,
            "finite_memory_rows": 0,
            "selected_homoclinic_wedges_recomputed_in_combined_family": 0,
            "round25_compact_q_gt_999_over_1000_belongs_to_different_refuted_candidate": True,
        },
        "strict_nonpromotion": {
            "combined_all_plaque_third_gauge": "NOT_CERTIFIED",
            "same_representative_class_H_plus_twisting": "NOT_CERTIFIED",
            "full_mass_physical_projective_PPE": "NOT_CERTIFIED",
            "Gate1": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result = dict(core)
    result["internal_replay_digest"] = digest(core)
    return result


EXPECTED_VERDICT = {
    "uniform_rate_gap_cross_term_theorem": "CERTIFIED_CONDITIONAL",
    "finite_memory_cross_term_theorem": "CERTIFIED_CONDITIONAL",
    "amplitude_only_repair_when_rate_is_adverse": "REFUTED",
    "actual_combined_third_gauge": "NOT_CERTIFIED",
    "Gate1": "NOT_CERTIFIED",
    "CM2": "NO-GO_FOR_CLAIM",
}


def validate(manifest: Any) -> None:
    require(isinstance(manifest, dict), "manifest shape")
    require(set(manifest) == {
        "schema", "date", "certificate_sha256", "verifier_sha256",
        "report_sha256", "dependencies", "result", "verdict",
    }, "top-level keys")
    require(manifest["schema"]
            == "cm2.gate1.round29-cross-term-rate-frontier.manifest.v1",
            "schema")
    require(manifest["date"] == "2026-07-18", "date")
    require(manifest["dependencies"] == EXPECTED_DEPENDENCIES, "dependencies")
    require(manifest["certificate_sha256"] == EXPECTED_CERTIFICATE_SHA256,
            "certificate manifest hash")
    require(manifest["certificate_sha256"] == sha256_path(CERTIFICATE),
            "certificate live hash")
    require(manifest["verifier_sha256"] == sha256_path(Path(__file__).resolve()),
            "verifier live hash")
    require(manifest["report_sha256"] == sha256_path(REPORT), "report live hash")
    expected = expected_result()
    require(manifest["result"] == expected, "independent result replay")
    core = dict(manifest["result"])
    stored = core.pop("internal_replay_digest")
    require(stored == digest(core), "internal digest")
    require(manifest["verdict"] == EXPECTED_VERDICT, "verdict")


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    node: Any = value
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = replacement


def self_test(good: dict[str, Any]) -> int:
    mutations: list[tuple[tuple[str, ...], Any]] = [
        (("verdict", "Gate1"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate1"), "CERTIFIED"),
        (("result", "uniform_rate_gap_theorem", "exact_bound"), "0"),
        (("result", "exact_rational_replay", "decay_sample", "omega_over_m"), "9/5"),
        (("result", "finite_memory_exact_route", "finite_future_memory_of_actual_normalised_ratio_and_marker"), "CERTIFIED"),
        (("result", "current_physical_instantiation", "same_combined_third_gauge_rows"), 1),
        (("dependencies", "cm2-twenty-eighth-direct-assault-manifest-2026-07-18.sha256"), "0" * 64),
        (("result", "internal_replay_digest"), "0" * 64),
    ]
    passed = 0
    for batch in range(8):
        for path, replacement in mutations:
            bad = deepcopy(good)
            if isinstance(replacement, int):
                replacement = replacement + batch
            elif isinstance(replacement, str) and replacement not in {"CERTIFIED", "0", "9/5"}:
                replacement = replacement + str(batch)
            set_path(bad, path, replacement)
            try:
                validate(bad)
            except VerificationError:
                passed += 1
            else:
                raise VerificationError(f"hostile mutation accepted: {path}")
    for text in ('{"a":1,"a":2}', '{"x":NaN}'):
        try:
            parse_json(text)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError("hostile JSON accepted")
    require(passed == 66, f"hostile count {passed}")
    print("HOSTILE_TESTS: 66/66")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    for path in (CERTIFICATE, Path(__file__).resolve(), REPORT, args.manifest.resolve()):
        safe_file(path)
    manifest = parse_json(args.manifest.read_text(encoding="utf-8"))
    validate(manifest)
    if args.self_test:
        return self_test(manifest)
    if args.integrity_only:
        print("INTEGRITY: PASS")
        return 0
    if args.replay:
        print("REPLAY: PASS")
        return 0
    print("LIVE_VERDICT: GATE1_NOT_CERTIFIED; CM2_NO_GO")
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"VERIFY_FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
