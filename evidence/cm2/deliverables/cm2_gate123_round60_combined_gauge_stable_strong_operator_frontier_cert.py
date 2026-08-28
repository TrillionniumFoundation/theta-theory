#!/usr/bin/env python3
"""CM2 Round-60 Gate-1/2/3 typed-frontier certificate.

The positive modes certify exact conditional interfaces, separators and
re-audits.  Default execution exits two because Gates 1, 2 and 3 remain open.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / "deliverables"
REPORT = HERE / (
    "cm2-gate123-round60-combined-gauge-stable-strong-operator-"
    "frontier-assault-2026-07-20.md"
)
MANIFEST = HERE / (
    "cm2-gate123-round60-combined-gauge-stable-strong-operator-"
    "frontier-manifest-2026-07-20.json"
)
VERIFIER = HERE / (
    "cm2_gate123_round60_combined_gauge_stable_strong_operator_"
    "frontier_verifier.py"
)
Q = Fraction


DEPENDENCIES = {
    "deliverables/cm2-fifty-ninth-direct-assault-2026-07-20.md":
        "ec0623ec2fd6138c74d3707fd1c6f5e385b98187dcbd616cadee3b19e39dd5ef",
    "deliverables/cm2-fifty-ninth-direct-assault-manifest-2026-07-20.sha256":
        "c013b5aa22db44308c7aa4cbe2b0800da14f709bcc80250464478b047cfc0712",
    "deliverables/cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.json":
        "16a2562868df58b2e14bf672d2d0d11735581016ff50e10f5a6d2c1e660d3466",
    "deliverables/cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.sha256":
        "985910708fe715d0c891cd6a288b37a5e1b88530db858a712e7e82e80cbb4b71",
}


class CertificateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def qtext(value: Q) -> str:
    return str(value)


def validate_dependencies() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for rel, expected in DEPENDENCIES.items():
        path = ROOT / rel
        require(path.is_file() and not path.is_symlink(), f"dependency file/type: {rel}")
        require(sha256_path(path) == expected, f"dependency hash drift: {rel}")
        rows.append({"path": rel, "sha256": expected})
    return rows


def gate1_replay() -> dict[str, Any]:
    compact_error = Q(8568, 10**52)
    wedge_lower = Q(17344, 10**32)
    gauge_budget = wedge_lower / compact_error
    require(gauge_budget == Q(216800000000000000000000, 1071),
            "compact-to-combined gauge budget")
    require(gauge_budget > 2 * 10**20, "gauge budget magnitude")

    selected_rows = [(n + 1) * Q(1, 10) ** n for n in range(8)]
    selected_sum = Q(1) / (1 - Q(1, 10)) ** 2
    require(selected_sum == Q(100, 81), "selected compact Dini sum")

    harmonic_rows: list[dict[str, str | int]] = []
    previous = Q(0)
    for power in range(1, 11):
        count = 2**power
        partial = sum((Q(1, n + 1) for n in range(count)), Q(0))
        require(partial > previous, "harmonic partial monotonicity")
        require(partial >= 1 + Q(power, 2), "harmonic dyadic lower bound")
        harmonic_rows.append({
            "power": power,
            "terms": count,
            "partial_sum": qtext(partial),
            "certified_lower_bound": qtext(1 + Q(power, 2)),
        })
        previous = partial

    amplification_rows = []
    for n in range(8):
        compact = (n + 1) * Q(1, 10) ** n
        factor = 10**n
        combined = factor * compact
        require(combined == n + 1, "gauge amplification row")
        amplification_rows.append({
            "n": n,
            "compact_increment": qtext(compact),
            "unbounded_comparison_factor": factor,
            "combined_increment": qtext(combined),
        })

    return {
        "compact_to_combined_twisting_budget": {
            "frozen_compact_loop_error_strict_upper": qtext(compact_error),
            "frozen_smallest_wedge_strict_lower": qtext(wedge_lower),
            "exact_K_gauge_strict_upper": qtext(gauge_budget),
            "magnitude_strict_lower": "2*10^20",
            "conditional_statement": (
                "if one immutable same-representative join proves "
                "E_combined<=K_gauge*E_compact with K_gauge below the exact "
                "budget, all four selected twisting wedges remain strict"
            ),
            "physical_K_gauge": "NOT_CERTIFIED",
            "same_representative_join": "NOT_CERTIFIED",
            "status": "CERTIFIED_CONDITIONAL_GAUGE_COMPARISON_BUDGET",
        },
        "selected_to_all_plaque_separator": {
            "scope": (
                "exact logical two-plaque completion of fields left unconstrained "
                "by the frozen selected-germ row; not a billiard realization"
            ),
            "selected_compact_sequence": "(n+1)*10^-n",
            "selected_exact_sum": qtext(selected_sum),
            "selected_first_eight": [qtext(x) for x in selected_rows],
            "bad_plaque_combined_sequence": "1/(n+1)",
            "harmonic_dyadic_rows": harmonic_rows,
            "conclusion": (
                "one selected physical compact-gauge Dini loop does not imply "
                "an all-plaque combined-gauge Dini registry"
            ),
            "status": "CERTIFIED_FALSE_BY_LOGICAL_PLAQUE_SEPARATOR",
        },
        "unbounded_gauge_separator": {
            "scope": "logical gauge ledger only; no physical gauge is constructed",
            "factor": "A_n=10^n",
            "rows_first_eight": amplification_rows,
            "combined_sequence": "n+1",
            "status": "CERTIFIED_NO_CROSS_GAUGE_PROMOTION_WITHOUT_UNIFORM_COMPARISON",
        },
        "minimal_physical_interface": {
            "rows": [
                "all-actual-plaque standard-Borel registry with immutable IDs",
                "combined half-density increments in one common gauge",
                "physical summable weighted all-plaque envelope",
                "immutable same-representative H join and finite K_gauge",
                "selected twisting transported through that same join",
            ],
            "physical_all_plaque_combined_gauge_registry": "NOT_CERTIFIED",
            "same_representative_H_plus_twisting": "NOT_CERTIFIED",
            "gate1": "NOT_CERTIFIED",
        },
    }


def gate2_replay() -> dict[str, Any]:
    prefix = [True] * 96 + [False]
    require(sum(prefix[:96]) == 96 and prefix[96] is False,
            "depth-97 prefix separator")
    sampled_rows = [
        {"depth": depth, "required_chart_survives": prefix[depth - 1]}
        for depth in (1, 2, 95, 96, 97)
    ]

    join_rows = [
        {"field": 1, "name": "physical stable-product rectangles", "status": "NOT_CERTIFIED"},
        {"field": 2, "name": "stable projection and two-sided physical J_hol", "status": "NOT_CERTIFIED"},
        {"field": 3, "name": "full-span or bounded landing fragmentation", "status": "NOT_CERTIFIED"},
        {"field": 4, "name": "same-law unstable conditionals and distortion", "status": "NOT_CERTIFIED_EXISTING_CURVE_DENSITIES_ONLY"},
        {"field": 5, "name": "J_land,min<C_p*h almost everywhere", "status": "NOT_CERTIFIED"},
        {"field": 6, "name": "tagged Borel first-return branch inverse", "status": "CERTIFIED_ROUND59"},
        {"field": 7, "name": "strong restriction and assembly", "status": "NOT_CERTIFIED_WEAK_GRAPH_REASSEMBLY_ONLY"},
    ]
    require([row["field"] for row in join_rows] == list(range(1, 8)),
            "seven-field numbering")
    require(sum(row["status"].startswith("CERTIFIED") for row in join_rows) == 1,
            "seven-field completed count")

    return {
        "finite_prefix_separator": {
            "frozen_actual_collision_shadow_prefixes": "1..96",
            "accepted_prefix_count": 96,
            "logical_completion_sample": sampled_rows,
            "first_unconstrained_depth": 97,
            "scope": (
                "logical depth ledger compatible with all frozen finite-prefix rows; "
                "not a claim that the billiard fails at depth 97"
            ),
            "conclusion": (
                "96 finite collision-shadow zeros do not imply all-depth "
                "graph-transform chart survival"
            ),
            "status": "CERTIFIED_FALSE_BY_DEPTH_97_SEPARATOR",
        },
        "minimal_all_depth_stable_package": {
            "rows": [
                "actual stable plaques on a stable-saturated Borel base",
                "all-depth graph transforms with common charts and controlled bad shadow",
                "Borel stable projection",
                "two-sided Radon-Nikodym J_hol for the collision Liouville/SRB law",
                "same-arclength target density and fragmentation/span rows",
                "immutable join to the actual first-return landing graph",
                "strong restriction and assembly on the target physical space",
            ],
            "physical_all_depth_graph_transforms": "NOT_CERTIFIED",
            "physical_base_projection_two_sided_J_hol": "NOT_CERTIFIED",
            "status": "CERTIFIED_MINIMAL_INTERFACE_ONLY",
        },
        "actual_landing_join_audit": {
            "rows": join_rows,
            "completed_fields": "1/7",
            "official_immutable_gate2_fields": "0/17",
            "weak_graph_reconditioning_is_strong_assembly": False,
            "gate2": "NOT_CERTIFIED",
        },
    }


def no_earlier_root(a: Q, b: Q, tau: Q) -> bool:
    require(b > 0 and tau > 0, "first-root domain")
    delta = a * a - b
    return a <= 0 or delta < 0 or (
        a - tau >= 0 and delta <= (a - tau) ** 2
    )


def earlier_root_exists(a: Q, b: Q, tau: Q) -> bool:
    """Independent exact predicate for an earliest root in (0,tau)."""
    require(b > 0 and tau > 0, "earlier-root domain")
    delta = a * a - b
    if a <= 0 or delta < 0:
        return False
    if a - tau < 0:
        return True
    return delta > (a - tau) ** 2


def first_root_grid() -> dict[str, Any]:
    rows: list[list[str | bool]] = []
    true_count = 0
    for ai in range(-6, 11):
        a = Q(ai, 2)
        for bi in range(1, 25):
            b = Q(bi, 4)
            for ti in range(1, 9):
                tau = Q(ti, 2)
                no_root = no_earlier_root(a, b, tau)
                has_root = earlier_root_exists(a, b, tau)
                require(no_root is (not has_root), "first-root predicate complement")
                true_count += int(no_root)
                rows.append([qtext(a), qtext(b), qtext(tau), no_root])
    require(len(rows) == 3264, "first-root grid size")
    return {
        "grid_cases": len(rows),
        "no_earlier_true_cases": true_count,
        "earlier_root_true_cases": len(rows) - true_count,
        "grid_sha256": canonical_digest(rows),
    }


def gate3_replay() -> dict[str, Any]:
    grid = first_root_grid()

    competitor_slots = 161
    rows_per_competitor = 5
    competitor_budget = competitor_slots * rows_per_competitor
    other_budget = 25
    per_step = competitor_budget + other_budget
    require((competitor_budget, per_step) == (805, 830), "atom budget")

    budget_rows = []
    for n in range(1, 9):
        variables = 8 * n + 5
        atoms = per_step * n + 12
        require(variables <= 400 * n + 20, "declared variable fit")
        require(atoms <= 2000 * n + 100, "declared atom fit")
        budget_rows.append({
            "depth": n,
            "physical_variables_upper": variables,
            "physical_atoms_upper": atoms,
            "physical_degree_upper": 4,
            "raw_word_candidates": 8 * 162**n,
        })

    clock_rows = []
    for n in range(8):
        probability = Q(1, 2 ** (n + 1))
        raw_candidates = 8 * 162**n
        contribution = probability * raw_candidates
        require(contribution == 4 * 81**n, "raw enumeration expectation term")
        clock_rows.append({
            "depth": n,
            "probability": qtext(probability),
            "raw_candidate_upper": raw_candidates,
            "expectation_term": qtext(contribution),
        })
    require(math.exp(1 / 6) < 2, "installed exponential moment ratio")

    degree_rows = []
    d_value = 8
    for r in range(9):
        closed = 2 ** (4 * 2**r - 1)
        require(d_value == closed, "CAD degree closed form")
        degree_rows.append({"projection_step": r, "D_r": str(d_value)})
        d_value = 2 * d_value**2

    return {
        "chosen_target_first_root_reaudit": {
            "domain": "|u|=1, b>0 for distinct competitors, tau>0",
            "predicate": (
                "a<=0 OR Delta<0 OR "
                "[a-tau>=0 AND Delta<=(a-tau)^2]"
            ),
            "sign_guard_before_squaring": True,
            "chosen_target_is_not_silently_selected_by_competitor_predicate": True,
            "current_source_uses_outgoing_convexity_row": True,
            **grid,
            "status": "CERTIFIED_EXACT_REAUDIT",
        },
        "atom_and_depth_scope_reaudit": {
            "target_slots": 162,
            "chosen_slots": 1,
            "nonchosen_slots": competitor_slots,
            "padded_atoms_per_nonchosen_slot": rows_per_competitor,
            "competitor_atom_budget": competitor_budget,
            "dynamics_sign_tie_cemetery_budget": other_budget,
            "per_step_atom_budget": per_step,
            "initial_atom_budget": 12,
            "per_step_auxiliary_variables": 8,
            "budget_rows_first_eight": budget_rows,
            "scope": "for every fixed depth n; no depth-integrated conclusion",
            "status": "CERTIFIED_FIXED_DEPTH_REAUDIT_NO_PROMOTION",
        },
        "clock_vs_raw_enumeration_separator": {
            "optimistic_typing": "formula depth N is identified with Dbar",
            "logical_clock_law": "P{N=n}=2^(-n-1), n>=0",
            "installed_moment": "E exp(N/6)=1/[2*(1-exp(1/6)/2)]<infinity",
            "raw_bound_expectation": "4*sum_(n>=0)81^n=infinity",
            "rows_first_eight": clock_rows,
            "guard": (
                "divergence concerns the current raw candidate upper bound; "
                "it is not a lower bound on actual nonempty physical branches"
            ),
            "status": "CERTIFIED_MOMENT_DOES_NOT_PAY_RAW_ENUMERATION_ROUTE",
        },
        "cad_degree_frontier": {
            "recurrence": "D_0=8, D_(r+1)=2*D_r^2",
            "closed_form": "D_r=2^(4*2^r-1)",
            "rows_first_nine": degree_rows,
            "actual_cell_lower_bound": False,
            "depth_integrated_complexity": "NOT_CERTIFIED",
        },
        "direct_strong_interface": {
            "rows": [
                "physical strong restriction R_s and quotient/assembly Q_s",
                "moving-scatterer directional Piola including singular/current terms",
                "common-domain derivative and MT_DQ moving-test estimate",
                "commutation and immutable carrier/owner/cemetery joins",
            ],
            "physical_strong_R_s_Q_s": "NOT_CERTIFIED",
            "directional_Piola": "NOT_CERTIFIED",
            "MT_DQ": "NOT_CERTIFIED",
            "gate3": "NOT_CERTIFIED",
        },
        "latest_official_technology_audit": {
            "checked_on": "2026-07-20",
            "arXiv_2604_19671v2": {
                "title": "Linear response for Sinai billiards with small holes",
                "useful_local_analogue": (
                    "hole conditional evolution preserves regular standard families; "
                    "C^1-test coupling and a one-step vertical-boundary standard-family "
                    "representation are available"
                ),
                "type_mismatch": (
                    "fixed billiard with varying hole size, not moving-scatterer "
                    "directional Piola/MT_DQ or the CM2 strong R/Q maps"
                ),
                "explicit_Banach_space_boundary": (
                    "the paper states that no known Banach spaces for general "
                    "piecewise hyperbolic systems contain standard pairs"
                ),
            },
            "arXiv_2605_18110v3": (
                "sample points for connected components of one real inequation under "
                "generic smoothness; no billiard inverse lengths or depth integration"
            ),
            "arXiv_2607_02400v1": (
                "fixed-dimensional polytopal-measure cutting algorithms; no moving "
                "billiard operator interface"
            ),
            "external_theorem_promoted": False,
        },
    }


def result_payload() -> dict[str, Any]:
    result = {
        "gate1": gate1_replay(),
        "gate2": gate2_replay(),
        "gate3": gate3_replay(),
        "strict_status": {
            "gate1": "NOT_CERTIFIED",
            "gate2": "NOT_CERTIFIED",
            "gate2_immutable_fields": "0/17",
            "gate2_landing_join": "1/7",
            "gate3": "NOT_CERTIFIED",
            "composite_gates": "0/5",
            "cm2": "NO-GO_FOR_CLAIM",
        },
    }
    return result


def build_manifest(check_dependencies: bool = True) -> dict[str, Any]:
    dependencies = validate_dependencies() if check_dependencies else [
        {"path": rel, "sha256": digest} for rel, digest in DEPENDENCIES.items()
    ]
    require(REPORT.is_file() and not REPORT.is_symlink(), "report file/type")
    require(VERIFIER.is_file() and not VERIFIER.is_symlink(), "verifier file/type")
    result = result_payload()
    return {
        "schema": "cm2.gate123.round60.combined-gauge-stable-strong-operator-frontier.v1",
        "artifact": "cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier",
        "date": "2026-07-20",
        "dependencies": dependencies,
        "result": result,
        "result_sha256": canonical_digest(result),
        "strict_verdict": (
            "exact gauge, finite-prefix and clock/counting frontiers are certified; "
            "physical all-plaque Dini, all-depth stable holonomy and strong moving-"
            "scatterer R/Q/Piola/MT_DQ remain not certified"
        ),
        "report_sha256": sha256_path(REPORT),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(VERIFIER),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--summary-json", action="store_true")
    parser.add_argument("--emit-manifest", type=Path)
    args = parser.parse_args()

    try:
        data = build_manifest(check_dependencies=True)
        if args.emit_manifest is not None:
            args.emit_manifest.write_bytes(canonical_bytes(data))
            print(f"EMITTED: {args.emit_manifest}")
            return 0
        if args.summary_json:
            print(json.dumps(data["result"], indent=2, sort_keys=True))
            return 0
        require(MANIFEST.is_file() and not MANIFEST.is_symlink(), "manifest file/type")
        require(MANIFEST.read_bytes() == canonical_bytes(data), "manifest drift")
    except (CertificateError, OSError, ValueError) as exc:
        print(f"CERTIFICATE_ERROR: {exc}", file=sys.stderr)
        return 1

    print("DEPENDENCIES: 4/4")
    print("GATE1_COMPACT_TO_COMBINED_BUDGET: CERTIFIED_CONDITIONAL")
    print("GATE1_SELECTED_TO_ALL_PLAQUE: CERTIFIED_FALSE_BY_SEPARATOR")
    print("GATE2_PREFIX_TO_ALL_DEPTH: CERTIFIED_FALSE_BY_SEPARATOR")
    print("GATE3_FIRST_ROOT_AND_ATOM_BUDGET: CERTIFIED_REAUDIT")
    print("GATE3_CLOCK_PAYS_RAW_ENUMERATION: CERTIFIED_FALSE_BY_SEPARATOR")
    print("GATES_1_2_3: NOT_CERTIFIED")
    print("COMPOSITE_GATES: 0/5")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.audit else 2


if __name__ == "__main__":
    raise SystemExit(main())
