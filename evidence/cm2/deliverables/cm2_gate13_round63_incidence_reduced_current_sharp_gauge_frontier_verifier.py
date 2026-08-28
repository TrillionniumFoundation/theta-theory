#!/usr/bin/env python3
"""Independent verifier for the Round-63 Gate-1/3 frontier leaf."""

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
    "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-"
    "frontier-assault-2026-07-21.md"
)
MANIFEST = HERE / (
    "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-"
    "frontier-manifest-2026-07-21.json"
)
CERT = HERE / (
    "cm2_gate13_round63_incidence_reduced_current_sharp_gauge_"
    "frontier_cert.py"
)
Q = Fraction


DEPENDENCIES = {
    "deliverables/cm2-sixty-second-direct-assault-2026-07-21.md":
        "873557a6653a826700d5daf11e8b118f5ddca1cf911e085f9c20aa591ab2136f",
    "deliverables/cm2-sixty-second-direct-assault-manifest-2026-07-21.sha256":
        "e54b5a1de2b4bddf0c7589b77997b1f28284040b64b31fdfbf58af9e73233bac",
    "deliverables/cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.json":
        "eb9e086e973866beaba19111a74e67772f5b0998bbee7c43f06c273c96c68fe2",
    "deliverables/cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.sha256":
        "14e13e71fbe1a9c0ed1ef8524da549939417c8406fa60a78f60d56e45deab450",
    "deliverables/cm2-round62-independent-core-frontier-audit-manifest-2026-07-21.json":
        "19a02d00e2ac85849f6197054166e193e1d4e3433c21505fd4bfd2b450faea20",
    "deliverables/cm2-round62-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "32504c8eda5125d11a460199c3471158720127bf2bc1081664a8a20747c7a414",
    "deliverables/cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.json":
        "bb0d263454a33acdf8b2ba443fcc5e247ff1b9214c385f70fa1af2fc26e7c019",
    "deliverables/cm2-gate1-round25-common-frame-manifest-2026-07-18.json":
        "66d4b207a0155ee98a7632154c81caebd567f43aa1a449ffc28b421b175cd436",
    "deliverables/cm2-gate1-third-gauge-escape-frontier-manifest-2026-07-17.json":
        "03174972b28265463fba1bb52a1dbdb1a85f6c1ae074c48f4a3774b5b9731dd7",
    "deliverables/cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json":
        "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
    "deliverables/cm2-gate3-cancellation-free-current-frontier-manifest-2026-07-16.json":
        "c1fc42c517ee930d265468104481b290f16aa90eb72cb8ceb0adb6649760d981",
    "deliverables/cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json":
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d",
    "deliverables/cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json":
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73",
}


