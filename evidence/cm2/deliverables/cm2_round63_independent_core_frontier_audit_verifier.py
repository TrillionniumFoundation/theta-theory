#!/usr/bin/env python3
"""Fail-closed independent verifier for the Round-63 core-frontier audit."""

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
RESULT_SCHEMA = "cm2.round63-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round63-independent-core-frontier-audit"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
REPORT = HERE / f"{PREFIX}-2026-07-21.md"
LEDGER = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
CERT = HERE / "cm2_round63_independent_core_frontier_audit_cert.py"
VERIFIER = Path(__file__).resolve()
EXPECTED_RESULT_DIGEST = "3bd27e8c2e740dd1d31bfd2f44dc581865b7c6ceb8be2cbbe99ffe59bb930b65"

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

LEAF_LEDGERS = [
    "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-manifest-2026-07-21.sha256",
    "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.sha256",
    "cm2-gate5-round63-killed-trace-kernel-jordan-join-frontier-manifest-2026-07-21.sha256",
]

EXPECTED_STRICT = {
    "Gate1": "NOT_CERTIFIED",
    "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
    "Gate3": "NOT_CERTIFIED",
    "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
    "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
    "complete_composite_gates": "0/5",
    "CM2": "NO-GO_FOR_CLAIM",
    "audit_verdict": "PASS__NO_SOURCE_LEAF_CORRECTION_REQUIRED",
}

CP = Q(4 * 10**90 * 360493663, 358863)


class VerifyError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerifyError(label)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise VerifyError(f"duplicate key: {key}")
        out[key] = value
    return out


def reject_constant(token: str) -> None:
    raise VerifyError(f"non-finite JSON: {token}")


def strict_json(text: str) -> Any:
    return json.loads(text, object_pairs_hook=strict_object, parse_constant=reject_constant)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_sidecar_name(token: str) -> Path:
    path = HERE.parent / token if token.startswith("deliverables/") else HERE / token
    path = path.resolve()
    require(path.parent == HERE, f"sidecar parent: {token}")
    return path


def check_pins_and_sidecars() -> None:
    for name, expected in PINS.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink() and path.resolve().parent == HERE,
                f"pin path: {name}")
        require(sha256_path(path) == expected, f"pin hash: {name}")
    total = 0
    for name in LEAF_LEDGERS:
        rows = [line.strip() for line in (HERE / name).read_text(encoding="utf-8").splitlines()
                if line.strip()]
        require(len(rows) == 4, f"ledger rows: {name}")
        seen: set[Path] = set()
        for row in rows:
            parts = row.split(maxsplit=1)
            require(len(parts) == 2, f"ledger syntax: {name}")
            expected, token = parts
            require(len(expected) == 64 and all(c in "0123456789abcdef" for c in expected),
                    f"ledger digest: {name}")
            path = resolve_sidecar_name(token)
            require(path not in seen, f"ledger duplicate: {name}")
            seen.add(path)
            require(path.is_file() and not path.is_symlink(), f"ledger file/type: {token}")
            require(sha256_path(path) == expected, f"ledger hash: {token}")
            total += 1
    require(total == 12, "ledger total")


def load_manifest() -> dict[str, Any]:
    require(MANIFEST.is_file() and not MANIFEST.is_symlink() and MANIFEST.resolve().parent == HERE,
            "manifest path")
    data = strict_json(MANIFEST.read_text(encoding="utf-8"))
    require(isinstance(data, dict), "manifest root")
    return data


def integrity(data: dict[str, Any], *, files: bool = True) -> None:
    if files:
        check_pins_and_sidecars()
    require(data.get("schema") == MANIFEST_SCHEMA, "manifest schema")
    require(data.get("pins") == PINS, "manifest pins")
    require(data.get("certificate_sha256") == sha256_path(CERT), "certificate hash")
    require(data.get("verifier_sha256") == sha256_path(VERIFIER), "verifier hash")
    require(data.get("report_sha256") == sha256_path(REPORT), "report hash")
    result = data.get("result")
    require(isinstance(result, dict), "result root")
    replay = copy.deepcopy(result)
    recorded = replay.pop("internal_replay_digest", None)
    require(recorded == EXPECTED_RESULT_DIGEST and digest(replay) == recorded,
            "result digest")
    require(data.get("verdict") == result.get("strict_final_state"), "verdict alias")


