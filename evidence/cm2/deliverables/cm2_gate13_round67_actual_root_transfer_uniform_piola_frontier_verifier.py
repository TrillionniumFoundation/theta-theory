#!/usr/bin/env python3
"""Independent verifier for the Round-67 Gate-1/3 frontier."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round67_common import (
    CertError, digest, replay_sidecar, require, semantic_mutation_test,
    sha256_path, strict_json_path, strict_json_self_test, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate13.round67.actual-root-transfer-uniform-piola-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate13-round67-actual-root-transfer-uniform-piola-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_gate13_round67_actual_root_transfer_uniform_piola_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round67_common.py"
EXPECTED_RESULT_DIGEST = "ab9e49a674afc469d0f2d0d1d8b6563e669aee50895fd594219e4ea069e966e6"

PINS = {
    "cm2-sixty-sixth-direct-assault-2026-07-21.md":
        "690cfeb13108314a3a05f5e4cd342d573c41e66551464ebf7f4b5576f374b811",
    "cm2-sixty-sixth-direct-assault-manifest-2026-07-21.sha256":
        "b437761fb84aa431e468af587e2207adadf6e0a996ee593a93df467147be3b5d",
    "cm2-round66-independent-core-frontier-audit-2026-07-21.md":
        "68d9b65f843c6e35e9f8c5e6954fb76e87970fc9bc558e691cecaafeb9850ebd",
    "cm2-round66-independent-core-frontier-audit-manifest-2026-07-21.json":
        "b67b76e52d073989fac6fb41eaf3e49167aa1e166d32003c72129e08ec6d46b3",
    "cm2-round66-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "6d09b81b683464dcf45815ed9e98635c6c3a94087c19b0e4528eaf4c1659175e",
    "cm2-gate13-round66-same-representative-material-trace-frontier-assault-2026-07-21.md":
        "6d37428dde6b8360d759554a9bcd2bfeb91b0c67c0ab3bcc98d91d850fa49278",
    "cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.json":
        "11bb7ba12e3302a547893dae3a897efc5a66223bbc2cf740bb6f7b5e53882224",
    "cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.sha256":
        "4d38f3145099b2cd4222930d32c88dd7ba6bc9797def4673fc9ea00415f3b38e",
    "cm2-gate1-global-coding-class-h-separation-frontier-assault-2026-07-16.md":
        "7ec0d1545ac7ebc52a03ac871adfe10fb7a9b7a070a9d91ee3fcf116d8edfda2",
    "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.json":
        "1e61f6f600300d15a15cf04179ee6e889ceb09edcf3d3b26f0d6f735afd6bdec",
    "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.sha256":
        "2187c87105f2b86c9906856733fa025763981b852e54ed0715ba3934dc515d0f",
    "cm2-gate1-variable-diagonal-groupoid-frontier-assault-2026-07-17.md":
        "bbee54be4aea1df1d9b00a8a97145029ee68fd538aa44931dd2b21d1644c1fdd",
    "cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.json":
        "dacbae6255707086bc7486e4933d8c890ede1547a9e545995800a5fc18698f83",
    "cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.sha256":
        "9d98591462771a9e553dd93c24518642c22aa2832c269a8380bd827a76666200",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-assault-2026-07-16.md":
        "35f0632a29c93b639120cdffe5720b5d4ba282b02b3a247b476fcfb8f1ab4925",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json":
        "4b9baaacaf7a315659448072d8d382bc90c4b41a9d98746b63c786f206ad449a",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.sha256":
        "c446a1a0f9ef2c67871181a96e4dc6d0bdf7890b739a6f9a2bba13ef6fd5b37b",
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
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def matmul(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    return [[sum((a[i][k] * b[k][j] for k in range(2)), Q(0))
             for j in range(2)] for i in range(2)]


def det(a: list[list[Q]]) -> Q:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv(a: list[list[Q]]) -> list[list[Q]]:
    d = det(a)
    require(d != 0, "independent singular matrix")
    return [[a[1][1] / d, -a[0][1] / d], [-a[1][0] / d, a[0][0] / d]]


def path_ledger(m: list[Q], ell: list[Q]) -> Q:
    total = Q(0)
    for r, lr in enumerate(ell):
        product = Q(1)
        for i, mi in enumerate(m):
            if i != r:
                product *= mi
        total += lr * product
    return total


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
        "append_only": True, "old_artifacts_modified": False,
        "direct_pin_count": len(PINS), "pins": PINS,
    }, "provenance")

    g1 = result["gate1"]
    root = g1["maximal_actual_root_crosswalk"]
    require(root["status"] == "CERTIFIED_ACTUAL_ROOT_AND_EXACT_FORMAL_TRANSFER" and
            root["relative_transfer"] == "C=Q^-1 E D" and
            root["cohomology"] == "A_c=C(sigma x)^-1 A_q C(x)" and
            root["same_root_tokens"] == "CERTIFIED" and
            root["same_physical_derivative_cocycle"] == "CERTIFIED" and
            root["same_key_Q_E_u_v_rows"] == "NOT_CERTIFIED" and
            root["rational_replay"]["det_C"] == "1", "root crosswalk")
    separator = g1["endpoint_completion_separator"]
    require(separator["status"] == "CERTIFIED_SHARP_NONDETERMINATION" and
            separator["selected_constants_determine_actual_endpoint_limits"] is False and
            len(separator["rows"]) == 8, "endpoint separator")
    for n, row in enumerate(separator["rows"], start=1):
        require(row["n"] == n and row["renormalized_zero"] == "0" and
                row["renormalized_constant"] == "1" and
                row["renormalized_oscillatory"] == str((-1) ** n),
                f"endpoint row {n}")
    wedge = g1["wedge_transport_boundary"]
    require(wedge["simultaneous_exact_transport_preserves_nonzero_wedges"] is True and
            wedge["actual_tail_limits"] == "NOT_CERTIFIED" and
            wedge["actual_four_wedges_in_combined_family"] == "NOT_CERTIFIED" and
            g1["strict_status"] == "NOT_CERTIFIED", "wedge boundary")

    g3 = result["gate3"]
    window = g3["common_material_window"]
    require(window["radius_definition"] ==
            "r_k is the supremal admissible connected material radius for branch k" and
            window["criterion"] == "r_*=inf_k r_k>0" and
            window["actual_all_cell_all_depth_infimum"] == "NOT_CERTIFIED" and
            window["rows"][-1] == {"finite_cutoff": 32, "minimum_radius": "1/32"},
            "material window")
    weighted = g3["weighted_direct_sum"]
    require(weighted["status"] == "CERTIFIED_EXACT_IFF" and
            weighted["replay_supremum"] == "2" and len(weighted["rows"]) == 3 and
            weighted["actual_uniform_weighted_remainder"] == "NOT_CERTIFIED",
            "weighted direct sum")
    composition = g3["three_factor_uniform_piola"]
    require(composition["scalar_derivative"] == "293" and
            composition["product_differentiability_implies_each_factor"] is False and
            composition["actual_strong_Rhat_Phat_Qhat"] == "NOT_CERTIFIED",
            "three factor composition")
    trace = g3["side_tagged_trace_current"]
    require(trace["status"] == "CERTIFIED_EXACT_IFF" and
            trace["side_tags_disjoint"] is True and
            trace["signed_cross_side_cancellation_allowed"] is False and
            trace["replay_total"] == "47/2", "tagged trace")
    stopped = g3["nonautonomous_stopped_MT_DQ"]
    require(stopped["status"] == "CERTIFIED_EXACT_POSITIVE_SCALAR_AND_SHARP_MAJORANT" and
            stopped["good_bound"] == "A_n<=4 n^2 2^-n despite sup_i M_i=1" and
            stopped["spike_lower_bound"] == "A_n>=2n, so p_n=1/[n(n+1)] diverges" and
            stopped["physical_MT_DQ"] == "NOT_CERTIFIED" and len(stopped["rows"]) == 6,
            "nonautonomous stopped ledger")
    require(g3["strict_status"] == "NOT_CERTIFIED", "Gate3 status")
    require(result["latest_same_type_technology_audit"]["external_theorem_promoted"] is False,
            "technology promotion")
    require(result["strict_status"] == {
        "Gate1": "NOT_CERTIFIED", "Gate3": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5", "CM2": "NO-GO_FOR_CLAIM",
    }, "strict state")


def independent_replay() -> dict[str, Any]:
    q_matrix = [[Q(1), Q(1, 2)], [Q(0), Q(1)]]
    e_matrix = [[Q(2), Q(1)], [Q(1), Q(1)]]
    d_matrix = [[Q(13, 12), Q(1, 4)], [Q(1, 3), Q(1)]]
    c_matrix = matmul(matmul(inv(q_matrix), e_matrix), d_matrix)
    require(det(q_matrix) == det(e_matrix) == det(d_matrix) == det(c_matrix) == 1,
            "independent relative determinants")
    require(c_matrix == [[Q(43, 24), Q(7, 8)], [Q(17, 12), Q(5, 4)]],
            "independent relative transfer")

    for n in range(1, 9):
        amplitude = Q((-1) ** n, 4 ** n)
        require(amplitude * Q(4 ** n) == (-1) ** n, f"independent defect {n}")

    weighted = [Q(2) * Q(1, 3) / Q(1), Q(1) * Q(4) / Q(2),
                Q(8) * Q(1, 2) / Q(4)]
    require(weighted == [Q(2, 3), Q(2), Q(1)], "independent weighted norms")

    good_m = [Q(1) if ((i + 1) & i) == 0 else Q(1, 2) for i in range(32)]
    good_l = [Q(1) for _ in range(32)]
    spike_m = [Q(1, 2) for _ in range(32)]
    spike_l = [Q(2 ** (i + 1) * (i + 1)) for i in range(32)]
    good = path_ledger(good_m, good_l)
    spike = path_ledger(spike_m, spike_l)
    require(good <= Q(4 * 32 * 32, 2 ** 32), "independent good bound")
    require(spike >= 64, "independent spike lower bound")
    return {
        "relative_C": [[qstr(v) for v in row] for row in c_matrix],
        "weighted_norms": [qstr(v) for v in weighted],
        "good_A_32": qstr(good), "spike_A_32": qstr(spike),
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
        print(f"ROUND67_GATE13_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate1/Gate3: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
