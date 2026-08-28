#!/usr/bin/env python3
"""Producer for the append-only Round-64 Gate-1/3 frontier certificate."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round64_common import (
    CertError, canonical_bytes, digest, require, sha256_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate13.round64.resonant-tail-transport-current-clock.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate13-round64-resonant-tail-transport-current-clock-frontier"
DEFAULT_REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
DEFAULT_MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
DEFAULT_VERIFIER = HERE / "cm2_gate13_round64_resonant_tail_transport_current_clock_frontier_verifier.py"
COMMON = HERE / "cm2_round64_common.py"

PINS = {
    "cm2-sixty-third-direct-assault-2026-07-21.md":
        "9cde412ba689be87d777906404c9c9426a2a8a102385a2c4c510df8f9b7a6a05",
    "cm2-sixty-third-direct-assault-manifest-2026-07-21.sha256":
        "a0b512f32914ef2692b31466a4ea156c44698b1eaf44d8ead45b2c74ee73230e",
    "cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.json":
        "3aae6d018fc15aaab47116d311eed8333c56b87542b0b5761b849221cbf76d6b",
    "cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "8227dd32e36d2879f9dbbdced54f3c50b3eac1536ce8fceac480d22cb8617bfd",
    "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-manifest-2026-07-21.json":
        "bdd351955c4537e649009e753900a7f61e3befcc16db55f810af2902dd3581ea",
    "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-manifest-2026-07-21.sha256":
        "b48def6d29a68f9cf30db2b349a41e06b3e5df58766f8d9323e256f75c6ad058",
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def mmul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def safe_dbar(m: int) -> int:
    return 0 if m <= 310 else m - 309


def build_result() -> dict[str, Any]:
    identity = [[1, 0], [0, 1]]
    ls = [[0, 0], [-1, 0]]
    lu = [[0, 1], [0, 0]]
    stable = [[identity[i][j] + ls[i][j] for j in range(2)] for i in range(2)]
    unstable = [[identity[i][j] + lu[i][j] for j in range(2)] for i in range(2)]
    loop = mmul(stable, unstable)
    e1_image = [loop[0][0], loop[1][0]]
    e2_image = [loop[0][1], loop[1][1]]
    wedge_e1 = e1_image[1]
    wedge_e2 = -e2_image[0]

    transport_rows = []
    for n in range(1, 13):
        distance = Q(1, 2**n)
        transport_rows.append({
            "n": n,
            "distance": qstr(distance),
            "raw_TV": "2",
            "BL_transport_upper": qstr(distance),
        })

    clocks = [{"M": m, "Dbar": safe_dbar(m), "R0": 696 * safe_dbar(m)}
              for m in range(307, 316)]

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "append_only": True,
            "old_artifacts_modified": False,
            "pinned_round63_artifacts": PINS,
        },
        "gate1": {
            "resonant_tail_identity": {
                "status": "CERTIFIED_EXACT_INTERFACE",
                "stable": "H_B^s=C(y)^-1(H_A^s+L_s)C(x)",
                "unstable": "H_B^u=C(y)^-1(H_A^u+L_u)C(x)",
                "loop": "C(p)^-1(H_A^s+L_s)(H_A^u+L_u)C(p)",
                "required_regularities": [
                    "uniform two-sided tail convergence",
                    "uniform Holder tails on actual plaques",
                    "same physical representative carries class H and selected twisting",
                ],
            },
            "zero_tail_guard": {
                "zero_tail_preserves_zero_twisting": True,
                "round63_zero_tail_sufficient_for_Holder_only": True,
                "actual_nonzero_resonant_tail": "NOT_CERTIFIED",
            },
            "critical_SL2_replay": {
                "A": [["2", "0"], ["0", "1/2"]],
                "L_s": ls,
                "L_u": lu,
                "loop": loop,
                "determinant": loop[0][0] * loop[1][1] - loop[0][1] * loop[1][0],
                "wedge_e1": wedge_e1,
                "wedge_e2": wedge_e2,
                "zero_tail_loop": identity,
                "scope": "logical critical model, not an actual billiard gauge",
            },
            "strict_status": "NOT_CERTIFIED",
        },
        "gate3": {
            "BL_transport_bound": {
                "status": "CERTIFIED_EXACT",
                "formula": "||alpha delta_y-beta delta_z||_BL*<=|alpha-beta|+min(alpha,beta)min(2,d(y,z))",
                "rows": transport_rows,
                "finite_raw_TV_sum": qstr(sum((Q(row["raw_TV"]) for row in transport_rows), Q(0))),
                "finite_transport_sum": qstr(sum((Q(row["BL_transport_upper"]) for row in transport_rows), Q(0))),
                "infinite_transport_sum": "1",
                "infinite_raw_TV_sum": "DIVERGES",
                "physical_landing_distance_speed_ledger": "NOT_CERTIFIED",
            },
            "safe_clock": {
                "closed_form": "Dbar(M)=0 for M<=310; Dbar(M)=M-309 for M>=311",
                "rows": clocks,
                "first_jump_collision_terms": 1392,
                "later_jump_collision_terms": 696,
                "coboundary": "P^r'-P^r=sum_(k=r)^(r'-1)P^k(P-I)",
                "physical_level_trace_sum": "NOT_CERTIFIED",
            },
            "moving_null_separator": {
                "family": "mu_s=1_[s,1]dx",
                "endpoint_mass_at_s0": "0",
                "distributional_derivative_at_s0": "-delta_0",
                "fixed_time_null_implies_zero_current": False,
            },
            "strong_product_rules": {
                "D_QPR_terms": 3,
                "D_Tn_terms": "n",
                "bounded_differentiable_physical_Rs_Qs": "NOT_CERTIFIED",
                "anisotropic_Piola": "NOT_CERTIFIED",
                "MT_DQ": "NOT_CERTIFIED",
            },
            "strict_status": "NOT_CERTIFIED",
        },
        "latest_technology_boundary": {
            "arxiv_2604_19671v2": "shrinking boundary-hole conditional survival; wrong perturbation and current",
            "arxiv_2606_10155v1": "review; no moving-scatterer strong-current theorem",
            "external_theorem_promoted": False,
        },
        "strict_status": {
            "Gate1": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    replay = copy.deepcopy(result)
    result["internal_replay_digest"] = digest(replay)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    validate_pins(HERE, PINS)
    result = build_result()
    require(DEFAULT_REPORT.is_file() and verifier.is_file() and COMMON.is_file(), "artifact missing")
    return {
        "schema": MANIFEST_SCHEMA,
        "pins": PINS,
        "report_sha256": sha256_path(DEFAULT_REPORT),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier.resolve()),
        "common_sha256": sha256_path(COMMON),
        "result": result,
        "verdict": result["strict_status"],
    }


def replay() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    result = build_result()
    model = result["gate1"]["critical_SL2_replay"]
    require(model["loop"] == [[1, 1], [-1, 0]] and model["determinant"] == 1, "SL2 loop")
    require(model["wedge_e1"] == model["wedge_e2"] == -1, "axis wedges")
    transport = result["gate3"]["BL_transport_bound"]
    require(Q(transport["finite_raw_TV_sum"]) == 24, "finite raw TV")
    require(Q(transport["finite_transport_sum"]) == Q(4095, 4096), "finite transport")
    clock = result["gate3"]["safe_clock"]
    require(clock["rows"][4] == {"M": 311, "Dbar": 2, "R0": 1392}, "first safe-clock jump")
    return {"pins": "6/6", "transport_rows": 12, "clock_rows": 9, "status": "PASS"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    args = parser.parse_args()
    try:
        if args.replay:
            print(json.dumps(replay(), sort_keys=True))
            return 0
        manifest = build_manifest(args.verifier)
        payload = canonical_bytes(manifest)
        if args.manifest_json:
            sys.stdout.buffer.write(payload)
            return 0
        if args.write_manifest is not None:
            args.write_manifest.write_bytes(payload)
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, ArithmeticError) as exc:
        print(f"ROUND64_GATE13_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate1: NOT_CERTIFIED")
    print("Gate3: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
