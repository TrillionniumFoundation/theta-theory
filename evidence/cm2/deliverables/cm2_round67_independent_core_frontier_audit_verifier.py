#!/usr/bin/env python3
"""Independent verifier for the Round-67 aggregate core-frontier audit."""

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

from cm2_round67_common import (
    CertError, digest, replay_sidecar, require, semantic_mutation_test,
    sha256_path, strict_json_path, strict_json_self_test, validate_pins,
)
from cm2_round67_independent_core_frontier_audit_cert import PINS


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round67-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round67-independent-core-frontier-audit"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-2026-07-21.md"
CERT = HERE / "cm2_round67_independent_core_frontier_audit_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round67_common.py"
EXPECTED_RESULT_DIGEST = "8d244c4dd5a03ce43876756bc7d0dc3e1f02b20dde5af7d05ccfeb03fc55b51f"

SOURCE_SPECS = [
    {
        "manifest": "cm2-gate13-round67-actual-root-transfer-uniform-piola-frontier-manifest-2026-07-21.json",
        "sidecar": "cm2-gate13-round67-actual-root-transfer-uniform-piola-frontier-manifest-2026-07-21.sha256",
        "sidecar_rows": 5, "pin_rows": 26, "hostile": 283,
        "cert": "cm2_gate13_round67_actual_root_transfer_uniform_piola_frontier_cert.py",
        "verifier": "cm2_gate13_round67_actual_root_transfer_uniform_piola_frontier_verifier.py",
    },
    {
        "manifest": "cm2-gate24-round67-actual-root-stable-tail-variation-frontier-manifest-2026-07-21.json",
        "sidecar": "cm2-gate24-round67-actual-root-stable-tail-variation-frontier-manifest-2026-07-21.sha256",
        "sidecar_rows": 4, "pin_rows": 32, "hostile": 218,
        "cert": "cm2_gate24_round67_actual_root_stable_tail_variation_frontier_cert.py",
        "verifier": "cm2_gate24_round67_actual_root_stable_tail_variation_frontier_verifier.py",
    },
    {
        "manifest": "cm2-gate5-round67-direct-positive-potential-attenuation-frontier-manifest-2026-07-21.json",
        "sidecar": "cm2-gate5-round67-direct-positive-potential-attenuation-frontier-manifest-2026-07-21.sha256",
        "sidecar_rows": 5, "pin_rows": 32, "hostile": 362,
        "cert": "cm2_gate5_round67_direct_positive_potential_attenuation_frontier_cert.py",
        "verifier": "cm2_gate5_round67_direct_positive_potential_attenuation_frontier_verifier.py",
    },
    {
        "manifest": "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.json",
        "sidecar": "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.sha256",
        "sidecar_rows": 5, "pin_rows": 11, "hostile": 182,
        "cert": "cm2_round67_fixed_j_occurrence_owner_root_time_potential_frontier_cert.py",
        "verifier": "cm2_round67_fixed_j_occurrence_owner_root_time_potential_frontier_verifier.py",
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
        "actual_formal_root": "PASS", "endpoint_completion_rows": "8/8",
        "actual_endpoint_wedge_rows": "0/3", "material_window_rows": "6/6",
        "Piola_rows": "5/5", "trace_tags": "3/3", "stopped_rows": "6/6",
        "status": "INDEPENDENT_PASS",
    }, "Gate13 audit")
    require(result["gate24"] == {
        "actual_pre_registry": "PASS_LOCAL_R1_ONLY", "affine_chart": "PASS",
        "actual_tree_rows": "0/7", "hazard_rows": "0/96_FULL",
        "hazard_replays": "2/2", "immutable_anchor_join": "NOT_CERTIFIED",
        "marker_BV_guards": "3/3", "BV_remainder_rows": "5/5",
        "status": "INDEPENDENT_PASS",
    }, "Gate24 audit")
    require(result["gate5"] == {
        "direct_potential": "PASS", "conditional_terminal_model": "PASS",
        "strong_separator_rows": "12/12", "departure_rows": "12/12",
        "sector_rows": "7/7", "oriented_guards": "3/3",
        "open_fields": "8/8", "status": "INDEPENDENT_PASS",
    }, "Gate5 audit")
    require(result["fixed_j_root"] == {
        "fixed_j_subroot": "PASS", "retained_keys": "8/8",
        "time_carrier": "BOREL_ONLY", "separator_rows": "16/16",
        "actual_all_sector_potential": "NOT_CERTIFIED", "open_crosswalks": "4/4",
        "status": "INDEPENDENT_PASS",
    }, "fixed-j root audit")
    cross = result["cross_leaf_consistency"]
    require(cross["status"] == "PASS_NO_TYPE_SUBSTITUTION_OR_STATE_CONTRADICTION" and
            len(cross["rows"]) == 17 and digest(cross["rows"]) == cross["rows_sha256"] and
            "DETERMINISTIC_UNBOUNDED_TERMINAL_ELIGIBILITY_HAS_UNBOUNDED_H" in cross["rows"] and
            "CONDITIONAL_RANDOM_TERMINATION_MAY_LAWFULLY_HAVE_ESS_SUP_E_W_TO_N_FINITE" in cross["rows"],
            "cross consistency")
    require(result["source_leaf_acceptance"] == {
        "new_python_syntax_including_round67_common": "9/9",
        "dependency_pin_rows": "101/101", "SHA_artifact_rows": "19/19",
        "audit_replay_self_test_reemit": "4/4",
        "hostile_semantic": "1045/1045_REJECTED",
        "strict_JSON": "16/16_REJECTED", "default_entry_points": "8/8_EXIT_2",
    }, "source acceptance")
    require(result["independent_replay"] == {
        "gate13_transfer": "PASS", "gate24_hazards": "2/2",
        "gate5_conditional_terminal": "PASS", "fixed_j_separators": "2/2",
        "terminal_typing_consistency": "PASS",
    }, "independent replay")
    require(result["latest_technology_boundary"]["external_theorem_promoted"] is False,
            "technology guard")
    require(result["strict_status"] == {
        "Gate1": "NOT_CERTIFIED",
        "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
        "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
        "complete_composite_gates": "0/5", "CM2": "NO-GO_FOR_CLAIM",
        "audit_verdict": "PASS__NO_SOURCE_LEAF_CORRECTION_REQUIRED",
    }, "strict state")


