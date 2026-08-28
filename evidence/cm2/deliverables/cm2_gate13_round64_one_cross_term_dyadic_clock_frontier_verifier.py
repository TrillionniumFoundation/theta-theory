#!/usr/bin/env python3
"""Independent verifier for the Round-64 Gate-1/3 frontier leaf."""

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
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-"
    "assault-2026-07-21.md"
)
MANIFEST = HERE / (
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-"
    "manifest-2026-07-21.json"
)
CERT = HERE / (
    "cm2_gate13_round64_one_cross_term_dyadic_clock_frontier_cert.py"
)
Q = Fraction


DEPENDENCIES = {
    "deliverables/cm2-sixty-third-direct-assault-2026-07-21.md":
        "9cde412ba689be87d777906404c9c9426a2a8a102385a2c4c510df8f9b7a6a05",
    "deliverables/cm2-sixty-third-direct-assault-manifest-2026-07-21.sha256":
        "a0b512f32914ef2692b31466a4ea156c44698b1eaf44d8ead45b2c74ee73230e",
    "deliverables/cm2-round63-independent-core-frontier-audit-2026-07-21.md":
        "b30aff208e9e5707e443f59abd07507f7f9d93d765ecaf3fd675f4150c5bf978",
    "deliverables/cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.json":
        "3aae6d018fc15aaab47116d311eed8333c56b87542b0b5761b849221cbf76d6b",
    "deliverables/cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "8227dd32e36d2879f9dbbdced54f3c50b3eac1536ce8fceac480d22cb8617bfd",
    "deliverables/cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-assault-2026-07-21.md":
        "c6429e3b52a5af4af59ea1beccd02d9410a7bdee7a8abc05885d00978f99942d",
    "deliverables/cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-manifest-2026-07-21.json":
        "bdd351955c4537e649009e753900a7f61e3befcc16db55f810af2902dd3581ea",
    "deliverables/cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-manifest-2026-07-21.sha256":
        "b48def6d29a68f9cf30db2b349a41e06b3e5df58766f8d9323e256f75c6ad058",
    "deliverables/cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.json":
        "dacbae6255707086bc7486e4933d8c890ede1547a9e545995800a5fc18698f83",
    "deliverables/cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.sha256":
        "9d98591462771a9e553dd93c24518642c22aa2832c269a8380bd827a76666200",
    "deliverables/cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json":
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73",
    "deliverables/cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.sha256":
        "7fd9547443951d9960b466aa914f73b1a36f73897e31585018eceed409be4716",
    "deliverables/cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json":
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d",
    "deliverables/cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.sha256":
        "07dc2b60d6b8003f0fa3ed7bd7a69167777e8a78958811169caff847ac31480c",
}


RESULT_SHA256 = "7361b50fc879a4e420d6dc9f721bc14940a05fd86b75c8cc19de4bad0aa42da1"
STRICT_VERDICT = (
    "the combined clean-SFT Green gauge is reduced to one scalar cross term and "
    "the safe clock to one dyadic trace ledger, but the actual scalar limit, "
    "selected same-representative twisting, finite-s clock traces, strong "
    "cemetery, anisotropic bulk Piola, strong R/Q and MT_DQ remain not certified"
)
C_P = Q(4 * 10**90 * 360493663, 358863)


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
    return (json.dumps(value, indent=2, sort_keys=True,
                       ensure_ascii=False) + "\n").encode()


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
        require(path.is_file() and not path.is_symlink(),
                f"dependency file/type: {rel}")
        require(sha256_path(path) == expected,
                f"dependency hash drift: {rel}")
        rows.append({"path": rel, "sha256": expected})
    return rows


