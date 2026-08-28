#!/usr/bin/env python3
"""Independent verifier for the Round-64 Gate-2/4 frontier."""

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
RESULT_SCHEMA = "cm2.gate24.round64.rooted-atlas-jacobian-tag-lift.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate24-round64-rooted-atlas-jacobian-tag-lift-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_gate24_round64_rooted_atlas_jacobian_tag_lift_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round64_common.py"
EXPECTED_RESULT_DIGEST = "3d65eb8f52be0a5996eb2ca3c0a67adb883ea63225f40dce407c1e425b008ed7"

PINS = {
    "cm2-sixty-third-direct-assault-2026-07-21.md":
        "9cde412ba689be87d777906404c9c9426a2a8a102385a2c4c510df8f9b7a6a05",
    "cm2-sixty-third-direct-assault-manifest-2026-07-21.sha256":
        "a0b512f32914ef2692b31466a4ea156c44698b1eaf44d8ead45b2c74ee73230e",
    "cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.json":
        "3aae6d018fc15aaab47116d311eed8333c56b87542b0b5761b849221cbf76d6b",
    "cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "8227dd32e36d2879f9dbbdced54f3c50b3eac1536ce8fceac480d22cb8617bfd",
    "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.json":
        "955908ee74ff6ec0354224978850ef683aeacd1923ce85bffd1290467321d23f",
    "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.sha256":
        "a739ffbe1bb9f14fdc8c72c573594f56930a7c4f32efb77fa4dac60d256ec870",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json":
        "e0b89d604e89852b574638428a60daa1f6e8231b85177230a5dd67615205bad1",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.sha256":
        "b94df87ba8362827bb1115f474c0beec59f887325e8db58b55a9020bf99ae6bc",
}


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
        "append_only": True, "old_artifacts_modified": False,
        "pinned_round63_and_actual_graph": PINS,
    }, "provenance")
    bridge = result["jacobian_arclength_bridge"]
    require(bridge["status"] == "CERTIFIED_EXACT_CONDITIONAL", "bridge status")
    require("rho_u(x)/(J(hx)rho_v(hx))" == bridge["lambda"], "lambda identity")
    require("j_+^2" in bridge["strict_budget"] and "a_u^2" in bridge["strict_budget"],
            "substituted budget")
    replay = bridge["replay"]
    m = Q(replay["a_u"]) / (Q(replay["j_plus"]) * Q(replay["b_v"]))
    big_m = Q(replay["b_u"]) / (Q(replay["j_minus"]) * Q(replay["a_v"]))
    require(Q(replay["m_lower"]) == m == Q(2, 35), "metric lower")
    require(Q(replay["M_upper"]) == big_m == Q(1, 8), "metric upper")
    original_left = Q(replay["F"]) * Q(replay["R"]) * big_m
    original_right = Q(replay["C_p_test"]) * m * m * Q(replay["theta"]) * Q(replay["L"])
    require(Q(replay["original_left"]) == original_left and
            Q(replay["original_right"]) == original_right and
            replay["both_strict"] is True, "bridge replay")
    scale = Q(replay["j_minus"]) * Q(replay["a_v"]) * Q(replay["j_plus"])**2 * Q(replay["b_v"])**2
    require(Q(replay["transformed_left"]) == original_left * scale and
            Q(replay["transformed_right"]) == original_right * scale, "bridge equivalence")
    require(bridge["actual_density_J_metric_rows"] == "NOT_CERTIFIED", "bridge guard")

    atlas = result["rooted_atlas_saturation"]
    require(atlas["status"] == "CERTIFIED_EXACT_COUNTABLE_INTERFACE", "atlas status")
    require(atlas["zero_iff_all_pulled_back_markers_equal"] is True and
            atlas["commuting_tree_source_landing_delta_equal"] is True, "atlas exact rows")
    a = atlas["replay"]
    require([Q(x) for x in a["weights"]] == [Q(1, 5), Q(1, 2), Q(3, 10)],
            "atlas weights")
    require([[Q(x) for x in row] for row in a["markers"]] ==
            [[Q(0), Q(1)], [Q(1), Q(3)], [Q(4), Q(0)]], "atlas markers")
    require([Q(x) for x in a["coordinate_medians"]] == [Q(1), Q(1)],
            "atlas medians")
    require([Q(x) for x in a["coordinate_costs"]] == [Q(11, 10), Q(13, 10)],
            "atlas costs")
    require(Q(a["delta_atlas"]) == Q(6, 5) and Q(a["P"]) == Q(3, 4),
            "atlas delta/P")
    require(a["strict_sandwich"] is True and Q(a["P"]) < Q(a["delta_atlas"]) < 2 * Q(a["P"]),
            "atlas sandwich")
    require(atlas["actual_root_edges_zero_defect"] == "NOT_CERTIFIED", "atlas guard")

    graph = result["graph_tag_lift"]
    require(graph["actual_round62_covariance"] == "CERTIFIED_PINNED", "actual graph pin")
    require(graph["bounded_iff"] == "W_D in L_infinity(kappa_B)", "boundedness criterion")
    separator = graph["separator"]
    require(len(separator["rows"]) == 12 and Q(separator["full_mass"]) == 1 and
            Q(separator["full_one_vector_moment"]) == 3, "separator totals")
    for row in separator["rows"]:
        n = row["n"]
        require(Q(row["kappa_mass"]) == Q(3, 4**n), "separator mass")
        require(Q(row["tag_weight"]) == Q(2**n), "separator tag")
        require(Q(row["moment_term"]) == Q(3, 2**n), "separator moment")
        require(Q(row["unit_L1_atom_lift_norm"]) == Q(2**n), "separator atom")
    require(separator["W_D_unbounded"] is True and
            separator["unit_L1_atom_lift_norm_tends_to_infinity"] is True, "unbounded guard")
    require(graph["actual_weighted_operator_bound"] == "NOT_CERTIFIED" and
            graph["physical_anisotropic_Piola_lift"] == "NOT_CERTIFIED", "physical graph guard")
    require(result["latest_technology_boundary"]["external_theorem_promoted"] is False,
            "external theorem guard")
    require(result["strict_status"] == {
        "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
        "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
        "complete_composite_gates": "0/5", "CM2": "NO-GO_FOR_CLAIM",
    }, "strict state")


