#!/usr/bin/env python3
"""Round120 parameterized actual standard-curve children on the 72 endpoint cells.

The source-grazing root graphs are disjoint from the old compact Q2 parent-W
registry.  This producer therefore builds a fresh fixed-s=0 Borel foliation
on the Round113/117 relative interiors.  On the source G cylinder put

    phi = sigma * arccos(c),
    b   = phi - 4 r,
    r   = (9/25) theta_C(t).

Every point has one intercept b.  Along a fixed-b leaf the implicit root sheet
has strictly monotone squared third coordinate: c3^2 decreases on all eight
HIT parents and b3^2 increases on all sixty-four BYPASS parents.  Hence the
intersection with every half-open Round117 operator cell is empty or one
connected interval.

The source registry uses the corrected Round47 *adapted* arclength rule, never
the superseded Round31 Euclidean source-cell rule.  The output also freezes the
three image-recut schema and the universal F5/F6 constants, but it deliberately
does not call those schemas actual recut instances: interval endpoints,
natural indices and pulled-back common-refinement ranks are not materialized
here.  Consequently this round installs child-local F1--F4 only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as component
import cm2_round112_rank3_double_grazing_two_sided_root_sheet as round112
import cm2_round113_rank3_root_sheet_owner_ordering_spike as round113
from cm2_round76_r2_numeric_fields_generator import aq, interval
from cm2_round79_tangency_intersection_generator import digest, strict_sign


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2-round120-rank3-relative-interior-actual-standard-curve-recut-2026-07-23.json"
SCHEMA = "cm2.round120.rank3-relative-interior-actual-standard-curve-recut.v1"
PRECISION_BITS = 768

ROUND112 = HERE / "cm2-round112-rank3-double-grazing-two-sided-root-sheet-2026-07-23.json"
ROUND113 = HERE / "cm2-round113-rank3-endpoint-sheet-owner-ordering-2026-07-23.json"
ROUND117 = HERE / "cm2-round117-rank3-countable-homogeneity-operator-cells-2026-07-23.json"
ROUND118 = HERE / "cm2-round118-rank3-repaired-endpoint-source-cylinder-transfer-atlas-2026-07-23.json"
ROUND119 = HERE / "cm2-round119-rank3-eight-grazing-trace-extended-cylinder-reach-2026-07-23.json"
ROUND31 = HERE / "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json"
ROUND35 = HERE / "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
CONE = HERE / "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json"
UNIVERSAL = HERE / "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
ROUND47 = HERE / "cm2-gate34-round47-postcut-dyadic-recovery-manifest-2026-07-19.json"
ROUND50 = HERE / "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json"
GATE5 = HERE / "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"

PINS = {
    ROUND112.name: "94a54ddbf31518cfc2a93b105d66337111f2b950be894f126e7b9c042e6b02e5",
    ROUND113.name: "d38d0fb159ea31ce430c1e2a27b88cc630d786921d3d4642f2bd3fe7c298e181",
    ROUND117.name: "31b6535e21886d825d5a4658f2c9d3ccc8c5525c2b9d2fb181f88baa7dcf9eb0",
    ROUND118.name: "91bd73445fd13eeb759e932b0626ba64acef1f10a061d6d416577dfd96feb34f",
    ROUND119.name: "9ff985c91472e0ef57ced9fc10dbb6b2aa9e9627a5ac94c999caeefeca29a749",
    ROUND31.name: "fa654b2c852f2b89e6e85a457f7ec7689dc56b7ccc9582d994db6b2e269bfb74",
    ROUND35.name: "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c",
    CONE.name: "173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9",
    UNIVERSAL.name: "d532eeab0fa24901228a589724ffc4dbcff721f7d174a2b519187d77faab883b",
    ROUND47.name: "79eeff7d5c18ec7d28a30c61ae857a733b3136202917c54f6aeaf93d7f414089",
    ROUND50.name: "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73",
    GATE5.name: "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "cm2_round113_rank3_root_sheet_owner_ordering_spike.py": "2263d213bad42163da326c892662f500f29a3c5f6cf4b8ba28cc2bb57990b11e",
    "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py": "ccdfeebfa14fdaa466a67b79269145b2a36076b7027f2bac0a9c5daa030b5e3f",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_gate25_roof_two_wall_chart_frontier_cert.py": "153e64610404eb4035d3bc019f1eb19e5dc72c577c2de0b7309344ec33ce15f1",
    "cm2_gate25_selected_component_chart_field_slots_cert.py": "666e7f1ea4198528b143b522d2c5daf55ba4fecfd127d86663b23e0bb38a477f",
    "cm2_gate34_round28_nonempty_adaptive_component_registry_cert.py": "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
    "cm2_round76_r2_numeric_fields_generator.py": "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf",
    "cm2_round79_tangency_intersection_generator.py": "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
    "cm2_gate34_round47_postcut_dyadic_recovery_cert.py": "378f50e56c76e80c5d571eb52c99d708710a8b8b0238c8b8024643e6dfdeeca9",
    "cm2_gate34_round50_physical_whole_family_grouping_cert.py": "f0e95a2756383ee23aa2d6a5df3b5d453b497df8500df7fdddf96096e900a809",
    "cm2_gate25_universal_operator_endpoint_template_frontier_cert.py": "254a4cc0b26fc12565e8816d9a09a946079114d774f87254f99e448f87a91944",
    "cm2_gate5_return_word_three_norm_frontier_cert.py": "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
}

# The replay executes older geometry functions rather than merely reading their
# certificates.  Close the runtime dependency graph: first inherit every byte
# pin asserted by the already pinned Round113 engine, then add the two helper
# modules reached transitively through Round76/Round79.
for _name, _expected in {
    **round113.PINS,
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
    "cm2_round78_tangency_curve_generator.py": "cc9da9d607bbe19c54ffccfd4974b37eb96459f0c4ed9e70d7a68e732f625d85",
}.items():
    if _name in PINS and PINS[_name] != _expected:
        raise RuntimeError(f"inconsistent inherited runtime pin: {_name}")
    PINS[_name] = _expected

CLOSED_SCHEMAS = {
    ROUND112.name: "cm2.round112.rank3-double-grazing-two-sided-root-sheet.v1",
    ROUND113.name: "cm2.round113.rank3-endpoint-sheet-owner-ordering.v1",
    ROUND117.name: "cm2.round117.rank3-countable-homogeneity-operator-cells.v1",
    ROUND118.name: "cm2.round118.rank3-repaired-endpoint-source-cylinder-transfer-atlas.v1",
    ROUND119.name: "cm2.round119.rank3-eight-grazing-trace-extended-cylinder-reach.v1",
}

SOURCE_RADIUS = Q(9, 25)
SOURCE_CURVATURE = Q(25, 9)
CANONICAL_SLOPE = Q(4)
SOURCE_ADAPTED_DENSITY = SOURCE_CURVATURE + CANONICAL_SLOPE
CANONICAL_ADAPTED_LENGTH = "1e-90"
THETA = Q(144000, 180337)
ONE_STEP_LOG_VARIATION = Q(3, 200000)
THREE_STEP_THETA = THETA**3
THREE_STEP_LOG_VARIATION = 3 * ONE_STEP_LOG_VARIATION
OUTER = Q(1, 16384)
CHART_ORIENTATION = {"E": 1, "N": -1, "W": -1, "S": 1}
CANONICAL_ANGULAR_LIFT = {
    "E": "asin(t)",
    "N": "pi/2-asin(t)",
    "W": "pi-asin(t)",
    "S": "-pi/2+asin(t)",
}
GATE5_FIELDS = (
    "nonempty_or_empty_domain_proof",
    "physical_homogeneity_subbranch_table",
    "homogeneous_prefix_chart",
    "homogeneous_suffix_chart",
    "inverse_Jacobian_bound",
    "log_Jacobian_distortion_sum",
)
INSTALLED_GATE5_FIELDS = GATE5_FIELDS[:4]
CARRIER_CHILD_ID_SCHEMA = (
    "(round120-child-v1,typed-parent-W-id,round117-operator-cell-id(active-labels),"
    "source-interval-rank,source-adapted-index-k,connected-rank-0)"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def closed_digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
        parse_float=lambda token: (_ for _ in ()).throw(ValueError(f"float forbidden: {token}")),
    )
    require(type(value) is dict, f"top-level object: {path.name}")
    return value


def exact_dyadic(point: arb) -> Q:
    mantissa, exponent = point.man_exp()
    return Q(int(mantissa)) * (Q(2) ** int(exponent))


def arb_pair(value: arb) -> tuple[Q, Q]:
    return exact_dyadic(value.lower()), exact_dyadic(value.upper())


def abs_lower(value: arb, label: str) -> Q:
    lower, upper = arb_pair(value)
    if lower > 0:
        return lower
    if upper < 0:
        return -upper
    raise RuntimeError(f"zero in interval: {label}")


def abs_upper(value: arb) -> Q:
    lower, upper = arb_pair(value)
    return max(abs(lower), abs(upper))


def qstr(value: Q) -> str:
    return str(Q(value))


def load_closed(path: Path) -> dict[str, Any]:
    document = strict_json(path)
    require(set(document) == {"schema", "result", "result_sha256"}, f"closed keys: {path.name}")
    require(document["schema"] == CLOSED_SCHEMAS[path.name], f"schema: {path.name}")
    require(document["result_sha256"] == closed_digest(document["result"]), f"digest: {path.name}")
    return document["result"]


def load_inputs() -> dict[str, Any]:
    for name, expected in PINS.items():
        require(sha256(HERE / name) == expected, f"pin mismatch: {name}")
    values = {
        "r112": load_closed(ROUND112),
        "r113": load_closed(ROUND113),
        "r117": load_closed(ROUND117),
        "r118": load_closed(ROUND118),
        "r119": load_closed(ROUND119),
        "r31": strict_json(ROUND31),
        "r35": strict_json(ROUND35),
        "cone": strict_json(CONE),
        "universal": strict_json(UNIVERSAL),
        "r47": strict_json(ROUND47),
        "r50": strict_json(ROUND50),
        "gate5": strict_json(GATE5),
    }
    require(values["r113"]["certified_parameter_cell_count"] == 72, "Round113 parents")
    require(values["r113"]["residual_parameter_cell_count"] == 0, "Round113 residual")
    require(values["r117"]["round113_parent_proof_box_count"] == 72, "Round117 parents")
    require(values["r117"]["finite_generator_family_template_instance_count"] == 112, "Round117 templates")
    require(values["r117"]["actual_parent_W_standard_curve_join_installed"] is False, "Round117 join frontier")
    require(values["r118"]["repaired_endpoint_identity_count"] == 8, "Round118 repaired IDs")
    require(values["r119"]["certified_per_trace_ambient_extended_cosine_master_reach_count"] == 8, "Round119 trace input")
    return values


def inherited_contracts(values: dict[str, Any]) -> dict[str, Any]:
    old = values["r31"]["result"]["Q2_parent_W_Borel_registry"]
    require(old["actual_parent_W_registry"] == "CERTIFIED_PARAMETERIZED", "Round31 registry")
    borel = values["r35"]["result"]["arbitrary_Rn_parent_W_Borel_registry"]
    require(borel["registry_type"] == "standard-Borel parameterized actual curve registry", "Round35 Borel registry")
    require(borel["source_interval_rank"].startswith("least rational-dyadic interval basis index"), "Round35 locator")
    cone = values["cone"]["result"]["global_invariant_geometric_cone"]
    require(Q(cone["curvature_lower"]) == Q(25, 9), "cone lower")
    require(Q(cone["cone_upper"]) > CANONICAL_SLOPE, "slope cone")
    require(cone["strict_forward_invariance"] is True, "cone invariance")
    universal = values["universal"]["result"]["universal_full_collision_branch_templates"]
    require(universal["canonical_adapted_length_upper"] == CANONICAL_ADAPTED_LENGTH, "universal length")
    require(Q(universal["field_5_inverse_Jacobian_seed"]["universal_adapted_inverse_strict_upper"]) == THETA, "F5")
    require(Q(universal["field_6_log_Jacobian_distortion_seed"]["canonical_curve_log_variation_strict_upper"]) == ONE_STEP_LOG_VARIATION, "F6")
    correction = values["r47"]["result"]["corrected_adapted_source_cell_registry"]
    require(correction["status"] == "CERTIFIED_CORRECTED_ADAPTED_SOURCE_CELL_SCHEMA", "Round47 correction")
    require(correction["Round31_Euclidean_cell_bound_not_reused_as_adapted"] is True, "metric correction")
    ownership = values["r50"]["result"]["physical_Borel_whole_family_grouping"]
    require(ownership["physical_full_registry_reconstructed"] is True, "Round50 Borel grouping")
    require(ownership["half_open_endpoint_owner"].startswith("use oriented half-open natural cells"), "Round50 half-open owner")
    fields = values["gate5"]["result"]["required_operator_field_schema"]["required_fields"]
    require(len(fields) == 18, "Gate5 field count")
    require(tuple(fields[:6]) == GATE5_FIELDS, "Gate5 F1-F6 order")
    return {"old": old, "borel": borel, "cone": cone, "universal": universal, "correction": correction, "ownership": ownership, "fields": fields}


def repaired_index(r118: dict[str, Any]) -> dict[tuple[str, tuple[Any, ...]], dict[str, Any]]:
    result: dict[tuple[str, tuple[Any, ...]], dict[str, Any]] = {}
    for row in r118["repaired_endpoint_rows"]:
        branch = tuple(row["branch_key"])
        for kind in ("HIT", "BYPASS"):
            key = (kind, branch)
            require(key not in result, "duplicate repaired key")
            result[key] = row
    require(len(result) == 16, "repaired sheet crosswalk")
    return result


def cell_indexes(values: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    sheets112 = {row["sheet_id"]: row for row in values["r112"]["sheet_rows"]}
    sheets113: dict[str, dict[str, Any]] = {}
    parents113: dict[str, dict[str, Any]] = {}
    for sheet in values["r113"]["sheet_rows"]:
        sheets113[sheet["sheet_id"]] = sheet
        for parent in sheet["certified_cells"]:
            require(parent["cell_id"] not in parents113, "duplicate Round113 parent")
            parents113[parent["cell_id"]] = {"sheet": sheet, "parent": parent}
    rows117 = {row["parent_round113_cell_id"]: row for row in values["r117"]["common_refinement_rows"]}
    require(len(sheets112) == 16 and len(parents113) == 72 and len(rows117) == 72, "index counts")
    return sheets112, parents113, rows117


def minimum_chart_margin(fresh: dict[str, Any]) -> Q:
    margins: list[Q] = []
    for leg in fresh["leg_audits"]:
        lower = arb_pair(arb(leg["selected_collision_chart_dominance_margin"][0]))[0]
        require(lower > 0, "chart margin")
        margins.append(lower)
    return min(margins)


def transparent_wall_chart(token: str) -> str:
    require(token in {"X+", "X-", "Y+", "Y-"}, "transparent wall token")
    wall_index = 1 if token[1] == "+" else 0
    if token[0] == "X":
        return f"transparent-wall:x={wall_index}:(z=y, eta=u_y)"
    return f"transparent-wall:y={wall_index}:(z=x, eta=u_x)"


def roof_level_chart_pairs(
    source_chart: str, target_chart: str, clean_walls: list[str], roof: int,
) -> list[dict[str, Any]]:
    require(roof == len(clean_walls) + 1, "roof/wall count")
    source = f"collision:{source_chart}"
    target = f"collision:{target_chart}"
    if not clean_walls:
        return [{
            "roof_level_j": 0,
            "prefix_chart": source,
            "suffix_chart": target,
            "transparent_wall_token": None,
        }]
    require(len(clean_walls) == 1 and roof == 2, "rank3 roof-two contract")
    wall = transparent_wall_chart(clean_walls[0])
    return [
        {
            "roof_level_j": 0,
            "prefix_chart": source,
            "suffix_chart": wall,
            "transparent_wall_token": clean_walls[0],
        },
        {
            "roof_level_j": 1,
            "prefix_chart": wall,
            "suffix_chart": target,
            "transparent_wall_token": clean_walls[0],
        },
    ]


def recut_rows(fresh: dict[str, Any], parent_id: str) -> list[dict[str, Any]]:
    owners = fresh["ordered_regular_relative_interior_owner_ids"]
    words = fresh["official_word_key_ids"]
    rows = []
    for stage in range(3):
        word = fresh["leg_audits"][stage]["official_word_key"]
        require(word["row"][1][0] == owners[stage][0], "official target species")
        target_chart = f"{word['row'][1]}:{fresh['leg_audits'][stage]['selected_collision_chart']}"
        clean_walls = word["row"][2]
        roof = word["row"][3]
        payload = {
            "parent_round113_cell_id": parent_id,
            "stage": stage,
            "official_word_key_id": words[stage],
            "source_chart": word["row"][0],
            "target_chart": target_chart,
            "target_owner_id": owners[stage],
            "clean_wall_records": clean_walls,
            "roof_level_count": roof,
            "roof_level_domain": f"0<=roof_level_j<{roof}",
            "roof_level_chart_pairs": roof_level_chart_pairs(
                word["row"][0], target_chart, clean_walls, roof,
            ),
            "adapted_coordinate": "u_i(x)=integral_(x_left)^x (kappa_i+V_i) dr",
            "natural_rule": "half-open [j*1e-90,(j+1)*1e-90), clipped at the last endpoint which is closed",
            "candidate_actual_instance_key": "(round120-child-id,stage,natural-adapted-index-j)",
            "actual_instance_materialized": False,
            "candidate_one_step_F5_template_not_installed": qstr(THETA),
            "candidate_one_step_F6_template_not_installed": qstr(ONE_STEP_LOG_VARIATION),
        }
        rows.append({**payload, "recut_rule_id": f"round120-recut-rule:step{stage}:" + closed_digest(payload)})
    return rows


def slot_schema_rows(
    generators: list[dict[str, Any]], recuts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for generator in generators:
        family = generator["family"]
        source_domain = generator["source_label_domain"]
        third_domain = generator.get(
            "third_label_domain", generator.get("actual_third_collision_class"),
        )
        sample_operator_cell_id = generator["stable_id_interface_sample"]["operator_cell_id"]
        subbranch_schema = (
            "round117-operator-cell-id(active-labels); this inherited immutable ID is the "
            f"Round120 homogeneous-subbranch ID for family {family}"
        )
        carrier_child_schema = CARRIER_CHILD_ID_SCHEMA
        homogeneity_value = (
            f"source={source_domain}; collision1=H0_CENTRAL; collision2=H0_CENTRAL; "
            f"actual-collision3={third_domain}"
        )
        for recut in recuts:
            stage = recut["stage"]
            for roof_level in range(recut["roof_level_count"]):
                chart_pair = recut["roof_level_chart_pairs"][roof_level]
                require(chart_pair["roof_level_j"] == roof_level, "roof chart ordering")
                for field_index, field_name in enumerate(INSTALLED_GATE5_FIELDS, start=1):
                    values = {
                        1: "strict empty or positive-length interval query; singleton is boundary-only",
                        2: homogeneity_value,
                        3: chart_pair["prefix_chart"],
                        4: chart_pair["suffix_chart"],
                    }
                    sample_slot_payload = [
                        recut["official_word_key_id"], sample_operator_cell_id,
                        roof_level, field_name,
                    ]
                    rows.append({
                        "generator_family": family,
                        "label_parameter_domains": {
                            "source": source_domain,
                            "actual_third": third_domain,
                        },
                        "official_word_key_id": recut["official_word_key_id"],
                        "homogeneous_subbranch_id_schema": subbranch_schema,
                        "carrier_child_id_schema": carrier_child_schema,
                        "roof_level_j": roof_level,
                        "field_index": field_index,
                        "field_name": field_name,
                        "field_value_or_contract": values[field_index],
                        "immutable_slot_key_schema": (
                            "(official-word-key-id,homogeneous-subbranch-id,roof-level-j,field-name)"
                        ),
                        "parameterized_slot_id_constructor": (
                            "round120-slot:sha256(canonical([official-word-key-id,"
                            "round117-operator-cell-id(active-labels),roof-level-j,field-name]))"
                        ),
                        "stable_ID_interface_sample": {
                            "homogeneous_subbranch_id": sample_operator_cell_id,
                            "slot_id": "round120-slot:" + closed_digest(sample_slot_payload),
                            "sample_is_an_ID_API_test_not_a_nonempty_claim": True,
                        },
                        "slot_status": "CERTIFIED_PARAMETERIZED_ON_EVERY_NONEMPTY_ACTUAL_CHILD",
                        "recut_schema_row_id": recut["recut_rule_id"],
                    })
    return rows


def certify_parent(
    joined: dict[str, Any],
    input_sheet: dict[str, Any],
    row117: dict[str, Any],
    repaired: dict[str, Any],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
    cores: tuple[Any, ...],
) -> dict[str, Any]:
    sheet = joined["sheet"]
    parent = joined["parent"]
    kind = sheet["sheet_kind"]
    coordinate = "c3" if kind == "HIT" else "b3"
    branch = tuple(input_sheet["branch_key"])
    require(tuple(sheet["branch_key"]) == branch == tuple(row117["branch_key"]), "branch join")
    require(row117["sheet_kind"] == kind, "kind join")
    source = replace(cores[branch[0]], chart_id=input_sheet["source_chart"])
    c0, c1 = map(Q, parent["parameter_box"]["c0"])
    z0, z1 = map(Q, parent["parameter_box"][coordinate])

    fresh = round113.audit_cell(
        input_sheet, source, branch, c0, c1, z0, z1, pair_index, pattern_index,
    )
    require(fresh["official_path_id"] == parent["official_path_id"] == row117["official_path_id_inherited"], "official path replay")
    require(fresh["official_word_key_ids"] == parent["official_word_key_ids"] == row117["official_word_key_ids_inherited"], "word replay")
    require(fresh["ordered_regular_relative_interior_owner_ids"] == parent["ordered_regular_relative_interior_owner_ids"], "owner replay")

    t0, t1 = map(Q, fresh["implicit_t_root_enclosure"])
    geometry = round113.path_geometry(
        source, branch, input_sheet["source_grazing_sign_sigma0"], kind,
        t0, t1, c0, c1, z0, z1,
    )
    equation = geometry["equation"]
    t = interval(t0, t1)
    c = interval(c0, c1)
    radial_t = (arb(1) - t * t).sqrt()
    radial_c = (arb(1) - c * c).sqrt()
    sigma = input_sheet["source_grazing_sign_sigma0"]
    chart = input_sheet["source_chart"].split(":")[1]
    epsilon = CHART_ORIENTATION[chart]
    angular_lift_id = f"round120-angular-lift:G:{chart}:k0"
    B_c = -arb(sigma) / radial_c
    B_t = -arb(4) * aq(SOURCE_RADIUS) * arb(epsilon) / radial_t
    t_c = -B_c / B_t
    delta_c_on_leaf = equation.gradient[1] + equation.gradient[0] * t_c
    third_radius = aq(round112.radius(branch[2]))
    squared_third_c = delta_c_on_leaf / (third_radius * third_radius)
    if kind == "BYPASS":
        squared_third_c = -squared_third_c
    monotonicity_sign = strict_sign(squared_third_c)
    require(monotonicity_sign == (-1 if kind == "HIT" else 1), "squared-coordinate monotonicity")

    first_cosine = (arb(1) - geometry["selected"][0]["momentum"].value ** 2).sqrt()
    second_cosine = (arb(1) - geometry["selected"][1]["momentum"].value ** 2).sqrt()
    first_lower = arb_pair(first_cosine)[0]
    second_lower = arb_pair(second_cosine)[0]
    require(first_lower > Q(4, 5) and second_lower > Q(9, 10), "middle H0")
    chart_lower = minimum_chart_margin(fresh)
    require(chart_lower > Q(1, 1000), "chart dominance")

    if kind == "HIT":
        require(abs_lower(squared_third_c, "HIT derivative") > Q(424), "HIT derivative lower")
    else:
        require(abs_lower(squared_third_c, "BYPASS derivative") > Q(480), "BYPASS derivative lower")

    generators = row117["generator_families"]
    generator_contract = [{
        "family": row["family"],
        "source_label_domain": row["source_label_domain"],
        "third_label_domain": row.get("third_label_domain", row.get("actual_third_collision_class")),
        "active_intersection_predicate": row.get("active_intersection_predicate", row.get("source_active_intersection_predicate")),
        "cardinality": row["cardinality"],
        "stable_id_interface_sample": row["stable_id_interface_sample"],
    } for row in generators]
    recuts = recut_rows(fresh, parent["cell_id"])
    slots = slot_schema_rows(generators, recuts)
    child_key = CARRIER_CHILD_ID_SCHEMA
    field_slots = {
        "F1": "CERTIFIED_PARAMETERIZED_EMPTY_OR_CONNECTED_RANK_0",
        "F2": "CERTIFIED_PARAMETERIZED_PHYSICAL_HOMOGENEITY_SUBBRANCH",
        "F3": "CERTIFIED_PARAMETERIZED_PREFIX_CHART",
        "F4": "CERTIFIED_PARAMETERIZED_SUFFIX_CHART",
        "F5": "NOT_INSTALLED_MISSING_ACTUAL_IMAGE_RECUT_INSTANCES",
        "F6": "NOT_INSTALLED_MISSING_ACTUAL_IMAGE_RECUT_INSTANCES",
    }
    return {
        "parent_round113_cell_id": parent["cell_id"],
        "parent_round113_sheet_id": sheet["sheet_id"],
        "round117_generator_family_digest": closed_digest(generators),
        "round117_generator_contract_rows": generator_contract,
        "sheet_kind": kind,
        "branch_key": list(branch),
        "repaired_endpoint_id": repaired["repaired_endpoint_id"],
        "exterior_port_id": repaired["exterior_port_id"],
        "source_chart": input_sheet["source_chart"],
        "source_grazing_sign_sigma0": sigma,
        "parameter_box": parent["parameter_box"],
        "official_path_id": fresh["official_path_id"],
        "official_word_key_ids": fresh["official_word_key_ids"],
        "ordered_owner_ids": fresh["ordered_regular_relative_interior_owner_ids"],
        "actual_third_collision_contract": {
            "owner_id": row117["actual_third_collision_owner_id"],
            "homogeneity_label_or_parameter": (
                "R117 active third-label parameter" if kind == "HIT"
                else row117["actual_third_collision_homogeneity_label"]
            ),
            "BYPASS_actual_winner_H0_whole_parent": (
                row117.get("actual_third_collision_H0_strict_whole_parent_cell", False)
                if kind == "BYPASS" else None
            ),
            "BYPASS_actual_winner_cosine_minus_b128_enclosure": (
                row117.get("actual_third_collision_cosine_minus_b128_enclosure")
                if kind == "BYPASS" else None
            ),
            "BYPASS_b3_is_collision_angle": row117.get("bypass_b3_is_collision_angle"),
            "BYPASS_b3_homogeneity_index": row117.get("bypass_b3_homogeneity_index"),
        },
        "canonical_parent_W_leaf": {
            "fixed_system_parameter_s": "0",
            "equation": "phi(r)=4*r+b; p(r)=sin(phi(r)); cos(phi)>0",
            "intercept_on_this_sheet": "b=sigma0*arccos(c0)-4*(9/25)*theta_source_chart(t)",
            "angular_lift_id": angular_lift_id,
            "canonical_theta_source_chart_of_t": CANONICAL_ANGULAR_LIFT[chart],
            "angular_lift_additive_2pi_index": 0,
            "source_chart_theta_derivative_sign": epsilon,
            "B_t_sign": strict_sign(B_t),
            "B_c_sign": strict_sign(B_c),
            "dt_dc_at_fixed_b_sign": strict_sign(t_c),
            "abs_B_t_strict_lower": qstr(abs_lower(B_t, "B_t")),
            "abs_B_c_strict_lower": qstr(abs_lower(B_c, "B_c")),
            "abs_dt_dc_strict_lower": qstr(abs_lower(t_c, "t_c")),
            "abs_dt_dc_strict_upper": qstr(abs_upper(t_c)),
        },
        "squared_third_coordinate": f"{coordinate}^2",
        "squared_third_coordinate_derivative_sign": monotonicity_sign,
        "squared_third_coordinate_derivative_abs_strict_lower": qstr(abs_lower(squared_third_c, "w_c")),
        "squared_third_coordinate_derivative_abs_strict_upper": qstr(abs_upper(squared_third_c)),
        "empty_or_one_connected_interval_for_every_fixed_b_and_active_generator": True,
        "connected_rank": 0,
        "natural_boundaries_excluded": ["c0=0", f"{coordinate}=0"],
        "boundary_owner_conjunction": {
            "priority_1_natural": {
                "source_c0_zero_owned_by_singular_ledger": True,
                "third_coordinate": coordinate,
                "third_coordinate_zero_owned_by_singular_ledger": True,
                "regular_child_owns_either_natural_boundary": False,
                "logical_relation": "each natural boundary is excluded individually; simultaneous zero is not required",
            },
            "priority_2_round113_dyadic": row117["parent_artificial_boundary_ownership"],
            "priority_3_round117_homogeneity": (
                "H_n=(sin((n+1)^-2),sin(n^-2)] owns its upper boundary; "
                "H0_CENTRAL_OUTER=(sin(128^-2),1/16384] is open at its lower boundary"
            ),
            "priority_4_source_adapted": (
                "oriented [k*1e-90,(k+1)*1e-90), clipped at the last endpoint which is closed"
            ),
            "coincident_artificial_boundaries_use_the_conjunction_of_all_unique_owner_rules": True,
            "natural_boundary_always_overrides_artificial_ownership": True,
        },
        "first_collision_cosine_strict_lower": qstr(first_lower),
        "second_collision_cosine_strict_lower": qstr(second_lower),
        "first_and_second_collision_homogeneity": "H0_CENTRAL",
        "minimum_selected_collision_chart_dominance_strict_lower": qstr(chart_lower),
        "parameterized_actual_child_id_schema": child_key,
        "typed_Borel_locator_contract": {
            "intercept_parameter": "exact mathematical real b represented by a canonical nested rational-dyadic locator",
            "source_interval_rank": "least rational-dyadic interval basis index whose closure lies inside the positive-length component",
            "component_rank": 0,
            "angular_lift_id": angular_lift_id,
            "same_canonical_angular_lift_used_in_intercept_b": True,
            "locator_validity": "nonempty closed dyadic intervals, nested, diameters tending to zero",
            "dyadic_endpoint_representation": "canonical terminating expansion with trailing zeros",
            "analytic_boundary_equality": "symbolic half-open owner predicate; no finite-precision equality inference",
            "total_computable_real_comparison_oracle_claimed": False,
            "Arb_or_decimal_text_in_stable_ID": False,
            "typed_parent_W_tuple": (
                "(round120-grazing-parent-W-v1,repaired-endpoint-id,angular-lift-id,exact-b)"
            ),
        },
        "parameterized_component_rank": 0,
        "positive_length_proof_required_before_child_emission": True,
        "three_step_adapted_recut_frontier_schema_rows": recuts,
        "three_step_adapted_recut_frontier_schema_rows_sha256": closed_digest(recuts),
        "actual_image_recut_instance_rows": [],
        "actual_image_recut_instance_count": 0,
        "gate5_F1_F4_slot_schema_rows": slots,
        "gate5_F1_F4_slot_schema_rows_sha256": closed_digest(slots),
        "gate5_F1_F4_slot_schema_template_count": len(slots),
        "gate5_actual_child_field_status": field_slots,
        "candidate_three_step_F5_template_not_installed": qstr(THREE_STEP_THETA),
        "candidate_three_step_F6_template_not_installed": qstr(THREE_STEP_LOG_VARIATION),
    }


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    require(precision_bits >= 512, "precision")
    ctx.prec = precision_bits
    values = load_inputs()
    contracts = inherited_contracts(values)
    sheets112, parents113, rows117 = cell_indexes(values)
    repaired = repaired_index(values["r118"])
    pair_index, pattern_index, registry_digest = component.key_index_tables()
    cores = core_cert.physical_cores()

    rows: list[dict[str, Any]] = []
    for parent_id in sorted(parents113):
        joined = parents113[parent_id]
        sheet = joined["sheet"]
        input_sheet = sheets112[sheet["sheet_id"]]
        branch = tuple(input_sheet["branch_key"])
        row = certify_parent(
            joined, input_sheet, rows117[parent_id], repaired[(sheet["sheet_kind"], branch)],
            pair_index, pattern_index, cores,
        )
        rows.append(row)

    hit = [row for row in rows if row["sheet_kind"] == "HIT"]
    bypass = [row for row in rows if row["sheet_kind"] == "BYPASS"]
    require(len(hit) == 8 and len(bypass) == 64, "row kinds")
    require(all(Q(row["squared_third_coordinate_derivative_abs_strict_lower"]) > 424 for row in hit), "global HIT")
    require(all(Q(row["squared_third_coordinate_derivative_abs_strict_lower"]) > 480 for row in bypass), "global BYPASS")

    nonempty_rows117 = sorted(
        (
            row for row in values["r117"]["common_refinement_rows"]
            if row["central_outer_source_child_nonempty"] is True
        ),
        key=lambda row: row["parent_round113_cell_id"],
    )
    require(len(nonempty_rows117) == 24, "Round117 nonempty central-outer parents")
    require(
        values["r117"]["parent_rows_with_nonempty_source_central_outer_child"] == 24,
        "Round117 nonempty census",
    )
    seed117 = nonempty_rows117[0]
    seed_generator = next(
        row for row in seed117["generator_families"]
        if "CENTRAL_OUTER" in row["family"]
    )

    old_p_upper = Q(1, 50)
    grazing_p_lower_squared = 1 - OUTER**2
    require(grazing_p_lower_squared > old_p_upper**2, "Round31 domain disjointness")
    source_registry = {
        "registry_type": "fixed-s=0 grazing-cylinder Borel parameterized actual parent-W registry",
        "base_region_key": "round117 operator-cell/root-graph region ID",
        "canonical_leaf_equation": "phi(r)=4*r+b; p(r)=sin(4*r+b)",
        "canonical_slope_dphi_dr": "4",
        "source_component": "G",
        "source_radius": qstr(SOURCE_RADIUS),
        "source_curvature": qstr(SOURCE_CURVATURE),
        "unique_leaf_parameter": "b=sigma0*arccos(c0)-4*r",
        "source_adapted_coordinate": "u_*(r)=integral_(r_left)^r (kappa_G+4)dt=(61/9)*(r-r_left)",
        "source_adapted_density": qstr(SOURCE_ADAPTED_DENSITY),
        "corrected_natural_source_cell_rule": "half-open u_* intervals [k*1e-90,(k+1)*1e-90), clipped at the last endpoint which is closed",
        "adapted_cell_length_upper": CANONICAL_ADAPTED_LENGTH,
        "Round31_Euclidean_source_cell_rule_reused": False,
        "finite_actual_curve_count_claimed": False,
        "parameterized_actual_parent_W_registry_installed": True,
    }
    result = {
        "precision_bits": precision_bits,
        "round113_parent_proof_box_count": len(rows),
        "round117_generator_family_template_count": sum(len(row["round117_generator_contract_rows"]) for row in rows),
        "official_candidate_registry_rows_sha256": registry_digest,
        "actual_parent_W_registry_contract": source_registry,
        "typed_Borel_locator_precedent": {
            "Round35_physical_domain_reused": False,
            "locator_pattern_only": contracts["borel"]["source_interval_rank"],
            "formal_b_is_an_exact_typed_parameter_not_a_decimal_hash": True,
        },
        "Round31_compact_Q2_parent_W_domain_reused": False,
        "Round31_compact_Q2_source_abs_momentum_upper": qstr(old_p_upper),
        "Round120_grazing_source_momentum_square_certified_lower": qstr(grazing_p_lower_squared),
        "Round31_and_Round120_physical_source_domains_strictly_disjoint": True,
        "parameterized_actual_child_registry_installed": True,
        "finite_actual_child_count_claimed": False,
        "actual_child_registry_cardinality": "BOREL_PARAMETERIZED_NOT_A_FINITE_INTEGER_ENUMERATION",
        "nonvacuous_actual_child_fibre_existence": {
            "round117_nonempty_central_outer_parent_count": len(nonempty_rows117),
            "positive_length_fixed_b_fibre_family_exists": True,
            "proof": (
                "each certified nonempty relative-interior operator region is open in its two root-graph "
                "coordinates; B_t is nonzero, so the canonical b-level foliation is regular, and every "
                "strict interior point lies on a locally positive-length fixed-b fibre"
            ),
            "stable_interface_seed_parent_round113_cell_id": seed117["parent_round113_cell_id"],
            "stable_interface_seed_operator_cell_id": seed_generator["stable_id_interface_sample"]["operator_cell_id"],
            "seed_is_an_existence_interface_not_a_materialized_exact_b_ID": True,
            "materialized_exact_b_witness_ID_count": 0,
        },
        "nonempty_or_empty_intersection_theorem": {
            "fixed_leaf_equations": "B(t,c0)=b and F_sheet(t,c0,z)=0",
            "B_t_nonzero_on_all_72_parents": True,
            "HIT_squared_coordinate_derivative": "d(c3^2)/dc0=(Delta_t*dt/dc0+Delta_c)/R3^2",
            "BYPASS_squared_coordinate_derivative": "d(b3^2)/dc0=-(Delta_t*dt/dc0+Delta_c)/R3^2",
            "HIT_parent_count_with_strict_negative_derivative": len(hit),
            "BYPASS_parent_count_with_strict_positive_derivative": len(bypass),
            "HIT_global_derivative_abs_strict_lower": qstr(min(Q(row["squared_third_coordinate_derivative_abs_strict_lower"]) for row in hit)),
            "BYPASS_global_derivative_abs_strict_lower": qstr(min(Q(row["squared_third_coordinate_derivative_abs_strict_lower"]) for row in bypass)),
            "every_fixed_b_active_operator_cell_intersection_is_empty_or_one_connected_interval": True,
            "connected_rank": 0,
            "Borel_fibre_construction": (
                "form the set-theoretic intersection of the exact R113 dyadic c0 interval, exact R117 half-open "
                "homogeneity intervals, and one corrected source-adapted cell; strict squared-third monotonicity "
                "makes every fibre empty or one interval; symbolic endpoint predicates assign half-open ownership"
            ),
            "total_numeric_decision_procedure_for_arbitrary_exact_real_b_claimed": False,
            "positive_length_proof_is_required_before_any_child_ID_is_emitted": True,
            "formal_intercept_parameter_is_never_hashed_from_an_Arb_decimal": True,
        },
        "child_generator_rows": rows,
        "child_generator_rows_sha256": closed_digest(rows),
        "canonical_three_step_recut_frontier": {
            "stage_count": 3,
            "source_rule": source_registry["corrected_natural_source_cell_rule"],
            "image_rule": "on each forward image use its own adapted coordinate u_i and deterministic half-open natural index j",
            "candidate_future_rule": (
                "pull each actual image cut back to the source, sort the finite common refinement, "
                "and use its natural zero-based rank"
            ),
            "candidate_actual_instance_key": "(round120-child-id,stage,natural-adapted-index-j)",
            "actual_interval_endpoints_materialized": False,
            "actual_natural_indices_materialized": False,
            "actual_image_pullback_common_refinement_ranks_materialized": False,
            "global_invariant_cone_carries_every_image_curve": contracts["cone"]["strict_forward_invariance"],
            "recut_schema_frontier_installed": True,
            "parameterized_actual_recut_instance_registry_installed": False,
            "actual_recut_instance_count": 0,
            "finite_recut_instance_count_claimed": False,
            "half_open_owner_contract_inherited_from_Round50": contracts["ownership"]["half_open_endpoint_owner"],
        },
        "owner_candidate_replay_counts": {
            "parent_cells": 72,
            "three_leg_replays": 216,
            "HIT_cells": 8,
            "BYPASS_cells_with_actual_winner": 64,
            "residual_cells": 0,
        },
        "uninstalled_actual_child_F5_F6_frontier": {
            "universal_template_scope": contracts["universal"]["scope"],
            "one_step_adapted_inverse_strict_upper": qstr(THETA),
            "one_step_log_variation_strict_upper": qstr(ONE_STEP_LOG_VARIATION),
            "three_step_adapted_inverse_strict_upper": qstr(THREE_STEP_THETA),
            "three_step_log_variation_strict_upper": qstr(THREE_STEP_LOG_VARIATION),
            "area_Jacobian_used": False,
            "chart_norm_used": False,
            "restriction_monotonicity_requires_future_actual_child_and_recut_ID_binding": True,
            "per_leg_per_roof_F5_F6_immutable_slots_installed": False,
            "finite_slot_instance_count_claimed": False,
            "first_missing_evidence": (
                "actual image-recut interval endpoints, natural adapted indices, and pulled-back finite "
                "common-refinement ranks on the same child IDs"
            ),
        },
        "gate5_actual_child_field_status": {
            **{f"F{i}": "CERTIFIED_PARAMETERIZED_ON_EVERY_NONEMPTY_ROUND120_ACTUAL_CHILD" for i in range(1, 5)},
            **{f"F{i}": "NOT_INSTALLED_ON_ROUND120_ACTUAL_CHILD" for i in range(5, 19)},
        },
        "rank3_actual_child_field_maturity": "4/18",
        "gate5_global_maturity": "10/18",
        "complete_18_field_block_count": 0,
        "gate5_block_count": 0,
        "cm2_verdict": "NO-GO_FOR_CLAIM",
        "natural_boundary_ledger": {
            "c0_zero": "source grazing singular trace; owned by the singular ledger",
            "c3_zero": "HIT designated third tangency; owned by the singular ledger",
            "b3_zero": "BYPASS designated tangent boundary; owned by the singular ledger",
            "regular_child_scope": "c0>0 and c3>0 (HIT), or c0>0 and b3>0 (BYPASS)",
            "owner_priority": {
                "natural_boundary_overrides_artificial_rules": True,
                "artificial_owner_rule": "conjunction of every applicable unique half-open owner",
                "artificial_layers": [
                    "Round113 dyadic half-open owner",
                    "Round117 homogeneity half-open owner",
                    "corrected source-adapted half-open owner",
                ],
            },
            "round117_boundary_ownership_ledger_sha256": values["r117"]["boundary_ownership_ledger_sha256"],
        },
        "strict_scope": (
            "fixed-s=0 Borel-parameterized canonical parent-W intersections with the 72 Round113/117 "
            "regular relative-interior operator-cell root graphs, child-local F1-F4, and an explicitly "
            "uninstalled three-image-recut/F5-F6 frontier schema"
        ),
        "strict_nonclaims": [
            "the compact Round31 Q2 parent-W registry is physically disjoint and is not reused as this grazing registry",
            "no finite integer count of the Borel-parameterized child or recut registry is claimed",
            "c0=0, c3=0, and b3=0 remain natural singular-ledger strata and are not regular children",
            "no endpoint-inclusive bounded physical two-sided collar, cross-trace union reach, or whole-face owner atlas is installed",
            "actual image recut instances and child-local F5/F6 are not installed; the stored F5/F6 constants are frontier templates only",
            "F5-F18 are not installed on the Round120 actual children",
            "child-local 4/18 does not upgrade the global Gate5 10/18 maturity or create a complete block",
            "Gate5 and CM2 remain unavailable",
        ],
        "upstream_and_helper_pins": PINS,
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": closed_digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    document = build(args.precision_bits)
    args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")
    print("PARAMETERIZED_ACTUAL_CHILD_REGISTRY: CERTIFIED")
    print("RANK3_ACTUAL_CHILD_FIELDS: 4/18")
    print("GATE5_GLOBAL: 10/18")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
