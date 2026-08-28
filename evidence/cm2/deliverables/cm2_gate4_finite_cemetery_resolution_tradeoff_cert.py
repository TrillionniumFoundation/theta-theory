#!/usr/bin/env python3
"""Exact finite-cemetery versus native-resolution tradeoff for Gate 4.

On a normalized physical row cumulative-mass coordinate u in [0,1], let a
deterministic native stop retain mass at least 1-epsilon in finitely many
positive-mass atoms of u-diameter at most delta.  The normalized row measure
pushes forward to Lebesgue measure, so every atom has mass at most delta and
the atom count N is at least ceil((1-epsilon)/delta).  Under the Gate-4 leafwise normalization
interface, atom A of mass p_A costs at least p_A^{-1}; hence its unconditional
expected charge is exactly one and the total charge is at least N.

Thus a finite cemetery does not give a uniform escape when resolution tends
to zero and cemetery mass tends to zero.  For dyadic resolution 2^{-K}, the
charge is at least (1-epsilon)2^K; if epsilon<=2^{-K}, it is at least 2^K-1.
Any nonnegative recovery factor only increases the bound.

The result is conditional on the existing leafwise inverse-mass cost
interface.  It does not exclude a different unnormalised/reweighted-family
theorem or an external random depth mark.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
SOURCE_MANIFEST = (
    HERE / "cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json"
)
SOURCE_CERTIFICATE = HERE / "cm2_gate4_native_stopping_repeated_recovery_frontier_cert.py"
EXPECTED_SOURCE_MANIFEST_SHA256 = (
    "20f595ed4bcf62cb5cc5c89c22ab31a3ca039f43fff29fd35855673dc970b4a2"
)
EXPECTED_SOURCE_CERTIFICATE_SHA256 = (
    "9935fcfdb043fa0e069b635a464a486357921727e99ddec9d44216c149d022bb"
)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def load_source() -> dict[str, Any]:
    assert sha256_path(SOURCE_MANIFEST) == EXPECTED_SOURCE_MANIFEST_SHA256
    assert sha256_path(SOURCE_CERTIFICATE) == EXPECTED_SOURCE_CERTIFICATE_SHA256
    manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == (
        "cm2.gate4.native-stopping-repeated-recovery-frontier.manifest.v1"
    )
    assert manifest["replay_summary"]["native_prefix_antichain"] == "CERTIFIED"
    assert manifest["replay_summary"]["native_recovery_target"] == (
        "DIVERGES_BEFORE_RECOVERY"
    )
    spec = importlib.util.spec_from_file_location(
        "cm2_gate4_native_stopping_repeated_recovery_frontier_cert",
        SOURCE_CERTIFICATE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.certify()
    assert result["schema"] == (
        "cm2.gate4.native-stopping-repeated-recovery-frontier.v1"
    )
    assert result["scope_limits"][
        "native_physical_mass_coordinate_prefix_antichain"
    ] is True
    assert result["scope_limits"][
        "native_antichain_finite_normalization_recovery_moment"
    ] is False
    obstruction = result["native_recovery_charge_obstruction"]
    assert obstruction["general_partition_identity"] == (
        "for disjoint positive-mass atoms A_i with normalization cost "
        "1/mu(A_i), sum_i mu(A_i)/mu(A_i)=number of atoms"
    )
    return result


def resolution_rows() -> list[dict[str, Any]]:
    rows = []
    for k in range(1, 21):
        delta = Fraction(1, 1 << k)
        epsilon = delta
        atom_lower = ceil_fraction((1 - epsilon) / delta)
        assert atom_lower == (1 << k) - 1
        rows.append({
            "K": k,
            "delta": str(delta),
            "epsilon_upper": str(epsilon),
            "minimum_atom_count": atom_lower,
            "unconditional_inverse_mass_charge_lower": atom_lower,
            "dyadic_formula": f"2^{k}-1",
        })
    return rows


def certify() -> dict[str, Any]:
    source = load_source()
    rows = resolution_rows()
    theorem = {
        "carrier": "normalized physical cumulative-mass coordinate u in [0,1]",
        "parameter_range": "0<=epsilon<1 and 0<delta<=1",
        "coordinate_pushforward": (
            "(u_e,s)_*(m_e,s/m_e,s(row_s)) is Lebesgue measure on [0,1]"
        ),
        "retained_mass": "at least 1-epsilon",
        "atom_geometry": (
            "every retained positive-mass measurable atom has u-diameter <=delta"
        ),
        "mass_per_atom_upper": "p_a<=delta",
        "mass_per_atom_derivation": (
            "p_a=Lebesgue(A_a)<=diam_u(A_a)<=delta"
        ),
        "count_lower": "N>=ceil((1-epsilon)/delta)",
        "leafwise_cost_interface": "cost(a)>=p_a^-1",
        "unconditional_charge_identity": "sum_a p_a p_a^-1=N",
        "unconditional_charge_lower": "E[cost]>=ceil((1-epsilon)/delta)",
        "conditional_on_survival_lower": (
            "with P_ret=sum_a p_a, E[cost | retained]>=N/P_ret>=1/delta"
        ),
        "recovery_factor": (
            "multiplication by exp(gamma R_a)>=1 cannot improve any lower bound"
        ),
        "vanishing_cemetery_fine_resolution_consequence": (
            "if epsilon_j->0 and delta_j->0 then the charged moment diverges"
        ),
        "dyadic_consequence": (
            "delta=2^-K and epsilon<=2^-K imply E[cost]>=2^K-1"
        ),
    }
    result = {
        "schema": "cm2.gate4.finite-cemetery-resolution-tradeoff.v1",
        "provenance": {
            "source_manifest": SOURCE_MANIFEST.name,
            "source_manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
            "source_certificate": SOURCE_CERTIFICATE.name,
            "source_certificate_sha256": EXPECTED_SOURCE_CERTIFICATE_SHA256,
            "source_native_rows_digest": source["internal_replay_digests"][
                "native_rows"
            ],
        },
        "finite_cemetery_resolution_theorem": theorem,
        "dyadic_replay_rows": rows,
        "dyadic_replay_rows_sha256": digest(rows),
        "scope_limits": {
            "finite_cemetery_uniform_leafwise_moment_escape": False,
            "deterministic_native_vanishing_cemetery_fine_resolution": (
                "CHARGE_DIVERGES_UNDER_INVERSE_MASS_INTERFACE"
            ),
            "unnormalized_reweighted_family_recovery_refuted": False,
            "external_random_depth_policy_refuted": False,
            "uses_only_normalized_cumulative_mass_coordinate": True,
            "diameter_to_mass_claim_outside_that_coordinate": False,
            "numeric_growth_constants_certified": False,
            "propagated_q_certified": False,
            "gate4_certified": False,
            "unconditional_cm2": False,
        },
        "strict_frontier": {
            "closed_escape_route": (
                "finite native antichains with simultaneously vanishing "
                "cemetery and arbitrarily fine resolution cannot have a "
                "uniform leafwise inverse-mass recovery moment"
            ),
            "remaining_escape_route": (
                "prove recovery for one unnormalised/reweighted family "
                "without leafwise p_a^-1 charging, or change the interface"
            ),
            "gate4": "NOT_CERTIFIED",
        },
    }
    result["internal_digest"] = digest({
        "theorem": theorem,
        "rows": rows,
        "scope": result["scope_limits"],
    })
    return result


def main() -> None:
    print(json.dumps(certify(), indent=2, sort_keys=True))
    print("GATE4_FINITE_CEMETERY_RESOLUTION_TRADEOFF: CERTIFIED")
    print("GATE4_NATIVE_CHARGED_RECOVERY_AND_PROPAGATED_Q: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