RESULT_SHA256 = "fbad24d4527e954c7cf733dc51ee009bc6d5eda8c5398d00b05231bbe12a1cff"
STRICT_VERDICT = (
    "endpoint-conjugacy Holder inheritance, the sharp plaque-tempered budget, "
    "incidence reduction and the base regular F13 join are certified, but the "
    "actual all-plaque transfer, moving clock/cemetery currents, anisotropic bulk "
    "Piola, strong R/Q and MT_DQ remain not certified"
)


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
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


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
    rows: list[dict[str, str]] = []
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
            "cm2.gate13.round63.incidence-reduced-current-sharp-gauge-frontier.v1",
            "schema")
    require(data["artifact"] ==
            "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier",
            "artifact")
    require(data["date"] == "2026-07-21", "date")
    expected_deps = [{"path": rel, "sha256": digest}
                     for rel, digest in DEPENDENCIES.items()]
    require(data["dependencies"] == expected_deps, "dependency rows")
    require(type(data["result"]) is dict, "result type")
    require(canonical_digest(data["result"]) == data["result_sha256"] == RESULT_SHA256,
            "result digest")
    require(data["strict_verdict"] == STRICT_VERDICT, "strict verdict")
    require(data["result"].get("strict_status") == {
        "cm2": "NO-GO_FOR_CLAIM",
        "composite_gates": "0/5",
        "gate1": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
    }, "strict status")

    gate1 = data["result"].get("gate1", {})
    require(gate1.get("endpoint_conjugacy_holder_inheritance", {}).get("status") ==
            "CERTIFIED_EXACT_HOLDER_INHERITANCE_INTERFACE", "Gate1 inheritance")
    require(gate1.get("sharp_plaque_tempered_budget", {}).get("status") ==
            "CERTIFIED_SUFFICIENT_THRESHOLD_SHARP_IN_MODEL", "Gate1 threshold")
    require(gate1.get("physical_boundary", {}).get("actual_all_plaque_transfer_C") ==
            "NOT_CERTIFIED", "Gate1 actual transfer boundary")
    require(gate1.get("physical_boundary", {}).get("separate_approximant_equi_holder_debt") ==
            "NOT_INDEPENDENTLY_REQUIRED_UNDER_ROWS_1_TO_3", "Gate1 redundant row")

    gate3 = data["result"].get("gate3", {})
    require(gate3.get("oriented_incidence_reduction", {}).get("status") ==
            "CERTIFIED_EXACT_INCIDENCE_REDUCTION_INTERFACE", "Gate3 incidence")
    require(gate3.get("actual_stopped_cut_taxonomy", {}).get("status") ==
            "CERTIFIED_TYPED_CUT_TAXONOMY", "Gate3 taxonomy")
    require(gate3.get("same_ID_regular_F13_join", {}).get("status") ==
            "CERTIFIED_BASE_REGULAR_BOREL_JOIN", "Gate3 F13 join")
    require(gate3.get("stopping_clock_jump_frontier", {}).get("status") ==
            "CERTIFIED_EXACT_NEW_CLOCK_JUMP_INTERFACE", "Gate3 clock jump")
    require(gate3.get("stopping_clock_jump_frontier", {})
            .get("covered_by_round44_five_face_F13") is False, "clock not F13")
    require(gate3.get("physical_boundary", {}) == {
        "MT_DQ": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
        "physical_directional_Piola_current": "NOT_CERTIFIED",
        "physical_strong_R_s_Q_s": "NOT_CERTIFIED",
    }, "Gate3 physical boundary")
    require(data["result"].get("latest_official_technology_audit", {})
            .get("external_theorem_promoted") is False, "literature nonpromotion")

    require(REPORT.is_file() and not REPORT.is_symlink(), "report file/type")
    require(CERT.is_file() and not CERT.is_symlink(), "certificate file/type")
    require(Path(__file__).resolve().is_file(), "verifier file/type")
    require(data["report_sha256"] == sha256_path(REPORT), "report hash")
    require(data["certificate_sha256"] == sha256_path(CERT), "certificate hash")
    require(data["verifier_sha256"] == sha256_path(Path(__file__).resolve()),
            "verifier hash")


def safe_dbar(m: int) -> int:
    c_p = Q(4 * 10**90 * 360493663, 358863)
    if Q(2) ** m <= c_p:
        return 0
    d = 1
    while not Q(2) ** (m - d) < c_p / 2:
        d += 1
    return d


def independent_replay(data: dict[str, Any]) -> dict[str, int | str]:
    # Gate 1 sharp threshold rows.
    rows = data["result"]["gate1"]["sharp_plaque_tempered_budget"]["threshold_rows"]
    require(len(rows) == 3, "Gate1 regime count")
    expected = [
        ("subcritical", Q(3, 2), Q(1, 4), Q(9, 16), "DECAYS"),
        ("critical", Q(2), Q(1, 4), Q(1), "CONSTANT_NONZERO"),
        ("supercritical", Q(2), Q(1, 2), Q(2), "DIVERGES"),
    ]
    sample_count = 0
    for row, (name, a, lam, theta, behavior) in zip(rows, expected):
        require(row["regime"] == name and Q(row["a"]) == a, "Gate1 regime identity")
        require(Q(row["lambda"]) == lam and Q(row["theta=a^2*lambda"]) == theta,
                "Gate1 theta")
        require(row["behavior"] == behavior and len(row["samples"]) == 10,
                "Gate1 behavior/samples")
        for n, sample in enumerate(row["samples"], 1):
            require(sample["n"] == n, "Gate1 sample n")
            require(Q(sample["endpoint_lower_defect"]) == lam ** n,
                    "Gate1 endpoint defect")
            require(Q(sample["renormalized_lower_defect"]) == theta ** n,
                    "Gate1 renormalized defect")
            sample_count += 1

    # Gate 3 artificial incidence cancellation and physical mismatch.
    incidence = data["result"]["gate3"]["oriented_incidence_reduction"]
    artificial = incidence["artificial_replay"]
    require([Q(row["cut"]) for row in artificial] ==
            [Q(1, 4), Q(1, 2), Q(3, 4)], "artificial cuts")
    for row in artificial:
        require(Q(row["left_trace"]) == Q(row["right_trace"]), "matching trace")
        require(Q(row["assembled_pairing"]) == 0, "zero artificial pairing")
    mismatch = incidence["physical_mismatch_replay"]
    require(Q(mismatch["pairing_against_phi(t)=t"]) == -1, "mismatch pairing")
    require(Q(mismatch["TV"]) == 2, "mismatch TV")

    # Exact safe-clock thresholds.
    clock = data["result"]["gate3"]["stopping_clock_jump_frontier"]["rows"]
    require(len(clock) == 13, "clock row count")
    for row in clock:
        d = safe_dbar(row["M"])
        require(row["Dbar"] == d, "Dbar replay")
        require(row["R0=696*Dbar"] == 696 * d, "clock replay")
    require(safe_dbar(310) == 0 and safe_dbar(311) == 2, "first clock jump")

    join = data["result"]["gate3"]["same_ID_regular_F13_join"]
    require(Q(join["F13_over_X"]) == Q(3816937, 7800000) < Q(1, 2),
            "F13/X ratio")
    require(Q(join["F13_over_D1"]) == Q(3816937, 47112000) < Q(25, 302),
            "F13/D1 ratio")

    taxonomy = data["result"]["gate3"]["actual_stopped_cut_taxonomy"]["rows"]
    require(len(taxonomy) == 11, "taxonomy row count")
    require(taxonomy[0]["treatment"] == "ABSENT_FROM_ACTUAL_INCIDENCE_CHAIN",
            "proof-only cuts absent")
    require(taxonomy[-1]["treatment"] == "RETAIN_SEPARATE_CLOCK_JUMP_CURRENT",
            "clock cut retained")

    return {
        "gate1_threshold_regimes": len(rows),
        "gate1_threshold_samples": sample_count,
        "gate3_artificial_faces": len(artificial),
        "gate3_taxonomy_rows": len(taxonomy),
        "gate3_clock_rows": len(clock),
        "gate3_F13_ratio_rows": 2,
        "status": "PASS",
    }