def semantics(result: dict[str, Any]) -> None:
    require(result.get("schema") == RESULT_SCHEMA, "result schema")
    provenance = result["provenance"]
    require(provenance["all_three_leaves_frozen_before_read"] is True,
            "frozen-before-read provenance")
    require(provenance["audit_authored_source_leaf"] is False and
            provenance["old_artifacts_modified"] is False, "independence provenance")
    require(provenance["pinned_artifacts"] == PINS, "provenance pins")

    gate13 = result["gate13_independent_audit"]
    require(gate13["status"] == "INDEPENDENT_PASS", "Gate13 audit status")
    require(gate13["algebra_and_arithmetic"] == {
        "endpoint_conjugacy_identity": "PASS",
        "threshold_regimes": "3/3",
        "threshold_samples": "30/30",
        "incidence_rows": "3/3",
        "taxonomy_rows": "11/11",
        "clock_rows": "13/13",
        "F13_ratio_rows": "2/2",
    }, "Gate13 replay summary")
    require(gate13["red_team"]["theta_less_than_one"] ==
            "SUFFICIENT_ONLY__SHARP_ONLY_IN_DECLARED_LOGICAL_SL2_MODEL", "Gate13 theta guard")
    require(gate13["red_team"]["Round44_F13"] == "BASE_S0_REGULAR_BOREL_TV_ONLY",
            "Gate13 F13 guard")
    require(gate13["red_team"]["clock_jump"] ==
            "DISTINCT_SIXTH_DEBT_NOT_PAID_BY_FIVE_F13_GRAMMARS", "Gate13 clock guard")
    require(gate13["acceptance"] == {
        "dependency_pins": "13/13", "integrity": "PASS", "replay": "PASS",
        "reemit": "BYTE_IDENTICAL", "hostile_semantic": "385/385_REJECTED",
        "strict_JSON": "15/15_REJECTED", "SHA": "4/4", "default_exit2": "2/2",
    }, "Gate13 acceptance")

    gate24 = result["gate24_independent_audit"]
    require(gate24["status"] == "INDEPENDENT_PASS", "Gate24 audit status")
    require(gate24["algebra_and_arithmetic"] == {
        "square_identity": "PASS",
        "source_landing_defect_norms": "1/6__1/6",
        "two_plaque_outer_weights": "1/2__1/2",
        "two_plaque_saturation_distance": "1/12",
        "holonomy_transport_target_bound": "72",
        "zero_defect_separators": "2/2",
    }, "Gate24 replay summary")
    require(gate24["red_team"]["square_effect"] ==
            "PRESERVES_DEBT__DOES_NOT_ANNIHILATE_DEBT", "Gate24 square guard")
    require(gate24["red_team"]["L1_outer_weight"] == "EXACTLY_ONE_HALF",
            "Gate24 outer weight guard")
    require(gate24["red_team"]["m_squared_origin"] ==
            "ONE_SPAN_FACTOR__ONE_INVERSE_DENSITY_FACTOR", "Gate24 m squared guard")
    require(gate24["acceptance"] == {
        "dependency_and_baseline_pins": "15/15", "integrity": "PASS", "replay": "PASS",
        "reemit": "BYTE_IDENTICAL", "hostile_semantic": "180/180_REJECTED",
        "strict_JSON": "4/4_REJECTED", "SHA": "4/4", "default_exit2": "2/2",
    }, "Gate24 acceptance")

    gate5 = result["gate5_independent_audit"]
    require(gate5["status"] == "INDEPENDENT_PASS", "Gate5 audit status")
    arithmetic = gate5["algebra_and_arithmetic"]
    require(arithmetic["killed_kernel_rows"] == "3/3" and
            arithmetic["sharp_ratios"] == ["3/4", "1", "9/8"], "Gate5 kernel summary")
    require(Q(arithmetic["orientation_cost_rational_sum"]) == Q(2395081816467609, 880000),
            "Gate5 cost total")
    jordan = arithmetic["finite_Jordan_replay"]
    require(Q(jordan["positive_total"]) ==
            Q(jordan["variation"]) + 2 * Q(jordan["common_mode"]), "Gate5 Jordan replay")
    require(arithmetic["complement_rows"] == "4/4", "Gate5 complement summary")
    require(gate5["red_team"]["killed_kernel"] ==
            "EXACT_CONDITIONAL_INTERFACE__NO_ACTUAL_DRIFT", "Gate5 kernel type")
    require(gate5["red_team"]["cost_Jordan"] == "NOT_ROUND54_SIGNED_PHYSICAL_FLUX",
            "Gate5 Jordan type")
    require(gate5["red_team"]["all_time_decay"] == "NOT_CERTIFIED",
            "Gate5 all-time guard")
    require(gate5["acceptance"] == {
        "dependency_and_baseline_pins": "13/13", "integrity": "PASS", "replay": "PASS",
        "reemit": "BYTE_IDENTICAL", "hostile_semantic": "160/160_REJECTED",
        "strict_JSON": "4/4_REJECTED", "SHA": "4/4", "default_exit2": "2/2",
    }, "Gate5 acceptance")

    cross = result["cross_leaf_consistency"]
    require(cross["status"] == "PASS_NO_CROSS_LEAF_TYPE_SUBSTITUTION_OR_STATE_CONTRADICTION",
            "cross status")
    require(len(cross["rows"]) == 7 and digest(cross["rows"]) == cross["rows_sha256"],
            "cross rows")
    require("CLOCK_JUMP_IS_A_DISTINCT_SIXTH_DEBT" in cross["rows"][1]["verdict"],
            "cross clock row")
    require("DOES_NOT_ANNIHILATE" in cross["rows"][2]["verdict"],
            "cross square row")
    require("NOT_IDENTIFIED" in cross["rows"][5]["verdict"], "cross Jordan row")

    acceptance = result["source_leaf_acceptance"]
    require(acceptance == {
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
    }, "acceptance matrix")
    require(len(result["red_team_guards"]) == 6, "red-team guard count")
    require(result["latest_technology_boundary"]["external_theorem_promoted_by_audit"] is False,
            "external theorem promotion")
    require(result["strict_final_state"] == EXPECTED_STRICT, "strict final state")


