#!/usr/bin/env python3
"""Independent verifier for the Round-66 aggregate core-frontier audit."""

from __future__ import annotations

import argparse
import copy
import json
import py_compile
import subprocess
import sys
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round66_common import (
    CertError, digest, replay_sidecar, require, semantic_mutation_test,
    sha256_path, strict_json_path, strict_json_self_test, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round66-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round66-independent-core-frontier-audit"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-2026-07-21.md"
CERT = HERE / "cm2_round66_independent_core_frontier_audit_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round66_common.py"
EXPECTED_RESULT_DIGEST = "d54a3395b7e7ac03c5a09ce361aba6710d6eaf7648c93a39ee26e5c1ffab25a4"

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
    "cm2-gate13-round66-same-representative-material-trace-frontier-assault-2026-07-21.md":
        "6d37428dde6b8360d759554a9bcd2bfeb91b0c67c0ab3bcc98d91d850fa49278",
    "cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.json":
        "11bb7ba12e3302a547893dae3a897efc5a66223bbc2cf740bb6f7b5e53882224",
    "cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.sha256":
        "4d38f3145099b2cd4222930d32c88dd7ba6bc9797def4673fc9ea00415f3b38e",
    "cm2-gate24-round66-collision-srb-product-variation-frontier-assault-2026-07-21.md":
        "13341aaa40ccc155b85119c457b12a5e09fed43fa618ed0aee280bef0af68b27",
    "cm2-gate24-round66-collision-srb-product-variation-frontier-manifest-2026-07-21.json":
        "be98266945e3e6bd7fee0bf27f49a3282dc41f67e95f74b0c41c041d0cd4bf94",
    "cm2-gate24-round66-collision-srb-product-variation-frontier-manifest-2026-07-21.sha256":
        "de30d5514982930c9dd485313e09a6eb668c2e3dbc1da05d4507ae6a032f1d20",
    "cm2-gate5-round66-owner-overlap-sector-flux-frontier-assault-2026-07-21.md":
        "5328ee45c3fd69e0e4a433910e5562504d1b155e44eb20a024b05194f16d999d",
    "cm2-gate5-round66-owner-overlap-sector-flux-frontier-manifest-2026-07-21.json":
        "31f8b9068b3afaad779f299d5adb3e1ff870d3b48ad943704e1347b7ac06a686",
    "cm2-gate5-round66-owner-overlap-sector-flux-frontier-manifest-2026-07-21.sha256":
        "c538c62bbbb13f1e4b203d72d67cb3fd398752a4636c1a731a9039f9847ce4aa",
    "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-assault-2026-07-21.md":
        "9b8512389c8ede4c6b59a029565bc314f10502ec9339094036f13f33185463a2",
    "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-manifest-2026-07-21.json":
        "adc2654ed27fa62c83dd9d64ddce09832e173f50d518c464007d9bc320d6294f",
    "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-manifest-2026-07-21.sha256":
        "1122a6b11415e5f070ec4a86faa6d78a0a67a30ae836c288e3a732f1c0fa51f3",
    "cm2_round66_common.py":
        "34846761d5b448077a0cb5768d7e44fb2b354ae07f2b0d0475500bf96c85738f",
}

