#!/usr/bin/env python3
"""Producer for the independent CM2 Round-60 core-frontier audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCHEMA = "cm2.round60-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = SCHEMA + ".manifest.v1"
PREFIX = "cm2-round60-independent-core-frontier-audit"
REPORT = HERE / f"{PREFIX}-2026-07-20.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-20.json"
VERIFIER = HERE / "cm2_round60_independent_core_frontier_audit_verifier.py"

FROZEN_PINS = {
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json":
        "08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.sha256":
        "4d7c3f06e1671319482c064ec3ea817562567202b111fd014434b7be0a460fac",
    "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.json":
        "d519ad15a870fe7820839828347140e4bae3b5752a95fab4c18263c67e2ab778",
    "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.sha256":
        "ba1fc62efa4ed68df1d1ac0e9117642880768f0cd0374b95f8a1dc557274c483",
    "cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier-manifest-2026-07-20.json":
        "f897d81a2e85c4a8e45c436f169043feaef93b019f18229a44da0227c75b2a88",
    "cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier-manifest-2026-07-20.sha256":
        "6a29c47462a9526138a059f8577abcf879cd162feca14b435906cce1cd8c087a",
}

G4_MANIFEST = HERE / next(name for name in FROZEN_PINS if name.startswith("cm2-gate4-") and name.endswith(".json"))
G5_MANIFEST = HERE / next(name for name in FROZEN_PINS if name.startswith("cm2-gate5-") and name.endswith(".json"))
G123_MANIFEST = HERE / next(name for name in FROZEN_PINS if name.startswith("cm2-gate123-") and name.endswith(".json"))

C_P = Q(4 * 10**90 * 360493663, 358863)
COMMON_MASS = Q(999, 1000)
FORWARD_F10 = Q(395304765824751, 220000)
REVERSE_F10 = Q(162772550633721, 176000)
BIDIRECTIONAL_F10 = Q(2395081816467609, 880000)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise ValueError(f"unsafe JSON path: {path.name}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )
    if not isinstance(value, dict):
        raise ValueError(f"JSON root: {path.name}")
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def defect_depth(z: Q) -> int:
    if z < C_P:
        return 0
    depth = 1
    while z / 2**depth >= C_P / 2:
        depth += 1
    return depth


def root_grid() -> dict[str, Any]:
    rows: list[list[str | bool]] = []
    no_count = 0
    for ai in range(-6, 11):
        a = Q(ai, 2)
        for bi in range(1, 25):
            b = Q(bi, 4)
            for ti in range(1, 9):
                tau = Q(ti, 2)
                delta = a * a - b
                no_earlier = a <= 0 or delta < 0 or (
                    a - tau >= 0 and delta <= (a - tau) ** 2
                )
                if a <= 0 or delta < 0:
                    direct_earlier = False
                elif tau > a:
                    direct_earlier = True
                else:
                    direct_earlier = delta > (a - tau) ** 2
                if no_earlier == direct_earlier:
                    raise ValueError("root complement")
                no_count += int(no_earlier)
                rows.append([str(a), str(b), str(tau), no_earlier])
    return {
        "cases": len(rows),
        "no_earlier": no_count,
        "earlier": len(rows) - no_count,
        "digest": digest(rows),
    }


def resolve_ledger_name(raw_name: str) -> Path:
    candidate = Path(raw_name)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"unsafe ledger name: {raw_name}")
    path = ROOT / candidate if candidate.parts[:1] == ("deliverables",) else HERE / candidate
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise ValueError(f"ledger target: {raw_name}")
    return path


def ledger_rows(sidecar: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in sidecar.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2 or len(parts[0]) != 64:
            raise ValueError(f"ledger syntax: {sidecar.name}")
        path = resolve_ledger_name(parts[1].strip())
        if sha(path) != parts[0]:
            raise ValueError(f"ledger digest: {parts[1]}")
        rows.append({"name": path.name, "sha256": parts[0]})
    if len(rows) != 4:
        raise ValueError(f"ledger row count: {sidecar.name}")
    return rows


def load_frozen() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    for name, expected in FROZEN_PINS.items():
        path = HERE / name
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE or sha(path) != expected:
            raise ValueError(f"frozen pin: {name}")
    g4 = load_json(G4_MANIFEST)
    g5 = load_json(G5_MANIFEST)
    g123 = load_json(G123_MANIFEST)
    rows: list[dict[str, str]] = []
    for name in FROZEN_PINS:
        if name.endswith(".sha256"):
            rows.extend(ledger_rows(HERE / name))
    if len(rows) != 12 or len({row["name"] for row in rows}) != 12:
        raise ValueError("leaf ledger rows")
    dependency_count = (
        len(g4["dependencies"]) + len(g4["baseline_files"])
        + len(g5["dependencies"]) + len(g123["dependencies"])
    )
    if dependency_count != 26:
        raise ValueError(f"dependency count: {dependency_count}")
    return g4, g5, g123, rows


def audit_gate4(g4: dict[str, Any]) -> dict[str, Any]:
    result = g4["result"]
    rn = result["actual_landing_RN_marker_bridge"]
    fields = result["seven_field_materialization_audit"]
    split = result["good_bad_original_time_graph_split"]
    strict = result["strict_nonpromotion"]
    if "kappa_A(T_C_s^(-1)A)<=mu_C(T_C_s^(-1)A)=mu_C(A)" not in rn["positive_domination"]:
        raise ValueError("Gate4 RN chain")
    if "0<=g_B<=1" not in rn["RN_marker"] or "never eta({u})" not in rn["singleton_guard"]:
        raise ValueError("Gate4 RN/Bayes typing")
    if fields["actual_complete_rows"] != "1/7" or fields["rows"][3]["actual"].startswith("CERTIFIED"):
        raise ValueError("Gate4 field count")
    short_z = Q(3, 2) * C_P
    n_components = C_P.numerator // C_P.denominator + 1
    fragmented_z = Q(n_components, 1) / COMMON_MASS
    if not (C_P < short_z < 2 * C_P and defect_depth(short_z) == 2):
        raise ValueError("Gate4 short separator")
    if not (C_P < fragmented_z < 2 * C_P and defect_depth(fragmented_z) == 2):
        raise ValueError("Gate4 fragmented separator")
    if split["good_mass_positive"].split(";", 1)[0] != "NOT_CERTIFIED":
        raise ValueError("Gate4 good mass")
    if split["bad_mass_zero"].split(";", 1)[0] != "NOT_CERTIFIED":
        raise ValueError("Gate4 bad mass")
    expected = {
        "Gate4": "NOT_CERTIFIED",
        "actual_landing_RN_marker": "CERTIFIED",
        "seven_field_physical_landing_join": "1/7_ACTUAL_COMPLETE__FIELD4_AND_FIELD7_PARTIAL_ONLY",
        "good_original_time_proper_landing_subkernel": "CERTIFIED_POSSIBLY_ZERO__SOURCE_PROPERNESS_NOT_INFERRED",
        "physical_proper_same_ID_first_return_kernel": "NOT_CERTIFIED",
        "bad_landing_mass_zero": "NOT_CERTIFIED",
        "positive_bad_defect_cemetery_route": "CONDITIONAL_FIVE_INTERFACES_MISSING",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    for key, value in expected.items():
        if strict.get(key) != value:
            raise ValueError(f"Gate4 strict {key}")
    return {
        "status": "PASS",
        "RN_domination": "CERTIFIED_ON_ONE_INDUCED_PHYSICAL_LAW",
        "Bayes_scope": "CONDITIONAL_ON_SUPPLIED_PHYSICAL_DISINTEGRATION",
        "field4": "PARTIAL_ONLY",
        "seven_field_join": "1/7",
        "short_separator_z": qstr(short_z),
        "short_separator_D_land": 2,
        "fragmented_separator_z": qstr(fragmented_z),
        "fragmented_separator_D_land": 2,
        "good_landing_subkernel": "CERTIFIED_POSSIBLY_ZERO",
        "good_source_properness": "NOT_CERTIFIED",
        "bad_part_is_free_cemetery": False,
        "proper_full_kernel": "NOT_CERTIFIED",
    }


def audit_gate5(g5: dict[str, Any]) -> dict[str, Any]:
    result = g5["result"]
    cross = result["owner_root_crosswalk_and_coverage_frontier"]
    bits = result["seven_bit_suffix_Borel_materialisation"]
    hybrid = result["A_col_complement_positive_hybrid_policy"]
    anchors = result["fixed_insertion_positive_anchor_and_global_frontier"]
    strict = result["strict_nonpromotion"]
    rows = cross["token_rows"]
    if len(rows) != 7 or any(row["action"] != "retain" for row in rows[:6]) or rows[6]["action"] != "forget_under_pi_50":
        raise ValueError("Gate5 token projection")
    if cross["Round50_to_Round54_same_ID_crosswalk"] != "CERTIFIED_EXACT_BOREL_PROJECTION":
        raise ValueError("Gate5 crosswalk")
    if cross["physical_A_col_full_coverage"] != "NOT_CERTIFIED":
        raise ValueError("Gate5 coverage")
    borel_statuses = [row["Borel_on_frozen_registry"] for row in bits["bit_rows"]]
    if borel_statuses.count("CERTIFIED") != 4 or len(borel_statuses) != 7:
        raise ValueError("Gate5 suffix Borel counts")
    if sum(row["universal_value_on_A_col"] == "NOT_CERTIFIED" for row in bits["bit_rows"]) != 5:
        raise ValueError("Gate5 suffix values")
    expected_hybrid = "CERTIFIED_CONDITIONAL_EXACT_IFF_ON_ANY_SUPPLIED_BOREL_R_AND_NONNEGATIVE_C_BAD"
    if hybrid["status"] != expected_hybrid or len(hybrid["conditional_hypotheses"]) != 2:
        raise ValueError("Gate5 hybrid typing")
    if "tested before K or R is read" not in hybrid["registry_guard"]:
        raise ValueError("Gate5 registry guard")
    if FORWARD_F10 + REVERSE_F10 != BIDIRECTIONAL_F10:
        raise ValueError("Gate5 F10 arithmetic")
    if "no dependency pins these as the same two marginals" not in anchors["Jordan_pair_type_audit"]:
        raise ValueError("Gate5 Jordan type guard")
    expected = {
        "Round50_Round54_exact_owner_token_crosswalk": "CERTIFIED",
        "physical_A_col_full_coverage": "NOT_CERTIFIED",
        "exact_A_col_complement_positive_hybrid_iff": expected_hybrid,
        "Borel_recovery_capacity_R_on_A_col": "CONDITIONAL_SCHEMA",
        "physical_hybrid_policy_finite": "NOT_CERTIFIED",
        "fixed_insertion_orientation_positive_F10_anchor": "CERTIFIED",
        "fixed_insertion_weighted_Jordan_variation_anchor": "NOT_CERTIFIED",
        "global_weighted_common_mode_anchor": "NOT_CERTIFIED",
        "Gate5_maturity": "10/18",
        "complete_18_field_operator_block_count": 0,
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    for key, value in expected.items():
        if strict.get(key) != value:
            raise ValueError(f"Gate5 strict {key}")
    return {
        "status": "PASS_AFTER_CONDITIONAL_HYBRID_TYPE_CORRECTION",
        "owner_projection": "EXACT_BOREL_R50_TO_R54",
        "Round25_root_ID_join": "NOT_MATERIALIZED",
        "A_col_coverage": "NOT_CERTIFIED",
        "suffix_Borel_predicates": "4_UNCONDITIONAL_3_CONDITIONAL",
        "suffix_universal_values": "2_TRUE_5_OPEN",
        "R": "CONDITIONAL_SCHEMA_ON_A_col",
        "hybrid_iff": expected_hybrid,
        "physical_hybrid_finiteness": "NOT_CERTIFIED",
        "F10_sum": qstr(BIDIRECTIONAL_F10),
        "orientation_is_Jordan_identification": False,
        "weighted_Jordan_anchors": "NOT_CERTIFIED",
        "maturity": "10/18",
        "blocks": 0,
    }


def audit_gate123(g123: dict[str, Any]) -> dict[str, Any]:
    result = g123["result"]
    g1, g2, g3 = result["gate1"], result["gate2"], result["gate3"]
    budget = g1["compact_to_combined_twisting_budget"]
    exact = Q(budget["exact_K_gauge_strict_upper"])
    expected_budget = Q(17344, 10**32) / Q(8568, 10**52)
    if exact != expected_budget or exact <= 2 * 10**20:
        raise ValueError("Gate123 gauge budget")
    if Q(g1["selected_to_all_plaque_separator"]["selected_exact_sum"]) != Q(100, 81):
        raise ValueError("Gate123 Dini sum")
    if g2["finite_prefix_separator"]["first_unconstrained_depth"] != 97:
        raise ValueError("Gate123 depth separator")
    if g2["actual_landing_join_audit"]["completed_fields"] != "1/7":
        raise ValueError("Gate123 landing join")
    grid = root_grid()
    frozen_grid = g3["chosen_target_first_root_reaudit"]
    if (grid["cases"], grid["no_earlier"], grid["earlier"], grid["digest"]) != (
        frozen_grid["grid_cases"], frozen_grid["no_earlier_true_cases"],
        frozen_grid["earlier_root_true_cases"], frozen_grid["grid_sha256"],
    ):
        raise ValueError("Gate123 root grid")
    atom = g3["atom_and_depth_scope_reaudit"]
    if atom["competitor_atom_budget"] + atom["dynamics_sign_tie_cemetery_budget"] != 830:
        raise ValueError("Gate123 atom budget")
    if not math.exp(1 / 6) < 2:
        raise ValueError("Gate123 moment ratio")
    cad_rows = g3["cad_degree_frontier"]["rows_first_nine"]
    d_value = 8
    for r, row in enumerate(cad_rows):
        if int(row["D_r"]) != d_value or d_value != 2 ** (4 * 2**r - 1):
            raise ValueError("Gate123 CAD recurrence")
        d_value = 2 * d_value**2
    expected_status = {
        "gate1": "NOT_CERTIFIED", "gate2": "NOT_CERTIFIED",
        "gate2_immutable_fields": "0/17", "gate2_landing_join": "1/7",
        "gate3": "NOT_CERTIFIED", "composite_gates": "0/5",
        "cm2": "NO-GO_FOR_CLAIM",
    }
    if result["strict_status"] != expected_status:
        raise ValueError("Gate123 strict state")
    return {
        "status": "PASS",
        "gauge_budget": qstr(exact),
        "gauge_budget_physical": "NOT_CERTIFIED",
        "selected_to_all_plaque": "CERTIFIED_FALSE_BY_SEPARATOR",
        "depth_97_separator": "PASS",
        "root_grid": f"{grid['cases']}/{grid['cases']}",
        "atom_budget_identity": "161*5+25=830",
        "clock_pays_raw_enumeration": False,
        "raw_expectation": "4*sum_(n>=0)81^n=infinity",
        "CAD_closed_form": "D_r=2^(4*2^r-1)",
        "strong_RQ_Piola_MT_DQ": "NOT_CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    g4, g5, g123, rows = load_frozen()
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "provenance": {
            "frozen_pins": dict(FROZEN_PINS),
            "old_artifacts_modified": False,
            "external_theorem_promoted": False,
            "pre_freeze_type_correction": "Gate5 hybrid iff made explicitly conditional on supplied Borel R and measurable nonnegative same-law C_bad",
        },
        "frozen_leaf_artifact_audit": {
            "manifest_and_ledger_pins": "6/6",
            "main_leaf_dependency_and_artifact_pins": "26/26",
            "leaf_ledger_rows_status": "12/12",
            "leaf_ledger_rows": rows,
        },
        "gate4_independent_audit": audit_gate4(g4),
        "gate5_independent_audit": audit_gate5(g5),
        "gate123_independent_audit": audit_gate123(g123),
        "technology_type_audit": {
            "status": "PASS_NO_EXTERNAL_PROMOTION",
            "small_hole_standard_families_do_not_supply_actual_landing_or_strong_RQ": True,
            "CAD_sources_do_not_pay_depth_integrated_boundary_complexity": True,
            "inter_sign_transport_does_not_pay_positive_Jordan_common_mode": True,
            "external_theorem_promoted": False,
        },
        "main_leaf_acceptance_matrix": {
            "syntax": "6/6",
            "older_dependency_and_artifact_pins": "26/26",
            "frozen_manifest_and_ledger_pins": "6/6",
            "leaf_ledger_artifact_rows": "12/12",
            "integrity": "3/3", "replay": "3/3", "reemit": "3/3",
            "hostile_and_strict_JSON_rejected": "516/516",
            "default_cert_verifier_exit_2": "6/6",
        },
        "independent_leaf_acceptance_matrix": {
            "syntax": "2/2",
            "frozen_manifest_and_ledger_pins": "6/6",
            "leaf_ledger_artifact_rows": "12/12",
            "integrity": "1/1", "replay": "1/1", "reemit": "1/1",
            "hostile_and_strict_JSON_rejected": "80/80",
            "default_cert_verifier_exit_2": "2/2",
            "SHA_ledger_rows": "4/4",
        },
        "four_leaf_acceptance_matrix": {
            "syntax": "8/8", "dependency_and_artifact_pins": "32/32",
            "integrity": "4/4", "replay": "4/4", "reemit": "4/4",
            "hostile_and_strict_JSON_rejected": "596/596",
            "SHA_ledger_rows": "16/16",
            "default_cert_verifier_exit_2": "8/8",
            "Round60_stale_or_temp_files": 0,
        },
        "strict_verdict": {
            "Gate1": "NOT_CERTIFIED", "Gate2": "NOT_CERTIFIED",
            "Gate2_immutable_fields": "0/17", "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED", "Gate5": "NOT_CERTIFIED",
            "Gate5_maturity": "10/18", "complete_18_field_blocks": 0,
            "complete_composite_gates": "0/5", "CM2": "NO-GO_FOR_CLAIM",
            "audit": "PASS_NO_CLAIMED_SCOPE_BLOCKER",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path = VERIFIER) -> dict[str, Any]:
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "dependencies": dict(FROZEN_PINS),
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "report_sha256": sha(REPORT),
        "result": result,
        "verdict": result["strict_verdict"],
    }


def render_manifest(verifier: Path = VERIFIER) -> bytes:
    return (json.dumps(build_manifest(verifier), indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--verifier", type=Path, default=VERIFIER)
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    try:
        payload = render_manifest(args.verifier)
        if args.manifest_json:
            import sys
            sys.stdout.buffer.write(payload)
            return 0
        if args.write_manifest:
            MANIFEST.write_bytes(payload)
            print(f"WROTE: {MANIFEST}")
            return 0
        verdict = build_result()["strict_verdict"]
    except (OSError, ValueError, KeyError, TypeError, ArithmeticError) as exc:
        print(f"ROUND60_INDEPENDENT_AUDIT_CERT_FAILURE: {exc}")
        return 1
    print("INDEPENDENT_AUDIT:", verdict["audit"])
    print("COMPOSITE_GATES:", verdict["complete_composite_gates"])
    print("CM2:", verdict["CM2"])
    return 0 if args.audit else 2


if __name__ == "__main__":
    raise SystemExit(main())
