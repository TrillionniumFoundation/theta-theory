#!/usr/bin/env python3
"""Join 4,216 full-dimensional R1-inner candidates to Gate-5 fields 1--7.

The round-25 adaptive C24 leaf materializes positive two-dimensional
first-return-at-one inner atoms.  Every such atom comes from a roof-one
central source core and lands strictly inside a central destination core.
This certificate independently binds each atom to the selected Gate-5 source
component and verifies the *candidate-local* status of fields F1--F7.  The
upstream adaptive registry has a nonempty unresolved outer cover, so none of
these rows is a complete physical R1 partition or a global Gate-5 roof level.

F1--F6 become immutable candidate-local slots on every R1-inner atom.  In
particular, F2 is a one-row central-to-central physical homogeneity table,
while the universal pointwise inverse-Jacobian and log-distortion estimates
become F5/F6 slots because restriction cannot worsen either bound.

F7 deliberately does not transfer.  Every adaptive atom has artificial
dyadic source/parameter faces.  The strict destination-core test classifies
the whole rectangle; it does not materialize destination-preimage boundary
faces.  The frozen maximal-word/component characteristic-Z theorem charges
only the physical word/component boundary grammar.  No new Z bound for the
artificial adaptive faces is present, so the parent F7 slot is kept only as
provenance and is not installed on the R1 atom.

The result is candidate/local maturity 6/18 on each materialized R1-inner
atom.  It creates zero complete 18-field blocks and gives zero new global
Gate-5 maturity credit; the frozen global Gate-5 maturity remains 4/18.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate25_selected_component_chart_field_slots_cert as chart_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as adaptive_cert


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": (
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24"
    ),
    "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json": (
        "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate25_selected_component_chart_field_slots_cert.py": (
        "666e7f1ea4198528b143b522d2c5daf55ba4fecfd127d86663b23e0bb38a477f"
    ),
    "cm2-gate25-selected-component-chart-field-slots-manifest-2026-07-17.json": (
        "417464531cae76bf774bdc35f1d2f25799237d1efde39be8850cf3408740f271"
    ),
    "cm2-gate25-selected-component-field7-slot-frontier-manifest-2026-07-17.json": (
        "75de341183ef7fbcc7937f69bc7c6f276d06db0883397a7c99e4d54bbc5dc91a"
    ),
    "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json": (
        "d532eeab0fa24901228a589724ffc4dbcff721f7d174a2b519187d77faab883b"
    ),
    "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json": (
        "41c766d25b007944313db93b389a616d086a7318700a867e13d90aedd159be35"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}

CANDIDATE_LOCAL_FIELDS = (
    "nonempty_or_empty_domain_proof",
    "physical_homogeneity_subbranch_table",
    "homogeneous_prefix_chart",
    "homogeneous_suffix_chart",
    "inverse_Jacobian_bound",
    "log_Jacobian_distortion_sum",
)
FIELD7 = "one_step_cut_growth_Z_sum"
PARAMETER_LOWER = Q(-1, 400)
PARAMETER_UPPER = Q(1, 400)


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


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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

    adaptive = loaded[
        "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
    ]
    require(
        adaptive["verdict"]["positive_full_dimensional_R1_inner_branches"]
        == "CERTIFIED",
        "R1 inner verdict",
    )
    registry = adaptive["result"]["adaptive_full_core_step1_registry"]
    require(registry["classification_histogram"]["RETURN_AT_1_INNER"] == 4216, "R1 count")
    require(registry["source_phase_dimension_at_fixed_parameter"] == 2, "source dimension")
    require(registry["step1_collision_singular_atom_count"] == 0, "step1 singular count")
    require(
        adaptive["verdict"]["unresolved_step1_outer_cover"] == "NONEMPTY",
        "unresolved cover",
    )

    selected = loaded[
        "cm2-gate25-selected-component-chart-field-slots-manifest-2026-07-17.json"
    ]["result"]
    require(
        selected["Gate5_maturity_update"][
            "completed_field_count_on_each_selected_component_level"
        ]
        == 4,
        "prior 4/18 maturity",
    )
    require(
        selected["Gate5_maturity_update"]["field_5_6_completed_roof_level_slot_count"]
        == 0,
        "prior F5/F6 slot count",
    )

    universal = loaded[
        "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
    ]["result"]["universal_full_collision_branch_templates"]
    require(
        universal["scope"].startswith("every actual homogeneous physical solid-collision child"),
        "universal template scope",
    )
    require(
        universal["canonical_adapted_length_upper"] == "1e-90",
        "canonical carrier length",
    )
    require(
        universal["field_5_inverse_Jacobian_seed"][
            "universal_adapted_inverse_strict_upper"
        ]
        == "144000/180337",
        "F5 bound",
    )
    require(
        universal["field_6_log_Jacobian_distortion_seed"][
            "canonical_curve_log_variation_strict_upper"
        ]
        == "3/200000",
        "F6 bound",
    )
    require(
        universal["field_6_log_Jacobian_distortion_seed"][
            "all_standard_curve_constant"
        ]
        == "15000000000000000000000000",
        "F6 all-curve constant",
    )

    characteristic = loaded[
        "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json"
    ]["result"]
    boundary = characteristic["set_theoretic_boundary_inheritance"]
    require(
        boundary["relative_boundary_inclusion"].startswith("boundary(D_w(s))"),
        "F7 boundary scope",
    )
    require(
        characteristic["operator_field_frontier"][
            "full_key_field7_finite_characteristic_formula"
        ]
        == "CERTIFIED",
        "parent F7 formula",
    )

    schema = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["required_operator_field_schema"]
    require(schema["required_field_count_per_physical_homogeneous_level"] == 18, "schema count")
    require(
        tuple(schema["required_fields"][:7])
        == CANDIDATE_LOCAL_FIELDS + (FIELD7,),
        "F1-F7 order",
    )
    return loaded


def selected_source_bindings() -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    loaded = chart_cert.load_dependencies()
    selected = loaded[
        "cm2-gate25-selected-component-field7-slot-frontier-manifest-2026-07-17.json"
    ]
    walls = loaded[
        "cm2-gate25-roof-two-wall-chart-frontier-manifest-2026-07-16.json"
    ]
    universal = loaded[
        "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
    ]
    chart_rows, seed_packets, registry = chart_cert.materialize_chart_slots(
        selected, walls, universal
    )
    require(registry["materialized_chart_field_slot_count"] == 56, "chart slots")
    require(len(seed_packets) == 24, "seed packets")

    components = {
        canonical_json(row["physical_key"]): row
        for row in selected["result"]["selected_component_rows"]
    }
    require(len(components) == 24, "unique selected components")
    charts = {
        (
            row["maximal_component_id"],
            row["homogeneous_subbranch_id"],
            row["roof_level_j"],
            row["field_name"],
        ): row
        for row in chart_rows
    }
    require(len(charts) == 56, "unique chart slots")
    field7 = {
        (
            row["maximal_component_id"],
            row["homogeneous_subbranch_id"],
            row["roof_level_j"],
        ): row
        for row in selected["result"]["materialized_field7_level_slots"]
    }
    require(len(field7) == 28, "unique parent F7 slots")
    packets = {
        row["maximal_component_id"]: row for row in seed_packets
    }
    require(len(packets) == 24, "unique seed packets")

    bindings: dict[str, dict[str, Any]] = {}
    for core in core_cert.physical_cores():
        identifier = adaptive_cert.core_id(core)
        physical_key = chart_cert.exact_key(core)
        component = components[canonical_json(physical_key)]
        component_id = component["maximal_component_id"]
        parent_h = component["selected_homogeneous_component_row_id"]
        roof = component["roof"]
        require(roof == len(core.crossings) + 1, "roof binding")
        level_rows = []
        for level in range(roof):
            f3 = charts[(component_id, parent_h, level, "homogeneous_prefix_chart")]
            f4 = charts[(component_id, parent_h, level, "homogeneous_suffix_chart")]
            f7 = field7[(component_id, parent_h, level)]
            level_rows.append({
                "roof_level_j": level,
                "parent_F3_slot_id": f3["immutable_slot_id"],
                "parent_F3_prefix_chart": f3["field_value"],
                "parent_F4_slot_id": f4["immutable_slot_id"],
                "parent_F4_suffix_chart": f4["field_value"],
                "parent_F7_slot_id": f7["immutable_slot_id"],
                "parent_F7_multiplier_upper": f7["field_7_multiplier_upper"],
            })
        packet = packets[component_id]
        require(
            packet["component_local_seed_is_complete_roof_level_slot"] is False,
            "prior seed typing",
        )
        payload = {
            "source_core_id": identifier,
            "physical_key": physical_key,
            "source_chart_id": core.chart_id,
            "physical_target_id": core.target_id,
            "transparent_wall_record": list(core.crossings),
            "roof": roof,
            "maximal_component_id": component_id,
            "parent_selected_homogeneous_component_row_id": parent_h,
            "source_and_target_central_homogeneity": component[
                "source_and_target_central_homogeneity"
            ],
            "level_rows": level_rows,
        }
        payload["source_binding_id"] = "r1-source-binding:" + canonical_digest(payload)
        bindings[identifier] = payload
    require(len(bindings) == 24, "source binding count")
    return bindings, {
        "all_source_binding_count": 24,
        "all_source_binding_rows_sha256": canonical_digest(
            [bindings[key] for key in sorted(bindings)]
        ),
    }


def field_templates(loaded: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    universal = loaded[
        "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
    ]["result"]["universal_full_collision_branch_templates"]
    f5 = universal["field_5_inverse_Jacobian_seed"]
    f6 = universal["field_6_log_Jacobian_distortion_seed"]
    templates: dict[str, dict[str, Any]] = {
        "F1": {
            "field": CANDIDATE_LOCAL_FIELDS[0],
            "value": "NONEMPTY_ON_OWNED_ADAPTIVE_BOX_EMPTY_OUTSIDE",
            "proof": "positive_two_dimensional_source_rectangle_at_each_guarded_s",
        },
        "F2": {
            "field": CANDIDATE_LOCAL_FIELDS[1],
            "table_shape": "one_row_central_source_to_central_target",
            "central_label": "H0:abs(p)<3/10",
            "intermediate_solid_collision_count": 0,
            "transparent_wall_level_count": 0,
        },
        "F5": {
            "field": CANDIDATE_LOCAL_FIELDS[4],
            "physical_type": f5["physical_type"],
            "carrier_quantifier": (
                "each connected component of W intersect A_atom, where W is a "
                "canonical adapted unstable standard curve of length at most 1e-90 "
                "inside the frozen smooth parent collision child"
            ),
            "central_child_adapted_inverse_strict_upper": f5[
                "central_child_adapted_inverse_strict_upper"
            ],
            "universal_adapted_inverse_strict_upper": f5[
                "universal_adapted_inverse_strict_upper"
            ],
            "universal_Euclidean_inverse_Jacobian_strict_upper": f5[
                "universal_Euclidean_inverse_Jacobian_strict_upper"
            ],
            "restriction_monotonicity": (
                "a pointwise inverse-Jacobian upper remains valid after domain restriction"
            ),
            "invariant_area_Jacobian_used": False,
        },
        "F6": {
            "field": CANDIDATE_LOCAL_FIELDS[5],
            "physical_type": (
                "leafwise log-distortion of the adapted unstable one-dimensional Jacobian"
            ),
            "carrier_quantifier": (
                "each connected component of W intersect A_atom on the same frozen "
                "smooth parent collision child, with W canonical adapted length at most 1e-90"
            ),
            "Holder_exponent": f6["Holder_exponent"],
            "all_standard_curve_constant": f6["all_standard_curve_constant"],
            "canonical_curve_log_variation_strict_upper": f6[
                "canonical_curve_log_variation_strict_upper"
            ],
            "restriction_monotonicity": (
                "log-Jacobian oscillation on a subset is at most the parent-child oscillation"
            ),
            "canonical_variation_derivation": (
                "15000000000000000000000000*(1e-90)^(1/3)=3/200000"
            ),
            "invariant_area_Jacobian_used": False,
        },
    }
    for key, value in templates.items():
        value["template_id"] = f"template:{key}:" + canonical_digest(value)
    return templates


def fraction_pair(values: list[str]) -> tuple[Q, Q]:
    require(isinstance(values, list) and len(values) == 2, "fraction pair")
    return Q(values[0]), Q(values[1])


def materialize_r1_blocks(
    adaptive: dict[str, Any],
    bindings: dict[str, dict[str, Any]],
    templates: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    physical_cores = core_cert.physical_cores()
    require(len(physical_cores) == 24, "physical core count")
    all_cores = {adaptive_cert.core_id(core): core for core in physical_cores}
    require(len(all_cores) == 24, "unique physical core ids")
    require(
        core_cert.S_LOWER == PARAMETER_LOWER
        and core_cert.S_UPPER == PARAMETER_UPPER,
        "parameter interval binding",
    )
    raw_rows = adaptive["result"]["adaptive_full_core_step1_raw_leaf_rows"]
    r1_rows = [row for row in raw_rows if row["classification"] == "RETURN_AT_1_INNER"]
    require(len(r1_rows) == 4216, "filtered R1 count")

    blocks: list[dict[str, Any]] = []
    source_histogram: Counter[str] = Counter()
    destination_histogram: Counter[str] = Counter()
    depth_histogram: Counter[int] = Counter()
    slot_ids: set[str] = set()
    h_ids: set[str] = set()
    atom_ids: set[str] = set()
    for row in r1_rows:
        require(row["atom_id"] not in atom_ids, "duplicate R1 atom id")
        atom_ids.add(row["atom_id"])
        require(row["positive_two_dimensional_source_rectangle_at_each_s"] is True, "positive 2D")
        require(row["positive_parameter_interval"] is True, "positive parameter")
        require(row["strict_next_collision_owner_inherited_from_whole_parent_core"] is True, "owner")
        require(row["complete_retained_candidate_comparison_inherited"] is True, "candidate comparison")
        require(row["absolute_inverse_invariant_area_Jacobian"] == "1", "area Jacobian")
        require(row["log_invariant_area_Jacobian_distortion"] == "0", "area distortion")
        require(row["destination_core_id"] in all_cores, "destination core")
        require(row["depth"] == len(row["dyadic_path"]) and row["depth"] > 0, "dyadic depth")

        source = all_cores[row["source_core_id"]]
        destination = all_cores[row["destination_core_id"]]
        binding = bindings[row["source_core_id"]]
        require(binding["roof"] == 1, "R1 source roof is one")
        require(source.crossings == (), "R1 source has no wall level")
        require(len(binding["level_rows"]) == 1, "one roof level")

        t0, t1 = fraction_pair(row["source_box"]["t"])
        p0, p1 = fraction_pair(row["source_box"]["p"])
        s0, s1 = fraction_pair(row["source_box"]["s"])
        require(source.t0 <= t0 < t1 <= source.t1, "source t containment")
        require(source.p0 <= p0 < p1 <= source.p1, "source p containment")
        require(PARAMETER_LOWER <= s0 < s1 <= PARAMETER_UPPER, "parameter containment")
        require(max(abs(source.p0), abs(source.p1)) <= Q(1, 50), "source central p")
        require(max(abs(destination.p0), abs(destination.p1)) <= Q(1, 50), "target central p")
        require(Q(1, 50) < Q(3, 10), "central strip margin")

        artificial_face = (
            t0 != source.t0
            or t1 != source.t1
            or p0 != source.p0
            or p1 != source.p1
            or s0 != PARAMETER_LOWER
            or s1 != PARAMETER_UPPER
        )
        require(artificial_face, "adaptive artificial face")

        h_payload = {
            "atom_id": row["atom_id"],
            "source_core_id": row["source_core_id"],
            "destination_core_id": row["destination_core_id"],
            "source_label": "H0:abs(p)<3/10",
            "target_label": "H0:abs(p)<3/10",
            "intermediate_solid_collision_count": 0,
            "transparent_wall_level_count": 0,
            "complete_table_row_count": 1,
        }
        h_id = "h:r1:" + canonical_digest(h_payload)
        require(h_id not in h_ids, "duplicate R1 h id")
        h_ids.add(h_id)

        guard = {
            "s_lower": str(s0),
            "s_upper": str(s1),
            "lower_closed": True,
            "upper_closed": s1 == PARAMETER_UPPER,
            "internal_boundary_owner": (
                "right_leaf_via_lower_closed_upper_open_convention"
            ),
        }
        candidate_domain = {
            "closed_box_provenance": row["source_box"],
            "owned_set_convention": (
                "lower_closed_upper_open_in_each_coordinate_except_the_"
                "corresponding_parent_core_global_upper_face_is_closed"
            ),
            "t_upper_is_parent_upper": t1 == source.t1,
            "p_upper_is_parent_upper": p1 == source.p1,
            "s_upper_is_global_upper": s1 == PARAMETER_UPPER,
            "positive_phase_rectangle_at_each_guarded_parameter": True,
            "positive_parameter_interval": True,
            "candidate_domain_is_complete_global_R1_partition": False,
        }
        field_payloads = {
            CANDIDATE_LOCAL_FIELDS[0]: {
                "template_id": templates["F1"]["template_id"],
                "parameter_guard": guard,
                "candidate_domain": candidate_domain,
            },
            CANDIDATE_LOCAL_FIELDS[1]: {
                "template_id": templates["F2"]["template_id"],
                "physical_homogeneity_subbranch_id": h_id,
                "table_rows_sha256": canonical_digest([h_payload]),
            },
            CANDIDATE_LOCAL_FIELDS[2]: {
                "parent_slot_id": binding["level_rows"][0]["parent_F3_slot_id"],
                "field_value": binding["level_rows"][0]["parent_F3_prefix_chart"],
                "restriction_inherits_chart": True,
            },
            CANDIDATE_LOCAL_FIELDS[3]: {
                "parent_slot_id": binding["level_rows"][0]["parent_F4_slot_id"],
                "field_value": binding["level_rows"][0]["parent_F4_suffix_chart"],
                "restriction_inherits_chart": True,
            },
            CANDIDATE_LOCAL_FIELDS[4]: {
                "template_id": templates["F5"]["template_id"],
                "physical_type": "adapted unstable one-dimensional Jacobian",
                "carrier_scope": "connected_components_of_canonical_W_intersect_atom",
                "adapted_inverse_strict_upper": "144000/180337",
                "Euclidean_inverse_strict_upper": "27410400/180337",
                "invariant_area_Jacobian_used": False,
            },
            CANDIDATE_LOCAL_FIELDS[5]: {
                "template_id": templates["F6"]["template_id"],
                "physical_type": (
                    "leafwise_log_distortion_of_adapted_unstable_one_dimensional_Jacobian"
                ),
                "carrier_scope": (
                    "connected_components_of_same_canonical_W_intersect_atom"
                ),
                "Holder_exponent": "1/3",
                "canonical_log_variation_strict_upper": "3/200000",
                "invariant_area_Jacobian_used": False,
            },
        }
        candidate_local_slots = {}
        for field in CANDIDATE_LOCAL_FIELDS:
            slot_payload = {
                "atom_id": row["atom_id"],
                "physical_homogeneity_subbranch_id": h_id,
                "roof_level_j": 0,
                "field_name": field,
                "field_payload": field_payloads[field],
            }
            slot_id = "slot:r1:" + canonical_digest(slot_payload)
            require(slot_id not in slot_ids, "duplicate R1 slot")
            slot_ids.add(slot_id)
            candidate_local_slots[field] = {
                "immutable_slot_id": slot_id,
                "payload": field_payloads[field],
            }

        f7 = binding["level_rows"][0]
        block_payload = {
            "atom_id": row["atom_id"],
            "source_core_id": row["source_core_id"],
            "destination_core_id": row["destination_core_id"],
            "source_binding_id": binding["source_binding_id"],
            "maximal_component_id": binding["maximal_component_id"],
            "parent_selected_homogeneous_component_row_id": binding[
                "parent_selected_homogeneous_component_row_id"
            ],
            "physical_homogeneity_subbranch_id": h_id,
            "roof": 1,
            "roof_level_j": 0,
            "parameter_guard": guard,
            "source_box_sha256": canonical_digest(row["source_box"]),
            "candidate_local_fields": list(CANDIDATE_LOCAL_FIELDS),
            "candidate_local_slots": candidate_local_slots,
            "F7_parent_provenance": {
                "parent_slot_id": f7["parent_F7_slot_id"],
                "parent_multiplier_upper": f7["parent_F7_multiplier_upper"],
                "adaptive_atom_has_artificial_dyadic_face": artificial_face,
                "destination_core_preimage_boundary_materialized": False,
                "destination_core_test_role": (
                    "strict_whole_rectangle_classification_only"
                ),
                "adaptive_restriction_boundary_Z_bound": "NOT_CERTIFIED",
                "R1_atom_F7_slot": "NOT_MATERIALIZED",
            },
        }
        block_payload["r1_candidate_field_packet_id"] = (
            "r1-candidate-field-packet:" + canonical_digest(block_payload)
        )
        blocks.append(block_payload)
        source_histogram[row["source_core_id"]] += 1
        destination_histogram[row["destination_core_id"]] += 1
        depth_histogram[row["depth"]] += 1

    blocks.sort(key=lambda value: value["atom_id"])
    require(len(blocks) == 4216, "block count")
    require(len(slot_ids) == 4216 * 6, "slot count")
    require(len(h_ids) == 4216, "h count")
    require(len(source_histogram) == 16, "source count")
    require(len(destination_histogram) == 16, "destination count")
    require(set(depth_histogram) == {13, 14, 15}, "depth support")
    return blocks, {
        "R1_inner_atom_count": len(blocks),
        "R1_inner_candidate_local_roof_histogram": {"1": len(blocks)},
        "R1_inner_source_core_count": len(source_histogram),
        "R1_inner_destination_core_count": len(destination_histogram),
        "R1_inner_source_histogram_sha256": canonical_digest(dict(sorted(source_histogram.items()))),
        "R1_inner_destination_histogram_sha256": canonical_digest(dict(sorted(destination_histogram.items()))),
        "R1_inner_depth_histogram": {
            str(key): value for key, value in sorted(depth_histogram.items())
        },
        "materialized_candidate_local_physical_homogeneity_table_count": len(h_ids),
        "materialized_candidate_local_F1_to_F6_slot_count": len(slot_ids),
        "materialized_candidate_local_slot_count_per_field": {
            field: len(blocks) for field in CANDIDATE_LOCAL_FIELDS
        },
        "materialized_R1_F7_slot_count": 0,
        "all_R1_atoms_have_artificial_adaptive_restriction_faces": True,
        "R1_candidate_field_packet_rows_sha256": canonical_digest(blocks),
    }


def field_maturity(schema_fields: list[str]) -> dict[str, Any]:
    rows = []
    for index, field in enumerate(schema_fields, start=1):
        if field in CANDIDATE_LOCAL_FIELDS:
            status = "CANDIDATE_LOCAL_ON_EACH_OF_4216_R1_INNER_ATOMS"
            slot_count = 4216
        elif field == FIELD7:
            status = "PARENT_SLOT_ONLY_ADAPTIVE_RESTRICTION_Z_NOT_CERTIFIED"
            slot_count = 0
        else:
            status = "NOT_CERTIFIED_ON_R1_INNER_CANDIDATES"
            slot_count = 0
        rows.append({
            "index": index,
            "field": field,
            "R1_inner_maturity": status,
            "candidate_local_R1_inner_atom_slot_count": slot_count,
            "global_complete_roof_level_slot_count_added": 0,
        })
    require(len(rows) == 18, "maturity row count")
    require(
        sum(row["candidate_local_R1_inner_atom_slot_count"] > 0 for row in rows)
        == 6,
        "6 candidate-local fields",
    )
    return {
        "required_field_count_per_complete_operator_roof_level": 18,
        "candidate_local_field_count_per_R1_inner_atom": 6,
        "candidate_local_fields_per_R1_inner_atom": list(CANDIDATE_LOCAL_FIELDS),
        "candidate_local_maturity": "6/18",
        "global_Gate5_maturity_before_round25_leaf": "4/18",
        "global_Gate5_maturity_after_round25_leaf": "4/18",
        "global_Gate5_field_credit_added": 0,
        "first_missing_field": FIELD7,
        "F7_parent_slot_is_R1_restricted_slot": False,
        "materialized_R1_inner_F7_candidate_local_slot_count": 0,
        "complete_18_field_R1_inner_operator_block_count": 0,
        "rows": rows,
        "rows_sha256": canonical_digest(rows),
    }


def build_result() -> dict[str, Any]:
    loaded = load_dependencies()
    adaptive = loaded[
        "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
    ]
    bindings, binding_registry = selected_source_bindings()
    templates = field_templates(loaded)
    blocks, block_registry = materialize_r1_blocks(
        adaptive, bindings, templates
    )
    schema_fields = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["required_operator_field_schema"]["required_fields"]
    used_sources = sorted({row["source_core_id"] for row in blocks})
    used_bindings = [bindings[key] for key in used_sources]
    require(all(row["roof"] == 1 for row in used_bindings), "all used roof one")

    result: dict[str, Any] = {
        "schema": "cm2.gate5.round25-r1-field-join.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "join_policy": "independent_fieldwise_fail_closed",
            "upstream_R1_scope": "strict_positive_full_dimensional_inner_atoms_only",
        },
        "R1_source_component_binding_registry": {
            **binding_registry,
            "used_roof_one_source_binding_count": len(used_bindings),
            "used_roof_one_source_binding_rows": used_bindings,
            "used_roof_one_source_binding_rows_sha256": canonical_digest(used_bindings),
        },
        "R1_field_template_registry": templates,
        "R1_inner_field_join_registry": block_registry,
        "R1_inner_candidate_field_packet_rows": blocks,
        "Gate5_R1_inner_18_field_maturity": field_maturity(schema_fields),
        "strict_nonpromotion": {
            "parent_F7_slot_survives_unpriced_adaptive_restriction": False,
            "invariant_area_Jacobian_one_is_F5_unstable_Jacobian": False,
            "F5_F6_candidate_local_installation_uses_area_Jacobian_seed": False,
            "F5_F6_candidate_local_installation_uses_universal_unstable_template_and_restriction_monotonicity": True,
            "R1_inner_candidate_atoms_form_complete_true_R1_partition_modulo_null": False,
            "upstream_unresolved_outer_cover_nonempty": True,
            "global_Gate5_maturity_before_and_after": "4/18 -> 4/18",
            "global_Gate5_field_credit_added": 0,
            "materialized_R1_inner_F7_candidate_local_slot_count": 0,
            "complete_18_field_R1_inner_operator_block_count": 0,
            "complete_full_R1_operator": "NOT_CERTIFIED",
            "return_wide_three_CM2_norm_intertwiners": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke_coefficient": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    result = build_result()
    print(json.dumps(result, indent=2, sort_keys=True))
    registry = result["R1_inner_field_join_registry"]
    print("R1_INNER_ATOMS_JOINED: 4216")
    print(
        "R1_F1_TO_F6_CANDIDATE_LOCAL_SLOTS: "
        f"{registry['materialized_candidate_local_F1_to_F6_slot_count']}"
    )
    print("R1_CANDIDATE_LOCAL_FIELD_MATURITY: 6/18")
    print("R1_F7_ADAPTIVE_BOUNDARY_Z: NOT_CERTIFIED")
    print("R1_COMPLETE_18_FIELD_BLOCKS: 0")
    print("GATE5_GLOBAL_MATURITY: 4/18 (UNCHANGED)")
    print("GATE5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
