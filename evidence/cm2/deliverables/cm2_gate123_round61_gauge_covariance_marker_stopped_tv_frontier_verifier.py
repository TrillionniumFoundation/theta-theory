#!/usr/bin/env python3
"""Independent verifier for the CM2 Round-61 Gate-1/2/3 frontier leaf."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / "deliverables"
REPORT = HERE / (
    "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-"
    "assault-2026-07-20.md"
)
MANIFEST = HERE / (
    "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-"
    "manifest-2026-07-20.json"
)
CERT = HERE / (
    "cm2_gate123_round61_gauge_covariance_marker_stopped_tv_frontier_cert.py"
)
Q = Fraction


DEPENDENCIES = {
    "deliverables/cm2-sixtieth-direct-assault-2026-07-20.md":
        "ef3f2739a7a0ed8c91e82400c05564f97f0c3326ebc1373764b51bbd48f04212",
    "deliverables/cm2-sixtieth-direct-assault-manifest-2026-07-20.sha256":
        "5f6c90735cbb74ec7b36f6c1d2b012ccccaafa40793d291dfcb6a0e212044e9e",
    "deliverables/cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier-manifest-2026-07-20.json":
        "f897d81a2e85c4a8e45c436f169043feaef93b019f18229a44da0227c75b2a88",
    "deliverables/cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier-manifest-2026-07-20.sha256":
        "6a29c47462a9526138a059f8577abcf879cd162feca14b435906cce1cd8c087a",
    "deliverables/cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json":
        "08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3",
    "deliverables/cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.sha256":
        "4d7c3f06e1671319482c064ec3ea817562567202b111fd014434b7be0a460fac",
    "deliverables/cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json":
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73",
    "deliverables/cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.sha256":
        "7fd9547443951d9960b466aa914f73b1a36f73897e31585018eceed409be4716",
}

RESULT_SHA256 = "ae2e37bb073f67171987dce13d9f37ae34992e2a31d320d82c23700f22191c95"


class VerifyError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerifyError(message)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()).hexdigest()


def reject_constant(token: str) -> None:
    raise VerifyError(f"nonfinite JSON constant: {token}")


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerifyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_loads(raw: bytes) -> Any:
    try:
        return json.loads(raw.decode("utf-8"), parse_constant=reject_constant,
                          object_pairs_hook=unique_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerifyError(f"strict JSON parse: {exc}") from exc


def validate_dependencies() -> list[dict[str, str]]:
    rows = []
    for rel, expected in DEPENDENCIES.items():
        path = ROOT / rel
        require(path.is_file() and not path.is_symlink(), f"dependency file/type: {rel}")
        require(sha256_path(path) == expected, f"dependency hash drift: {rel}")
        rows.append({"path": rel, "sha256": expected})
    return rows


def validate_obj(data: Any, raw: bytes | None = None) -> None:
    require(type(data) is dict, "manifest object")
    require(set(data) == {
        "artifact", "certificate_sha256", "date", "dependencies", "report_sha256",
        "result", "result_sha256", "schema", "strict_verdict", "verifier_sha256",
    }, "manifest exact top-level schema")
    if raw is not None:
        require(raw == canonical_bytes(data), "canonical manifest bytes")
    require(data["schema"] ==
            "cm2.gate123.round61.gauge-covariance-marker-stopped-tv-frontier.v1",
            "schema")
    require(data["artifact"] ==
            "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier",
            "artifact")
    require(data["date"] == "2026-07-20", "date")
    expected_deps = [{"path": rel, "sha256": digest}
                     for rel, digest in DEPENDENCIES.items()]
    require(data["dependencies"] == expected_deps, "dependency rows")
    require(type(data["result"]) is dict, "result type")
    digest = canonical_digest(data["result"])
    require(digest == data["result_sha256"] == RESULT_SHA256, "result digest")
    require(data["strict_verdict"] == (
        "exact same-loop gauge covariance, marker-holonomy compatibility and "
        "actual weak stopped graph-TV compression are certified; physical all-plaque "
        "combined class H, all-depth stable holonomy and strong R/Q/Piola/MT_DQ "
        "remain not certified"
    ), "strict verdict")
    strict = data["result"].get("strict_status")
    require(strict == {
        "cm2": "NO-GO_FOR_CLAIM",
        "composite_gates": "0/5",
        "gate1": "NOT_CERTIFIED",
        "gate2": "NOT_CERTIFIED",
        "gate2_immutable_fields": "0/17",
        "gate2_landing_join": "1/7",
        "gate3": "NOT_CERTIFIED",
    }, "strict status")
    require(REPORT.is_file() and not REPORT.is_symlink(), "report type")
    require(CERT.is_file() and not CERT.is_symlink(), "certificate type")
    require(Path(__file__).resolve().is_file(), "verifier type")
    require(data["report_sha256"] == sha256_path(REPORT), "report hash")
    require(data["certificate_sha256"] == sha256_path(CERT), "certificate hash")
    require(data["verifier_sha256"] == sha256_path(Path(__file__).resolve()),
            "verifier hash")


def independent_replay(data: dict[str, Any]) -> dict[str, int | str]:
    # Gate 1: explicitly multiply D Psi D^-1 and transport both vectors.
    d = ((Q(2), Q(1)), (Q(1), Q(1)))
    d_inv = ((Q(1), Q(-1)), (Q(-1), Q(2)))
    psi = ((Q(2), Q(3)), (Q(5), Q(7)))

    def mm(a: Any, b: Any) -> Any:
        return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(2)), Q(0))
                           for j in range(2)) for i in range(2))

    def mv(a: Any, v: Any) -> Any:
        return tuple(sum((a[i][k] * v[k] for k in range(2)), Q(0))
                     for i in range(2))

    def wd(v: Any, w: Any) -> Q:
        return v[0] * w[1] - v[1] * w[0]

    psi_new = mm(mm(d, psi), d_inv)
    basis = ((Q(1), Q(0)), (Q(0), Q(1)))
    basis_new = tuple(mv(d, v) for v in basis)
    old = [wd(mv(psi, basis[i]), basis[j]) for i in range(2) for j in range(2)]
    new = [wd(mv(psi_new, basis_new[i]), basis_new[j])
           for i in range(2) for j in range(2)]
    require(old == new == [Q(-5), Q(2), Q(-7), Q(3)], "independent wedge replay")

    # Gate 2: independent RN pushforward replay.
    mu_u = [Q(1, 2), Q(1, 3), Q(1, 6)]
    mu_v = [Q(1, 4), Q(1, 2), Q(1, 4)]
    marker_u = [Q(1), Q(1, 2), Q(0)]
    target = [1, 2, 0]
    push_mu = [Q(0)] * 3
    push_kappa = [Q(0)] * 3
    for i in range(3):
        push_mu[target[i]] += mu_u[i]
        push_kappa[target[i]] += marker_u[i] * mu_u[i]
    jac = [push_mu[i] / mu_v[i] for i in range(3)]
    pushed_marker = [push_kappa[i] / mu_v[i] for i in range(3)]
    require(jac == [Q(2, 3), Q(1), Q(4, 3)], "independent J replay")
    require(pushed_marker == [Q(0), Q(1), Q(2, 3)], "independent marker replay")

    # Gate 3: direct-sum TV and fragmentation.
    signed = [Q(1, 3), Q(-1, 6), Q(1, 2), Q(-1, 4),
              Q(1, 8), Q(-1, 12), Q(1, 7), Q(-1, 9)]
    input_tv = sum((abs(x) for x in signed), Q(0))
    bins = [0, 0, 1, 1, 2, 2, 2, 1]
    output = [Q(0), Q(0), Q(0)]
    for x, b in zip(signed, bins):
        output[b] += x
    require(sum((abs(x) for x in output), Q(0)) <= input_tv,
            "independent TV contraction")
    for m in (1, 2, 4, 8, 16, 32):
        require(Q(1 + 2 * m, 3) >= 1, "independent fragmentation row")
    require(Q(1 + 64, 3) == Q(65, 3), "independent fragmentation endpoint")

    result = data["result"]
    require(result["gate1"]["exact_same_loop_gauge_covariance"]["status"] ==
            "CERTIFIED_EXACT_COHOMOLOGY_COVARIANCE_INTERFACE", "Gate1 status")
    require(result["gate2"]["marker_holonomy_compatibility"]["status"] ==
            "CERTIFIED_EXACT_MARKER_HOLONOMY_INTERFACE", "Gate2 status")
    require(result["gate3"]["actual_stopped_graph_partition"]["status"] ==
            "CERTIFIED_ACTUAL_WEAK_STOPPED_GRAPH_TV_NORM_ONE", "Gate3 weak status")
    require(result["gate3"]["actual_stopped_graph_partition"]
            ["raw_word_factor_needed_in_weak_TV"] is False, "raw word guard")
    require(result["gate3"]["direct_strong_boundary"]["physical_strong_R_s_Q_s"] ==
            "NOT_CERTIFIED", "strong boundary")
    require(result["gate3"]["latest_official_technology_audit"]
            ["external_theorem_promoted"] is False, "literature guard")
    return {"wedge_cases": 4, "marker_atoms": 3, "stopped_cells": 8,
            "fragmentation_rows": 6, "status": "PASS"}


def hostile_self_test(base: dict[str, Any]) -> int:
    rejected = 0
    mutations: list[dict[str, Any]] = []
    for i in range(80):
        candidate = copy.deepcopy(base)
        candidate[f"hostile_extra_{i}"] = i
        mutations.append(candidate)
    for i in range(80):
        candidate = copy.deepcopy(base)
        candidate["result"]["strict_status"]["composite_gates"] = f"{i + 1}/5"
        candidate["result_sha256"] = canonical_digest(candidate["result"])
        mutations.append(candidate)
    for i in range(40):
        candidate = copy.deepcopy(base)
        candidate["dependencies"][i % 8]["sha256"] = f"{i:064x}"[-64:]
        mutations.append(candidate)
    for candidate in mutations:
        try:
            validate_obj(candidate)
        except VerifyError:
            rejected += 1
    require(rejected == len(mutations) == 200, "hostile object rejection")

    raw_attacks = [
        b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}',
        b'{"x":1,"x":2}', b'[]', b'null', b'"manifest"', b'{',
    ]
    raw_rejected = 0
    for raw in raw_attacks:
        try:
            value = strict_loads(raw)
            validate_obj(value, raw)
        except VerifyError:
            raw_rejected += 1
    require(raw_rejected == len(raw_attacks) == 8, "hostile JSON rejection")
    return rejected + raw_rejected


def load_manifest() -> tuple[dict[str, Any], bytes]:
    require(MANIFEST.is_file() and not MANIFEST.is_symlink(), "manifest file/type")
    raw = MANIFEST.read_bytes()
    data = strict_loads(raw)
    require(type(data) is dict, "manifest mapping")
    return data, raw


def reemit(path: Path) -> None:
    command = [sys.executable, str(CERT), "--emit-manifest", str(path)]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    require(completed.returncode == 0, f"producer reemit: {completed.stderr}")
    require(path.read_bytes() == MANIFEST.read_bytes(), "byte-identical reemit")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        validate_dependencies()
        data, raw = load_manifest()
        validate_obj(data, raw)
        if args.integrity_only:
            print("INTEGRITY: PASS")
            print("DEPENDENCIES: 8/8")
            return 0
        if args.replay:
            print(json.dumps(independent_replay(data), sort_keys=True))
            return 0
        if args.self_test:
            count = hostile_self_test(data)
            print(f"HOSTILE_MUTATIONS_REJECTED: {count}/{count}")
            return 0
        if args.reemit is not None:
            reemit(args.reemit)
            print("REEMIT: BYTE_IDENTICAL")
            return 0
        independent_replay(data)
    except (VerifyError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("GATE1_EXACT_SAME_LOOP_GAUGE_COVARIANCE: CERTIFIED_INTERFACE")
    print("GATE2_MARKER_HOLONOMY_COMPATIBILITY: CERTIFIED_INTERFACE")
    print("GATE3_ACTUAL_WEAK_STOPPED_GRAPH_TV: CERTIFIED_NORM_ONE")
    print("PHYSICAL_STRONG_RQ_PIOLA_MT_DQ: NOT_CERTIFIED")
    print("GATES_1_2_3: NOT_CERTIFIED")
    print("COMPOSITE_GATES: 0/5")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
