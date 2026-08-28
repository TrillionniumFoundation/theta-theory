#!/usr/bin/env python3
"""Fail-closed verifier for the Round-59 independent core audit."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
CERT = HERE / "cm2_round59_independent_core_frontier_audit_cert.py"
MANIFEST = HERE / "cm2-round59-independent-core-frontier-audit-manifest-2026-07-20.json"
REPORT = HERE / "cm2-round59-independent-core-frontier-audit-2026-07-20.md"
SCHEMA = "cm2.round59-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = SCHEMA + ".manifest.v1"
EXPECTED_PINS = {
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json": "e7305e0b72eed28bc68b115e1201fc02e2b66d3cc95906fc6d1efc5e9463a4f5",
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.sha256": "967421bc83b283510cdb25013f2e723e5761337e56471fad64a9ef74b35536c0",
    "cm2-gate5-round59-unified-clearance-join-jordan-frontier-manifest-2026-07-20.json": "46eb285a7532377b89e37c1ba2ce6a5b28db1e661eaee4889e576c0a89c94ced",
    "cm2-gate5-round59-unified-clearance-join-jordan-frontier-manifest-2026-07-20.sha256": "2a1487d9fcfb9535f1d05c4c538ff56e6b726d209fe12e48bd637ad2e11b1161",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.json": "16a2562868df58b2e14bf672d2d0d11735581016ff50e10f5a6d2c1e660d3466",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.sha256": "985910708fe715d0c891cd6a288b37a5e1b88530db858a712e7e82e80cbb4b71",
}


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(key)
        out[key] = value
    return out


def strict_load_text(text: str) -> dict[str, Any]:
    value = json.loads(text, object_pairs_hook=strict_object, parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    if not isinstance(value, dict):
        raise ValueError("root")
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def load() -> dict[str, Any]:
    if not MANIFEST.is_file() or MANIFEST.is_symlink():
        raise ValueError("manifest path")
    return strict_load_text(MANIFEST.read_text(encoding="utf-8"))


def integrity(data: dict[str, Any]) -> None:
    if set(data) != {"schema", "dependencies", "certificate_sha256", "verifier_sha256", "report_sha256", "result", "verdict"}:
        raise ValueError("manifest shape")
    if data["schema"] != MANIFEST_SCHEMA or data["dependencies"] != EXPECTED_PINS:
        raise ValueError("schema/dependencies")
    for name, expected in EXPECTED_PINS.items():
        path = HERE / name
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE or sha(path) != expected:
            raise ValueError(f"pin: {name}")
    if data["certificate_sha256"] != sha(CERT) or data["verifier_sha256"] != sha(Path(__file__).resolve()) or data["report_sha256"] != sha(REPORT):
        raise ValueError("artifact digest")
    result = data["result"]
    if result["schema"] != SCHEMA:
        raise ValueError("result schema")
    replay = copy.deepcopy(result)
    observed = replay.pop("internal_replay_digest")
    if observed != digest(replay):
        raise ValueError("result digest")
    if data["verdict"] != result["strict_verdict"]:
        raise ValueError("verdict mirror")


def semantics(data: dict[str, Any]) -> None:
    result = data["result"]
    if set(result) != {"schema", "provenance", "frozen_leaf_artifact_audit", "gate4_independent_audit", "gate5_independent_audit", "gate123_independent_audit", "technology_type_audit", "main_leaf_acceptance_matrix", "independent_leaf_acceptance_matrix", "four_leaf_acceptance_matrix", "strict_verdict", "internal_replay_digest"}:
        raise ValueError("result shape")
    provenance = result["provenance"]
    if provenance["frozen_pins"] != EXPECTED_PINS or provenance["old_artifacts_modified"] is not False or provenance["external_theorem_promoted"] is not False:
        raise ValueError("provenance")
    frozen = result["frozen_leaf_artifact_audit"]
    if frozen["manifest_and_ledger_pins"] != "6/6" or frozen["leaf_ledger_rows_status"] != "12/12" or len(frozen["leaf_ledger_rows"]) != 12:
        raise ValueError("frozen rows")
    for row in frozen["leaf_ledger_rows"]:
        path = HERE / row["name"]
        if not path.is_file() or path.is_symlink() or sha(path) != row["sha256"]:
            raise ValueError("ledger artifact")
    g4 = result["gate4_independent_audit"]
    if g4["status"] != "PASS" or g4["D_bad"] != 2 or g4["bridge_bound"] != "7833600000/1999" or g4["seven_field_join"] != "1/7_NOT_A_GATE2_PROMOTION":
        raise ValueError("Gate4 replay")
    cp = Q(4 * 10**90 * 360493663, 358863)
    h = Q(999, 1000)
    n = cp.numerator // cp.denominator + 1
    if not (1 / h < cp < Q(n) / h < 2 * cp):
        raise ValueError("Gate4 independent threshold")
    g5 = result["gate5_independent_audit"]
    if g5["status"] != "PASS" or g5["critical_threshold"] != "p>1" or g5["seven_operator_bits"] != "2_FROZEN_5_OPEN" or len(g5["Abel_toy_rows"]) != 3:
        raise ValueError("Gate5 replay")
    for row in g5["Abel_toy_rows"]:
        if row["direct"] != row["Abel"]:
            raise ValueError("Abel equality")
    g123 = result["gate123_independent_audit"]
    if g123["status"] != "PASS" or g123["Gate1_scope"] != "SELECTED_QNL_GERM_ONLY" or g123["Gate2_collision_shadow_rows"] != "96/96_FINITE_PREFIX_ONLY" or g123["Gate3_atom_budget_identity"] != "161*5+25=830" or g123["Gate3_scope"] != "FIXED_DEPTH_NOT_DEPTH_INTEGRATED":
        raise ValueError("Gate123 replay")
    if g123["Gate3_exact_rational_root_cases"] < 200:
        raise ValueError("root replay count")
    tech = result["technology_type_audit"]
    if tech["status"] != "PASS" or tech["external_theorem_promoted"] is not False or len(tech["records"]) != 7:
        raise ValueError("technology type")
    matrix = result["main_leaf_acceptance_matrix"]
    expected_matrix = {"syntax": "6/6", "older_dependency_pins": "31/31", "frozen_manifest_and_ledger_pins": "6/6", "leaf_ledger_artifact_rows": "12/12", "integrity": "3/3", "replay": "3/3", "reemit": "3/3", "hostile_mutations_rejected": "272/272", "default_cert_verifier_exit_2": "6/6"}
    if matrix != expected_matrix:
        raise ValueError("acceptance matrix")
    independent = {"syntax": "2/2", "frozen_manifest_and_ledger_pins": "6/6", "leaf_ledger_artifact_rows": "12/12", "integrity": "1/1", "replay": "1/1", "reemit": "1/1", "hostile_mutations_rejected": "59/59", "default_cert_verifier_exit_2": "2/2", "SHA_ledger_rows": "4/4"}
    if result["independent_leaf_acceptance_matrix"] != independent:
        raise ValueError("independent acceptance matrix")
    combined = {"syntax": "8/8", "dependency_pins": "37/37", "integrity": "4/4", "replay": "4/4", "reemit": "4/4", "hostile_mutations_rejected": "331/331", "SHA_ledger_rows": "16/16", "default_cert_verifier_exit_2": "8/8", "Round59_stale_or_temp_files": 0}
    if result["four_leaf_acceptance_matrix"] != combined:
        raise ValueError("four-leaf acceptance matrix")
    verdict = result["strict_verdict"]
    if verdict != {"Gate1": "NOT_CERTIFIED", "Gate2": "NOT_CERTIFIED", "Gate2_immutable_fields": "0/17", "Gate3": "NOT_CERTIFIED", "Gate4": "NOT_CERTIFIED", "Gate5": "NOT_CERTIFIED", "Gate5_maturity": "10/18", "complete_18_field_blocks": 0, "complete_composite_gates": "0/5", "CM2": "NO-GO_FOR_CLAIM", "audit": "PASS_NO_CLAIMED_SCOPE_BLOCKER"}:
        raise ValueError("strict verdict")


def validate(data: dict[str, Any]) -> None:
    integrity(data)
    semantics(data)


def assign(data: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    target: Any = data
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def hostile() -> tuple[int, int]:
    original = load()
    mutations: list[tuple[tuple[Any, ...], Any]] = [
        (("schema",), "bad"), (("certificate_sha256",), "0" * 64), (("verifier_sha256",), "0" * 64), (("report_sha256",), "0" * 64),
        (("dependencies", next(iter(EXPECTED_PINS))), "0" * 64), (("result", "schema"), "bad"), (("result", "internal_replay_digest"), "0" * 64),
        (("result", "provenance", "old_artifacts_modified"), True), (("result", "provenance", "external_theorem_promoted"), True), (("result", "provenance", "frozen_pins"), {}),
        (("result", "frozen_leaf_artifact_audit", "manifest_and_ledger_pins"), "0/6"), (("result", "frozen_leaf_artifact_audit", "leaf_ledger_rows_status"), "0/12"),
        (("result", "frozen_leaf_artifact_audit", "leaf_ledger_rows"), []), (("result", "frozen_leaf_artifact_audit", "leaf_ledger_rows", 0, "sha256"), "0" * 64),
        (("result", "gate4_independent_audit", "status"), "FAIL"), (("result", "gate4_independent_audit", "D_bad"), 1), (("result", "gate4_independent_audit", "bridge_bound"), "0"),
        (("result", "gate4_independent_audit", "seven_field_join"), "7/7"), (("result", "gate4_independent_audit", "threshold_chain"), "false"),
        (("result", "gate5_independent_audit", "status"), "FAIL"), (("result", "gate5_independent_audit", "critical_threshold"), "p>0"), (("result", "gate5_independent_audit", "seven_operator_bits"), "7_FROZEN"),
        (("result", "gate5_independent_audit", "Abel_toy_rows"), []), (("result", "gate5_independent_audit", "Abel_toy_rows", 0, "direct"), "0"), (("result", "gate5_independent_audit", "Orlicz_scope"), "uniform"),
        (("result", "gate123_independent_audit", "status"), "FAIL"), (("result", "gate123_independent_audit", "Gate1_scope"), "ALL_PLAQUES"),
        (("result", "gate123_independent_audit", "Gate2_collision_shadow_rows"), "ALL_DEPTH"), (("result", "gate123_independent_audit", "Gate2_landing_join"), "7/7"),
        (("result", "gate123_independent_audit", "Gate3_exact_rational_root_cases"), 0), (("result", "gate123_independent_audit", "Gate3_atom_budget_identity"), "false"),
        (("result", "gate123_independent_audit", "Gate3_word_universe"), "8*1^n"), (("result", "gate123_independent_audit", "Gate3_scope"), "ALL_DEPTH"),
        (("result", "technology_type_audit", "status"), "FAIL"), (("result", "technology_type_audit", "records"), []), (("result", "technology_type_audit", "external_theorem_promoted"), True),
        (("result", "technology_type_audit", "MME_is_not_pinned_collision_law"), False), (("result", "technology_type_audit", "inter_sign_OT_is_not_positive_Jordan_control"), False),
        (("result", "main_leaf_acceptance_matrix", "syntax"), "0/6"), (("result", "main_leaf_acceptance_matrix", "older_dependency_pins"), "0/31"),
        (("result", "main_leaf_acceptance_matrix", "replay"), "0/3"), (("result", "main_leaf_acceptance_matrix", "reemit"), "0/3"),
        (("result", "main_leaf_acceptance_matrix", "hostile_mutations_rejected"), "0/272"), (("result", "main_leaf_acceptance_matrix", "default_cert_verifier_exit_2"), "0/6"),
        (("result", "strict_verdict", "Gate1"), "CERTIFIED"), (("result", "strict_verdict", "Gate2"), "CERTIFIED"), (("result", "strict_verdict", "Gate3"), "CERTIFIED"),
        (("result", "strict_verdict", "Gate4"), "CERTIFIED"), (("result", "strict_verdict", "Gate5"), "CERTIFIED"), (("result", "strict_verdict", "Gate5_maturity"), "18/18"),
        (("result", "strict_verdict", "complete_18_field_blocks"), 1), (("result", "strict_verdict", "complete_composite_gates"), "1/5"),
        (("result", "strict_verdict", "CM2"), "GO_FOR_CLAIM"), (("result", "strict_verdict", "audit"), "FAIL"), (("verdict", "CM2"), "GO_FOR_CLAIM"),
    ]
    rejected = 0
    for path, value in mutations:
        candidate = copy.deepcopy(original)
        assign(candidate, path, value)
        try:
            validate(candidate)
        except (OSError, ValueError, RuntimeError, KeyError, TypeError):
            rejected += 1
    strict_cases = ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '[1,2]')
    for payload in strict_cases:
        try:
            strict_load_text(payload)
        except ValueError:
            rejected += 1
    return rejected, len(mutations) + len(strict_cases)


def generator_replay() -> None:
    proc = subprocess.run([sys.executable, str(CERT), "--manifest-json"], cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode != 0 or proc.stdout != MANIFEST.read_bytes():
        raise ValueError("generator replay")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        data = load()
        validate(data)
        if args.replay:
            generator_replay()
        if args.self_test:
            rejected, total = hostile()
            if rejected != total:
                raise ValueError(f"hostile shortfall {rejected}/{total}")
            print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
            return 0
        if args.reemit is not None:
            target = args.reemit.resolve()
            if target.parent != HERE:
                raise ValueError("reemit outside deliverables")
            target.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"REEMIT: {target}")
            return 0
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as exc:
        print(f"ROUND59_INDEPENDENT_AUDIT_VERIFIER_FAILURE: {exc}", file=sys.stderr)
        return 1
    if args.integrity_only or args.replay:
        print("ROUND59_INDEPENDENT_AUDIT: PASS")
        print("NO_GATE_PROMOTION: PASS")
        return 0
    verdict = data["verdict"]
    print("INDEPENDENT_AUDIT:", verdict["audit"])
    print("COMPOSITE_GATES:", verdict["complete_composite_gates"])
    print("CM2:", verdict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