def independent_replay() -> dict[str, Any]:
    weights = [Q(1, 5), Q(1, 2), Q(3, 10)]
    markers = [[Q(0), Q(1)], [Q(1), Q(3)], [Q(4), Q(0)]]
    medians = [Q(1), Q(1)]
    costs = []
    pairwise = []
    for k in range(2):
        values = [row[k] for row in markers]
        costs.append(sum((w * abs(x - medians[k]) for x, w in zip(values, weights)), Q(0)))
        pairwise.append(sum((weights[i] * weights[j] * abs(values[i] - values[j])
                             for i in range(3) for j in range(i + 1, 3)), Q(0)))
    delta = sum(costs, Q(0)) / 2
    dispersion = sum(pairwise, Q(0)) / 2
    require(delta == Q(6, 5) and dispersion == Q(3, 4), "independent atlas")
    full_mass = sum((Q(3, 4**n) for n in range(1, 80)), Q(0))
    full_moment = sum((Q(3, 2**n) for n in range(1, 80)), Q(0))
    require(full_mass < 1 and full_moment < 3, "finite separator prefixes")
    return {"delta": "6/5", "P": "3/4", "tag_separator": "PASS"}


def deterministic(data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=180,
    )
    require(proc.returncode == 0, f"producer: {proc.stderr.decode().strip()}")
    require(proc.stdout == MANIFEST.read_bytes() and strict_json_path(MANIFEST) == data,
            "deterministic producer")


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
        print(f"ROUND64_GATE24_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate2/Gate4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
