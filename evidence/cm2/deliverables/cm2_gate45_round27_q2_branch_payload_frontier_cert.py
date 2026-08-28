#!/usr/bin/env python3
"""Round-27 typed branch payload frontier on all strict Q2-inner atoms.

The frozen round-26 time-two replay contains 114,006 whole source boxes that
avoid the complete 24-core union at collision times one and two.  This leaf
replays that registry and attaches exactly the payload that is already
licensed by those physical finite words:

* rational coordinate-base mass and an exact symbolic collision-area mass;
* the two-collision word and one immutable restriction ID shared by the
  forward and reverse Borel/smooth views;
* the invariant collision-area Jacobian 1 at each collision and for the
  two-step composition; and
* one symbolic, once-charged q2 expression using that same restriction and
  exact mass.

The leaf deliberately keeps three distinct Jacobians apart.  Preservation of
``dr dp`` does not say that the adaptive ``(t,p)`` coordinate Jacobian is one,
and it does not supply the one-dimensional unstable Jacobian.  The existing
universal unstable estimates therefore enter only as a conditional template:
after a physical homogeneity refinement at both collisions, the adapted
two-step inverse bound is theta^2 and the two canonical-recut distortion
contributions sum to less than 3/100000.  The round-26 atoms do not carry
homogeneity-child IDs, so no F5/F6 slot is installed.

Likewise the symbolic formula
``q2=max(C_fw,C_rev,2)*m2`` is not numerical because neither strong cost is
available on the common geometric recovery carriers.  F14--F18 remain empty.
This is an append-only, fail-closed frontier; it does not certify a complete
R2/Q2 partition, an arbitrary-n construction, a weighted tail, or Gate 4/5.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_round26_q1_time2_frontier_cert as time2_cert


Q = Fraction
HERE = Path(__file__).resolve().parent

RESULT_SCHEMA = "cm2.gate45.round27-q2-branch-payload-frontier.v1"
MANIFEST_SCHEMA = "cm2.gate45.round27-q2-branch-payload-frontier.manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json"
)

DEPENDENCIES = {
    "cm2_gate34_round26_q1_time2_frontier_cert.py": (
        "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9"
    ),
    "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json": (
        "9fe21726952e83e121536d2ad6344f586405c5699183f12d210929487190832d"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json": (
        "d532eeab0fa24901228a589724ffc4dbcff721f7d174a2b519187d77faab883b"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}

PARAMETER_WIDTH = core_cert.S_UPPER - core_cert.S_LOWER
RADIUS_SUM = time2_cert.first_hit.RADIUS["G"] + time2_cert.first_hit.RADIUS["W"]
THETA = Q(144000, 180337)
TWO_STEP_THETA = THETA * THETA
ONE_STEP_CANONICAL_LOG_VARIATION = Q(3, 200000)
TWO_STEP_CANONICAL_RECUT_LOG_VARIATION = 2 * ONE_STEP_CANONICAL_LOG_VARIATION
REQUIRED_FIELDS = (
    "nonempty_or_empty_domain_proof",
    "physical_homogeneity_subbranch_table",
    "homogeneous_prefix_chart",
    "homogeneous_suffix_chart",
    "inverse_Jacobian_bound",
    "log_Jacobian_distortion_sum",
    "one_step_cut_growth_Z_sum",
    "face_transversality_lower",
    "face_C2_atlas_bound",
    "coarea_density_regular_bound",
    "dynamic_Holder_test_pullback_bound",
    "C1_face_trace_pullback_bound",
    "moving_boundary_DQ_current_and_two_traces",
    "regular_density_operator_cost",
    "standard_family_operator_cost",
    "flux_face_operator_cost",
    "dynamic_test_operator_cost",
    "operator_phase_block",
)


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def parse_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def streaming_rows_digest(rows: Iterable[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for row in rows:
        digest.update(canonical_json(row).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency path: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        if path.suffix == ".json":
            value = parse_json_text(path.read_text(encoding="utf-8"))
            require(isinstance(value, dict), f"dependency JSON type: {name}")
            loaded[name] = value

    time2 = loaded[
        "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json"
    ]
    registry = time2["result"]["Q1_time2_adaptive_registry"]
    mass = time2["result"]["Q1_time2_mass_frontier"]
    require(registry["strict_Q2_inner_atom_count"] == 114006, "Q2 count")
    require(registry["strict_R2_inner_atom_count"] == 0, "depth-16 R2 count")
    require(
        mass["Q2_inner_base_mass"] == "5257799/5120000000",
        "Q2 base mass",
    )
    require(
        time2["verdict"]["complete_R2_Q2_partition"] == "NOT_CERTIFIED",
        "time2 frontier boundary",
    )

    core = loaded[
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ]["result"]["physical_return_core_registry"]
    require(core["physical_compact_homogeneous_core_count"] == 24, "core count")
    completion = core["full_key_schema_field_completion"]
    require(
        completion[
            "area_Jacobian_seed_is_not_unstable_curve_inverse_Jacobian_field"
        ]
        is True,
        "area/unstable separation",
    )
    require(
        completion[
            "log_area_seed_is_not_log_unstable_Jacobian_distortion_field"
        ]
        is True,
        "area/distortion separation",
    )

    universal = loaded[
        "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
    ]["result"]["universal_full_collision_branch_templates"]
    f5 = universal["field_5_inverse_Jacobian_seed"]
    f6 = universal["field_6_log_Jacobian_distortion_seed"]
    require(f5["physical_type"] == "adapted unstable one-dimensional Jacobian", "F5 type")
    require(f5["universal_adapted_inverse_strict_upper"] == qstr(THETA), "theta")
    require(f5["completed_full_key_roof_level_field"] is False, "F5 incomplete")
    require(
        f6["canonical_curve_log_variation_strict_upper"]
        == qstr(ONE_STEP_CANONICAL_LOG_VARIATION),
        "F6 variation",
    )
    require(f6["completed_full_key_roof_level_field"] is False, "F6 incomplete")

    schema = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["required_operator_field_schema"]
    require(tuple(schema["required_fields"]) == REQUIRED_FIELDS, "18-field schema")
    require(schema["homogeneous_subbranch_ids_materialized"] is False, "old F2 frontier")
    return loaded


def replay_time2_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], tuple[Any, ...]]:
    step1_manifest = time2_cert.load_step1_manifest()
    cores = core_cert.physical_cores()
    require(len(cores) == 24, "physical core replay")
    q1_rows = [
        row
        for row in step1_manifest["result"]["adaptive_full_core_step1_raw_leaf_rows"]
        if row["classification"] == "SURVIVE_THROUGH_1_INNER"
    ]
    require(len(q1_rows) == 2868, "Q1 parent replay")
    all_rows = time2_cert.adaptive_time2_rows(q1_rows, cores)
    time2_cert.verify_prefix_and_mass(q1_rows, all_rows)
    q2_rows = [
        row for row in all_rows if row["classification"] == "SURVIVE_THROUGH_2_INNER"
    ]
    require(len(all_rows) == 416994, "time2 leaf replay")
    require(len(q2_rows) == 114006, "Q2 leaf replay")
    require(
        sum(Q(row["parameter_averaged_unnormalized_base_mass"]) for row in q2_rows)
        == Q(5257799, 5120000000),
        "Q2 replay base mass",
    )
    return q1_rows, q2_rows, cores


def exact_mass_payload(row: dict[str, Any], source: str) -> dict[str, Any]:
    box = row["source_box"]
    t0, t1 = Q(box["t"][0]), Q(box["t"][1])
    p0, p1 = Q(box["p"][0]), Q(box["p"][1])
    s0, s1 = Q(box["s"][0]), Q(box["s"][1])
    require(t0 < t1 and p0 < p1 and s0 < s1, "positive Q2 box")
    radius = time2_cert.first_hit.RADIUS[source]
    fixed_fibre_coefficient = radius * (p1 - p0)
    averaged_coefficient = fixed_fibre_coefficient * (s1 - s0) / PARAMETER_WIDTH
    normalized_fixed_fibre_coefficient = fixed_fibre_coefficient / (4 * RADIUS_SUM)
    normalized_averaged_coefficient = averaged_coefficient / (4 * RADIUS_SUM)
    theta_width = f"asin({qstr(t1)})-asin({qstr(t0)})"
    rational_base = Q(row["parameter_averaged_unnormalized_base_mass"])
    require(rational_base == radius * (t1 - t0) * (p1 - p0) * (s1 - s0) / PARAMETER_WIDTH, "row base mass")
    payload = {
        "time2_atom_id": row["time2_atom_id"],
        "coordinate_base_mass_exact_rational": qstr(rational_base),
        "coordinate_base_measure": "R_source*dt*dp averaged over the full s-window",
        "fixed_fibre_unnormalized_collision_area_mass_exact": (
            f"{qstr(fixed_fibre_coefficient)}*({theta_width})"
        ),
        "parameter_averaged_unnormalized_collision_area_mass_exact": (
            f"{qstr(averaged_coefficient)}*({theta_width})"
        ),
        "fixed_fibre_normalized_collision_SRB_mass_exact": (
            f"{qstr(normalized_fixed_fibre_coefficient)}*({theta_width})/pi"
        ),
        "parameter_averaged_normalized_collision_SRB_mass_exact": (
            f"{qstr(normalized_averaged_coefficient)}*({theta_width})/pi"
        ),
        "strict_comparison_to_coordinate_base": (
            "base_mass < collision_area_mass < (1401/1000)*base_mass"
        ),
        "rational_base_mass_is_not_renamed_exact_collision_SRB_mass": True,
    }
    payload["mass_slot_id"] = "mass:q2:" + canonical_digest(payload)
    return payload


def strong_template() -> dict[str, Any]:
    payload = {
        "scope": (
            "each connected two-collision child after physical owner and homogeneity "
            "refinement at both collision steps, with canonical recut before each step"
        ),
        "one_step_adapted_unstable_inverse_strict_upper": qstr(THETA),
        "conditional_two_step_adapted_unstable_inverse_strict_upper": qstr(TWO_STEP_THETA),
        "one_step_canonical_recut_log_variation_strict_upper": qstr(
            ONE_STEP_CANONICAL_LOG_VARIATION
        ),
        "conditional_two_step_canonical_recut_log_variation_strict_upper": qstr(
            TWO_STEP_CANONICAL_RECUT_LOG_VARIATION
        ),
        "composition_rules": [
            "||(D(T^2)|Eu)^-1|| <= ||(DT|Eu)^-1 at time1||*||(DT|Eu)^-1 at time2||",
            "osc(log J^u T^2) <= osc(log J^u T at step1)+osc(log J^u T at step2)",
        ],
        "required_missing_row_fields": [
            "time1_physical_homogeneity_child_id",
            "time2_physical_homogeneity_child_id",
            "canonical_recut_component_ids",
        ],
        "applies_directly_to_unsplit_Q2_atom": False,
        "F5_materialized_slot_count": 0,
        "F6_materialized_slot_count": 0,
    }
    payload["conditional_template_id"] = (
        "template:q2:conditional-unstable:" + canonical_digest(payload)
    )
    return payload


def branch_payload_row(
    row: dict[str, Any], cores: tuple[Any, ...], template_id: str
) -> dict[str, Any]:
    require(row["classification"] == "SURVIVE_THROUGH_2_INNER", "Q2 row type")
    require(row["owner_status"] == "strict_unique_second_collision_owner", "Q2 owner")
    require(row["destination_core_id"] is None, "Q2 destination")
    require(row["selected_second_target_id"] is not None, "Q2 second target")
    require(row["canonical_invariant_area_Jacobian_per_regular_collision"] == "1", "area seed")
    index = row["source_core_index"]
    core = cores[index]
    source_core_id = time2_cert.step1.core_id(core)
    collision_word = [
        f"{core.source}:source-core-chart",
        core.target_id,
        row["selected_second_target_id"],
    ]
    branch_identity = {
        "time2_atom_id": row["time2_atom_id"],
        "Q1_parent_atom_id": row["Q1_parent_atom_id"],
        "refinement_suffix": row["refinement_suffix"],
        "source_core_id": source_core_id,
        "source_box": row["source_box"],
        "collision_word": collision_word,
        "clock": "source_core_time0_then_strict_outside_at_time1_and_time2",
    }
    restriction_id = "restriction:q2:" + canonical_digest(branch_identity)
    mass = exact_mass_payload(row, core.source)
    area_payload = {
        "restriction_id": restriction_id,
        "invariant_coordinates": "collision Birkhoff (r,p)",
        "per_regular_collision_area_Jacobian": ["1", "1"],
        "two_collision_area_Jacobian": "1",
        "adaptive_t_p_coordinate_Jacobian_claimed_equal_to_one": False,
        "unstable_one_dimensional_Jacobian_claimed_equal_to_one": False,
    }
    area_slot_id = "jacobian:q2:area:" + canonical_digest(area_payload)
    charge_payload = {
        "restriction_id": restriction_id,
        "mass_slot_id": mass["mass_slot_id"],
        "formula": "q2=max(C_fw(restriction_id),C_rev(restriction_id),2)*m2",
        "forward_and_reverse_views_are_nonadditive": True,
        "same_mass_charged_once": True,
        "numeric_C_fw_available": False,
        "numeric_C_rev_available": False,
        "numeric_q2_available": False,
    }
    symbolic_charge_id = "charge:q2:symbolic:" + canonical_digest(charge_payload)
    return {
        "time2_atom_id": row["time2_atom_id"],
        "source_core_id": source_core_id,
        "source_box_sha256": canonical_digest(row["source_box"]),
        "collision_word": collision_word,
        "mass_slot_id": mass["mass_slot_id"],
        "coordinate_base_mass_exact_rational": mass[
            "coordinate_base_mass_exact_rational"
        ],
        "fixed_fibre_unnormalized_collision_area_mass_exact": mass[
            "fixed_fibre_unnormalized_collision_area_mass_exact"
        ],
        "parameter_averaged_unnormalized_collision_area_mass_exact": mass[
            "parameter_averaged_unnormalized_collision_area_mass_exact"
        ],
        "restriction_id": restriction_id,
        "forward_view_id": "view:q2:fw:" + canonical_digest(
            {"restriction_id": restriction_id, "orientation": "forward_T2"}
        ),
        "reverse_view_id": "view:q2:rev:" + canonical_digest(
            {"restriction_id": restriction_id, "orientation": "reverse_Tminus2"}
        ),
        "area_Jacobian_slot_id": area_slot_id,
        "two_collision_invariant_area_Jacobian": "1",
        "conditional_unstable_template_id": template_id,
        "time1_homogeneity_child_id": None,
        "time2_homogeneity_child_id": None,
        "F5_unstable_Jacobian_slot_materialized": False,
        "F6_unstable_distortion_slot_materialized": False,
        "symbolic_q2_charge_id": symbolic_charge_id,
        "numeric_strong_q2": None,
    }


def downstream_frontier() -> dict[str, Any]:
    reasons = {
        REQUIRED_FIELDS[13]: (
            "no branchwise regular-density cost: physical homogeneity rows and F10 are absent"
        ),
        REQUIRED_FIELDS[14]: (
            "no Q2 characteristic-boundary F7 sum or survivor-conditioned standard-family recovery"
        ),
        REQUIRED_FIELDS[15]: (
            "no physical moving face/coarea/DQ atlas on the Q2 branch registry"
        ),
        REQUIRED_FIELDS[16]: (
            "no return-wide dynamic test current and no numerical common-carrier C_fw/C_rev"
        ),
        REQUIRED_FIELDS[17]: "F14-F17 are not assembled into an operator block",
    }
    rows = [
        {
            "field_index": index,
            "field_name": REQUIRED_FIELDS[index - 1],
            "materialized_Q2_slot_count": 0,
            "status": "NOT_CERTIFIED",
            "first_missing_dependency": reasons[REQUIRED_FIELDS[index - 1]],
        }
        for index in range(14, 19)
    ]
    return {
        "rows": rows,
        "rows_sha256": canonical_digest(rows),
        "F14_through_F18_materialized_Q2_slot_count": 0,
        "first_missing_strong_field_on_the_Q2_candidate_schema": {
            "field_index": 2,
            "field_name": REQUIRED_FIELDS[1],
            "reason": (
                "round26 materializes strict collision owners but no physical "
                "homogeneity-child IDs at either step"
            ),
        },
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    _q1_rows, q2_rows, cores = replay_time2_rows()
    template = strong_template()

    ledger_digest = hashlib.sha256()
    mass_digest = hashlib.sha256()
    restriction_ids: set[str] = set()
    mass_ids: set[str] = set()
    area_ids: set[str] = set()
    charge_ids: set[str] = set()
    source_histogram: Counter[str] = Counter()
    word_histogram: Counter[str] = Counter()
    base_denominator_histogram: Counter[int] = Counter()
    representatives: list[dict[str, Any]] = []
    base_total = Q(0)

    for index, row in enumerate(q2_rows):
        payload = branch_payload_row(row, cores, template["conditional_template_id"])
        canonical = canonical_json(payload).encode("utf-8")
        ledger_digest.update(canonical)
        ledger_digest.update(b"\n")
        mass_projection = {
            key: payload[key]
            for key in (
                "time2_atom_id",
                "mass_slot_id",
                "coordinate_base_mass_exact_rational",
                "fixed_fibre_unnormalized_collision_area_mass_exact",
                "parameter_averaged_unnormalized_collision_area_mass_exact",
            )
        }
        mass_digest.update(canonical_json(mass_projection).encode("utf-8"))
        mass_digest.update(b"\n")
        require(payload["restriction_id"] not in restriction_ids, "restriction ID uniqueness")
        require(payload["mass_slot_id"] not in mass_ids, "mass ID uniqueness")
        require(payload["area_Jacobian_slot_id"] not in area_ids, "area ID uniqueness")
        require(payload["symbolic_q2_charge_id"] not in charge_ids, "charge ID uniqueness")
        restriction_ids.add(payload["restriction_id"])
        mass_ids.add(payload["mass_slot_id"])
        area_ids.add(payload["area_Jacobian_slot_id"])
        charge_ids.add(payload["symbolic_q2_charge_id"])
        source_histogram[payload["source_core_id"]] += 1
        word_histogram[" -> ".join(payload["collision_word"])] += 1
        base = Q(payload["coordinate_base_mass_exact_rational"])
        base_total += base
        base_denominator_histogram[base.denominator] += 1
        if index in (0, len(q2_rows) // 2, len(q2_rows) - 1):
            representatives.append(payload)

    require(len(restriction_ids) == 114006, "restriction count")
    require(len(mass_ids) == len(area_ids) == len(charge_ids) == 114006, "slot counts")
    require(base_total == Q(5257799, 5120000000), "base total")
    require(all(value > 0 for value in source_histogram.values()), "source histogram")

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "source_registry": "round26 strict Q2-inner depth<=16 admitted atoms",
            "physical_clock": "source core at time0; strict C24 avoidance at times1 and2",
            "replay_engine": "fresh round26 384-bit Arb whole-box geometry",
        },
        "Q2_exact_mass_and_restriction_registry": {
            "strict_Q2_inner_atom_count": 114006,
            "exact_coordinate_base_mass_slot_count": len(mass_ids),
            "exact_symbolic_collision_area_mass_slot_count": len(mass_ids),
            "parameter_averaged_coordinate_base_mass_exact": qstr(base_total),
            "mass_ledger_rows_sha256": mass_digest.hexdigest(),
            "common_forward_reverse_restriction_id_count": len(restriction_ids),
            "forward_view_id_count": len(restriction_ids),
            "reverse_view_id_count": len(restriction_ids),
            "branch_payload_rows_sha256": ledger_digest.hexdigest(),
            "source_core_histogram": dict(sorted(source_histogram.items())),
            "source_core_histogram_sha256": canonical_digest(dict(sorted(source_histogram.items()))),
            "distinct_collision_word_count": len(word_histogram),
            "collision_word_histogram_sha256": canonical_digest(dict(sorted(word_histogram.items()))),
            "coordinate_base_mass_denominator_histogram": {
                str(key): value for key, value in sorted(base_denominator_histogram.items())
            },
            "representative_rows": representatives,
            "forward_reverse_views_share_one_restriction_and_one_mass": True,
            "target_image_carrier_formula": "B_atom,s=T_s^2(A_atom,s)",
            "restriction_is_smooth_and_invertible_on_each_regular_fixed_s_slice": True,
            "common_strong_recovery_carrier_count": 0,
        },
        "Q2_invariant_area_Jacobian_registry": {
            "per_collision_area_Jacobian_slot_count": 2 * len(area_ids),
            "two_collision_composed_area_Jacobian_slot_count": len(area_ids),
            "per_collision_value": "1",
            "two_collision_composed_value": "1",
            "invariant_measure_type": "collision Birkhoff dr dp at fixed s",
            "adaptive_t_p_coordinate_Jacobian_is_one": False,
            "invariant_area_Jacobian_is_unstable_curve_Jacobian": False,
            "invariant_area_log_distortion_is_F6": False,
        },
        "Q2_conditional_unstable_payload_template": template,
        "Q2_symbolic_strong_charge_registry": {
            "symbolic_q2_charge_count": len(charge_ids),
            "formula": "q2_atom=max(C_fw(atom),C_rev(atom),2)*m2_atom",
            "same_restriction_id_and_exact_mass_used_by_both_views": True,
            "two_views_are_not_two_charges": True,
            "numeric_C_fw_count": 0,
            "numeric_C_rev_count": 0,
            "numeric_q2_count": 0,
            "strong_q2_weighted_mass_sum": "NOT_CERTIFIED",
        },
        "Q2_F14_F18_frontier": downstream_frontier(),
        "strict_nonpromotion": {
            "complete_limiting_R2_Q2_partition": "NOT_CERTIFIED",
            "depth16_R2_admitted_count_zero_means_physical_R2_empty": False,
            "arbitrary_n_Rn_Qn_partition": "NOT_CERTIFIED",
            "homogeneity_subbranch_rows_on_Q2_atoms": 0,
            "F5_unstable_Jacobian_slots": 0,
            "F6_unstable_distortion_slots": 0,
            "F14_through_F18_slots": 0,
            "collision_area_Jacobian_promoted_to_unstable_Jacobian": False,
            "coordinate_base_mass_promoted_to_exact_collision_SRB_mass": False,
            "symbolic_q2_promoted_to_numeric_q2": False,
            "common_Borel_smooth_restriction_promoted_to_common_strong_recovery_carrier": False,
            "strong_q_weighted_tail": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def verdict(result: dict[str, Any]) -> dict[str, Any]:
    registry = result["Q2_exact_mass_and_restriction_registry"]
    return {
        "Q2_exact_mass_slots": f"CERTIFIED_{registry['exact_symbolic_collision_area_mass_slot_count']}",
        "Q2_common_fw_rev_restriction_ids": f"CERTIFIED_{registry['common_forward_reverse_restriction_id_count']}",
        "Q2_two_collision_invariant_area_Jacobians": "CERTIFIED_114006",
        "Q2_symbolic_once_charged_q2": "CERTIFIED_114006",
        "Q2_numeric_strong_q2": "NOT_CERTIFIED",
        "Q2_F5_F6": "NOT_CERTIFIED",
        "Q2_F14_F18": "NOT_CERTIFIED",
        "arbitrary_n_Rn_Qn": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def write_manifest(path: Path, verifier_path: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier_path.resolve()),
        "dependencies": dict(DEPENDENCIES),
        "result": result,
        "verdict": verdict(result),
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate45_round27_q2_branch_payload_frontier_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest is not None:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    registry = result["Q2_exact_mass_and_restriction_registry"]
    print("Q2_EXACT_MASS_AND_COMMON_RESTRICTION_PAYLOAD: CERTIFIED")
    print(f"Q2_ATOMS: {registry['strict_Q2_inner_atom_count']}")
    print(f"Q2_COORDINATE_BASE_MASS: {registry['parameter_averaged_coordinate_base_mass_exact']}")
    print("Q2_TWO_COLLISION_INVARIANT_AREA_JACOBIAN: 1")
    print("Q2_UNSTABLE_JACOBIAN_DISTORTION: CONDITIONAL_TEMPLATE_ONLY")
    print("Q2_NUMERIC_STRONG_Q2: NOT_CERTIFIED")
    print("Q2_F14_F18: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    sys.exit(main())
