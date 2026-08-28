#!/usr/bin/env python3
"""Round-62 Gate-4/2 branch-covariance / graph-cylinder frontier.

This append-only certificate proves two exact interfaces without promoting
Gate 2, Gate 4, or CM2:

* RN markers are exactly covariant on each already certified invertible
  tagged physical first-return branch;
* every finite Round-61 weighted graph-TV defect has a canonical normal
  metric 1-current on a tagged graph cylinder with exact endpoint traces.

The cylinder is a bookkeeping current, not a physical phase-space
anisotropic current, Piola carrier, or accepted cemetery.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate42.round62-branch-covariance-graph-cylinder-current-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier"
DEFAULT_MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
DEFAULT_REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
DEFAULT_VERIFIER = HERE / "cm2_gate42_round62_branch_covariance_graph_cylinder_current_frontier_verifier.py"

DEPENDENCIES = {
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.json":
        "2edf4d7801525c746c619cb85b39c59d30018df7c6971f5e48639dc390573b9b",
    "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.json":
        "bb0d263454a33acdf8b2ba443fcc5e247ff1b9214c385f70fa1af2fc26e7c019",
}

BASELINE = {
    "cm2-sixty-first-direct-assault-2026-07-20.md":
        "b9ad28ed23e88768234b304dd9f9ecb02577c7aa18dc8a982185690ea8f6f02b",
    "cm2-sixty-first-direct-assault-manifest-2026-07-20.sha256":
        "2a3ae3ebf1a6e11b734611e260a340398f475d70e4888010c8294ac321d84265",
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-assault-2026-07-20.md":
        "e99800b998a2fc547229a6b2a93dd84433634af76c691ef65c37b9024fc0d45c",
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.sha256":
        "a7499c939a1b167a21b62f8f0485ceaac5b44a9c21d2c59e3e22ee45805c56e2",
    "cm2_gate4_round61_marker_weighted_curve_defect_ledger_frontier_cert.py":
        "0edb32c9572cbf3dc7ba4ef500a0ec011c379c19f42cc581c0e095176dc20f82",
    "cm2_gate4_round61_marker_weighted_curve_defect_ledger_frontier_verifier.py":
        "0dfa89b59db7567b871219878011a77db177f857af9daab92665a927a486a23a",
    "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-assault-2026-07-20.md":
        "94d943e25c3f43a909f0ec691fe86f43848f41228da5378fa16a94405654dea6",
    "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.sha256":
        "744bf350c4b3511bb35cefb12d294d4ef407d9c09b43dacb1123eba6103a1f0b",
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


def push_vector(values: list[Q], image: list[int]) -> list[Q]:
    require(len(values) == len(image), "push size")
    out = [Q(0) for _ in values]
    require(sorted(image) == list(range(len(values))), "push permutation")
    for index, target in enumerate(image):
        out[target] += values[index]
    return out


def componentwise_product(left: list[Q], right: list[Q]) -> list[Q]:
    require(len(left) == len(right), "product size")
    return [a * b for a, b in zip(left, right)]


def qlist(values: list[Q]) -> list[str]:
    return [qstr(value) for value in values]


def branch_covariance() -> dict[str, Any]:
    mu_u = [Q(1, 2), Q(1, 3), Q(1, 6)]
    marker_a = [Q(1), Q(1, 2), Q(0)]
    image = [1, 2, 0]
    kappa_u = componentwise_product(mu_u, marker_a)
    mu_v = push_vector(mu_u, image)
    kappa_v = push_vector(kappa_u, image)
    marker_b = [k / m if m else Q(0) for k, m in zip(kappa_v, mu_v)]
    inverse = [image.index(target) for target in range(len(image))]
    transported = [marker_a[inverse[target]] for target in range(len(image))]
    require(marker_b == transported, "branch marker covariance")
    require(sum(mu_u) == sum(mu_v) == Q(1), "branch reference mass")
    require(sum(kappa_u) == sum(kappa_v) == Q(2, 3), "branch common mass")
    replay = {
        "mu_U": qlist(mu_u),
        "source_marker_a": qlist(marker_a),
        "H_image": image,
        "mu_V": qlist(mu_v),
        "kappa_V": qlist(kappa_v),
        "landing_marker_g_B": qlist(marker_b),
        "a_after_H_inverse": qlist(transported),
        "common_mass": qstr(sum(kappa_v)),
    }
    return {
        "actual_scope": "each frozen invertible n/path/physical-ID/half-open-owner tagged branch of the exact raw physical first-return graph",
        "reference_transport": "mu_V=H_#mu_U and kappa_V=H_#kappa_U on the same branch",
        "RN_identity": "g_B=a o H^-1 mu_V-a.e.; equivalently a=g_B o H mu_U-a.e.",
        "jacobian_guard": "the branch coordinate Jacobian occurs in both marked and unmarked densities and cancels in their RN ratio; no extra J_ell H belongs in the marker identity",
        "tag_guard": "the identity is branchwise before n/path/physical-ID/half-open-owner/once tags are forgotten",
        "stable_holonomy_guard": "this is dynamic first-return covariance, not covariance between distinct unstable plaques under stable holonomy",
        "finite_replay": replay,
        "finite_replay_sha256": digest(replay),
        "status": "CERTIFIED_EXACT_ACTUAL_TAGGED_FIRST_RETURN_BRANCH_RN_COVARIANCE__NOT_STABLE_HOLONOMY_COVARIANCE",
    }


def holonomy_defect() -> dict[str, Any]:
    mu = [Q(1, 3)] * 3
    g_u = [Q(1), Q(0), Q(1, 2)]
    g_v = [Q(3, 4), Q(1, 4), Q(1, 2)]
    g_w = [Q(1, 2), Q(1, 2), Q(1, 2)]
    d_uv = [v - u for u, v in zip(g_u, g_v)]
    d_vw = [w - v for v, w in zip(g_v, g_w)]
    d_uw = [w - u for u, w in zip(g_u, g_w)]
    require(d_uw == [a + b for a, b in zip(d_uv, d_vw)], "defect cocycle")

    def l1(values: list[Q]) -> Q:
        return sum((m * abs(v) for m, v in zip(mu, values)), Q(0))

    require(l1(d_uv) == Q(1, 6), "uv norm")
    require(l1(d_vw) == Q(1, 6), "vw norm")
    require(l1(d_uw) == Q(1, 3), "uw norm")
    replay = {
        "reference_law_each_fibre": qlist(mu),
        "g_u": qlist(g_u),
        "g_v": qlist(g_v),
        "g_w": qlist(g_w),
        "Delta_uv": qlist(d_uv),
        "Delta_vw": qlist(d_vw),
        "Delta_uw": qlist(d_uw),
        "L1_Delta_uv": qstr(l1(d_uv)),
        "L1_Delta_vw": qstr(l1(d_vw)),
        "L1_Delta_uw": qstr(l1(d_uw)),
    }
    return {
        "transfer": "P_uv f=(f o h_uv^-1)J_uv when (h_uv)_#mu_u=J_uv mu_v",
        "isometry": "for a bijective nonsingular holonomy, P_uv is positive and ||P_uv f||_L1(mu_v)=||f||_L1(mu_u)",
        "defect": "Delta_uv=g_v-P_uv g_u; Delta_uv=0 a.e. iff the holonomy transports the same marked common law",
        "composition": "if h_uw=h_vw o h_uv, then P_uw=P_vw P_uv and Delta_uw=Delta_vw+P_vw Delta_uv",
        "triangle": "||Delta_uw||_1<=||Delta_vw||_1+||Delta_uv||_1",
        "registry_value": "zero defects on a spanning holonomy tree would propagate the marker from one base plaque",
        "physical_guard": "no actual all-depth stable product quotient, h_uv, J_uv, or zero physical defect is produced",
        "finite_replay": replay,
        "finite_replay_sha256": digest(replay),
        "status": "CERTIFIED_EXACT_POSITIVE_L1_ISOMETRY_AND_MARKER_DEFECT_COCYCLE_INTERFACE__PHYSICAL_HOLONOMY_ABSENT",
    }


def graph_cylinder_current() -> dict[str, Any]:
    atoms = [
        {"mass": "3/20", "D_land": 2},
        {"mass": "1/80", "D_land": 5},
        {"mass": "1/320", "D_land": 7},
    ]
    total = Q(0)
    weighted = Q(0)
    rows: list[dict[str, Any]] = []
    for atom in atoms:
        mass = Q(atom["mass"])
        depth = int(atom["D_land"])
        weight = Q(2**depth)
        weighted_mass = weight * mass
        total += mass
        weighted += weighted_mass
        rows.append(
            {
                "mass": qstr(mass),
                "D_land": depth,
                "weight": qstr(weight),
                "weighted_mass": qstr(weighted_mass),
                "recovered_mass": qstr(weighted_mass / weight),
            }
        )
    require(total == Q(53, 320), "current total")
    require(weighted == Q(7, 5), "current weighted")
    replay = {
        "atoms": rows,
        "ordinary_current_mass": qstr(total),
        "ordinary_boundary_mass": qstr(2 * total),
        "weighted_current_mass": qstr(weighted),
        "weighted_boundary_mass": qstr(2 * weighted),
        "ordinary_normal_norm_mass_plus_boundary": qstr(3 * total),
        "weighted_normal_norm_mass_plus_boundary": qstr(3 * weighted),
    }
    interfaces = [
        {"index": 1, "row": "positive endpoint-preserving embedding", "cylinder_current": "CERTIFIED"},
        {"index": 2, "row": "retain endpoints and n/path/ID/owner/once", "cylinder_current": "CERTIFIED"},
        {"index": 3, "row": "norm paid by D_land", "cylinder_current": "CERTIFIED"},
        {"index": 4, "row": "exact full=good+bad trace recovery", "cylinder_current": "CERTIFIED"},
        {"index": 5, "row": "downstream physical strong/cemetery acceptance", "cylinder_current": "NOT_CERTIFIED"},
    ]
    return {
        "record_space": "Z is the standard-Borel bad first-return graph record space including physical source/landing and n/path/ID/owner/once/D_land",
        "metric_typing": "a refined bounded complete compatible metric can make the finite endpoint/tag coordinate maps Lipschitz without changing the Borel sets; this is a bookkeeping topology",
        "current_definition": "T_nu(f,pi)=integral_Z integral_0^1 f(t,z)*partial_t pi(t,z) dt dnu(z) on [0,1]xZ",
        "ordinary_exact_identities": "M(T_nu)=|nu|(Z), partial T_nu=(i_1)_#nu-(i_0)_#nu, M(partial T_nu)=2|nu|(Z)",
        "physical_trace": "after the two disjoint labelled traces, the Lipschitz record projections give exactly landing_#nu and source_#nu",
        "weighted_exact_identities": "for w=2^D_land, M(T_(w nu))=||nu||_X and M(partial T_(w nu))=2||nu||_X",
        "weighted_charge_guard": "the weighted current traces are w*nu, not nu; the unweighted physical trace is recovered only by multiplying the boundary 0-currents by w^-1=2^-D_land",
        "ordinary_control": "M(T_nu)+M(partial T_nu)=3|nu|(Z)<=3||nu||_X",
        "hybrid_identity": "Gamma_cap=Gamma_G+trace_1(partial T_Gamma_B), with exact original graph records and no normalization/deletion/duplicate charge",
        "replay": replay,
        "replay_sha256": digest(replay),
        "five_interface_rows": interfaces,
        "five_interface_rows_sha256": digest(interfaces),
        "cylinder_rows_complete": "4/5",
        "physical_strong_rows_complete": "1/5_TAG_ROW_ONLY_PINNED",
        "type_guard": "a normal metric current on the artificial tagged graph cylinder is not a physical collision-space anisotropic current, transfer-operator/Piola carrier, or singular cemetery",
        "status": "CERTIFIED_EXACT_ENDPOINT_TRACED_NORMAL_METRIC_CURRENT_ON_TAGGED_GRAPH_CYLINDER__DOWNSTREAM_PHYSICAL_ACCEPTANCE_ABSENT",
    }


def type_separator() -> dict[str, Any]:
    return {
        "endpoint_space": "the discrete two-point metric space {a,b}",
        "graph_record": "one positive record with source a and landing b",
        "cylinder_fact": "the tagged graph cylinder carries a unit interval normal current whose labelled boundary traces are delta_b and delta_a",
        "physical_fact": "every metric 1-current on a finite discrete space is zero, so no physical-space current has boundary delta_b-delta_a",
        "scope": "exact logical type/nonimplication model; not asserted to be a billiard realization",
        "conclusion": "endpoint-preserving graph-cylinder current existence does not imply a physical phase-space current or operator-compatible strong recipient",
        "status": "CERTIFIED_TYPE_SEPARATOR__GRAPH_CYLINDER_CURRENT_DOES_NOT_PROMOTE_TO_PHYSICAL_CURRENT",
    }


def seven_fields() -> dict[str, Any]:
    rows = [
        {"field": 1, "name": "physical invariant product rectangles", "state": "PARTIAL_TAGGED_FINITE_DEPTH_CONE_CURVE_ATLAS_ONLY"},
        {"field": 2, "name": "stable projection and two-sided J_hol", "state": "NOT_CERTIFIED__EXACT_DEFECT_CALCULUS_ONLY"},
        {"field": 3, "name": "full span or marker fragmentation", "state": "NOT_CERTIFIED"},
        {"field": 4, "name": "same-law unstable conditionals and density bounds", "state": "PARTIAL_ACTUAL_DYNAMIC_BRANCH_RN_COVARIANCE__NO_STABLE_QUOTIENT_OR_TWO_SIDED_BOUNDS"},
        {"field": 5, "name": "physical boundary charge below C_p", "state": "NOT_CERTIFIED"},
        {"field": 6, "name": "tagged Borel branch inverse", "state": "CERTIFIED_PINNED_ROUND59"},
        {"field": 7, "name": "strong restriction and assembly", "state": "PARTIAL_GRAPH_CYLINDER_NORMAL_CURRENT__NO_PHYSICAL_STRONG_OPERATOR_ASSEMBLY"},
    ]
    return {
        "rows": rows,
        "rows_sha256": digest(rows),
        "complete_rows": "1/7",
        "partial_rows": [1, 4, 7],
        "official_immutable_Gate2_fields": "0/17",
        "quantitative_bridge": "F(u)R(u)<C_p*theta(u)*L(u) remains unpaid on the actual common landing law",
        "independent_debts": "Round60 smooth perfect-product separators retain independent short-plaque and fragmentation debts; Round61 g_N retains unbounded BV/derivative trace at fixed scalar D_land moment",
        "status": "CERTIFIED_ROUND62_SEVEN_FIELD_AUDIT__ONE_COMPLETE_THREE_PARTIAL__NO_GATE_PROMOTION",
    }


STRICT = {
    "actual_first_return_branch_RN_covariance": "CERTIFIED_EXACT",
    "physical_stable_holonomy_marker_covariance": "NOT_CERTIFIED",
    "holonomy_defect_isometry_cocycle_interface": "CERTIFIED_EXACT",
    "physical_invariant_product_quotient_and_J_hol": "NOT_CERTIFIED",
    "fibrewise_FR_below_Cp_theta_L": "NOT_CERTIFIED",
    "tagged_graph_cylinder_normal_current": "CERTIFIED_EXACT",
    "D_land_pays_cylinder_current_norms": "CERTIFIED_EXACT",
    "physical_anisotropic_current_Piola_recipient": "NOT_CERTIFIED",
    "downstream_accepts_positive_bad_current": "NOT_CERTIFIED",
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


def build_result() -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "claim_type": "actual tagged first-return RN covariance, exact stable-holonomy defect calculus, and exact tagged graph-cylinder normal-current recipient",
            "parameter_scope": "parameterwise for every fixed |s|<=1/400",
            "dependency_sha256": DEPENDENCIES,
            "baseline_file_sha256": BASELINE,
            "old_artifacts_modified": False,
            "external_theorem_promoted": False,
        },
        "actual_branch_RN_covariance": branch_covariance(),
        "stable_holonomy_marker_defect": holonomy_defect(),
        "tagged_graph_cylinder_current": graph_cylinder_current(),
        "graph_to_physical_current_type_separator": type_separator(),
        "seven_field_materialization_audit": seven_fields(),
        "latest_official_technology_audit": {
            "checked_through": "2026-07-21 official arXiv surface",
            "new_2607_closure_found": False,
            "Climenhaga_Day_2604_25881v1": "MME total-image-length/product law is the wrong measure and does not control retained component inverse lengths, marker theta/R/F, or the pinned common landing",
            "Canestrari_2604_19671v2": "starts from already regular standard families and pays survival-mass normalization; it does not create the present landing regularity or strict threshold",
            "Demers_Liverani_2606_10155v1": "review does not install the tagged graph carrier in a physical strong/Piola space",
            "external_theorem_promoted": False,
            "status": "AUDITED_NO_CURRENT_OFFICIAL_THEOREM_CLOSES_PINNED_PRODUCT_MARKER_OR_PHYSICAL_CURRENT_JOIN",
        },
        "downstream_typing": {
            "killed_C24": "the original first-hit/intermediate-avoidance record is retained exactly in the cylinder trace, but no accepted killed strong kernel follows",
            "properness": "the good subkernel may have zero mass and source properness is not inferred; F*R<C_p*theta*L remains unpaid",
            "later_clocks": "D_land is a landing defect mark, not a joint later/repeated recovery clock",
            "physical_q": "normal mass on a bookkeeping cylinder is not collision-time q in L^(6/5)",
            "cemetery": "the positive bad measure remains ordinary collision-SRB mass and is not renamed singular or collision-null cemetery",
            "operator": "no billiard transfer operator, moving-domain Piola map, strong R_s/Q_s, or MT_DQ acts on the graph cylinder",
            "status": "CERTIFIED_EXACT_ENDPOINT_AND_KILLED_TAG_RETENTION__ALL_PHYSICAL_STRONG_DOWNSTREAM_JOINS_OPEN",
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
        print(f"ROUND62_GATE42_BRANCH_CURRENT_CERT_FAILURE: {exc}")
        return 1

    print("BRANCH_RN_COVARIANCE:", data["result"]["strict_nonpromotion"]["actual_first_return_branch_RN_covariance"])
    print("GRAPH_CYLINDER_CURRENT:", data["result"]["strict_nonpromotion"]["tagged_graph_cylinder_normal_current"])
    print("PHYSICAL_CURRENT:", data["result"]["strict_nonpromotion"]["physical_anisotropic_current_Piola_recipient"])
    print("GATE2:", data["result"]["strict_nonpromotion"]["Gate2"])
    print("GATE4:", data["result"]["strict_nonpromotion"]["Gate4"])
    print("CM2:", data["result"]["strict_nonpromotion"]["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
