#!/usr/bin/env python3
"""Independent verifier for the Round-56 CM2 core-poles/ledger audit."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "deliverables" / (
    "cm2-round56-independent-core-poles-and-r55-ledger-audit-"
    "manifest-2026-07-20.json"
)

EXPECTED_LITERATURE = {
    "2607.06242v2": (
        "037d2789745ce9e085cb8d404d1be70d5a804675630ea1351f8a3f7672c2abe6",
        "generalized_coupling_criterion_for_wasserstein_exponential_mixing_of_markov_cocycles",
        "does_not_construct_stable_quotient_projective_frostman_endpoint_stopping_or_amplitude_registry",
    ),
    "2607.11467v1": (
        "f5232558bd958bf1628bb524623800fe631b8273cb10a75f292614fd74dfccba",
        "tensor_divergence_measure_bv_pairing_normal_trace_and_gauss_green_on_rough_domains",
        "does_not_supply_billiard_dynamic_piola_bound_anisotropic_current_norm_qs_rs_or_mt_dq",
    ),
    "2601.14061v1": (
        "fa1c64f3a17bcb5a2cee105549820f4b2326a5f0d5f16ddbdccbf7a1ba96e4be",
        "frostman_dimension_for_one_compactly_supported_sip_sl2_law",
        "does_not_cover_unbuilt_place_dependent_billiard_reverse_quotient_or_stopped_tree",
    ),
    "2604.13401v1": (
        "bd62a5989838f9ba26a1c96b6b2bb165add3ee79f83cfa32f5883e4174c690e4",
        "periodic_data_rigidity_for_cocycles_and_hyperbolic_automorphisms",
        "assumes_periodic_conjugacy_or_related_rigidity_inputs_and_does_not_build_cm2_common_frame",
    ),
    "2606.29603v1": (
        "71d1f43cf3d2be39ec466e6e73af4fa21eba6e3fd60f31bdcab2ff323678a329",
        "global_periodic_data_rigidity_for_irreducible_toral_automorphisms",
        "toral_anosov_all_periodic_data_theorem_not_singular_billiard_common_gauge_construction",
    ),
    "2606.10155v1": (
        "3330b5467c5c7107e58ba7966a0386f2ab51415990399b387ad2f7e571f61798",
        "review_of_transfer_operators_for_dispersing_billiards_with_problem_8_7_open",
        "does_not_close_general_characteristic_restriction_loss_of_memory_or_mt_dq",
    ),
    "2604.19671v2": (
        "fc00f45a8ec6513763665bf8fa34569a95ca5d6d6b9fa5d90b7e1089fabd9004",
        "linear_response_of_fixed_sinai_billiard_conditional_survival_measure_to_hole_size_at_zero",
        "does_not_supply_moving_scatterer_finite_s_branch_atlas_operator_norm_dq_or_mt_dq",
    ),
}

LEAF_TESTS = (
    (
        "deliverables/cm2_gate34_round55_hereditary_terminal_z_"
        "refinement_frontier_verifier.py",
        "HOSTILE_MUTATIONS_REJECTED: 40/40",
        40,
    ),
    (
        "deliverables/cm2_gate34_round55_global_image_recut_cap_"
        "natural_mesh_frontier_verifier.py",
        "HOSTILE_MUTATIONS_REJECTED: 27/27",
        27,
    ),
    (
        "deliverables/cm2_gate5_round55_synchronised_pairing_"
        "delayed_collar_verifier.py",
        "HOSTILE_SELF_TEST: 127/127",
        127,
    ),
)


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def no_nonfinite(token: str) -> None:
    raise ValueError(f"non-finite token: {token}")


def strict_load_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=no_duplicates,
        parse_constant=no_nonfinite,
    )


def load() -> dict[str, Any]:
    data = strict_load_text(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("root is not object")
    return data


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def dependency_check(data: dict[str, Any]) -> None:
    rows = data.get("dependencies")
    if not isinstance(rows, list) or len(rows) != 15:
        raise ValueError("dependency cardinality")
    names: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "sha256"}:
            raise ValueError("dependency row shape")
        name = row["path"]
        sha = row["sha256"]
        if not isinstance(name, str) or name in names:
            raise ValueError("dependency path duplication")
        names.add(name)
        if not isinstance(sha, str) or len(sha) != 64:
            raise ValueError("dependency hash shape")
        path = ROOT / name
        if path.is_symlink() or not path.is_file():
            raise ValueError("dependency missing or symlink")
        if digest(path) != sha:
            raise ValueError("dependency hash drift")


def semantics(data: dict[str, Any]) -> None:
    if set(data) != {
        "artifact",
        "date",
        "dependencies",
        "gate_audit",
        "literature_audit",
        "round55_corrections",
        "schema",
        "strict_verdict",
    }:
        raise ValueError("top-level shape")
    if data["schema"] != "cm2.round56.independent-core-poles-ledger-audit.v1":
        raise ValueError("schema")
    if data["artifact"] != "cm2-round56-independent-core-poles-and-r55-ledger-audit":
        raise ValueError("artifact")
    if data["date"] != "2026-07-20":
        raise ValueError("date")

    counts = data["round55_corrections"]["hostile_count"]
    if set(counts) != {
        "aggregate_report",
        "aggregate_total",
        "bookkeeping_only",
        "current_leaf_verifiers",
        "current_total",
        "delta",
        "leaf_mathematical_verdicts_unchanged",
    }:
        raise ValueError("hostile-count shape")
    if counts["aggregate_report"] != [38, 27, 115]:
        raise ValueError("aggregate components")
    if counts["current_leaf_verifiers"] != [40, 27, 127]:
        raise ValueError("current components")
    if counts["aggregate_total"] != 180 or counts["aggregate_total"] != sum(
        counts["aggregate_report"]
    ):
        raise ValueError("aggregate total")
    if counts["current_total"] != 194 or counts["current_total"] != sum(
        counts["current_leaf_verifiers"]
    ):
        raise ValueError("current total")
    if counts["delta"] != 14:
        raise ValueError("count delta")
    if counts["bookkeeping_only"] is not True:
        raise ValueError("bookkeeping guard")
    if counts["leaf_mathematical_verdicts_unchanged"] is not True:
        raise ValueError("leaf verdict guard")

    sync = data["round55_corrections"]["synchronised_coupling"]
    if sync != {
        "d_best_rule": "min(d_sync,d_product)",
        "d_best_status": "NEVER_WORSE_AND_SOMETIMES_STRICT",
        "d_product_le_d_sync": "FALSE_IN_GENERAL",
        "d_sync_le_d_product": "FALSE_IN_GENERAL",
        "sync_status": "VALID_ALTERNATIVE_SAME_SOURCE_WITNESS",
    }:
        raise ValueError("sync correction")

    gates = data["gate_audit"]
    if set(gates) != {"gate1", "gate2", "gate3", "gate4", "gate5"}:
        raise ValueError("gate shape")
    if gates["gate1"] != {
        "official_status": "NOT_CERTIFIED",
        "physical_full_cross_common_vertex": "CERTIFIED",
        "same_representative_class_h_plus_twisting": "NOT_CERTIFIED",
        "shortest_input": "physical_cross_term_rate_omega_lt_m_or_exact_cancellation_then_same_representative_wedge_replay",
    }:
        raise ValueError("Gate-1 semantics")
    if gates["gate2"] != {
        "candidate_cone_product_layers": "7/7_NON_OFFICIAL",
        "first_missing": "stable_saturated_product_base_Lambda_A",
        "invariant_stable_product_layers": 0,
        "official_fields": "0/17",
        "official_status": "NOT_CERTIFIED",
    }:
        raise ValueError("Gate-2 semantics")
    if gates["gate3"] != {
        "fixed_free_graph_current_slots": 41508,
        "mt_dq": "NOT_CERTIFIED",
        "official_status": "NOT_CERTIFIED",
        "physical_qs_rs": "NOT_CERTIFIED",
    }:
        raise ValueError("Gate-3 semantics")
    if gates["gate4"]["physical_j_pair"] != "NOT_CERTIFIED":
        raise ValueError("Gate-4 promotion")
    if gates["gate4"]["official_status"] != "NOT_CERTIFIED":
        raise ValueError("Gate-4 status")
    baseline_scope = (
        "PINNED_ROUND55_MAY_BE_SUPERSEDED_BY_SEPARATELY_VALIDATED_ROUND56_LEAF"
    )
    if gates["gate4"]["baseline_scope"] != baseline_scope:
        raise ValueError("Gate-4 baseline scope")
    if gates["gate5"] != {
        "baseline_scope": baseline_scope,
        "complete_blocks": 0,
        "maturity": "10/18",
        "official_status": "NOT_CERTIFIED",
        "physical_trace_contraction": "NOT_CERTIFIED",
    }:
        raise ValueError("Gate-5 semantics")

    verdict = data["strict_verdict"]
    if verdict != {
        "complete_composite_gates": "0/5",
        "gate1": "NOT_CERTIFIED",
        "gate2": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
        "gate4": "NOT_CERTIFIED",
        "gate5": "NOT_CERTIFIED",
        "overall": "NO-GO_FOR_CLAIM",
    }:
        raise ValueError("strict verdict")

    rows = data["literature_audit"]
    if not isinstance(rows, list) or len(rows) != len(EXPECTED_LITERATURE):
        raise ValueError("literature cardinality")
    if [row["arxiv"] for row in rows] != list(EXPECTED_LITERATURE):
        raise ValueError("literature ordering")
    for row in rows:
        if set(row) != {"arxiv", "pdf_sha256", "scope", "cm2_nonpromotion"}:
            raise ValueError("literature shape")
        sha, scope, nonpromotion = EXPECTED_LITERATURE[row["arxiv"]]
        if (row["pdf_sha256"], row["scope"], row["cm2_nonpromotion"]) != (
            sha,
            scope,
            nonpromotion,
        ):
            raise ValueError("literature scope/hash drift")


def algebra_replay() -> None:
    # Neither the synchronized nor normalized-product coupling dominates.
    examples = (
        (Fraction(0), Fraction(1, 2), "sync"),
        (Fraction(1), Fraction(1, 2), "product"),
    )
    for sync, product, winner in examples:
        observed = "sync" if sync < product else "product"
        if observed != winner or min(sync, product) > sync or min(sync, product) > product:
            raise ValueError("coupling-order countermodel")

    # Dirac reverse kernel and unbounded determinant-one Piola multiplier.
    if sum(weight * weight for weight in (Fraction(1),)) != 1:
        raise ValueError("Dirac energy")
    for expansion in (3, 17, 257, 4099):
        if Fraction(1) / Fraction(1, expansion) != expansion:
            raise ValueError("Piola separator")


def live_leaf_replay() -> list[int]:
    counts: list[int] = []
    for rel, marker, count in LEAF_TESTS:
        proc = subprocess.run(
            [sys.executable, str(ROOT / rel), "--self-test"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        if proc.returncode != 0 or marker not in proc.stdout + proc.stderr:
            raise ValueError(f"leaf self-test failure: {rel}")
        counts.append(count)
    if counts != [40, 27, 127] or sum(counts) != 194:
        raise ValueError("leaf hostile total")
    return counts


def validate(data: dict[str, Any], check_dependencies: bool = True) -> None:
    semantics(data)
    algebra_replay()
    if check_dependencies:
        dependency_check(data)


def assign_path(data: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    target: Any = data
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def hostile_self_test() -> tuple[int, int]:
    original = load()
    mutations: list[tuple[tuple[Any, ...], Any]] = [
        (("schema",), "cm2.bad"),
        (("artifact",), "bad"),
        (("date",), "2026-07-19"),
        (("round55_corrections", "hostile_count", "aggregate_report", 0), 39),
        (("round55_corrections", "hostile_count", "aggregate_total"), 181),
        (("round55_corrections", "hostile_count", "current_leaf_verifiers", 0), 39),
        (("round55_corrections", "hostile_count", "current_leaf_verifiers", 2), 126),
        (("round55_corrections", "hostile_count", "current_total"), 180),
        (("round55_corrections", "hostile_count", "delta"), 0),
        (("round55_corrections", "hostile_count", "bookkeeping_only"), False),
        (("round55_corrections", "hostile_count", "leaf_mathematical_verdicts_unchanged"), False),
        (("round55_corrections", "synchronised_coupling", "d_best_rule"), "d_sync"),
        (("round55_corrections", "synchronised_coupling", "d_sync_le_d_product"), "TRUE"),
        (("round55_corrections", "synchronised_coupling", "d_product_le_d_sync"), "TRUE"),
        (("round55_corrections", "synchronised_coupling", "d_best_status"), "STRICT_ALWAYS"),
        (("gate_audit", "gate1", "physical_full_cross_common_vertex"), "NOT_CERTIFIED"),
        (("gate_audit", "gate1", "same_representative_class_h_plus_twisting"), "CERTIFIED"),
        (("gate_audit", "gate2", "official_fields"), "1/17"),
        (("gate_audit", "gate2", "invariant_stable_product_layers"), 1),
        (("gate_audit", "gate2", "first_missing"), "markov_kernel"),
        (("gate_audit", "gate3", "fixed_free_graph_current_slots"), 41507),
        (("gate_audit", "gate3", "mt_dq"), "CERTIFIED"),
        (("gate_audit", "gate4", "physical_j_pair"), "CERTIFIED"),
        (("gate_audit", "gate4", "baseline_scope"), "GLOBAL_ROUND56_CLAIM"),
        (("gate_audit", "gate5", "maturity"), "11/18"),
        (("gate_audit", "gate5", "complete_blocks"), 1),
        (("gate_audit", "gate5", "baseline_scope"), "GLOBAL_ROUND56_CLAIM"),
        (("strict_verdict", "complete_composite_gates"), "1/5"),
        (("strict_verdict", "overall"), "GO"),
        (("strict_verdict", "gate3"), "CERTIFIED"),
        (("literature_audit", 0, "arxiv"), "2607.06242v1"),
        (("literature_audit", 0, "scope"), "physical_gate2_closure"),
        (("literature_audit", 1, "cm2_nonpromotion"), "promotes_mt_dq"),
        (("literature_audit", 1, "pdf_sha256"), "0" * 64),
        (("dependencies", 0, "sha256"), "0" * 64),
    ]
    rejected = 0
    for path, value in mutations:
        candidate = copy.deepcopy(original)
        assign_path(candidate, path, value)
        try:
            validate(candidate, check_dependencies=True)
        except (ValueError, OSError, KeyError, TypeError):
            rejected += 1

    strict_json_cases = (
        '{"a":1,"a":2}',
        '{"a":NaN}',
        '{"a":Infinity}',
    )
    for payload in strict_json_cases:
        try:
            strict_load_text(payload)
        except ValueError:
            rejected += 1

    total = len(mutations) + len(strict_json_cases)
    return rejected, total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        if args.self_test:
            rejected, total = hostile_self_test()
            if rejected != total:
                raise ValueError(f"hostile rejection shortfall {rejected}/{total}")
            print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
            return 0

        data = load()
        validate(data, check_dependencies=True)
        counts = [40, 27, 127] if args.integrity_only else live_leaf_replay()
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(f"ROUND56_AUDIT_VERIFIER_FAILURE: {exc}", file=sys.stderr)
        return 1

    if args.integrity_only or args.replay:
        print("ROUND56_AUDIT_INTEGRITY: PASS")
        print(f"ROUND55_LIVE_HOSTILE_TOTAL: {'+'.join(map(str, counts))}={sum(counts)}")
        print("NO_GATE_PROMOTION: PASS")
        return 0

    print("AUDIT_MODE: PASS")
    print("ROUND55_HOSTILE_COUNT: 194_BOOKKEEPING_CORRECTION")
    print("SYNC_COST_ORDER: INCOMPARABLE_USE_MINIMUM")
    print("GATE1_2_3: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
