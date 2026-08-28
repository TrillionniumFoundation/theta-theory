#!/usr/bin/env python3
"""Round-64 Gate-1/3 one-cross-term and dyadic-clock certificate.

Positive modes audit/replay, verify an existing canonical manifest, or emit
the deterministic manifest.  Default execution exits two because neither
Gate 1 nor Gate 3 is closed.
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
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-"
    "assault-2026-07-21.md"
)
MANIFEST = HERE / (
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-"
    "manifest-2026-07-21.json"
)
VERIFIER = HERE / (
    "cm2_gate13_round64_one_cross_term_dyadic_clock_frontier_verifier.py"
)
Q = Fraction


DEPENDENCIES = {
    "deliverables/cm2-sixty-third-direct-assault-2026-07-21.md":
        "9cde412ba689be87d777906404c9c9426a2a8a102385a2c4c510df8f9b7a6a05",
    "deliverables/cm2-sixty-third-direct-assault-manifest-2026-07-21.sha256":
        "a0b512f32914ef2692b31466a4ea156c44698b1eaf44d8ead45b2c74ee73230e",
    "deliverables/cm2-round63-independent-core-frontier-audit-2026-07-21.md":
        "b30aff208e9e5707e443f59abd07507f7f9d93d765ecaf3fd675f4150c5bf978",
    "deliverables/cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.json":
        "3aae6d018fc15aaab47116d311eed8333c56b87542b0b5761b849221cbf76d6b",
    "deliverables/cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "8227dd32e36d2879f9dbbdced54f3c50b3eac1536ce8fceac480d22cb8617bfd",
    "deliverables/cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-assault-2026-07-21.md":
        "c6429e3b52a5af4af59ea1beccd02d9410a7bdee7a8abc05885d00978f99942d",
    "deliverables/cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-manifest-2026-07-21.json":
        "bdd351955c4537e649009e753900a7f61e3befcc16db55f810af2902dd3581ea",
    "deliverables/cm2-gate13-round63-incidence-reduced-current-sharp-gauge-frontier-manifest-2026-07-21.sha256":
        "b48def6d29a68f9cf30db2b349a41e06b3e5df58766f8d9323e256f75c6ad058",
    "deliverables/cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.json":
        "dacbae6255707086bc7486e4933d8c890ede1547a9e545995800a5fc18698f83",
    "deliverables/cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.sha256":
        "9d98591462771a9e553dd93c24518642c22aa2832c269a8380bd827a76666200",
    "deliverables/cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json":
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73",
    "deliverables/cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.sha256":
        "7fd9547443951d9960b466aa914f73b1a36f73897e31585018eceed409be4716",
    "deliverables/cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json":
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d",
    "deliverables/cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.sha256":
        "07dc2b60d6b8003f0fa3ed7bd7a69167777e8a78958811169caff847ac31480c",
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
    return (json.dumps(value, indent=2, sort_keys=True,
                       ensure_ascii=False) + "\n").encode()


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
        require(path.is_file() and not path.is_symlink(),
                f"dependency file/type: {rel}")
        require(sha256_path(path) == expected,
                f"dependency hash drift: {rel}")
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


def green_matrix(u: Q, v: Q) -> Matrix:
    return ((1 + v * u, v), (u, Q(1)))


def gate1_replay() -> dict[str, Any]:
    # Exact U_v L_u relative-matrix identity at a generic rational row.
    ux, uy = Q(2, 7), Q(5, 11)
    vx, vy = Q(3, 5), Q(-4, 9)
    du, dv = uy - ux, vy - vx
    left = mm(green_matrix(uy, vy), inv(green_matrix(ux, vx)))
    right: Matrix = (
        (1 + vy * du, dv - vy * du * vx),
        (du, 1 - du * vx),
    )
    require(det(green_matrix(ux, vx)) == 1, "D_x in SL2")
    require(det(green_matrix(uy, vy)) == 1, "D_y in SL2")
    require(left == right and det(right) == 1, "relative Green identity")

    regimes = [
        ("subcritical_decay", Q(1, 2), Q(1, 4), Q(1, 2),
         "positive", "DECAYS_TO_ZERO"),
        ("critical_constant", Q(1, 4), Q(1, 4), Q(1),
         "positive", "CONVERGES_NONZERO"),
        ("critical_oscillatory", Q(1, 4), Q(1, 4), Q(1),
         "alternating", "NO_LIMIT"),
        ("supercritical", Q(1, 4), Q(1, 2), Q(2),
         "positive", "UNBOUNDED"),
    ]
    regime_rows: list[dict[str, Any]] = []
    for name, rho, lam_alpha, q, pattern, behavior in regimes:
        require(lam_alpha / rho == q, f"cross ratio: {name}")
        samples = []
        for n in range(1, 11):
            sign = -1 if pattern == "alternating" and n % 2 else 1
            delta_u = sign * lam_alpha ** n
            d_x = green_matrix(Q(0), Q(1))
            d_y = green_matrix(delta_u, Q(1))
            relative = mm(d_y, inv(d_x))
            expected_relative: Matrix = (
                (1 + delta_u, -delta_u),
                (delta_u, 1 - delta_u),
            )
            require(relative == expected_relative and det(relative) == 1,
                    f"SL2 endpoint relative row: {name}/{n}")
            scalar = delta_u / (rho ** n)
            expected_scalar = sign * q ** n
            require(scalar == expected_scalar,
                    f"renormalized scalar cross term: {name}/{n}")
            samples.append({
                "D_y_D_x_inverse_upper_cross_coordinate": qtext(-delta_u),
                "T_n": qtext(scalar),
                "delta_u_n": qtext(delta_u),
                "n": n,
            })
        regime_rows.append({
            "behavior": behavior,
            "lambda_u_to_alpha": qtext(lam_alpha),
            "name": name,
            "pattern": pattern,
            "q_cross": qtext(q),
            "rho_star": qtext(rho),
            "samples": samples,
        })

    return {
        "exact_one_cross_term_reduction": {
            "chosen_gauge": "D=U_v L_u=[[1+vu,v],[u,1]]",
            "relative_matrix": (
                "D_y D_x^-1=[[1+v_y du,dv-v_y du v_x],"
                "[du,1-du v_x]]"
            ),
            "remaining_scalar": (
                "T_n=R_n^-1 v(sigma^-n y)"
                "[u(sigma^-n y)-u(sigma^-n x)]v(sigma^-n x)"
            ),
            "class_H_requirement": (
                "uniform plaque convergence of T_n with a uniform Holder modulus; "
                "the limit need not be zero"
            ),
            "zero_limit_consequence": (
                "exact join of the two frozen one-sided canonical families"
            ),
            "generic_rational_identity_replayed": True,
            "scope": "pinned finite clean physical SFT; not full-mass PPE",
            "status": "CERTIFIED_EXACT_ONE_CROSS_TERM_REDUCTION_ON_CLEAN_SFT",
        },
        "sharp_scalar_budget": {
            "hypotheses": [
                "abs(R_n)>=rho_star^n",
                "abs(v)<=V",
                "abs(u(sigma^-n y)-u(sigma^-n x))"
                "<=H_u lambda_u^(alpha n)d(x,y)^alpha",
            ],
            "bound": (
                "abs(T_n)<=V^2 H_u"
                "(lambda_u^alpha/rho_star)^n d(x,y)^alpha"
            ),
            "sufficient_row": "q_cross=lambda_u^alpha/rho_star<1",
            "regime_rows": regime_rows,
            "critical_boundary": (
                "q_cross=1 permits both a nonzero convergent sequence and an "
                "oscillatory nonconvergent sequence"
            ),
            "necessity_claimed_for_class_H": False,
            "status": "CERTIFIED_CONDITIONAL_BUDGET_SHARP_FOR_AUTOMATIC_DECAY",
        },
        "physical_boundary": {
            "actual_numeric_q_cross_less_than_one": "NOT_CERTIFIED",
            "actual_uniform_holder_limit_of_T_n": "NOT_CERTIFIED",
            "selected_twisting_in_same_combined_representative": "NOT_CERTIFIED",
            "compact_to_third_plaque_tempered_transport": "NOT_CERTIFIED",
            "full_mass_physical_PPE": "NOT_CERTIFIED",
            "gate1": "NOT_CERTIFIED",
        },
    }


C_P = Q(4 * 10**90 * 360493663, 358863)


def safe_dbar(m: int) -> int:
    require(type(m) is int and m >= 0, "nonnegative integer M")
    if Q(2) ** m <= C_P:
        return 0
    d = 1
    while not Q(2) ** (m - d) < C_P / 2:
        d += 1
    return d


def closed_dbar(m: int) -> int:
    require(type(m) is int and m >= 0, "nonnegative integer M")
    return 0 if m <= 310 else m - 309


def gate3_replay() -> dict[str, Any]:
    require(Q(2) ** 310 < C_P < Q(2) ** 311, "C_p dyadic bracket")
    require(Q(2) ** 309 < C_P / 2 < Q(2) ** 310,
            "C_p/2 dyadic bracket")
    for m in range(0, 501):
        require(safe_dbar(m) == closed_dbar(m),
                f"closed safe clock row M={m}")

    clock_ms = [306, 307, 308, 309, 310, 311, 312, 313,
                314, 315, 319, 330, 400]
    clock_rows = [{
        "Dbar": closed_dbar(m),
        "M": m,
        "R0=696*Dbar": 696 * closed_dbar(m),
    } for m in clock_ms]
    require(clock_rows[4]["Dbar"] == 0 and clock_rows[5]["Dbar"] == 2,
            "first clock jump")

    separator_rows: list[dict[str, Any]] = []
    for count in (1, 2, 4, 8, 16, 32):
        atoms: dict[tuple[int, str, int], Q] = {}
        for k in range(1, count + 1):
            m_left = 310 + k - 1
            m_right = 310 + k
            t_left = 696 * closed_dbar(m_left)
            t_right = 696 * closed_dbar(m_right)
            require(t_left != t_right, "adjacent clock labels differ")
            # The face id makes different physical landing atoms disjoint.
            atoms[(k, "left", t_left)] = atoms.get((k, "left", t_left), Q(0)) + 1
            atoms[(k, "right", t_right)] = atoms.get((k, "right", t_right), Q(0)) - 1
        current_tv = sum((abs(value) for value in atoms.values()), Q(0))
        require(current_tv == 2 * count, "finite clock separator TV")
        separator_rows.append({
            "base_regular_F13_charge": "0",
            "clock_current_TV": qtext(current_tv),
            "moving_clock_faces": count,
            "weak_cemetery_mass": "0",
            "weak_source_restriction_TV": "1",
        })

    return {
        "safe_clock_closed_form": {
            "C_p": qtext(C_P),
            "dyadic_brackets": [
                "2^310<C_p<2^311",
                "2^309<C_p/2<2^310",
            ],
            "closed_form": [
                "Dbar(M)=0 for 0<=M<=310",
                "Dbar(M)=M-309 for M>=311",
            ],
            "exhaustive_replay_range": "0<=M<=500",
            "rows": clock_rows,
            "first_jump": "M:310->311 gives R0:0->1392",
            "later_jump_size": 696,
            "status": "CERTIFIED_EXACT_SAFE_CLOCK_CLOSED_FORM",
        },
        "dyadic_clock_trace_ledger": {
            "level_face_current": (
                "B_m=v_m[(Y_m^-)_*(rho_m^- trace_m)-"
                "(Y_m^+)_*(rho_m^+ trace_m)]"
            ),
            "extended_carrier": "physical stopped output plus immutable output-time tag",
            "exact_TV": (
                "||B_m||_TV=int_Gamma_m abs(v_m)(rho_m^-+rho_m^+)dH"
            ),
            "collision_time_distance_multiplier": False,
            "single_ledger": (
                "E_clock^dyad=sum_(m>=310) int_Gamma_m "
                "abs(v_m)(rho_m^-+rho_m^+)dH"
            ),
            "sufficient_row": (
                "absolute finiteness on one common finite-s atlas with actual landing maps"
            ),
            "status": "CERTIFIED_EXACT_DYADIC_CLOCK_TRACE_INTERFACE",
        },
        "weak_input_separator": {
            "model": (
                "unit density on [0,1], cuts e_k(s)=k/(N+1)+s, cell labels "
                "M_k=310+k, and distinct face/landing tags"
            ),
            "rows": separator_rows,
            "scope": "finite logical stopped-atlas models; not billiard realizations",
            "conclusion": (
                "weak TV, zero base regular F13 charge and zero weak cemetery mass "
                "do not bound the dyadic clock trace ledger"
            ),
            "status": "CERTIFIED_FALSE_FROM_WEAK_TV_F13_AND_WEAK_CEMETERY",
        },
        "physical_boundary": {
            "common_finite_s_dyadic_level_atlas": "NOT_CERTIFIED",
            "finite_physical_E_clock_dyad": "NOT_CERTIFIED",
            "moving_regular_strong_trace": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "anisotropic_bulk_directional_Piola": "NOT_CERTIFIED",
            "physical_strong_R_s_Q_s": "NOT_CERTIFIED",
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
            "arXiv_2604_19671v2": (
                "shrinking-boundary-hole conditional survival starts from regular "
                "families; no moving-scatterer finite-s current atlas or Piola theorem"
            ),
            "arXiv_2606_10155v1": (
                "transfer-operator and anisotropic-space review; no moving stopped "
                "Piola/current theorem"
            ),
            "arXiv_1909_11548v2": (
                "defines canonical class-H limits; does not solve the combined "
                "non-fibre-bunched Green cross term"
            ),
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
    "the combined clean-SFT Green gauge is reduced to one scalar cross term and "
    "the safe clock to one dyadic trace ledger, but the actual scalar limit, "
    "selected same-representative twisting, finite-s clock traces, strong "
    "cemetery, anisotropic bulk Piola, strong R/Q and MT_DQ remain not certified"
)


def build_manifest() -> dict[str, Any]:
    dependencies = validate_dependencies()
    require(REPORT.is_file() and not REPORT.is_symlink(), "report file/type")
    require(Path(__file__).resolve().is_file(), "certificate file/type")
    require(VERIFIER.is_file() and not VERIFIER.is_symlink(), "verifier file/type")
    result = build_result()
    return {
        "artifact": "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier",
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "date": "2026-07-21",
        "dependencies": dependencies,
        "report_sha256": sha256_path(REPORT),
        "result": result,
        "result_sha256": canonical_digest(result),
        "schema": "cm2.gate13.round64.one-cross-term-dyadic-clock-frontier.v1",
        "strict_verdict": STRICT_VERDICT,
        "verifier_sha256": sha256_path(VERIFIER),
    }


def resolve_emit(args: argparse.Namespace) -> Path | None:
    paths = [path for path in (args.emit, args.emit_manifest) if path is not None]
    require(not (len(paths) == 2 and paths[0] != paths[1]),
            "--emit and --emit-manifest disagree")
    return paths[0] if paths else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--print-result-sha", action="store_true")
    parser.add_argument("--emit", type=Path)
    parser.add_argument("--emit-manifest", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    try:
        emit_path = resolve_emit(args)
        if args.print_result_sha:
            print(canonical_digest(build_result()))
            return 0
        if emit_path is not None:
            emit_path.write_bytes(canonical_bytes(build_manifest()))
            print(f"EMITTED: {emit_path}")
            return 0
        if args.verify is not None:
            require(args.verify.is_file() and not args.verify.is_symlink(),
                    "verify manifest file/type")
            require(args.verify.read_bytes() == canonical_bytes(build_manifest()),
                    "manifest is not the deterministic canonical emission")
            print("VERIFY: PASS")
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
                "gate1_regimes": len(result["gate1"]["sharp_scalar_budget"]["regime_rows"]),
                "gate1_samples": sum(len(row["samples"]) for row in result["gate1"]["sharp_scalar_budget"]["regime_rows"]),
                "gate3_clock_rows": len(result["gate3"]["safe_clock_closed_form"]["rows"]),
                "gate3_closed_form_checks": 501,
                "gate3_separator_rows": len(result["gate3"]["weak_input_separator"]["rows"]),
                "status": "PASS",
            }, sort_keys=True))
            return 0
    except (CertificateError, OSError, ValueError) as exc:
        print(f"CERTIFICATE_ERROR: {exc}", file=sys.stderr)
        return 1
    print("GATE1_ONE_CROSS_TERM_REDUCTION: CERTIFIED")
    print("GATE3_DYADIC_CLOCK_TRACE_INTERFACE: CERTIFIED")
    print("ACTUAL_CROSS_TERM_CLOCK_PIOLA_STRONG_RQ_MT_DQ: NOT_CERTIFIED")
    print("GATES_1_3: NOT_CERTIFIED")
    print("COMPOSITE_GATES: 0/5")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
