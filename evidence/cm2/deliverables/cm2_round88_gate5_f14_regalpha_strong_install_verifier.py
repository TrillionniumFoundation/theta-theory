#!/usr/bin/env python3
"""Fail-closed verifier for the Round88 fixed-density/F14 frontier."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import arb, ctx

import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as return_cert
import cm2_gate4_inner_core_strong_product_bridge_frontier_cert as strong_cert
import cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert as growth_cert
import cm2_round88_gate5_f14_regalpha_strong_install_cert as cert


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round88-gate5-f14-regalpha-strong-install-2026-07-22.json"
SCHEMA = "cm2.round88.gate5-f14-regalpha-strong-frontier.audit.v2"


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def strict_load_text(text: str) -> Any:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"duplicate key: {key}")
            out[key] = value
        return out

    return json.loads(
        text, object_pairs_hook=unique,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )


def strict_load(path: Path) -> dict[str, Any]:
    value = strict_load_text(path.read_text())
    if not isinstance(value, dict):
        raise ValueError("top-level object")
    return value


def aq(value: Q | str | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    if set(value) != expected:
        raise ValueError(f"{label} closed schema")


def independent_proposed_slot_key(row: dict[str, Any]) -> str:
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


def validate_schema(document: dict[str, Any]) -> None:
    exact_keys(document, {"schema", "pins", "result", "result_sha256"}, "top")
    if document["schema"] != cert.SCHEMA or document["pins"] != cert.PINS:
        raise ValueError("schema or pins")
    result = document["result"]
    exact_keys(result, {
        "status", "fixed_collision_density_Regalpha_synthesis_cost",
        "F14_regular_density_operator_cost", "finite_root_F14_slot_installation",
        "new_immutable_F14_slots_installed", "finite_root_candidate_local_maturity_before",
        "finite_root_candidate_local_maturity_after", "first_remaining_finite_root_field",
        "complete_18_field_operator_blocks", "global_Gate5", "strict_nonclaims",
        "evidence", "evidence_sha256",
    }, "result")
    if digest(result) != document["result_sha256"] or digest(result["evidence"]) != result["evidence_sha256"]:
        raise ValueError("digest")
    evidence = result["evidence"]
    exact_keys(evidence, {
        "precision_bits", "finite_root_packet_count", "completed_same_key_F10_slot_count",
        "installed_immutable_F14_slot_count", "proposed_F14_slot_key_count", "recipient",
        "intertwiner", "official_F14_interface_audit", "slot_rows",
    }, "evidence")
    exact_keys(evidence["recipient"], {
        "completion", "curve_class", "adapted_density_cone_constant", "canonical_delta_star",
        "Reg_alpha_crosswalk", "normalization_invariance",
    }, "recipient")
    exact_keys(evidence["intertwiner"], {
        "domain", "weighted_disintegration", "map", "codomain", "mass_term_upper",
        "Reg_alpha_term_strict_upper", "weighted_prechop_Z_strict_upper",
        "canonical_chop_Z_additive_upper", "operator_norm_strict_upper", "bounded",
    }, "intertwiner")
    exact_keys(evidence["official_F14_interface_audit"], {
        "required_field", "frozen_regular_density_prefix_suffix_intertwiner",
        "frozen_immutable_complete_return_word_operator_registry",
        "arbitrary_regular_density_input_supported", "branchwise_prefix_suffix_operator_supported",
        "fixed_profile_span_is_the_official_operator_domain", "conclusion",
    }, "official F14 audit")
    row_keys = {
        "atom_id", "candidate_packet_id", "physical_homogeneity_subbranch_id", "roof_level_j",
        "source_core_id", "destination_core_id", "completed_F10_slot_id", "completed_F10_value",
        "field_index", "field_name", "curve_slope_dphi_dr", "adapted_line_element",
        "conditional_density", "adapted_log_density_Lipschitz_strict_upper", "Reg_alpha_definition",
        "Reg_alpha_strict_upper_after_restriction_and_normalization", "canonical_delta_star",
        "properization", "weighted_prechop_Z_strict_upper", "canonical_chop_Z_additive_upper",
        "accepted_strong_source_norm", "accepted_strong_synthesis_cost_strict_upper",
        "proposed_F14_slot_key", "immutable_F14_slot_id", "F14_slot_status",
    }
    rows = evidence["slot_rows"]
    if not isinstance(rows, list) or len(rows) != 152:
        raise ValueError("slot row count")
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("slot row object")
        exact_keys(row, row_keys, "slot row")


def independent_recompute(document: dict[str, Any], bits: int = 1024) -> dict[str, Any]:
    ctx.prec = bits
    validate_schema(document)
    result = document["result"]
    evidence = result["evidence"]
    rows = evidence["slot_rows"]

    if result["status"] != "CERTIFIED_152_FIXED_COLLISION_DENSITY_REG_ALPHA_STRONG_SYNTHESIS__OFFICIAL_F14_OPEN":
        raise ValueError("status")
    if result["finite_root_F14_slot_installation"] != "NOT_CERTIFIED":
        raise ValueError("F14 noninstallation")
    if result["new_immutable_F14_slots_installed"] != 0:
        raise ValueError("F14 nonpromotion")
    if result["finite_root_candidate_local_maturity_before"] != "13/18" or result["finite_root_candidate_local_maturity_after"] != "13/18":
        raise ValueError("local maturity")
    if result["first_remaining_finite_root_field"] != "F14_regular_density_operator_cost":
        raise ValueError("next field")
    if result["complete_18_field_operator_blocks"] != 0 or result["global_Gate5"] != "NOT_CERTIFIED__10/18_BLOCKS_0":
        raise ValueError("global nonpromotion")

    strong = strong_cert.core_local_strong_multiplier()
    density = growth_cert.invariant_density_and_distortion()["invariant_adapted_density_cone"]
    growth = growth_cert.numeric_growth_and_recovery()["adapted_boundary_Growth_recurrence"]
    if strong["source_norm"] != evidence["recipient"]["completion"]:
        raise ValueError("strong completion")
    if density["density_constant"] != evidence["recipient"]["adapted_density_cone_constant"]:
        raise ValueError("density cone")
    delta = Q(density["canonical_maximum_adapted_curve_length"])
    if delta != Q(1, 10**90) or evidence["recipient"]["canonical_delta_star"] != str(delta):
        raise ValueError("delta star")
    chop = Q(growth["additive_mass_coefficient"])
    if chop != 2 * 10**90:
        raise ValueError("chop charge")
    expected_cost = chop + 4302
    if evidence["intertwiner"]["operator_norm_strict_upper"] != str(expected_cost):
        raise ValueError("operator cost")
    if result["fixed_collision_density_Regalpha_synthesis_cost"] != f"STRICTLY_LESS_THAN_{expected_cost}":
        raise ValueError("fixed-profile synthesis cost")
    if result["F14_regular_density_operator_cost"] != "NOT_CERTIFIED__NO_ARBITRARY_REGULAR_DENSITY_PREFIX_SUFFIX_INTERTWINER":
        raise ValueError("official F14 frontier")
    if evidence["intertwiner"]["Reg_alpha_term_strict_upper"] != "1/80" or evidence["intertwiner"]["bounded"] is not True:
        raise ValueError("Reg_alpha recipient")
    if evidence["intertwiner"]["weighted_prechop_Z_strict_upper"] != "4300" or evidence["intertwiner"]["canonical_chop_Z_additive_upper"] != str(chop):
        raise ValueError("Z intertwiner")
    interface = evidence["official_F14_interface_audit"]
    if interface != {
        "required_field": "regular_density_operator_cost",
        "frozen_regular_density_prefix_suffix_intertwiner": False,
        "frozen_immutable_complete_return_word_operator_registry": False,
        "arbitrary_regular_density_input_supported": False,
        "branchwise_prefix_suffix_operator_supported": False,
        "fixed_profile_span_is_the_official_operator_domain": False,
        "conclusion": "NO_OFFICIAL_F14_SLOT_MATERIALIZATION",
    }:
        raise ValueError("official F14 interface audit")
    norm_frontier = strict_load(cert.NORM_FRONTIER)["result"]["completion"]
    if norm_frontier["regular_density_prefix_suffix_intertwiner"] is not False or norm_frontier["immutable_complete_return_word_operator_registry"] is not False:
        raise ValueError("frozen norm frontier")

    round87 = strict_load(cert.ROUND87)["result"]
    windows = strict_load(cert.WINDOWS)["result"]["evidence"]["window_rows"]
    operator = strict_load(cert.OPERATOR)["result"]
    packets = strict_load(cert.PACKETS)["result"]["R1_inner_candidate_field_packet_rows"]
    prior_map = {row["atom_id"]: row for row in round87["evidence"]["integration_rows"]}
    window_map = {row["positive_atom_id"]: row for row in windows}
    attachment_map = {row["atom_id"]: row for row in operator["evidence"]["attachment_rows"]}
    packet_map = {row["atom_id"]: row for row in packets}
    cores = {return_cert.core_id(core): core for core in core_cert.physical_cores()}
    proposed_keys: set[str] = set()
    minimum_reg_margin: arb | None = None
    for row in rows:
        atom_id = row["atom_id"]
        if atom_id not in window_map or atom_id not in prior_map or atom_id not in attachment_map or atom_id not in packet_map:
            raise ValueError("same-key row")
        window = window_map[atom_id]
        prior = prior_map[atom_id]
        attach = attachment_map[atom_id]
        packet = packet_map[atom_id]
        if row["candidate_packet_id"] != prior["candidate_packet_id"] or row["candidate_packet_id"] != attach["candidate_packet_id"] or row["candidate_packet_id"] != packet["r1_candidate_field_packet_id"]:
            raise ValueError("packet crosswalk")
        if row["physical_homogeneity_subbranch_id"] != prior["physical_homogeneity_subbranch_id"] or row["physical_homogeneity_subbranch_id"] != attach["physical_homogeneity_subbranch_id"]:
            raise ValueError("branch crosswalk")
        if row["completed_F10_slot_id"] != attach["F10_slot_id"] or attach["F10_coarea_density_regular_cost"] != "0":
            raise ValueError("F10 dependency")
        if packet["roof"] != 1 or packet["roof_level_j"] != 0 or row["roof_level_j"] != 0:
            raise ValueError("roof")
        if row["source_core_id"] != window["source_core_id"] or row["destination_core_id"] != window["destination_core_id"]:
            raise ValueError("core crosswalk")
        core = cores[row["source_core_id"]]
        radius = Q(first_hit.RADIUS[core.source])
        p0, p1 = map(Q, window["common_p"])
        pmax = max(abs(p0), abs(p1))
        if pmax > Q(1, 50):
            raise ValueError("p core")
        # This recomputation uses the exact source radius rather than the
        # producer's displayed universal 36/2989 intermediate bound.
        log_lip = 4 * aq(pmax) / (1 - aq(pmax) ** 2).sqrt() / aq(1 / radius + 4)
        margin = aq(Q(1, 80)) - log_lip
        if not (margin > 0):
            raise ValueError("adapted Reg_alpha")
        minimum_reg_margin = margin if minimum_reg_margin is None else min(minimum_reg_margin, margin)
        if row["adapted_log_density_Lipschitz_strict_upper"] != "1/80" or row["Reg_alpha_strict_upper_after_restriction_and_normalization"] != "1/80":
            raise ValueError("row Reg_alpha")
        if row["canonical_delta_star"] != str(delta) or row["accepted_strong_synthesis_cost_strict_upper"] != str(expected_cost):
            raise ValueError("row properization")
        if row["field_index"] != 14 or row["field_name"] != "regular_density_operator_cost":
            raise ValueError("row field")
        if row["immutable_F14_slot_id"] != "NOT_MATERIALIZED" or row["F14_slot_status"] != "NOT_CERTIFIED__FIXED_PROFILE_SYNTHESIS_IS_NOT_THE_FULL_REGULAR_DENSITY_BRANCH_OPERATOR":
            raise ValueError("row F14 noninstallation")
        if row["proposed_F14_slot_key"] != independent_proposed_slot_key(row):
            raise ValueError("proposed slot key")
        proposed_keys.add(row["proposed_F14_slot_key"])

    if len(proposed_keys) != 152:
        raise ValueError("unique proposed keys")
    if evidence["finite_root_packet_count"] != 152 or evidence["completed_same_key_F10_slot_count"] != 152 or evidence["installed_immutable_F14_slot_count"] != 0 or evidence["proposed_F14_slot_key_count"] != 152:
        raise ValueError("evidence counts")
    if len(result["strict_nonclaims"]) != 6:
        raise ValueError("nonclaims")
    return {
        "bits": bits,
        "same_key_packet_crosswalks": 152,
        "completed_F10_dependencies": 152,
        "adapted_Reg_alpha_proofs": 152,
        "canonical_delta_star": str(delta),
        "canonical_chop_charge": str(chop),
        "proposed_F14_slot_keys": 152,
        "immutable_F14_slots": 0,
        "official_regular_density_prefix_suffix_intertwiner": "NOT_CERTIFIED",
        "minimum_adapted_log_lipschitz_margin": str(minimum_reg_margin),
        "verdict": "PASS",
    }


def rehash(document: dict[str, Any]) -> None:
    document["result"]["evidence_sha256"] = digest(document["result"]["evidence"])
    document["result_sha256"] = digest(document["result"])


def rejected(document: dict[str, Any], mutate: Callable[[dict[str, Any]], None]) -> bool:
    trial = copy.deepcopy(document)
    mutate(trial)
    rehash(trial)
    try:
        independent_recompute(trial, 768)
    except Exception:
        return True
    return False


def audit() -> dict[str, Any]:
    document = strict_load(MANIFEST)
    expected = cert.build(512)
    if document != expected:
        raise ValueError("producer cold-build mismatch")
    high = independent_recompute(document, 1024)

    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda x: x["result"].__setitem__("F14_regular_density_operator_cost", "CERTIFIED"),
        lambda x: x["result"].__setitem__("fixed_collision_density_Regalpha_synthesis_cost", "STRICTLY_LESS_THAN_2"),
        lambda x: x["result"].__setitem__("finite_root_candidate_local_maturity_after", "18/18"),
        lambda x: x["result"].__setitem__("new_immutable_F14_slots_installed", 4216),
        lambda x: x["result"].__setitem__("global_Gate5", "CERTIFIED"),
        lambda x: x["result"]["evidence"]["recipient"].__setitem__("canonical_delta_star", "1"),
        lambda x: x["result"]["evidence"]["intertwiner"].__setitem__("Reg_alpha_term_strict_upper", "0"),
        lambda x: x["result"]["evidence"]["intertwiner"].__setitem__("canonical_chop_Z_additive_upper", "0"),
        lambda x: x["result"]["evidence"]["official_F14_interface_audit"].__setitem__("arbitrary_regular_density_input_supported", True),
        lambda x: x["result"]["evidence"]["slot_rows"][0].__setitem__("immutable_F14_slot_id", "slot:r1:f14:fake"),
        lambda x: x["result"]["evidence"]["slot_rows"][0].__setitem__("proposed_F14_slot_key", "proposed-slot-key:r1:f14:fake"),
        lambda x: x["result"]["evidence"]["slot_rows"][0].__setitem__("completed_F10_slot_id", "slot:r1:f10:fake"),
        lambda x: x["result"]["evidence"]["slot_rows"][0].__setitem__("F14_slot_status", "CERTIFIED_GLOBAL"),
    ]
    hostile = [rejected(document, mutation) for mutation in mutations]
    if not all(hostile):
        raise ValueError("hostile mutation accepted")

    pin_results = []
    for key in sorted(cert.PINS):
        trial = copy.deepcopy(document)
        trial["pins"][key] = "0" * 64
        rehash(trial)
        try:
            independent_recompute(trial, 768)
        except Exception:
            pin_results.append(True)
        else:
            pin_results.append(False)
    if not all(pin_results):
        raise ValueError("pin mutation accepted")

    attacks = [
        '{"schema":"x","schema":"y"}',
        '{"x":NaN}',
        '[]',
        canonical({**document, "extra": True}),
    ]
    strict_rejected = 0
    for index, text in enumerate(attacks):
        try:
            value = strict_load_text(text)
            if not isinstance(value, dict):
                raise ValueError("top")
            validate_schema(value)
            if index == 3:
                raise ValueError("extra top accepted")
        except Exception:
            strict_rejected += 1
    if strict_rejected != 4:
        raise ValueError("strict JSON attack")

    result = {
        "producer_bits": 512,
        "independent_bits": 1024,
        "finite_root_packets": 152,
        "fixed_profile_Regalpha_synthesis": "CERTIFIED_152_OF_152",
        "installed_immutable_F14_slots": 0,
        "official_F14": "NOT_CERTIFIED",
        "finite_root_candidate_local_maturity": "13/18_UNCHANGED",
        "global_Gate5": "10/18_UNCHANGED",
        "complete_operator_blocks": 0,
        "independent_recomputation": high,
        "hostile_mutations_rejected": f"{sum(hostile)}/{len(hostile)}",
        "pin_mutations_rejected": f"{sum(pin_results)}/{len(pin_results)}",
        "strict_JSON_attacks_rejected": f"{strict_rejected}/4",
        "verdict": "PASS",
    }
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    try:
        print(canonical(audit()))
        return 0
    except Exception as exc:
        print(canonical({"schema": SCHEMA, "status": "FAIL_CLOSED", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
