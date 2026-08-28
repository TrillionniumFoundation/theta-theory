#!/usr/bin/env python3
"""Finite-root fixed-density Reg_alpha synthesis and official F14 frontier.

The Round87 packet disintegration removes the apparent short-fibre BV
singularity, but deliberately stops before identifying its recipient with the
frozen standard-family source completion.  This certificate makes precisely
that missing identification.  It uses the adapted line element and density
cone already frozen by the numerical Growth theorem, canonically chops every
conditional curve at ``delta_*=10^-90``, and pays the chop in the *weighted*
boundary functional.  No individual short conditional fibre is normalized
before the transverse mass is integrated.

The resulting map is defined only on the 152-dimensional span of the frozen
collision-density profiles.  The official F14 field requires the branchwise
regular-density prefix/suffix intertwiner on its full input recipient.  That
interface remains false in the frozen norm ledger, so this certificate does
not materialize an official F14 slot.
"""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as return_cert
import cm2_gate4_inner_core_strong_product_bridge_frontier_cert as strong_cert
import cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert as growth_cert


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round88.gate5-f14-regalpha-strong-frontier.v2"

ROUND87 = HERE / "cm2-round87-gate5-f14-transverse-packet-recovery-2026-07-22.json"
WINDOWS = HERE / "cm2-round85-gate3-s0-two-sided-material-window-2026-07-22.json"
TYPED = HERE / "cm2-round85-gate5-f14-typed-standard-pair-frontier-2026-07-22.json"
OPERATOR = HERE / "cm2-round85-gate5-finite-root-operator-field-frontier-2026-07-22.json"
PACKETS = HERE / "cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json"
EMPTY = HERE / "cm2-gate5-round27-r1-empty-physical-face-join-manifest-2026-07-18.json"
STRONG = HERE / "cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json"
GROWTH = HERE / "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
CONE = HERE / "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json"
NORM_FRONTIER = HERE / "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json"