def hostile_self_test(base: dict[str, Any]) -> int:
    mutations: list[dict[str, Any]] = []
    for i in range(96):
        candidate = copy.deepcopy(base)
        candidate[f"hostile_extra_{i}"] = i
        mutations.append(candidate)
    for i in range(96):
        candidate = copy.deepcopy(base)
        candidate["result"]["strict_status"]["composite_gates"] = f"{i + 1}/5"
        candidate["result_sha256"] = canonical_digest(candidate["result"])
        mutations.append(candidate)
    for i in range(65):
        candidate = copy.deepcopy(base)
        candidate["dependencies"][i % len(DEPENDENCIES)]["sha256"] = f"{i:064x}"[-64:]
        mutations.append(candidate)
    for i in range(64):
        candidate = copy.deepcopy(base)
        candidate["result"]["gate1"]["physical_boundary"]["gate1"] = f"HOSTILE_{i}"
        candidate["result_sha256"] = canonical_digest(candidate["result"])
        mutations.append(candidate)
    for i in range(64):
        candidate = copy.deepcopy(base)
        candidate["result"]["gate3"]["stopping_clock_jump_frontier"][
            "covered_by_round44_five_face_F13"
        ] = True
        candidate["result_sha256"] = canonical_digest(candidate["result"])
        mutations.append(candidate)

    rejected = 0
    for candidate in mutations:
        try:
            validate_obj(candidate)
        except VerifyError:
            rejected += 1
    require(rejected == len(mutations) == 385, "hostile object rejection")

    raw_attacks = [
        b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}',
        b'{"x":1,"x":2}', b'[]', b'null', b'"manifest"', b'{', b'\xff',
        b'{"artifact":null}', b'{}', b'{"date":"2026-07-21"}',
        b'{"result":{}}', b'{"dependencies":[]}', b'{"schema":null}',
    ]
    raw_rejected = 0
    for raw in raw_attacks:
        try:
            value = strict_loads(raw)
            validate_obj(value, raw)
        except (VerifyError, TypeError):
            raw_rejected += 1
    require(raw_rejected == len(raw_attacks) == 15, "hostile JSON rejection")
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
            print(f"DEPENDENCIES: {len(DEPENDENCIES)}/{len(DEPENDENCIES)}")
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
    print("GATE1_SHARP_PLAQUE_TEMPERED_INTERFACE: CERTIFIED")
    print("GATE3_INCIDENCE_REDUCED_BASE_F13_JOIN: CERTIFIED")
    print("PHYSICAL_ALL_PLAQUE_STRONG_RQ_PIOLA_MT_DQ: NOT_CERTIFIED")
    print("GATES_1_3: NOT_CERTIFIED")
    print("COMPOSITE_GATES: 0/5")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
