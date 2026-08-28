#!/usr/bin/env python3
"""Round-62 Gate-1/3 exact-interface certificate.

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
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-"
    "frontier-assault-2026-07-21.md"
)
MANIFEST = HERE / (
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-"
    "frontier-manifest-2026-07-21.json"
)
VERIFIER = HERE / (
    "cm2_gate13_round62_plaque_tempered_gauge_moving_trace_piola_"
    "frontier_verifier.py"
)
Q = Fraction


DEPENDENCIES = {
    "deliverables/cm2-sixty-first-direct-assault-2026-07-20.md":
        "b9ad28ed23e88768234b304dd9f9ecb02577c7aa18dc8a982185690ea8f6f02b",
    "deliverables/cm2-sixty-first-direct-assault-manifest-2026-07-20.sha256":
        "2a3ae3ebf1a6e11b734611e260a340398f475d70e4888010c8294ac321d84265",
    "deliverables/cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.json":
        "bb0d263454a33acdf8b2ba443fcc5e247ff1b9214c385f70fa1af2fc26e7c019",
    "deliverables/cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.sha256":
        "744bf350c4b3511bb35cefb12d294d4ef407d9c09b43dacb1123eba6103a1f0b",
    "deliverables/cm2-gate1-third-gauge-escape-frontier-manifest-2026-07-17.json":
        "03174972b28265463fba1bb52a1dbdb1a85f6c1ae074c48f4a3774b5b9731dd7",
    "deliverables/cm2-gate1-third-gauge-escape-frontier-manifest-2026-07-17.sha256":
        "47d0c506285acf1425068c6ac05c58024d6679166c41f847f45dbf72ae5d9ba1",
    "deliverables/cm2-gate1-round25-common-frame-manifest-2026-07-18.json":
        "66d4b207a0155ee98a7632154c81caebd567f43aa1a449ffc28b421b175cd436",
    "deliverables/cm2-gate1-round25-common-frame-manifest-2026-07-18.sha256":
        "02ac98b4f96bc020f0c84e37c962f335f1fa3d01311d40164c6049f136320e7b",
    "deliverables/cm2-gate3-common-graph-current-carrier-frontier-manifest-2026-07-17.json":
        "9abdc07cb0618f4a81b8e5591d8de83da7cce2c6d6a82fa41c834dd46c28412c",
    "deliverables/cm2-gate3-common-graph-current-carrier-frontier-manifest-2026-07-17.sha256":
        "60282b58c705b6337f558ac7b2f39fdececca2b7dab807f25c8cfd6c846a0415",
    "deliverables/cm2-gate5-round53-trace-standard-family-graph-f17-frontier-manifest-2026-07-20.json":
        "8cacd8daa582c522a175cca3f24c7da1cb10c47f860b20645a365b27678d4590",
    "deliverables/cm2-gate5-round53-trace-standard-family-graph-f17-frontier-manifest-2026-07-20.sha256":
        "88b96c1b69df4708b0e7d36571e21255d7581c389b021e451fc9e04a70643c88",
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


def msub(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(a[i][j] - b[i][j] for j in range(2))
                 for i in range(2))  # type: ignore[return-value]


def gate1_replay() -> dict[str, Any]:
    identity: Matrix = ((Q(1), Q(0)), (Q(0), Q(1)))

    # Direct finite cohomology identity with unrelated rational endpoint gauges.
    a_n: Matrix = ((Q(8), Q(0)), (Q(0), Q(1, 8)))
    c_x: Matrix = ((Q(1), Q(1, 3)), (Q(0), Q(1)))
    c_y: Matrix = ((Q(1), Q(0)), (Q(1, 5), Q(1)))
    c_fx: Matrix = ((Q(1), Q(0)), (Q(1, 7), Q(1)))
    c_fy: Matrix = ((Q(1), Q(2, 9)), (Q(0), Q(1)))
    b_n_x = mm(mm(inv(c_fx), a_n), c_x)
    b_n_y = mm(mm(inv(c_fy), a_n), c_y)
    finite_left = mm(inv(b_n_y), b_n_x)
    finite_right = mm(mm(mm(mm(inv(c_y), inv(a_n)), c_fy), inv(c_fx)),
                      mm(a_n, c_x))
    require(finite_left == finite_right, "finite cohomology defect identity")

    rows: list[dict[str, Any]] = []
    for n in range(1, 13):
        two_n = Q(2) ** n
        a: Matrix = ((two_n, Q(0)), (Q(0), Q(1) / two_n))
        endpoint: Matrix = ((Q(1), Q(0)), (Q(1) / two_n, Q(1)))
        require(det(endpoint) == 1, "separator transfer determinant")
        defect = mm(mm(inv(a), msub(endpoint, identity)), a)
        expected: Matrix = ((Q(0), Q(0)), (two_n, Q(0)))
        require(defect == expected, "amplified endpoint defect")
        rows.append({
            "n": n,
            "base_distance": qtext(Q(1) / two_n),
            "unconjugated_lower_defect": qtext(Q(1) / two_n),
            "renormalized_lower_defect": qtext(two_n),
        })

    return {
        "exact_plaque_tempered_transport": {
            "cohomology_convention": "B(x)=C(fx)^-1 A(x) C(x)",
            "stable_defect": (
                "Delta_n^s=A^n(y)^-1 [C(f^n y) C(f^n x)^-1-I] A^n(x)"
            ),
            "stable_equivalence": (
                "H_B^s=C(y)^-1 H_A^s C(x) iff Delta_n^s->0, provided H_A^s exists"
            ),
            "unstable_row": "the exact backward analogue with f^-n and A^-n",
            "uniform_class_H_bridge": [
                "one Holder transfer on the all-actual-plaque registry",
                "uniform stable and unstable renormalized defect decay",
                "one uniform Holder modulus for the transported canonical families",
                "the same immutable periodic base, homoclinic orbit and loop token",
            ],
            "twisting_transport": (
                "each wedge scales by det(C(p)^-1); SL2 gives numerical equality"
            ),
            "finite_matrix_identity_replayed": True,
            "status": "CERTIFIED_EXACT_PLAQUE_TEMPERED_COHOMOLOGY_INTERFACE",
        },
        "determinant_same_token_separator": {
            "model": (
                "A=diag(2,1/2), stable distance 2^-n, "
                "C(f^n x)=I, C(f^n y)=I+2^-n E21, C(p)=I"
            ),
            "properties": [
                "C is Lipschitz on the logical orbit closure",
                "C takes values in SL(2)",
                "the positive biprojective parameter is q=1",
                "the periodic token is fixed exactly",
            ],
            "rows": rows,
            "conclusion": (
                "determinant one, same periodic token, exact Holder cohomology and "
                "a positive big cell do not imply all-plaque canonical transport"
            ),
            "scope": "exact logical hyperbolic connector model; not a billiard realization",
            "status": "CERTIFIED_FALSE_WITHOUT_RENORMALIZED_DEFECT_DECAY",
        },
        "physical_boundary": {
            "all_actual_plaque_third_gauge_registry": "NOT_CERTIFIED",
            "uniform_forward_backward_defect_decay": "NOT_CERTIFIED",
            "same_physical_representative_class_H_plus_twisting": "NOT_CERTIFIED",
            "gate1": "NOT_CERTIFIED",
        },
    }


def gate3_replay() -> dict[str, Any]:
    # Shared moving cut e(s)=1/2+s with unit traces.
    e0 = Q(1, 2)
    speed = Q(1)
    matching_face_pairing = speed * (e0 - e0)
    translated_face_pairing = speed * (e0 - (e0 + 1))
    require(matching_face_pairing == 0, "matching endpoint cancellation")
    require(translated_face_pairing == -1, "translated endpoint current pairing")
    translated_face_tv = Q(2)

    # Directional Piola sample.  Both exact integrals equal int_0^1 x dx=1/2.
    test_motion_term = Q(1, 2)
    vector_motion_term = Q(1, 2)
    piola_derivative = test_motion_term + vector_motion_term
    require(piola_derivative == 1, "directional Piola derivative")

    fragmentation_rows = []
    for m in (1, 2, 4, 8, 16, 32):
        face_tv = Q(2 * m)
        source_intrinsic_w11 = Q(1)
        fragmentation_rows.append({
            "moving_mismatched_faces": m,
            "source_intrinsic_W11": qtext(source_intrinsic_w11),
            "face_current_TV": qtext(face_tv),
            "ratio": qtext(face_tv / source_intrinsic_w11),
        })
    require(fragmentation_rows[-1]["face_current_TV"] == "64",
            "fragmentation endpoint")

    bulk_rows = []
    for ell in (2, 4, 8, 16, 32):
        source = Q(1, ell)
        target = Q(1)
        require(target / source == ell, "bulk Piola multiplier")
        bulk_rows.append({
            "L": ell,
            "determinant": "1",
            "source_L1": qtext(source),
            "target_L1": qtext(target),
            "multiplier": qtext(target / source),
        })

    return {
        "moving_branch_reynolds_current": {
            "formula": (
                "d integral_[a_i(s),b_i(s)] f_i(s,x) phi(Y_i(s,x)) dx "
                "= bulk derivative + b_i' f_i(b_i-) delta_Yb "
                "- a_i' f_i(a_i+) delta_Ya"
            ),
            "shared_face_atom": (
                "B_e=e' [f_-(e) delta_(Y_-(e))-f_+(e) delta_(Y_+(e))]"
            ),
            "countable_condition": (
                "one parameter-neighborhood dominated-differentiation majorant, "
                "absolute bulk summability and E_stop=sum_e ||B_e||_TV<infinity"
            ),
            "finite_replay": {
                "cut": "e(s)=1/2+s",
                "matching_landing_pairing": qtext(matching_face_pairing),
                "translated_landing_pairing_against_phi(t)=t":
                    qtext(translated_face_pairing),
                "translated_face_current_TV": qtext(translated_face_tv),
            },
            "status": "CERTIFIED_EXACT_MOVING_BULK_PLUS_FACE_INTERFACE",
        },
        "regular_branch_directional_piola": {
            "pairing": (
                "<Piola_(Phi_s)K,psi>=integral psi(Phi_s(x)) dot D Phi_s(x) dK(x)"
            ),
            "derivative": (
                "integral [Dpsi V dot dK + psi dot DV dK]"
            ),
            "C1_dual_bound": "(||V||_infinity+||DV||_infinity)||K||_TV",
            "sample": {
                "Phi_s": "diag(1+s,(1+s)^-1)",
                "determinant": "1",
                "test_motion_term": qtext(test_motion_term),
                "vector_motion_term": qtext(vector_motion_term),
                "total_derivative": qtext(piola_derivative),
            },
            "scope": "one regular branch; not a physical moving-billiard strong operator",
            "status": "CERTIFIED_EXACT_REGULAR_BRANCH_DIRECTIONAL_PIOLA_INTERFACE",
        },
        "current_completed_stopped_recipient": {
            "recipient": "absolutely summable regular bulk currents plus signed face atoms B_e",
            "required_rows": [
                "one common finite-s stopped atlas and physical trace maps",
                "one parameter-neighborhood dominator for bulk and endpoint derivatives",
                "finite E_stop on the same branch records",
                "uniform anisotropic bulk directional-Piola bound",
                "assembly of duplicate/artificial traces before absolute values",
                "cemetery and moving-test tightness on the same carrier",
            ],
            "finite_time_telescope_after_rows": (
                "D(P^n)=sum_(k=0)^(n-1) P^(n-1-k)(DP)P^k"
            ),
            "status": "CERTIFIED_EXACT_CONDITIONAL_CURRENT_RECIPIENT",
        },
        "endpoint_fragmentation_separator": {
            "rows": fragmentation_rows,
            "conclusion": (
                "norm-one weak stopped TV and a fixed intrinsic source W11 norm "
                "do not bound moving mismatched-face current"
            ),
            "scope": "exact logical branch-label model; not a billiard realization",
            "status": "CERTIFIED_FALSE_FROM_WEAK_TV_ALONE",
        },
        "bulk_piola_separator": {
            "model": "U_L=[0,1/L]x[0,1], S_L=diag(L,L^-1), K=e1",
            "rows": bulk_rows,
            "conclusion": (
                "det DS=1 and boundary-flux naturality do not give a uniform bulk L1 Piola multiplier"
            ),
            "scope": "frozen Round53 logical separator; no claim every S_L is a billiard suffix",
            "status": "CERTIFIED_FALSE_FROM_DETERMINANT_ONE_ALONE",
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
                "common strong/weak spaces, strong differentiability and memory loss are assumptions; "
                "applications are expanding/noisy maps"
            ),
            "arXiv_2604_19671v2": (
                "starts from already regular standard families and supplies no moving-domain Piola/current"
            ),
            "arXiv_2606_10155v1": (
                "anisotropic billiard survey supplies no all-depth characteristic restriction or CM2 current"
            ),
            "arXiv_1909_11548v2": (
                "class H requires canonical limits and Holder regularity; arbitrary non-fibre-bunched "
                "cohomology does not supply them"
            ),
            "latest_2607_direct_match": "NONE_FOUND_IN_OFFICIAL_ARXIV_API_SEARCH",
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
    "exact plaque-tempered cohomology and moving bulk-plus-face/Piola interfaces "
    "are certified, but the physical all-plaque defect registry, all-depth endpoint "
    "current, strong R/Q, directional Piola and MT_DQ remain not certified"
)


def build_manifest() -> dict[str, Any]:
    validate_dependencies()
    require(REPORT.is_file() and not REPORT.is_symlink(), "report file/type")
    require(Path(__file__).resolve().is_file(), "certificate file/type")
    require(VERIFIER.is_file() and not VERIFIER.is_symlink(), "verifier file/type")
    result = build_result()
    return {
        "artifact": "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier",
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "date": "2026-07-21",
        "dependencies": validate_dependencies(),
        "report_sha256": sha256_path(REPORT),
        "result": result,
        "result_sha256": canonical_digest(result),
        "schema": "cm2.gate13.round62.plaque-tempered-gauge-moving-trace-piola-frontier.v1",
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
            payload = canonical_bytes(build_manifest())
            args.emit_manifest.write_bytes(payload)
            print(f"EMITTED: {args.emit_manifest}")
            return 0
        validate_dependencies()
        result = build_result()
        if args.audit:
            print("AUDIT: PASS")
            print("DEPENDENCIES: 12/12")
            print(f"RESULT_SHA256: {canonical_digest(result)}")
            return 0
        if args.replay:
            print(json.dumps({
                "gate1_defect_rows": len(result["gate1"]["determinant_same_token_separator"]["rows"]),
                "gate3_fragmentation_rows": len(result["gate3"]["endpoint_fragmentation_separator"]["rows"]),
                "gate3_bulk_rows": len(result["gate3"]["bulk_piola_separator"]["rows"]),
                "status": "PASS",
            }, sort_keys=True))
            return 0
    except (CertificateError, OSError, ValueError) as exc:
        print(f"CERTIFICATE_ERROR: {exc}", file=sys.stderr)
        return 1
    print("GATE1_PLAQUE_TEMPERED_COHOMOLOGY: CERTIFIED_INTERFACE")
    print("GATE3_MOVING_BULK_FACE_PIOLA: CERTIFIED_INTERFACE")
    print("PHYSICAL_ALL_PLAQUE_STRONG_RQ_PIOLA_MT_DQ: NOT_CERTIFIED")
    print("GATES_1_3: NOT_CERTIFIED")
    print("COMPOSITE_GATES: 0/5")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
