#!/usr/bin/env python3
"""Independent verifier for the Round-58 three-leaf core-frontier audit."""

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
CERT_PATH = HERE / "cm2_round58_independent_core_frontier_audit_cert.py"
MANIFEST_PATH = HERE / "cm2-round58-independent-core-frontier-audit-manifest-2026-07-20.json"
RESULT_SCHEMA = "cm2.round58-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"

PINNED_FILES = {
    "cm2_gate4_round58_unshifted_landing_minimal_z_first_hit_frontier_cert.py": "873b159a00a0d2154df2c34255cc70c30e50496447d6bb24adba7f920fcd04d8",
    "cm2_gate4_round58_unshifted_landing_minimal_z_first_hit_frontier_verifier.py": "3f3de463190a83c0f718188a2c0e1aa87f7f0697692fc64357b5a79127d43eef",
    "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json": "d335ea6b9bfdc68c13fa0c44f5f2893af7399546f5951d0cfc156be8b5236ffb",
    "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-assault-2026-07-20.md": "0e9ce7397039c86178858bdd5e1ebe6228938e473711ce65075a3c4d45db16c8",
    "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.sha256": "eb11050e4b06c37a2b34ec8fb1b68c4687937d78050c2376c152360996b0bb6d",
    "cm2_gate5_round58_owner_ledger_positive_transport_frontier_cert.py": "9d898bd753ecf61662ded5c75ffdb4387b7a4c582dc138d81b9fcf5cd4fd9a6e",
    "cm2_gate5_round58_owner_ledger_positive_transport_frontier_verifier.py": "8aba976e795013ad856c4383be5f9572fa02e436b15debaa12f03f888b33f3c0",
    "cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.json": "27c5d2e9a6ac9ed8eeb3d42dc96aa1c0a8faa8e50e006811efea22b45c86b859",
    "cm2-gate5-round58-owner-ledger-positive-transport-frontier-assault-2026-07-20.md": "eb971f719c58593114e3d187fd1de1aacac9fe9012b4c4934c6890bef6d68c9a",
    "cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.sha256": "6f0bce6fb81a58a9f4ecf940c0bb8e43f4b525f193341dc4ea497ac4e801391b",
    "cm2_gate123_round58_dini_shadow_cad_landing_join_frontier_cert.py": "ffc6c5ff611119148542db100a11a777175c0bd3f0edf541f3de4847273ae759",
    "cm2_gate123_round58_dini_shadow_cad_landing_join_frontier_verifier.py": "ff7753de555251ca3b936d738730ace0e65a178d7b959fc30678878803155775",
    "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-manifest-2026-07-20.json": "42a035e38687acb4ae1a3ce43a1459c49ba08a1406083c811f919823ecc8d526",
    "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-assault-2026-07-20.md": "e6b87bd43bf4c35ca4804dc1a563a916d27cb0550c45e7b3fb1d670dddfd0934",
    "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-manifest-2026-07-20.sha256": "83cf81e1ffd0630696d417f55fa6b2debd5a1bcb4e158c99bd92d3e976d92e62",
}

C_P = Q(4 * 10**90 * 360493663, 358863)
COMMON_MASS = Q(999, 1000)
N_COMPONENTS = C_P.numerator // C_P.denominator + 1


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate key: {key}")
        out[key] = value
    return out


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON token: {token}")


def strict_json(text: str) -> Any:
    return json.loads(text, object_pairs_hook=strict_object, parse_constant=reject_constant)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def expected_minimal_rows() -> list[dict[str, Any]]:
    source = [
        (Q(3, 5), Q(7, 20), [(Q(1, 5), Q(1, 10)), (Q(2, 5), Q(1, 4))]),
        (Q(5, 8), Q(9, 32), [(Q(1, 8), Q(1, 32)), (Q(1, 4), Q(1, 8)), (Q(1, 4), Q(1, 8))]),
        (Q(7, 10), Q(2, 5), [(Q(1, 10), Q(1, 20)), (Q(3, 10), Q(3, 20)), (Q(3, 10), Q(1, 5))]),
    ]
    result = []
    for index, (length, mass, pieces) in enumerate(source):
        if sum((ell for ell, _ in pieces), Q(0)) != length or sum((weight for _, weight in pieces), Q(0)) != mass:
            raise ValueError("minimal row partition")
        cut_z = sum((weight / ell for ell, weight in pieces), Q(0))
        minimum = mass / length
        if cut_z < minimum:
            raise ValueError("minimal row inequality")
        result.append({"component": index, "length": qstr(length), "mass": qstr(mass), "maximal_component_Z": qstr(minimum), "sample_cut_Z": qstr(cut_z), "cut_not_better": True})
    return result


