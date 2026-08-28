#!/usr/bin/env python3
"""Independent verifier for the CM2 Round-59 Gate-1/2/3 package."""

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
CERT = HERE / "cm2_gate123_round59_physical_formula_shadow_dini_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
REPORT = HERE / (
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-"
    "assault-2026-07-20.md"
)
MANIFEST = HERE / (
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-"
    "manifest-2026-07-20.json"
)
Q = Fraction

RESULT_DIGEST = "67bc3c3de37ab394a257ce1fbb83f53ee1066cd60632d1341dcf0ff2942a5a0b"

DEPENDENCIES = {
    "deliverables/cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-assault-2026-07-20.md":
        "e6b87bd43bf4c35ca4804dc1a563a916d27cb0550c45e7b3fb1d670dddfd0934",
    "deliverables/cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-manifest-2026-07-20.json":
        "42a035e38687acb4ae1a3ce43a1459c49ba08a1406083c811f919823ecc8d526",
    "deliverables/cm2-gate1-numeric-holonomy-tail-twisting-frontier-assault-2026-07-16.md":
        "35f0632a29c93b639120cdffe5720b5d4ba282b02b3a247b476fcfb8f1ab4925",
    "deliverables/cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json":
        "4b9baaacaf7a315659448072d8d382bc90c4b41a9d98746b63c786f206ad449a",
    "deliverables/cm2-gate2-actual-stable-plaque-continuation-2026-07-15.md":
        "3f1852862ea5192d4ab350c2c67dc874d5d69634856ee874f350fe2ca038e37d",
    "deliverables/cm2-gate2-actual-stable-plaque-continuation-manifest-2026-07-15.json":
        "1bfc3ea9f5eb587b41a94ba4fd808c03c309389269f8d5e903f9bfce09a4f871",
    "deliverables/cm2-gate2-round25-product-base-assault-2026-07-18.md":
        "db75a6a8741d435182a1e0d0510e06d1b75b15eaba3d0c26e090e9c5990664e6",
    "deliverables/cm2-gate2-round25-product-base-manifest-2026-07-18.json":
        "8045c36fb14c69a145be4ebf4cd33ae11d55fd77f4591b91782f13516c80679b",
    "deliverables/cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-assault-2026-07-20.md":
        "0e9ce7397039c86178858bdd5e1ebe6228938e473711ce65075a3c4d45db16c8",
    "deliverables/cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json":
        "d335ea6b9bfdc68c13fa0c44f5f2893af7399546f5951d0cfc156be8b5236ffb",
    "deliverables/cm2-gate3-first-hit-atlas-assault-2026-07-15.md":
        "fd2c1c47602e361da8eab48b88e5c169fd679dd783ee8aea38512bdbdde2b3d5",
    "deliverables/cm2-gate3-first-hit-atlas-manifest-2026-07-15.json":
        "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4",
    "deliverables/cm2-gate3-iterated-common-atlas-mt-dq-assault-2026-07-16.md":
        "235cf2c74ea3871a1d3862476d5e7d0ac506acc0e490ea5df12d8d2940c6b8f6",
    "deliverables/cm2-gate3-iterated-common-atlas-mt-dq-manifest-2026-07-16.json":
        "8b6e8ca2c436237f8eb41f24c94bb11fe9ddb393cbbe4845d41b6c7a2409c0e1",
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


def no_earlier(a: Q, b: Q, tau: Q) -> bool:
    require(b > 0 and tau > 0, "root domain")
    delta = a * a - b
    return a <= 0 or delta < 0 or (
        a - tau >= 0 and delta <= (a - tau) ** 2
    )


def validate_replay(result: dict[str, Any]) -> None:
    require(set(result) == {"gate1", "gate2", "gate3", "strict_status"},
            "result keys")

    gate1 = result["gate1"]
    selected = gate1["physical_selected_QNL_tail"]
    require(selected["normalized_critical_Dini_sum"] == "100/81",
            "Gate1 critical sum field")
    require(selected["normalized_diagonal_Dini_sum"] == "10000/9801",
            "Gate1 diagonal sum field")
    require(sum((m + 1) * Q(1, 10) ** m for m in range(400)) < Q(100, 81),
            "Gate1 independent critical partial sum")
    require(Q(1) / (1 - Q(1, 10)) ** 2 == Q(100, 81),
            "Gate1 critical closed form")
    require(Q(1) / (1 - Q(1, 100)) ** 2 == Q(10000, 9801),
            "Gate1 diagonal closed form")
    error = Q(selected["two_sided_entry_error_strict_upper"])
    radius = Q(selected["same_fibre_robustness_radius"])
    wedge = Q(selected["smallest_wedge_strict_inward_lower"])
    require(error < radius and error < wedge, "Gate1 loop/wedge inequalities")
    require(selected["status"] == "CERTIFIED_PHYSICAL_SELECTED_GERM_AND_LOOP_ONLY",
            "Gate1 local type")
    boundary1 = gate1["type_boundary"]
    require(boundary1["physical_all_plaque_Dini_rows"] == "NOT_CERTIFIED",
            "Gate1 no all-plaque promotion")
    require(boundary1["combined_gauge_loop_comparison_error_le_1e_minus_29"]
            == "NOT_CERTIFIED", "Gate1 no combined-gauge promotion")
    require(boundary1["gate1"] == "NOT_CERTIFIED", "Gate1 status")

    gate2 = result["gate2"]
    finite = gate2["physical_finite_shadow_registry"]
    rows = finite["rows"]
    require(len(rows) == finite["row_count"] == 96, "Gate2 shadow count")
    require([row["depth"] for row in rows] == list(range(1, 97)),
            "Gate2 shadow depths")
    require(all(row["physical_collision_singularity_shadow_measure"] == "0"
                for row in rows), "Gate2 shadow zero rows")
    require(finite["graph_transform_chart_defined_at_every_prefix"]
            == "NOT_CERTIFIED", "Gate2 graph-transform boundary")
    join = gate2["gate2_to_gate4_seven_field_audit"]
    jrows = join["rows"]
    require([row["field"] for row in jrows] == list(range(1, 8)),
            "Gate2 join numbering")
    certified = sum(row["status"].startswith("CERTIFIED") for row in jrows)
    require(certified == join["fully_certified_field_count"] == 1,
            "Gate2 join completed count")
    require(jrows[5]["status"] == "CERTIFIED_ON_THE_EXACT_RAW_FIRST_RETURN_GRAPH",
            "Gate2 exact completed field")
    require(join["join_closed"] is False, "Gate2 join no-promotion")
    technology = gate2["measure_type_audit_2604_25881"]
    require(technology["is_CM2_collision_Liouville_SRB_law"] is False,
            "Gate2 MME/SRB distinction")
    require(gate2["strict_status"]["immutable_gate2_fields"] == "0/17",
            "Gate2 immutable status")

    gate3 = result["gate3"]
    formula = gate3["actual_physical_circular_pilot_formula"]
    require(formula["fixed_depth_formula_fits_declared_budget"] is True,
            "Gate3 budget verdict")
    require(formula["physical_polynomial_degree_upper"] == 4,
            "Gate3 degree")
    brows = formula["first_eight_budget_rows"]
    require(len(brows) == 8, "Gate3 budget row count")
    for n, row in enumerate(brows, 1):
        require(row["depth"] == n, "Gate3 budget depth")
        require(row["physical_variables"] == 8 * n + 5, "Gate3 variables")
        require(row["physical_atomic_predicates_upper"] == 830 * n + 12,
                "Gate3 atoms")
        require(row["physical_degree_upper"] == 4, "Gate3 row degree")
        require(row["physical_variables"] <= 400 * n + 20,
                "Gate3 declared variable fit")
        require(row["physical_atomic_predicates_upper"] <= 2000 * n + 100,
                "Gate3 declared atom fit")
        require(row["branch_words"] == 8 * 162**n, "Gate3 branch words")

    samples = formula["root_test_samples"]
    require([no_earlier(Q(row["a"]), Q(row["b"]), Q(row["tau"]))
             for row in samples] == [True, True, True, False],
            "Gate3 no-earlier Boolean replay")
    require(formula["root_formula_domain"].startswith("|u|=1, b>0"),
            "Gate3 root domain typing")
    cad = gate3["physical_fixed_depth_CAD"]
    require(cad["physical_formula_instantiates_Round58_recurrence"] is True,
            "Gate3 physical recurrence instantiation")
    for depth_row in cad["first_three_projection_replays"]:
        n = depth_row["depth"]
        s_value, d_value, product = 2000 * n + 100, 8, 1
        expected = []
        for projection_step in range(3):
            stack = 2 * s_value * d_value + 1
            product *= stack
            expected.append((str(s_value), str(d_value), str(stack), str(product)))
            s_value = 2 * (s_value * d_value + 1) ** 2
            d_value = 2 * d_value**2
        actual = [(
            row["polynomial_count_majorant"], row["degree_majorant"],
            row["stack_factor"], row["cell_product_prefix"]
        ) for row in depth_row["rows"]]
        require(actual == expected, "Gate3 CAD recurrence")
    nonpromotion = gate3["strict_nonpromotion"]
    require(nonpromotion == {
        "existing_exp_Dbar_over_6_moment_pays_CAD_majorant": False,
        "physical_strong_R_s_Q_s": "NOT_CERTIFIED",
        "directional_Piola": "NOT_CERTIFIED",
        "MT_DQ": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
    }, "Gate3 strict nonpromotion")

    require(result["strict_status"] == {
        "gate1": "NOT_CERTIFIED",
        "gate2": "NOT_CERTIFIED",
        "gate2_immutable_fields": "0/17",
        "gate3": "NOT_CERTIFIED",
        "composite_gates": "0/5",
        "cm2": "NO-GO_FOR_CLAIM",
    }, "global strict status")


def validate_data(data: dict[str, Any], check_files: bool = True) -> None:
    require(set(data) == {
        "schema", "artifact", "date", "dependencies", "result",
        "strict_verdict", "report_sha256", "certificate_sha256",
        "verifier_sha256",
    }, "manifest top-level keys")
    require(data["schema"] ==
            "cm2.gate123.round59.physical-formula-shadow-dini-frontier.v1",
            "schema")
    require(data["artifact"] ==
            "cm2-gate123-round59-physical-formula-shadow-dini-frontier",
            "artifact")
    require(data["date"] == "2026-07-20", "date")
    expected_dependencies = [
        {"path": rel, "sha256": value} for rel, value in DEPENDENCIES.items()
    ]
    require(data["dependencies"] == expected_dependencies, "dependencies ledger")
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
    require(canonical_digest(data["result"]) == RESULT_DIGEST, "result digest")
    require(data["strict_verdict"] == (
        "actual fixed-depth circular-pilot formulas fit the explicit CAD budget; "
        "the selected QNL loop and finite physical shadows do not supply all-plaque "
        "Dini, an all-depth stable quotient, strong R/Q, Piola or MT_DQ"
    ), "strict verdict")
    validate_replay(data["result"])


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
    require(len(leaves) >= 96, "hostile leaf supply")
    for path in leaves[:96]:
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


def reemit_check(data: dict[str, Any]) -> None:
    with tempfile.TemporaryDirectory(prefix="cm2-r59-g123-") as temp_dir:
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
        require(MANIFEST.read_bytes() == canonical_bytes(data), "noncanonical manifest bytes")
        validate_data(data, check_files=True)
        if args.self_test:
            rejected_count, total = hostile_suite(data)
            require((rejected_count, total) == (100, 100), "hostile suite")
            print(f"HOSTILE_MUTATIONS_REJECTED: {rejected_count}/{total}")
        if args.reemit:
            reemit_check(data)
            print("DETERMINISTIC_REEMIT: PASS")
    except (VerificationError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"VERIFICATION_ERROR: {exc}", file=sys.stderr)
        return 1

    print("INTEGRITY: PASS")
    print("DEPENDENCIES: 14/14")
    print("REPLAY: PASS")
    print("GATE1_SELECTED_QNL_PHYSICAL_DINI_TAIL: CERTIFIED_SELECTED_GERM_ONLY")
    print("GATE2_PHYSICAL_FINITE_COLLISION_SHADOW_ROWS: 96/96")
    print("GATE3_ACTUAL_PHYSICAL_FIXED_DEPTH_FORMULA_BUDGET: CERTIFIED")
    print("GATES_1_2_3: NOT_CERTIFIED")
    print("COMPOSITE_GATES: 0/5")
    print("CM2: NO-GO_FOR_CLAIM")
    positive = args.integrity_only or args.replay or args.self_test or args.reemit
    return 0 if positive else 2


if __name__ == "__main__":
    raise SystemExit(main())