def matmul(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    return [[sum((a[i][k] * b[k][j] for k in range(2)), Q(0))
             for j in range(2)] for i in range(2)]


def independent_replay() -> dict[str, str]:
    qinv = [[Q(1), Q(-1, 2)], [Q(0), Q(1)]]
    e = [[Q(2), Q(1)], [Q(1), Q(1)]]
    d = [[Q(13, 12), Q(1, 4)], [Q(1, 3), Q(1)]]
    c = matmul(matmul(qinv, e), d)
    require(c == [[Q(43, 24), Q(7, 8)], [Q(17, 12), Q(5, 4)]] and
            c[0][0] * c[1][1] - c[0][1] * c[1][0] == 1,
            "independent Gate13 transfer")

    ns = [1, 2, 8, 32, 96, 256]
    summable = [Q(n + 2, 2 * (n + 1)) for n in ns]
    divergent = [Q(1, n + 1) for n in ns]
    require(summable == [Q(3, 4), Q(2, 3), Q(5, 9), Q(17, 33), Q(49, 97), Q(129, 257)] and
            divergent == [Q(1, 2), Q(1, 3), Q(1, 9), Q(1, 33), Q(1, 97), Q(1, 257)],
            "independent Gate24 hazards")

    w, r = Q(3, 2), Q(1, 3)
    h_live = 1 / (1 - w * r)
    e_w_n = 1 + (w - 1) * h_live
    require(w * r == Q(1, 2) and h_live == 2 and e_w_n == 2,
            "independent conditional terminal moment")

    single = Q(3, 4) / (1 - Q(3, 8))
    e_w_n_det = 3 * Q(3, 8) / (1 - Q(3, 8))
    eligibility = (e_w_n_det - 1) / (w - 1)
    require(single == Q(6, 5) and eligibility == Q(8, 5),
            "independent fixed-j separators")
    require((w**32 - 1) / (w - 1) > 100000 and h_live == 2,
            "deterministic versus conditional terminal typing")
    return {
        "gate13_transfer": "PASS", "gate24_hazards": "2/2",
        "gate5_conditional_terminal": "PASS", "fixed_j_separators": "2/2",
        "terminal_typing_consistency": "PASS",
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
    with tempfile.TemporaryDirectory(prefix="cm2-r67-audit-") as tmp:
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
            (9, 101, 19, 1045, 16, 8, 4), "source acceptance totals")
    return {
        "new_python_syntax_including_round67_common": "9/9",
        "dependency_pin_rows": "101/101", "SHA_artifact_rows": "19/19",
        "audit_replay_self_test_reemit": "4/4",
        "hostile_semantic": "1045/1045_REJECTED",
        "strict_JSON": "16/16_REJECTED", "default_entry_points": "8/8_EXIT_2",
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
    require(independent_replay() == data["result"]["independent_replay"],
            "independent replay alias")
    require(source_acceptance() == data["result"]["source_leaf_acceptance"],
            "source acceptance replay")
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
            print("ROUND67_INDEPENDENT_AUDIT: PASS")
            print("SOURCE_PINS: 101/101")
            print("SOURCE_SHA_ROWS: 19/19")
            print("SOURCE_HOSTILE_SEMANTIC: 1045/1045_REJECTED")
            print("SOURCE_STRICT_JSON: 16/16_REJECTED")
            return 0
        if args.replay:
            integrity(data)
            semantics(data["result"])
            print(json.dumps(independent_replay(), sort_keys=True))
            return 0
        if args.self_test:
            integrity(data)
            semantics(data["result"])
            hostile = semantic_mutation_test(data, integrity, semantics)
            strict = strict_json_self_test()
            require(hostile == 96 and strict == 4, "audit self-test counts")
            print(f"HOSTILE_SEMANTIC_REJECTED: {hostile}/{hostile}")
            print(f"HOSTILE_JSON_REJECTED: {strict}/{strict}")
            return 0
        if args.reemit is not None:
            run_audit(data)
            args.reemit.write_bytes(MANIFEST.read_bytes())
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, IndexError,
            ArithmeticError, subprocess.SubprocessError) as exc:
        print(f"ROUND67_AUDIT_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND67 AUDIT: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
