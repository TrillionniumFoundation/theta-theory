#!/usr/bin/env python3
"""Compactly supported QNL logarithmic gauge and local plaque holonomies.

The preceding exact certificate constructs one two-axis logarithmic gauge in
an analytic QNL eigenchart and proves convergence of the stable and unstable
canonical tails relative to the QNL periodic point.  This certificate closes
the next purely local compatibility step.

Choose nested QNL neighbourhoods U_core compactly contained in U_chart on the
same non-grazing return branch and a smooth cutoff chi which is one on U_core
and zero on a collar of the boundary of U_chart.  Multiplying both logarithmic
terms by chi gives a single C^{1,alpha}, alpha<1, determinant-one gauge on the
whole return section, equal to the identity outside U_chart.  Every
sufficiently local stable orbit eventually stays in U_core, and every local
unstable orbit does so in backward time, so the compact extension changes
only a finite prefix of the already summable tails.

Tail convergence relative to the QNL point then gives canonical convergence
for every pair on the corresponding local stable or unstable plaque by the
exact finite-n factorisation H_{x,y,n}=H_{p,y,n} H_{p,x,n}^{-1}.

This does not prove a global symbolic coding, a uniform Hoelder modulus for
all coded plaques, a typed homoclinic loop, Butler--Park class H, or Gate 1.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
SOURCE_MANIFEST = (
    HERE / "cm2-gate1-resonant-log-gauge-frontier-manifest-2026-07-16.json"
)
SOURCE_CERTIFICATE = HERE / "cm2_gate1_resonant_log_gauge_frontier_cert.py"
EXPECTED_SOURCE_MANIFEST_SHA256 = (
    "b8ccde10c35be374116c896c68264b34e6f52952cbf4c240c71a79c9278aea17"
)
EXPECTED_SOURCE_CERTIFICATE_SHA256 = (
    "4e5cbbf7551e2ca3b76fac1226fe966ffdce0f843f4068b5cf9d3e77fa925090"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_source() -> dict[str, Any]:
    assert sha256_path(SOURCE_MANIFEST) == EXPECTED_SOURCE_MANIFEST_SHA256
    assert sha256_path(SOURCE_CERTIFICATE) == EXPECTED_SOURCE_CERTIFICATE_SHA256
    source = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    assert source["schema"] == (
        "cm2.gate1.resonant-log-gauge-frontier.manifest.v1"
    )
    result = source["result"]
    assert result["schema"] == "cm2.gate1.resonant-log-gauge-frontier.v1"
    assert result["gauge_regularity_and_minimality"]["regularity"] == (
        "C^1 and C^{1,alpha} for every 0<alpha<1"
    )
    assert result["exact_resonant_truncated_gauge"]["determinant_B"] == (
        "1 exactly"
    )
    assert result["analytic_physical_QNL_tail"][
        "local_transformed_QNL_stable_canonical_limit"
    ] == "CONVERGENT"
    assert result["analytic_physical_QNL_tail"][
        "local_transformed_QNL_unstable_canonical_limit"
    ] == "CONVERGENT"
    assert result["scope_limits"]["gate1_certified"] is False
    return source


def compact_extension() -> dict[str, Any]:
    return {
        "nested_neighbourhoods": (
            "QNL point p in U_core with closure(U_core) subset U_chart, "
            "both on one analytic non-grazing induced-return branch"
        ),
        "cutoff": (
            "chi in C_c^infinity(U_chart), chi=1 on U_core, "
            "chi=0 on a boundary collar"
        ),
        "stable_term": "t_s(x,y)=chi(x,y) k y^2 log|y|, t_s(x,0)=0",
        "unstable_term": "t_u(x,y)=chi(x,y) k x^2 log|x|, t_u(0,y)=0",
        "single_section_gauge": (
            "B_hat(x,y)=(I+t_u E_12)(I+t_s E_21) in U_chart, "
            "B_hat=I outside U_chart"
        ),
        "same_coefficient": "k=-325/(144 log(mu))",
        "regularity": "C^1 and C^{1,alpha} for every 0<alpha<1",
        "regularity_reason": (
            "smooth multiplication preserves the C^{1,alpha} logarithmic "
            "terms, and the gauge is exactly I on a chart-boundary collar"
        ),
        "determinant": "1 exactly",
        "global_inverse_on_section": True,
        "no_chart_boundary_seam": True,
        "equals_previous_local_gauge_on_core": True,
        "compact_support_changes_only_finite_orbit_prefixes": True,
    }


def local_plaque_holonomies() -> dict[str, Any]:
    return {
        "stable_entry": (
            "for every sufficiently local z in W^s_loc(p), some N(z) has "
            "F^n z in U_core for every n>=N(z)"
        ),
        "unstable_entry": (
            "for every sufficiently local z in W^u_loc(p), some N_u(z) has "
            "F^-n z in U_core for every n>=N_u(z)"
        ),
        "finite_prefix_principle": (
            "multiplying a convergent canonical tail by finitely many fixed "
            "invertible factors preserves convergence"
        ),
        "stable_reference_limits": (
            "H^s_{p,z}=lim_{n->infinity} A_hat^n(z)^-1 A_hat^n(p) exists "
            "for every sufficiently local z in W^s_loc(p)"
        ),
        "unstable_reference_limits": (
            "H^u_{p,z}=lim_{n->-infinity} A_hat^n(z)^-1 A_hat^n(p) exists "
            "for every sufficiently local z in W^u_loc(p)"
        ),
        "finite_n_pair_factorisation": (
            "H^s_{x,y;n}=H^s_{p,y;n}(H^s_{p,x;n})^-1 exactly"
        ),
        "stable_all_pairs_local_plaque": (
            "H^s_{x,y}=H^s_{p,y}(H^s_{p,x})^-1 exists for every local "
            "stable-plaque pair x,y"
        ),
        "unstable_all_pairs_local_plaque": (
            "H^u_{x,y}=H^u_{p,y}(H^u_{p,x})^-1 exists for every local "
            "unstable-plaque pair x,y"
        ),
        "local_cocycle_and_groupoid_identities": True,
        "uniform_holder_modulus_on_global_coding": False,
    }


def certify() -> dict[str, Any]:
    source = load_source()
    extension = compact_extension()
    plaques = local_plaque_holonomies()
    result = {
        "schema": "cm2.gate1.compact-log-gauge-plaque-holonomy-frontier.v1",
        "provenance": {
            "source_manifest": SOURCE_MANIFEST.name,
            "source_manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
            "source_certificate": SOURCE_CERTIFICATE.name,
            "source_certificate_sha256": EXPECTED_SOURCE_CERTIFICATE_SHA256,
            "source_internal_digest": source["result"]["internal_digest"],
        },
        "compact_supported_section_gauge": extension,
        "local_qnl_plaque_holonomies": plaques,
        "scope_limits": {
            "single_compact_supported_gauge_on_qnl_return_section": True,
            "stable_all_pairs_on_one_local_qnl_plaque": True,
            "unstable_all_pairs_on_one_local_qnl_plaque": True,
            "global_faithful_symbolic_coding": False,
            "global_all_pairs_holder_holonomies": False,
            "typed_qnl_homoclinic_loop": False,
            "butler_park_class_H": False,
            "park_piraino_fiber_bunching": False,
            "physical_projective_spectral_gap_or_PPE": False,
            "gate1_certified": False,
            "unconditional_cm2": False,
        },
        "strict_frontier": {
            "new_positive_layer": (
                "one seam-free compactly supported section gauge and canonical "
                "all-pairs limits on the local QNL stable/unstable plaques"
            ),
            "first_missing_layer": (
                "a faithful global coding with one uniform Hoelder holonomy "
                "modulus on every coded plaque and a typed twisting loop"
            ),
            "gate1": "NOT_CERTIFIED",
        },
    }
    result["internal_digest"] = digest({
        "extension": extension,
        "plaques": plaques,
        "scope": result["scope_limits"],
    })
    return result


def main() -> None:
    print(json.dumps(certify(), indent=2, sort_keys=True))
    print("GATE1_COMPACT_SECTION_GAUGE_AND_LOCAL_PLAQUE_HOLONOMIES: CERTIFIED")
    print("GATE1_GLOBAL_CLASS_H_AND_UNCONDITIONAL_TYPICALITY: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