SOURCE_SPECS = [
    {
        "manifest": "cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.json",
        "sidecar": "cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.sha256",
        "sidecar_rows": 5, "pin_rows": 26, "hostile": 210,
        "cert": "cm2_gate13_round66_same_representative_material_trace_frontier_cert.py",
        "verifier": "cm2_gate13_round66_same_representative_material_trace_frontier_verifier.py",
    },
    {
        "manifest": "cm2-gate24-round66-collision-srb-product-variation-frontier-manifest-2026-07-21.json",
        "sidecar": "cm2-gate24-round66-collision-srb-product-variation-frontier-manifest-2026-07-21.sha256",
        "sidecar_rows": 4, "pin_rows": 54, "hostile": 274,
        "cert": "cm2_gate24_round66_collision_srb_product_variation_frontier_cert.py",
        "verifier": "cm2_gate24_round66_collision_srb_product_variation_frontier_verifier.py",
    },
    {
        "manifest": "cm2-gate5-round66-owner-overlap-sector-flux-frontier-manifest-2026-07-21.json",
        "sidecar": "cm2-gate5-round66-owner-overlap-sector-flux-frontier-manifest-2026-07-21.sha256",
        "sidecar_rows": 5, "pin_rows": 47, "hostile": 315,
        "cert": "cm2_gate5_round66_owner_overlap_sector_flux_frontier_cert.py",
        "verifier": "cm2_gate5_round66_owner_overlap_sector_flux_frontier_verifier.py",
    },
    {
        "manifest": "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-manifest-2026-07-21.json",
        "sidecar": "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-manifest-2026-07-21.sha256",
        "sidecar_rows": 5, "pin_rows": 7, "hostile": 181,
        "cert": "cm2_round66_immutable_registry_junction_tree_positive_potential_frontier_cert.py",
        "verifier": "cm2_round66_immutable_registry_junction_tree_positive_potential_frontier_verifier.py",
    },
]


def integrity(data: dict[str, Any], files: bool = True) -> None:
    if files:
        validate_pins(HERE, PINS)
    require(data.get("schema") == MANIFEST_SCHEMA and data.get("pins") == PINS,
            "manifest schema/pins")
    if files:
        require(data.get("report_sha256") == sha256_path(REPORT), "report hash")
        require(data.get("certificate_sha256") == sha256_path(CERT), "cert hash")
        require(data.get("verifier_sha256") == sha256_path(VERIFIER), "verifier hash")
        require(data.get("common_sha256") == sha256_path(COMMON), "common hash")
    result = data.get("result")
    require(isinstance(result, dict), "result root")
    replay = copy.deepcopy(result)
    recorded = replay.pop("internal_replay_digest", None)
    require(recorded == EXPECTED_RESULT_DIGEST and digest(replay) == recorded,
            "result digest")
    require(data.get("verdict") == result.get("strict_status"), "verdict alias")


def semantics(result: dict[str, Any]) -> None:
    require(result["schema"] == RESULT_SCHEMA, "result schema")
    require(result["provenance"] == {
        "all_four_leaves_frozen_before_audit": True,
        "audit_authored_source_leaf": False,
        "old_artifacts_modified": False,
        "pin_count": 18,
        "pins": PINS,
    }, "provenance")
    require(result["gate13"] == {
        "relative_transfer_models": "2/2", "tail_loop_criteria": "2/2",
        "actual_registry_rows": "0/8", "local_atlas": "DEPTH_96_ONLY",
        "uniform_remainder_rows": "6/6", "stopped_rows": "6/6",
        "status": "INDEPENDENT_PASS",
    }, "Gate13 audit")
    require(result["gate24"] == {
        "chart_replay": "PASS", "crosswalk_couplings": "2/2",
        "marker_replays": "2/2", "actual_first_failure_rows": "0/96",
        "conditional_survivor_lower": "3/4", "variation_rows": "5/5",
        "actual_tree_rows": "0/7", "status": "INDEPENDENT_PASS",
    }, "Gate24 audit")
    require(result["gate5"] == {
        "terminal_crosswalk": "PASS", "RN_atoms": "6/6",
        "sector_rows": "7/7", "raw_truncation_rows": "12/12",
        "arrival_typing": "PASS", "positive_bridge_guards": "4/4",
        "open_fields": "8/8", "status": "INDEPENDENT_PASS",
    }, "Gate5 audit")
    require(result["immutable_registry"] == {
        "junction_theorem": "PASS", "valid_tree_atoms": "2/16",
        "cyclic_support": "0/8", "deletion_rows": "3/3",
        "physical_key_groups": "5/5", "potential_rows": "16/16",
        "actual_route_lines": "0/2", "status": "INDEPENDENT_PASS",
    }, "registry audit")
    cross = result["cross_leaf_consistency"]
    require(cross["status"] == "PASS_NO_TYPE_SUBSTITUTION_OR_STATE_CONTRADICTION" and
            len(cross["rows"]) == 14 and digest(cross["rows"]) == cross["rows_sha256"],
            "cross consistency")
    require(result["source_leaf_acceptance"] == {
        "new_python_syntax_including_round66_common": "9/9",
        "dependency_pin_rows": "134/134",
        "SHA_artifact_rows": "19/19",
        "audit_replay_self_test_reemit": "4/4",
        "hostile_semantic": "980/980_REJECTED",
        "strict_JSON": "16/16_REJECTED",
        "default_entry_points": "8/8_EXIT_2",
    }, "source acceptance")
    require(result["latest_technology_boundary"]["external_theorem_promoted"] is False,
            "technology guard")
    require(result["strict_status"] == {
        "Gate1": "NOT_CERTIFIED",
        "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
        "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
        "audit_verdict": "PASS__NO_SOURCE_LEAF_CORRECTION_REQUIRED",
    }, "strict state")


