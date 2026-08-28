#!/usr/bin/env python3
"""Independent verifier for the CM2 Round-60 Gate-1/2/3 frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / "deliverables"
CERT = HERE / (
    "cm2_gate123_round60_combined_gauge_stable_strong_operator_"
    "frontier_cert.py"
)
VERIFIER = Path(__file__).resolve()
REPORT = HERE / (
    "cm2-gate123-round60-combined-gauge-stable-strong-operator-"
    "frontier-assault-2026-07-20.md"
)
MANIFEST = HERE / (
    "cm2-gate123-round60-combined-gauge-stable-strong-operator-"
    "frontier-manifest-2026-07-20.json"
)
Q = Fraction


RESULT_DIGEST = "765cec614cf2a016876b3f1f16f9a5e8afe7a4128405f4260a3794535038f748"

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


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def reject_constant(value: str) -> None:
    raise VerificationError(f"non-finite JSON constant: {value}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_manifest(path: Path = MANIFEST) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "manifest file/type")
    try:
        data = json.loads(
            path.read_text(),
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise VerificationError(f"manifest parse: {exc}") from exc
    require(isinstance(data, dict), "manifest root object")
    return data


def no_earlier_root(a: Q, b: Q, tau: Q) -> bool:
    require(b > 0 and tau > 0, "root domain")
    delta = a * a - b
    return a <= 0 or delta < 0 or (
        a - tau >= 0 and delta <= (a - tau) ** 2
    )


def direct_earlier_root(a: Q, b: Q, tau: Q) -> bool:
    require(b > 0 and tau > 0, "direct root domain")
    delta = a * a - b
    if a <= 0 or delta < 0:
        return False
    if tau > a:
        return True
    return delta > (a - tau) ** 2


def independent_root_grid() -> dict[str, int | str]:
    rows: list[list[str | bool]] = []
    no_count = 0
    for ai in range(-6, 11):
        a = Q(ai, 2)
        for bi in range(1, 25):
            b = Q(bi, 4)
            for ti in range(1, 9):
                tau = Q(ti, 2)
                no_root = no_earlier_root(a, b, tau)
                has_root = direct_earlier_root(a, b, tau)
                require(no_root == (not has_root), "root grid complement")
                no_count += int(no_root)
                rows.append([str(a), str(b), str(tau), no_root])
    return {
        "grid_cases": len(rows),
        "no_earlier_true_cases": no_count,
        "earlier_root_true_cases": len(rows) - no_count,
        "grid_sha256": canonical_digest(rows),
    }


def validate_gate1(gate1: dict[str, Any]) -> None:
    require(set(gate1) == {
        "compact_to_combined_twisting_budget",
        "selected_to_all_plaque_separator",
        "unbounded_gauge_separator",
        "minimal_physical_interface",
    }, "Gate1 keys")
    budget = gate1["compact_to_combined_twisting_budget"]
    error = Q(budget["frozen_compact_loop_error_strict_upper"])
    wedge = Q(budget["frozen_smallest_wedge_strict_lower"])
    exact = Q(budget["exact_K_gauge_strict_upper"])
    require(error == Q(8568, 10**52), "Gate1 compact error")
    require(wedge == Q(17344, 10**32), "Gate1 wedge")
    require(exact == wedge / error == Q(216800000000000000000000, 1071),
            "Gate1 exact gauge budget")
    require(exact > 2 * 10**20, "Gate1 gauge magnitude")
    require(budget["physical_K_gauge"] == "NOT_CERTIFIED", "Gate1 K no-promotion")

    separator = gate1["selected_to_all_plaque_separator"]
    require(Q(separator["selected_exact_sum"]) == Q(100, 81),
            "Gate1 selected sum")
    require(Q(1) / (1 - Q(1, 10)) ** 2 == Q(100, 81),
            "Gate1 independent geometric-log sum")
    rows = separator["harmonic_dyadic_rows"]
    require(len(rows) == 10, "Gate1 harmonic row count")
    for power, row in enumerate(rows, 1):
        count = 2**power
        partial = sum((Q(1, n + 1) for n in range(count)), Q(0))
        require(row["power"] == power and row["terms"] == count,
                "Gate1 harmonic row index")
        require(Q(row["partial_sum"]) == partial, "Gate1 harmonic partial")
        require(partial >= 1 + Q(power, 2), "Gate1 harmonic lower bound")

    gauge = gate1["unbounded_gauge_separator"]
    for n, row in enumerate(gauge["rows_first_eight"]):
        compact = (n + 1) * Q(1, 10) ** n
        require(row["n"] == n, "Gate1 gauge row index")
        require(Q(row["compact_increment"]) == compact, "Gate1 compact row")
        require(row["unbounded_comparison_factor"] == 10**n,
                "Gate1 factor row")
        require(Q(row["combined_increment"]) == n + 1,
                "Gate1 combined row")
    interface = gate1["minimal_physical_interface"]
    require(len(interface["rows"]) == 5, "Gate1 interface count")
    require(interface["gate1"] == "NOT_CERTIFIED", "Gate1 strict status")


def validate_gate2(gate2: dict[str, Any]) -> None:
    require(set(gate2) == {
        "finite_prefix_separator", "minimal_all_depth_stable_package",
        "actual_landing_join_audit",
    }, "Gate2 keys")
    separator = gate2["finite_prefix_separator"]
    require(separator["accepted_prefix_count"] == 96, "Gate2 prefix count")
    require(separator["first_unconstrained_depth"] == 97, "Gate2 first open depth")
    expected = {1: True, 2: True, 95: True, 96: True, 97: False}
    require({row["depth"]: row["required_chart_survives"]
             for row in separator["logical_completion_sample"]} == expected,
            "Gate2 depth-97 separator")
    package = gate2["minimal_all_depth_stable_package"]
    require(len(package["rows"]) == 7, "Gate2 minimal package count")
    require(package["physical_all_depth_graph_transforms"] == "NOT_CERTIFIED",
            "Gate2 graph transform status")

    audit = gate2["actual_landing_join_audit"]
    rows = audit["rows"]
    require([row["field"] for row in rows] == list(range(1, 8)),
            "Gate2 join numbering")
    require(sum(row["status"].startswith("CERTIFIED") for row in rows) == 1,
            "Gate2 join certified count")
    require(rows[5]["status"] == "CERTIFIED_ROUND59", "Gate2 branch inverse")
    require(audit["completed_fields"] == "1/7", "Gate2 join fraction")
    require(audit["official_immutable_gate2_fields"] == "0/17",
            "Gate2 immutable fields")
    require(audit["weak_graph_reconditioning_is_strong_assembly"] is False,
            "Gate2 weak/strong guard")
    require(audit["gate2"] == "NOT_CERTIFIED", "Gate2 status")


def validate_gate3(gate3: dict[str, Any]) -> None:
    require(set(gate3) == {
        "chosen_target_first_root_reaudit", "atom_and_depth_scope_reaudit",
        "clock_vs_raw_enumeration_separator", "cad_degree_frontier",
        "direct_strong_interface", "latest_official_technology_audit",
    }, "Gate3 keys")
    root = gate3["chosen_target_first_root_reaudit"]
    require(root["sign_guard_before_squaring"] is True, "Gate3 sign guard")
    require(root["chosen_target_is_not_silently_selected_by_competitor_predicate"] is True,
            "Gate3 chosen-target guard")
    require(root["current_source_uses_outgoing_convexity_row"] is True,
            "Gate3 source guard")
    grid = independent_root_grid()
    for key, value in grid.items():
        require(root[key] == value, f"Gate3 root grid {key}")
    require(root["grid_cases"] == 3264, "Gate3 root grid count")

    atom = gate3["atom_and_depth_scope_reaudit"]
    require(atom["target_slots"] == 162 and atom["chosen_slots"] == 1,
            "Gate3 target slots")
    require(atom["nonchosen_slots"] == 161, "Gate3 nonchosen slots")
    require(atom["padded_atoms_per_nonchosen_slot"] == 5, "Gate3 padding")
    require(atom["competitor_atom_budget"] == 805, "Gate3 competitor budget")
    require(atom["dynamics_sign_tie_cemetery_budget"] == 25,
            "Gate3 other budget")
    require(atom["per_step_atom_budget"] == 830, "Gate3 per-step budget")
    rows = atom["budget_rows_first_eight"]
    require(len(rows) == 8, "Gate3 budget rows")
    for n, row in enumerate(rows, 1):
        require(row == {
            "depth": n,
            "physical_variables_upper": 8 * n + 5,
            "physical_atoms_upper": 830 * n + 12,
            "physical_degree_upper": 4,
            "raw_word_candidates": 8 * 162**n,
        }, "Gate3 budget row")
        require(row["physical_variables_upper"] <= 400 * n + 20,
                "Gate3 variable fit")
        require(row["physical_atoms_upper"] <= 2000 * n + 100,
                "Gate3 atom fit")

    clock = gate3["clock_vs_raw_enumeration_separator"]
    require(math.exp(1 / 6) / 2 < 1, "Gate3 clock moment ratio")
    for n, row in enumerate(clock["rows_first_eight"]):
        probability = Q(1, 2 ** (n + 1))
        require(row["depth"] == n, "Gate3 clock depth")
        require(Q(row["probability"]) == probability, "Gate3 clock probability")
        require(row["raw_candidate_upper"] == 8 * 162**n,
                "Gate3 raw candidates")
        require(Q(row["expectation_term"]) == 4 * 81**n,
                "Gate3 expectation term")
    require(clock["status"] ==
            "CERTIFIED_MOMENT_DOES_NOT_PAY_RAW_ENUMERATION_ROUTE",
            "Gate3 clock status")

    cad = gate3["cad_degree_frontier"]
    d_value = 8
    for r, row in enumerate(cad["rows_first_nine"]):
        require(row["projection_step"] == r, "Gate3 degree row index")
        require(int(row["D_r"]) == d_value == 2 ** (4 * 2**r - 1),
                "Gate3 degree closed form")
        d_value = 2 * d_value**2
    require(cad["actual_cell_lower_bound"] is False, "Gate3 upper/lower guard")

    direct = gate3["direct_strong_interface"]
    require(len(direct["rows"]) == 4, "Gate3 direct interface count")
    require(direct["physical_strong_R_s_Q_s"] == "NOT_CERTIFIED",
            "Gate3 strong RQ")
    require(direct["directional_Piola"] == "NOT_CERTIFIED",
            "Gate3 Piola")
    require(direct["MT_DQ"] == "NOT_CERTIFIED", "Gate3 MT_DQ")
    require(direct["gate3"] == "NOT_CERTIFIED", "Gate3 status")

    tech = gate3["latest_official_technology_audit"]
    require(tech["checked_on"] == "2026-07-20", "technology date")
    require(tech["external_theorem_promoted"] is False, "technology no import")
    require("not moving-scatterer" in tech["arXiv_2604_19671v2"]["type_mismatch"],
            "technology operator type guard")
    require("no known Banach spaces" in
            tech["arXiv_2604_19671v2"]["explicit_Banach_space_boundary"],
            "technology standard-pair Banach boundary")


def validate_result(result: dict[str, Any]) -> None:
    require(set(result) == {"gate1", "gate2", "gate3", "strict_status"},
            "result keys")
    validate_gate1(result["gate1"])
    validate_gate2(result["gate2"])
    validate_gate3(result["gate3"])
    require(result["strict_status"] == {
        "gate1": "NOT_CERTIFIED",
        "gate2": "NOT_CERTIFIED",
        "gate2_immutable_fields": "0/17",
        "gate2_landing_join": "1/7",
        "gate3": "NOT_CERTIFIED",
        "composite_gates": "0/5",
        "cm2": "NO-GO_FOR_CLAIM",
    }, "strict status")


def validate_data(data: dict[str, Any], check_files: bool = True) -> None:
    require(set(data) == {
        "schema", "artifact", "date", "dependencies", "result",
        "result_sha256", "strict_verdict", "report_sha256",
        "certificate_sha256", "verifier_sha256",
    }, "manifest top-level keys")
    require(data["schema"] ==
            "cm2.gate123.round60.combined-gauge-stable-strong-operator-frontier.v1",
            "schema")
    require(data["artifact"] ==
            "cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier",
            "artifact")
    require(data["date"] == "2026-07-20", "date")
    expected_dependencies = [
        {"path": rel, "sha256": digest} for rel, digest in DEPENDENCIES.items()
    ]
    require(data["dependencies"] == expected_dependencies, "dependency ledger")
    if check_files:
        for row in expected_dependencies:
            path = ROOT / row["path"]
            require(path.is_file() and not path.is_symlink(),
                    f"dependency file/type: {row['path']}")
            require(sha256_path(path) == row["sha256"],
                    f"dependency hash: {row['path']}")
        for path in (REPORT, CERT, VERIFIER):
            require(path.is_file() and not path.is_symlink(), f"artifact file/type: {path}")
    require(data["report_sha256"] == sha256_path(REPORT), "report hash")
    require(data["certificate_sha256"] == sha256_path(CERT), "certificate hash")
    require(data["verifier_sha256"] == sha256_path(VERIFIER), "verifier hash")
    require(data["result_sha256"] == canonical_digest(data["result"]),
            "result self digest")
    require(data["result_sha256"] == RESULT_DIGEST, "pinned result digest")
    require(data["strict_verdict"] == (
        "exact gauge, finite-prefix and clock/counting frontiers are certified; "
        "physical all-plaque Dini, all-depth stable holonomy and strong moving-"
        "scatterer R/Q/Piola/MT_DQ remain not certified"
    ), "strict verdict")
    validate_result(data["result"])


def iter_leaf_paths(value: Any, prefix: tuple[Any, ...] = ()) -> Iterable[tuple[Any, ...]]:
    if isinstance(value, dict):
        for key in sorted(value):
            yield from iter_leaf_paths(value[key], prefix + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from iter_leaf_paths(item, prefix + (index,))
    else:
        yield prefix


def get_parent(value: Any, path: tuple[Any, ...]) -> tuple[Any, Any]:
    cursor = value
    for key in path[:-1]:
        cursor = cursor[key]
    return cursor, path[-1]


def changed_scalar(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, float):
        return value + 1.0
    if value is None:
        return "not-null"
    if isinstance(value, str):
        return value + "__MUTATED"
    raise TypeError(type(value))


def rejected(data: dict[str, Any]) -> bool:
    try:
        validate_data(data, check_files=False)
    except (VerificationError, OSError, ValueError, KeyError, TypeError):
        return True
    return False


def hostile_suite(data: dict[str, Any]) -> tuple[int, int]:
    tests: list[dict[str, Any]] = []
    leaves = list(iter_leaf_paths(data))
    require(len(leaves) >= 124, "hostile leaf supply")
    for path in leaves[:124]:
        trial = copy.deepcopy(data)
        parent, key = get_parent(trial, path)
        parent[key] = changed_scalar(parent[key])
        tests.append(trial)

    trial = copy.deepcopy(data)
    trial.pop("result")
    tests.append(trial)
    trial = copy.deepcopy(data)
    trial["unexpected"] = True
    tests.append(trial)
    trial = copy.deepcopy(data)
    trial["dependencies"] = list(reversed(trial["dependencies"]))
    tests.append(trial)
    trial = copy.deepcopy(data)
    trial["result"]["strict_status"]["gate3"] = "CERTIFIED"
    tests.append(trial)
    rejected_count = sum(rejected(test) for test in tests)
    return rejected_count, len(tests)


def parser_guard_suite() -> tuple[int, int]:
    bad_payloads = [
        '{"x":1,"x":2}',
        '{"x":NaN}',
        '[1,2,3]',
    ]
    rejected_count = 0
    for payload in bad_payloads:
        try:
            value = json.loads(
                payload, object_pairs_hook=unique_object,
                parse_constant=reject_constant,
            )
            require(isinstance(value, dict), "parser root object")
        except (VerificationError, json.JSONDecodeError):
            rejected_count += 1
    return rejected_count, len(bad_payloads)


def reemit_check(data: dict[str, Any]) -> None:
    with tempfile.TemporaryDirectory(prefix="cm2-r60-g123-") as temp_dir:
        emitted = Path(temp_dir) / "manifest.json"
        completed = subprocess.run(
            [sys.executable, str(CERT), "--emit-manifest", str(emitted)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        require(completed.returncode == 0,
                f"producer reemit exit {completed.returncode}: {completed.stderr}")
        require(emitted.read_bytes() == canonical_bytes(data), "reemit byte drift")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", action="store_true")
    args = parser.parse_args()

    try:
        data = load_manifest()
        require(MANIFEST.read_bytes() == canonical_bytes(data),
                "noncanonical manifest bytes")
        validate_data(data, check_files=True)
        if args.self_test:
            rejected_count, total = hostile_suite(data)
            require((rejected_count, total) == (128, 128), "hostile suite")
            parser_rejected, parser_total = parser_guard_suite()
            require((parser_rejected, parser_total) == (3, 3), "parser guard suite")
            print(f"HOSTILE_MUTATIONS_REJECTED: {rejected_count}/{total}")
            print(f"STRICT_JSON_GUARDS_REJECTED: {parser_rejected}/{parser_total}")
        if args.reemit:
            reemit_check(data)
            print("DETERMINISTIC_REEMIT: PASS")
    except (VerificationError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"VERIFICATION_ERROR: {exc}", file=sys.stderr)
        return 1

    print("INTEGRITY: PASS")
    print("DEPENDENCIES: 4/4")
    print("REPLAY: PASS")
    print("GATE1_COMPACT_TO_COMBINED_BUDGET: CERTIFIED_CONDITIONAL")
    print("GATE1_SELECTED_TO_ALL_PLAQUE: CERTIFIED_FALSE_BY_SEPARATOR")
    print("GATE2_PREFIX_TO_ALL_DEPTH: CERTIFIED_FALSE_BY_SEPARATOR")
    print("GATE3_FIRST_ROOT_GRID: 3264/3264")
    print("GATE3_CLOCK_PAYS_RAW_ENUMERATION: CERTIFIED_FALSE_BY_SEPARATOR")
    print("GATES_1_2_3: NOT_CERTIFIED")
    print("COMPOSITE_GATES: 0/5")
    print("CM2: NO-GO_FOR_CLAIM")
    positive = args.integrity_only or args.replay or args.self_test or args.reemit
    return 0 if positive else 2


if __name__ == "__main__":
    raise SystemExit(main())