def expected_gate4() -> dict[str, Any]:
    rows = expected_minimal_rows()
    boundary_d = next(d for d in range(1, 20) if Q(1, 2**d) * C_P < C_P / 2)
    if boundary_d != 2 or not (N_COMPONENTS / COMMON_MASS > C_P > Q(2) / COMMON_MASS):
        raise ValueError("Gate4 rational replay")
    return {
        "fixed_registry_scope": "the exact minimum and iff are valid only after fixing (y, physical landing chart, immutable physical restriction ID)",
        "borel_and_zero_fibre": "least-rational component owners give Borel endpoint/mass/length fields; h=0 has the empty registry, J_land,min=z_land=0 and is never normalized",
        "minimum_replay": "each exact positive carrier lies in one maximal positive component and has no greater length; restricting the inherited positive density to each maximal component attains the lower bound",
        "sample_rows": rows,
        "sample_rows_sha256": digest(rows),
        "properness_iff": "same-time same-ID physical landing is proper iff J_land,min(y)<C_p*h(y) on almost every positive fibre",
        "cross_registry_guard": "cross-y/cross-chart Rokhlin redistribution is not covered and remains a conditional Gate-2 physical interface",
        "global_integrability": "Round57 finite landing Z implies J_land,min,total<infinity; this is not the fibrewise strict threshold",
        "D_land_replay": {"strict_boundary_z_equals_C_p_gives_D_land": boundary_d, "pointwise_defect_bound": "2^D_land<=4*z_land/C_p", "moment": "integral h*2^D_land<=H+(4/C_p)J_land,min,total<infinity"},
        "D_cap_type_guard": "D_cap is stopped reference/common-refinement geometry; D_land is unshifted physical landing geometry",
        "separator": {"N_rule": "floor(C_p)+1", "physical_improper": True, "reference_D_cap": 0, "full_ambient_proper": True, "logical_model_only": True},
        "reinduction": "a once-covering rebased next return has finite Z but is a second return from the original A endpoint and need not be proper",
        "status": "PASS_NO_CLAIMED_SCOPE_BLOCKER__GATE4_REMAINS_NOT_CERTIFIED",
    }


def expected_abel_rows() -> list[dict[str, Any]]:
    masses = [Q(1, 8), Q(1, 4), Q(1, 16), Q(1, 8), Q(1, 16), Q(3, 8)]
    weights = [Q(1001, 1000) ** (k + 1) for k in range(6)]
    lhs = sum((weights[k] * masses[k] for k in range(6)), Q(0))
    rhs = weights[0] * sum(masses, Q(0))
    rows: list[dict[str, Any]] = []
    for j in range(5):
        tail = sum(masses[j + 1 :], Q(0))
        increment = weights[j + 1] - weights[j]
        rhs += increment * tail
        rows.append({"j": j, "tail_F_j": qstr(tail), "weight_increment": qstr(increment)})
    if lhs != rhs:
        raise ValueError("Abel identity")
    rows.append({"finite_lhs": qstr(lhs), "finite_rhs": qstr(rhs), "equal": True})
    return rows


def expected_transport_rows() -> list[dict[str, Any]]:
    pi = [[Q(1, 8), Q(1, 8), Q(0)], [Q(1, 8), Q(0), Q(1, 8)], [Q(0), Q(1, 8), Q(3, 8)]]
    charges = [Q(1), Q(4), Q(9)]
    rows = [sum(row, Q(0)) for row in pi]
    cols = [sum((pi[i][j] for i in range(3)), Q(0)) for j in range(3)]
    lhs = sum((pi[i][j] * (charges[i] + charges[j]) for i in range(3) for j in range(3)), Q(0))
    rhs = sum((rows[i] * charges[i] for i in range(3)), Q(0)) + sum((cols[j] * charges[j] for j in range(3)), Q(0))
    if lhs != rhs:
        raise ValueError("transport identity")
    return [{"row_marginal": [qstr(x) for x in rows], "column_marginal": [qstr(x) for x in cols], "coupled_positive_cost": qstr(lhs), "two_marginal_cost": qstr(rhs), "equal": True}]


