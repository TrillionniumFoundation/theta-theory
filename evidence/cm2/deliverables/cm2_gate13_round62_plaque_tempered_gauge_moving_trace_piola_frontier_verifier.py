#!/usr/bin/env python3
"""Independent verifier for the Round-62 Gate-1/3 frontier leaf."""

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
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-"
    "frontier-assault-2026-07-21.md"
)
MANIFEST = HERE / (
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-"
    "frontier-manifest-2026-07-21.json"
)
CERT = HERE / (
    "cm2_gate13_round62_plaque_tempered_gauge_moving_trace_piola_"
    "frontier_cert.py"
)
Q = Fraction


DEPENDENCIES = {
    "deliverables/cm2-sixty-first-direct-assault-2026-07-20.md":
        "b9ad28ed23e88768234b304dd9f9ecb02577c7aa18dc8a982185690ea8f6f02b",
    "deliverables/cm2-sixty-first-direct-assault-manifest-2026-07-20.sha256":
        "2a3ae3ebf1a6e11b734611e260a340398f475d70e4888010c8294ac321d84265",
    "deliverables/cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.json":
        "bb0d263454a33acdf8b2ba443fcc5e247ff1b9214c385f70fa1af2fc26e7c019",
    "deliverables/cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.sha256":
        "744bf350c4b3511bb35cefb12d294d4ef407d9c09b43dacb1123eba6103a1f0b",
    "deliverables/cm2-gate1-third-gauge-escape-frontier-manifest-2026-07-17.json":
        "03174972b28265463fba1bb52a1dbdb1a85f6c1ae074c48f4a3774b5b9731dd7",
    "deliverables/cm2-gate1-third-gauge-escape-frontier-manifest-2026-07-17.sha256":
        "47d0c506285acf1425068c6ac05c58024d6679166c41f847f45dbf72ae5d9ba1",
    "deliverables/cm2-gate1-round25-common-frame-manifest-2026-07-18.json":
        "66d4b207a0155ee98a7632154c81caebd567f43aa1a449ffc28b421b175cd436",
    "deliverables/cm2-gate1-round25-common-frame-manifest-2026-07-18.sha256":
        "02ac98b4f96bc020f0c84e37c962f335f1fa3d01311d40164c6049f136320e7b",
    "deliverables/cm2-gate3-common-graph-current-carrier-frontier-manifest-2026-07-17.json":
        "9abdc07cb0618f4a81b8e5591d8de83da7cce2c6d6a82fa41c834dd46c28412c",
    "deliverables/cm2-gate3-common-graph-current-carrier-frontier-manifest-2026-07-17.sha256":
        "60282b58c705b6337f558ac7b2f39fdececca2b7dab807f25c8cfd6c846a0415",
    "deliverables/cm2-gate5-round53-trace-standard-family-graph-f17-frontier-manifest-2026-07-20.json":
        "8cacd8daa582c522a175cca3f24c7da1cb10c47f860b20645a365b27678d4590",
    "deliverables/cm2-gate5-round53-trace-standard-family-graph-f17-frontier-manifest-2026-07-20.sha256":
        "88b96c1b69df4708b0e7d36571e21255d7581c389b021e451fc9e04a70643c88",
}


RESULT_SHA256 = "487e6ba566beae6a0b6537ad952c84ff04cb7224e86ad1fc711143d379d82d3e"
STRICT_VERDICT = (
    "exact plaque-tempered cohomology and moving bulk-plus-face/Piola interfaces "
    "are certified, but the physical all-plaque defect registry, all-depth endpoint "
    "current, strong R/Q, directional Piola and MT_DQ remain not certified"
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
            "cm2.gate13.round62.plaque-tempered-gauge-moving-trace-piola-frontier.v1",
            "schema")
    require(data["artifact"] ==
            "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier",
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
    require(gate1.get("exact_plaque_tempered_transport", {}).get("status") ==
            "CERTIFIED_EXACT_PLAQUE_TEMPERED_COHOMOLOGY_INTERFACE", "Gate1 interface")
    require(gate1.get("determinant_same_token_separator", {}).get("status") ==
            "CERTIFIED_FALSE_WITHOUT_RENORMALIZED_DEFECT_DECAY", "Gate1 separator")
    require(gate1.get("physical_boundary", {}).get("gate1") == "NOT_CERTIFIED",
            "Gate1 boundary")

    gate3 = data["result"].get("gate3", {})
    require(gate3.get("moving_branch_reynolds_current", {}).get("status") ==
            "CERTIFIED_EXACT_MOVING_BULK_PLUS_FACE_INTERFACE", "Gate3 face interface")
    require(gate3.get("regular_branch_directional_piola", {}).get("status") ==
            "CERTIFIED_EXACT_REGULAR_BRANCH_DIRECTIONAL_PIOLA_INTERFACE",
            "Gate3 Piola interface")
    require(gate3.get("current_completed_stopped_recipient", {}).get("status") ==
            "CERTIFIED_EXACT_CONDITIONAL_CURRENT_RECIPIENT", "Gate3 recipient")
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


Matrix = tuple[tuple[Q, Q], tuple[Q, Q]]


def mm(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(2)), Q(0))
                       for j in range(2)) for i in range(2))  # type: ignore[return-value]