PINS = {
    "round87_weighted_BV": "4693a3d5fc21211452d82f5c28268b61c377ff8d8af7cc99c45f02a072ce5181",
    "round87_weighted_BV_source": "c422b6a50d697b3da6507aeead6dc85f88dddf5510bd04fe92f94b503a41af08",
    "windows": "81356d91e1725c9f454ac010b264a0bd1fbd92b2892cca602f1ff5f9ae64b2c7",
    "typed": "5ade1c0ed5183b316277cd9b519e2291dcf2a4c914cd17c86c7ee1afcf2b6f78",
    "operator_frontier": "f0fd1dc13a7a51b82ca0eb511ce3bd6d44fcd1744b11a0c512b7e5a96f652d19",
    "packet_registry": "f6950d0a6ccf6984f888a102d846557e807becfddf3a95a72565e514934783e4",
    "empty_F10_F13_registry": "9d900f2d0fee5ab8ad1a7e1f999e640ef88edc928ba6208987d1a74c93ca0e38",
    "strong_recipient": "3a9fdd11c952fd8517a8fa068794c5737fee7265ee5532032af9605eae2feee3",
    "strong_recipient_source": "4720669e90824e8c630276aa3d73606435eb88da2a51b2a756f651f56071605a",
    "numeric_growth": "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d",
    "numeric_growth_source": "01e32ca209818f4077443a7692622c4202ab7f1066e2f95802185e2be7a2cc9a",
    "invariant_cone": "173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9",
    "invariant_cone_source": "675980a44658a77c2849920b749b2d74ff482fb61ce151a58cfdfcd23bae746a",
    "first_hit_source": "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "physical_core_source": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "return_classifier_source": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
    "physical_prefix_norm_frontier": "64f3820e2dc2f6d544be94bbe205fcf08f9517eef29131311e6fafa295060a93",
    "physical_prefix_norm_source": "e3cc04cb10cf116a85b2be69b6ead272c849ee07c47a2668cbb8bd85b95ce039",
    "round27_empty_slot_source": "aabe7f375036e68b742695f27a3a274bc47f594e547579e3592cf97f46989c43",
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_load(path: Path) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"duplicate JSON key: {key}")
            out[key] = value
        return out

    value = json.loads(
        path.read_text(), object_pairs_hook=unique,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if not isinstance(value, dict):
        raise ValueError("top-level JSON object required")
    return value


def aq(value: Q | str | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def actual_pins() -> dict[str, str]:
    return {
        "round87_weighted_BV": file_digest(ROUND87),
        "round87_weighted_BV_source": file_digest(HERE / "cm2_round87_gate5_f14_transverse_packet_recovery_cert.py"),
        "windows": file_digest(WINDOWS),
        "typed": file_digest(TYPED),
        "operator_frontier": file_digest(OPERATOR),
        "packet_registry": file_digest(PACKETS),
        "empty_F10_F13_registry": file_digest(EMPTY),
        "strong_recipient": file_digest(STRONG),
        "strong_recipient_source": file_digest(HERE / "cm2_gate4_inner_core_strong_product_bridge_frontier_cert.py"),
        "numeric_growth": file_digest(GROWTH),
        "numeric_growth_source": file_digest(HERE / "cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py"),
        "invariant_cone": file_digest(CONE),
        "invariant_cone_source": file_digest(HERE / "cm2_gate45_global_invariant_cone_cert.py"),
        "first_hit_source": file_digest(HERE / "cm2_gate3_candidate_first_hit_cert.py"),
        "physical_core_source": file_digest(HERE / "cm2_gate25_physical_return_core_registry_cert.py"),
        "return_classifier_source": file_digest(HERE / "cm2_gate34_full_core_return_adaptive_frontier_cert.py"),
        "physical_prefix_norm_frontier": file_digest(NORM_FRONTIER),
        "physical_prefix_norm_source": file_digest(HERE / "cm2_gate5_physical_prefix_kac_norm_frontier_cert.py"),
        "round27_empty_slot_source": file_digest(HERE / "cm2_gate5_round27_r1_empty_physical_face_join_cert.py"),
    }


def proposed_slot_key(row: dict[str, Any]) -> str:
    payload = {
        "slot_schema": "cm2.gate5.immutable-operator-field-slot.v1",
        "field_index": 14,
        "field_name": "regular_density_operator_cost",
        "atom_id": row["atom_id"],
        "candidate_packet_id": row["candidate_packet_id"],
        "physical_homogeneity_subbranch_id": row["physical_homogeneity_subbranch_id"],
        "roof_level_j": row["roof_level_j"],
        "recipient": "M*(1+Reg_alpha(rho)+1/length)",
        "properization": "adapted_equal_chop_delta_star_1e-90",
    }
    return "proposed-slot-key:r1:f14:" + digest(payload)


def build(bits: int = 512) -> dict[str, Any]:
    ctx.prec = bits
    pins = actual_pins()
    if pins != PINS:
        raise ValueError("frozen upstream pin mismatch")

    round87 = strict_load(ROUND87)["result"]
    windows = strict_load(WINDOWS)["result"]["evidence"]["window_rows"]
    typed = strict_load(TYPED)["result"]
    operator = strict_load(OPERATOR)["result"]
    packets = strict_load(PACKETS)["result"]["R1_inner_candidate_field_packet_rows"]
    empty = strict_load(EMPTY)["result"]
    norm_frontier = strict_load(NORM_FRONTIER)["result"]

    if round87["weighted_BV_disintegration_on_152_packets"] != "CERTIFIED":
        raise ValueError("Round87 weighted disintegration")
    if round87["new_F14_slots_installed"] != 0 or round87["candidate_local_maturity_after"] != "13/18":
        raise ValueError("Round87 frontier")
    if typed["finite_root_typed_F14_central_subfamily_input"] != "CERTIFIED_152_OF_152":
        raise ValueError("typed standard pairs")
    if operator["candidate_local_maturity_after"] != "13/18":
        raise ValueError("operator frontier")
    if empty["F14_F18_frontier"]["F14_through_F18_materialized_slot_count"] != 0:
        raise ValueError("prior F14 registry must be empty")
    if norm_frontier["completion"]["regular_density_prefix_suffix_intertwiner"] is not False:
        raise ValueError("unexpected official regular-density intertwiner")
    if norm_frontier["completion"]["immutable_complete_return_word_operator_registry"] is not False:
        raise ValueError("unexpected complete operator registry")

    strong = strong_cert.core_local_strong_multiplier()
    density = growth_cert.invariant_density_and_distortion()["invariant_adapted_density_cone"]
    growth = growth_cert.numeric_growth_and_recovery()["adapted_boundary_Growth_recurrence"]
    if strong["source_norm"] != "M*(1+Reg_alpha(rho)+1/length)":
        raise ValueError("strong recipient")
    if density["density_constant"] != str(5 * 10**26):
        raise ValueError("density cone")
    if density["canonical_maximum_adapted_curve_length"] != "1/1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000":
        raise ValueError("canonical delta")
    if growth["additive_mass_coefficient"] != str(2 * 10**90):
        raise ValueError("canonical chop charge")

    packet_map = {row["atom_id"]: row for row in packets}
    attachment_map = {row["atom_id"]: row for row in operator["evidence"]["attachment_rows"]}
    round87_map = {row["atom_id"]: row for row in round87["evidence"]["integration_rows"]}
    core_map = {return_cert.core_id(core): core for core in core_cert.physical_cores()}
    if not (len(windows) == len(round87_map) == len(attachment_map) == 152):
        raise ValueError("152-row census")

    delta = Q(1, 10**90)
    reg_upper = Q(1, 80)
    old_weighted_z_upper = Q(4300)
    chop_additive = Q(2 * 10**90)
    operator_upper = chop_additive + Q(4302)
    rows: list[dict[str, Any]] = []
    for window in sorted(windows, key=lambda row: row["positive_atom_id"]):
        atom_id = window["positive_atom_id"]
        prior = round87_map[atom_id]
        attach = attachment_map[atom_id]
        packet = packet_map[atom_id]
        if not (
            prior["candidate_packet_id"]
            == attach["candidate_packet_id"]
            == packet["r1_candidate_field_packet_id"]
        ):
            raise ValueError("packet key chain")
        if prior["physical_homogeneity_subbranch_id"] != attach["physical_homogeneity_subbranch_id"]:
            raise ValueError("branch key chain")
        if prior["F10_slot_id"] != attach["F10_slot_id"] or attach["F10_coarea_density_regular_cost"] != "0":
            raise ValueError("completed F10 slot")
        if packet["roof_level_j"] != 0 or packet["roof"] != 1:
            raise ValueError("roof key")

        core = core_map[window["source_core_id"]]
        radius = Q(first_hit.RADIUS[core.source])
        p0, p1 = map(Q, window["common_p"])
        if max(abs(p0), abs(p1)) > Q(1, 50):
            raise ValueError("source core p bound")
        # Along phi=4r+v, d(log rho)/dr=-4 tan(phi).  Since
        # |p|<=1/50, cos(phi)>49/50 and kappa+V>25/9+4=61/9,
        # the adapted log-Lipschitz coefficient is <36/2989<1/80.
        pmax = max(abs(p0), abs(p1))
        log_lip = 4 * aq(pmax) / (1 - aq(pmax) ** 2).sqrt() / aq(Q(1, radius) + 4)
        if not (log_lip < aq(Q(36, 2989)) < aq(reg_upper)):
            raise ValueError("adapted log-density regularity")

        row = {
            "atom_id": atom_id,
            "candidate_packet_id": attach["candidate_packet_id"],
            "physical_homogeneity_subbranch_id": attach["physical_homogeneity_subbranch_id"],
            "roof_level_j": 0,
            "source_core_id": window["source_core_id"],
            "destination_core_id": window["destination_core_id"],
            "completed_F10_slot_id": attach["F10_slot_id"],
            "completed_F10_value": "0_EMPTY_PHYSICAL_OCCURRENCE_FACE_FAMILY",
            "field_index": 14,
            "field_name": "regular_density_operator_cost",
            "curve_slope_dphi_dr": "4",
            "adapted_line_element": "dell_*=(kappa+4)*abs(dr)",
            "conditional_density": "rho_v=cos(4r+v)/(sqrt(17)*m(v))",
            "adapted_log_density_Lipschitz_strict_upper": "1/80",
            "Reg_alpha_definition": "sup_abs_Delta_log_rho/dell_*^(1/3)",
            "Reg_alpha_strict_upper_after_restriction_and_normalization": "1/80",
            "canonical_delta_star": str(delta),
            "properization": "N=ceil(ell_*/delta_*); N equal adapted-length pieces, so ell_*/N is in (delta_*/2,delta_*] when N>1; an already-short curve is retained",
            "weighted_prechop_Z_strict_upper": str(old_weighted_z_upper),
            "canonical_chop_Z_additive_upper": str(chop_additive),
            "accepted_strong_source_norm": strong["source_norm"],
            "accepted_strong_synthesis_cost_strict_upper": str(operator_upper),
            "proposed_F14_slot_key": "",
            "immutable_F14_slot_id": "NOT_MATERIALIZED",
            "F14_slot_status": "NOT_CERTIFIED__FIXED_PROFILE_SYNTHESIS_IS_NOT_THE_FULL_REGULAR_DENSITY_BRANCH_OPERATOR",
        }
        row["proposed_F14_slot_key"] = proposed_slot_key(row)
        rows.append(row)

    proposed = {row["proposed_F14_slot_key"] for row in rows}
    if len(rows) != 152 or len(proposed) != 152:
        raise ValueError("proposed F14 key uniqueness")

    evidence = {
        "precision_bits": bits,
        "finite_root_packet_count": 152,
        "completed_same_key_F10_slot_count": 152,
        "installed_immutable_F14_slot_count": 0,
        "proposed_F14_slot_key_count": 152,
        "recipient": {
            "completion": strong["source_norm"],
            "curve_class": "canonical phase-typed unstable standard curves",
            "adapted_density_cone_constant": str(5 * 10**26),
            "canonical_delta_star": str(delta),
            "Reg_alpha_crosswalk": "CERTIFIED_FROM_ADAPTED_LOG_LIPSCHITZ_AND_DELTA_STAR_LESS_THAN_ONE",
            "normalization_invariance": "restriction/conditional normalization adds only a curvewise constant to log rho",
        },
        "intertwiner": {
            "domain": "ell^1(152) coefficients on one fixed normalized collision-density profile per packet",
            "weighted_disintegration": "Round87 dLambda=m(v)dv/M and rho_v=h_v/m(v)",
            "map": "disintegrate, then canonical equal-adapted-length chop at delta_*",
            "codomain": "fixed-profile subspace of the signed-Jordan completion of the frozen strong standard-family source space",
            "mass_term_upper": "1",
            "Reg_alpha_term_strict_upper": "1/80",
            "weighted_prechop_Z_strict_upper": "4300",
            "canonical_chop_Z_additive_upper": str(chop_additive),
            "operator_norm_strict_upper": str(operator_upper),
            "bounded": True,
        },
        "official_F14_interface_audit": {
            "required_field": "regular_density_operator_cost",
            "frozen_regular_density_prefix_suffix_intertwiner": False,
            "frozen_immutable_complete_return_word_operator_registry": False,
            "arbitrary_regular_density_input_supported": False,
            "branchwise_prefix_suffix_operator_supported": False,
            "fixed_profile_span_is_the_official_operator_domain": False,
            "conclusion": "NO_OFFICIAL_F14_SLOT_MATERIALIZATION",
        },
        "slot_rows": rows,
    }
    result = {
        "status": "CERTIFIED_152_FIXED_COLLISION_DENSITY_REG_ALPHA_STRONG_SYNTHESIS__OFFICIAL_F14_OPEN",
        "fixed_collision_density_Regalpha_synthesis_cost": f"STRICTLY_LESS_THAN_{operator_upper}",
        "F14_regular_density_operator_cost": "NOT_CERTIFIED__NO_ARBITRARY_REGULAR_DENSITY_PREFIX_SUFFIX_INTERTWINER",
        "finite_root_F14_slot_installation": "NOT_CERTIFIED",
        "new_immutable_F14_slots_installed": 0,
        "finite_root_candidate_local_maturity_before": "13/18",
        "finite_root_candidate_local_maturity_after": "13/18",
        "first_remaining_finite_root_field": "F14_regular_density_operator_cost",
        "complete_18_field_operator_blocks": 0,
        "global_Gate5": "NOT_CERTIFIED__10/18_BLOCKS_0",
        "strict_nonclaims": [
            "a bounded synthesis on 152 fixed density profiles is not the arbitrary-input regular-density branch operator",
            "no regular-density prefix/suffix intertwiner is inferred from the codomain embedding",
            "the 152 finite-root slots are not a complete limiting-R1 branch assembly",
            "canonical properization does not supply F15 raw-Z/Orlicz recovery or cemetery control",
            "no F16, F17, F18, all-depth, or global Gate-5 field is promoted",
            "the empty F10 value is only a completed dependency and is not used to pay the nonzero F14 norm",
        ],
        "evidence": evidence,
        "evidence_sha256": digest(evidence),
    }
    return {"schema": SCHEMA, "pins": pins, "result": result, "result_sha256": digest(result)}


def main() -> int:
    try:
        print(canonical(build()))
        return 0
    except Exception as exc:
        print(canonical({"schema": SCHEMA, "status": "FAIL_CLOSED", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
