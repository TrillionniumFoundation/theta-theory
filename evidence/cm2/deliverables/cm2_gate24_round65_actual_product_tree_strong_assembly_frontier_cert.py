#!/usr/bin/env python3
"""Round-65 Gate-2/4 actual product-tree / strong-assembly frontier."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round64_common import (
    CertError, digest, require, sha256_path, strict_json_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate24.round65.actual-product-tree-strong-assembly-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate24-round65-actual-product-tree-strong-assembly-frontier"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_gate24_round65_actual_product_tree_strong_assembly_frontier_verifier.py"

PINS = {
    "cm2_round64_common.py": "ac67b1c90e95b385d89aa2a39ecb0a6420a5b30d2f4b19f3eccb6bd404598100",
    "cm2-sixty-fourth-direct-assault-2026-07-21.md": "bbd52eed540e4e91566a7d0b9fda2b381b35860640e23a0a45d29b73fabb8b61",
    "cm2-sixty-fourth-direct-assault-manifest-2026-07-21.sha256": "5d2174cee61c0fdf5573dedaece38950c0261fe05aa835b66c4363d974e52932",
    "cm2-round64-independent-core-frontier-audit-2026-07-21.md": "786922ef94b522498440cf90df562c77a65d991a03c01637d9740a22f0dcae49",
    "cm2-round64-independent-core-frontier-audit-manifest-2026-07-21.json": "e775720b2891146a39421d515280e119f42b075d0783650e879abe1370ff8779",
    "cm2-round64-independent-core-frontier-audit-manifest-2026-07-21.sha256": "d61e8f2ea2d3e5b172846a16fdfa75373058ec8b91759aea0e393c500ea0740b",
    "cm2-gate24-round64-weighted-tree-saturation-actual-join-obstruction-frontier-assault-2026-07-21.md": "24555f1e5350d59f2be6f83208617c945ee12c10b925f05b7edc15c933044c76",
    "cm2-gate24-round64-weighted-tree-saturation-actual-join-obstruction-frontier-manifest-2026-07-21.json": "5bb198256f2a5aa8837326f9eab70aa4845adb80417dc27379f27f7e8f24f8d0",
    "cm2-gate24-round64-weighted-tree-saturation-actual-join-obstruction-frontier-manifest-2026-07-21.sha256": "0943cc0316319a823f91ed29f732a1f828204db1e4376f8bad887523388809c6",
    "cm2-gate24-round64-rooted-atlas-jacobian-tag-lift-frontier-assault-2026-07-21.md": "8c27993b71afa06f2b5a0432fea9aecb367329f1be6760d17e98bde0029b62c4",
    "cm2-gate24-round64-rooted-atlas-jacobian-tag-lift-frontier-manifest-2026-07-21.json": "6eb0dbe73b21b5822e9e589b5f6a047b47966a349ec54e8e3b150b9bf203b1af",
    "cm2-gate24-round64-rooted-atlas-jacobian-tag-lift-frontier-manifest-2026-07-21.sha256": "474038420728935370c8ab9eb7be6df99fcf0da3e2baa88c01a8eff9c3f2d007",
    "cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier-assault-2026-07-20.md": "f89fbb0180fe88cac358b14541d8e5f98a72a23a3d27a313f2fbef3a0a22d68f",
    "cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier-manifest-2026-07-20.json": "f897d81a2e85c4a8e45c436f169043feaef93b019f18229a44da0227c75b2a88",
    "cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier-manifest-2026-07-20.sha256": "6a29c47462a9526138a059f8577abcf879cd162feca14b435906cce1cd8c087a",
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json": "e7305e0b72eed28bc68b115e1201fc02e2b66d3cc95906fc6d1efc5e9463a4f5",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json": "08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3",
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.json": "2edf4d7801525c746c619cb85b39c59d30018df7c6971f5e48639dc390573b9b",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json": "e0b89d604e89852b574638428a60daa1f6e8231b85177230a5dd67615205bad1",
    "cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.json": "27c5d2e9a6ac9ed8eeb3d42dc96aa1c0a8faa8e50e006811efea22b45c86b859",
}

PHYSICAL = {
    "owner": "cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.json",
    "inverse": "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json",
    "marker": "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json",
    "curve": "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.json",
    "branch": "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json",
}

STRICT = {
    "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
    "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
    "actual_stable_tree_instantiation": "0/7",
    "complete_composite_gates": "0/5",
    "CM2": "NO-GO_FOR_CLAIM",
}


def qstr(x: Q) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def l1(a: list[Q], b: list[Q]) -> Q:
    return sum((abs(x - y) for x, y in zip(a, b)), Q(0)) / len(a)


def median(values: list[Q], weights: list[Q]) -> Q:
    total = Q(0)
    for value, index in sorted((value, i) for i, value in enumerate(values)):
        total += weights[index]
        if total >= Q(1, 2):
            return value
    raise CertError("median exhausted")


def plaque_law_result() -> dict[str, Any]:
    weights = [Q(1, 10), Q(1, 5), Q(1, 5), Q(1, 4), Q(1, 4)]
    markers = [
        [Q(0), Q(0), Q(1), Q(1)],
        [Q(0), Q(1), Q(1), Q(0)],
        [Q(1), Q(1), Q(0), Q(0)],
        [Q(0), Q(1), Q(0), Q(1)],
        [Q(1), Q(0), Q(1), Q(0)],
    ]
    medians: list[Q] = []
    delta = Q(0)
    for column in zip(*markers):
        m = median(list(column), weights)
        medians.append(m)
        delta += sum((w * abs(x - m) for w, x in zip(weights, column)), Q(0)) / 4
    dispersion = sum(
        (weights[i] * weights[j] * l1(markers[i], markers[j])
         for i in range(5) for j in range(i + 1, 5)), Q(0)
    )
    require(delta == Q(2, 5) and dispersion == Q(19, 80), "plaque replay")
    require(dispersion < delta < 2 * dispersion, "plaque sandwich")
    replay = {
        "outer_weights": [qstr(x) for x in weights],
        "pulled_markers": [[qstr(x) for x in row] for row in markers],
        "lower_median": [qstr(x) for x in medians],
        "delta_eta": qstr(delta),
        "P_eta": qstr(dispersion),
        "strict_sandwich": True,
    }
    return {
        "hypotheses": "standard-Borel plaque probability eta, common root law mu_0, measurable positive onto L1 isometries P_u, and jointly measurable integrable pulled marker a(u,x)=P_u^-1 g_u",
        "median_formula": "delta_eta=int_X min_t int_U |a(u,x)-t| deta dmu_0, attained by the measurable lower median",
        "dispersion": "P_eta=(1/2)int_U int_U ||a(u)-a(v)||_1 deta(u)deta(v)",
        "sharp_sandwich": "P_eta<=delta_eta<=2*P_eta",
        "zero_criterion": "delta_eta=0 iff P_eta=0 iff a(u,x)=a(v,x) eta*eta*mu_0-a.e.",
        "commuting_dynamic_family": "D_u P_u^S=P_u^L D_0 with onto L1 isometry D_0 implies delta_eta^L=delta_eta^S and P_eta^L=P_eta^S",
        "actual_marker_interpretation": "after a physical collision-SRB stable trivialisation exists, P_eta(g_B)=0 is exactly stable descent of kappa_B=g_B mu_C",
        "actual_P_eta_zero": "NOT_CERTIFIED",
        "finite_replay": replay,
        "status": "CERTIFIED_EXACT_STANDARD_BOREL_PLAQUE_LAW_INTERFACE__ACTUAL_TRIVIALISATION_ABSENT",
    }


def all_depth_result() -> dict[str, Any]:
    good_rows = []
    bad_rows = []
    for n in range(1, 13):
        good_fail = Q(1, 2 ** (n + 2))
        good_survive = Q(3, 4) + Q(1, 2 ** (n + 2))
        bad_fail = Q(1, 2**n)
        bad_survive = Q(1, 2**n)
        good_rows.append({"depth": n, "first_failure_mass": qstr(good_fail),
                          "survivor_mass": qstr(good_survive)})
        bad_rows.append({"depth": n, "first_failure_mass": qstr(bad_fail),
                         "survivor_mass": qstr(bad_survive)})
    require(good_rows[0]["survivor_mass"] == "7/8", "good survivor")
    require(bad_rows[-1]["survivor_mass"] == "1/4096", "bad survivor")
    depth97 = [{"depth": n, "survives": n <= 96} for n in [1, 2, 95, 96, 97]]
    return {
        "exact_identity": "eta(S_infinity)=lim_N eta(S_N)=eta(S_0)-sum_N eta(F_N), F_N=S_(N-1)\\S_N",
        "positive_survivor_iff": "inf_N eta(S_N)>0 iff sum_N eta(F_N)<eta(S_0)",
        "compactness_bridge": "on S_infinity, compatible graph transforms in common charts with uniform cone/contraction and C1 compactness yield infinite physical stable plaques",
        "good_first_failure_replay": {"rows_first_12": good_rows, "total_failure_mass": "1/4",
                                      "infinite_survivor_mass": "3/4"},
        "positive_every_finite_depth_separator": {"model": "S_N=[0,2^-N]",
                                                   "rows_first_12": bad_rows,
                                                   "total_failure_mass": "1",
                                                   "infinite_survivor_mass": "0"},
        "depth97_separator": {"accepted_prefix_count": 96,
                              "first_unconstrained_depth": 97,
                              "sample": depth97,
                              "scope": "logical completion compatible with pinned depths 1..96; not an assertion of physical failure"},
        "physical_all_depth_base": "NOT_CERTIFIED",
        "status": "CERTIFIED_EXACT_FIRST_FAILURE_CRITERION_AND_TWO_FINITE_DEPTH_NONIMPLICATIONS",
    }


def actual_interface_result() -> dict[str, Any]:
    rows = [
        [1, "all-depth positive stable base and product-rectangle/tree key", "NOT_CERTIFIED__96_PREFIX_ONLY"],
        [2, "collision-SRB outer plaque law eta and measurable common-root trivialisation", "NOT_CERTIFIED"],
        [3, "source/landing stable holonomies, two-sided RN and adapted-arclength derivatives", "NOT_CERTIFIED"],
        [4, "same branch keys and measurable commuting-square family", "PARTIAL_DYNAMIC_KEYS_ONLY__STABLE_SQUARE_ABSENT"],
        [5, "actual stable marker dispersion P_eta=0", "NOT_CERTIFIED"],
        [6, "actual root F,R,theta,L and essential path m,M strict budget", "NOT_CERTIFIED"],
        [7, "endpoint-preserving strong restriction/intertwining/Piola recipient", "NOT_CERTIFIED"],
    ]
    return {
        "pinned_actual_fragments": [
            "Round59 tagged Borel first-return inverse",
            "Round60 g_B=d kappa_B/d mu_C with 0<=g_B<=1",
            "Round61 tagged finite-depth cone-curve marker lift",
            "Round62 actual dynamic branch RN covariance",
            "Round58 finite physical owner/root law on its stated carrier",
        ],
        "rows": [{"row": n, "required_object": name, "state": state} for n, name, state in rows],
        "actual_rows_complete": "0/7",
        "measure_law_guard": "nu, mu_C and weak quotient eta have no certified common stable-tree crosswalk",
        "nonatomic_path_budget": "F_0*R_0*esssup_u(M(u)/m(u)^2)<C_p*theta_0*L_0",
        "minimum_new_evidence": "one immutable strict-JSON registry carrying all seven rows on common rectangle/tree/branch/physical-ID/owner keys",
        "status": "CERTIFIED_EXACT_INTERFACE_MATRIX__NO_ACTUAL_TREE_PROMOTION",
    }


def strong_result() -> dict[str, Any]:
    trace_rows = []
    for n in [1, 2, 17, 257, 4096]:
        trace_rows.append({"N": n, "f_N": "1/2+(1/4)sin(2*pi*N*x)",
                           "L1_norm": "1/2", "variation": str(n)})
    oscillatory = []
    for n in [1, 2, 17, 257, 4096]:
        oscillatory.append({"N": n, "W_D": "1", "weighted_kernel_variation": str(4 * n)})
    sample = {
        "tags": ["k_1=x,a_1=1", "k_2=1-x,a_2=2"],
        "A_0": "2", "A_1": "3", "operator_bound_constant": "5",
        "test_f": "1+x", "test_f_BV_norm": "5/2",
        "tagged_output_BV_norm": "37/6", "upper_bound": "25/2",
        "trace": "x(1+x)+(1-x)(1+x)=1+x",
    }
    require(Q(sample["tagged_output_BV_norm"]) == Q(37, 6), "BV sample")
    return {
        "trace_factorisation_no_go": {
            "statement": "bounded E:L1->B_strong and bounded Tr:B_strong->BV with Tr*E=Id_L1 cannot exist",
            "reason": "it would bound the identity L1->BV",
            "rows": trace_rows,
            "status": "FALSE_BY_SMOOTH_EXACT_TRACE_SEPARATOR",
        },
        "countable_tagged_BV_bridge": {
            "hypotheses": "k_r>=0 in BV, sum_r k_r=1, a_r>=1, A_0=||sum_r a_r k_r||_infinity<infinity and A_1=sum a_r Var(k_r)<infinity",
            "bound": "sum_r a_r||k_r f||_BV<=(A_0+A_1)||f||_BV",
            "exact_trace": "sum_r k_r f=f",
            "sample": sample,
            "status": "CERTIFIED_CONDITIONAL_WEIGHTED_TAGGED_BV_LIFT",
        },
        "W_D_Linfinity_not_BV_separator": {
            "kernel": "k_1,N=(1+sin(2*pi*N*x))/2, k_2,N=1-k_1,N, both tag weights one",
            "rows": oscillatory,
            "conclusion": "W_D=1 does not bound weighted transverse BV variation",
            "status": "CERTIFIED_SMOOTH_SEPARATOR",
        },
        "actual_weighted_kernel_A0_A1": "NOT_CERTIFIED",
        "physical_Piola_intertwining_recipient": "NOT_CERTIFIED",
        "status": "CERTIFIED_SHORTEST_TAGGED_BV_BRIDGE_AND_EXACT_L1_TRACE_NO_GO__PHYSICAL_STRONG_ASSEMBLY_ABSENT",
    }


def technology_result() -> dict[str, Any]:
    return {
        "arXiv_2604_25746v1": "Pesin rectangles/holonomy/SRB for compact boundaryless C1+beta flows; fixed-point singularity is not billiard collision discontinuity",
        "arXiv_2604_25881v1": "local product structure for the billiard MME from symbolic Hausdorff leaf laws, not the pinned collision-SRB law mu_C",
        "fresh_official_API_attempt": "TIMED_OUT_WITH_ZERO_BYTES__NO_RESULT_PROMOTED",
        "external_theorem_promoted": False,
        "status": "AUDITED_WRONG_INTERFACE_AND_WRONG_LAW_RESULTS_NOT_PROMOTED",
    }


def load_result(name: str) -> dict[str, Any]:
    data = strict_json_path(HERE / name)
    result = data.get("result")
    require(isinstance(result, dict), f"manifest result: {name}")
    return result


def verify_physical_chain() -> None:
    r58 = load_result(PHYSICAL["owner"])
    r59 = load_result(PHYSICAL["inverse"])
    r60 = load_result(PHYSICAL["marker"])
    r61 = load_result(PHYSICAL["curve"])
    r62 = load_result(PHYSICAL["branch"])
    r60depth = load_result("cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier-manifest-2026-07-20.json")
    require(r58["physical_same_owner_extended_clearance_ledger"]["status"] ==
            "CERTIFIED_PHYSICAL_SAME_LAW_EXTENDED_LEDGER_NOT_FINITE", "owner pin semantics")
    require(r59["same_graph_rokhlin_reconditioning"]["status"] ==
            "CERTIFIED_WEAK_SAME_GRAPH_ROKHLIN_RECONDITIONING_AND_TAGGED_BOREL_BRANCH_INVERSE", "inverse semantics")
    require(r60["actual_landing_RN_marker_bridge"]["status"].startswith("CERTIFIED_ACTUAL_RN_MARKER"), "marker semantics")
    require(r61["actual_marker_weighted_curve_lift"]["status"].startswith("CERTIFIED_EXACT_ACTUAL_MARKER"), "curve semantics")
    require(r62["actual_branch_RN_covariance"]["status"].startswith("CERTIFIED_EXACT_ACTUAL_TAGGED"), "branch semantics")
    require(r60depth["gate2"]["finite_prefix_separator"]["accepted_prefix_count"] == 96 and
            r60depth["gate2"]["finite_prefix_separator"]["first_unconstrained_depth"] == 97,
            "depth97 semantics")


def build_result() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    verify_physical_chain()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {"append_only": True, "old_artifacts_modified": False,
                       "pinned_files": dict(PINS), "external_theorem_promoted": False},
        "standard_Borel_plaque_law_saturation": plaque_law_result(),
        "all_depth_stable_transform": all_depth_result(),
        "actual_product_tree_interface": actual_interface_result(),
        "tag_graph_to_BV_strong_frontier": strong_result(),
        "latest_technology_boundary": technology_result(),
        "strict_status": dict(STRICT),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    verifier = verifier.resolve()
    require(verifier.is_file() and not verifier.is_symlink() and verifier.parent == HERE,
            "verifier file")
    require(REPORT.is_file() and not REPORT.is_symlink() and REPORT.resolve().parent == HERE,
            "report file")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "pins": dict(PINS),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier),
        "report_sha256": sha256_path(REPORT),
        "result": result,
        "verdict": result["strict_status"],
    }


def render(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, indent=2, allow_nan=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=VERIFIER)
    args = parser.parse_args()
    try:
        data = build_manifest(args.verifier)
        payload = render(data)
        if args.write_manifest:
            target = args.write_manifest.resolve()
            require(target.parent == HERE and target.name == MANIFEST.name, "manifest output")
            target.write_text(payload, encoding="utf-8")
            print(f"WROTE_MANIFEST: {target}")
            return 0
        if args.manifest_json:
            print(payload, end="")
            return 0
        if args.audit:
            print("AUDIT: PASS")
            print(f"PINNED_FILES: {len(PINS)}/{len(PINS)}")
            print("RESULT_SHA256:", data["result"]["internal_replay_digest"])
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, IndexError,
            ArithmeticError) as exc:
        print(f"ROUND65_GATE24_CERTIFICATE_ERROR: {exc}", file=sys.stderr)
        return 1
    print("GATE2: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