def safe_dbar(m: int) -> int:
    if Q(2) ** m <= CP:
        return 0
    d = 1
    while not Q(2) ** (m - d) < CP / 2:
        d += 1
    return d


def load_source(name: str) -> dict[str, Any]:
    value = strict_json((HERE / name).read_text(encoding="utf-8"))
    require(isinstance(value, dict) and isinstance(value.get("result"), dict),
            f"source manifest: {name}")
    return value["result"]


def source_replays() -> dict[str, int | str]:
    gate13 = load_source(
        "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-manifest-2026-07-21.json"
    )
    samples = 0
    expected = [(Q(3, 2), Q(1, 4), Q(9, 16)), (Q(2), Q(1, 4), Q(1)),
                (Q(2), Q(1, 2), Q(2))]
    for row, (a, lam, theta) in zip(
            gate13["gate1"]["sharp_plaque_tempered_budget"]["threshold_rows"], expected):
        require(Q(row["a"]) == a and Q(row["lambda"]) == lam and
                Q(row["theta=a^2*lambda"]) == theta == a * a * lam,
                "source Gate13 threshold")
        for n, sample in enumerate(row["samples"], 1):
            require(Q(sample["endpoint_lower_defect"]) == lam**n and
                    Q(sample["renormalized_lower_defect"]) == theta**n,
                    "source Gate13 sample")
            samples += 1
    clock = gate13["gate3"]["stopping_clock_jump_frontier"]["rows"]
    for row in clock:
        require(row["Dbar"] == safe_dbar(row["M"]) and
                row["R0=696*Dbar"] == 696 * row["Dbar"], "source Gate13 clock")
    require(safe_dbar(310) == 0 and safe_dbar(311) == 2, "source Gate13 first jump")

    gate24 = load_source(
        "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.json"
    )
    replay = gate24["branch_holonomy_square"]["finite_replay"]
    require(Q(replay["L1_Delta_S"]) == Q(replay["L1_Delta_L"]) == Q(1, 6),
            "source Gate24 defect norms")
    sat = gate24["two_plaque_stable_saturation"]["finite_replay"]
    require(Q(sat["outer_weight_u"]) == Q(sat["outer_weight_v"]) == Q(1, 2) and
            Q(sat["delta_sat"]) == Q(1, 12), "source Gate24 saturation")
    tr = gate24["quantitative_holonomy_transport"]["finite_replay"]
    target = (Q(tr["F_u"]) * Q(tr["R_u"]) * Q(tr["metric_derivative_upper_M"]) /
              (Q(tr["metric_derivative_lower_m"])**2 * Q(tr["theta_u"]) * Q(tr["L_u"])))
    require(target == Q(tr["target_z_upper"]) == 72, "source Gate24 transport")

    gate5 = load_source(
        "cm2-gate5-round63-killed-trace-kernel-jordan-join-frontier-manifest-2026-07-21.json"
    )
    kernel_rows = gate5["killed_trace_kernel_frontier"]["replay_rows"]
    for row in kernel_rows:
        ratio = Q(row["w_test"]) * Q(row["kappa_test"])
        require(Q(row["ratio"]) == ratio and Q(row["partial_sum"]) ==
                sum((ratio**j for j in range(row["N"] + 1)), Q(0)),
                "source Gate5 kernel")
    jordan5 = gate5["fixed_j_orientation_cost_Jordan"]
    require(Q(jordan5["forward_strict_upper"]) + Q(jordan5["reverse_strict_upper"]) ==
            Q(jordan5["bidirectional_strict_upper"]) == Q(2395081816467609, 880000),
            "source Gate5 Jordan total")
    require(len(gate5["complement_strata_frontier"]["rows"]) == 4,
            "source Gate5 complement rows")
    return {
        "gate13_threshold_samples": samples,
        "gate13_clock_rows": len(clock),
        "gate24_square_saturation_transport_rows": 3,
        "gate5_kernel_rows": len(kernel_rows),
        "gate5_complement_rows": 4,
        "status": "PASS",
    }