def validate_obj(data: Any, raw: bytes | None = None) -> None:
    require(type(data) is dict, "manifest object")
    require(set(data) == {
        "artifact", "certificate_sha256", "date", "dependencies",
        "report_sha256", "result", "result_sha256", "schema",
        "strict_verdict", "verifier_sha256",
    }, "manifest exact top-level schema")
    if raw is not None:
        require(raw == canonical_bytes(data), "canonical manifest bytes")
    require(data["artifact"] ==
            "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier",
            "artifact")
    require(data["schema"] ==
            "cm2.gate13.round64.one-cross-term-dyadic-clock-frontier.v1",
            "schema")
    require(data["date"] == "2026-07-21", "date")
    expected_deps = [{"path": rel, "sha256": digest}
                     for rel, digest in DEPENDENCIES.items()]
    require(data["dependencies"] == expected_deps, "dependency rows")
    require(type(data["result"]) is dict, "result type")
    require(canonical_digest(data["result"]) ==
            data["result_sha256"] == RESULT_SHA256, "result digest")
    require(data["strict_verdict"] == STRICT_VERDICT, "strict verdict")
    require(data["result"].get("strict_status") == {
        "cm2": "NO-GO_FOR_CLAIM",
        "composite_gates": "0/5",
        "gate1": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
    }, "strict status")

    gate1 = data["result"].get("gate1", {})
    require(gate1.get("exact_one_cross_term_reduction", {}).get("status") ==
            "CERTIFIED_EXACT_ONE_CROSS_TERM_REDUCTION_ON_CLEAN_SFT",
            "Gate1 reduction status")
    require(gate1.get("sharp_scalar_budget", {}).get("status") ==
            "CERTIFIED_CONDITIONAL_BUDGET_SHARP_FOR_AUTOMATIC_DECAY",
            "Gate1 budget status")
    require(gate1.get("sharp_scalar_budget", {}).get("necessity_claimed_for_class_H")
            is False, "Gate1 no necessity promotion")
    require(gate1.get("physical_boundary", {}) == {
        "actual_numeric_q_cross_less_than_one": "NOT_CERTIFIED",
        "actual_uniform_holder_limit_of_T_n": "NOT_CERTIFIED",
        "compact_to_third_plaque_tempered_transport": "NOT_CERTIFIED",
        "full_mass_physical_PPE": "NOT_CERTIFIED",
        "gate1": "NOT_CERTIFIED",
        "selected_twisting_in_same_combined_representative": "NOT_CERTIFIED",
    }, "Gate1 physical boundary")

    gate3 = data["result"].get("gate3", {})
    require(gate3.get("safe_clock_closed_form", {}).get("status") ==
            "CERTIFIED_EXACT_SAFE_CLOCK_CLOSED_FORM", "clock closed form")
    require(gate3.get("dyadic_clock_trace_ledger", {}).get("status") ==
            "CERTIFIED_EXACT_DYADIC_CLOCK_TRACE_INTERFACE", "clock ledger")
    require(gate3.get("dyadic_clock_trace_ledger", {})
            .get("collision_time_distance_multiplier") is False,
            "no collision-time distance multiplier")
    require(gate3.get("weak_input_separator", {}).get("status") ==
            "CERTIFIED_FALSE_FROM_WEAK_TV_F13_AND_WEAK_CEMETERY",
            "clock separator")
    require(gate3.get("physical_boundary", {}) == {
        "MT_DQ": "NOT_CERTIFIED",
        "anisotropic_bulk_directional_Piola": "NOT_CERTIFIED",
        "common_finite_s_dyadic_level_atlas": "NOT_CERTIFIED",
        "finite_physical_E_clock_dyad": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
        "moving_regular_strong_trace": "NOT_CERTIFIED",
        "physical_strong_R_s_Q_s": "NOT_CERTIFIED",
        "strong_cemetery": "NOT_CERTIFIED",
    }, "Gate3 physical boundary")
    require(data["result"].get("latest_official_technology_audit", {})
            .get("external_theorem_promoted") is False,
            "literature nonpromotion")

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


def det(a: Matrix) -> Q:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv(a: Matrix) -> Matrix:
    d = det(a)
    require(d != 0, "matrix invertibility")
    return ((a[1][1] / d, -a[0][1] / d),
            (-a[1][0] / d, a[0][0] / d))


def green_matrix(u: Q, v: Q) -> Matrix:
    return ((1 + v * u, v), (u, Q(1)))


def safe_dbar(m: int) -> int:
    if Q(2) ** m <= C_P:
        return 0
    d = 1
    while not Q(2) ** (m - d) < C_P / 2:
        d += 1
    return d


