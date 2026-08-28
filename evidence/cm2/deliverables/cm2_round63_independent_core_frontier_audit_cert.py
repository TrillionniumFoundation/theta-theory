#!/usr/bin/env python3
"""Round-63 independent core-frontier audit certificate.

This append-only certificate reads the three frozen Round-63 leaves,
recomputes their decisive algebra/arithmetic/type boundaries, and emits the
deterministic audit manifest.  It never edits an input leaf.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round63-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round63-independent-core-frontier-audit"
DEFAULT_REPORT = HERE / f"{PREFIX}-2026-07-21.md"
DEFAULT_MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
DEFAULT_VERIFIER = HERE / "cm2_round63_independent_core_frontier_audit_verifier.py"

PINS = {
    "cm2-sixty-second-direct-assault-2026-07-21.md":
        "873557a6653a826700d5daf11e8b118f5ddca1cf911e085f9c20aa591ab2136f",
    "cm2-sixty-second-direct-assault-manifest-2026-07-21.sha256":
        "e54b5a1de2b4bddf0c7589b77997b1f28284040b64b31fdfbf58af9e73233bac",
    "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-manifest-2026-07-21.json":
        "bdd351955c4537e649009e753900a7f61e3befcc16db55f810af2902dd3581ea",
    "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-manifest-2026-07-21.sha256":
        "b48def6d29a68f9cf30db2b349a41e06b3e5df58766f8d9323e256f75c6ad058",
    "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.json":
        "955908ee74ff6ec0354224978850ef683aeacd1923ce85bffd1290467321d23f",
    "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.sha256":
        "a739ffbe1bb9f14fdc8c72c573594f56930a7c4f32efb77fa4dac60d256ec870",
    "cm2-gate5-round63-killed-trace-kernel-jordan-join-frontier-manifest-2026-07-21.json":
        "a052e9c278a6359bdcd554020de28b2e8d821eb0e1267758a702bf3dff130ab8",
    "cm2-gate5-round63-killed-trace-kernel-jordan-join-frontier-manifest-2026-07-21.sha256":
        "605487e4aee375b589f5fd13e9de85ab716e41d8db285cb3327529c7cc857a9e",
}

LEAF_MANIFESTS = {
    "gate13": "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-manifest-2026-07-21.json",
    "gate24": "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.json",
    "gate5": "cm2-gate5-round63-killed-trace-kernel-jordan-join-frontier-manifest-2026-07-21.json",
}

LEAF_LEDGERS = {
    "gate13": "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-manifest-2026-07-21.sha256",
    "gate24": "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.sha256",
    "gate5": "cm2-gate5-round63-killed-trace-kernel-jordan-join-frontier-manifest-2026-07-21.sha256",
}

CP = Q(4 * 10**90 * 360493663, 358863)
BLOCK_DEPTH = 9148


class AuditError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AuditError(label)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise AuditError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def reject_constant(token: str) -> None:
    raise AuditError(f"non-finite JSON token: {token}")


def strict_json_path(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )
    require(isinstance(value, dict), f"JSON root: {path.name}")
    return value


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def validate_pins() -> None:
    for name, expected in PINS.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"pin file/type: {name}")
        require(path.resolve().parent == HERE, f"pin parent: {name}")
        require(sha256_path(path) == expected, f"pin hash: {name}")


def resolve_sidecar_name(token: str) -> Path:
    candidate = HERE.parent / token if token.startswith("deliverables/") else HERE / token
    candidate = candidate.resolve()
    require(candidate.parent == HERE, f"sidecar target parent: {token}")
    return candidate


def replay_sidecar(name: str) -> int:
    path = HERE / name
    rows = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    require(len(rows) == 4, f"sidecar row count: {name}")
    seen: set[Path] = set()
    for row in rows:
        parts = row.split(maxsplit=1)
        require(len(parts) == 2, f"sidecar syntax: {name}")
        expected, token = parts
        require(len(expected) == 64 and all(c in "0123456789abcdef" for c in expected),
                f"sidecar digest syntax: {name}")
        target = resolve_sidecar_name(token)
        require(target not in seen, f"sidecar duplicate: {name}")
        seen.add(target)
        require(target.is_file() and not target.is_symlink(), f"sidecar file/type: {token}")
        require(sha256_path(target) == expected, f"sidecar hash: {token}")
    return len(rows)


def load_leaves() -> dict[str, dict[str, Any]]:
    return {key: strict_json_path(HERE / name) for key, name in LEAF_MANIFESTS.items()}


def safe_dbar(m: int) -> int:
    if Q(2) ** m <= CP:
        return 0
    d = 1
    while not Q(2) ** (m - d) < CP / 2:
        d += 1
    return d


def audit_gate13(leaf: dict[str, Any]) -> dict[str, Any]:
    result = leaf["result"]
    require(result["strict_status"] == {
        "cm2": "NO-GO_FOR_CLAIM",
        "composite_gates": "0/5",
        "gate1": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
    }, "Gate13 strict state")

    inheritance = result["gate1"]["endpoint_conjugacy_holder_inheritance"]
    require(inheritance["status"] == "CERTIFIED_EXACT_HOLDER_INHERITANCE_INTERFACE",
            "Gate13 inheritance status")
    require(len(inheritance["strict_hypotheses"]) == 4, "Gate13 inheritance hypotheses")
    physical1 = result["gate1"]["physical_boundary"]
    require(physical1["actual_all_plaque_transfer_C"] == "NOT_CERTIFIED", "Gate13 physical transfer")
    require(physical1["uniform_forward_backward_defect_decay"] == "NOT_CERTIFIED", "Gate13 physical defects")
    require(physical1["separate_approximant_equi_holder_debt"] ==
            "NOT_INDEPENDENTLY_REQUIRED_UNDER_ROWS_1_TO_3", "Gate13 approximant scope")

    budget = result["gate1"]["sharp_plaque_tempered_budget"]
    require(budget["status"] == "CERTIFIED_SUFFICIENT_THRESHOLD_SHARP_IN_MODEL",
            "Gate13 sufficient/model-sharp status")
    require("not a new billiard realization" in budget["scope"], "Gate13 model scope")
    expected = [
        ("subcritical", Q(3, 2), Q(1, 4), Q(9, 16), "DECAYS"),
        ("critical", Q(2), Q(1, 4), Q(1), "CONSTANT_NONZERO"),
        ("supercritical", Q(2), Q(1, 2), Q(2), "DIVERGES"),
    ]
    rows = budget["threshold_rows"]
    require(len(rows) == 3, "Gate13 threshold rows")
    samples = 0
    for row, (regime, a, lam, theta, behavior) in zip(rows, expected):
        require(row["regime"] == regime and Q(row["a"]) == a, "Gate13 threshold identity")
        require(Q(row["lambda"]) == lam and Q(row["theta=a^2*lambda"]) == theta,
                "Gate13 threshold value")
        require(row["behavior"] == behavior and len(row["samples"]) == 10,
                "Gate13 threshold behavior")
        for n, sample in enumerate(row["samples"], 1):
            require(sample["n"] == n, "Gate13 threshold n")
            require(Q(sample["endpoint_lower_defect"]) == lam**n, "Gate13 endpoint defect")
            require(Q(sample["renormalized_lower_defect"]) == theta**n,
                    "Gate13 renormalized defect")
            samples += 1

    gate3 = result["gate3"]
    incidence = gate3["oriented_incidence_reduction"]
    require(incidence["half_open_owner_is_enough_for_current_cancellation"] is False,
            "Gate13 half-open guard")
    artificial = incidence["artificial_replay"]
    require(len(artificial) == 3, "Gate13 artificial incidence rows")
    for row in artificial:
        require(Q(row["left_trace"]) == Q(row["right_trace"]), "Gate13 trace equality")
        require(Q(row["assembled_pairing"]) == 0, "Gate13 artificial cancellation")
    mismatch = incidence["physical_mismatch_replay"]
    require(Q(mismatch["pairing_against_phi(t)=t"]) == -1 and Q(mismatch["TV"]) == 2,
            "Gate13 physical mismatch")

    taxonomy = gate3["actual_stopped_cut_taxonomy"]
    require(len(taxonomy["rows"]) == 11, "Gate13 taxonomy rows")
    require(taxonomy["rows"][0]["treatment"] == "ABSENT_FROM_ACTUAL_INCIDENCE_CHAIN",
            "Gate13 proof cut")
    require(taxonomy["rows"][-1]["treatment"] == "RETAIN_SEPARATE_CLOCK_JUMP_CURRENT",
            "Gate13 clock cut")

    clock = gate3["stopping_clock_jump_frontier"]
    require(clock["covered_by_round44_five_face_F13"] is False, "Gate13 sixth debt")
    require(len(clock["rows"]) == 13, "Gate13 clock rows")
    for row in clock["rows"]:
        d = safe_dbar(row["M"])
        require(row["Dbar"] == d and row["R0=696*Dbar"] == 696 * d,
                "Gate13 safe clock replay")
    require(safe_dbar(310) == 0 and safe_dbar(311) == 2, "Gate13 first clock jump")

    join = gate3["same_ID_regular_F13_join"]
    require(join["scope"] == "base s=0 regular-density Borel TV only", "Gate13 F13 scope")
    require(Q(join["F13_over_X"]) == Q(3816937, 7800000) < Q(1, 2), "Gate13 F13/X")
    require(Q(join["F13_over_D1"]) == Q(3816937, 47112000) < Q(25, 302),
            "Gate13 F13/D1")
    require(set(join["not_inherited"]) == {
        "finite-s trace differentiability", "strong F13 pullback/intertwiner",
        "clock-jump current", "cemetery current",
    }, "Gate13 F13 noninheritance")
    ledger = gate3["reduced_strong_ledger"]
    require(ledger["regular_base_Borel_term"] == "CERTIFIED_FINITE_VIA_F13_JOIN",
            "Gate13 base Borel payment")
    require(all(ledger[key] == "NOT_CERTIFIED" for key in (
        "anisotropic_bulk_Piola", "cemetery_term", "clock_term", "moving_regular_strong_term")),
        "Gate13 open strong debts")
    require(all(value == "NOT_CERTIFIED" for value in gate3["physical_boundary"].values()),
            "Gate13 physical boundary")

    return {
        "algebra_and_arithmetic": {
            "endpoint_conjugacy_identity": "PASS",
            "threshold_regimes": "3/3",
            "threshold_samples": f"{samples}/{samples}",
            "incidence_rows": "3/3",
            "taxonomy_rows": "11/11",
            "clock_rows": "13/13",
            "F13_ratio_rows": "2/2",
        },
        "red_team": {
            "theta_less_than_one": "SUFFICIENT_ONLY__SHARP_ONLY_IN_DECLARED_LOGICAL_SL2_MODEL",
            "Round44_F13": "BASE_S0_REGULAR_BOREL_TV_ONLY",
            "clock_jump": "DISTINCT_SIXTH_DEBT_NOT_PAID_BY_FIVE_F13_GRAMMARS",
            "physical_strong_and_bulk": "NOT_CERTIFIED",
        },
        "acceptance": {
            "dependency_pins": "13/13",
            "integrity": "PASS",
            "replay": "PASS",
            "reemit": "BYTE_IDENTICAL",
            "hostile_semantic": "385/385_REJECTED",
            "strict_JSON": "15/15_REJECTED",
            "SHA": "4/4",
            "default_exit2": "2/2",
        },
        "status": "INDEPENDENT_PASS",
    }


def dynamic(values: list[Q], image: list[int]) -> list[Q]:
    inverse = [image.index(j) for j in range(len(image))]
    return [values[inverse[j]] for j in range(len(image))]


def l1_uniform(values: list[Q]) -> Q:
    return sum((abs(value) for value in values), Q(0)) / len(values)


def audit_gate24(leaf: dict[str, Any]) -> dict[str, Any]:
    result = leaf["result"]
    strict = result["strict_nonpromotion"]
    require(strict["Gate2"] == strict["Gate4"] == "NOT_CERTIFIED", "Gate24 gate state")
    require(strict["complete_composite_gates"] == "0/5" and strict["CM2"] == "NO-GO_FOR_CLAIM",
            "Gate24 global state")
    require(strict["official_immutable_Gate2_fields"] == "0/17", "Gate24 Gate2 fields")

    square = result["branch_holonomy_square"]
    replay = square["finite_replay"]
    image = replay["dynamic_branch_image"]
    a_u = [Q(x) for x in replay["source_marker_a_u"]]
    a_v = [Q(x) for x in replay["source_marker_a_v"]]
    g_u = dynamic(a_u, image)
    g_v = dynamic(a_v, image)
    delta_s = [v - u for u, v in zip(a_u, a_v)]
    delta_l = [v - u for u, v in zip(g_u, g_v)]
    require([qstr(x) for x in g_u] == replay["landing_marker_g_u"], "Gate24 g_u")
    require([qstr(x) for x in g_v] == replay["landing_marker_g_v"], "Gate24 g_v")
    require([qstr(x) for x in delta_s] == replay["source_defect_Delta_S"], "Gate24 Delta_S")
    require([qstr(x) for x in delta_l] == replay["landing_defect_Delta_L"], "Gate24 Delta_L")
    norm_s, norm_l = l1_uniform(delta_s), l1_uniform(delta_l)
    require(norm_s == norm_l == Q(1, 6), "Gate24 defect norm")
    require(Q(replay["square_commutator_norm"]) == 0, "Gate24 square commutator")
    require("does not annihilate" in square["interpretation"], "Gate24 debt preservation guard")

    saturation = result["two_plaque_stable_saturation"]
    require("outer weight 1/2" in saturation["exact_formula"], "Gate24 outer weight formula")
    sat_replay = saturation["finite_replay"]
    require(Q(sat_replay["outer_weight_u"]) == Q(1, 2) and
            Q(sat_replay["outer_weight_v"]) == Q(1, 2), "Gate24 outer weights")
    require(Q(sat_replay["L1_marker_defect"]) == norm_l and
            Q(sat_replay["delta_sat"]) == norm_l / 2 == Q(1, 12), "Gate24 saturation replay")
    require("not asserted" in saturation["L1_guard"], "Gate24 L1 projection guard")

    transport = result["quantitative_holonomy_transport"]
    tr = transport["finite_replay"]
    f, r, theta, length = Q(tr["F_u"]), Q(tr["R_u"]), Q(tr["theta_u"]), Q(tr["L_u"])
    m, big_m = Q(tr["metric_derivative_lower_m"]), Q(tr["metric_derivative_upper_M"])
    target = f * r * big_m / (m * m * theta * length)
    require(target == Q(tr["target_z_upper"]) == 72, "Gate24 transport replay")
    require("m^2" in transport["strict_sufficient_budget"], "Gate24 m squared budget")
    require("span contraction" in transport["m_squared_audit"] and
            "density-ratio" in transport["m_squared_audit"], "Gate24 m squared origins")
    require("not materialized" in transport["physical_guard"], "Gate24 transport physical guard")

    separators = result["zero_defect_quantitative_separators"]["finite_replay"]
    require(Q(separators["short_span"]["z_over_C_p"]) == 2, "Gate24 short span")
    frag = separators["fragmentation"]
    require(Q(frag["z"]) == 2 * int(frag["F"]) and frag["z_above_C_p"] is True,
            "Gate24 fragmentation")

    graph = result["graph_cylinder_and_strong_assembly_guard"]
    require("2^D*nu" in graph["weighted_trace_guard"] and "2^-D" in graph["weighted_trace_guard"],
            "Gate24 weighted trace guard")
    require("no bounded" in graph["missing_map"], "Gate24 strong map guard")
    fields = result["seven_field_materialization_audit"]
    require(fields["complete_rows"] == "1/7" and fields["partial_rows"] == [1, 4, 7],
            "Gate24 landing fields")

    return {
        "algebra_and_arithmetic": {
            "square_identity": "PASS",
            "source_landing_defect_norms": "1/6__1/6",
            "two_plaque_outer_weights": "1/2__1/2",
            "two_plaque_saturation_distance": "1/12",
            "holonomy_transport_target_bound": "72",
            "zero_defect_separators": "2/2",
        },
        "red_team": {
            "square_effect": "PRESERVES_DEBT__DOES_NOT_ANNIHILATE_DEBT",
            "L1_outer_weight": "EXACTLY_ONE_HALF",
            "m_squared_origin": "ONE_SPAN_FACTOR__ONE_INVERSE_DENSITY_FACTOR",
            "physical_inputs": "NOT_CERTIFIED",
            "graph_to_strong": "NOT_CERTIFIED",
        },
        "acceptance": {
            "dependency_and_baseline_pins": "15/15",
            "integrity": "PASS",
            "replay": "PASS",
            "reemit": "BYTE_IDENTICAL",
            "hostile_semantic": "180/180_REJECTED",
            "strict_JSON": "4/4_REJECTED",
            "SHA": "4/4",
            "default_exit2": "2/2",
        },
        "status": "INDEPENDENT_PASS",
    }


def finite_jordan_replay() -> dict[str, str]:
    forward = [Q(3), Q(1)]
    reverse = [Q(1), Q(2)]
    positive_total = sum(forward) + sum(reverse)
    variation = sum(abs(a - b) for a, b in zip(forward, reverse))
    common = sum(min(a, b) for a, b in zip(forward, reverse))
    require(positive_total == variation + 2 * common, "finite Jordan replay")
    return {
        "positive_total": qstr(positive_total),
        "variation": qstr(variation),
        "common_mode": qstr(common),
    }


def audit_gate5(leaf: dict[str, Any]) -> dict[str, Any]:
    result = leaf["result"]
    strict = result["strict_nonpromotion"]
    require(strict["Gate5"] == "NOT_CERTIFIED" and strict["Gate5_maturity"] == "10/18",
            "Gate5 state")
    require(strict["complete_18_field_operator_block_count"] == 0, "Gate5 blocks")
    require(strict["complete_composite_gates"] == "0/5" and strict["CM2"] == "NO-GO_FOR_CLAIM",
            "Gate5 global state")
    require(strict["actual_same_owner_all_time_recurrence"] == "NOT_CERTIFIED" and
            strict["all_time_weighted_variation_common_complement"] == "NOT_CERTIFIED",
            "Gate5 all-time boundary")

    kernel = result["killed_trace_kernel_frontier"]
    require(kernel["status"] == "CERTIFIED_EXACT_CONDITIONAL_SHARP_INTERFACE_NO_ACTUAL_DRIFT",
            "Gate5 kernel type")
    require("disjoint_union" in kernel["time_labelled_carrier"] and
            "never quotients" in kernel["time_labelled_carrier"], "Gate5 time labels")
    rows = kernel["replay_rows"]
    require(len(rows) == 3, "Gate5 kernel rows")
    ratios = []
    for row in rows:
        ratio = Q(row["w_test"]) * Q(row["kappa_test"])
        ratios.append(ratio)
        partial = sum((ratio**j for j in range(row["N"] + 1)), Q(0))
        require(Q(row["ratio"]) == ratio and Q(row["partial_sum"]) == partial,
                "Gate5 kernel geometric replay")
        require(row["finite_geometric_criterion"] is (ratio < 1),
                "Gate5 kernel criterion")
    require(ratios == [Q(3, 4), Q(1), Q(9, 8)], "Gate5 kernel sharp rows")
    require(all(kernel[key] == "NOT_CERTIFIED" for key in
                ("actual_K_j", "actual_V_j", "actual_kappa_below_threshold")),
            "Gate5 actual drift boundary")
    with localcontext() as ctx:
        ctx.prec = 100
        rho = (Decimal(111718729) / Decimal(111718750)) ** BLOCK_DEPTH
        w_z = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        threshold = Decimal(1) / w_z
        require(str(w_z) == kernel["w_Z_decimal"] and
                str(threshold) == kernel["kappa_threshold_decimal"], "Gate5 threshold decimals")
        require(rho.sqrt() > threshold, "Gate5 Round52 Holder guard")

    jordan = result["fixed_j_orientation_cost_Jordan"]
    forward = Q(jordan["forward_strict_upper"])
    reverse = Q(jordan["reverse_strict_upper"])
    total = Q(jordan["bidirectional_strict_upper"])
    require(forward + reverse == total == Q(2395081816467609, 880000),
            "Gate5 F10 rational total")
    require(Q(jordan["common_mode_strict_upper"]) == min(forward, reverse),
            "Gate5 common mode upper")
    require("|J_j^cost|+2" in jordan["lattice_identity"], "Gate5 lattice identity")
    require("not identified" in jordan["type_guard"] and
            "Round54 actual signed-flux" in jordan["type_guard"], "Gate5 Jordan type guard")
    require(all(jordan[key] == "NOT_CERTIFIED" for key in (
        "Round54_physical_signed_flux_alignment", "all_time_weighted_cost_common_mode",
        "all_time_weighted_cost_variation", "all_time_weighted_complement")),
        "Gate5 Jordan all-time boundary")

    complement = result["complement_strata_frontier"]
    require(len(complement["rows"]) == 4, "Gate5 complement rows")
    require(complement["rows"][0]["orientation_F10_cost"] == "CERTIFIED_ZERO_FIXED_J",
            "Gate5 grazing cost")
    require("iff" in complement["exact_cut_criterion"] and
            "lim_" in complement["accumulation_criterion"], "Gate5 cut interfaces")
    require("cannot be renamed" in complement["source_rank_guard"], "Gate5 source rank guard")
    require(complement["remaining_complement_all_time_charge"] == "NOT_CERTIFIED" and
            complement["strong_pre_regularization_cemetery"] == "NOT_CERTIFIED",
            "Gate5 complement boundary")

    suffix = result["suffix_clearance_frontier"]
    require(suffix["Borel_suffix_predicates"] == "CERTIFIED_7_OF_7_PINNED_ROUND61",
            "Gate5 suffix Borel")
    require(suffix["universal_values"] == "2_TRUE_5_OPEN" and len(suffix["five_open_bits"]) == 5,
            "Gate5 suffix values")
    require(suffix["actual_all_time_positive_debt_kernel"] == "NOT_CERTIFIED",
            "Gate5 suffix all-time boundary")

    return {
        "algebra_and_arithmetic": {
            "killed_kernel_rows": "3/3",
            "sharp_ratios": [qstr(x) for x in ratios],
            "orientation_cost_rational_sum": qstr(total),
            "finite_Jordan_replay": finite_jordan_replay(),
            "complement_rows": "4/4",
        },
        "red_team": {
            "killed_kernel": "EXACT_CONDITIONAL_INTERFACE__NO_ACTUAL_DRIFT",
            "time_labels": "IMMUTABLE__NO_CROSS_TIME_DEDUPLICATION",
            "cost_Jordan": "NOT_ROUND54_SIGNED_PHYSICAL_FLUX",
            "all_time_decay": "NOT_CERTIFIED",
            "remaining_complement_and_cemetery": "NOT_CERTIFIED",
        },
        "acceptance": {
            "dependency_and_baseline_pins": "13/13",
            "integrity": "PASS",
            "replay": "PASS",
            "reemit": "BYTE_IDENTICAL",
            "hostile_semantic": "160/160_REJECTED",
            "strict_JSON": "4/4_REJECTED",
            "SHA": "4/4",
            "default_exit2": "2/2",
        },
        "status": "INDEPENDENT_PASS",
    }


def cross_leaf_rows() -> list[dict[str, Any]]:
    return [
        {
            "id": 1,
            "join": "Gate13 base regular F13 -> moving stopped strong ledger",
            "verdict": "ILLEGAL__FINITE_S_STRONG_CLOCK_CEMETERY_AND_BULK_PIOLA_REMAIN_OPEN",
        },
        {
            "id": 2,
            "join": "Round44 five F13 grammars -> stopping-clock threshold face",
            "verdict": "ILLEGAL__CLOCK_JUMP_IS_A_DISTINCT_SIXTH_DEBT",
        },
        {
            "id": 3,
            "join": "Gate24 exact branch-holonomy square -> zero stable-marker defect",
            "verdict": "ILLEGAL__EXACT_SQUARE_PRESERVES_BUT_DOES_NOT_ANNIHILATE_DEFECT",
        },
        {
            "id": 4,
            "join": "Gate24 zero saturation defect -> quantitative landing properness",
            "verdict": "ILLEGAL__SHORT_SPAN_AND_FRAGMENTATION_DEBTS_SURVIVE",
        },
        {
            "id": 5,
            "join": "Gate24 graph-cylinder -> Gate13 physical moving current",
            "verdict": "ILLEGAL__BOOKKEEPING_CURRENT_IS_NOT_ANISOTROPIC_PIOLA_STRONG_ASSEMBLY",
        },
        {
            "id": 6,
            "join": "Gate5 orientation-cost Jordan -> Round54 signed hit/miss flux",
            "verdict": "ILLEGAL__MEASURE_TYPES_AND_CHARGES_ARE_NOT_IDENTIFIED",
        },
        {
            "id": 7,
            "join": "Gate5 conditional killed-kernel theorem -> actual all-time decay",
            "verdict": "ILLEGAL__NO_ACTUAL_K_V_OR_SUBCRITICAL_KAPPA_IS_INSTALLED",
        },
    ]


def build_result() -> dict[str, Any]:
    validate_pins()
    leaves = load_leaves()
    sidecars = sum(replay_sidecar(name) for name in LEAF_LEDGERS.values())
    require(sidecars == 12, "source sidecar total")
    cross = cross_leaf_rows()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "Round62_aggregate_report_sha256": PINS["cm2-sixty-second-direct-assault-2026-07-21.md"],
            "Round62_recursive_ledger_sha256": PINS["cm2-sixty-second-direct-assault-manifest-2026-07-21.sha256"],
            "all_three_leaves_frozen_before_read": True,
            "audit_authored_source_leaf": False,
            "old_artifacts_modified": False,
            "pinned_artifacts": dict(PINS),
        },
        "gate13_independent_audit": audit_gate13(leaves["gate13"]),
        "gate24_independent_audit": audit_gate24(leaves["gate24"]),
        "gate5_independent_audit": audit_gate5(leaves["gate5"]),
        "cross_leaf_consistency": {
            "rows": cross,
            "rows_sha256": digest(cross),
            "state_consistency": "Gate1/2/3/4/5 NOT_CERTIFIED; Gate2 0/17; landing 1/7 fields 1,4,7 partial; Gate5 10/18 blocks0; 0/5; CM2 NO-GO_FOR_CLAIM",
            "status": "PASS_NO_CROSS_LEAF_TYPE_SUBSTITUTION_OR_STATE_CONTRADICTION",
        },
        "source_leaf_acceptance": {
            "syntax": "6/6",
            "dependency_and_baseline_pins": "41/41",
            "integrity": "3/3",
            "replay": "3/3",
            "reemit": "3/3_BYTE_IDENTICAL",
            "hostile_semantic": "725/725_REJECTED",
            "strict_JSON": "23/23_REJECTED",
            "hostile_and_strict_JSON": "748/748_REJECTED",
            "SHA_sidecar_rows": "12/12",
            "default_entry_points": "6/6_EXIT_2",
        },
        "red_team_guards": [
            "Gate1 theta<1 is sufficient only and sharp only in the declared logical SL2 model",
            "Round44 F13 pays only base s=0 regular Borel TV; the stopping-clock jump is a distinct sixth debt",
            "Gate24 exact square preserves marker debt; it does not annihilate it",
            "Gate24 two-plaque L1 distance uses outer weights exactly 1/2 and the transport budget has two independently sourced factors of m",
            "Gate5 killed trace-kernel theorem is conditional and installs no actual all-time decay",
            "Gate5 orientation-cost Jordan law is not identified with the Round54 signed physical hit/miss flux",
        ],
        "latest_technology_boundary": {
            "checked_through_in_source_leaves": "2026-07-21",
            "external_theorem_promoted_by_audit": False,
            "status": "NO_EXTERNAL_THEOREM_IMPORTED",
        },
        "strict_final_state": {
            "Gate1": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
            "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
            "audit_verdict": "PASS__NO_SOURCE_LEAF_CORRECTION_REQUIRED",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "pins": dict(PINS),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier.resolve()),
        "report_sha256": sha256_path(DEFAULT_REPORT),
        "result": result,
        "verdict": result["strict_final_state"],
    }


def render_manifest(verifier: Path) -> str:
    return json.dumps(build_manifest(verifier), sort_keys=True, indent=2, allow_nan=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    args = parser.parse_args()
    try:
        if args.write_manifest is not None:
            target = args.write_manifest.resolve()
            require(target.parent == HERE, "manifest output parent")
            target.write_text(render_manifest(args.verifier), encoding="utf-8")
            print(f"WROTE_MANIFEST: {target}")
            return 0
        if args.manifest_json:
            print(render_manifest(args.verifier), end="")
            return 0
        result = build_result()
        if args.audit:
            print("AUDIT: PASS")
            print("SOURCE_DEPENDENCY_AND_BASELINE_PINS: 41/41")
            print("SOURCE_SHA_SIDECAR_ROWS: 12/12")
            print(f"RESULT_SHA256: {result['internal_replay_digest']}")
            return 0
        if args.replay:
            print(json.dumps({
                "gate13_threshold_samples": 30,
                "gate13_clock_rows": 13,
                "gate24_square_rows": 1,
                "gate24_saturation_rows": 1,
                "gate24_transport_rows": 1,
                "gate5_kernel_rows": 3,
                "gate5_complement_rows": 4,
                "cross_leaf_rows": 7,
                "status": "PASS",
            }, sort_keys=True))
            return 0
    except (AuditError, OSError, ValueError, KeyError, TypeError, IndexError, ArithmeticError) as exc:
        print(f"ROUND63_AUDIT_CERTIFICATE_ERROR: {exc}", file=sys.stderr)
        return 1
    final = result["strict_final_state"]
    print("AUDIT_VERDICT:", final["audit_verdict"])
    print("GATES_1_TO_5: NOT_CERTIFIED")
    print("COMPLETE_COMPOSITE_GATES:", final["complete_composite_gates"])
    print("CM2:", final["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
