#!/usr/bin/env python3
"""Independent verifier for the Round-62 core-frontier audit package."""

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
RESULT_SCHEMA = "cm2.round62-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round62-independent-core-frontier-audit"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
REPORT = HERE / f"{PREFIX}-2026-07-21.md"
CERT = HERE / "cm2_round62_independent_core_frontier_audit_cert.py"
VERIFIER = Path(__file__).resolve()
EXPECTED_RESULT_DIGEST = "5dee7f99229f5b1edb4f45ddfd733e43df1cd1bffa59140a6ad8d18ce75d3a0a"

PINS = {
    "cm2-sixty-first-direct-assault-2026-07-20.md":
        "b9ad28ed23e88768234b304dd9f9ecb02577c7aa18dc8a982185690ea8f6f02b",
    "cm2-sixty-first-direct-assault-manifest-2026-07-20.sha256":
        "2a3ae3ebf1a6e11b734611e260a340398f475d70e4888010c8294ac321d84265",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json":
        "e0b89d604e89852b574638428a60daa1f6e8231b85177230a5dd67615205bad1",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.sha256":
        "b94df87ba8362827bb1115f474c0beec59f887325e8db58b55a9020bf99ae6bc",
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.json":
        "eb9e086e973866beaba19111a74e67772f5b0998bbee7c43f06c273c96c68fe2",
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.sha256":
        "14e13e71fbe1a9c0ed1ef8524da549939417c8406fa60a78f60d56e45deab450",
    "cm2-gate5-round62-all-time-owner-trace-decay-frontier-manifest-2026-07-21.json":
        "ddbe8545e6471977ac7bd06b584717cbe7ffeeb62df2ac3baeb8cb70f0ad27d9",
    "cm2-gate5-round62-all-time-owner-trace-decay-frontier-manifest-2026-07-21.sha256":
        "ce399f98596b9906eb89d1bd68b80d5f49a5ed29471ba2b8d9648c250a805e61",
}

LEDGERS = [
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.sha256",
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.sha256",
    "cm2-gate5-round62-all-time-owner-trace-decay-frontier-manifest-2026-07-21.sha256",
]

EXPECTED_STRICT = {
    "Gate1": "NOT_CERTIFIED",
    "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
    "Gate3": "NOT_CERTIFIED",
    "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
    "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
    "complete_composite_gates": "0/5",
    "CM2": "NO-GO_FOR_CLAIM",
    "audit_verdict": "PASS_AFTER_RED_TEAM_CORRECTIONS",
}


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


def strict_json(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=strict_object,
        parse_constant=lambda token: (_ for _ in ()).throw(VerifyError(f"nonfinite: {token}")),
    )


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
        require(path.is_file() and not path.is_symlink() and path.resolve().parent == HERE, f"pin path: {name}")
        require(sha256_path(path) == expected, f"pin hash: {name}")
    total = 0
    for name in LEDGERS:
        rows = [line.strip() for line in (HERE / name).read_text(encoding="utf-8").splitlines() if line.strip()]
        require(len(rows) == 4, f"ledger rows: {name}")
        for row in rows:
            parts = row.split(maxsplit=1)
            require(len(parts) == 2, f"ledger syntax: {name}")
            expected, token = parts
            path = resolve_sidecar_name(token)
            require(path.is_file() and not path.is_symlink(), f"ledger path: {token}")
            require(sha256_path(path) == expected, f"ledger hash: {token}")
            total += 1
    require(total == 12, "ledger total")


def load_manifest() -> dict[str, Any]:
    require(MANIFEST.is_file() and not MANIFEST.is_symlink() and MANIFEST.resolve().parent == HERE, "manifest path")
    data = strict_json(MANIFEST.read_text(encoding="utf-8"))
    require(isinstance(data, dict), "manifest root")
    return data


def integrity(data: dict[str, Any], *, files: bool = True) -> None:
    if files:
        check_pins_and_sidecars()
    require(data.get("schema") == MANIFEST_SCHEMA, "manifest schema")
    require(data.get("pins") == PINS, "manifest pins")
    require(data.get("certificate_sha256") == sha256_path(CERT), "cert hash")
    require(data.get("verifier_sha256") == sha256_path(VERIFIER), "verifier hash")
    require(data.get("report_sha256") == sha256_path(REPORT), "report hash")
    result = data.get("result")
    require(isinstance(result, dict), "result root")
    core = dict(result)
    recorded = core.pop("internal_replay_digest", None)
    require(recorded == EXPECTED_RESULT_DIGEST and digest(core) == recorded, "result digest")
    require(data.get("verdict") == result.get("strict_final_state"), "verdict alias")


