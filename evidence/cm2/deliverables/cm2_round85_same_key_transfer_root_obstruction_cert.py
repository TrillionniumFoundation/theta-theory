#!/usr/bin/env python3
"""Bind the Round-67 transfer equation to the Round-69 base-root escape."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_round84_c24_base_root_same_key_escape_cert as escape


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round85.same-key-transfer-root-obstruction.v1"
ROUND67 = HERE / "cm2-gate13-round67-actual-root-transfer-uniform-piola-frontier-manifest-2026-07-21.json"
ROUND69 = HERE / "cm2-round69-base-s-return-incidence-all-gate-manifest-2026-07-21.json"
ESCAPE_JSON = HERE / "cm2-round84-c24-base-root-same-key-escape-2026-07-22.json"
ESCAPE_AUDIT = HERE / "cm2-round84-c24-base-root-same-key-escape-audit-2026-07-22.json"
EXPECTED_PINS = {
    "round67_transfer_manifest": "af4a0013714bd241d32d3dea215cfbcce4673f594931763da36e6bc2356cfb46",
    "round69_base_root_manifest": "08d996d52d6aa8ea3b716a46b51d6ae8f0a6b4b9e24c9fab402afe88059bc838",
    "round84_escape_source": "49380d961dbaeff073c4387bb0456138d737af529eb14397e06a21114da8a20d",
    "round84_escape_certificate": "2a778de6b8a4650c927ff25df477fde813957289f9edfe2742dc5aafae67706b",
    "round84_escape_audit": "4d9c6e2672b413efa07a3d078c181d97c32d517b1134dce160dab8d2d87955e1",
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_strict(path: Path) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate key in {path.name}: {key}")
            result[key] = value
        return result

    value = json.loads(
        path.read_text(), object_pairs_hook=unique,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if not isinstance(value, dict):
        raise ValueError(f"top-level object: {path.name}")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def build(precision_bits: int = 512) -> dict[str, Any]:
    round67 = load_strict(ROUND67)
    round69 = load_strict(ROUND69)
    frozen_escape = load_strict(ESCAPE_JSON)
    replay_escape = escape.build(precision_bits)
    if precision_bits == 512:
        require(frozen_escape == replay_escape, "Round84 escape exact replay")
    else:
        frozen_result = frozen_escape["result"]
        replay_result = replay_escape["result"]
        require(
            replay_result["registered_base_root_depth2_self_intersection_count"]
            == frozen_result["registered_base_root_depth2_self_intersection_count"],
            "Round84 escape higher-precision intersection invariant",
        )
        for key in (
            "registered_base_owner_atom_count", "registered_directed_core_edge_count",
            "landing_atom_count", "same_destination_core_atom_comparison_count",
            "separator_histogram", "uniform_coordinate_gap_strict_lower",
        ):
            require(
                replay_result["evidence"][key] == frozen_result["evidence"][key],
                f"Round84 escape higher-precision invariant: {key}",
            )

    root67 = round67["result"]["gate1"]["maximal_actual_root_crosswalk"]
    require(root67["same_root_tokens"] == "CERTIFIED", "Round67 root tokens")
    require(root67["same_physical_derivative_cocycle"] == "CERTIFIED", "Round67 cocycle")
    require(root67["relative_transfer"] == "C=Q^-1 E D", "Round67 transfer identity")
    require(root67["same_key_Q_E_u_v_rows"] == "NOT_CERTIFIED", "Round67 missing rows")

    base69 = round69["result"]["actual_base_s_return_root"]
    require(base69["owned_by_lower_closed_upper_open_rule"] == 176, "Round69 owner census")
    escaped = replay_escape["result"]
    evidence = escaped["evidence"]
    require(evidence["registered_base_owner_atom_count"] == 176, "escape owner census")
    require(evidence["landing_atom_count"] == 176, "escape landing census")
    require(evidence["same_destination_core_atom_comparison_count"] == 1360,
            "escape comparison census")
    require(escaped["registered_base_root_depth2_self_intersection_count"] == 0,
            "empty depth2 self-intersection")
    require(evidence["uniform_coordinate_gap_strict_lower"] == "1/100",
            "uniform escape gap")

    # The Round-67 cohomology formula evaluates Q at sigma(x).  A row whose
    # domain and landing key are both the chosen root therefore requires
    # x in R and sigma(x) in R.  The certified empty R cap sigma^-1(R) makes
    # every nonempty same-root transfer row impossible on this frozen root.
    result = {
        "status": "CERTIFIED_CURRENT_ROUND69_ROOT_HAS_NO_NONEMPTY_SAME_KEY_TRANSFER_DOMAIN",
        "transfer_requirement": {
            "equation": "A_c(x)=C(sigma x)^-1 A_q(x) C(x)",
            "relative_transfer": "C=Q^-1 E D",
            "required_key_membership": "x in R and sigma(x) in R",
            "required_export": "Q,E,u,v on one immutable physical root key",
        },
        "current_root": {
            "root": "Round69 lower-closed s=0 owner union R",
            "owner_atom_count": 176,
            "one_step_landing_atom_count": 176,
            "destination_owner_comparison_count": 1360,
            "uniform_p_coordinate_gap_strict_lower": "1/100",
            "R_intersection_sigma_inverse_R_atom_count": 0,
        },
        "same_key_Q_E_u_v_transfer_rows_installable_on_current_root": 0,
        "necessary_next_action": "RESELECT_OR_ENLARGE_THE_PHYSICAL_ROOT_BEFORE_EXPORTING_TRANSFER_ROWS",
        "gate1": "NOT_CERTIFIED_UNCHANGED",
        "gate4": "1/7_UNCHANGED",
        "strict_nonclaims": [
            "no claim that another C24 subroot cannot be invariant",
            "no claim that all C24 points escape C24",
            "no abstract or selected-record completion of Q,E,u,v",
            "no claim that the formal rational replay is a physical transfer row",
        ],
    }
    pins = {
        "round67_transfer_manifest": file_digest(ROUND67),
        "round69_base_root_manifest": file_digest(ROUND69),
        "round84_escape_source": file_digest(HERE / "cm2_round84_c24_base_root_same_key_escape_cert.py"),
        "round84_escape_certificate": file_digest(ESCAPE_JSON),
        "round84_escape_audit": file_digest(ESCAPE_AUDIT),
    }
    require(pins == EXPECTED_PINS, "frozen upstream pin mismatch")
    return {"schema": SCHEMA, "pins": pins, "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2, allow_nan=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
