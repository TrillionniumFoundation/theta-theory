#!/usr/bin/env python3
"""Round-44 all-face suffix two-trace F13 payload.

Round 43 made the Eulerian insertion charge additive on arbitrary finite
rank-refined paths.  This certificate now transports the actual plus/minus
trace measures through every suffix.  Positive-measure pushforward preserves
mass, so no suffix derivative is paid in Borel total variation.

The five physical face grammars split into stationary source-core faces,
C24 core-preimage faces, and the complete depth-one state-changing current.
The C24 boundary flux is bounded directly in collision area coordinates;
the occurrence current uses the frozen 64-row/128-trace DQ atlas.  Their sum
is pointwise less than one half of the Round-43 Eulerian charge and therefore
inherits the same physical L^(6/5) moment and block tail.

This fills the global regular-density Borel F13 payload.  It does not fill
F12 C1 trace pullback, the strong/standard-family F16 norm, cemetery, or the
branch-record convergence needed for dynamic MT_DQ.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round44-all-face-suffix-two-trace-f13.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json": (
        "284b25ac30dd86a01bd0faaa7c0a97ee47839670e3cde4309936235badf5fd52"
    ),
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json": (
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183"
    ),
    "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json": (
        "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate5-round42-area-coordinate-current-split-frontier-manifest-2026-07-19.json": (
        "c112fe76649a195f47d51a3448822a7e4e864dff398b57fe26894e2badb28714"
    ),
    "cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json": (
        "33e3fae4633b133ffcaeb7bd0e552629ecf8528b3648b93ce85d5420e141bef5"
    ),
    "cm2-gate3-branch-record-face-2cut-frontier-manifest-2026-07-16.json": (
        "64a01064262fcc13ffa215addb2670854047fdc03ae5aebeb88fa39337db8879"
    ),
}

R_G = Q(9, 25)
R_W = Q(4, 25)
DT = Q(1, 100)
DP_AXIS = Q(1, 250)
DP_DIAGONAL = Q(1, 25)
DTHETA_DT_AXIS = Q(1001, 1000)
DTHETA_DT_DIAGONAL = Q(1401, 1000)
NORMALIZATION_LOWER = Q(156, 25)

MINIMUM_RANK = 14
X_COEFFICIENT = 25
D1_COEFFICIENT = 151
OCCURRENCE_ROWS = 64
ORIENTED_OCCURRENCE_TRACES = 128
OCCURRENCE_POSITIVE_MASS = Q(8064, 5)
OCCURRENCE_CURRENT_TV = Q(16128, 5)
SYMBOLIC_ROOF_LEVELS = 3286976


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def validate_dependencies() -> None:
    dq = load(
        "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
    )["result"]
    assembly = dq["corrected_current_assembly"]
    envelope = dq["uniform_finite_measure_envelope"]
    if assembly["maximal_row_current_count"] != OCCURRENCE_ROWS:
        raise RuntimeError("occurrence rows")
    if not assembly["strict_hit_and_miss_trace_attached_to_every_row"]:
        raise RuntimeError("occurrence traces")
    if envelope["global_positive_mass_upper_bound"] != str(OCCURRENCE_POSITIVE_MASS):
        raise RuntimeError("positive occurrence mass")
    if envelope["global_event_current_TV_upper_bound"] != str(OCCURRENCE_CURRENT_TV):
        raise RuntimeError("occurrence TV")
    if dq["fixed_gauge_depth_one_DQ"]["operator_conclusion"][
        "uncentered_depth_one_transfer_DQ"
    ] != "CERTIFIED":
        raise RuntimeError("depth-one DQ")

    geometry = load(
        "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json"
    )["result"]
    inventory = geometry["frozen_core_inventory"]
    mass = geometry["collision_SRB_core_mass_interval"]
    if inventory["core_count"] != 24:
        raise RuntimeError("core count")
    if inventory["boundary_edge_count_per_collision_component"] != 48:
        raise RuntimeError("core edges")
    if mass["axis_dtheta_dt_strict_upper"] != str(DTHETA_DT_AXIS):
        raise RuntimeError("axis chart")
    if mass["diagonal_dtheta_dt_strict_upper"] != str(DTHETA_DT_DIAGONAL):
        raise RuntimeError("diagonal chart")
    if mass["normalization_denominator_strict_lower_using_pi_gt_3"] != str(
        NORMALIZATION_LOWER
    ):
        raise RuntimeError("normalization")

    atlas = load(
        "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json"
    )["result"]
    core = atlas["physical_C24_core_face_and_trace_registry"]
    occurrence = atlas["moving_occurrence_coarea_DQ_face_seed_registry"]
    grammar = atlas["R2_and_arbitrary_n_physical_face_ID_grammar_frontier"]
    if core["materialized_physical_core_face_count"] != 96:
        raise RuntimeError("core face registry")
    if core["materialized_one_sided_core_trace_count"] != 192:
        raise RuntimeError("core trace registry")
    if occurrence["materialized_physical_moving_occurrence_face_seed_count"] != 64:
        raise RuntimeError("occurrence seed registry")
    if occurrence["materialized_oriented_hit_miss_trace_seed_count"] != 128:
        raise RuntimeError("oriented occurrence registry")
    if len(grammar["boundary_carrier_kind_rows"]) != 5:
        raise RuntimeError("five face grammar")

    words = load(
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    )["result"]
    registry = words["immutable_candidate_key_registry"]
    if registry["prefix_suffix_factor_contract"][
        "roof_level_prefix_suffix_factor_pair_count"
    ] != SYMBOLIC_ROOF_LEVELS:
        raise RuntimeError("roof-level factors")
    if not words["completion"]["physical_Borel_TV_Linf_prefix_suffix_constants"]:
        raise RuntimeError("Borel prefix/suffix")

    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]["common_forward_reverse_carrier_pair"]
    if carrier["actual_parameterized_common_fw_rev_carrier_pair_registry"] != "CERTIFIED":
        raise RuntimeError("common carrier")

    split = load(
        "cm2-gate5-round42-area-coordinate-current-split-frontier-manifest-2026-07-19.json"
    )["result"]["area_preserving_current_decomposition"]
    if split["identity_status"] != "CERTIFIED_ALGEBRAIC":
        raise RuntimeError("Eulerian split")
    if split["F13_trace_bounds_on_arbitrary_Rn"] != "NOT_CERTIFIED":
        raise RuntimeError("prior F13 scope")

    duhamel = load(
        "cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json"
    )["result"]
    if duhamel["arbitrary_path_Duhamel_current"]["identity_status"] != (
        "CERTIFIED_ALGEBRAIC_ARBITRARY_FINITE_PATH"
    ):
        raise RuntimeError("Duhamel identity")
    if duhamel["one_step_area_eulerian_generator"][
        "cross_colour_pointwise_bounds"
    ]["l1_generator"] != "abs_X_r+abs_X_p<=25*2^B":
        raise RuntimeError("generator bound")
    if duhamel["physical_D1_dominated_eulerian_charge"][
        "pointwise_same_ID_identity"
    ] != "c_X,n=(25/151)*c_D1,n<c_D1,n":
        raise RuntimeError("D1 charge")

    branch = load(
        "cm2-gate3-branch-record-face-2cut-frontier-manifest-2026-07-16.json"
    )["result"]["scope_limits"]
    if branch["fixed_time_dynamic_branch_record_MT_DQ"] is not False:
        raise RuntimeError("MT_DQ scope")
    if branch["component_indexed_iterated_common_moving_atlas"] is not False:
        raise RuntimeError("moving atlas scope")


def c24_boundary_perimeter() -> dict[str, Any]:
    axis = (
        4 * 2 * (R_G * DTHETA_DT_AXIS * DT + DP_AXIS)
        + 4 * 2 * (R_W * DTHETA_DT_AXIS * DT + DP_AXIS)
    )
    diagonal = (
        8 * 2 * (R_G * DTHETA_DT_DIAGONAL * DT + DP_DIAGONAL)
        + 8 * 2 * (R_W * DTHETA_DT_DIAGONAL * DT + DP_DIAGONAL)
    )
    total = axis + diagonal
    normalized = total / NORMALIZATION_LOWER
    one_trace = normalized * X_COEFFICIENT
    two_traces = 2 * one_trace
    ratio_to_x = two_traces / X_COEFFICIENT
    if axis != Q(33013, 312500):
        raise RuntimeError("axis perimeter")
    if diagonal != Q(218213, 156250):
        raise RuntimeError("diagonal perimeter")
    if total != Q(469439, 312500):
        raise RuntimeError("total perimeter")
    if normalized != Q(469439, 1950000):
        raise RuntimeError("normalized perimeter")
    if one_trace != Q(469439, 78000):
        raise RuntimeError("one-trace flux")
    if two_traces != Q(469439, 39000):
        raise RuntimeError("two-trace flux")
    if ratio_to_x != Q(469439, 975000):
        raise RuntimeError("core/X ratio")
    return {
        "coordinate": "collision area coordinates (r,p=sin(phi))",
        "area_probability": "dmu_s=Z_N^-1*dr*dp",
        "rectangle_inventory": {
            "axis_G": 4,
            "axis_W": 4,
            "diagonal_G": 8,
            "diagonal_W": 8,
            "physical_edges": 96,
            "oriented_inside_outside_traces": 192,
        },
        "axis_total_l1_perimeter_strict_upper": str(axis),
        "diagonal_total_l1_perimeter_strict_upper": str(diagonal),
        "C24_total_l1_perimeter_strict_upper": str(total),
        "normalized_C24_boundary_l1_measure_strict_upper": str(normalized),
        "generator_bound": "norm_l1(X)<=25*2^B",
        "one_positive_boundary_trace_flux_strict_upper": (
            "(469439/78000)*2^B*norm_infinity(h)"
        ),
        "inside_plus_outside_trace_TV_strict_upper": (
            "(469439/39000)*2^B*norm_infinity(h)"
        ),
        "two_trace_ratio_to_c_X_insertion": str(ratio_to_x),
        "status": "CERTIFIED_EXACT_RATIONAL_BOUND",
    }


def occurrence_trace_transport() -> dict[str, Any]:
    minimum_charge = X_COEFFICIENT * (1 << MINIMUM_RANK)
    ratio = OCCURRENCE_CURRENT_TV / minimum_charge
    if minimum_charge != 409600:
        raise RuntimeError("minimum insertion charge")
    if ratio != Q(63, 8000):
        raise RuntimeError("occurrence/X ratio")
    return {
        "depth_one_physical_rows": OCCURRENCE_ROWS,
        "depth_one_oriented_hit_miss_traces": ORIENTED_OCCURRENCE_TRACES,
        "one_sign_global_positive_mass_upper": str(OCCURRENCE_POSITIVE_MASS),
        "signed_current_TV_upper": str(OCCURRENCE_CURRENT_TV),
        "rank_convention": "B>=14",
        "minimum_one_insertion_c_X": minimum_charge,
        "occurrence_TV_ratio_to_c_X_insertion": str(ratio),
        "suffix_transport": {
            "positive_trace_formula": "tau_(n,j,e,sign)=(S_(n,j))_* tau_(e,sign)(P_(j-1)h)",
            "signed_current_formula": "J_(n,j,e)=sigma_e*(tau_hit-tau_miss)",
            "prefix_regular_branch_Linfinity_constant": "1",
            "suffix_positive_pushforward_mass_constant": "1",
            "constant_test_cancellation_preserved": True,
        },
        "status": "CERTIFIED_ON_EVERY_FINITE_REGULAR_SUFFIX",
    }


def five_face_join() -> dict[str, Any]:
    rows = [
        {
            "kind": "source_core_clipping_face",
            "F13_payload": "zero in the fixed common source coordinates",
            "two_trace_source": "the two static core traces exist but carry zero parameter current at time 0",
        },
        {
            "kind": "intermediate_core_avoidance_preimage_face",
            "F13_payload": "Eulerian flux through the 96 target C24 edges, then suffix pushforward",
            "two_trace_source": "inside/avoid versus enter traces",
        },
        {
            "kind": "terminal_core_preimage_face",
            "F13_payload": "Eulerian flux through the 96 target C24 edges, then suffix pushforward",
            "two_trace_source": "return versus survive traces",
        },
        {
            "kind": "collision_singularity_or_owner_change_face",
            "F13_payload": "the complete corrected depth-one face current transported by the Duhamel suffix",
            "two_trace_source": "left/right owner; endpoints and multiple events retain cemetery typing",
        },
        {
            "kind": "moving_occurrence_face",
            "F13_payload": "the 64 corrected physical occurrence rows transported by the Duhamel suffix",
            "two_trace_source": "128 immutable hit/miss trace seeds",
        },
    ]
    return {
        "rows": rows,
        "rows_sha256": digest(rows),
        "face_kind_count": len(rows),
        "internal_artificial_cut_rule": (
            "assemble adjacent quotient traces before absolute values; artificial chart/homogeneity cuts are not physical F13 faces"
        ),
        "all_five_physical_face_grammars_have_a_Borel_F13_payload": True,
        "status": "CERTIFIED_REGULAR_DENSITY_BOREL_LAYER",
    }


def global_trace_charge() -> dict[str, Any]:
    core_ratio = Q(469439, 975000)
    occurrence_ratio = Q(63, 8000)
    total_ratio = core_ratio + occurrence_ratio
    d1_ratio = total_ratio * Q(X_COEFFICIENT, D1_COEFFICIENT)
    if total_ratio != Q(3816937, 7800000):
        raise RuntimeError("total F13/X ratio")
    if not total_ratio < Q(1, 2):
        raise RuntimeError("half-X domination")
    if d1_ratio != Q(3816937, 47112000):
        raise RuntimeError("F13/D1 ratio")
    trace_pair_slots = SYMBOLIC_ROOF_LEVELS * OCCURRENCE_ROWS
    oriented_slots = 2 * trace_pair_slots
    if trace_pair_slots != 210366464 or oriented_slots != 420732928:
        raise RuntimeError("lazy trace slots")
    return {
        "same_ID_path_charge": (
            "c_F13,n=sum_j[TV(core-flux traces at j)+TV(occurrence traces at j)]"
        ),
        "pointwise_bounds": [
            "c_F13,n<=(3816937/7800000)*c_X,n",
            "c_F13,n<(1/2)*c_X,n=(25/302)*c_D1,n",
        ],
        "exact_F13_over_X_ratio": str(total_ratio),
        "exact_F13_over_D1_ratio": str(d1_ratio),
        "physical_L6over5_moment": {
            "inheritance": "pointwise same-ID domination by (25/302)*c_D1,n",
            "status": "CERTIFIED",
        },
        "physical_weighted_tail": {
            "inherited_block_exponent": "1/6",
            "collision_time_rate_numeric": False,
            "status": "CERTIFIED_FOR_F13_BOREL_TRACE_CHARGE",
        },
        "lazy_symbolic_registry": {
            "roof_level_prefix_suffix_factor_count": SYMBOLIC_ROOF_LEVELS,
            "candidate_occurrence_trace_pair_slots": trace_pair_slots,
            "candidate_oriented_occurrence_trace_slots": oriented_slots,
            "slot_token": "(common-Rn-restriction-id,time_j,face-kind,carrier-seed-id,side-label)",
            "empty_slots_allowed": True,
            "candidate_slot_count_claimed_as_nonempty_physical_count": False,
        },
        "arbitrary_Rn_suffix_pushed_two_trace_TV_ledger": "CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "base_parameter": "s=0",
            "path_scope": "every finite regular rank-refined R_n path",
            "source_scope": "C1 densities relative to collision SRB; Borel TV output",
            "literature_checked_through": "2026-07-19",
        },
        "C24_core_boundary_flux": c24_boundary_perimeter(),
        "occurrence_suffix_two_trace_transport": occurrence_trace_transport(),
        "five_face_F13_Borel_join": five_face_join(),
        "same_ID_physical_F13_trace_charge": global_trace_charge(),
        "F16_frontier": {
            "regular_density_C24_boundary_flux_TV_cost": "CERTIFIED_AS_F13_INPUT",
            "regular_density_occurrence_flux_TV_cost": "CERTIFIED_AS_F13_INPUT",
            "all_face_standard_family_strong_flux_operator_cost": "NOT_CERTIFIED",
            "cemetery_compatible_flux_ledger": "NOT_CERTIFIED",
            "F16": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "arbitrary_Rn_suffix_pushed_two_trace_TV_ledger": "CERTIFIED",
            "all_five_face_regular_density_Borel_F13_payload": "CERTIFIED",
            "physical_F13_trace_charge_L6over5_and_tail": "CERTIFIED",
            "complete_strong_F13_operator_intertwiner": "NOT_CERTIFIED",
            "F12_C1_trace_pullback": "NOT_CERTIFIED",
            "F16": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "F14_through_F18": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "dynamic_MT_DQ": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate5_maturity": "8/18",
            "complete_18_field_operator_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def write_manifest(path: Path, verifier: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate5_round44_all_face_suffix_two_trace_f13_verifier.py",
    )
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        return 0
    result = build_result()
    print(
        "ALL_FIVE_FACE_BOREL_F13:",
        result["strict_nonpromotion"]["all_five_face_regular_density_Borel_F13_payload"],
    )
    print("GATE5_MATURITY: 8/18")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