def expected_gate5() -> dict[str, Any]:
    abel = expected_abel_rows()
    transport = expected_transport_rows()
    rho_num = 111718729**9148
    rho_den = 111718750**9148
    gamma_num = 2000 * (1 + 48 * 9148) * 900337**9148
    gamma_den = 1999 * 901685**9148
    if not ((rho_num + rho_den) ** 2 < 8 * rho_num**2 and 2 * gamma_num < gamma_den):
        raise ValueError("Gate5 exact clock inequalities")
    return {
        "same_owner_ledger": "K and r_K are Borel on the actual finite owner/root law; the clock moment is a well-typed [0,infinity]-valued integral, not a proved finite one",
        "Abel_identity": "M=a_0*nu(A_col)+sum_j(a_(j+1)-a_j)nu{K>j} by pointwise telescoping and Tonelli",
        "Abel_replay_rows": abel,
        "Abel_replay_rows_sha256": digest(abel),
        "coverage_guard": "A_col full coverage and restricted moment finiteness are independent; neither is certified",
        "density_type": "the physical owner trace is one root atom per parent over an outer law, not an along-collar AC density",
        "artificial_extension_guard": "the uniform artificial collar has density ell^-1 and aggregate exactly raw Z_col, so it cannot be used for free",
        "HJ_policy": "the exact positive policy needs the joint (K,H,J) law; H is compatible 9148-block horizon and J is exact labelled operator/domain equality",
        "HJ_separator": {"same_frozen_K_marginal": True, "aligned_finite": True, "short_raw_debt_infinite": True, "exact_checks": ["gamma<1/2 so beta<1 and r_(2n)<=2n+1", "w_Z^2/2<1"]},
        "positive_transport_identity": "integral(a(y+)+a(y-))dpi is the sum of the two positive marginal moments and is coupling-independent",
        "positive_transport_replay_rows": transport,
        "positive_transport_replay_rows_sha256": digest(transport),
        "zero_OT_separator": "mu_n^+=mu_n^-=2^-n delta_xn has signed OT zero while clearance charge sum 2^(alpha_opt*n^2-n) diverges for alpha_opt>0",
        "strict_scope": {"Gate5_maturity": "10/18", "complete_blocks": 0, "same_law_moment": "NOT_CERTIFIED", "physical_HJ": "NOT_CERTIFIED", "positive_F10": "NOT_CERTIFIED", "strong_cemetery": "NOT_CERTIFIED"},
        "status": "PASS_NO_CLAIMED_SCOPE_BLOCKER__GATE5_REMAINS_NOT_CERTIFIED",
    }


def expected_cad_rows() -> list[dict[str, Any]]:
    result = []
    for depth in (1, 2, 3):
        s, d, product = 2000 * depth + 100, 8, 1
        prefix = []
        for step in range(3):
            factor = 2 * s * d + 1
            product *= factor
            prefix.append({"step": step, "S": str(s), "D": str(d), "stack": str(factor), "product": str(product)})
            s, d = 2 * (s * d + 1) ** 2, 2 * d**2
        result.append({"depth": depth, "variables": 400 * depth + 20, "branch_words": 8 * 162**depth, "first_three_projection_rows": prefix})
    return result


