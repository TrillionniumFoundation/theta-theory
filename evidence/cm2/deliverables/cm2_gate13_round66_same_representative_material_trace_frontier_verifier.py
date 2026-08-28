#!/usr/bin/env python3
"""Independent verifier for the Round-66 Gate-1/3 frontier."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round66_common import (
    CertError, digest, replay_sidecar, require, semantic_mutation_test,
    sha256_path, strict_json_path, strict_json_self_test, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate13.round66.same-representative-material-trace-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate13-round66-same-representative-material-trace-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_gate13_round66_same_representative_material_trace_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round66_common.py"
EXPECTED_RESULT_DIGEST = "0804794d92f9f0bb4e02fb5426e186406eefcd99929e2d11de90de998bc3b402"

PINS = {
    "cm2-sixty-fifth-direct-assault-2026-07-21.md":
        "aeaafaf3411e90d6d1843159e248f18af12e5fdf993acfb9685adcc1b14e7bb0",
    "cm2-sixty-fifth-direct-assault-manifest-2026-07-21.sha256":
        "22283d37c12651e955b2502ad7660fa22d309c1d1902c471b1527470d6cc1cc2",
    "cm2-round65-independent-core-frontier-audit-2026-07-21.md":
        "b33405043f505f3f6323a6faf0de8f33e3f4c1f28db7ac891a56b2242a4df9e4",
    "cm2-round65-independent-core-frontier-audit-manifest-2026-07-21.json":
        "92ba883654f761a4df5974d889f99aa077769bb37ba0cd5d6fd03ceb8470629f",
    "cm2-round65-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "56cdbe5748338979e03eca9a859f119fda8c88d7b6663f530400f00f69583ed9",
    "cm2-gate13-round65-actual-cross-tail-piola-current-frontier-assault-2026-07-21.md":
        "634eb5d96d5837fb1a09f6c87d18b362a35d62be296c8a516d6e9ad648a016a8",
    "cm2-gate13-round65-actual-cross-tail-piola-current-frontier-manifest-2026-07-21.json":
        "e87bb0896c1fc59b6b020d1325bd9462fd932f5d186acabb0fcf770ed9b34701",
    "cm2-gate13-round65-actual-cross-tail-piola-current-frontier-manifest-2026-07-21.sha256":
        "1adc6c78ae09bfd0113271794d5a99ad95655297e54e248c87c16eddbab6ab49",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-assault-2026-07-21.md":
        "9bcf25242a4190e591919bd38233da4e036be22fc2c84739540a555f5f56b0ab",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.json":
        "f731715bd734649073e0bd35763c170a48ef8383f6dd892696b52a98ea86eb14",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.sha256":
        "ba3e550ac55d7e482d15817cdb9011c7a118100d90158d1c7aabdfeb94785b5a",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-assault-2026-07-20.md":
        "43f50426abfc92e041903af4d4eb6a416d686ea7ad25ad0f013bb56cd9f4110d",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.json":
        "16a2562868df58b2e14bf672d2d0d11735581016ff50e10f5a6d2c1e660d3466",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.sha256":
        "985910708fe715d0c891cd6a288b37a5e1b88530db858a712e7e82e80cbb4b71",
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-assault-2026-07-21.md":
        "3b75e26e9f5ec518e621b5c575ddddb5d7b66254ada4cb87ecec8bbaac788751",
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.json":
        "eb9e086e973866beaba19111a74e67772f5b0998bbee7c43f06c273c96c68fe2",
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.sha256":
        "14e13e71fbe1a9c0ed1ef8524da549939417c8406fa60a78f60d56e45deab450",
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-assault-2026-07-21.md":
        "c4c1574e546900947a9248275f8a8be16d5b67e6e186c04b818da05fe4900f3a",
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-manifest-2026-07-21.json":
        "df730945a80aad801b5923729e5c8239148b040a6983cf001e19ad569d880880",
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-manifest-2026-07-21.sha256":
        "c7552aa293baad4a021f85bff9c5cba3a15001d78a3e103e6f89cfc2b7c44319",
    "cm2-gate13-round64-resonant-tail-transport-current-clock-frontier-assault-2026-07-21.md":
        "338f2aebff9501e8457d978898dc8c1cd9bfe06e1cc9a3d720bba7163d78cdeb",
    "cm2-gate13-round64-resonant-tail-transport-current-clock-frontier-manifest-2026-07-21.json":
        "81a994f232af17d050a1582c396f8deeaae09e86856b5290e5eda764a238d4b8",
    "cm2-gate13-round64-resonant-tail-transport-current-clock-frontier-manifest-2026-07-21.sha256":
        "55fd5b62f3bab1fbea0c3334b4264176ab0bde8f140f3b7241d131b684756722",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-assault-2026-07-16.md":
        "35f0632a29c93b639120cdffe5720b5d4ba282b02b3a247b476fcfb8f1ab4925",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json":
        "4b9baaacaf7a315659448072d8d382bc90c4b41a9d98746b63c786f206ad449a",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.sha256":
        "c446a1a0f9ef2c67871181a96e4dc6d0bdf7890b739a6f9a2bba13ef6fd5b37b",
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def integrity(data: dict[str, Any], check_artifacts: bool = True) -> None:
    require(data.get("schema") == MANIFEST_SCHEMA, "manifest schema")
    require(data.get("pins") == PINS, "manifest pins")
    validate_pins(HERE, PINS)
    if check_artifacts:
        require(data.get("report_sha256") == sha256_path(REPORT), "report hash")
        require(data.get("certificate_sha256") == sha256_path(CERT), "certificate hash")
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
    require(result.get("schema") == RESULT_SCHEMA, "result schema")
    replay = copy.deepcopy(result)
    recorded = replay.pop("internal_replay_digest", None)
    require(recorded == EXPECTED_RESULT_DIGEST and digest(replay) == EXPECTED_RESULT_DIGEST,
            "semantic digest")
    require(result["provenance"] == {
        "append_only": True,
        "old_artifacts_modified": False,
        "direct_pin_count": 26,
        "pins": PINS,
    }, "provenance")

    g1 = result["gate1"]
    audit = g1["frozen_same_gauge_audit"]
    require(audit["shared_triangular_syntax_implies_same_gauge"] is False and
            audit["lawful_frozen_QNL_to_T_n_transport"] is False and
            audit["same_scalar_functions"] == "NOT_CERTIFIED" and
            audit["same_orbit_plaque_gauge_key"] == "NOT_CERTIFIED",
            "same-gauge audit")
    transfer = g1["relative_shear_transfer"]
    require(transfer["status"] == "CERTIFIED_EXACT_IFF" and
            transfer["identity_iff"] == "v_c-v_q=0 and u_c=u_q" and
            transfer["models"][0]["is_identity"] is True and
            transfer["models"][1] == {
                "u_q": "1/2", "v_q": "1/3", "u_c": "2/3", "v_c": "5/6",
                "delta_v": "1/2", "matrix": [["4/3", "1/2"], ["0", "3/4"]],
                "determinant": "1", "is_identity": False,
            }, "relative transfer")
    tails = g1["all_plaque_tail_transport"]
    require(tails["status"] == "CERTIFIED_EXACT_IFF_ON_COMMON_REGISTRY" and
            tails["zero_tail_required"] is False and
            tails["actual_common_registry"] == "NOT_CERTIFIED",
            "tail iff")
    loop = g1["selected_loop_transport"]
    require(loop["status"] == "CERTIFIED_EXACT_IFF" and
            loop["exact_source_loop_transport_iff"] ==
            "H_A^s L_u+L_s H_A^u+L_s L_u=0" and
            loop["diagonal_source_exact_transport_iff"] ==
            "l=0 and u=0 when a*b!=0" and
            loop["models"][0]["vanishes"] is True and
            loop["models"][1]["correction"] == [["0", "2"], ["-3/2", "-1/2"]] and
            loop["models"][1]["vanishes"] is False,
            "loop transport")
    require(g1["minimal_keyed_registry"]["status"] == "0/8_ACTUAL_COMMON_ROWS" and
            len(g1["minimal_keyed_registry"]["rows"]) == 8 and
            g1["strict_status"] == "NOT_CERTIFIED", "Gate1 boundary")

    g3 = result["gate3"]
    atlas = g3["physical_compact_interior_atlas"]
    require(atlas["status"] == "CERTIFIED_LOCAL" and
            atlas["contact_tau_derivative"] == "2 R_i (u_j dot n_(j+1))" and
            atlas["all_cells_all_depth_common_s_window"] == "NOT_CERTIFIED" and
            atlas["physical_anisotropic_recipient"] == "NOT_CERTIFIED",
            "local atlas")
    remainder = g3["direct_sum_uniform_remainder"]
    require(remainder["status"] == "CERTIFIED_EXACT_IFF" and
            remainder["uniform_o_s_iff"] == "sup_k epsilon_k(s)->0" and
            remainder["each_fixed_branch_converges"] is True and
            remainder["global_uniform_remainder"] is False and
            len(remainder["rows"]) == 6,
            "uniform remainder")
    for n, row in zip((2, 4, 8, 16, 32, 64), remainder["rows"]):
        require(row == {
            "N": n, "s": qstr(Q(1, n)),
            "fixed_branch_k_1_remainder": qstr(Q(1, n)), "global_supremum": "1",
        }, f"remainder row {n}")
    require(g3["material_trace_join"] == {
        "status": "CERTIFIED_EXACT_TYPED_INTERFACE",
        "persistent_requirement": "direct-sum uniform remainder",
        "topology_requirement": "Gamma:X->ell1(face/side tags) bounded",
        "disjoint_tags_prevent_cross_cancellation": True,
        "clock_and_cemetery_remain_separate": True,
        "actual_join": "NOT_CERTIFIED",
    }, "material trace join")
    stopped = g3["stopped_generating_function"]
    require(stopped["status"] == "CERTIFIED_EXACT_POSITIVE_SCALAR_CRITERION" and
            stopped["positive_tagged_scalar_iff"] is True and
            stopped["finite_for_M_lt_1"] is True and
            stopped["diverges_at_M_eq_1"] is True and
            stopped["actual_common_strong_M_lt_1"] == "NOT_CERTIFIED" and
            len(stopped["rows"]) == 6,
            "stopped criterion")
    for cutoff, row in zip((1, 2, 4, 8, 16, 32), stopped["rows"]):
        at_one = sum((Q(1, n + 1) for n in range(1, cutoff + 1)), Q(0))
        at_half = sum((Q(1, 2) ** (n - 1) / Q(n + 1)
                       for n in range(1, cutoff + 1)), Q(0))
        require(row == {
            "cutoff": cutoff,
            "P_prime_at_1_partial": qstr(at_one),
            "P_prime_at_half_partial": qstr(at_half),
        }, f"depth row {cutoff}")
    require(g3["minimal_physical_registry"]["physical_MT_DQ"] == "NOT_CERTIFIED" and
            g3["strict_status"] == "NOT_CERTIFIED", "Gate3 boundary")
    require(result["latest_same_type_technology_audit"]["external_theorem_promoted"] is False,
            "technology promotion")
    require(result["strict_status"] == {
        "Gate1": "NOT_CERTIFIED", "Gate3": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5", "CM2": "NO-GO_FOR_CLAIM",
    }, "strict state")


def independent_replay() -> dict[str, Any]:
    uq, vq, uc, vc = Q(1, 2), Q(1, 3), Q(2, 3), Q(5, 6)
    dv = vc - vq
    matrix = [[1 + dv * uc, dv], [uc - uq * (1 + dv * uc), 1 - uq * dv]]
    require(matrix == [[Q(4, 3), Q(1, 2)], [Q(0), Q(3, 4)]], "independent C")
    require(matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0] == 1,
            "independent det")
    a, b, ell, u = Q(2), Q(3), Q(-1, 2), Q(1)
    correction = [[Q(0), a * u], [ell * b, ell * u]]
    require(correction == [[Q(0), Q(2)], [Q(-3, 2), Q(-1, 2)]],
            "independent loop correction")
    half_32 = sum((Q(1, 2) ** (n - 1) / Q(n + 1) for n in range(1, 33)), Q(0))
    one_32 = sum((Q(1, n + 1) for n in range(1, 33)), Q(0))
    require(half_32 < 1 and one_32 > 3, "depth contrast")
    return {
        "relative_transfer": [[qstr(v) for v in row] for row in matrix],
        "loop_correction": [[qstr(v) for v in row] for row in correction],
        "P_prime_half_cutoff_32": qstr(half_32),
        "P_prime_one_cutoff_32": qstr(one_32),
    }


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
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        data = strict_json_path(MANIFEST)
        if args.audit or args.verify:
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
        print(f"ROUND66_GATE13_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate1/Gate3: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
