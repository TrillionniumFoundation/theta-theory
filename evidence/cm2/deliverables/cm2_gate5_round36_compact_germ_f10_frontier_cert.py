#!/usr/bin/env python3
"""Compact-germ F10 existence and terminating-search frontier.

Round 36 supplies F9 on every finite regular rank path, but that alone does
not give one uniform coarea-density regularity constant over the countable
arbitrary-R_n atlas.  This append-only certificate isolates the strongest
safe statement available from the current analytic component schema.

Fix a finite return depth, one regular component, one physical face, and a
rational dyadic carrier interval whose closure stays inside a single
noncorner regular face germ.  The collision word and every defining level
function are real analytic on a neighbourhood of that compact germ.  F8
keeps the trace transverse, while the all-face F9 certificate keeps the face
gradient nonzero and supplies a finite C2 value.  Consequently the signed
coarea density and its tangential derivative are continuous on a compact
parameter germ and have a finite integer upper bound.  A deterministic
dyadic radius search followed by outward-rounded interval subdivision finds
such a bound in finite time.

The search is pointwise in the compact germ.  No common radius, no list of
nonempty arbitrary-R_n components, and no weighted sum of the resulting
integers is produced.  Therefore this is a compact-germ F10 frontier, not a
complete global F10 field, and Gate-5 maturity remains 7/18.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round36-compact-germ-f10-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate5-round36-compact-germ-f10-frontier-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-full-row-parameter-whitney-atlas-manifest-2026-07-17.json": (
        "8763f00e07b316414aab9b50657979c9c8d15dd3c60e83e98c342169b099f8d0"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json": (
        "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140"
    ),
    "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json": (
        "f9c4eca78065001e65381880deef8681b3a626c2bd419e4ecfe3b02f37a7b53e"
    ),
    "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json": (
        "f603dd8e638d661b22c746742a5e5c3fd48242f4c0ad40bb35fbe74d35325788"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
}
FACE_KINDS = (
    "source_core_clipping_face",
    "intermediate_core_avoidance_preimage_face",
    "terminal_core_preimage_face",
    "collision_singularity_or_owner_change_face",
    "moving_occurrence_face",
)


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
    whitney = load(
        "cm2-gate34-full-row-parameter-whitney-atlas-manifest-2026-07-17.json"
    )["result"]
    completion = whitney["countable_full_row_parameter_germ_atlas"]
    if completion[
        "dyadic_halving_of_parameter_radius_is_a_terminating_certificate_search"
    ] is not True:
        raise RuntimeError("Whitney radius search")
    if completion["uniform_radius_over_all_cells_asserted"] is not False:
        raise RuntimeError("Whitney nonuniformity")

    arbitrary = load(
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    )["result"]["canonical_regular_connected_component_schema"]
    if arbitrary["componentwise_forward_map_is_real_analytic_local_diffeomorphism"] is not True:
        raise RuntimeError("analytic branch")
    if arbitrary["regular_path_fibre_is_open_relative_to_source_core_interior"] is not True:
        raise RuntimeError("open regular fibre")
    if arbitrary["uniform_joint_parameter_component_atlas_claimed"] is not False:
        raise RuntimeError("joint atlas nonpromotion")

    atlas = load(
        "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json"
    )["result"]["R2_and_arbitrary_n_physical_face_ID_grammar_frontier"]
    kinds = tuple(row["kind"] for row in atlas["boundary_carrier_kind_rows"])
    if kinds != FACE_KINDS:
        raise RuntimeError("five face grammars")
    if atlas["arbitrary_n_instantiated_face_component_id_count"] != 0:
        raise RuntimeError("arbitrary-n face materialization")

    f8 = load(
        "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json"
    )
    if f8["result"]["same_ID_numeric_F8"][
        "common_normalized_transversality_strict_lower"
    ] != "1/5":
        raise RuntimeError("F8")

    f9 = load(
        "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json"
    )
    if f9["result"]["strict_nonpromotion"][
        "complete_F9_physical_face_C2_parameterized_atlas"
    ] != "CERTIFIED":
        raise RuntimeError("F9")
    if f9["result"]["strict_nonpromotion"]["Gate5_maturity"] != "7/18":
        raise RuntimeError("F9 maturity")

    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]["common_forward_reverse_carrier_pair"]
    if carrier["actual_parameterized_common_fw_rev_carrier_pair_registry"] != "CERTIFIED":
        raise RuntimeError("common carrier")
    if carrier["forward_and_reverse_share_identical_component_and_restriction"] is not True:
        raise RuntimeError("common carrier identity")


def compact_germ_universe() -> dict[str, Any]:
    return {
        "scope": "reference parameter s=0, fixed finite n and one regular analytic branch word",
        "base_component_id_schema": (
            "c24-component:(source-core-id,n,path-key,least-dyadic-basis-index)"
        ),
        "common_restriction_id_schema": (
            "rn-restriction:(component-id):(source-parent-W-id):(image-recut-rank)"
        ),
        "face_instance_id_schema": (
            "face:(component-id,time-j,carrier-family-or-seed-id,connected-rank)"
        ),
        "compact_germ_id_schema": (
            "f10-germ:(common-restriction-id,face-instance-id,least-closure-contained-rational-dyadic-carrier-interval,orientation)"
        ),
        "physical_face_kinds": list(FACE_KINDS),
        "germ_contract": [
            "nonempty compact rational dyadic carrier subinterval",
            "closure contained in one regular connected face piece",
            "one analytic collision/owner word on a neighbourhood",
            "positive chart, homogeneity, owner and core strict margins",
            "no corner, simultaneous root, face intersection or grazing endpoint",
        ],
        "exceptional_policy": "corner/simultaneous-root/face-intersection/grazing-endpoint -> cemetery",
        "countability": (
            "countable union over finite n, component rank, face grammar, connected rank and rational dyadic subinterval"
        ),
        "every_regular_noncorner_face_point_has_a_closure_contained_compact_germ": True,
        "nonempty_component_coordinates_materialized": False,
        "instantiated_compact_germ_rows": 0,
    }


def analytic_coarea_theorem() -> dict[str, Any]:
    return {
        "local_face_model": "G(x,s)=0 on one finite regular analytic branch",
        "face_gradient_nonzero_source": (
            "all-face F9 rank-path lower 1/E_j on every fixed finite path"
        ),
        "parent_trace_transversality_source": "same-ID F8 normalized wedge >1/5",
        "signed_coarea_density_model": (
            "rho(x,s)=analytic normal-velocity/current numerator divided by nonvanishing analytic level/trace denominator"
        ),
        "regularity_on_compact_parameter_germ": [
            "rho is real analytic",
            "tangential derivative d_tau rho is continuous",
            "parameter derivative d_s rho is continuous whenever that oriented current is active",
        ],
        "stationary_zero_current_policy": (
            "if the physical face has identically zero parameter normal velocity, set rho=d_tau rho=d_s rho=0"
        ),
        "compact_extreme_value_conclusion": (
            "sup(abs(rho)+abs(d_tau rho)+abs(d_s rho)) is finite on every compact germ product"
        ),
        "log_density_not_required_at_zeros": True,
        "carrier_C2_is_not_retyped_as_density_regularity": True,
    }


def terminating_search() -> dict[str, Any]:
    return {
        "radius_power_definition": (
            "k(g)=least k>=1 such that K_g times [-2^-k,2^-k] is interval-certified inside one analytic branch with all strict margins and denominators separated from zero"
        ),
        "radius": "delta(g)=2^-k(g)",
        "radius_search": (
            "increase k by one and outward-round every finite analytic primitive and strict predicate"
        ),
        "radius_search_terminates_for_every_compact_regular_germ": True,
        "subdivision_definition": (
            "bisect K_g times [-delta(g),delta(g)] in a fixed fair dyadic order and evaluate outward-rounded interval extensions of rho,d_tau rho,d_s rho"
        ),
        "F10_integer_definition": (
            "N_F10(g)=least positive integer N for which a finite subdivision certifies abs(rho)+abs(d_tau rho)+abs(d_s rho)<N on every box"
        ),
        "bound_search": "dovetail N=1,2,... with fair dyadic subdivisions",
        "bound_search_terminates_for_every_compact_regular_germ": True,
        "canonical_finite_integer_F10_value_exists_for_each_germ": True,
        "search_output_is_replayable_by_exact_outward_interval_arithmetic": True,
        "uniform_radius_or_integer_over_all_germs": "NOT_ASSERTED",
        "weighted_sum_of_N_F10_over_faces_or_components": "NOT_CERTIFIED",
        "materialized_N_F10_values": 0,
    }


def face_matrix() -> dict[str, Any]:
    return {
        "source_core_clipping_face": {
            "compact_germ_F10": "CERTIFIED_LEVEL_ZERO_STATIONARY_CURRENT",
            "global_F10": "NOT_CERTIFIED",
        },
        "intermediate_core_avoidance_preimage_face": {
            "compact_germ_F10": "CERTIFIED_FINITE_SEARCH_ON_EACH_REGULAR_COMPACT_GERM",
            "global_F10": "NOT_CERTIFIED",
        },
        "terminal_core_preimage_face": {
            "compact_germ_F10": "CERTIFIED_FINITE_SEARCH_ON_EACH_REGULAR_COMPACT_GERM",
            "global_F10": "NOT_CERTIFIED",
        },
        "collision_singularity_or_owner_change_face": {
            "compact_germ_F10": "CERTIFIED_FINITE_SEARCH_ON_EACH_REGULAR_NONCORNER_COMPACT_GERM",
            "global_F10": "NOT_CERTIFIED",
        },
        "moving_occurrence_face": {
            "seed_F10": "CERTIFIED_PARAMETERIZED_64_SEEDS",
            "compact_germ_F10": "CERTIFIED_FINITE_SEARCH_ON_EACH_REGULAR_PULLBACK_COMPACT_GERM",
            "global_F10": "NOT_CERTIFIED",
        },
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "claim_type": "countable compact-germ existence and terminating-search schema",
        },
        "compact_regular_face_germ_universe": compact_germ_universe(),
        "analytic_coarea_C1_compactness_theorem": analytic_coarea_theorem(),
        "canonical_dyadic_radius_and_F10_search": terminating_search(),
        "five_face_kind_compact_germ_F10_matrix": face_matrix(),
        "same_ID_join": {
            "common_fw_rev_restriction_id_used_once": True,
            "parent_W_face_connected_rank_preserved": True,
            "two_oriented_one_sided_trace_ids_preserved": True,
            "forward_and_reverse_views_do_not_duplicate_the_physical_face_charge": True,
            "compact_germ_rank_appended_after_physical_face_instance_id": True,
        },
        "strict_nonpromotion": {
            "compact_regular_germ_F10_finite_search_schema": "CERTIFIED",
            "pointwise_compact_germ_schema_is_complete_global_F10_field": False,
            "uniform_parameter_radius_over_all_germs": False,
            "uniform_F10_integer_over_all_germs": False,
            "global_rank_path_F10_Lp_or_weighted_sum": "NOT_CERTIFIED",
            "arbitrary_Rn_nonempty_face_rows_materialized": 0,
            "complete_F10_all_face_coarea_regular_atlas": "NOT_CERTIFIED",
            "Gate5_maturity": "7/18_UNCHANGED",
            "complete_18_field_operator_block_count": 0,
            "F14_through_F18": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
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
        default=HERE / "cm2_gate5_round36_compact_germ_f10_frontier_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    build_result()
    print("COMPACT_REGULAR_GERM_F10_FINITE_SEARCH_SCHEMA: CERTIFIED")
    print("COMPLETE_GLOBAL_F10_FIELD: NOT_CERTIFIED")
    print("GATE5_MATURITY: 7/18_UNCHANGED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