def independent_replay(data: dict[str, Any]) -> dict[str, int | str]:
    # Re-derive the generic relative matrix independently.
    ux, uy = Q(2, 7), Q(5, 11)
    vx, vy = Q(3, 5), Q(-4, 9)
    du, dv = uy - ux, vy - vx
    relative = mm(green_matrix(uy, vy), inv(green_matrix(ux, vx)))
    expected: Matrix = (
        (1 + vy * du, dv - vy * du * vx),
        (du, 1 - du * vx),
    )
    require(relative == expected and det(relative) == 1,
            "independent Green relative identity")

    regimes = data["result"]["gate1"]["sharp_scalar_budget"]["regime_rows"]
    expected_regimes = [
        ("subcritical_decay", Q(1, 2), Q(1, 4), Q(1, 2),
         "positive", "DECAYS_TO_ZERO"),
        ("critical_constant", Q(1, 4), Q(1, 4), Q(1),
         "positive", "CONVERGES_NONZERO"),
        ("critical_oscillatory", Q(1, 4), Q(1, 4), Q(1),
         "alternating", "NO_LIMIT"),
        ("supercritical", Q(1, 4), Q(1, 2), Q(2),
         "positive", "UNBOUNDED"),
    ]
    require(len(regimes) == len(expected_regimes), "Gate1 regime count")
    sample_count = 0
    for row, (name, rho, lam, q, pattern, behavior) in zip(regimes,
                                                            expected_regimes):
        require(row["name"] == name and Q(row["rho_star"]) == rho,
                "Gate1 regime identity")
        require(Q(row["lambda_u_to_alpha"]) == lam and
                Q(row["q_cross"]) == q == lam / rho,
                "Gate1 regime ratio")
        require(row["pattern"] == pattern and row["behavior"] == behavior,
                "Gate1 regime behavior")
        require(len(row["samples"]) == 10, "Gate1 sample count")
        for n, sample in enumerate(row["samples"], 1):
            sign = -1 if pattern == "alternating" and n % 2 else 1
            delta = sign * lam ** n
            scalar = sign * q ** n
            require(sample["n"] == n, "Gate1 sample n")
            require(Q(sample["delta_u_n"]) == delta, "Gate1 delta_u")
            require(Q(sample["D_y_D_x_inverse_upper_cross_coordinate"]) ==
                    -delta, "Gate1 relative upper cross")
            require(Q(sample["T_n"]) == scalar, "Gate1 scalar cross")
            d_x = green_matrix(Q(0), Q(1))
            d_y = green_matrix(delta, Q(1))
            require(det(mm(d_y, inv(d_x))) == 1,
                    "Gate1 sample SL2 identity")
            sample_count += 1

    clock = data["result"]["gate3"]["safe_clock_closed_form"]
    require(Q(2) ** 310 < C_P < Q(2) ** 311, "independent C_p bracket")
    require(Q(2) ** 309 < C_P / 2 < Q(2) ** 310,
            "independent C_p/2 bracket")
    for m in range(501):
        closed = 0 if m <= 310 else m - 309
        require(safe_dbar(m) == closed, "independent safe-clock closed form")
    expected_ms = [306, 307, 308, 309, 310, 311, 312, 313,
                   314, 315, 319, 330, 400]
    require([row["M"] for row in clock["rows"]] == expected_ms,
            "clock row M values")
    for row in clock["rows"]:
        d = safe_dbar(row["M"])
        require(row["Dbar"] == d and row["R0=696*Dbar"] == 696 * d,
                "clock row replay")

    separator = data["result"]["gate3"]["weak_input_separator"]["rows"]
    expected_counts = [1, 2, 4, 8, 16, 32]
    require([row["moving_clock_faces"] for row in separator] == expected_counts,
            "separator face counts")
    for row, count in zip(separator, expected_counts):
        require(Q(row["weak_source_restriction_TV"]) == 1,
                "separator weak TV")
        require(Q(row["base_regular_F13_charge"]) == 0 and
                Q(row["weak_cemetery_mass"]) == 0,
                "separator zero old inputs")
        require(Q(row["clock_current_TV"]) == 2 * count,
                "separator clock TV")

    return {
        "gate1_regimes": len(regimes),
        "gate1_samples": sample_count,
        "gate3_clock_rows": len(clock["rows"]),
        "gate3_closed_form_checks": 501,
        "gate3_separator_rows": len(separator),
        "status": "PASS",
    }


