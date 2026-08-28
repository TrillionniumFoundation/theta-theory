#!/usr/bin/env python3
"""Round-61 Gate-4 marker-weighted curve / graph-defect frontier.

This append-only certificate starts from the frozen Round-60 Gate-4 leaf.
It certifies two exact interfaces without promoting Gate 4:

* the actual common landing marker can be multiplied into the already
  certified Round-56 slope-four physical standard-family representation of
  ``mu_s|C_s``.  This gives an exact marker-weighted curve-measure lift, but not a
  Rokhlin partition, invariant unstable plaques, stable holonomy, or the
  quantitative fragmentation/density bounds needed for properness;
* the finite ``D_land`` moment is exactly the norm of the bad graph measure
  in a weighted graph-total-variation Banach lattice.  This preserves every
  endpoint and immutable tag and gives an exact good+bad identity.  It is not
  the requested anisotropic/current cemetery space.  A smooth separator
  proves that the scalar moment cannot control even BV/derivative variation;
  it is not asserted to refute every possible anisotropic norm.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate4.round61-marker-weighted-curve-defect-ledger-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier"
DEFAULT_MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-20.json"
DEFAULT_REPORT = HERE / f"{PREFIX}-assault-2026-07-20.md"
DEFAULT_VERIFIER = HERE / "cm2_gate4_round61_marker_weighted_curve_defect_ledger_frontier_verifier.py"

DEPENDENCIES = {
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json":
        "08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3",
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json":
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c",
    "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json":
        "7c9d089219ef00234b7e7bdafaea706bd4c91a46990d6f14d0837ea360406414",
    "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json":
        "d335ea6b9bfdc68c13fa0c44f5f2893af7399546f5951d0cfc156be8b5236ffb",
    "cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json":
        "1600a3e060e7ae9601a55d425fbce5a27612300e26e01c77f53158b93010a424",
}

PINNED_BASELINE_FILES = {
    "cm2-sixtieth-direct-assault-2026-07-20.md":
        "ef3f2739a7a0ed8c91e82400c05564f97f0c3326ebc1373764b51bbd48f04212",
    "cm2-sixtieth-direct-assault-manifest-2026-07-20.sha256":
        "5f6c90735cbb74ec7b36f6c1d2b012ccccaafa40793d291dfcb6a0e212044e9e",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-assault-2026-07-20.md":
        "88f042ed434f6199123a5f164385572dabfcde0af13a8d6b9d7ca1385079d00f",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json":
        "08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.sha256":
        "4d7c3f06e1671319482c064ec3ea817562567202b111fd014434b7be0a460fac",
    "cm2_gate4_round60_physical_rn_good_bad_assembly_frontier_cert.py":
        "4a5d914ce8fec6c259e8df49f6c9ce04cc17285adfd2fd06173270635982f1b7",
    "cm2_gate4_round60_physical_rn_good_bad_assembly_frontier_verifier.py":
        "c74c71809b8484c85eadc921a74e6fdc6c38e85179167f68226844f685267503",
}

C_P = Q(4 * 10**90 * 360493663, 358863)
SHORT_L = Q(2, 1) / (3 * C_P)
SHORT_H = SHORT_L / 2
SHORT_J = Q(1, 2)
SHORT_Z = SHORT_J / SHORT_H
SHORT_D = 2
SHORT_WEIGHTED_MOMENT = SHORT_H * 2**SHORT_D


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(key)
        out[key] = value
    return out


def strict_json(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=strict_object,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def defect_depth(z: Q) -> int:
    if z < C_P:
        return 0
    d = 1
    while Q(1, 2**d) * z >= C_P / 2:
        d += 1
    return d


def load_inputs() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"dependency path: {name}")
        require(path.resolve().parent == HERE, f"dependency scope: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        data = strict_json(path.read_text(encoding="utf-8"))
        require(isinstance(data, dict) and isinstance(data.get("result"), dict), f"dependency root: {name}")
        loaded[name] = data

    for name, expected in PINNED_BASELINE_FILES.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"baseline path: {name}")
        require(path.resolve().parent == HERE, f"baseline scope: {name}")
        require(sha256_path(path) == expected, f"baseline hash: {name}")

    r60 = loaded[
        "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json"
    ]["result"]
    require(r60["strict_nonpromotion"]["Gate4"] == "NOT_CERTIFIED", "Round60 Gate4")
    require(r60["strict_nonpromotion"]["complete_composite_gates"] == "0/5", "Round60 gates")
    require(r60["actual_landing_RN_marker_bridge"]["status"].startswith("CERTIFIED_ACTUAL_RN_MARKER"), "Round60 marker")
    require("integral_B h*2^D_land" in r60["good_bad_original_time_graph_split"]["bad_dyadic_moment"], "Round60 D moment")

    r35 = loaded[
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    ]["result"]
    leaf = r35["collision_SRB_leaf_disintegration"]
    require(leaf["coordinate_change"] == "(r,b)->(r,p=sin(4r+b))", "Round35 coordinates")
    require(leaf["conditional_density_wrt_dell"] == "cp/sqrt(17)", "Round35 density")
    require(leaf["integrating_leaf_weights_recovers_mu_s_restricted_to_component"] is True, "Round35 recovery")
    require(r35["arbitrary_Rn_parent_W_Borel_registry"]["inside_invariant_unstable_cone"] is True, "Round35 cone")

    r56 = loaded[
        "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json"
    ]["result"]["paired_leafwise_reverse_replay"]
    require("exactly mu_s|C_s" in r56["forward_initial_family"], "Round56 exact source")
    require("represents (T_C_s)_#(mu_s|C_s)=mu_s|C_s exactly once" in r56["induced_return_once_coverage"], "Round56 exact landing")
    require("subinterval of the exact Round35 slope-four" in r56["forward_terminal_exact_inclusion"], "Round56 curve lift")

    r58 = loaded[
        "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json"
    ]["result"]
    require(r58["maximal_component_minimum_Z_theorem"]["status"].startswith("CERTIFIED_MAXIMAL_COMPONENT"), "Round58 iff")
    require(r58["landing_bad_stratum_interface"]["dyadic_moment"].startswith("integral h(y)*2^D_land"), "Round58 moment")

    r57 = loaded[
        "cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json"
    ]["result"]["raw_common_first_return_typing"]
    require(r57["status"] == "CERTIFIED_BUT_UNPROPER", "Round57 graph")
    require("notin C_s" in r57["first_hit_semantics"], "Round57 killed path")
    require("charged exactly once" in r57["charge"], "Round57 once charge")
    return loaded


def marker_weighted_curve_lift() -> dict[str, Any]:
    return {
        "ambient_representation": "the frozen Round56 E_fw,total is a countable actual physical standard-family representation of mu_C=mu_s|C_s exactly once on regular images of Round35 slope-four leaves",
        "source_marker": "a=d kappa_A/d mu_C exists with 0<=a<=1 and satisfies a=g_B after transport by the exact induced branch, modulo the fixed branch tags",
        "linear_multiplier_identity": "if mu_C=integral mu_omega dP(omega), then kappa_B=g_B*mu_C=integral (g_B*mu_omega) dP(omega) without conditioning or fibre normalization",
        "source_leaf_density": "on a Round35 source leaf, d(a*mu_omega)/dell_A=a*cp/sqrt(17)",
        "landing_leaf_density": "on each fixed tagged regular branch H=T_s^n|U, the image is a regular unstable-cone C1 curve (not generally slope four), and the pushed curve-measure density is the source density divided by the one-dimensional Euclidean-arclength Jacobian J_ellE H; the outer branch/tag measure is pushed simultaneously",
        "support_and_tags": "every marked landing curve-measure is a positive Borel restriction of B'=T_s^n(A') and retains n/path/physical-ID/half-open owner and one parent charge",
        "zero_mass_policy": "zero marked proof curves are deleted without normalization; no value is assigned to a null conditional",
        "exact_scope": "CERTIFIED on the countable tagged finite-depth cone-curve measure lift of the physical landing measure",
        "rokhlin_guard": "the standard-family mixture may overlap after forgetting proof tags and is not asserted to be a partition subordinate to invariant unstable manifolds",
        "holonomy_guard": "the slope-four foliation is an artificial invariant-cone foliation, not a stable-holonomy product rectangle or a dynamically invariant unstable Rokhlin quotient",
        "quantitative_guard": "an arbitrary Borel 0<=g_B<=1 can create zero sets, arbitrarily many components and unbounded log/BV oscillation; no positive lower density, theta, F, R or plaque-span bound follows",
        "field_effect": "fields 1 and 4 gain exact tagged curve-measure-lift partial interfaces only; arbitrary Borel marking is not claimed to remain a regular standard family, and no complete seven-field row is added",
        "status": "CERTIFIED_EXACT_ACTUAL_MARKER_WEIGHTED_CONE_CURVE_MEASURE_LIFT__NOT_REGULAR_STANDARD_FAMILY_OR_PHYSICAL_ROKHLIN_HOLONOMY_PRODUCT",
    }


def graph_defect_lattice() -> dict[str, Any]:
    atoms = [
        {"D": 2, "mass": "3/20", "weighted_mass": "3/5"},
        {"D": 5, "mass": "1/80", "weighted_mass": "2/5"},
        {"D": 7, "mass": "1/320", "weighted_mass": "2/5"},
    ]
    mass = sum(Q(row["mass"]) for row in atoms)
    weighted = sum(Q(row["weighted_mass"]) for row in atoms)
    require(mass == Q(53, 320), "sample graph mass")
    require(weighted == Q(7, 5), "sample graph norm")
    require(all(Q(row["weighted_mass"]) == 2 ** row["D"] * Q(row["mass"]) for row in atoms), "sample weights")
    rows = [
        {"index": 1, "required": "positive endpoint-preserving embedding", "graph_lattice": "CERTIFIED_IDENTITY_EMBEDDING_IN_X_D_GRAPH", "strong_current_cemetery": "NOT_CERTIFIED"},
        {"index": 2, "required": "retain n/path/ID/owner and once charge", "graph_lattice": "CERTIFIED_EXACTLY", "strong_current_cemetery": "NOT_A_SEPARATE_ISSUE"},
        {"index": 3, "required": "norm bound paid by D_land", "graph_lattice": "CERTIFIED_EQUALITY_WITH_CONSTANT_ONE", "strong_current_cemetery": "NOT_CERTIFIED"},
        {"index": 4, "required": "Full=Good+included Bad without endpoint replacement", "graph_lattice": "CERTIFIED_EXACT_MEASURE_IDENTITY", "strong_current_cemetery": "NOT_CERTIFIED"},
        {"index": 5, "required": "downstream CM2 theorem accepts the positive remainder", "graph_lattice": "NOT_CERTIFIED", "strong_current_cemetery": "NOT_CERTIFIED"},
    ]
    return {
        "space": "X_D^graph={finite signed tagged graph measures nu: integral 2^D_land(y) d|nu|<infinity}",
        "norm": "||nu||_X=integral 2^D_land(y) d|nu|",
        "banach_lattice_proof": "multiplication nu->2^D_land nu is an isometric order isomorphism from X_D^graph onto finite signed measures with total variation norm",
        "bad_embedding": "E_B Gamma_B=Gamma_B with identical physical source/landing endpoints and immutable tags",
        "exact_norm_identity": "||E_B Gamma_B||_X=integral_B h(y)*2^D_land(y) dlambda(y)<infinity",
        "endpoint_contractions": "source and landing pushforwards have ordinary total variation at most ||nu||_X because 2^D_land>=1",
        "exact_hybrid_identity": "Gamma_cap=Gamma_G+iota_B(E_B Gamma_B) as positive tagged graph measures; no bad regular mass is deleted, normalized, moved, or renamed singular cemetery",
        "tail": "for every integer k, |Gamma_B|{D_land>=k}<=2^-k ||E_B Gamma_B||_X; the weighted tail itself vanishes qualitatively by integrability",
        "sample_atoms": atoms,
        "sample_atoms_sha256": digest(atoms),
        "sample_total_mass": qstr(mass),
        "sample_weighted_norm": qstr(weighted),
        "five_interface_rows": rows,
        "five_interface_rows_sha256": digest(rows),
        "graph_rows_complete": "4/5",
        "requested_strong_interface_rows_complete": "1/5_TAG_ROW_ONLY",
        "type_guard": "X_D^graph is a weighted total-variation trace ledger, not the anisotropic distribution/current space required by the strong cemetery or Piola/operator joins",
        "status": "CERTIFIED_EXACT_POSITIVE_GOOD_BAD_HYBRID_IN_WEIGHTED_GRAPH_TV_LATTICE__DOWNSTREAM_STRONG_ACCEPTANCE_ABSENT",
    }


def smooth_strong_separator() -> dict[str, Any]:
    require(SHORT_Z == Q(3, 2) * C_P, "short z")
    require(defect_depth(SHORT_Z) == SHORT_D, "short D")
    require(SHORT_WEIGHTED_MOMENT == 2 * SHORT_L, "short moment")
    rows = []
    for frequency in (1, 2, 17, 257, 4096):
        rows.append(
            {
                "frequency_N": frequency,
                "plaque_length_L": qstr(SHORT_L),
                "marker": "g_N(x)=1/2+(1/4)sin(2*pi*N*x/L)",
                "marker_range": "[1/4,3/4]",
                "mass_h": qstr(SHORT_H),
                "minimal_boundary_J": qstr(SHORT_J),
                "normalized_boundary_z": qstr(SHORT_Z),
                "D_land": SHORT_D,
                "weighted_D_moment": qstr(SHORT_WEIGHTED_MOMENT),
                "BV_variation_of_marker": frequency,
            }
        )
    require(all(Q(row["weighted_D_moment"]) == SHORT_WEIGHTED_MOMENT for row in rows), "constant moment")
    require(rows[-1]["BV_variation_of_marker"] > 1000 * rows[0]["BV_variation_of_marker"], "BV separation")
    return {
        "scope": "exact smooth Euclidean product identity-return logical models; not asserted to be billiard realizations",
        "geometry": "one short full plaque with identity holonomy, one physical ID, no gaps, smooth strictly positive RN marker and exact identity first return",
        "rows": rows,
        "rows_sha256": digest(rows),
        "calculus": "integral_0^L g_N=L/2, J=(L/2)/L=1/2, z=1/L=3C_p/2, D_land=2, and integral_0^L |g_N'|=N",
        "conclusion": "the same finite D_land graph moment and perfect endpoint geometry coexist with arbitrarily large BV/derivative trace charge; no universal BV/derivative estimate follows from the scalar moment. This does not purport to refute every possible anisotropic norm",
        "status": "CERTIFIED_SMOOTH_SEPARATOR__D_LAND_MOMENT_DOES_NOT_CONTROL_BV_DERIVATIVE_TRACE",
    }


def field_audit() -> dict[str, Any]:
    rows = [
        {"field": 1, "name": "physical product-rectangle cover", "actual": "PARTIAL_TAGGED_FINITE_DEPTH_CONE_CURVE_ATLAS__NO_STABLE_PRODUCT_RECTANGLES"},
        {"field": 2, "name": "stable projection and two-sided holonomy Jacobian", "actual": "NOT_CERTIFIED"},
        {"field": 3, "name": "full span or quantitative marker fragmentation", "actual": "NOT_CERTIFIED"},
        {"field": 4, "name": "same-measure unstable conditionals with density/log distortion", "actual": "PARTIAL_EXACT_MARKER_WEIGHTED_CURVE_MEASURE_LIFT__NOT_REGULAR_STANDARD_FAMILY__NO_ROKHLIN_PARTITION_OR_TWO_SIDED_BOUNDS"},
        {"field": 5, "name": "physical boundary charge below C_p", "actual": "NOT_CERTIFIED"},
        {"field": 6, "name": "tagged Borel branch inverse retaining n/path/ID/owner", "actual": "CERTIFIED_ROUND59"},
        {"field": 7, "name": "strong restriction and assembly", "actual": "PARTIAL_EXACT_GRAPH_TV_ASSEMBLY__NOT_STRONG_CURRENT_OR_OPERATOR_ASSEMBLY"},
    ]
    return {
        "rows": rows,
        "rows_sha256": digest(rows),
        "actual_complete_rows": "1/7",
        "partial_rows": [1, 4, 7],
        "official_Gate2_fields_unchanged": "0/17",
        "quantitative_bridge": "F(u)R(u)<C_p*theta(u)*L(u) remains necessary on an actual compatible product law; none of F,R,theta,L is supplied for g_B",
        "shortest_remaining_join": "construct an actual invariant unstable/stable product quotient on the common landing, bound marker fragmentation/span/density there, prove the strict fibrewise threshold, and identify X_D^graph with an accepted strong operator/current space or supply a downstream positive-remainder theorem",
        "status": "CERTIFIED_ROUND61_SEVEN_FIELD_AUDIT__ONE_COMPLETE_THREE_PARTIAL__NO_PROMOTION",
    }


def literature_audit() -> dict[str, Any]:
    return {
        "checked_on": "2026-07-20 through the official arXiv API/current versions",
        "Climenhaga_Day": "arXiv:2604.25881v1, Every finite horizon Sinai billiard map has a unique measure of maximal entropy",
        "Theorem_B_value": "for unstable C1 curves above a fixed length scale, the theorem controls total connected-image length up to Q*exp(n*h_top)",
        "Theorem_B_measure_guard": "the paper's product law and symbolic holonomy are for its MME, not the pinned Liouville/SRB marker g_B*mu_C",
        "Theorem_B_boundary_guard": "total image length controls neither marker component count nor the inverse component lengths entering J_land,min; it supplies no theta, two-sided density ratio R, or F*R<C_p*theta*L",
        "Canestrari": "arXiv:2604.19671v2 starts standard-family evolution from an already regular (omega,B,D) family; thin restrictions pay conditioned-mass normalization and no theorem installs the present marker boundary bound",
        "strong_space_guard": "the small-hole paper explicitly notes that no known general piecewise-hyperbolic Banach spaces contain standard pairs; its C1-test coupling does not identify X_D^graph with the required strong current space",
        "latest_relevant_API_entry": "arXiv:2606.10155v1 remains a transfer-operator review and adds no typed common-landing closure",
        "external_theorem_promoted": False,
        "status": "AUDITED_NO_CURRENT_OFFICIAL_THEOREM_PAYS_MARKER_FRAGMENTATION_OR_STRONG_DEFECT_JOIN",
    }


def downstream_audit() -> dict[str, Any]:
    return {
        "killed_C24": "the original first-hit predicate is retained on both Gamma_G and E_B Gamma_B in the exact graph identity; it becomes an accepted killed kernel only after a legal full hybrid target space is supplied",
        "good_scope": "Gamma_G remains a possibly-zero proper landing subfamily; physical source properness is not inferred",
        "bad_scope": "Gamma_B remains positive ordinary physical mass in X_D^graph and is never relabelled collision-null singular cemetery",
        "later_clocks": "D_land is a landing geometry mark, not a joint all-stage recovery clock; no later or repeated exponential moment follows",
        "physical_q": "the X_D^graph norm is weighted L1 total variation and supplies neither the same-law all-time C_fw/C_rev ledger nor an L^(6/5) collision-time q",
        "strong_cemetery": "the smooth separator blocks a free BV/derivative-trace promotion; no typed identification with the requested anisotropic/current cemetery has been supplied",
        "status": "CERTIFIED_EXACT_KILLED_TAG_RETENTION_IN_GRAPH_LEDGER__ALL_DOWNSTREAM_STRONG_JOINS_NOT_CERTIFIED",
    }


def strict_frontier() -> dict[str, Any]:
    return {
        "actual_landing_RN_marker": "CERTIFIED_PINNED_ROUND60",
        "actual_marker_weighted_cone_curve_lift": "CERTIFIED_EXACT",
        "physical_invariant_unstable_Rokhlin_and_stable_holonomy": "NOT_CERTIFIED",
        "seven_field_physical_landing_join": "1/7_COMPLETE__FIELDS_1_4_7_PARTIAL_ONLY",
        "fibrewise_J_land_min_below_Cp_h": "NOT_CERTIFIED",
        "positive_good_bad_weighted_graph_hybrid": "CERTIFIED_EXACT_IN_X_D_GRAPH_ONLY",
        "D_land_pays_weighted_graph_TV_defect": "CERTIFIED_EXACT",
        "D_land_pays_BV_or_strong_current_defect": "NOT_CERTIFIED__BV_DERIVATIVE_ROUTE_FALSE_BY_SMOOTH_SEPARATOR",
        "downstream_accepts_positive_graph_defect": "NOT_CERTIFIED",
        "physical_proper_same_ID_first_return_landing_kernel": "NOT_CERTIFIED",
        "physical_proper_same_ID_first_return_kernel": "NOT_CERTIFIED",
        "original_Rn_intermediate_C24_avoidance": "CERTIFIED_PINNED_ROUND57",
        "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
        "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
        "strong_singular_current_cemetery": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def build_result() -> dict[str, Any]:
    load_inputs()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "baseline_file_sha256": dict(PINNED_BASELINE_FILES),
            "old_artifacts_modified": False,
            "parameter_scope": "parameterwise for every fixed |s|<=1/400",
            "claim_type": "exact marker-weighted physical cone-curve measure lift, exact weighted graph-TV good/bad ledger, and strong-norm separator",
            "external_theorem_promoted": False,
        },
        "actual_marker_weighted_curve_lift": marker_weighted_curve_lift(),
        "weighted_graph_defect_lattice": graph_defect_lattice(),
        "smooth_Dland_vs_strong_separator": smooth_strong_separator(),
        "seven_field_materialization_audit": field_audit(),
        "latest_official_technology_audit": literature_audit(),
        "downstream_join_audit": downstream_audit(),
        "strict_nonpromotion": strict_frontier(),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path = DEFAULT_VERIFIER) -> dict[str, Any]:
    verifier = verifier.resolve()
    require(verifier.is_file() and not verifier.is_symlink(), "verifier path")
    require(verifier.parent == HERE, "verifier scope")
    require(DEFAULT_REPORT.is_file() and not DEFAULT_REPORT.is_symlink(), "report path")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "dependencies": dict(DEPENDENCIES),
        "baseline_files": dict(PINNED_BASELINE_FILES),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier),
        "report_sha256": sha256_path(DEFAULT_REPORT),
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }


def encoded_manifest(verifier: Path = DEFAULT_VERIFIER) -> str:
    return json.dumps(build_manifest(verifier), indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
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
    except (OSError, RuntimeError, ValueError, KeyError, TypeError) as exc:
        print(f"ROUND61_GATE4_CURVE_DEFECT_CERT_FAILURE: {exc}")
        return 1

    strict = build_result()["strict_nonpromotion"]
    print("CURVE_LIFT:", strict["actual_marker_weighted_cone_curve_lift"])
    print("GRAPH_HYBRID:", strict["positive_good_bad_weighted_graph_hybrid"])
    print("STRONG_DEFECT:", strict["D_land_pays_BV_or_strong_current_defect"])
    print("GATE4:", strict["Gate4"])
    print("CM2:", strict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