def deterministic(data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=180,
    )
    require(proc.returncode == 0, f"producer exit: {proc.stderr.strip()}")
    produced = strict_json(proc.stdout)
    require(produced == data and proc.stdout.encode("utf-8") == MANIFEST.read_bytes(),
            "producer mismatch")


def run_audit(data: dict[str, Any], *, regenerate: bool = True) -> None:
    integrity(data)
    semantics(data["result"])
    source_replays()
    if regenerate:
        deterministic(data)


def reemit(path: Path, data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=180,
    )
    require(proc.returncode == 0, f"reemit producer: {proc.stderr.decode().strip()}")
    path.write_bytes(proc.stdout)
    require(path.read_bytes() == MANIFEST.read_bytes(), "reemit bytes")


def deep_paths(value: Any, prefix: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    out: list[tuple[Any, ...]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key != "internal_replay_digest":
                out.extend(deep_paths(child, prefix + (key,)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            out.extend(deep_paths(child, prefix + (index,)))
    else:
        out.append(prefix)
    return out


def get_path(root: Any, path: tuple[Any, ...]) -> Any:
    node = root
    for step in path:
        node = node[step]
    return node


def set_path(root: Any, path: tuple[Any, ...], value: Any) -> None:
    node = root
    for step in path[:-1]:
        node = node[step]
    node[path[-1]] = value


def hostile_value(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "__HOSTILE"
    if value is None:
        return "HOSTILE"
    return {"hostile": True}


def self_test(data: dict[str, Any]) -> int:
    paths = deep_paths(data["result"])
    require(len(paths) >= 100, "hostile path count")
    rejected = 0
    for path in paths:
        mutant = copy.deepcopy(data)
        result = mutant["result"]
        set_path(result, path, hostile_value(get_path(result, path)))
        replay = copy.deepcopy(result)
        replay.pop("internal_replay_digest", None)
        result["internal_replay_digest"] = digest(replay)
        mutant["verdict"] = result["strict_final_state"]
        try:
            integrity(mutant, files=False)
            semantics(result)
        except (VerifyError, ValueError, KeyError, TypeError, IndexError):
            rejected += 1
    require(rejected == len(paths), f"hostile accepted: {rejected}/{len(paths)}")
    hostile_json = ['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}']
    json_rejected = 0
    for payload in hostile_json:
        try:
            strict_json(payload)
        except (VerifyError, ValueError):
            json_rejected += 1
    require(json_rejected == 4, "hostile JSON")
    print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{len(paths)}")
    print(f"HOSTILE_JSON_REJECTED: {json_rejected}/4")
    return rejected + json_rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        data = load_manifest()
        if args.audit:
            run_audit(data)
            print("AUDIT_MODE: PASS")
            return 0
        if args.replay:
            run_audit(data, regenerate=False)
            print(json.dumps(source_replays(), sort_keys=True))
            return 0
        if args.self_test:
            run_audit(data)
            self_test(data)
            print("SELF_TEST: PASS")
            return 0
        if args.reemit is not None:
            run_audit(data, regenerate=False)
            reemit(args.reemit, data)
            print(f"REEMIT: {args.reemit}")
            return 0
    except (VerifyError, OSError, ValueError, KeyError, TypeError, IndexError,
            ArithmeticError, subprocess.SubprocessError) as exc:
        print(f"ROUND63_AUDIT_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    final = data["result"]["strict_final_state"]
    print("AUDIT_VERDICT:", final["audit_verdict"])
    print("GATES_1_TO_5: NOT_CERTIFIED")
    print("COMPLETE_COMPOSITE_GATES:", final["complete_composite_gates"])
    print("CM2:", final["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