def replay_gate13(section: dict[str, Any]) -> None:
    require(section["status"] == "INDEPENDENT_PASS", "Gate13 audit status")
    algebra = section["algebra"]
    require(algebra["shear_amplification_rows"] == "12/12", "Gate13 defects")
    require(algebra["moving_face_rows"] == "2/2" and algebra["directional_Piola_rows"] == "1/1", "Gate13 face Piola")
    require(algebra["fragmentation_rows"] == "6/6" and algebra["bulk_separator_rows"] == "5/5", "Gate13 separators")
    acceptance = section["acceptance"]
    require(acceptance["dependencies"] == "12/12" and acceptance["hostile_and_JSON"] == "300/300_REJECTED", "Gate13 acceptance")
    require("CONDITIONAL" in section["type_review"] and "PHYSICAL_RQ_PIOLA_MTDQ_OPEN" in section["type_review"], "Gate13 type")


def replay_gate5(section: dict[str, Any]) -> None:
    require(section["status"] == "INDEPENDENT_PASS", "Gate5 audit status")
    abel = section["outer_Abel_replay"]
    require(Q(abel["w"]) == Q(3, 2) and Q(abel["lhs"]) == Q(abel["rhs"]), "Gate5 Abel replay")
    jordan = section["Jordan_replay"]
    require(Q(jordan["positive_total"]) == Q(jordan["variation"]) + 2 * Q(jordan["common_mode"]), "Gate5 Jordan replay")
    require(section["harmonic_rows"] == "6/6", "Gate5 harmonic")
    require("CANONICAL_MINIMAL_NOT_UNIQUE" in section["registry_typing"], "Gate5 registry")
    require("NCUT_NACC" in section["measure_typing"], "Gate5 strata")
    acceptance = section["acceptance"]
    require(acceptance["dependency_and_aggregate_pins"] == "9/9" and acceptance["hostile_and_JSON"] == "168/168_REJECTED", "Gate5 acceptance")


def semantics(result: dict[str, Any]) -> None:
    require(result.get("schema") == RESULT_SCHEMA, "result schema")
    provenance = result["provenance"]
    require("accepted from a separate root-agent review" in provenance["independence_guard"], "independence guard")
    gate42 = result["gate42_root_independent_audit"]
    require(gate42["status"] == "PASS_BY_ROOT_INDEPENDENT_REVIEW__CROSS_LEAF_CONSISTENCY_RECHECKED", "Gate42 provenance")
    checks = gate42["root_independent_checks"]
    require(checks["hostile_semantic"] == "180/180_REJECTED" and checks["strict_JSON"] == "4/4_REJECTED", "Gate42 hostile")
    require(gate42["typed_findings"]["physical_Piola_or_cemetery"] == "NOT_CERTIFIED", "Gate42 type")
    replay_gate13(result["gate13_independent_audit"])
    replay_gate5(result["gate5_independent_audit"])
    cross = result["cross_leaf_consistency"]
    require(cross["status"] == "PASS_NO_CROSS_LEAF_TYPE_SUBSTITUTION_OR_STATE_CONTRADICTION", "cross status")
    require(len(cross["rows"]) == 6 and digest(cross["rows"]) == cross["rows_sha256"], "cross rows")
    acceptance = result["source_leaf_acceptance"]
    expected = {
        "syntax": "6/6",
        "dependency_and_baseline_pins": "31/31",
        "integrity": "3/3",
        "replay": "3/3",
        "reemit": "3/3_BYTE_IDENTICAL",
        "hostile_and_strict_JSON": "652/652_REJECTED",
        "SHA_sidecar_rows": "12/12",
        "default_entry_points": "6/6_EXIT_2",
    }
    require(acceptance == expected, "acceptance matrix")
    require(result["strict_final_state"] == EXPECTED_STRICT, "strict final")
    require(result["latest_technology_boundary"]["external_theorem_promoted"] is False, "external promotion")
    require(len(result["red_team_corrections"]) == 4, "red-team corrections")


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
    require(produced == data and proc.stdout.encode("utf-8") == MANIFEST.read_bytes(), "producer mismatch")


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
        core = dict(result)
        core.pop("internal_replay_digest", None)
        result["internal_replay_digest"] = digest(core)
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


def run_audit(data: dict[str, Any], *, regenerate: bool = True) -> None:
    integrity(data)
    semantics(data["result"])
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
    require(proc.returncode == 0, "reemit producer")
    path.write_bytes(proc.stdout)
    require(path.read_bytes() == MANIFEST.read_bytes(), "reemit bytes")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        data = load_manifest()
        if args.audit:
            run_audit(data)
            print("AUDIT_MODE: PASS")
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
    except (OSError, VerifyError, ValueError, KeyError, TypeError, IndexError, subprocess.SubprocessError) as exc:
        print(f"ROUND62_INDEPENDENT_AUDIT_VERIFY_FAILURE: {exc}")
        return 1
    state = data["result"]["strict_final_state"]
    print("AUDIT_VERDICT:", state["audit_verdict"])
    print("COMPOSITE_GATES:", state["complete_composite_gates"])
    print("GATE5:", state["Gate5"])
    print("CM2:", state["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
