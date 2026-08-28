#!/usr/bin/env python3
"""Exact crosswalk of the Round-67 affine collision-SRB root to 152 F14 keys."""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round85.gate5-f14-collision-srb-crosswalk.v1"
ROUND67 = HERE / "cm2-gate24-round67-actual-root-stable-tail-variation-frontier-manifest-2026-07-21.json"
WINDOWS = HERE / "cm2-round85-gate3-s0-two-sided-material-window-2026-07-22.json"
GATE5 = HERE / "cm2-round85-gate5-finite-root-operator-field-frontier-2026-07-22.json"
FROZEN_PINS = {
    "round67_collision_SRB_formula_root": "d868ff5865dd573077e814e1d562a14ef6aaee75c1607ce0303d02a40ddcee9f",
    "round67_collision_SRB_source": "35b408588971b1227bfee42877cf01ed5e861f578fd791c963fdcb83d423bc39",
    "round85_material_windows": "81356d91e1725c9f454ac010b264a0bd1fbd92b2892cca602f1ff5f9ae64b2c7",
    "round85_gate5_same_key_frontier": "f0fd1dc13a7a51b82ca0eb511ce3bd6d44fcd1744b11a0c512b7e5a96f652d19",
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_load(path: Path) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in pairs:
            if key in result: raise ValueError(f"duplicate key: {key}")
            result[key] = value
        return result
    value = json.loads(path.read_text(), object_pairs_hook=unique,
                       parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    if not isinstance(value, dict): raise ValueError("top-level object")
    return value


def count_key(value: Any, key: str) -> int:
    if isinstance(value, dict):
        return int(key in value) + sum(count_key(child, key) for child in value.values())
    if isinstance(value, list): return sum(count_key(child, key) for child in value)
    return 0


def build() -> dict[str, Any]:
    actual_pins = {
        "round67_collision_SRB_formula_root": file_digest(ROUND67),
        "round67_collision_SRB_source": file_digest(HERE / "cm2_gate24_round67_actual_root_stable_tail_variation_frontier_cert.py"),
        "round85_material_windows": file_digest(WINDOWS),
        "round85_gate5_same_key_frontier": file_digest(GATE5),
    }
    if actual_pins != FROZEN_PINS: raise ValueError(f"frozen upstream pin mismatch: {actual_pins}")
    round67 = strict_load(ROUND67)
    windows = strict_load(WINDOWS)
    gate5 = strict_load(GATE5)
    affine = round67["result"]["actual_graph_supported_pre_registry"]
    root = affine["root"]
    chart = affine["affine_chart"]
    if root["S"] != ["-3/1600", "-1/640"]: raise ValueError("Round67 S slab")
    if chart["conditional_density"] != "rho_v=q/(Z(v)*a)": raise ValueError("rho formula")
    if chart["candidate_holonomy_arclength_derivative"] != "lambda_(v,w)=a(u,w)/a(u,v)":
        raise ValueError("lambda formula")
    if chart["candidate_holonomy_RN"] != "J_(v,w)=q(u,v)Z(w)/(q(u,w)Z(v))":
        raise ValueError("J formula")
    if affine["scope_guards"]["is_Round50_58_owner_law"] is not False:
        raise ValueError("pre-registry owner guard")
    if count_key(round67, "atom_id") != 0 or count_key(round67, "r1_candidate_field_packet_id") != 0:
        raise ValueError("unexpected atom key in Round67 root")

    window_rows = windows["result"]["evidence"]["window_rows"]
    packet_rows = gate5["result"]["evidence"]["attachment_rows"]
    packet_map = {row["atom_id"]: row for row in packet_rows}
    if len(window_rows) != 152 or len(packet_map) != 152: raise ValueError("152-key census")
    S0, S1 = map(Q, root["S"])
    crosswalk_rows = []
    minimum_gap: Q | None = None
    for row in sorted(window_rows, key=lambda item: item["positive_atom_id"]):
        atom_id = row["positive_atom_id"]
        if atom_id not in packet_map: raise ValueError("material/packet key")
        W0, W1 = map(Q, row["common_s"])
        if S1 < W0:
            separator, gap = "ROUND67_S_UPPER_BELOW_WINDOW_S_LOWER", W0 - S1
        elif W1 < S0:
            separator, gap = "WINDOW_S_UPPER_BELOW_ROUND67_S_LOWER", S0 - W1
        else:
            raise ValueError("unexpected Round67/window material intersection")
        if gap <= 0: raise ValueError("strict material gap")
        minimum_gap = gap if minimum_gap is None else min(minimum_gap, gap)
        crosswalk_rows.append({
            "atom_id": atom_id,
            "candidate_packet_id": packet_map[atom_id]["candidate_packet_id"],
            "window_s": row["common_s"],
            "Round67_formula_root_s": root["S"],
            "separator": separator,
            "exact_gap": str(gap),
            "F14_formula_attachable": False,
        })
    if minimum_gap != Q(9, 6400): raise ValueError("uniform material-root separation")

    evidence = {
        "exact_rational_crosswalk": True,
        "Round67_formula_root": {
            "S": root["S"], "I_equals_V": root["I_equals_V"],
            "t0": root["t0"], "p0": root["p0"], "R_G": root["R_G"],
            "q": chart["exact_q"], "a": chart["exact_a"], "Z": chart["exact_Z"],
            "rho_v": chart["conditional_density"],
            "lambda": chart["candidate_holonomy_arclength_derivative"],
            "J": chart["candidate_holonomy_RN"],
            "is_later_owner_law": False,
        },
        "Round67_atom_id_key_count": count_key(round67, "atom_id"),
        "Round67_candidate_packet_key_count": count_key(round67, "r1_candidate_field_packet_id"),
        "material_window_count": len(window_rows),
        "strictly_material_disjoint_count": len(crosswalk_rows),
        "uniform_s_gap": "9/6400",
        "attachable_F14_row_count": 0,
        "crosswalk_rows": crosswalk_rows,
    }
    result = {
        "status": "CERTIFIED_ROUND67_COLLISION_SRB_FORMULA_ROOT_DISJOINT_FROM_ALL_152_F14_KEYS",
        "F14_regular_density_operator_cost": "NOT_CERTIFIED__FORMULA_ROOT_AND_PACKET_KEYS_DO_NOT_CROSSWALK",
        "candidate_local_maturity": "13/18_UNCHANGED",
        "F15_standard_family_operator_cost": "NOT_PROMOTED__FIRST_MISSING_FIELD_F14_REMAINS_OPEN",
        "complete_18_field_operator_blocks": 0,
        "global_Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
        "necessary_next_action": "DERIVE_COLLISION_SRB_AND_RECOVERED_STRONG_OPERATOR_COST_DIRECTLY_ON_THE_152_ATOM_KEYS",
        "strict_nonclaims": [
            "the generic algebraic formula is not relabelled onto disjoint material slabs",
            "candidate plaque formulas are not promoted to physical stable semantics",
            "no F15 value is inferred before F14 exists on the same packet",
            "no aggregate F16 value is attached",
        ],
        "evidence": evidence,
        "evidence_sha256": digest(evidence),
    }
    return {"schema": SCHEMA, "pins": dict(FROZEN_PINS), "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2, allow_nan=False); sys.stdout.write("\n"); return 0


if __name__ == "__main__": raise SystemExit(main())