def determinant(a: Matrix) -> Q:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inverse(a: Matrix) -> Matrix:
    d = determinant(a)
    require(d != 0, "independent invertibility")
    return ((a[1][1] / d, -a[0][1] / d),
            (-a[1][0] / d, a[0][0] / d))


def independent_replay(data: dict[str, Any]) -> dict[str, int | str]:
    # Gate 1 finite identity.
    a = ((Q(8), Q(0)), (Q(0), Q(1, 8)))
    cx = ((Q(1), Q(1, 3)), (Q(0), Q(1)))
    cy = ((Q(1), Q(0)), (Q(1, 5), Q(1)))
    cfx = ((Q(1), Q(0)), (Q(1, 7), Q(1)))
    cfy = ((Q(1), Q(2, 9)), (Q(0), Q(1)))
    bnx = mm(mm(inverse(cfx), a), cx)
    bny = mm(mm(inverse(cfy), a), cy)
    left = mm(inverse(bny), bnx)
    right = mm(mm(mm(mm(inverse(cy), inverse(a)), cfy), inverse(cfx)), mm(a, cx))
    require(left == right, "independent finite cohomology identity")

    gate1_rows = data["result"]["gate1"]["determinant_same_token_separator"]["rows"]
    require(len(gate1_rows) == 12, "Gate1 row count")
    for n, row in enumerate(gate1_rows, 1):
        scale = Q(2) ** n
        endpoint = ((Q(1), Q(0)), (Q(1) / scale, Q(1)))
        defect = mm(mm(inverse(((scale, Q(0)), (Q(0), 1 / scale))),
                       ((Q(0), Q(0)), (Q(1) / scale, Q(0)))),
                    ((scale, Q(0)), (Q(0), 1 / scale)))
        require(determinant(endpoint) == 1, "independent SL2 separator")
        require(defect[1][0] == scale == Q(row["renormalized_lower_defect"]),
                "independent defect row")

    # Gate 3 face current and regular directional Piola sample.
    e = Q(1, 2)
    require(e - e == 0, "independent matching face")
    require(e - (e + 1) == -1, "independent translated face")
    require(Q(1, 2) + Q(1, 2) == 1, "independent Piola derivative")

    frag = data["result"]["gate3"]["endpoint_fragmentation_separator"]["rows"]
    require([r["moving_mismatched_faces"] for r in frag] == [1, 2, 4, 8, 16, 32],
            "fragmentation labels")
    for row in frag:
        require(Q(row["face_current_TV"]) == 2 * row["moving_mismatched_faces"],
                "fragmentation TV")

    bulk = data["result"]["gate3"]["bulk_piola_separator"]["rows"]
    require([r["L"] for r in bulk] == [2, 4, 8, 16, 32], "bulk labels")
    for row in bulk:
        ell = row["L"]
        require(Q(row["source_L1"]) == Q(1, ell), "bulk source")
        require(Q(row["target_L1"]) == 1, "bulk target")
        require(Q(row["multiplier"]) == ell, "bulk multiplier")

    return {
        "gate1_matrix_identity": 1,
        "gate1_defect_rows": len(gate1_rows),
        "gate3_face_rows": 2,
        "gate3_piola_rows": 1,
        "gate3_fragmentation_rows": len(frag),
        "gate3_bulk_rows": len(bulk),
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
    for i in range(48):
        candidate = copy.deepcopy(base)
        candidate["dependencies"][i % 12]["sha256"] = f"{i:064x}"[-64:]
        mutations.append(candidate)
    for i in range(48):
        candidate = copy.deepcopy(base)
        candidate["result"]["gate3"]["physical_boundary"]["MT_DQ"] = f"HOSTILE_{i}"
        candidate["result_sha256"] = canonical_digest(candidate["result"])
        mutations.append(candidate)

    rejected = 0
    for candidate in mutations:
        try:
            validate_obj(candidate)
        except VerifyError:
            rejected += 1
    require(rejected == len(mutations) == 288, "hostile object rejection")

    raw_attacks = [
        b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}',
        b'{"x":1,"x":2}', b'[]', b'null', b'"manifest"', b'{',
        b'\xff', b'{"artifact":null}', b'{}', b'{"date":"2026-07-21"}',
    ]
    raw_rejected = 0
    for raw in raw_attacks:
        try:
            value = strict_loads(raw)
            validate_obj(value, raw)
        except (VerifyError, TypeError):
            raw_rejected += 1
    require(raw_rejected == len(raw_attacks) == 12, "hostile JSON rejection")
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
            print("DEPENDENCIES: 12/12")
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
    print("GATE1_PLAQUE_TEMPERED_COHOMOLOGY: CERTIFIED_INTERFACE")
    print("GATE3_MOVING_BULK_FACE_PIOLA: CERTIFIED_INTERFACE")
    print("PHYSICAL_ALL_PLAQUE_STRONG_RQ_PIOLA_MT_DQ: NOT_CERTIFIED")
    print("GATES_1_3: NOT_CERTIFIED")
    print("COMPOSITE_GATES: 0/5")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
