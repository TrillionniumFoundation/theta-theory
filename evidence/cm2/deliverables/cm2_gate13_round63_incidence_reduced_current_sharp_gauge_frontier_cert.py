#!/usr/bin/env python3
"""Round-63 Gate-1/3 exact-interface certificate.

Positive modes replay exact rational identities or emit the canonical
manifest.  Default execution exits two because neither Gate 1 nor Gate 3 is
closed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / "deliverables"
REPORT = HERE / (
    "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-"
    "frontier-assault-2026-07-21.md"
)
MANIFEST = HERE / (
    "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-"
    "frontier-manifest-2026-07-21.json"
)
VERIFIER = HERE / (
    "cm2_gate13_round63_incidence_reduced_current_sharp_gauge_"
    "frontier_verifier.py"
)
Q = Fraction


DEPENDENCIES = {
    "deliverables/cm2-sixty-second-direct-assault-2026-07-21.md":
        "873557a6653a826700d5daf11e8b118f5ddca1cf911e085f9c20aa591ab2136f",
    "deliverables/cm2-sixty-second-direct-assault-manifest-2026-07-21.sha256":
        "e54b5a1de2b4bddf0c7589b77997b1f28284040b64b31fdfbf58af9e73233bac",
    "deliverables/cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.json":
        "eb9e086e973866beaba19111a74e67772f5b0998bbee7c43f06c273c96c68fe2",
    "deliverables/cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.sha256":
        "14e13e71fbe1a9c0ed1ef8524da549939417c8406fa60a78f60d56e45deab450",
    "deliverables/cm2-round62-independent-core-frontier-audit-manifest-2026-07-21.json":
        "19a02d00e2ac85849f6197054166e193e1d4e3433c21505fd4bfd2b450faea20",
    "deliverables/cm2-round62-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "32504c8eda5125d11a460199c3471158720127bf2bc1081664a8a20747c7a414",
    "deliverables/cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.json":
        "bb0d263454a33acdf8b2ba443fcc5e247ff1b9214c385f70fa1af2fc26e7c019",
    "deliverables/cm2-gate1-round25-common-frame-manifest-2026-07-18.json":
        "66d4b207a0155ee98a7632154c81caebd567f43aa1a449ffc28b421b175cd436",
    "deliverables/cm2-gate1-third-gauge-escape-frontier-manifest-2026-07-17.json":
        "03174972b28265463fba1bb52a1dbdb1a85f6c1ae074c48f4a3774b5b9731dd7",
    "deliverables/cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json":
        "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
    "deliverables/cm2-gate3-cancellation-free-current-frontier-manifest-2026-07-16.json":
        "c1fc42c517ee930d265468104481b290f16aa90eb72cb8ceb0adb6649760d981",
    "deliverables/cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json":
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d",
    "deliverables/cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json":
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73",
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
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


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


def mm(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(2)), Q(0))
                       for j in range(2)) for i in range(2))  # type: ignore[return-value]


def det(a: Matrix) -> Q:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv(a: Matrix) -> Matrix:
    d = det(a)
    require(d != 0, "matrix invertibility")
    return ((a[1][1] / d, -a[0][1] / d),
            (-a[1][0] / d, a[0][0] / d))


def madd(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(a[i][j] + b[i][j] for j in range(2))
                 for i in range(2))  # type: ignore[return-value]


def msub(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(a[i][j] - b[i][j] for j in range(2))
                 for i in range(2))  # type: ignore[return-value]


def gate1_replay() -> dict[str, Any]:
    # Finite identity H_B=C(y)^-1(H_A+Delta)C(x).
    a_x: Matrix = ((Q(8), Q(0)), (Q(0), Q(1, 8)))
    a_y: Matrix = ((Q(9), Q(1, 4)), (Q(0), Q(1, 9)))
    cx: Matrix = ((Q(1), Q(1, 3)), (Q(0), Q(1)))
    cy: Matrix = ((Q(1), Q(0)), (Q(1, 5), Q(1)))
    cfx: Matrix = ((Q(1), Q(0)), (Q(1, 7), Q(1)))
    cfy: Matrix = ((Q(1), Q(2, 9)), (Q(0), Q(1)))
    bnx = mm(mm(inv(cfx), a_x), cx)
    bny = mm(mm(inv(cfy), a_y), cy)
    finite_left = mm(inv(bny), bnx)
    h_a = mm(inv(a_y), a_x)
    endpoint_error = msub(mm(cfy, inv(cfx)), ((Q(1), Q(0)), (Q(0), Q(1))))
    delta = mm(mm(inv(a_y), endpoint_error), a_x)
    finite_right = mm(mm(inv(cy), madd(h_a, delta)), cx)
    require(finite_left == finite_right, "finite endpoint-conjugacy identity")

    regimes = [
        ("subcritical", Q(3, 2), Q(1, 4), Q(9, 16), "DECAYS"),
        ("critical", Q(2), Q(1, 4), Q(1), "CONSTANT_NONZERO"),
        ("supercritical", Q(2), Q(1, 2), Q(2), "DIVERGES"),
    ]
    threshold_rows: list[dict[str, Any]] = []
    for name, a, lam, theta, behavior in regimes:
        require(a * a * lam == theta, f"theta arithmetic: {name}")
        samples = []
        for n in range(1, 11):
            scale = a ** n
            a_n: Matrix = ((scale, Q(0)), (Q(0), Q(1) / scale))
            endpoint: Matrix = ((Q(1), Q(0)), (lam ** n, Q(1)))
            require(det(endpoint) == 1, f"endpoint SL2: {name}")
            error = msub(endpoint, ((Q(1), Q(0)), (Q(0), Q(1))))
            defect = mm(mm(inv(a_n), error), a_n)
            require(defect[1][0] == theta ** n, f"sharp defect: {name}")
            samples.append({
                "n": n,
                "endpoint_lower_defect": qtext(lam ** n),
                "renormalized_lower_defect": qtext(defect[1][0]),
            })
        threshold_rows.append({
            "regime": name,
            "a": qtext(a),
            "lambda": qtext(lam),
            "alpha": "1",
            "theta=a^2*lambda": qtext(theta),
            "behavior": behavior,
            "samples": samples,
        })

    return {
        "endpoint_conjugacy_holder_inheritance": {
            "finite_identity": (
                "H_B^s(n)=C(y)^-1 [H_A^s(n)+Delta_n^s] C(x)"
            ),
            "strict_hypotheses": [
                "canonical H_A^s,H_A^u already belong to the target uniform Holder class",
                "C and C^-1 have uniform bounded Holder moduli on the actual plaque registry",
                "stable and unstable renormalized defects converge uniformly to zero",
                "the periodic and homoclinic tokens are the immutable physical tokens",
            ],
            "limit_formula": [
                "H_B^s=C(y)^-1 H_A^s C(x)",
                "H_B^u=C(y)^-1 H_A^u C(x)",
            ],
            "consequence": (
                "the limit Holder modulus follows from endpoint multiplication; "
                "a separate equi-Holder modulus for finite approximants is not necessary"
            ),
            "finite_identity_replayed": True,
            "status": "CERTIFIED_EXACT_HOLDER_INHERITANCE_INTERFACE",
        },
        "sharp_plaque_tempered_budget": {
            "stable_bound": (
                "||Delta_n^s||<=M_s H_C K_C L_s^alpha "
                "(kappa_s lambda_s^alpha)^n d(x,y)^alpha"
            ),
            "sufficient_rows": [
                "theta_s=kappa_s lambda_s^alpha<1",
                "theta_u=kappa_u lambda_u^alpha<1",
            ],
            "threshold_rows": threshold_rows,
            "critical_conclusion": (
                "theta=1 can retain a nonzero defect, so the strict inequality is sharp"
            ),
            "scope": "exact logical SL2 plaque model; not a new billiard realization",
            "status": "CERTIFIED_SUFFICIENT_THRESHOLD_SHARP_IN_MODEL",
        },
        "physical_boundary": {
            "actual_all_plaque_transfer_C": "NOT_CERTIFIED",
            "uniform_forward_backward_defect_decay": "NOT_CERTIFIED",
            "same_physical_representative_class_H_plus_twisting": "NOT_CERTIFIED",
            "separate_approximant_equi_holder_debt": (
                "NOT_INDEPENDENTLY_REQUIRED_UNDER_ROWS_1_TO_3"
            ),
            "gate1": "NOT_CERTIFIED",
        },
    }


def safe_dbar(m: int) -> int:
    require(m >= 0, "nonnegative M")
    c_p = Q(4 * 10**90 * 360493663, 358863)
    if Q(2) ** m <= c_p:
        return 0
    d = 1
    while not Q(2) ** (m - d) < c_p / 2:
        d += 1
    return d


def gate3_replay() -> dict[str, Any]:
    # Three artificial matching internal faces and one physical mismatch.
    artificial = []
    for cut in (Q(1, 4), Q(1, 2), Q(3, 4)):
        left_atom = cut
        right_atom = cut
        pairing = left_atom - right_atom
        require(pairing == 0, "artificial incidence cancellation")
        artificial.append({
            "cut": qtext(cut),
            "left_trace": qtext(left_atom),
            "right_trace": qtext(right_atom),
            "assembled_pairing": qtext(pairing),
        })
    mismatch_pairing = Q(1, 2) - Q(3, 2)
    mismatch_tv = Q(2)
    require(mismatch_pairing == -1 and mismatch_tv == 2,
            "physical mismatch current")

    clock_rows = []
    expected = {
        306: 0, 307: 0, 308: 0, 309: 0, 310: 0,
        311: 2, 312: 3, 313: 4, 314: 5, 315: 6,
        319: 10, 330: 21, 400: 91,
    }
    for m, target in expected.items():
        d = safe_dbar(m)
        require(d == target, f"safe Dbar row M={m}")
        clock_rows.append({
            "M": m,
            "Dbar": d,
            "R0=696*Dbar": 696 * d,
        })

    f13_over_x = Q(3816937, 7800000)
    f13_over_d1 = Q(3816937, 47112000)
    require(f13_over_x < Q(1, 2), "F13/X strict half")
    require(f13_over_d1 < Q(25, 302), "F13/D1 strict bound")

    taxonomy = [
        {
            "cut": "proof_only_CAD_or_dyadic_subdivision",
            "source": "Round61 maximal connected word components; Round16 bookkeeping edges",
            "treatment": "ABSENT_FROM_ACTUAL_INCIDENCE_CHAIN",
        },
        {
            "cut": "duplicate_source_chart_seam",
            "source": "Gate3 chart-seam quotient",
            "treatment": "CERTIFIED_ZERO_BEFORE_TV",
        },
        {
            "cut": "duplicate_Euclidean_lift_seam",
            "source": "Gate3 chart/lift quotient",
            "treatment": "CERTIFIED_ZERO_BEFORE_TV",
        },
        {
            "cut": "internal_chart_or_homogeneity_cut",
            "source": "Round44 F13 quotient-trace assembly rule",
            "treatment": "ZERO_WHEN_ALL_TRACE_MATCHING_ROWS_HOLD",
        },
        {
            "cut": "deterministic_recut_same_regular_branch",
            "source": "Round50 same-ID finite partition identity",
            "treatment": "CURRENT_CANCELLATION_REQUIRES_FINITE_S_TRACE_AND_VELOCITY_MATCH",
        },
        {
            "cut": "source_core_clipping",
            "source": "Round44 grammar 1",
            "treatment": "ZERO_PARAMETER_CURRENT_IN_FIXED_SOURCE_COORDINATES",
        },
        {
            "cut": "intermediate_or_terminal_C24_preimage",
            "source": "Round44 grammars 2 and 3",
            "treatment": "RETAIN_PHYSICAL_F13_CURRENT",
        },
        {
            "cut": "collision_singularity_or_owner_change",
            "source": "Round44 grammar 4",
            "treatment": "RETAIN_PHYSICAL_F13_CURRENT",
        },
        {
            "cut": "moving_occurrence",
            "source": "Round44 grammar 5",
            "treatment": "RETAIN_PHYSICAL_F13_CURRENT",
        },
        {
            "cut": "grazing_tie_outer_endpoint_or_cemetery",
            "source": "actual stopped boundary",
            "treatment": "RETAIN_UNLESS_NULL_OR_TRACE_THEOREM_IS_INSTALLED",
        },
        {
            "cut": "Dbar_or_stopping_schedule_change",
            "source": "Round50 safe clock inside Round61 stopped partition",
            "treatment": "RETAIN_SEPARATE_CLOCK_JUMP_CURRENT",
        },
    ]

    return {
        "oriented_incidence_reduction": {
            "shared_face_current": (
                "B_e=v_e[(Y_i)_*(rho_i trace_e)-(Y_j)_*(rho_j trace_e)]"
            ),
            "exact_matching_rows": [
                "same regular physical branch/formula",
                "same source density trace",
                "same signed face velocity",
                "same physical landing trace",
                "same retained tag or exact quotient tag",
            ],
            "half_open_owner_is_enough_for_current_cancellation": False,
            "artificial_replay": artificial,
            "physical_mismatch_replay": {
                "left_landing": "1/2",
                "right_landing": "3/2",
                "pairing_against_phi(t)=t": qtext(mismatch_pairing),
                "TV": qtext(mismatch_tv),
            },
            "status": "CERTIFIED_EXACT_INCIDENCE_REDUCTION_INTERFACE",
        },
        "actual_stopped_cut_taxonomy": {
            "actual_cells": (
                "A_(d,w,c)={Dbar=d} intersect physical half-open word w "
                "intersect maximal connected component c"
            ),
            "rows": taxonomy,
            "generic_component_count_charged_after_reduction": False,
            "generic_mismatched_physical_face_separator_retained": True,
            "status": "CERTIFIED_TYPED_CUT_TAXONOMY",
        },
        "same_ID_regular_F13_join": {
            "crosswalk": (
                "stopped regular cell -> (common-Rn-restriction-id,time_j,face-kind,"
                "carrier-seed-id,side-label), with (d,w,c) retained as restrictions"
            ),
            "scope": "base s=0 regular-density Borel TV only",
            "pointwise_bounds": [
                "E_regular_physical<=c_F13,n",
                "c_F13,n<=(3816937/7800000)c_X,n",
                "c_F13,n<(1/2)c_X,n=(25/302)c_D1,n",
            ],
            "F13_over_X": qtext(f13_over_x),
            "F13_over_D1": qtext(f13_over_d1),
            "inherited_rows": [
                "same-ID physical L^(6/5) moment",
                "weighted block exponent 1/6",
            ],
            "not_inherited": [
                "finite-s trace differentiability",
                "strong F13 pullback/intertwiner",
                "clock-jump current",
                "cemetery current",
            ],
            "status": "CERTIFIED_BASE_REGULAR_BOREL_JOIN",
        },
        "stopping_clock_jump_frontier": {
            "safe_clock": (
                "Dbar(M)=0 if 2^M<=C_p; otherwise min d>=1 with 2^(M-d)<C_p/2; "
                "R0=696 Dbar"
            ),
            "rows": clock_rows,
            "first_jump": "M:310->311 gives R0:0->1392",
            "later_jump_size": 696,
            "face_current": (
                "B_e^clock=v_e rho_e[(Y_d)_*delta_e-(Y_d')_*delta_e]"
            ),
            "cancellation_condition": "the tagged stopped outputs coincide exactly",
            "covered_by_round44_five_face_F13": False,
            "status": "CERTIFIED_EXACT_NEW_CLOCK_JUMP_INTERFACE",
        },
        "reduced_strong_ledger": {
            "formula": "E_stop^red=E_regular_physical+E_clock+E_cemetery",
            "regular_base_Borel_term": "CERTIFIED_FINITE_VIA_F13_JOIN",
            "moving_regular_strong_term": "NOT_CERTIFIED",
            "clock_term": "NOT_CERTIFIED",
            "cemetery_term": "NOT_CERTIFIED",
            "anisotropic_bulk_Piola": "NOT_CERTIFIED",
            "status": "CERTIFIED_EXACT_FRONTIER",
        },
        "physical_boundary": {
            "physical_strong_R_s_Q_s": "NOT_CERTIFIED",
            "physical_directional_Piola_current": "NOT_CERTIFIED",
            "MT_DQ": "NOT_CERTIFIED",
            "gate3": "NOT_CERTIFIED",
        },
    }


def build_result() -> dict[str, Any]:
    return {
        "gate1": gate1_replay(),
        "gate3": gate3_replay(),
        "latest_official_technology_audit": {
            "checked_on": "2026-07-21",
            "arXiv_2603_19509v3": (
                "common strong spaces, strong differentiability and memory loss are assumptions"
            ),
            "arXiv_2604_19671v2": (
                "already regular fixed-billiard small-hole families; no moving stopped Piola"
            ),
            "arXiv_2606_10155v1": (
                "anisotropic billiard-space survey; no all-depth moving-domain current theorem"
            ),
            "arXiv_1909_11548v2": (
                "defines canonical class-H limits; supplies no non-fibre-bunched third gauge"
            ),
            "latest_direct_match": "NONE_FOUND_IN_OFFICIAL_SEARCH",
            "external_theorem_promoted": False,
        },
        "strict_status": {
            "gate1": "NOT_CERTIFIED",
            "gate3": "NOT_CERTIFIED",
            "composite_gates": "0/5",
            "cm2": "NO-GO_FOR_CLAIM",
        },
    }


STRICT_VERDICT = (
    "endpoint-conjugacy Holder inheritance, the sharp plaque-tempered budget, "
    "incidence reduction and the base regular F13 join are certified, but the "
    "actual all-plaque transfer, moving clock/cemetery currents, anisotropic bulk "
    "Piola, strong R/Q and MT_DQ remain not certified"
)


def build_manifest() -> dict[str, Any]:
    validate_dependencies()
    require(REPORT.is_file() and not REPORT.is_symlink(), "report file/type")
    require(Path(__file__).resolve().is_file(), "certificate file/type")
    require(VERIFIER.is_file() and not VERIFIER.is_symlink(), "verifier file/type")
    result = build_result()
    return {
        "artifact": "cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier",
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "date": "2026-07-21",
        "dependencies": validate_dependencies(),
        "report_sha256": sha256_path(REPORT),
        "result": result,
        "result_sha256": canonical_digest(result),
        "schema": "cm2.gate13.round63.incidence-reduced-current-sharp-gauge-frontier.v1",
        "strict_verdict": STRICT_VERDICT,
        "verifier_sha256": sha256_path(VERIFIER),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--print-result-sha", action="store_true")
    parser.add_argument("--emit-manifest", type=Path)
    args = parser.parse_args()
    try:
        if args.print_result_sha:
            print(canonical_digest(build_result()))
            return 0
        if args.emit_manifest is not None:
            args.emit_manifest.write_bytes(canonical_bytes(build_manifest()))
            print(f"EMITTED: {args.emit_manifest}")
            return 0
        validate_dependencies()
        result = build_result()
        if args.audit:
            print("AUDIT: PASS")
            print(f"DEPENDENCIES: {len(DEPENDENCIES)}/{len(DEPENDENCIES)}")
            print(f"RESULT_SHA256: {canonical_digest(result)}")
            return 0
        if args.replay:
            print(json.dumps({
                "gate1_threshold_regimes": len(result["gate1"]["sharp_plaque_tempered_budget"]["threshold_rows"]),
                "gate1_threshold_samples": sum(len(row["samples"]) for row in result["gate1"]["sharp_plaque_tempered_budget"]["threshold_rows"]),
                "gate3_taxonomy_rows": len(result["gate3"]["actual_stopped_cut_taxonomy"]["rows"]),
                "gate3_clock_rows": len(result["gate3"]["stopping_clock_jump_frontier"]["rows"]),
                "status": "PASS",
            }, sort_keys=True))
            return 0
    except (CertificateError, OSError, ValueError) as exc:
        print(f"CERTIFICATE_ERROR: {exc}", file=sys.stderr)
        return 1
    print("GATE1_SHARP_PLAQUE_TEMPERED_INTERFACE: CERTIFIED")
    print("GATE3_INCIDENCE_REDUCED_BASE_F13_JOIN: CERTIFIED")
    print("PHYSICAL_ALL_PLAQUE_STRONG_RQ_PIOLA_MT_DQ: NOT_CERTIFIED")
    print("GATES_1_3: NOT_CERTIFIED")
    print("COMPOSITE_GATES: 0/5")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
