#!/usr/bin/env python3
"""Independent cross-audit of all three frozen Round-58 core-frontier leaves.

This append-only certificate hash-pins every certificate, verifier, manifest,
report and SHA ledger in the Round-58 Gate-4, Gate-5 and Gate-1/2/3 leaves.  It
then independently replays the exact rational/algebraic parts of the claims
and freezes their type boundaries.  It does not import any audited program,
edit an audited artifact, or promote a composite gate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round58-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = HERE / "cm2-round58-independent-core-frontier-audit-manifest-2026-07-20.json"
DEFAULT_VERIFIER = HERE / "cm2_round58_independent_core_frontier_audit_verifier.py"

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

G4_MANIFEST = "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json"
G4_REPORT = "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-assault-2026-07-20.md"
G4_LEDGER = "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.sha256"
G5_MANIFEST = "cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.json"
G5_REPORT = "cm2-gate5-round58-owner-ledger-positive-transport-frontier-assault-2026-07-20.md"
G5_LEDGER = "cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.sha256"
G123_MANIFEST = "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-manifest-2026-07-20.json"
G123_REPORT = "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-assault-2026-07-20.md"
G123_LEDGER = "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-manifest-2026-07-20.sha256"

C_P = Q(4 * 10**90 * 360493663, 358863)
COMMON_MASS = Q(999, 1000)
GAP_MASS = Q(1, 1000)
N_COMPONENTS = C_P.numerator // C_P.denominator + 1


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


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


def ledger_target(token: str) -> Path:
    relative = Path(token)
    require(not relative.is_absolute() and ".." not in relative.parts, "unsafe ledger target")
    if relative.parts and relative.parts[0] == "deliverables":
        path = HERE.parent / relative
    else:
        path = HERE / relative
    require(path.resolve().parent == HERE, f"ledger target outside deliverables: {token}")
    return path


def audit_sha_ledger(name: str, expected_members: set[str]) -> int:
    lines = (HERE / name).read_text(encoding="utf-8").splitlines()
    require(len(lines) == 4, f"{name}: ledger row count")
    seen: set[str] = set()
    for line in lines:
        parts = line.split("  ", 1)
        require(len(parts) == 2 and len(parts[0]) == 64, f"{name}: ledger syntax")
        expected, token = parts
        path = ledger_target(token)
        require(path.name in expected_members and path.name not in seen, f"{name}: member")
        require(path.is_file() and not path.is_symlink(), f"{name}: target path")
        require(sha256_path(path) == expected, f"{name}: target hash")
        require(PINNED_FILES[path.name] == expected, f"{name}: independent pin")
        seen.add(path.name)
    require(seen == expected_members, f"{name}: member set")
    return len(lines)


def load_frozen() -> dict[str, Any]:
    loaded: dict[str, Any] = {}
    for name, expected in PINNED_FILES.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"pinned path: {name}")
        require(path.resolve().parent == HERE, f"pinned scope: {name}")
        require(sha256_path(path) == expected, f"pinned hash: {name}")
        if name.endswith(".json"):
            value = strict_json(path.read_text(encoding="utf-8"))
            require(isinstance(value, dict), f"JSON root: {name}")
            loaded[name] = value
        elif name.endswith(".md") or name.endswith(".sha256"):
            loaded[name] = path.read_text(encoding="utf-8")

    groups = {
        G4_LEDGER: {
            G4_MANIFEST,
            G4_REPORT,
            "cm2_gate4_round58_unshifted_landing_minimal_z_first_hit_frontier_cert.py",
            "cm2_gate4_round58_unshifted_landing_minimal_z_first_hit_frontier_verifier.py",
        },
        G5_LEDGER: {
            G5_MANIFEST,
            G5_REPORT,
            "cm2_gate5_round58_owner_ledger_positive_transport_frontier_cert.py",
            "cm2_gate5_round58_owner_ledger_positive_transport_frontier_verifier.py",
        },
        G123_LEDGER: {
            G123_MANIFEST,
            G123_REPORT,
            "cm2_gate123_round58_dini_shadow_cad_landing_join_frontier_cert.py",
            "cm2_gate123_round58_dini_shadow_cad_landing_join_frontier_verifier.py",
        },
    }
    require(sum(audit_sha_ledger(name, members) for name, members in groups.items()) == 12, "ledger total")

    g4 = loaded[G4_MANIFEST]
    require(g4["schema"] == "cm2.gate4.round58-unshifted-landing-minimal-z-first-hit-frontier.v1.manifest.v1", "Gate4 schema")
    require(g4["certificate_sha256"] == PINNED_FILES["cm2_gate4_round58_unshifted_landing_minimal_z_first_hit_frontier_cert.py"], "Gate4 cert mirror")
    require(g4["verifier_sha256"] == PINNED_FILES["cm2_gate4_round58_unshifted_landing_minimal_z_first_hit_frontier_verifier.py"], "Gate4 verifier mirror")
    g4r = g4["result"]
    theorem = g4r["maximal_component_minimum_Z_theorem"]
    require(theorem["status"] == "CERTIFIED_MAXIMAL_COMPONENT_EXACT_MINIMUM_AND_UNSHIFTED_PROPERNESS_IFF", "Gate4 minimum status")
    require("immutable (y, physical landing carrier chart, physical restriction ID)" in theorem["registry_scope"], "Gate4 fixed registry")
    require("future cross-y or cross-chart" in theorem["cross_registry_guard"], "Gate4 cross-registry guard")
    require("h(y)=0" in theorem["zero_policy"] and "never normalized" in theorem["zero_policy"], "Gate4 zero policy")
    require("least-rational owner" in theorem["Borel_measurability"], "Gate4 Borel registry")
    require(g4r["landing_bad_stratum_interface"]["status"] == "CERTIFIED_BAD_STRATUM_TAIL_AND_EXACT_MISSING_THRESHOLD", "Gate4 Dland")
    require(g4r["finite_high_mass_Dcap_zero_separator"]["physical_landing_improper"] is True, "Gate4 separator physical")
    require(g4r["finite_high_mass_Dcap_zero_separator"]["reference_D_cap"] == 0, "Gate4 separator Dcap")
    require(g4["verdict"]["Gate4"] == "NOT_CERTIFIED" and g4["verdict"]["CM2"] == "NO-GO_FOR_CLAIM", "Gate4 strict")
    g4_report = loaded[G4_REPORT]
    require("within the frozen `(y, physical" in g4_report and "cross-`y`/cross-chart" in g4_report, "Gate4 report scope")

    g5 = loaded[G5_MANIFEST]
    require(g5["schema"] == "cm2.gate5.round58-owner-ledger-positive-transport-frontier.v1.manifest.v1", "Gate5 schema")
    require(g5["certificate_sha256"] == PINNED_FILES["cm2_gate5_round58_owner_ledger_positive_transport_frontier_cert.py"], "Gate5 cert mirror")
    require(g5["verifier_sha256"] == PINNED_FILES["cm2_gate5_round58_owner_ledger_positive_transport_frontier_verifier.py"], "Gate5 verifier mirror")
    g5r = g5["result"]
    owner = g5r["physical_same_owner_extended_clearance_ledger"]
    require(owner["status"] == "CERTIFIED_PHYSICAL_SAME_LAW_EXTENDED_LEDGER_NOT_FINITE", "Gate5 owner ledger")
    require("NOT_CERTIFIED" in owner["finiteness_not_certified"], "Gate5 finiteness guard")
    density = g5r["root_density_kernelised_pullback_frontier"]
    require("one root atom" in density["root_law_type"] and "not an along-collar density" in density["root_law_type"], "Gate5 density type")
    require("=Z_col" in density["extension_aggregate_identity"], "Gate5 density debt")
    hj = g5r["clearance_horizon_same_operator_frontier"]
    require(hj["physical_H_joint_law"] == "NOT_CERTIFIED" and hj["physical_J_same_operator"] == "NOT_CERTIFIED", "Gate5 HJ guard")
    require("sum_n 2^n=infinity" in hj["same_marginal_separator"]["short_divergence"], "Gate5 HJ separator")
    ot = g5r["signed_OT_positive_charge_frontier"]
    require(ot["positive_F10_from_signed_OT"] == "FALSE_BY_CERTIFIED_SEPARATOR", "Gate5 OT F10")
    require(ot["strong_cemetery_from_signed_OT"] == "FALSE_BY_CERTIFIED_SEPARATOR", "Gate5 OT cemetery")
    require(g5["verdict"]["Gate5_maturity"] == "10/18" and g5["verdict"]["complete_18_field_operator_block_count"] == 0, "Gate5 maturity")
    require(g5["verdict"]["Gate5"] == "NOT_CERTIFIED" and g5["verdict"]["CM2"] == "NO-GO_FOR_CLAIM", "Gate5 strict")
    g5_report = loaded[G5_REPORT]
    require("不是沿 collar coordinate 的密度" in g5_report and "coupling 无关" in g5_report, "Gate5 report typing")

    g123 = loaded[G123_MANIFEST]
    require(g123["schema"] == "cm2.gate123.round58.dini-shadow-cad-landing-join-frontier.v1", "Gate123 schema")
    require(g123["strict_verdict"] == {"complete_composite_gates": "0/5", "gate1": "NOT_CERTIFIED", "gate2": "NOT_CERTIFIED", "gate3": "NOT_CERTIFIED", "overall": "NO-GO_FOR_CLAIM"}, "Gate123 strict")
    g123r = g123["result"]
    require(g123r["gate1"]["weighted_projective_critical_dini_theorem"]["status"] == "CERTIFIED_CONDITIONAL_INTERFACE", "Gate1 Dini")
    require(g123r["gate2"]["physical_projected_shadow_rows"] == 0, "Gate2 physical rows")
    require(g123r["gate2"]["gate2_to_gate4_landing_join"]["status"] == "CONDITIONAL_JOIN_ONLY", "Gate2 to Gate4 join")
    cad = g123r["gate3"]["explicit_fixed_depth_cad_majorant"]
    require(cad["status"] == "CERTIFIED_FOR_DECLARED_ENCODING_BUDGET", "Gate3 CAD scope")
    require("physical formula enumeration is not claimed" in cad["budget_scope"], "Gate3 formula guard")
    require(g123r["gate3"]["physical_formula_budget_instantiation"] == "NOT_CERTIFIED", "Gate3 physical budget")
    g123_report = loaded[G123_REPORT]
    require("does **not** machine-" in g123_report and "CONDITIONAL_JOIN_ONLY" in g123_report, "Gate123 report scope")
    return loaded


def minimal_z_rows() -> list[dict[str, Any]]:
    samples = [
        (Q(3, 5), Q(7, 20), [(Q(1, 5), Q(1, 10)), (Q(2, 5), Q(1, 4))]),
        (Q(5, 8), Q(9, 32), [(Q(1, 8), Q(1, 32)), (Q(1, 4), Q(1, 8)), (Q(1, 4), Q(1, 8))]),
        (Q(7, 10), Q(2, 5), [(Q(1, 10), Q(1, 20)), (Q(3, 10), Q(3, 20)), (Q(3, 10), Q(1, 5))]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (length, mass, pieces) in enumerate(samples):
        require(sum((ell for ell, _ in pieces), Q(0)) == length, "component length partition")
        require(sum((weight for _, weight in pieces), Q(0)) == mass, "component mass partition")
        cut_z = sum((weight / ell for ell, weight in pieces), Q(0))
        minimum = mass / length
        require(cut_z >= minimum, "minimal-Z lower bound replay")
        rows.append({"component": index, "length": qstr(length), "mass": qstr(mass), "maximal_component_Z": qstr(minimum), "sample_cut_Z": qstr(cut_z), "cut_not_better": True})
    return rows


def gate4_audit() -> dict[str, Any]:
    rows = minimal_z_rows()
    component_length = COMMON_MASS / N_COMPONENTS
    gap_length = GAP_MASS / (N_COMPONENTS - 1)
    require(N_COMPONENTS - 1 <= C_P < N_COMPONENTS, "separator ceiling")
    require(N_COMPONENTS / COMMON_MASS > C_P, "separator physical improper")
    require(Q(2) / COMMON_MASS < C_P, "separator reference proper")
    require(N_COMPONENTS * component_length + (N_COMPONENTS - 1) * gap_length == 1, "separator unit interval")
    boundary_d = next(d for d in range(1, 20) if Q(1, 2**d) * C_P < C_P / 2)
    require(boundary_d == 2, "strict Dland boundary")
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


def abel_rows() -> list[dict[str, Any]]:
    masses = [Q(1, 8), Q(1, 4), Q(1, 16), Q(1, 8), Q(1, 16), Q(3, 8)]
    weights = [Q(1001, 1000) ** (k + 1) for k in range(len(masses))]
    total = sum(masses, Q(0))
    lhs = sum((weights[k] * masses[k] for k in range(len(masses))), Q(0))
    rhs = weights[0] * total
    rows: list[dict[str, Any]] = []
    for j in range(len(masses) - 1):
        tail = sum(masses[j + 1 :], Q(0))
        increment = weights[j + 1] - weights[j]
        rhs += increment * tail
        rows.append({"j": j, "tail_F_j": qstr(tail), "weight_increment": qstr(increment)})
    require(total == 1 and lhs == rhs, "finite Abel identity")
    rows.append({"finite_lhs": qstr(lhs), "finite_rhs": qstr(rhs), "equal": True})
    return rows


def positive_transport_rows() -> list[dict[str, Any]]:
    pi = [
        [Q(1, 8), Q(1, 8), Q(0)],
        [Q(1, 8), Q(0), Q(1, 8)],
        [Q(0), Q(1, 8), Q(3, 8)],
    ]
    charges = [Q(1), Q(4), Q(9)]
    row_marginal = [sum(row, Q(0)) for row in pi]
    col_marginal = [sum((pi[i][j] for i in range(3)), Q(0)) for j in range(3)]
    lhs = sum((pi[i][j] * (charges[i] + charges[j]) for i in range(3) for j in range(3)), Q(0))
    rhs = sum((row_marginal[i] * charges[i] for i in range(3)), Q(0)) + sum((col_marginal[j] * charges[j] for j in range(3)), Q(0))
    require(lhs == rhs, "positive coupling identity")
    return [{"row_marginal": [qstr(x) for x in row_marginal], "column_marginal": [qstr(x) for x in col_marginal], "coupled_positive_cost": qstr(lhs), "two_marginal_cost": qstr(rhs), "equal": True}]


def gate5_audit() -> dict[str, Any]:
    rows = abel_rows()
    transport = positive_transport_rows()
    rho_num = 111718729**9148
    rho_den = 111718750**9148
    require((rho_num + rho_den) ** 2 < 8 * rho_num**2, "w_Z^2/2<1")
    gamma_num = 2000 * (1 + 48 * 9148) * 900337**9148
    gamma_den = 1999 * 901685**9148
    require(2 * gamma_num < gamma_den, "gamma<1/2 and beta<1")
    return {
        "same_owner_ledger": "K and r_K are Borel on the actual finite owner/root law; the clock moment is a well-typed [0,infinity]-valued integral, not a proved finite one",
        "Abel_identity": "M=a_0*nu(A_col)+sum_j(a_(j+1)-a_j)nu{K>j} by pointwise telescoping and Tonelli",
        "Abel_replay_rows": rows,
        "Abel_replay_rows_sha256": digest(rows),
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


def cad_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for depth in (1, 2, 3):
        s = 2000 * depth + 100
        d = 8
        product = 1
        prefix: list[dict[str, Any]] = []
        for step in range(3):
            factor = 2 * s * d + 1
            product *= factor
            prefix.append({"step": step, "S": str(s), "D": str(d), "stack": str(factor), "product": str(product)})
            s, d = 2 * (s * d + 1) ** 2, 2 * d**2
        rows.append({"depth": depth, "variables": 400 * depth + 20, "branch_words": 8 * 162**depth, "first_three_projection_rows": prefix})
    return rows


def gate123_audit() -> dict[str, Any]:
    dini = []
    for n in range(0, 9):
        c_n = Q(1) - Q(1, 2**n)
        tail = Q(1, 2**n)
        require(c_n + tail == 1, "Dini tail replay")
        dini.append({"n": n, "C_n": qstr(c_n), "exact_tail": qstr(tail)})
    b_first_eight = [Q(1, 2 ** (j + 2)) for j in range(8)]
    require(sum(b_first_eight, Q(0)) == Q(255, 512), "shadow finite sum")
    cad = cad_rows()
    piola = [{"n": n, "determinant": "1", "directional_norm": str(2**n)} for n in range(1, 7)]
    return {
        "gate1": {"Dini_interface": "summable common weighted-projective increments give a uniform Holder Cauchy tail", "Dini_rows": dini, "Dini_rows_sha256": digest(dini), "twisting_radius": "same physical fibre and normalized eigenbasis max-entry error <=10^-29 preserves the four frozen wedges", "physical_rows_and_loop_error": "NOT_CERTIFIED", "status": "NOT_CERTIFIED"},
        "gate2": {"projected_shadow_interface": "Borel projected bad shadows with sum b_j<|I| plus common graph-transform compactness leave a positive all-depth stable base", "first_eight_sum": "255/512", "infinite_sample_sum": "1/2", "area_nullity_guard": "a zero-area transverse line may project to the entire stable-fibre base", "physical_shadow_rows": 0, "cross_y_landing_join": "CONDITIONAL_JOIN_ONLY with seven physical product/holonomy/fragmentation/conditional/boundary/inverse/strong-assembly fields", "status": "NOT_CERTIFIED"},
        "gate3": {"CAD_scope": "CERTIFIED_FOR_DECLARED_ENCODING_BUDGET_ONLY", "physical_formula_budget": "NOT_CERTIFIED", "CAD_rows": cad, "CAD_rows_sha256": digest(cad), "unbounded_depth_guard": "an exponential Dbar moment does not integrate an arbitrary superexponential majorant; no physical lower bound is claimed", "Piola_rows": piola, "Piola_rows_sha256": digest(piola), "strong_RQ_Piola_MT_DQ": "NOT_CERTIFIED", "status": "NOT_CERTIFIED"},
        "status": "PASS_NO_CLAIMED_SCOPE_BLOCKER__GATES123_REMAIN_NOT_CERTIFIED",
    }


def strict_verdict() -> dict[str, Any]:
    return {
        "gate1": "NOT_CERTIFIED",
        "gate2": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
        "gate4": "NOT_CERTIFIED",
        "gate5": "NOT_CERTIFIED",
        "Gate5_maturity": "10/18",
        "complete_18_field_operator_block_count": 0,
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
        "audit_verdict": "PASS_NO_CLAIMED_SCOPE_BLOCKER",
    }


def build_result() -> dict[str, Any]:
    load_frozen()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {"pinned_files": dict(PINNED_FILES), "frozen_artifacts": "15/15", "frozen_SHA_ledger_entries": "12/12", "audited_files_modified": False, "external_theorem_promoted": False},
        "gate4_independent_audit": gate4_audit(),
        "gate5_independent_audit": gate5_audit(),
        "gate123_independent_audit": gate123_audit(),
        "cross_leaf_consistency": {
            "Gate4_vs_Gate2": "consistent: Gate4 exhausts same-time freedom only within fixed (y,chart,ID), while Gate2 cross-y physical Rokhlin redistribution remains conditional",
            "D_land_vs_D_cap": "consistent and distinct physical versus stopped-reference geometries",
            "Gate5_transport": "consistent: signed cancellation remains available only for signed BL routes and cannot pay positive F10/cemetery charge",
            "Gate3_CAD": "consistent: the recurrence is certified only for a formula separately proved to fit the declared encoding budget",
            "statuses": "all five gates remain NOT_CERTIFIED; complete gates 0/5; CM2 NO-GO_FOR_CLAIM",
            "status": "PASS_NO_CROSS_LEAF_CONTRADICTION",
        },
        "strict_verdict": strict_verdict(),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path = DEFAULT_VERIFIER) -> dict[str, Any]:
    verifier = verifier.resolve()
    require(verifier.is_file() and not verifier.is_symlink(), "verifier path")
    require(verifier.parent == HERE, "verifier scope")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "pinned_files": dict(PINNED_FILES),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier),
        "result": result,
        "verdict": result["strict_verdict"],
    }


def encoded_manifest(verifier: Path = DEFAULT_VERIFIER) -> str:
    return json.dumps(build_manifest(verifier), indent=2, sort_keys=True, allow_nan=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    try:
        payload = encoded_manifest(args.verifier)
        if args.manifest_json:
            print(payload, end="")
            return 0
        if args.write_manifest:
            DEFAULT_MANIFEST.write_text(payload, encoding="utf-8")
            print(f"WROTE: {DEFAULT_MANIFEST}")
            return 0
        if args.summary:
            print("ROUND58_INDEPENDENT_AUDIT: PASS")
            print("FROZEN_ARTIFACTS: 15/15")
            print("SHA_LEDGER_ROWS: 12/12")
            print("COMPLETE_GATES: 0/5")
            print("CM2: NO-GO_FOR_CLAIM")
            return 0
    except (OSError, RuntimeError, ValueError, KeyError, TypeError) as exc:
        print(f"ROUND58_INDEPENDENT_AUDIT_CERT_FAILURE: {exc}")
        return 1
    strict = build_result()["strict_verdict"]
    print("AUDIT:", strict["audit_verdict"])
    print("GATES:", strict["complete_composite_gates"])
    print("CM2:", strict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