def expected_gate123() -> dict[str, Any]:
    dini = []
    for n in range(9):
        c_n, tail = Q(1) - Q(1, 2**n), Q(1, 2**n)
        if c_n + tail != 1:
            raise ValueError("Dini replay")
        dini.append({"n": n, "C_n": qstr(c_n), "exact_tail": qstr(tail)})
    cad = expected_cad_rows()
    piola = [{"n": n, "determinant": "1", "directional_norm": str(2**n)} for n in range(1, 7)]
    return {
        "gate1": {"Dini_interface": "summable common weighted-projective increments give a uniform Holder Cauchy tail", "Dini_rows": dini, "Dini_rows_sha256": digest(dini), "twisting_radius": "same physical fibre and normalized eigenbasis max-entry error <=10^-29 preserves the four frozen wedges", "physical_rows_and_loop_error": "NOT_CERTIFIED", "status": "NOT_CERTIFIED"},
        "gate2": {"projected_shadow_interface": "Borel projected bad shadows with sum b_j<|I| plus common graph-transform compactness leave a positive all-depth stable base", "first_eight_sum": "255/512", "infinite_sample_sum": "1/2", "area_nullity_guard": "a zero-area transverse line may project to the entire stable-fibre base", "physical_shadow_rows": 0, "cross_y_landing_join": "CONDITIONAL_JOIN_ONLY with seven physical product/holonomy/fragmentation/conditional/boundary/inverse/strong-assembly fields", "status": "NOT_CERTIFIED"},
        "gate3": {"CAD_scope": "CERTIFIED_FOR_DECLARED_ENCODING_BUDGET_ONLY", "physical_formula_budget": "NOT_CERTIFIED", "CAD_rows": cad, "CAD_rows_sha256": digest(cad), "unbounded_depth_guard": "an exponential Dbar moment does not integrate an arbitrary superexponential majorant; no physical lower bound is claimed", "Piola_rows": piola, "Piola_rows_sha256": digest(piola), "strong_RQ_Piola_MT_DQ": "NOT_CERTIFIED", "status": "NOT_CERTIFIED"},
        "status": "PASS_NO_CLAIMED_SCOPE_BLOCKER__GATES123_REMAIN_NOT_CERTIFIED",
    }


def expected_strict() -> dict[str, Any]:
    return {"gate1": "NOT_CERTIFIED", "gate2": "NOT_CERTIFIED", "gate3": "NOT_CERTIFIED", "gate4": "NOT_CERTIFIED", "gate5": "NOT_CERTIFIED", "Gate5_maturity": "10/18", "complete_18_field_operator_block_count": 0, "complete_composite_gates": "0/5", "CM2": "NO-GO_FOR_CLAIM", "audit_verdict": "PASS_NO_CLAIMED_SCOPE_BLOCKER"}


def expected_cross() -> dict[str, Any]:
    return {
        "Gate4_vs_Gate2": "consistent: Gate4 exhausts same-time freedom only within fixed (y,chart,ID), while Gate2 cross-y physical Rokhlin redistribution remains conditional",
        "D_land_vs_D_cap": "consistent and distinct physical versus stopped-reference geometries",
        "Gate5_transport": "consistent: signed cancellation remains available only for signed BL routes and cannot pay positive F10/cemetery charge",
        "Gate3_CAD": "consistent: the recurrence is certified only for a formula separately proved to fit the declared encoding budget",
        "statuses": "all five gates remain NOT_CERTIFIED; complete gates 0/5; CM2 NO-GO_FOR_CLAIM",
        "status": "PASS_NO_CROSS_LEAF_CONTRADICTION",
    }


