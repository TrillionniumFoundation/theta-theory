#!/usr/bin/env python3
"""Round-25 Gate-1 common-frame / same-representative frontier.

This append-only certificate joins four already frozen facts about the *same*
compact QNL logarithmic gauge and adds one exact algebraic layer:

* the product gauge U_v L_u has a positive Gauss big-cell factorisation;
* its biprojective factor has a uniform q > 999/1000 on the whole section;
* the selected local holonomies and four twisting wedges use that same gauge;
* that gauge nevertheless fails class H on the frozen connector basic set.

The certificate therefore closes the big-cell/common-frame typing gap for the
existing twisting candidate without promoting the missing all-plaque class-H
property or Gate 1.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-twenty-fourth-direct-assault-manifest-2026-07-18.sha256":
        "fde26b3f560086484a63cd0cc2e39a025d573c31982295a3702a14f9821e3c2c",
    "cm2-gate1-compact-log-gauge-plaque-holonomy-frontier-manifest-2026-07-16.json":
        "fc2d7263d4cb659a82c7ecb0fad48f538b466f861f1295d78bb6738331b8c4cd",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json":
        "4b9baaacaf7a315659448072d8d382bc90c4b41a9d98746b63c786f206ad449a",
    "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.json":
        "1e61f6f600300d15a15cf04179ee6e889ceb09edcf3d3b26f0d6f735afd6bdec",
    "cm2-gate1-biprojective-half-density-frontier-manifest-2026-07-17.json":
        "6c6e8465161a64785ae07b3bd7a229820c93bacd9d07a2cd10c4691686722d6b",
    "cm2-gate1-common-transport-ift-frontier-manifest-2026-07-17.json":
        "b4a7838178ea2fe54d6fed68f99fc03f20d4efaa2e5c9ba4df13e7c5613e8527",
}

COMPACT = "cm2-gate1-compact-log-gauge-plaque-holonomy-frontier-manifest-2026-07-16.json"
NUMERIC = "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json"
GLOBAL = "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.json"
HALF = "cm2-gate1-biprojective-half-density-frontier-manifest-2026-07-17.json"
TRANSPORT = "cm2-gate1-common-transport-ift-frontier-manifest-2026-07-17.json"


class CertificateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CertificateError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_dependencies() -> dict[str, Any]:
    loaded: dict[str, Any] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.parent.resolve() == HERE, f"dependency escapes directory: {name}")
        require(not path.is_symlink(), f"symlink dependency rejected: {name}")
        require(path.is_file(), f"missing dependency: {name}")
        require(sha256_path(path) == expected, f"dependency hash changed: {name}")
        if path.suffix == ".json":
            loaded[name] = json.loads(
                path.read_text(encoding="utf-8"),
                object_pairs_hook=reject_duplicate_pairs,
                parse_constant=lambda token: (_ for _ in ()).throw(
                    CertificateError(f"non-finite JSON token: {token}")
                ),
            )
    return loaded


def exact_factorisation_sample() -> dict[str, Any]:
    # A perfect-square sample keeps the replay entirely in Q.
    u = Fraction(7, 9)
    v = Fraction(1, 1)
    d = 1 + u * v
    f = Fraction(4, 3)
    require(f * f == d, "sample square-root identity failed")
    u_bip = u / d
    q = 1 / d

    product_gauge = ((d, v), (u, Fraction(1)))
    biprojective = (
        (f, f * v),
        (f * u_bip, f),
    )
    positive_diagonal = ((f, Fraction(0)), (Fraction(0), 1 / f))

    def mul(a: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
            b: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]):
        return tuple(
            tuple(sum((a[i][k] * b[k][j] for k in range(2)), Fraction(0))
                  for j in range(2))
            for i in range(2)
        )

    def det(a: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]):
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]

    require(mul(biprojective, positive_diagonal) == product_gauge,
            "exact Gauss factorisation failed")
    require(det(product_gauge) == det(biprojective) == det(positive_diagonal) == 1,
            "determinant-one replay failed")
    require(q == 1 - u_bip * v, "biprojective q identity failed")

    fmt = lambda x: f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)
    return {
        "sample_product_coordinates": {"u": fmt(u), "v": fmt(v), "d": fmt(d)},
        "sample_biprojective_coordinates": {
            "u_bip": fmt(u_bip), "v_bip": fmt(v), "q": fmt(q), "sqrt_d": fmt(f)
        },
        "product_gauge": [[fmt(x) for x in row] for row in product_gauge],
        "biprojective_factor": [[fmt(x) for x in row] for row in biprojective],
        "positive_diagonal_factor": [[fmt(x) for x in row] for row in positive_diagonal],
        "factorisation_and_three_determinants_exact": True,
    }


def build_result() -> dict[str, Any]:
    deps = load_dependencies()
    compact = deps[COMPACT]["result"]
    numeric = deps[NUMERIC]["result"]
    global_result = deps[GLOBAL]["result"]
    half = deps[HALF]["result"]
    transport = deps[TRANSPORT]["result"]

    compact_digest = compact["internal_digest"]
    require(
        numeric["provenance"]["compact_internal_digest"] == compact_digest,
        "numeric loop is not bound to the compact gauge",
    )
    require(
        global_result["provenance"]["compact_internal_digest"] == compact_digest,
        "connector obstruction is not bound to the compact gauge",
    )
    require(
        compact["compact_supported_section_gauge"]["single_section_gauge"]
        == "B_hat(x,y)=(I+t_u E_12)(I+t_s E_21) in U_chart, B_hat=I outside U_chart",
        "unexpected compact gauge formula",
    )
    require(
        numeric["canonical_coordinate_and_gauge_audit"]["gauge_matrix"]
        == "B_u(x) B_s(y)",
        "selected loop uses a different gauge order",
    )
    require(
        numeric["tail_majorants"]["chart_radius"] == "1e-10"
        and global_result["connector_compact_gauge_obstruction"]["compact_qnl_gauge_chart_radius"]
        == "1e-10",
        "chart-radius binding failed",
    )
    require(
        compact["compact_supported_section_gauge"]["determinant"] == "1 exactly"
        and compact["compact_supported_section_gauge"]["global_inverse_on_section"] is True,
        "compact gauge is not frozen determinant-one/invertible",
    )
    require(
        compact["local_qnl_plaque_holonomies"]["uniform_holder_modulus_on_global_coding"]
        is False,
        "dependency unexpectedly promotes a global Holder modulus",
    )

    wedges = numeric["four_selected_twisting_wedges"]
    require(len(wedges) == 4, "expected exactly four twisting wedges")
    require(
        numeric["scope_limits"]["four_selected_QNL_eigen_axis_twisting_wedges"] is True,
        "four selected wedges are not certified",
    )
    obstruction = global_result["connector_compact_gauge_obstruction"]
    require(obstruction["compact_qnl_gauge_connector_stable_limit_converges"] is False,
            "connector obstruction disappeared")
    require(obstruction["compact_qnl_gauge_class_H_on_common_basic_set_with_connector"] is False,
            "compact gauge unexpectedly entered class H")
    require(half["strict_nonpromotion"]["uniform_big_cell_q_lower_bound"] == "NOT_CERTIFIED",
            "predecessor already claimed the new big-cell layer")
    require(transport["strict_nonpromotion"]["coupled_half_density_groupoid_solution"]
            == "NOT_CERTIFIED", "predecessor coupled solution changed")

    # Exact uniform bound.  Choose the standard compact cutoff with 0<=chi<=1.
    # For 0<r<=10^-10, -r^2 log r is increasing and
    # -r^2 log r <= 10^-19 log(10) < 3*10^-19 < 10^-18.
    # The strict log bound is certified without floating point because
    # exp(3)>1+3+3^2/2+3^3/6=13>10.
    exp3_partial = Fraction(1) + Fraction(3) + Fraction(9, 2) + Fraction(27, 6)
    require(exp3_partial == 13 and exp3_partial > 10, "log(10)<3 witness failed")
    term_bound = Fraction(1, 10**18)
    product_bound = term_bound * term_bound
    q_lower = Fraction(999, 1000)
    require(Fraction(1, 1) / (1 + product_bound) > q_lower,
            "declared q lower bound is not strict")

    sample = exact_factorisation_sample()
    core: dict[str, Any] = {
        "schema": "cm2.gate1.round25.common-frame-same-representative-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "compact_gauge_internal_digest": compact_digest,
            "old_artifacts_modified": False,
            "arithmetic": "exact rational algebra plus frozen Arb interval dependencies",
        },
        "same_compact_gauge_binding": {
            "section_gauge": "G=U_v L_u=[[1+uv,v],[u,1]], with u=t_s and v=t_u",
            "cutoff_choice": "0<=chi<=1, chi=1 on U_core, chi=0 on the boundary collar",
            "chart_coordinate_radius": "1/10^10",
            "coefficient_bound": "0<k<1 (frozen 5000-bit Arb enclosure)",
            "same_gauge_local_qnl_stable_holonomies": True,
            "same_gauge_local_qnl_unstable_holonomies": True,
            "same_gauge_selected_homoclinic_loop": True,
            "same_gauge_four_nonzero_twisting_wedges": True,
            "same_gauge_connector_basic_set_obstruction": True,
            "gauge_identity_outside_chart": True,
        },
        "uniform_big_cell_certificate": {
            "log10_upper_witness": "exp(3)>1+3+9/2+27/6=13>10, hence log(10)<3",
            "monotonicity": "-r^2 log(r) is increasing on 0<r<=10^-10",
            "term_bounds": "|u|<1/10^18 and |v|<1/10^18",
            "product_bound": "|uv|<1/10^36",
            "gauss_denominator": "d=1+uv>0",
            "biprojective_coordinates": "u_bip=u/(1+uv), v_bip=v, q=1-u_bip*v_bip=1/(1+uv)",
            "uniform_q_lower_bound": "q>999/1000",
            "uniform_q_lower_bound_certified": True,
            "whole_compact_return_section": True,
            "outside_chart_q": "q=1",
        },
        "exact_common_frame_factorisation": {
            "identity": "U_v L_u = q^(-1/2)[[1,v_bip],[u_bip,1]] diag(sqrt(1+uv),1/sqrt(1+uv))",
            "biprojective_frame_columns": "a=q^(-1/2)(1,u_bip)^T, b=q^(-1/2)(v_bip,1)^T",
            "frame_determinant": "det(a,b)=1 exactly",
            "positive_diagonal_remainder": True,
            "same_original_physical_representative": True,
            "rational_replay": sample,
        },
        "same_representative_join": {
            "local_canonical_Hs_Hu_and_selected_twisting_in_one_gauge": True,
            "four_wedge_enclosures": dict(wedges),
            "connector_stable_increment": obstruction["canonical_increment_formula"],
            "connector_stable_increment_asymptotic": obstruction["canonical_increment_asymptotic"],
            "compact_gauge_class_H_on_common_basic_set_with_connector": False,
            "consequence": "this exact compact twisting candidate cannot close Gate 1 on the connector common basic set",
            "diagonal_class_H_representative_is_a_different_representative": True,
        },
        "maturity": {
            "candidate_interface_slots_total": 6,
            "candidate_interface_slots_positive": 5,
            "positive_slots": [
                "single determinant-one compact physical gauge",
                "uniform positive big cell and determinant-one common frame",
                "canonical Hs/Hu on the local QNL plaques",
                "typed selected immutable homoclinic loop",
                "four nonzero selected twisting wedges",
            ],
            "failed_global_slot": "uniform all-plaque Butler-Park class H in this same representative",
            "failed_global_slot_status": "REFUTED_ON_FROZEN_CONNECTOR_BASIC_SET",
            "gate1_maturity": "0/1",
        },
        "strict_nonpromotion": {
            "coupled_half_density_groupoid_equations_on_all_plaques": "NOT_CERTIFIED",
            "uniform_all_plaque_holder_holonomies_in_twisting_gauge": "NOT_CERTIFIED",
            "compact_twisting_gauge_in_class_H_on_connector_basic_set": False,
            "another_third_gauge_with_class_H_and_twisting": "NOT_CERTIFIED",
            "full_mass_physical_projective_PPE": "NOT_CERTIFIED",
            "Gate1": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result = dict(core)
    result["internal_replay_digest"] = digest(core)
    return result


def main() -> int:
    print(json.dumps(build_result(), sort_keys=True, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