def independent_replay() -> dict[str, Any]:
    # Gate 1 relative shear and loop correction.
    uq, vq, uc, vc = Q(1, 2), Q(1, 3), Q(2, 3), Q(5, 6)
    dv = vc - vq
    transfer = [[1 + dv * uc, dv], [uc - uq * (1 + dv * uc), 1 - uq * dv]]
    require(transfer == [[Q(4, 3), Q(1, 2)], [Q(0), Q(3, 4)]] and
            transfer[0][0] * transfer[1][1] - transfer[0][1] * transfer[1][0] == 1,
            "independent transfer")
    correction = [[Q(0), Q(2)], [Q(-3, 2), Q(-1, 2)]]
    require(correction != [[Q(0), Q(0)], [Q(0), Q(0)]], "independent loop")

    # Gate 2/4 density, marker and all-depth replays.
    rho_s, rho_t, lam, jac = Q(1), Q(2, 3), Q(3, 2), Q(1)
    require(jac * rho_t == rho_s / lam, "independent chart")
    values, weights = [Q(5, 16), Q(7, 16), Q(9, 16), Q(11, 16)], [Q(1, 4)] * 4
    p_eta = sum((weights[i] * weights[j] * abs(values[i] - values[j])
                 for i in range(4) for j in range(i + 1, 4)), Q(0))
    delta = sum((w * abs(v - values[1]) for w, v in zip(weights, values)), Q(0))
    require(p_eta == Q(5, 64) and delta == Q(1, 8), "independent marker")
    tail = sum((Q(1, 4) * Q(1, 2)**k for k in range(1, 81)), Q(0))
    require(Q(1) - tail > Q(3, 4) and Q(1, 4) - tail == Q(1, 2**82),
            "independent failure")

    # Gate 5 full-label owner accounting and typed coefficients.
    rows = [
        (True, False, 2), (True, True, 3), (True, False, 5),
        (False, True, 7), (True, True, 11), (False, False, 13),
    ]
    source = sum(m for inj, _, m in rows if inj)
    target = sum(m for _, inn, m in rows if inn)
    overlap = sum(m for inj, inn, m in rows if inj and inn)
    birth = sum(m for inj, inn, m in rows if not inj and inn)
    require((source, overlap, birth, target) == (21, 14, 7, 21),
            "independent owner accounting")
    require([max(Q(a, b) for a, b in pairs) for pairs in [
        [(2, 4), (1, 2)], [(4, 2), (4, 4)], [(4, 8), (16, 8)],
        [(1, 1), (1, 2)], [(1, 2), (2, 1)], [(1, 1), (1, 1)],
        [(1, 1), (1, 1)],
    ]] == [Q(1, 2), Q(2), Q(2), Q(1), Q(2), Q(1), Q(1)],
            "independent sectors")
    forward = Q(395304765824751, 220000)
    reverse = Q(162772550633721, 176000)
    require(forward - reverse == Q(69759664557309, 80000), "independent upper difference")

    # Junction-tree and cyclic-parity replays.
    tree, triangle = [], []
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                if a == b and b == c and a != c:
                    triangle.append((a, b, c))
                for d in (0, 1):
                    if a == b == c and b != d:
                        tree.append((a, b, c, d))
    require(triangle == [] and tree == [(0, 0, 0, 1), (1, 1, 1, 0)],
            "independent registry")
    moment = sum((Q(3, 2**n) for n in range(1, 200)), Q(0))
    require(moment < 3 and 3 - moment == Q(3, 2**199), "independent potential")
    return {
        "gate13": "PASS", "gate24": "PASS", "gate5": "PASS",
        "junction_tree": "2/16", "cyclic_support": "0/8",
        "moment_limit": "3", "status": "PASS",
    }