def load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.is_file() or MANIFEST_PATH.is_symlink():
        raise ValueError("manifest path")
    value = strict_json(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def check_pins() -> None:
    for name, expected in PINNED_FILES.items():
        path = HERE / name
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE or sha256_path(path) != expected:
            raise ValueError(f"pinned artifact: {name}")


def integrity_check(data: dict[str, Any]) -> None:
    if set(data) != {"certificate_sha256", "pinned_files", "result", "schema", "verdict", "verifier_sha256"}:
        raise ValueError("top-level shape")
    if data["schema"] != MANIFEST_SCHEMA or data["pinned_files"] != PINNED_FILES:
        raise ValueError("top-level schema/pins")
    if data["certificate_sha256"] != sha256_path(CERT_PATH):
        raise ValueError("certificate hash")
    if data["verifier_sha256"] != sha256_path(Path(__file__).resolve()):
        raise ValueError("verifier hash")
    result = data["result"]
    if result.get("schema") != RESULT_SCHEMA:
        raise ValueError("result schema")
    replay = copy.deepcopy(result)
    observed = replay.pop("internal_replay_digest", None)
    if observed != digest(replay):
        raise ValueError("internal digest")
    if data["verdict"] != result.get("strict_verdict"):
        raise ValueError("verdict mirror")


def semantic_check(data: dict[str, Any]) -> None:
    result = data["result"]
    if set(result) != {"cross_leaf_consistency", "gate123_independent_audit", "gate4_independent_audit", "gate5_independent_audit", "internal_replay_digest", "provenance", "schema", "strict_verdict"}:
        raise ValueError("result shape")
    expected_provenance = {"pinned_files": PINNED_FILES, "frozen_artifacts": "15/15", "frozen_SHA_ledger_entries": "12/12", "audited_files_modified": False, "external_theorem_promoted": False}
    if result["provenance"] != expected_provenance:
        raise ValueError("provenance")
    if result["gate4_independent_audit"] != expected_gate4():
        raise ValueError("Gate4 replay")
    if result["gate5_independent_audit"] != expected_gate5():
        raise ValueError("Gate5 replay")
    if result["gate123_independent_audit"] != expected_gate123():
        raise ValueError("Gate123 replay")
    if result["cross_leaf_consistency"] != expected_cross():
        raise ValueError("cross-leaf consistency")
    if result["strict_verdict"] != expected_strict():
        raise ValueError("strict verdict")


def collect_leaf_paths(value: Any, prefix: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    if isinstance(value, dict):
        out: list[tuple[Any, ...]] = []
        for key in sorted(value):
            if prefix == () and key == "internal_replay_digest":
                continue
            out.extend(collect_leaf_paths(value[key], prefix + (key,)))
        return out
    if isinstance(value, list):
        out = []
        for index, item in enumerate(value):
            out.extend(collect_leaf_paths(item, prefix + (index,)))
        return out
    return [prefix]


def mutate_leaf(value: Any, index: int) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + index + 1
    if value is None:
        return f"HOSTILE_{index}"
    if isinstance(value, str):
        return value + f"__HOSTILE_{index}"
    raise ValueError("unsupported mutation leaf")


def hostile_self_test(data: dict[str, Any]) -> int:
    strict_json('{"x":1}')
    for hostile in ('{"x":1,"x":2}', '{"x":NaN}'):
        try:
            strict_json(hostile)
        except ValueError:
            pass
        else:
            raise ValueError("strict JSON hostile accepted")
    paths = collect_leaf_paths(data["result"])
    if not paths:
        raise ValueError("no mutation paths")
    rejected = 0
    for index in range(96):
        candidate = copy.deepcopy(data)
        path = paths[index % len(paths)]
        cursor: Any = candidate["result"]
        for token in path[:-1]:
            cursor = cursor[token]
        cursor[path[-1]] = mutate_leaf(cursor[path[-1]], index)
        replay = copy.deepcopy(candidate["result"])
        replay.pop("internal_replay_digest")
        candidate["result"]["internal_replay_digest"] = digest(replay)
        candidate["verdict"] = copy.deepcopy(candidate["result"]["strict_verdict"])
        try:
            integrity_check(candidate)
            semantic_check(candidate)
        except (ValueError, KeyError, TypeError):
            rejected += 1
        else:
            raise ValueError(f"hostile mutation accepted: {index}")
    if rejected != 96:
        raise ValueError("hostile rejection total")
    return rejected


def deterministic_payload() -> str:
    proc = subprocess.run(
        [sys.executable, str(CERT_PATH), "--manifest-json", "--verifier", str(Path(__file__).resolve())],
        cwd=str(HERE),
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0 or proc.stderr:
        raise ValueError(f"certificate regeneration failed: {proc.stderr.strip()}")
    value = strict_json(proc.stdout)
    if not isinstance(value, dict):
        raise ValueError("regenerated manifest root")
    integrity_check(value)
    semantic_check(value)
    return proc.stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--integrity-only", action="store_true")
    group.add_argument("--replay", action="store_true")
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        check_pins()
        data = load_manifest()
        integrity_check(data)
        if args.integrity_only:
            print("ROUND58_INDEPENDENT_AUDIT_INTEGRITY: PASS (15/15 pins)")
            return 0
        semantic_check(data)
        if args.replay:
            print("ROUND58_INDEPENDENT_AUDIT_REPLAY: PASS")
            return 0
        if args.self_test:
            rejected = hostile_self_test(data)
            print(f"ROUND58_INDEPENDENT_AUDIT_HOSTILE: {rejected}/96 REJECTED")
            return 0
        if args.reemit is not None:
            payload = deterministic_payload()
            args.reemit.write_text(payload, encoding="utf-8")
            print(f"REEMIT: {args.reemit}")
            return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ROUND58_INDEPENDENT_AUDIT_VERIFIER_FAILURE: {exc}")
        return 1
    strict = data["verdict"]
    print("AUDIT:", strict["audit_verdict"])
    print("GATES:", strict["complete_composite_gates"])
    print("CM2:", strict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
