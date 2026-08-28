#!/usr/bin/env python3
"""Round-59 Gate-4 cross-fibre Rokhlin/landing-threshold frontier.

This append-only certificate starts from the frozen Round-58 exact
``J_land,min`` iff.  It proves two new type-level facts.

First, aggregate boundary control cannot replace the required fibrewise
strict inequality: an exact two-fibre identity-return model has arbitrarily
good aggregate normalized boundary, finite ``D_land`` moment and ``D_cap=0``
while one positive outer fibre remains physically improper.

Second, the tagged Round-57 first-return graph already supplies the Borel
branch inverse and the measure-a.e. graph/tag semantics for a lossless
Rokhlin reconditioning.  A supplied physical unstable-product disintegration would
therefore preserve the exact graph.  The physical product rectangles,
holonomy bounds, common-restriction fragmentation/density rows, boundary
inequality and strong assembly are not supplied, so Gate 4 is not promoted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate4.round59-cross-fibre-rokhlin-threshold-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier"
DEFAULT_MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-20.json"
DEFAULT_REPORT = HERE / f"{PREFIX}-assault-2026-07-20.md"
DEFAULT_VERIFIER = HERE / "cm2_gate4_round59_cross_fibre_rokhlin_threshold_frontier_verifier.py"

DEPENDENCIES = {
    "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json":
        "d335ea6b9bfdc68c13fa0c44f5f2893af7399546f5951d0cfc156be8b5236ffb",
    "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-manifest-2026-07-20.json":
        "42a035e38687acb4ae1a3ce43a1459c49ba08a1406083c811f919823ecc8d526",
    "cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json":
        "1600a3e060e7ae9601a55d425fbce5a27612300e26e01c77f53158b93010a424",
    "cm2-gate2-round25-product-base-manifest-2026-07-18.json":
        "8045c36fb14c69a145be4ebf4cd33ae11d55fd77f4591b91782f13516c80679b",
    "cm2-gate34-round49-incidence-safe-long-leaf-atlas-manifest-2026-07-19.json":
        "f8117b4d6b91c85597953366bc1eee26652a6ff7c3bd5486d3a3a38694550c18",
}

C_P = Q(4 * 10**90 * 360493663, 358863)
COMMON_MASS = Q(999, 1000)
N_COMPONENTS = C_P.numerator // C_P.denominator + 1
GOOD_Z = Q(1, 1) / COMMON_MASS
BAD_Z = Q(N_COMPONENTS, 1) / COMMON_MASS
TEST_F = 153
TEST_R = Q(2000, 1999)
TEST_THETA = Q(1, 2)
TEST_LENGTH = Q(1, 12800)
TEST_BOUND = Q(TEST_F) * TEST_R / (TEST_THETA * TEST_LENGTH)


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
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"dependency path: {name}")
        require(path.resolve().parent == HERE, f"dependency scope: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        data = strict_json(path.read_text(encoding="utf-8"))
        require(isinstance(data, dict), f"dependency root: {name}")
        loaded[name] = data

    r58 = loaded[
        "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json"
    ]["result"]
    require(
        r58["maximal_component_minimum_Z_theorem"]["status"]
        == "CERTIFIED_MAXIMAL_COMPONENT_EXACT_MINIMUM_AND_UNSHIFTED_PROPERNESS_IFF",
        "Round58 minimum-Z iff",
    )
    require(
        r58["strict_nonpromotion"]["physical_proper_same_ID_first_return_kernel"]
        == "NOT_CERTIFIED",
        "Round58 Gate4 boundary",
    )

    r123 = loaded[
        "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-manifest-2026-07-20.json"
    ]["result"]
    join = r123["gate2"]["gate2_to_gate4_landing_join"]
    require(join["status"] == "CONDITIONAL_JOIN_ONLY", "Round58 conditional join")
    require(len(join["shortest_sufficient_physical_interface"]) == 7, "seven-field list")
    require(r123["gate2"]["official_immutable_fields"] == "0/17", "Gate2 boundary")

    r57 = loaded[
        "cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json"
    ]["result"]
    raw = r57["raw_common_first_return_typing"]
    require(raw["status"] == "CERTIFIED_BUT_UNPROPER", "Round57 raw graph")
    require(
        "immutable positive integer" in raw["Borel_stopping_time"]
        and "countable half-open registry" in raw["Borel_stopping_time"],
        "Round57 Borel time",
    )
    require("is retained" in raw["same_restriction_ID"], "Round57 graph ID")
    require("charged exactly once" in raw["charge"], "Round57 once charge")

    r25 = loaded[
        "cm2-gate2-round25-product-base-manifest-2026-07-18.json"
    ]["result"]
    require(r25["candidate_maturity"]["official_Gate2_maturity"] == "0/17", "Round25 maturity")
    require(
        r25["exact_positive_cone_product_tile"]["affine_candidate_projection"]
        ["identified_with_physical_stable_holonomy_pi_s"] is False,
        "Round25 affine guard",
    )

    r49 = loaded[
        "cm2-gate34-round49-incidence-safe-long-leaf-atlas-manifest-2026-07-19.json"
    ]["result"]
    core = r49["incidence_safe_long_leaf_compact_core"]
    require(core["incidence_safe_piece_count_per_leaf_upper"] == TEST_F, "Round49 F")
    require(core["object_scope"].startswith("conditional per admissible"), "Round49 scope")
    return loaded


def separator_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for m in (2, 10, 1000):
        epsilon = Q(1, m * N_COMPONENTS)
        j_total = (1 - epsilon) + epsilon * N_COMPONENTS
        h_total = COMMON_MASS
        moment = COMMON_MASS * ((1 - epsilon) + 4 * epsilon)
        rows.append(
            {
                "m": m,
                "bad_outer_weight": qstr(epsilon),
                "bad_common_mass": qstr(epsilon * COMMON_MASS),
                "aggregate_J_land_min": qstr(j_total),
                "aggregate_H": qstr(h_total),
                "aggregate_normalized_Z": qstr(j_total / h_total),
                "aggregate_D_land_dyadic_moment": qstr(moment),
                "good_D_land": 0,
                "bad_D_land": 2,
                "bad_fibre_is_proper": False,
            }
        )
    return rows


def pinned_audit() -> dict[str, Any]:
    return {
        "Round58_exact_iff": "within each frozen (y, physical chart, immutable ID), exact unshifted properness iff J_land,min(y)<C_p*h(y)",
        "Round58_available_aggregate": "J_land,min,total<infinity and integral h*2^D_land<infinity",
        "Round58_cross_fibre_scope": "cross-y/cross-chart physical Rokhlin redisintegration was explicitly left outside the same-ID maximal-component theorem",
        "Round58_seven_field_join": "the Gate2-to-Gate4 leaf lists seven sufficient physical fields and certifies only a conditional join",
        "status": "CERTIFIED_PINNED_ROUND58_TYPE_AUDIT",
    }


def aggregate_separator() -> dict[str, Any]:
    rows = separator_rows()
    require(Q(N_COMPONENTS - 1) <= C_P < Q(N_COMPONENTS), "ceiling")
    require(GOOD_Z < C_P < BAD_Z, "good/bad split")
    require(BAD_Z < 2 * C_P, "bad D=2 upper")
    require(Q(2) / COMMON_MASS < C_P, "Dcap zero")
    for row, m in zip(rows, (2, 10, 1000), strict=True):
        eps = Q(1, m * N_COMPONENTS)
        j = 1 + Q(1, m) - Q(1, m * N_COMPONENTS)
        require(row["aggregate_J_land_min"] == qstr(j), "separator J")
        require(j / COMMON_MASS < C_P, "aggregate globally proper")
        require(eps * COMMON_MASS > 0, "positive bad mass")
    return {
        "scope": "exact logical two-fibre standard-family nonimplication model; not asserted to occur in the billiard",
        "ambient_map": "identity first return at time one on two outer fibres; each full unit interval is ambient proper",
        "common_marker_good_fibre": "one interval of mass/length 999/1000 and one gap of length 1/1000, so J_good=1 and z_good=1000/999<C_p",
        "common_marker_bad_fibre": "N=floor(C_p)+1 equal intervals of total mass/length 999/1000 separated by true gaps of total length 1/1000, so J_bad=N and z_bad=1000*N/999>C_p",
        "outer_mixture": "for every integer m>=2 put bad outer weight epsilon_m=1/(mN); the bad common mass is positive",
        "aggregate_identity": "J_total=1+1/m-1/(mN), H=999/1000, and the aggregate normalized boundary tends to 1000/999 as m tends to infinity",
        "dyadic_identity": "D_good=0, D_bad=2 and integral h*2^D=999/1000*(1+3/(mN)), arbitrarily close to 999/1000",
        "reference_identity": "piecewise translation reassembles each marker on a reference interval; two reference views have J_cap=2, z_cap=2000/999<C_p and D_cap=0",
        "strict_conclusion": "even finite and globally proper aggregate J_total/H, an almost-minimal full D_land moment, ambient properness, high common mass and D_cap=0 do not imply J_land,min(y)<C_p*h(y) almost everywhere",
        "N": str(N_COMPONENTS),
        "good_z": qstr(GOOD_Z),
        "bad_z": qstr(BAD_Z),
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_AGGREGATE_AND_DLAND_DYADIC_MOMENT_DO_NOT_IMPLY_FIBREWISE_PROPERNESS",
    }


def same_graph_reconditioning() -> dict[str, Any]:
    return {
        "tagged_branch_space": "the Round57 countable half-open R_n/path/ID registry on which Q_cap(x)=T_s^n x is a regular injective branch map",
        "Borel_inverse_theorem": "on each tagged branch the inverse is T_s^(-n); Lusin-Souslin makes the branch image and inverse Borel, and the countable tagged union is Borel modulo the pinned null cemetery",
        "supplied_partition": "let q:landing->U be a Borel map into a standard-Borel quotient U, hence generating a countably generated Borel partition of the physical landing coordinate; disintegrate the same Gamma_cap over q(landing)",
        "quotient_law": "eta=(q o pr_landing)_#Gamma_cap on U",
        "disintegration_identity": "there is a probability kernel u->Gamma_u, defined eta-almost everywhere, such that Gamma_cap(A)=integral Gamma_u(A)deta(u) for every Borel A; this is not division by the singleton mass eta({u})",
        "conditional_support": "if S is the tagged first-return graph intersected with q(landing)=u, then Gamma_u(S)=1 for eta-almost every u; landing=T_s^n(source) and n/path/ID/owner therefore hold Gamma_u-almost surely, not pointwise for every representative",
        "measure_charge": "the integral identity reassembles exactly the same graph measure Gamma_cap and therefore preserves its once-charge bookkeeping at measure level; it makes no pointwise survival or no-deletion/no-duplication statement for individual raw points",
        "endpoint_and_tag_typing": "source/physical-landing endpoint and tag identities are preserved Gamma_u-almost surely for eta-almost every u; no stable projection is substituted for the landing coordinate",
        "null_set_policy": "the conditional kernel is only eta-almost-everywhere determined; its values on an eta-null quotient set are arbitrary and carry no certified endpoint, tag or normalization statement",
        "what_is_certified": "measure-lossless weak same-graph reconditioning plus the seven-field branch-inverse/semantic row",
        "what_is_not_certified": "the supplied partition is not yet a physical unstable-product partition and its conditional laws are not yet strong proper standard families",
        "status": "CERTIFIED_WEAK_SAME_GRAPH_ROKHLIN_RECONDITIONING_AND_TAGGED_BOREL_BRANCH_INVERSE",
    }


def quantitative_bridge() -> dict[str, Any]:
    require(TEST_BOUND == Q(7_833_600_000, 1999), "test bound arithmetic")
    require(TEST_BOUND < C_P, "test bound margin")
    return {
        "physical_hypotheses": [
            "a countable Borel physical product-rectangle registry whose target fibres are actual unstable plaques of adapted length L(u)>0",
            "the common target conditional is f_u*1_E ds on the same physical landing points and E has at most F(u) connected interval components",
            "ds is the same adapted arclength used in L(u), component lengths and Z, and the retained adapted length satisfies |E|>=theta(u)*L(u)",
            "0<d_-(u)<=f_u<=d_+(u)<=R(u)*d_-(u), with the required log-distortion and Borel bounds",
            "the tagged Borel branch inverse from the certified same-graph theorem and a strong restriction/assembly theorem apply",
        ],
        "boundary_proof": "J_u=sum_C mass(C)/|C|<=F*d_+ while h_u=int_E f_u ds>=d_-*theta*L, hence z_u<=F*R/(theta*L)",
        "strict_sufficient_inequality": "F(u)*R(u)<C_p*theta(u)*L(u) almost everywhere",
        "conclusion": "under the listed physical hypotheses and strict inequality, the original time-n same-point first-return landing is proper; no recovery collision is added and the exact graph/ID/path/once charge are retained",
        "arithmetic_only_replay": {
            "F": TEST_F,
            "R": qstr(TEST_R),
            "theta": qstr(TEST_THETA),
            "L": qstr(TEST_LENGTH),
            "F_R_over_theta_L": qstr(TEST_BOUND),
            "strictly_below_C_p": True,
        },
        "misaligned_field_guard": "the replay deliberately combines a Round49-style F,R with a declared test L,theta only to check magnitude; Round49 is a conditional source compact core and Round25 is an affine candidate rather than the actual common landing product law, so these rows are not physically joinable",
        "status": "CERTIFIED_CONDITIONAL_QUANTITATIVE_PRODUCT_RECTANGLE_TO_PROPER_LANDING_THEOREM",
    }


def seven_field_audit() -> dict[str, Any]:
    rows = [
        {"field": 1, "name": "physical product-rectangle cover of common landing", "actual": "NOT_CERTIFIED"},
        {"field": 2, "name": "stable projection and two-sided Borel holonomy Jacobian", "actual": "NOT_CERTIFIED"},
        {"field": 3, "name": "full-span or quantitatively bounded common fragmentation", "actual": "NOT_CERTIFIED"},
        {"field": 4, "name": "same-measure unstable conditionals with density/log distortion", "actual": "NOT_CERTIFIED"},
        {"field": 5, "name": "physical boundary charge strictly below C_p", "actual": "NOT_CERTIFIED_CONDITIONAL_FORMULA_ONLY"},
        {"field": 6, "name": "Borel branch inverse retaining n/path/ID/owner", "actual": "CERTIFIED_ROUND59"},
        {"field": 7, "name": "strong restriction and assembly", "actual": "NOT_CERTIFIED_WEAK_GRAPH_ASSEMBLY_ONLY"},
    ]
    return {
        "rows": rows,
        "rows_sha256": digest(rows),
        "actual_complete_rows": "1/7",
        "official_Gate2_fields_unchanged": "0/17",
        "shortest_remaining_join": "materialize fields 1--4 and 7 on the actual common landing law and verify F*R<C_p*theta*L; field 6 and the measure-a.e. graph/tag identity need not be reproved",
        "status": "CERTIFIED_SEVEN_FIELD_AUDIT_ONE_SEMANTIC_ROW_COMPLETE_STRONG_PHYSICAL_JOIN_OPEN",
    }


def literature_audit() -> dict[str, Any]:
    return {
        "checked_on": "2026-07-20",
        "official_sources": [
            "arXiv:2604.25881v1, Climenhaga--Day, Every finite horizon Sinai billiard map has a unique measure of maximal entropy",
            "arXiv:2606.10155v1, Demers--Liverani, Recent Progress in the Application of Transfer Operators to Dispersing Billiards",
        ],
        "MME_type_audit": "Definition 2.12 gives local product equivalence for the constructed MME and Lemma 2.14 preserves symbolic Hausdorff leaf measures under symbolic stable holonomy; this is not the pinned Liouville/SRB common landing law",
        "missing_from_MME_source": "no physical common-landing chart, two-sided RN constants for that restricted law, fragmentation/retained-span row, boundary Z<C_p, tagged first-return branch inverse join or strong standard-family assembly",
        "finding": "no checked theorem instantiates the Round58 seven physical fields or proves same-time physical landing properness",
        "external_theorem_promoted": False,
        "status": "AUDITED_MME_LOCAL_PRODUCT_THEOREM_NOT_A_CM2_LANDING_PROPERISATION",
    }


def strict_frontier() -> dict[str, Any]:
    return {
        "physical_J_land_min_total": "CERTIFIED_FINITE_PINNED_ROUND58",
        "physical_D_land_full_dyadic_moment": "CERTIFIED_FINITE_PINNED_ROUND58",
        "fibrewise_J_land_min_below_Cp_h": "NOT_CERTIFIED",
        "aggregate_to_fibrewise_implication": "CERTIFIED_FALSE_BY_POSITIVE_BAD_FIBRE_SEPARATOR",
        "tagged_Borel_first_return_branch_inverse": "CERTIFIED",
        "weak_same_graph_Rokhlin_reconditioning": "CERTIFIED",
        "seven_field_physical_landing_join": "1/7_ACTUAL_STRONG_JOIN_NOT_CERTIFIED",
        "quantitative_product_rectangle_bridge": "CERTIFIED_CONDITIONAL",
        "physical_proper_same_ID_first_return_landing_kernel": "NOT_CERTIFIED",
        "physical_proper_same_ID_first_return_kernel": "NOT_CERTIFIED",
        "intermediate_C24_avoidance_after_proper_landing": "NOT_CERTIFIED",
        "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
        "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
        "strong_singular_current_cemetery": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "parameterwise for every fixed |s|<=1/400",
            "claim_type": "aggregate-to-fibre separator, weak same-graph Rokhlin theorem, branch-inverse row and quantitative physical product bridge",
            "external_theorem_promoted": False,
        },
        "pinned_round58_audit": pinned_audit(),
        "aggregate_to_fibrewise_separator": aggregate_separator(),
        "same_graph_rokhlin_reconditioning": same_graph_reconditioning(),
        "quantitative_product_rectangle_bridge": quantitative_bridge(),
        "seven_field_materialization_audit": seven_field_audit(),
        "latest_technical_literature_audit": literature_audit(),
        "strict_nonpromotion": strict_frontier(),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path = DEFAULT_VERIFIER) -> dict[str, Any]:
    verifier = verifier.resolve()
    require(verifier.is_file() and not verifier.is_symlink(), "verifier path")
    require(verifier.parent == HERE, "verifier outside deliverables")
    require(DEFAULT_REPORT.is_file() and not DEFAULT_REPORT.is_symlink(), "report path")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "dependencies": dict(DEPENDENCIES),
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
        print(f"ROUND59_GATE4_ROKHLIN_CERT_FAILURE: {exc}")
        return 1

    strict = build_result()["strict_nonpromotion"]
    print("BRANCH_INVERSE:", strict["tagged_Borel_first_return_branch_inverse"])
    print("SEVEN_FIELD_JOIN:", strict["seven_field_physical_landing_join"])
    print("PROPER_KERNEL:", strict["physical_proper_same_ID_first_return_kernel"])
    print("GATE4:", strict["Gate4"])
    print("CM2:", strict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