def hostile_self_test(base: dict[str, Any]) -> tuple[int, int]:
    mutations: list[dict[str, Any]] = []
    for i in range(64):
        candidate = copy.deepcopy(base)
        candidate[f"hostile_extra_{i}"] = i
        mutations.append(candidate)
    for i in range(64):
        candidate = copy.deepcopy(base)
        candidate["result"]["strict_status"]["gate1"] = f"PROMOTED_{i}"
        candidate["result_sha256"] = canonical_digest(candidate["result"])
        mutations.append(candidate)
    for i in range(64):
        candidate = copy.deepcopy(base)
        candidate["result"]["gate1"]["sharp_scalar_budget"][
            "necessity_claimed_for_class_H"
        ] = True
        candidate["result_sha256"] = canonical_digest(candidate["result"])
        mutations.append(candidate)
    for i in range(64):
        candidate = copy.deepcopy(base)
        candidate["result"]["gate3"]["dyadic_clock_trace_ledger"][
            "collision_time_distance_multiplier"
        ] = True
        candidate["result_sha256"] = canonical_digest(candidate["result"])
        mutations.append(candidate)
    for i in range(32):
        candidate = copy.deepcopy(base)
        candidate["dependencies"][i % len(DEPENDENCIES)]["sha256"] = (
            f"{i:064x}"[-64:]
        )
        mutations.append(candidate)

    semantic_rejected = 0
    for candidate in mutations:
        try:
            validate_obj(candidate)
        except VerifyError:
            semantic_rejected += 1
    require(semantic_rejected == len(mutations) == 288,
            "hostile semantic rejection")

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
        except (VerifyError, TypeError, KeyError):
            raw_rejected += 1
    require(raw_rejected == len(raw_attacks) == 15,
            "hostile strict-JSON rejection")
    return semantic_rejected, raw_rejected


def load_manifest(path: Path) -> tuple[dict[str, Any], bytes]:
    require(path.is_file() and not path.is_symlink(), "manifest file/type")
    raw = path.read_bytes()
    data = strict_loads(raw)
    require(type(data) is dict, "manifest mapping")
    return data, raw


def reemit(path: Path) -> None:
    completed = subprocess.run(
        [sys.executable, str(CERT), "--emit", str(path)],
        cwd=ROOT, text=True, capture_output=True,
    )
    require(completed.returncode == 0,
            f"producer reemit: {completed.stderr}")
    require(path.read_bytes() == MANIFEST.read_bytes(),
            "byte-identical producer reemit")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", nargs="?", const=MANIFEST, type=Path)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        validate_dependencies()
        manifest_path = args.verify if args.verify is not None else MANIFEST
        data, raw = load_manifest(manifest_path)
        validate_obj(data, raw)
        if args.integrity_only:
            print("INTEGRITY: PASS")
            print(f"DEPENDENCIES: {len(DEPENDENCIES)}/{len(DEPENDENCIES)}")
            return 0
        if args.replay:
            print(json.dumps(independent_replay(data), sort_keys=True))
            return 0
        if args.self_test:
            semantic, raw_count = hostile_self_test(data)
            print(f"HOSTILE_SEMANTIC_REJECTED: {semantic}/{semantic}")
            print(f"HOSTILE_STRICT_JSON_REJECTED: {raw_count}/{raw_count}")
            return 0
        if args.reemit is not None:
            reemit(args.reemit)
            print("REEMIT: BYTE_IDENTICAL")
            return 0
        independent_replay(data)
        if args.verify is not None:
            print("VERIFY: PASS")
            return 0
    except (VerifyError, OSError, ValueError, KeyError,
            subprocess.SubprocessError) as exc:
        print(f"VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("GATE1_ONE_CROSS_TERM_REDUCTION: CERTIFIED")
    print("GATE3_DYADIC_CLOCK_TRACE_INTERFACE: CERTIFIED")
    print("ACTUAL_CROSS_TERM_CLOCK_PIOLA_STRONG_RQ_MT_DQ: NOT_CERTIFIED")
    print("GATES_1_3: NOT_CERTIFIED")
    print("COMPOSITE_GATES: 0/5")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
