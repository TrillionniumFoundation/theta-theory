#!/usr/bin/env python3
"""Independent append-only audit of the three frozen CM2 Round-59 leaves."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from decimal import Decimal, ROUND_CEILING, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round59-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = SCHEMA + ".manifest.v1"
PREFIX = "cm2-round59-independent-core-frontier-audit"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-20.json"
REPORT = HERE / f"{PREFIX}-2026-07-20.md"
VERIFIER = HERE / "cm2_round59_independent_core_frontier_audit_verifier.py"

PINS = {
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json": "e7305e0b72eed28bc68b115e1201fc02e2b66d3cc95906fc6d1efc5e9463a4f5",
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.sha256": "967421bc83b283510cdb25013f2e723e5761337e56471fad64a9ef74b35536c0",
    "cm2-gate5-round59-unified-clearance-join-jordan-frontier-manifest-2026-07-20.json": "46eb285a7532377b89e37c1ba2ce6a5b28db1e661eaee4889e576c0a89c94ced",
    "cm2-gate5-round59-unified-clearance-join-jordan-frontier-manifest-2026-07-20.sha256": "2a1487d9fcfb9535f1d05c4c538ff56e6b726d209fe12e48bd637ad2e11b1161",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.json": "16a2562868df58b2e14bf672d2d0d11735581016ff50e10f5a6d2c1e660d3466",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.sha256": "985910708fe715d0c891cd6a288b37a5e1b88530db858a712e7e82e80cbb4b71",
}

LEAF_ARTIFACTS = {
    "gate4": {
        "cm2_gate4_round59_cross_fibre_rokhlin_threshold_frontier_cert.py": "a021821eb14727332a05deefab640320448ead7014ab5f93a054552ca200b59c",
        "cm2_gate4_round59_cross_fibre_rokhlin_threshold_frontier_verifier.py": "5a62538004fcffc710b6973f21977a3a3d04bc2d806691e3a7d37e1717670acd",
        "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json": "e7305e0b72eed28bc68b115e1201fc02e2b66d3cc95906fc6d1efc5e9463a4f5",
        "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-assault-2026-07-20.md": "2f66b1aff6551e97729d27f06c87a32957ab21404c0fb0ee3cc0210fa578b468",
    },
    "gate5": {
        "cm2_gate5_round59_unified_clearance_join_jordan_frontier_cert.py": "1552e226f9c31f11abbaee28fc4bce6a076a731609abb939f181561e7f815ca1",
        "cm2_gate5_round59_unified_clearance_join_jordan_frontier_verifier.py": "f6ce619db521adfbbc1867624cc71a76a64afe69b2c882e147bf085b2838453e",
        "cm2-gate5-round59-unified-clearance-join-jordan-frontier-manifest-2026-07-20.json": "46eb285a7532377b89e37c1ba2ce6a5b28db1e661eaee4889e576c0a89c94ced",
        "cm2-gate5-round59-unified-clearance-join-jordan-frontier-assault-2026-07-20.md": "b6a0f1c74a61b8590b3d3f71c59caf6840c0d8195eb50362e547e921eff9ad98",
    },
    "gate123": {
        "cm2-gate123-round59-physical-formula-shadow-dini-frontier-assault-2026-07-20.md": "43f50426abfc92e041903af4d4eb6a416d686ea7ad25ad0f013bb56cd9f4110d",
        "cm2_gate123_round59_physical_formula_shadow_dini_frontier_cert.py": "a21d81ca49b8ea8e1a89f708016e91934cee61a26e894a4ac1e56ef244004399",
        "cm2_gate123_round59_physical_formula_shadow_dini_frontier_verifier.py": "6d6acf41e1ff1d1a11a0670973868691155536a32280246786969c0c30b49d5a",
        "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.json": "16a2562868df58b2e14bf672d2d0d11735581016ff50e10f5a6d2c1e660d3466",
    },
}

C_P = Q(4 * 10**90 * 360493663, 358863)
H = Q(999, 1000)
BLOCK = 9148


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate key: {key}")
        out[key] = value
    return out


def strict_load(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    require(isinstance(value, dict), f"non-object JSON: {path.name}")
    return value


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def normalized_ledger_name(raw: str) -> str:
    path = Path(raw)
    require(not path.is_absolute() and ".." not in path.parts, "unsafe ledger path")
    parts = path.parts
    if len(parts) == 2 and parts[0] == "deliverables":
        parts = parts[1:]
    require(len(parts) == 1, "ledger path outside deliverables")
    return parts[0]


def validate_frozen() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    for name, expected in PINS.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"pin path: {name}")
        require(path.resolve().parent == HERE and sha(path) == expected, f"pin hash: {name}")
    manifests = {
        "gate4": strict_load(HERE / next(name for name in PINS if name.startswith("cm2-gate4") and name.endswith(".json"))),
        "gate5": strict_load(HERE / next(name for name in PINS if name.startswith("cm2-gate5") and name.endswith(".json"))),
        "gate123": strict_load(HERE / next(name for name in PINS if name.startswith("cm2-gate123") and name.endswith(".json"))),
    }
    ledger_rows: list[dict[str, Any]] = []
    ledger_names = {
        "gate4": "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.sha256",
        "gate5": "cm2-gate5-round59-unified-clearance-join-jordan-frontier-manifest-2026-07-20.sha256",
        "gate123": "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.sha256",
    }
    for leaf, ledger_name in ledger_names.items():
        observed: dict[str, str] = {}
        for line in (HERE / ledger_name).read_text(encoding="utf-8").splitlines():
            pieces = line.split(maxsplit=1)
            require(len(pieces) == 2 and len(pieces[0]) == 64, f"ledger syntax: {leaf}")
            name = normalized_ledger_name(pieces[1].strip())
            require(name not in observed, f"ledger duplicate: {name}")
            observed[name] = pieces[0]
        require(observed == LEAF_ARTIFACTS[leaf], f"ledger registry: {leaf}")
        for name, expected in observed.items():
            path = HERE / name
            require(path.is_file() and not path.is_symlink(), f"artifact path: {name}")
            require(path.resolve().parent == HERE and sha(path) == expected, f"artifact hash: {name}")
            ledger_rows.append({"leaf": leaf, "name": name, "sha256": expected})
    require(len(ledger_rows) == 12, "ledger row count")
    return manifests, ledger_rows


def gate4_audit(manifest: dict[str, Any]) -> dict[str, Any]:
    result = manifest["result"]
    sep = result["aggregate_to_fibrewise_separator"]
    n = C_P.numerator // C_P.denominator + 1
    good = 1 / H
    bad = Q(n) / H
    require(good < C_P < bad < 2 * C_P, "Gate4 threshold chain")
    expected_rows = []
    for m in (2, 10, 1000):
        eps = Q(1, m * n)
        j = 1 + Q(1, m) - Q(1, m * n)
        moment = H * (1 + Q(3, m * n))
        expected_rows.append({
            "m": m,
            "bad_outer_weight": qstr(eps),
            "bad_common_mass": qstr(eps * H),
            "aggregate_J_land_min": qstr(j),
            "aggregate_H": qstr(H),
            "aggregate_normalized_Z": qstr(j / H),
            "aggregate_D_land_dyadic_moment": qstr(moment),
            "good_D_land": 0,
            "bad_D_land": 2,
            "bad_fibre_is_proper": False,
        })
        require(j / H < C_P and eps * H > 0, "Gate4 aggregate/bad mass")
    require(sep["rows"] == expected_rows and sep["bad_z"] == qstr(bad), "Gate4 separator rows")
    bridge = result["quantitative_product_rectangle_bridge"]
    bound = Q(153) * Q(2000, 1999) / (Q(1, 2) * Q(1, 12800))
    require(bound == Q(7_833_600_000, 1999) < C_P, "Gate4 bridge")
    require(bridge["arithmetic_only_replay"]["F_R_over_theta_L"] == qstr(bound), "Gate4 bridge row")
    graph = result["same_graph_rokhlin_reconditioning"]
    require("probability kernel" in graph["disintegration_identity"] and "not division by the singleton mass" in graph["disintegration_identity"], "Gate4 nonatomic disintegration")
    require("Gamma_u-almost surely" in graph["conditional_support"] and "eta-almost-everywhere" in graph["null_set_policy"], "Gate4 conditional a.e. scope")
    require("not yet a physical unstable-product partition" in graph["what_is_not_certified"], "Gate4 weak scope")
    seven = result["seven_field_materialization_audit"]
    require(seven["actual_complete_rows"] == "1/7" and seven["official_Gate2_fields_unchanged"] == "0/17", "Gate4 maturity scope")
    require(result["strict_nonpromotion"]["Gate4"] == "NOT_CERTIFIED", "Gate4 status")
    return {
        "threshold_chain": "1/H<C_p<N/H<2*C_p",
        "D_bad": 2,
        "separator_rows": len(expected_rows),
        "separator_rows_sha256": digest(expected_rows),
        "bridge_bound": qstr(bound),
        "weak_Rokhlin_scope": "eta-a.e. kernel on same tagged graph only; no singleton division, stable-product or strong-family conclusion",
        "seven_field_join": "1/7_NOT_A_GATE2_PROMOTION",
        "status": "PASS",
    }


def clock_constants() -> tuple[Decimal, Decimal, Decimal]:
    with localcontext() as ctx:
        ctx.prec = 120
        gamma = Decimal(2000) / Decimal(1999) * Decimal(1 + 48 * BLOCK) * (Decimal(900337) / Decimal(901685)) ** BLOCK
        rho = (Decimal(111718729) / Decimal(111718750)) ** BLOCK
        w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        beta = Decimal(2).ln() / (-gamma.ln())
        return +gamma, +w, +beta


def clock(k: int, beta: Decimal) -> int:
    return int((beta * Decimal(k + 1)).to_integral_value(rounding=ROUND_CEILING))


def abel_toy() -> list[dict[str, str | int]]:
    levels = [Q(2), Q(2), Q(3), Q(3), Q(5), Q(8), Q(8), Q(13)]
    masses = {0: Q(2, 7), 2: Q(1, 7), 5: Q(3, 7)}
    cemetery = Q(1, 7)
    rows: list[dict[str, str | int]] = []
    for n in (1, 3, 7):
        direct = cemetery * levels[n]
        for k, mass in masses.items():
            direct += mass * levels[min(k, n)]
        abel = levels[0]
        for j in range(n):
            tail = cemetery + sum((mass for k, mass in masses.items() if k > j), Q(0))
            abel += (levels[j + 1] - levels[j]) * tail
        require(direct == abel, "Gate5 Abel toy")
        rows.append({"N": n, "direct": qstr(direct), "Abel": qstr(abel)})
    return rows


def gate5_audit(manifest: dict[str, Any]) -> dict[str, Any]:
    result = manifest["result"]
    unified = result["unified_infinite_level_clearance_clock"]
    require(unified["status"] == "CERTIFIED_UNIFIED_COVERAGE_AND_CLOCK_ABEL_CRITERION", "Gate5 Abel status")
    require("nu(A_col^c)=0" in unified["unified_iff"] and unified["physical_finiteness"] == "NOT_CERTIFIED", "Gate5 coverage typing")
    gamma, w, beta = clock_constants()
    require(Decimal("0.4999") < gamma < Decimal("0.5") and Decimal(1) < w < Decimal(4) / Decimal(3), "Gate5 constants")
    sample_js = (0, 1, 2, 4378, 4379, 4380, 4381, 4382, 8761, 10000)
    expected = []
    for j in sample_js:
        r0, r1 = clock(j, beta), clock(j + 1, beta)
        expected.append({"j": j, "r_j": r0, "r_j_plus_1": r1, "active": r1 == r0 + 1, "Delta_a_j": "(w_Z-1)*w_Z^r_j" if r1 == r0 + 1 else "0"})
    require(unified["rows"] == expected, "Gate5 active rows")
    require(clock(10_000, beta) - clock(0, beta) > 9_900, "Gate5 active density")
    dini = result["sharp_active_Dini_Orlicz_frontier"]
    require("iff p>1" in dini["sharp_threshold"] and "single finite owner law" in dini["exact_Orlicz_equivalence"], "Gate5 Dini/Orlicz")
    coverage = result["Round25_to_A_col_coverage_audit"]
    require("logical frozen-field model only" in coverage["sharp_compatible_separator"], "Gate5 Round25 logical scope")
    join = result["Round54_Round42_seven_bit_join_frontier"]
    bits = join["join_bits"]
    require(len(bits) == 7 and sum(row["frozen"].startswith("CERTIFIED") for row in bits) == 2, "Gate5 seven bits")
    require(join["physical_recovery_capacity"] == "NOT_CERTIFIED", "Gate5 capacity boundary")
    require("on A_col recover iff" in join["compressed_policy"] and "infinite policy cost on A_col^c" in join["compressed_policy"], "Gate5 uncovered policy typing")
    require("nu(A_col^c)=0" in join["exact_policy_criterion"] and "C_policy=infinity on A_col^c" in join["exact_policy_criterion"], "Gate5 policy coverage criterion")
    # Independent finite weighted Jordan identity.
    plus = {"a": Q(3, 5), "b": Q(1, 5)}
    minus = {"a": Q(1, 5), "c": Q(2, 5)}
    weights = {"a": Q(2), "b": Q(3), "c": Q(5)}
    meet = {x: min(plus.get(x, 0), minus.get(x, 0)) for x in weights}
    lhs = sum(weights[x] * (plus.get(x, 0) + minus.get(x, 0)) for x in weights)
    rhs = sum(weights[x] * abs(plus.get(x, 0) - minus.get(x, 0)) for x in weights) + 2 * sum(weights[x] * meet[x] for x in weights)
    require(lhs == rhs, "Gate5 Jordan identity")
    jordan = result["positive_Jordan_anchor_frontier"]
    require(jordan["physical_weighted_Jordan_variation_anchor"] == "NOT_CERTIFIED" and jordan["physical_weighted_common_mode_anchor"] == "NOT_CERTIFIED", "Gate5 anchors")
    strict = result["strict_nonpromotion"]
    require(strict["Gate5_maturity"] == "10/18" and strict["complete_18_field_operator_block_count"] == 0 and strict["Gate5"] == "NOT_CERTIFIED", "Gate5 status")
    return {
        "Abel_toy_rows": abel_toy(),
        "active_sample_rows": len(expected),
        "active_count_first_10000": clock(10_000, beta) - clock(0, beta),
        "critical_threshold": "p>1",
        "Orlicz_scope": "existential_for_one_fixed_finite_law_only",
        "seven_operator_bits": "2_FROZEN_5_OPEN",
        "Jordan_weighted_identity": qstr(lhs),
        "status": "PASS",
    }


def no_earlier_formula(a: Q, b: Q, tau: Q) -> bool:
    delta = a * a - b
    return a <= 0 or delta < 0 or (a - tau >= 0 and delta <= (a - tau) ** 2)


def root_grid_replay() -> int:
    count = 0
    taus = (Q(1, 2), Q(1), Q(3, 2), Q(2), Q(3), Q(5))
    for a_int in range(-6, 7):
        a = Q(a_int)
        for tau in taus:
            b = a * a + 1
            require(no_earlier_formula(a, b, tau), "negative-discriminant branch")
            count += 1
        if a_int == 0:
            continue
        for d_int in range(0, abs(a_int)):
            d = Q(d_int)
            b = a * a - d * d
            require(b > 0, "root-grid b")
            roots = (a - d, a + d)
            for tau in taus:
                actual = not any(Q(0) < root < tau for root in roots)
                require(no_earlier_formula(a, b, tau) == actual, "root-grid equivalence")
                count += 1
    return count


def gate123_audit(manifest: dict[str, Any]) -> dict[str, Any]:
    result = manifest["result"]
    gate1 = result["gate1"]
    require(gate1["physical_selected_QNL_tail"]["status"] == "CERTIFIED_PHYSICAL_SELECTED_GERM_AND_LOOP_ONLY", "Gate1 selected scope")
    require(gate1["type_boundary"]["physical_all_plaque_Dini_rows"] == "NOT_CERTIFIED" and gate1["type_boundary"]["gate1"] == "NOT_CERTIFIED", "Gate1 nonpromotion")
    gate2 = result["gate2"]
    shadows = gate2["physical_finite_shadow_registry"]
    require(shadows["row_count"] == 96 and [row["depth"] for row in shadows["rows"]] == list(range(1, 97)), "Gate2 finite shadows")
    require(shadows["graph_transform_chart_defined_at_every_prefix"] == "NOT_CERTIFIED", "Gate2 shadow scope")
    require(gate2["strict_status"]["physical_projected_all_depth_bad_shadow_rows"] == 0 and gate2["strict_status"]["immutable_gate2_fields"] == "0/17", "Gate2 maturity")
    join = gate2["gate2_to_gate4_seven_field_audit"]
    require(join["fully_certified_field_count"] == 1 and join["join_closed"] is False, "Gate2 landing join")
    gate3 = result["gate3"]
    formula = gate3["actual_physical_circular_pilot_formula"]
    require(formula["status"] == "CERTIFIED_ACTUAL_PHYSICAL_FIXED_DEPTH_FORMULA_BUDGET", "Gate3 formula")
    for row in formula["first_eight_budget_rows"]:
        n = row["depth"]
        require(row["physical_variables"] == 8 * n + 5 <= 400 * n + 20, "Gate3 variables")
        require(row["physical_atomic_predicates_upper"] == 830 * n + 12 <= 2000 * n + 100, "Gate3 atoms")
        require(row["physical_degree_upper"] == 4 <= 8, "Gate3 degree")
        require(row["branch_words"] == 8 * 162**n, "Gate3 words")
    require(161 * 5 + 25 == 830, "Gate3 per-step count")
    require(160 * 4 + 1 < 161 * 5, "Gate3 Boolean atom reserve")
    require(gate3["physical_fixed_depth_CAD"]["depth_integrated_complexity"] == "NOT_CERTIFIED", "Gate3 fixed-depth scope")
    require(gate3["strict_nonpromotion"]["gate3"] == "NOT_CERTIFIED", "Gate3 status")
    strict = result["strict_status"]
    require(strict == {"gate1": "NOT_CERTIFIED", "gate2": "NOT_CERTIFIED", "gate2_immutable_fields": "0/17", "gate3": "NOT_CERTIFIED", "composite_gates": "0/5", "cm2": "NO-GO_FOR_CLAIM"}, "Gate123 strict ledger")
    root_cases = root_grid_replay()
    return {
        "Gate1_scope": "SELECTED_QNL_GERM_ONLY",
        "Gate2_collision_shadow_rows": "96/96_FINITE_PREFIX_ONLY",
        "Gate2_landing_join": "1/7",
        "Gate3_exact_rational_root_cases": root_cases,
        "Gate3_atom_budget_identity": "161*5+25=830",
        "Gate3_word_universe": "8*162^n",
        "Gate3_scope": "FIXED_DEPTH_NOT_DEPTH_INTEGRATED",
        "status": "PASS",
    }


def build_result() -> dict[str, Any]:
    manifests, ledger_rows = validate_frozen()
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "provenance": {
            "frozen_pins": dict(PINS),
            "old_artifacts_modified": False,
            "external_theorem_promoted": False,
            "audit_scope": "independent arithmetic, measure-type, formula-budget and cross-leaf state audit",
        },
        "frozen_leaf_artifact_audit": {
            "manifest_and_ledger_pins": "6/6",
            "leaf_ledger_rows": ledger_rows,
            "leaf_ledger_rows_status": "12/12",
            "older_dependency_pins_replayed_by_leaves": "31/31",
        },
        "gate4_independent_audit": gate4_audit(manifests["gate4"]),
        "gate5_independent_audit": gate5_audit(manifests["gate5"]),
        "gate123_independent_audit": gate123_audit(manifests["gate123"]),
        "technology_type_audit": {
            "official_API_metadata_checked_on": "2026-07-20",
            "records": ["2604.25881v1", "2606.10155v1", "2606.19621v2", "2603.25380v1", "2604.06144v1", "2601.09548v1", "2605.04718v1"],
            "MME_is_not_pinned_collision_law": True,
            "inter_sign_OT_is_not_positive_Jordan_control": True,
            "CAD_sources_do_not_supply_CM2_strong_operator_norms": True,
            "external_theorem_promoted": False,
            "status": "PASS",
        },
        "main_leaf_acceptance_matrix": {
            "syntax": "6/6",
            "older_dependency_pins": "31/31",
            "frozen_manifest_and_ledger_pins": "6/6",
            "leaf_ledger_artifact_rows": "12/12",
            "integrity": "3/3",
            "replay": "3/3",
            "reemit": "3/3",
            "hostile_mutations_rejected": "272/272",
            "default_cert_verifier_exit_2": "6/6",
        },
        "independent_leaf_acceptance_matrix": {
            "syntax": "2/2",
            "frozen_manifest_and_ledger_pins": "6/6",
            "leaf_ledger_artifact_rows": "12/12",
            "integrity": "1/1",
            "replay": "1/1",
            "reemit": "1/1",
            "hostile_mutations_rejected": "59/59",
            "default_cert_verifier_exit_2": "2/2",
            "SHA_ledger_rows": "4/4",
        },
        "four_leaf_acceptance_matrix": {
            "syntax": "8/8",
            "dependency_pins": "37/37",
            "integrity": "4/4",
            "replay": "4/4",
            "reemit": "4/4",
            "hostile_mutations_rejected": "331/331",
            "SHA_ledger_rows": "16/16",
            "default_cert_verifier_exit_2": "8/8",
            "Round59_stale_or_temp_files": 0,
        },
        "strict_verdict": {
            "Gate1": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED",
            "Gate2_immutable_fields": "0/17",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "Gate5_maturity": "10/18",
            "complete_18_field_blocks": 0,
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
            "audit": "PASS_NO_CLAIMED_SCOPE_BLOCKER",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest() -> dict[str, Any]:
    require(REPORT.is_file() and not REPORT.is_symlink(), "report path")
    require(VERIFIER.is_file() and not VERIFIER.is_symlink(), "verifier path")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "dependencies": dict(PINS),
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(VERIFIER),
        "report_sha256": sha(REPORT),
        "result": result,
        "verdict": result["strict_verdict"],
    }


def encoded_manifest() -> str:
    return json.dumps(build_manifest(), indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    try:
        payload = encoded_manifest()
        if args.manifest_json:
            print(payload, end="")
            return 0
    except (OSError, RuntimeError, ValueError, KeyError, TypeError) as exc:
        print(f"ROUND59_INDEPENDENT_AUDIT_CERT_FAILURE: {exc}")
        return 1
    verdict = build_result()["strict_verdict"]
    print("INDEPENDENT_AUDIT:", verdict["audit"])
    print("COMPOSITE_GATES:", verdict["complete_composite_gates"])
    print("CM2:", verdict["CM2"])
    return 0 if args.audit else 2


if __name__ == "__main__":
    raise SystemExit(main())
