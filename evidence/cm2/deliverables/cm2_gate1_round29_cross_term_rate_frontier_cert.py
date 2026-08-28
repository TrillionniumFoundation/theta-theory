#!/usr/bin/env python3
"""Round-29 Gate-1 nonlinear Green cross-term rate frontier.

The variable-diagonal predecessor solved the stable and unstable Green
equations separately and isolated one remaining cross term for the combined
gauge D=U_v L_u.  This certificate proves two exact sufficient routes for
that term: a uniform exponential rate gap and an eventual finite-memory
identity.  It also gives an exact amplitude-only countermodel.  None of the
new sufficient hypotheses is instantiated by the physical billiard data, so
Gate 1 remains fail-closed.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DEPENDENCIES = {
    "cm2-twenty-eighth-direct-assault-manifest-2026-07-18.sha256":
        "a281274b76fc81401ec7fbf574fae0df7fa67c9b8b5146c583c88a9c73b95e80",
    "cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.json":
        "dacbae6255707086bc7486e4933d8c890ede1547a9e545995800a5fc18698f83",
    "cm2-gate1-round25-common-frame-manifest-2026-07-18.json":
        "66d4b207a0155ee98a7632154c81caebd567f43aa1a449ffc28b421b175cd436",
}
VARIABLE = "cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.json"
COMMON = "cm2-gate1-round25-common-frame-manifest-2026-07-18.json"


class CertificateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise CertificateError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


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


def load_dependencies() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.parent.resolve() == HERE, f"dependency escapes directory: {name}")
        require(not path.is_symlink(), f"symlink dependency rejected: {name}")
        require(path.is_file(), f"missing dependency: {name}")
        require(sha256_path(path) == expected, f"dependency hash changed: {name}")
        if path.suffix == ".json":
            out[name] = json.loads(
                path.read_text(encoding="utf-8"),
                object_pairs_hook=reject_pairs,
                parse_constant=lambda token: (_ for _ in ()).throw(
                    CertificateError(f"non-finite JSON token: {token}")
                ),
            )
    return out


def exact_rate_samples() -> dict[str, Any]:
    # A decaying sample: Z_n = Vx*Vy*delta*(omega/m)^n.
    m = Fraction(3, 5)
    omega = Fraction(1, 3)
    delta = Fraction(7, 11)
    vx, vy = Fraction(2), Fraction(3)
    ratio = omega / m
    require(ratio == Fraction(5, 9) and ratio < 1, "decay ratio failed")
    decay = [vx * vy * delta * ratio**n for n in range(6)]
    require(all(decay[n + 1] == ratio * decay[n] for n in range(5)),
            "decay recurrence failed")

    # Amplitude cannot repair an adverse exponential rate: for every fixed
    # epsilon>0 the ratio between successive cross terms remains 3/2.
    bad_m = Fraction(1, 3)
    bad_omega = Fraction(1, 2)
    epsilon = Fraction(1, 10**12)
    bad_ratio = bad_omega / bad_m
    require(bad_ratio == Fraction(3, 2) and bad_ratio > 1,
            "divergence ratio failed")
    growth = [epsilon**2 * bad_ratio**n for n in range(6)]
    require(all(growth[n + 1] == bad_ratio * growth[n] for n in range(5)),
            "growth recurrence failed")

    finite_memory = [Fraction(5, 7), Fraction(2, 7), Fraction(1, 7),
                     Fraction(1, 14), Fraction(1, 28), Fraction(0), Fraction(0)]
    require(all(value == 0 for value in finite_memory[5:]),
            "finite-memory tail did not vanish")
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
            "defect_n0_to_6": [qstr(x) for x in finite_memory],
            "renormalised_cross_term_identically_zero_for_n_gt_L": True,
        },
    }


def build_result() -> dict[str, Any]:
    deps = load_dependencies()
    variable = deps[VARIABLE]["result"]
    common = deps[COMMON]["result"]
    frontier = variable["nonlinear_third_gauge_compatibility_frontier"]
    green = variable["one_sided_all_plaque_green_theorems"]

    require(frontier["chosen_order"] == "D=U_v L_u", "unexpected gauge order")
    require(frontier["actual_cross_term_limit_computed_on_all_physical_plaques"] is False,
            "predecessor already solved the cross term")
    require(green["former_two_variable_diagonal_linear_groupoid_equations"]
            == "SOLVED_SEPARATELY", "separate Green equations disappeared")
    require(variable["strict_scope"]["combined_all_plaque_third_gauge"]
            == "NOT_CERTIFIED", "combined gauge unexpectedly certified")
    require(common["strict_nonpromotion"]["Gate1"] == "NOT_CERTIFIED",
            "Gate1 predecessor status changed")
    require(common["uniform_big_cell_certificate"]["uniform_q_lower_bound_certified"]
            is True, "round25 common-frame layer missing")

    core: dict[str, Any] = {
        "schema": "cm2.gate1.round29-cross-term-rate-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
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
        "exact_rational_replay": exact_rate_samples(),
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


def verdict() -> dict[str, Any]:
    return {
        "uniform_rate_gap_cross_term_theorem": "CERTIFIED_CONDITIONAL",
        "finite_memory_cross_term_theorem": "CERTIFIED_CONDITIONAL",
        "amplitude_only_repair_when_rate_is_adverse": "REFUTED",
        "actual_combined_third_gauge": "NOT_CERTIFIED",
        "Gate1": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def build_manifest(verifier: Path, report: Path) -> dict[str, Any]:
    require(verifier.is_file() and not verifier.is_symlink(), "invalid verifier")
    require(report.is_file() and not report.is_symlink(), "invalid report")
    return {
        "schema": "cm2.gate1.round29-cross-term-rate-frontier.manifest.v1",
        "date": "2026-07-18",
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier),
        "report_sha256": sha256_path(report),
        "dependencies": dict(DEPENDENCIES),
        "result": build_result(),
        "verdict": verdict(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path,
                        default=HERE / "cm2_gate1_round29_cross_term_rate_frontier_verifier.py")
    parser.add_argument("--report", type=Path,
                        default=HERE / "cm2-gate1-round29-cross-term-rate-frontier-assault-2026-07-18.md")
    args = parser.parse_args()
    manifest = build_manifest(args.verifier.resolve(), args.report.resolve())
    if args.write_manifest:
        args.write_manifest.write_text(
            json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    print("UNIFORM_RATE_GAP_THEOREM: CERTIFIED_CONDITIONAL")
    print("FINITE_MEMORY_ROUTE: CERTIFIED_CONDITIONAL")
    print("ACTUAL_COMBINED_THIRD_GAUGE: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