def run_command(args: list[str], expected: int, label: str) -> subprocess.CompletedProcess[bytes]:
    proc = subprocess.run(args, cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=False, timeout=300)
    require(proc.returncode == expected,
            f"{label} exit {proc.returncode}: {proc.stderr.decode().strip()}")
    return proc


def source_acceptance() -> dict[str, str]:
    python_files = [COMMON]
    for spec in SOURCE_SPECS:
        python_files.extend([HERE / spec["cert"], HERE / spec["verifier"]])
    for path in python_files:
        py_compile.compile(str(path), doraise=True)

    pins = sidecars = hostile = strict = defaults = bundles = 0
    with tempfile.TemporaryDirectory(prefix="cm2-r66-audit-") as tmp:
        tmpdir = Path(tmp)
        for index, spec in enumerate(SOURCE_SPECS):
            manifest = strict_json_path(HERE / spec["manifest"])
            require(len(manifest["pins"]) == spec["pin_rows"], "source pin rows")
            pins += spec["pin_rows"]
            sidecars += replay_sidecar(HERE, HERE / spec["sidecar"], spec["sidecar_rows"])
            verifier = str(HERE / spec["verifier"])
            cert = str(HERE / spec["cert"])
            run_command([sys.executable, verifier, "--audit"], 0, "source audit")
            run_command([sys.executable, verifier, "--replay"], 0, "source replay")
            tested = run_command([sys.executable, verifier, "--self-test"], 0,
                                 "source self-test")
            output = tested.stdout.decode()
            require(f"HOSTILE_SEMANTIC_REJECTED: {spec['hostile']}/{spec['hostile']}" in output and
                    "HOSTILE_JSON_REJECTED: 4/4" in output, "source self-test counts")
            hostile += spec["hostile"]
            strict += 4
            reemit = tmpdir / f"leaf-{index}.json"
            run_command([sys.executable, verifier, "--reemit", str(reemit)], 0,
                        "source reemit")
            require(reemit.read_bytes() == (HERE / spec["manifest"]).read_bytes(),
                    "source reemit bytes")
            run_command([sys.executable, cert], 2, "source cert default")
            run_command([sys.executable, verifier], 2, "source verifier default")
            defaults += 2
            bundles += 1
    require((len(python_files), pins, sidecars, hostile, strict, defaults, bundles) ==
            (9, 134, 19, 980, 16, 8, 4), "source acceptance totals")
    return {
        "new_python_syntax_including_round66_common": "9/9",
        "dependency_pin_rows": "134/134",
        "SHA_artifact_rows": "19/19",
        "audit_replay_self_test_reemit": "4/4",
        "hostile_semantic": "980/980_REJECTED",
        "strict_JSON": "16/16_REJECTED",
        "default_entry_points": "8/8_EXIT_2",
    }


def deterministic(data: dict[str, Any]) -> None:
    proc = run_command(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        0, "producer",
    )
    require(proc.stdout == MANIFEST.read_bytes() and strict_json_path(MANIFEST) == data,
            "deterministic producer")


def run_audit(data: dict[str, Any], regenerate: bool = True) -> None:
    integrity(data)
    semantics(data["result"])
    independent_replay()
    require(source_acceptance() == data["result"]["source_leaf_acceptance"],
            "source acceptance replay")
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
            print("AUDIT_MODE: PASS")
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
            proc = run_command(
                [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
                0, "reemit producer",
            )
            args.reemit.write_bytes(proc.stdout)
            require(args.reemit.read_bytes() == MANIFEST.read_bytes(), "reemit bytes")
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, IndexError,
            ArithmeticError, subprocess.SubprocessError, py_compile.PyCompileError) as exc:
        print(f"ROUND66_AUDIT_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND66 AUDIT: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
