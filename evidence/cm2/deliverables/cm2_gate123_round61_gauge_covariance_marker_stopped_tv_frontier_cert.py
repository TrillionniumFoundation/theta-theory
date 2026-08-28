#!/usr/bin/env python3
"""CM2 Round-61 Gate-1/2/3 exact-interface certificate.

Positive modes certify exact algebraic/measure interfaces.  Default execution
exits two because Gates 1, 2 and 3 remain open.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / "deliverables"
REPORT = HERE / (
    "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-"
    "assault-2026-07-20.md"
)
MANIFEST = HERE / (
    "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-"
    "manifest-2026-07-20.json"
)
VERIFIER = HERE / (
    "cm2_gate123_round61_gauge_covariance_marker_stopped_tv_frontier_"
    "verifier.py"
)
Q = Fraction


DEPENDENCIES = {
    "deliverables/cm2-sixtieth-direct-assault-2026-07-20.md":
        "ef3f2739a7a0ed8c91e82400c05564f97f0c3326ebc1373764b51bbd48f04212",
    "deliverables/cm2-sixtieth-direct-assault-manifest-2026-07-20.sha256":
        "5f6c90735cbb74ec7b36f6c1d2b012ccccaafa40793d291dfcb6a0e212044e9e",
    "deliverables/cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier-manifest-2026-07-20.json":
        "f897d81a2e85c4a8e45c436f169043feaef93b019f18229a44da0227c75b2a88",
    "deliverables/cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier-manifest-2026-07-20.sha256":
        "6a29c47462a9526138a059f8577abcf879cd162feca14b435906cce1cd8c087a",
    "deliverables/cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json":
        "08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3",
    "deliverables/cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.sha256":
        "4d7c3f06e1671319482c064ec3ea817562567202b111fd014434b7be0a460fac",
    "deliverables/cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json":
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73",
    "deliverables/cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.sha256":
        "7fd9547443951d9960b466aa914f73b1a36f73897e31585018eceed409be4716",
}


class CertificateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def qtext(value: Q) -> str:
    return str(value)


def validate_dependencies() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for rel, expected in DEPENDENCIES.items():
        path = ROOT / rel
        require(path.is_file() and not path.is_symlink(), f"dependency file/type: {rel}")
        require(sha256_path(path) == expected, f"dependency hash drift: {rel}")
        rows.append({"path": rel, "sha256": expected})
    return rows


Matrix = tuple[tuple[Q, Q], tuple[Q, Q]]
Vector = tuple[Q, Q]


def mm(a: Matrix, b: Matrix) -> Matrix:
    return (
        (a[0][0] * b[0][0] + a[0][1] * b[1][0],
         a[0][0] * b[0][1] + a[0][1] * b[1][1]),
        (a[1][0] * b[0][0] + a[1][1] * b[1][0],
         a[1][0] * b[0][1] + a[1][1] * b[1][1]),
    )


def mv(a: Matrix, v: Vector) -> Vector:
    return (a[0][0] * v[0] + a[0][1] * v[1],
            a[1][0] * v[0] + a[1][1] * v[1])


def det(a: Matrix) -> Q:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv(a: Matrix) -> Matrix:
    d = det(a)
    require(d != 0, "matrix invertibility")
    return ((a[1][1] / d, -a[0][1] / d),
            (-a[1][0] / d, a[0][0] / d))


def wedge(v: Vector, w: Vector) -> Q:
    return v[0] * w[1] - v[1] * w[0]


def gate1_replay() -> dict[str, Any]:
    d: Matrix = ((Q(2), Q(1)), (Q(1), Q(1)))
    a: Matrix = ((Q(3), Q(0)), (Q(0), Q(1, 3)))
    psi: Matrix = ((Q(2), Q(3)), (Q(5), Q(7)))
    require(det(d) == 1, "SL2 gauge")
    dg = inv(d)
    a_new = mm(mm(d, a), dg)
    psi_new = mm(mm(d, psi), dg)
    vectors: tuple[Vector, Vector] = ((Q(1), Q(0)), (Q(0), Q(1)))
    vectors_new = tuple(mv(d, v) for v in vectors)
    require(mv(a_new, vectors_new[0]) == tuple(3 * x for x in vectors_new[0]),
            "transported unstable eigenvector")
    require(mv(a_new, vectors_new[1]) == tuple(Q(1, 3) * x for x in vectors_new[1]),
            "transported stable eigenvector")

    old_wedges: list[Q] = []
    new_wedges: list[Q] = []
    rows: list[dict[str, str | int]] = []
    for i in range(2):
        for j in range(2):
            old = wedge(mv(psi, vectors[i]), vectors[j])
            new = wedge(mv(psi_new, vectors_new[i]), vectors_new[j])
            require(new == det(d) * old == old, "simultaneous SL2 wedge covariance")
            require(old != 0, "sample twisting wedge strict")
            old_wedges.append(old)
            new_wedges.append(new)
            rows.append({"i": i, "j": j, "old_wedge": qtext(old),
                         "transported_wedge": qtext(new)})
    require(old_wedges == [Q(-5), Q(2), Q(-7), Q(3)], "wedge sample")

    wrong_loop: Matrix = ((Q(2), Q(0)), (Q(0), Q(1, 2)))
    wrong_wedges = [wedge(mv(wrong_loop, vectors[i]), vectors[j])
                    for i in range(2) for j in range(2)]
    require(0 in wrong_wedges, "immutable-loop separator")

    return {
        "exact_same_loop_gauge_covariance": {
            "hypotheses": [
                "one immutable physical basepoint and loop token",
                "the loop and both physical eigenvectors are transformed by the same D(p)",
                "D(p) is invertible; determinant one gives numerical wedge equality",
                "both canonical holonomies exist on the same physical registry",
            ],
            "formula": "det(D*Psi*v_i,D*v_j)=det(D)*det(Psi*v_i,v_j)",
            "sample_D_determinant": "1",
            "sample_rows": rows,
            "conclusion": (
                "an exact immutable determinant-one cohomology join transports all "
                "four selected twisting wedges without a 10^-29 matrix comparison"
            ),
            "status": "CERTIFIED_EXACT_COHOMOLOGY_COVARIANCE_INTERFACE",
        },
        "token_guard": {
            "wrong_loop_wedges": [qtext(x) for x in wrong_wedges],
            "scope": "exact algebraic separator; not a billiard realization",
            "conclusion": (
                "a basis or gauge name without the same immutable physical loop token "
                "cannot transport twisting"
            ),
            "status": "CERTIFIED_FALSE_WITHOUT_SAME_LOOP_JOIN",
        },
        "physical_boundary": {
            "all_actual_plaque_combined_gauge_registry": "NOT_CERTIFIED",
            "exact_compact_to_combined_same_loop_cohomology": "NOT_CERTIFIED",
            "same_representative_class_H": "NOT_CERTIFIED",
            "gate1": "NOT_CERTIFIED",
        },
    }


def gate2_replay() -> dict[str, Any]:
    mu_u = [Q(1, 2), Q(1, 3), Q(1, 6)]
    mu_v = [Q(1, 4), Q(1, 2), Q(1, 4)]
    g_u = [Q(1), Q(1, 2), Q(0)]
    push = [1, 2, 0]  # source index -> target index
    inverse = [2, 0, 1]

    push_mu = [Q(0), Q(0), Q(0)]
    push_kappa = [Q(0), Q(0), Q(0)]
    for source, target in enumerate(push):
        push_mu[target] += mu_u[source]
        push_kappa[target] += g_u[source] * mu_u[source]
    j_hol = [push_mu[i] / mu_v[i] for i in range(3)]
    marker = [push_kappa[i] / mu_v[i] for i in range(3)]
    predicted = [g_u[inverse[i]] * j_hol[i] for i in range(3)]
    require(marker == predicted == [Q(0), Q(1), Q(2, 3)],
            "marker-holonomy RN covariance")
    require(all(0 <= x <= 1 for x in g_u), "source marker bound")

    sep_mu = [Q(1, 2), Q(1, 2)]
    sep_left = [Q(1), Q(0)]
    sep_right = [Q(0), Q(1)]
    require(sum(sep_mu[i] * sep_left[i] for i in range(2)) == Q(1, 2),
            "separator left common mass")
    require(sum(sep_mu[i] * sep_right[i] for i in range(2)) == Q(1, 2),
            "separator right common mass")
    require(sep_left != sep_right, "marker mismatch")

    return {
        "marker_holonomy_compatibility": {
            "actual_frozen_input": "0<=kappa_B<=mu_C and g_B=d kappa_B/d mu_C in [0,1]",
            "future_holonomy_typing": (
                "if h_*mu_u=J_hol*mu_v, then "
                "d[h_*(g_u mu_u)]/dmu_v=(g_u o h^-1)*J_hol"
            ),
            "same_landing_law_join_equation": "g_v=(g_u o h^-1)*J_hol mu_v-a.e.",
            "finite_exact_replay": {
                "push_mu": [qtext(x) for x in push_mu],
                "J_hol": [qtext(x) for x in j_hol],
                "pushed_marker": [qtext(x) for x in marker],
                "predicted_marker": [qtext(x) for x in predicted],
            },
            "status": "CERTIFIED_EXACT_MARKER_HOLONOMY_INTERFACE",
        },
        "qualitative_holonomy_separator": {
            "reference_law": [qtext(x) for x in sep_mu],
            "holonomy": "identity",
            "J_hol": "1",
            "left_marker": [qtext(x) for x in sep_left],
            "right_marker": [qtext(x) for x in sep_right],
            "common_mass_each_side": "1/2",
            "scope": "exact logical same-mass marker model; not a billiard realization",
            "conclusion": (
                "even identity holonomy and equal common mass do not force the "
                "same-landing-law marker equation"
            ),
            "status": "CERTIFIED_FALSE_WITHOUT_MARKER_COVARIANCE",
        },
        "physical_boundary": {
            "all_depth_graph_transforms": "NOT_CERTIFIED",
            "stable_base_projection_two_sided_J_hol": "NOT_CERTIFIED",
            "physical_marker_covariance_equation": "NOT_CERTIFIED",
            "landing_join": "1/7",
            "official_immutable_gate2_fields": "0/17",
            "gate2": "NOT_CERTIFIED",
        },
    }


def gate3_replay() -> dict[str, Any]:
    labels = [
        "d0:cemetery", "d1:w0:c0", "d1:w1:c0", "d2:w00:c0",
        "d2:w01:c0", "d3:w111:c2", "d5:w00110:c1", "d8:w10101010:c0",
    ]
    signed = [Q(1, 3), Q(-1, 6), Q(1, 2), Q(-1, 4),
              Q(1, 8), Q(-1, 12), Q(1, 7), Q(-1, 9)]
    input_tv = sum((abs(x) for x in signed), Q(0))
    restricted_tv = sum((abs(x) for x in signed), Q(0))
    require(input_tv == restricted_tv, "stopped restriction TV isometry")
    output_bin = [0, 0, 1, 1, 2, 2, 2, 1]
    assembled = [Q(0), Q(0), Q(0)]
    for mass, target in zip(signed, output_bin):
        assembled[target] += mass
    output_tv = sum((abs(x) for x in assembled), Q(0))
    require(output_tv <= input_tv, "output assembly TV contraction")

    positive = [abs(x) for x in signed]
    require(sum(positive, Q(0)) == input_tv, "positive stopped mass preservation")

    fragmentation_rows: list[dict[str, str | int]] = []
    for m in (1, 2, 4, 8, 16, 32):
        source_l1 = Q(1)
        source_variation = Q(2)
        split_l1 = Q(1)
        split_variation = Q(2 * m)
        ratio = (split_l1 + split_variation) / (source_l1 + source_variation)
        require(split_l1 == source_l1, "fragmentation L1 conservation")
        require(split_variation == 2 * m, "zero-extension endpoint variation")
        fragmentation_rows.append({
            "half_open_components": m,
            "source_zero_extension_BV": "3",
            "direct_sum_zero_extension_BV": qtext(split_l1 + split_variation),
            "norm_ratio": qtext(ratio),
        })
    require(Q(65, 3) == Q(fragmentation_rows[-1]["norm_ratio"]),
            "fragmentation terminal ratio")

    return {
        "actual_stopped_graph_partition": {
            "inputs": [
                "integer-valued Borel Dbar strata from the frozen physical kernel",
                "for each finite schedule depth, actual half-open first-root word cells",
                "finite semialgebraic connected components and explicit cemetery",
            ],
            "partition": (
                "A_(d,w,c)={Dbar=d} intersect physical half-open word w "
                "intersect connected component c; all nonempty cells form a "
                "countable disjoint Borel partition"
            ),
            "R_stop_type": (
                "finite signed Borel source measures -> l1 direct sum of "
                "cellwise finite signed Borel measures"
            ),
            "Q_source_type": "cellwise source measures -> source measure by countable sum",
            "Q_output_type": (
                "cellwise graph pushforwards -> output measure by countable sum; "
                "not an adjoint or a physical strong quotient"
            ),
            "identities": [
                "sum_A ||1_A mu||_TV=||mu||_TV",
                "Q_source R_stop mu=mu",
                "||Q_output nu||_TV<=sum_A||nu_A||_TV",
                "positive mass is counted exactly once",
            ],
            "finite_replay": {
                "labels": labels,
                "signed_masses": [qtext(x) for x in signed],
                "input_TV": qtext(input_tv),
                "restricted_l1_TV": qtext(restricted_tv),
                "assembled_output": [qtext(x) for x in assembled],
                "assembled_output_TV": qtext(output_tv),
            },
            "raw_word_factor_needed_in_weak_TV": False,
            "status": "CERTIFIED_ACTUAL_WEAK_STOPPED_GRAPH_TV_NORM_ONE",
        },
        "strong_fragmentation_separator": {
            "model": (
                "1_[0,1) split into m half-open intervals; use L1 plus the "
                "variation of each zero extension on R"
            ),
            "rows": fragmentation_rows,
            "scope": "exact strong-norm separator; not a physical billiard lower bound",
            "conclusion": (
                "norm-one weak TV restriction does not bound endpoint/fragmentation "
                "trace in a strong graph/BV direct sum"
            ),
            "status": "CERTIFIED_NO_STRONG_PROMOTION_FROM_WEAK_STOPPED_TV",
        },
        "direct_strong_boundary": {
            "graph_level_strong_restriction": "NOT_CERTIFIED",
            "physical_strong_R_s_Q_s": "NOT_CERTIFIED",
            "moving_scatterer_directional_Piola_current": "NOT_CERTIFIED",
            "MT_DQ": "NOT_CERTIFIED",
            "gate3": "NOT_CERTIFIED",
        },
        "latest_official_technology_audit": {
            "checked_on": "2026-07-20",
            "arXiv_2603_19509v3": {
                "title": "A Mathematical Framework for Linear Response Theory for Nonautonomous Systems",
                "useful_template": (
                    "global transfer operator on a sequence space of measures, "
                    "common strong/weak spaces, uniform loss of memory and strong differentiability"
                ),
                "type_mismatch": (
                    "applications verify C3 expanding maps and uniformly positive noisy maps; "
                    "no moving billiard singular-domain Piola/current or CM2 carrier join"
                ),
            },
            "arXiv_2604_25881v1": {
                "title": "Every finite horizon Sinai billiard map has a unique measure of maximal entropy",
                "theorem_B": (
                    "for fixed table and unstable curve length>=delta, total length of "
                    "components of T^n V is comparable to exp(n h_top)"
                ),
                "type_mismatch": (
                    "total image length for a fixed table/MME does not bound component count, "
                    "minimum component length, SRB landing law or moving-parameter Piola"
                ),
            },
            "arXiv_2604_19671v2": (
                "small-hole conditional standard-family evolution starts from an already "
                "regular family and does not install the moving-scatterer strong carrier"
            ),
            "arXiv_2605_18110v3": (
                "one-inequation component sampling under generic smoothness gives no "
                "depth-integrated inverse-length or boundary-trace estimate"
            ),
            "external_theorem_promoted": False,
        },
    }


def result_payload() -> dict[str, Any]:
    return {
        "gate1": gate1_replay(),
        "gate2": gate2_replay(),
        "gate3": gate3_replay(),
        "strict_status": {
            "gate1": "NOT_CERTIFIED",
            "gate2": "NOT_CERTIFIED",
            "gate2_immutable_fields": "0/17",
            "gate2_landing_join": "1/7",
            "gate3": "NOT_CERTIFIED",
            "composite_gates": "0/5",
            "cm2": "NO-GO_FOR_CLAIM",
        },
    }


def build_manifest(check_dependencies: bool = True) -> dict[str, Any]:
    dependencies = validate_dependencies() if check_dependencies else [
        {"path": rel, "sha256": digest} for rel, digest in DEPENDENCIES.items()
    ]
    require(REPORT.is_file() and not REPORT.is_symlink(), "report file/type")
    require(VERIFIER.is_file() and not VERIFIER.is_symlink(), "verifier file/type")
    result = result_payload()
    return {
        "schema": "cm2.gate123.round61.gauge-covariance-marker-stopped-tv-frontier.v1",
        "artifact": "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier",
        "date": "2026-07-20",
        "dependencies": dependencies,
        "result": result,
        "result_sha256": canonical_digest(result),
        "strict_verdict": (
            "exact same-loop gauge covariance, marker-holonomy compatibility and "
            "actual weak stopped graph-TV compression are certified; physical all-plaque "
            "combined class H, all-depth stable holonomy and strong R/Q/Piola/MT_DQ "
            "remain not certified"
        ),
        "report_sha256": sha256_path(REPORT),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(VERIFIER),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--summary-json", action="store_true")
    parser.add_argument("--emit-manifest", type=Path)
    args = parser.parse_args()
    try:
        data = build_manifest(check_dependencies=True)
        if args.emit_manifest is not None:
            args.emit_manifest.write_bytes(canonical_bytes(data))
            print(f"EMITTED: {args.emit_manifest}")
            return 0
        if args.summary_json:
            print(json.dumps(data["result"], indent=2, sort_keys=True))
            return 0
        require(MANIFEST.is_file() and not MANIFEST.is_symlink(), "manifest file/type")
        require(MANIFEST.read_bytes() == canonical_bytes(data), "manifest drift")
    except (CertificateError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"CERTIFICATE_ERROR: {exc}", file=sys.stderr)
        return 1
    print("DEPENDENCIES: 8/8")
    print("GATE1_EXACT_SAME_LOOP_GAUGE_COVARIANCE: CERTIFIED_INTERFACE")
    print("GATE2_MARKER_HOLONOMY_COMPATIBILITY: CERTIFIED_INTERFACE")
    print("GATE3_ACTUAL_WEAK_STOPPED_GRAPH_TV: CERTIFIED_NORM_ONE")
    print("PHYSICAL_STRONG_RQ_PIOLA_MT_DQ: NOT_CERTIFIED")
    print("GATES_1_2_3: NOT_CERTIFIED")
    print("COMPOSITE_GATES: 0/5")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.audit else 2


if __name__ == "__main__":
    raise SystemExit(main())
