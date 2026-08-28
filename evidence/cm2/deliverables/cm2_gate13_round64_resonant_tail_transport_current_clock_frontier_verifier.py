#!/usr/bin/env python3
"""Independent verifier for the Round-64 Gate-1/3 frontier."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round64_common import (
    CertError, digest, replay_sidecar, require, semantic_mutation_test,
    sha256_path, strict_json_path, strict_json_self_test, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate13.round64.resonant-tail-transport-current-clock.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate13-round64-resonant-tail-transport-current-clock-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_gate13_round64_resonant_tail_transport_current_clock_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round64_common.py"
EXPECTED_RESULT_DIGEST = "f213acc2a3eb6360973b895fc6c6bfc6082bf35a912b9be39fc9b3e575e0d0fd"

PINS = {
    "cm2-sixty-third-direct-assault-2026-07-21.md":
        "9cde412ba689be87d777906404c9c9426a2a8a102385a2c4c510df8f9b7a6a05",
    "cm2-sixty-third-direct-assault-manifest-2026-07-21.sha256":
        "a0b512f32914ef2692b31466a4ea156c44698b1eaf44d8ead45b2c74ee73230e",
    "cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.json":
        "3aae6d018fc15aaab47116d311eed8333c56b87542b0b5761b849221cbf76d6b",
    "cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "8227dd32e36d2879f9dbbdced54f3c50b3eac1536ce8fceac480d22cb8617bfd",
    "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-manifest-2026-07-21.json":
        "bdd351955c4537e649009e753900a7f61e3befcc16db55f810af2902dd3581ea",
    "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-manifest-2026-07-21.sha256":
        "b48def6d29a68f9cf30db2b349a41e06b3e5df58766f8d9323e256f75c6ad058",
}


def integrity(data: dict[str, Any], files: bool = True) -> None:
    if files:
        validate_pins(HERE, PINS)
    require(data.get("schema") == MANIFEST_SCHEMA, "manifest schema")
    require(data.get("pins") == PINS, "manifest pins")
    if files:
        require(data.get("report_sha256") == sha256_path(REPORT), "report hash")
        require(data.get("certificate_sha256") == sha256_path(CERT), "cert hash")
        require(data.get("verifier_sha256") == sha256_path(VERIFIER), "verifier hash")
        require(data.get("common_sha256") == sha256_path(COMMON), "common hash")
    result = data.get("result")
    require(isinstance(result, dict), "result root")
    replay = copy.deepcopy(result)
    recorded = replay.pop("internal_replay_digest", None)
    require(recorded == EXPECTED_RESULT_DIGEST, "expected result digest")
    require(digest(replay) == recorded, "recomputed result digest")
    require(data.get("verdict") == result.get("strict_status"), "verdict alias")


def semantics(result: dict[str, Any]) -> None:
    require(result["schema"] == RESULT_SCHEMA, "result schema")
    require(result["provenance"] == {
        "append_only": True,
        "old_artifacts_modified": False,
        "pinned_round63_artifacts": PINS,
    }, "provenance")
    g1 = result["gate1"]
    require(g1["resonant_tail_identity"]["status"] == "CERTIFIED_EXACT_INTERFACE",
            "resonant tail type")
    require(len(g1["resonant_tail_identity"]["required_regularities"]) == 3,
            "resonant tail requirements")
    require(g1["zero_tail_guard"] == {
        "zero_tail_preserves_zero_twisting": True,
        "round63_zero_tail_sufficient_for_Holder_only": True,
        "actual_nonzero_resonant_tail": "NOT_CERTIFIED",
    }, "zero-tail guard")
    model = g1["critical_SL2_replay"]
    require(model["loop"] == [[1, 1], [-1, 0]], "critical loop")
    require(model["determinant"] == 1 and model["wedge_e1"] == model["wedge_e2"] == -1,
            "critical determinant/wedges")
    require(model["zero_tail_loop"] == [[1, 0], [0, 1]], "zero-tail loop")
    require(g1["strict_status"] == "NOT_CERTIFIED", "Gate1 state")

    g3 = result["gate3"]
    transport = g3["BL_transport_bound"]
    require(transport["status"] == "CERTIFIED_EXACT" and len(transport["rows"]) == 12,
            "transport rows")
    for n, row in enumerate(transport["rows"], 1):
        require(row == {
            "n": n, "distance": str(Q(1, 2**n)), "raw_TV": "2",
            "BL_transport_upper": str(Q(1, 2**n)),
        }, f"transport row {n}")
    require(Q(transport["finite_raw_TV_sum"]) == 24, "raw TV sum")
    require(Q(transport["finite_transport_sum"]) == Q(4095, 4096), "transport sum")
    require(transport["infinite_transport_sum"] == "1" and
            transport["infinite_raw_TV_sum"] == "DIVERGES", "infinite comparison")
    require(transport["physical_landing_distance_speed_ledger"] == "NOT_CERTIFIED",
            "physical transport guard")

    clock = g3["safe_clock"]
    require(len(clock["rows"]) == 9, "clock rows")
    for row in clock["rows"]:
        expected_d = 0 if row["M"] <= 310 else row["M"] - 309
        require(row["Dbar"] == expected_d and row["R0"] == 696 * expected_d,
                "clock closed form")
    require(clock["first_jump_collision_terms"] == 1392 and
            clock["later_jump_collision_terms"] == 696, "clock term counts")
    require(clock["physical_level_trace_sum"] == "NOT_CERTIFIED", "clock physical guard")
    require(g3["moving_null_separator"]["fixed_time_null_implies_zero_current"] is False,
            "moving-null separator")
    require(g3["strong_product_rules"] == {
        "D_QPR_terms": 3,
        "D_Tn_terms": "n",
        "bounded_differentiable_physical_Rs_Qs": "NOT_CERTIFIED",
        "anisotropic_Piola": "NOT_CERTIFIED",
        "MT_DQ": "NOT_CERTIFIED",
    }, "strong product rules")
    require(g3["strict_status"] == "NOT_CERTIFIED", "Gate3 state")
    require(result["latest_technology_boundary"]["external_theorem_promoted"] is False,
            "external theorem guard")
    require(result["strict_status"] == {
        "Gate1": "NOT_CERTIFIED", "Gate3": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5", "CM2": "NO-GO_FOR_CLAIM",
    }, "strict final state")


def independent_replay() -> dict[str, Any]:
    stable = [[1, 0], [-1, 1]]
    unstable = [[1, 1], [0, 1]]
    loop = [[sum(stable[i][k] * unstable[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]
    require(loop == [[1, 1], [-1, 0]], "independent matrix product")
    det = loop[0][0] * loop[1][1] - loop[0][1] * loop[1][0]
    require(det == 1 and loop[1][0] == -1 and -loop[0][1] == -1,
            "independent loop invariants")
    distances = [Q(1, 2**n) for n in range(1, 13)]
    require(sum(distances, Q(0)) == Q(4095, 4096), "independent transport sum")
    require((0 if 310 <= 310 else 310 - 309) == 0 and 311 - 309 == 2,
            "independent clock boundary")
    return {"matrix": "PASS", "transport_rows": 12, "clock_boundary": "PASS"}


def deterministic(data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=180,
    )
    require(proc.returncode == 0, f"producer exit: {proc.stderr.decode().strip()}")
    require(proc.stdout == MANIFEST.read_bytes(), "producer bytes")
    require(strict_json_path(MANIFEST) == data, "producer object")


def run_audit(data: dict[str, Any], regenerate: bool = True) -> None:
    integrity(data)
    semantics(data["result"])
    independent_replay()
    if SIDECAR.exists():
        replay_sidecar(HERE, SIDECAR, 5)
    if regenerate:
        deterministic(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        data = strict_json_path(MANIFEST)
        if args.audit:
            run_audit(data)
            print("AUDIT: PASS")
            return 0
        if args.replay:
            integrity(data)
            semantics(data["result"])
            print(json.dumps(independent_replay(), sort_keys=True))
            return 0
        if args.self_test:
            run_audit(data)
            semantic = semantic_mutation_test(data, integrity, semantics)
            strict = strict_json_self_test()
            print(f"HOSTILE_SEMANTIC_REJECTED: {semantic}/{semantic}")
            print(f"HOSTILE_JSON_REJECTED: {strict}/{strict}")
            return 0
        if args.reemit is not None:
            run_audit(data, regenerate=False)
            proc = subprocess.run(
                [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
                cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=180,
            )
            require(proc.returncode == 0, "reemit producer")
            args.reemit.write_bytes(proc.stdout)
            require(args.reemit.read_bytes() == MANIFEST.read_bytes(), "reemit bytes")
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, ArithmeticError,
            subprocess.SubprocessError) as exc:
        print(f"ROUND64_GATE13_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate1/Gate3: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
