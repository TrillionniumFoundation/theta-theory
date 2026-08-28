#!/usr/bin/env python3
"""Round-63 Gate-2/4 stable-saturation / holonomy-square frontier.

This append-only certificate proves exact interface and nonimplication facts.
It does not certify a physical stable quotient, landing properness, Gate 2,
Gate 4, or CM2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate24.round63-stable-saturation-holonomy-square-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate24-round63-stable-saturation-holonomy-square-frontier"
DEFAULT_MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
DEFAULT_REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
DEFAULT_VERIFIER = HERE / "cm2_gate24_round63_stable_saturation_holonomy_square_frontier_verifier.py"

DEPENDENCIES = {
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json":
        "e0b89d604e89852b574638428a60daa1f6e8231b85177230a5dd67615205bad1",
    "cm2-round62-independent-core-frontier-audit-manifest-2026-07-21.json":
        "19a02d00e2ac85849f6197054166e193e1d4e3433c21505fd4bfd2b450faea20",
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.json":
        "2edf4d7801525c746c619cb85b39c59d30018df7c6971f5e48639dc390573b9b",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json":
        "08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3",
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json":
        "e7305e0b72eed28bc68b115e1201fc02e2b66d3cc95906fc6d1efc5e9463a4f5",
}

BASELINE = {
    "cm2-sixty-second-direct-assault-2026-07-21.md":
        "873557a6653a826700d5daf11e8b118f5ddca1cf911e085f9c20aa591ab2136f",
    "cm2-sixty-second-direct-assault-manifest-2026-07-21.sha256":
        "e54b5a1de2b4bddf0c7589b77997b1f28284040b64b31fdfbf58af9e73233bac",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-assault-2026-07-21.md":
        "4acca86b074ce3f6792aa04625c9576d2affeacb0ad9d7cdeb09cabd08d45b00",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.sha256":
        "b94df87ba8362827bb1115f474c0beec59f887325e8db58b55a9020bf99ae6bc",
    "cm2_gate42_round62_branch_covariance_graph_cylinder_current_frontier_cert.py":
        "12ef3cbaa17d727eeadb63fc6e1eb5a6256a38a7ebc35c8c159e5f951bdd4939",
    "cm2_gate42_round62_branch_covariance_graph_cylinder_current_frontier_verifier.py":
        "432c2b827e61a1d5db3bb5e5d2e8266c66abc25ccb3d341cc4d76257ed17ed0b",
    "cm2-round62-independent-core-frontier-audit-2026-07-21.md":
        "123f8ffc563e7d2b364f7caf565ac1a953ecc45123d1c483bc0f97b24c3cfeb4",
    "cm2-round62-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "32504c8eda5125d11a460199c3471158720127bf2bc1081664a8a20747c7a414",
    "cm2_round62_independent_core_frontier_audit_cert.py":
        "2d09eec99d4a32561f266702ad4e3e05bcf39b81f3b6c5a8d92e56d15b547c91",
    "cm2_round62_independent_core_frontier_audit_verifier.py":
        "893939d281c4bd3f6759b89e52a73c5057ff1fe64bc1117bad8875f38de1d804",
}

CP = Q(4 * 10**90 * 360493663, 358863)

STRICT = {
    "actual_tagged_first_return_branch_RN_covariance": "CERTIFIED_PINNED_ROUND62",
    "branch_holonomy_square_defect_identity": "CERTIFIED_EXACT",
    "exact_square_preserves_source_landing_defect_norm": "CERTIFIED_EXACT",
    "two_plaque_L1_stable_saturation_distance": "CERTIFIED_EXACT",
    "physical_invariant_product_rectangles": "NOT_CERTIFIED",
    "physical_stable_projection_and_two_sided_J_hol": "NOT_CERTIFIED",
    "actual_marker_zero_defect": "NOT_CERTIFIED",
    "holonomy_transport_m_squared_budget": "CERTIFIED_CONDITIONAL",
    "actual_FRthetaLmM_budget": "NOT_CERTIFIED",
    "fibrewise_FR_below_Cp_theta_L": "NOT_CERTIFIED",
    "tagged_graph_cylinder_normal_current": "CERTIFIED_PINNED_ROUND62",
    "physical_anisotropic_current_Piola_assembly": "NOT_CERTIFIED",
    "seven_field_landing_join": "1/7_COMPLETE__FIELDS_1_4_7_PARTIAL",
    "official_immutable_Gate2_fields": "0/17",
    "proper_physical_same_ID_first_return_kernel": "NOT_CERTIFIED",
    "original_Rn_intermediate_C24_avoidance": "CERTIFIED_PINNED_ROUND57",
    "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
    "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
    "strong_singular_current_cemetery": "NOT_CERTIFIED",
    "Gate2": "NOT_CERTIFIED",
    "Gate4": "NOT_CERTIFIED",
    "complete_composite_gates": "0/5",
    "CM2": "NO-GO_FOR_CLAIM",
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise ValueError(label)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def qlist(values: list[Q]) -> list[str]:
    return [qstr(x) for x in values]


def l1_uniform(values: list[Q]) -> Q:
    return sum((abs(x) for x in values), Q(0)) / len(values)


def dynamic_transfer(values: list[Q], image: list[int]) -> list[Q]:
    require(sorted(image) == list(range(len(values))), "dynamic permutation")
    inverse = [image.index(j) for j in range(len(image))]
    return [values[inverse[j]] for j in range(len(image))]


def square_replay() -> dict[str, Any]:
    mu = [Q(1, 3)] * 3
    image = [1, 2, 0]
    a_u = [Q(1), Q(0), Q(1, 2)]
    a_v = [Q(3, 4), Q(1, 4), Q(1, 2)]
    g_u = dynamic_transfer(a_u, image)
    g_v = dynamic_transfer(a_v, image)
    delta_s = [v - u for u, v in zip(a_u, a_v)]
    delta_l = [v - u for u, v in zip(g_u, g_v)]
    require(delta_l == dynamic_transfer(delta_s, image), "square transport")
    require(l1_uniform(delta_s) == l1_uniform(delta_l) == Q(1, 6), "square norm")
    replay = {
        "reference_law_each_plaque": qlist(mu),
        "dynamic_branch_image": image,
        "source_marker_a_u": qlist(a_u),
        "source_marker_a_v": qlist(a_v),
        "landing_marker_g_u": qlist(g_u),
        "landing_marker_g_v": qlist(g_v),
        "source_defect_Delta_S": qlist(delta_s),
        "landing_defect_Delta_L": qlist(delta_l),
        "L1_Delta_S": qstr(l1_uniform(delta_s)),
        "L1_Delta_L": qstr(l1_uniform(delta_l)),
        "square_commutator_norm": "0",
    }
    return {
        "source_direction": "P_S:L1(mu_u^S)->L1(mu_v^S); Delta_S=a_v-P_S*a_u",
        "landing_direction": "P_L:L1(mu_u^L)->L1(mu_v^L); Delta_L=g_v-P_L*g_u",
        "dynamic_direction": "D_i:L1(mu_i^S)->L1(mu_i^L), D_i f=f o H_i^-1",
        "commutator": "C_uv=D_v*P_S-P_L*D_u",
        "identity": "Delta_L=D_v*Delta_S+C_uv(a_u)",
        "bound": "||Delta_L||_1<=||Delta_S||_1+||C_uv(a_u)||_1",
        "exact_square": "if H_v o s=ell o H_u with the declared reference transports, then C_uv=0 and ||Delta_L||_1=||Delta_S||_1",
        "interpretation": "an exact branch-holonomy square transports stable-saturation debt; it does not annihilate it",
        "physical_guard": "the physical source/landing stable holonomies and the actual zero marker defect are not constructed",
        "finite_replay": replay,
        "finite_replay_sha256": digest(replay),
        "status": "CERTIFIED_EXACT_BRANCH_HOLONOMY_SQUARE_DEFECT_IDENTITY__PHYSICAL_HOLONOMY_AND_ZERO_DEFECT_ABSENT",
    }


def saturation_distance(square: dict[str, Any]) -> dict[str, Any]:
    replay0 = square["finite_replay"]
    g_u = [Q(x) for x in replay0["landing_marker_g_u"]]
    g_v = [Q(x) for x in replay0["landing_marker_g_v"]]
    defect = l1_uniform([v - u for u, v in zip(g_u, g_v)])
    distance = defect / 2
    require(defect == Q(1, 6) and distance == Q(1, 12), "saturation replay")
    replay = {
        "outer_weight_u": "1/2",
        "outer_weight_v": "1/2",
        "stable_transfer": "identity in the finite replay",
        "L1_marker_defect": qstr(defect),
        "delta_sat": qstr(distance),
        "attaining_quotient_marker": qlist(g_u),
    }
    return {
        "definition": "delta_sat=1/2 inf_f (||g_u-f||_L1(mu_u)+||g_v-Pf||_L1(mu_v))",
        "exact_formula": "delta_sat=1/2||g_v-Pg_u||_L1(mu_v) for two plaques of outer weight 1/2 and a positive L1 isometry P",
        "zero_criterion": "delta_sat=0 iff the two marker laws descend to one stable quotient marker",
        "L1_guard": "conditional expectation is not asserted to be the L1 best approximant; the proof is triangle inequality plus f=g_u",
        "actual_guard": "without a physical stable quotient/P, delta_sat for the actual common landing law is not yet instantiated",
        "finite_replay": replay,
        "finite_replay_sha256": digest(replay),
        "status": "CERTIFIED_EXACT_TWO_PLAQUE_L1_STABLE_SATURATION_DISTANCE__ACTUAL_PHYSICAL_DISTANCE_UNINSTANTIATED",
    }


def holonomy_transport() -> dict[str, Any]:
    F = Q(3)
    R = Q(4)
    theta = Q(1, 2)
    length = Q(2)
    m = Q(1, 2)
    M = Q(3, 2)
    bound = F * R * M / (m * m * theta * length)
    require(bound == Q(72), "transport replay")
    require(bound < CP, "transport magnitude")
    replay = {
        "F_u": qstr(F),
        "R_u": qstr(R),
        "theta_u": qstr(theta),
        "L_u": qstr(length),
        "metric_derivative_lower_m": qstr(m),
        "metric_derivative_upper_M": qstr(M),
        "target_z_upper": qstr(bound),
        "target_z_upper_below_C_p": True,
    }
    return {
        "hypotheses": "E_v=h(E_u), f_v(hx)=c*f_u(x)/lambda(x), c>0, and 0<m<=lambda=dh/ds<=M in one adapted arclength",
        "component_transport": "F_v=F_u",
        "span_transport": "|E_v|>=m*theta_u*L_u",
        "density_ratio_transport": "R_v<=R_u*M/m",
        "target_bound": "z_v<=F_u*R_u*M/(m^2*theta_u*L_u)",
        "strict_sufficient_budget": "F_u*R_u*M<C_p*m^2*theta_u*L_u",
        "m_squared_audit": "one factor m pays retained-span contraction and one factor m pays the 1/lambda density-ratio conversion",
        "type_guard": "two-sided measure J_hol alone does not determine adapted-arclength m,M; bi-Lipschitz geometry alone does not establish marker-law transport",
        "physical_guard": "F,R,theta,L,m,M are not materialized on the actual common landing law",
        "finite_replay": replay,
        "finite_replay_sha256": digest(replay),
        "status": "CERTIFIED_CONDITIONAL_EXACT_HOLONOMY_TRANSPORT_BUDGET_WITH_M_SQUARED_COST__ACTUAL_INPUTS_ABSENT",
    }


def zero_defect_separators() -> dict[str, Any]:
    short_L = Q(1, 1) / (2 * CP)
    short_z = Q(1, 1) / short_L
    N = CP.numerator // CP.denominator + 1
    frag_h = Q(1, 2)
    frag_J = Q(N)
    frag_z = frag_J / frag_h
    require(short_z == 2 * CP and short_z > CP, "short separator")
    require(frag_z == 2 * N and frag_z > CP, "fragment separator")
    replay = {
        "C_p": qstr(CP),
        "short_span": {
            "F": 1,
            "R": 1,
            "theta": 1,
            "L": qstr(short_L),
            "z": qstr(short_z),
            "z_over_C_p": "2",
        },
        "fragmentation": {
            "N_rule": "floor(C_p)+1",
            "F": str(N),
            "R": 1,
            "theta": "1/2",
            "L": 1,
            "J": str(N),
            "h": "1/2",
            "z": str(2 * N),
            "z_above_C_p": True,
        },
    }
    return {
        "common_hypotheses": "identity stable holonomy, the same marker on every plaque, exact commuting dynamic square, zero square commutator and delta_sat=0",
        "short_span_conclusion": "F=R=theta=1 with L=1/(2C_p) gives z=2C_p>C_p",
        "fragmentation_conclusion": "N=floor(C_p)+1 equal components of total length 1/2 give z=2N>C_p",
        "scope": "exact logical smooth/product nonimplication models; not asserted to be billiard realizations",
        "conclusion": "product geometry plus exact marker descent does not imply the quantitative properness inequality",
        "finite_replay": replay,
        "finite_replay_sha256": digest(replay),
        "status": "CERTIFIED_ZERO_DEFECT_SHORT_SPAN_AND_FRAGMENTATION_SEPARATORS__FR_THRESHOLD_REMAINS_INDEPENDENT",
    }


def seven_fields() -> dict[str, Any]:
    rows = [
        {"field": 1, "name": "physical invariant product rectangles", "state": "PARTIAL_TAGGED_FINITE_DEPTH_CONE_CURVE_ATLAS_ONLY"},
        {"field": 2, "name": "stable projection and two-sided J_hol", "state": "NOT_CERTIFIED__EXACT_SQUARE_AND_DEFECT_CALCULUS_ONLY"},
        {"field": 3, "name": "full span or marker fragmentation", "state": "NOT_CERTIFIED__EXACT_CONDITIONAL_TRANSPORT_BUDGET_ONLY"},
        {"field": 4, "name": "same-law conditionals and density bounds", "state": "PARTIAL_ACTUAL_DYNAMIC_BRANCH_RN_PLUS_EXACT_SATURATION_DISTANCE__NO_PHYSICAL_STABLE_QUOTIENT"},
        {"field": 5, "name": "physical boundary charge below C_p", "state": "NOT_CERTIFIED__NO_ACTUAL_INPUTS_FOR_STRICT_BUDGET"},
        {"field": 6, "name": "tagged Borel branch inverse", "state": "CERTIFIED_PINNED_ROUND59"},
        {"field": 7, "name": "strong restriction and assembly", "state": "PARTIAL_GRAPH_CYLINDER_ONLY__NO_PHYSICAL_STRONG_OPERATOR"},
    ]
    return {
        "rows": rows,
        "rows_sha256": digest(rows),
        "complete_rows": "1/7",
        "partial_rows": [1, 4, 7],
        "official_immutable_Gate2_fields": "0/17",
        "three_independent_debts": [
            "physical carrier/holonomy-square and its commutator",
            "stable-saturation marker defect",
            "quantitative F,R,theta,L and adapted-arclength holonomy distortion",
        ],
        "status": "CERTIFIED_ROUND63_SEVEN_FIELD_AUDIT__ONE_COMPLETE_THREE_PARTIAL__NO_GATE_PROMOTION",
    }


def build_result() -> dict[str, Any]:
    square = square_replay()
    result = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "claim_type": "exact branch-holonomy-square defect, exact two-plaque L1 stable-saturation distance, and conditional quantitative holonomy transport frontier",
            "dependency_sha256": DEPENDENCIES,
            "baseline_file_sha256": BASELINE,
            "parameter_scope": "parameterwise for every fixed |s|<=1/400; no uniform physical stable quotient is asserted",
            "old_artifacts_modified": False,
            "external_theorem_promoted": False,
        },
        "branch_holonomy_square": square,
        "two_plaque_stable_saturation": saturation_distance(square),
        "quantitative_holonomy_transport": holonomy_transport(),
        "zero_defect_quantitative_separators": zero_defect_separators(),
        "graph_cylinder_and_strong_assembly_guard": {
            "pinned_current": "the Round62 endpoint-traced normal current on the tagged graph cylinder remains exact",
            "weighted_trace_guard": "the weighted trace is 2^D*nu and multiplication by 2^-D is required to recover the original charge",
            "missing_map": "no bounded endpoint-preserving transfer-intertwining Piola-compatible E_phys:X_D^graph->B_strong is constructed",
            "cemetery_guard": "positive bad collision-SRB mass is not collision-null cemetery",
            "status": "CERTIFIED_TYPE_GUARD__GRAPH_CYLINDER_DOES_NOT_COMPLETE_PHYSICAL_FIELD7",
        },
        "seven_field_materialization_audit": seven_fields(),
        "latest_official_technology_audit": {
            "checked_through": "2026-07-21 official-source surface",
            "Canestrari_2604_19671v2": "evolves an already regular standard family with survival normalization; does not construct this common landing quotient or strict budget",
            "AxiomA_SRB_2604_18929": "wrong smooth-hyperbolic type for the singular moving billiard and does not install the pinned landing carrier",
            "new_direct_closure_found": False,
            "external_theorem_promoted": False,
            "status": "AUDITED_NO_OFFICIAL_THEOREM_CLOSES_THE_TYPED_PRODUCT_MARKER_QUANTITATIVE_STRONG_JOIN",
        },
        "strict_nonpromotion": STRICT,
    }
    result["internal_replay_digest"] = digest(result)
    return result


def verify_pins() -> None:
    for mapping in (DEPENDENCIES, BASELINE):
        for name, expected in mapping.items():
            path = HERE / name
            require(path.is_file() and not path.is_symlink(), f"missing or symlink pin: {name}")
            require(path.resolve().parent == HERE, f"pin parent: {name}")
            require(sha256_path(path) == expected, f"pin hash: {name}")


def build_manifest(verifier: Path) -> dict[str, Any]:
    verify_pins()
    verifier = verifier.resolve()
    require(verifier.is_file() and verifier.parent == HERE and not verifier.is_symlink(), "verifier path")
    require(DEFAULT_REPORT.is_file() and DEFAULT_REPORT.resolve().parent == HERE and not DEFAULT_REPORT.is_symlink(), "report path")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "dependencies": DEPENDENCIES,
        "baseline_files": BASELINE,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier),
        "report_sha256": sha256_path(DEFAULT_REPORT),
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }


def render_manifest(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    args = parser.parse_args()
    try:
        data = build_manifest(args.verifier)
        payload = render_manifest(data)
        if args.write_manifest is not None:
            target = args.write_manifest.resolve()
            require(target.parent == HERE, "manifest output parent")
            target.write_text(payload, encoding="utf-8")
            print(f"WROTE_MANIFEST: {target}")
            return 0
        if args.manifest_json:
            print(payload, end="")
            return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(f"ROUND63_GATE24_SATURATION_SQUARE_CERT_FAILURE: {exc}")
        return 1

    frontier = data["result"]["strict_nonpromotion"]
    print("SQUARE_DEFECT:", frontier["branch_holonomy_square_defect_identity"])
    print("STABLE_SATURATION_DISTANCE:", frontier["two_plaque_L1_stable_saturation_distance"])
    print("PHYSICAL_HOLONOMY:", frontier["physical_stable_projection_and_two_sided_J_hol"])
    print("GATE2:", frontier["Gate2"])
    print("GATE4:", frontier["Gate4"])
    print("CM2:", frontier["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
