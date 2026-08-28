#!/usr/bin/env python3
"""Gate-3 forward-time retraction audit and one immutable row orbit.

The predecessor's corrected audit retracts sixteen algebraic common-tangent
roots: the competing contact has negative flight time and hence is behind the
source.  This certificate independently replays that obstruction, then
certifies one complete four-element Jx/Jy orbit of compact connected physical
subrows with constant miss trace and constant parameter-coarea polarity.

No maximal global component registry, global DQ, or scalar matching is
claimed.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_owner_voronoi_event_registry_cert as frozen


ctx.prec = 320
Q = Fraction
HERE = Path(__file__).resolve().parent
PREDECESSOR = HERE / "cm2-gate3-owner-voronoi-event-registry-manifest-2026-07-15.json"
PREDECESSOR_SHA256 = "d7b1f9d879b9c02257552a6c51fad16de477e60deaac250b4fc55a13be44e8e5"
PREDECESSOR_SHA_MANIFEST = (
    HERE / "cm2-gate3-owner-voronoi-event-registry-manifest-2026-07-15.sha256"
)
PREDECESSOR_SHA_MANIFEST_SHA256 = (
    "2cb449e242b71e83f6b1d464b44f7ea64c8106b04c95e153fa15805004295fd4"
)
V52_MANIFEST = HERE / "cm2-v52-manifest.sha256"
V52_MANIFEST_SHA256 = "5cef5b8e60f0cfe2291da6bb34b2c57eed6cf2d1a13d164b74b566f752b6b368"
RESOLVER_MANIFEST = (
    HERE / "cm2-gate3-endpoint-descriptor-resolver-manifest-2026-07-15.json"
)
RESOLVER_MANIFEST_SHA256 = (
    "5ad53024dc83ed2118abce6b861cfb1059db4b205789fca6082403e599451f99"
)
RESOLVER_SHA_MANIFEST = (
    HERE / "cm2-gate3-endpoint-descriptor-resolver-manifest-2026-07-15.sha256"
)
RESOLVER_SHA_MANIFEST_SHA256 = (
    "4754427761dce6c9a359d9ce3f7f0c549335fb1cdbddb96df8df66f4b883c4e8"
)
TARGET_BY_ID = {target.target_id: target for target in base.TARGETS}


# These are exactly the sixteen collars claimed as physical before the
# forward-time audit.  The corrected test below proves ell_other<0 on every
# whole collar, so none is a physical forward endpoint.
RETRACTED_SEEDS = (
    ("G", "G[1,1]", 1, "W[-3,-2]", -1, -1, Q(584871,838860800), Q(233949,335544320)),
    ("G", "G[1,1]", 1, "G[-3,-2]", -1, -1, Q(1698461,3355443200), Q(849231,1677721600)),
    ("G", "G[-1,1]", 1, "W[1,-3]", -1, -1, Q(318859,838860800), Q(1275439,3355443200)),
    ("G", "G[-1,1]", 1, "G[2,-3]", -1, -1, Q(462833,1677721600), Q(925667,3355443200)),
    ("G", "G[-1,-1]", 1, "W[2,1]", -1, -1, Q(-233949,335544320), Q(-584871,838860800)),
    ("G", "G[-1,-1]", 1, "G[3,2]", -1, -1, Q(-849231,1677721600), Q(-1698461,3355443200)),
    ("G", "G[1,-1]", 1, "W[-2,2]", -1, -1, Q(-1275439,3355443200), Q(-318859,838860800)),
    ("G", "G[1,-1]", 1, "G[-2,3]", -1, -1, Q(-925667,3355443200), Q(-462833,1677721600)),
    ("G", "G[1,-1]", -1, "W[-3,1]", 1, -1, Q(584871,838860800), Q(233949,335544320)),
    ("G", "G[1,-1]", -1, "G[-3,2]", 1, -1, Q(1698461,3355443200), Q(849231,1677721600)),
    ("G", "G[-1,-1]", -1, "W[1,2]", 1, -1, Q(318859,838860800), Q(1275439,3355443200)),
    ("G", "G[-1,-1]", -1, "G[2,3]", 1, -1, Q(462833,1677721600), Q(925667,3355443200)),
    ("G", "G[-1,1]", -1, "W[2,-2]", 1, -1, Q(-233949,335544320), Q(-584871,838860800)),
    ("G", "G[-1,1]", -1, "G[3,-2]", 1, -1, Q(-849231,1677721600), Q(-1698461,3355443200)),
    ("G", "G[1,1]", -1, "W[-2,-3]", 1, -1, Q(-1275439,3355443200), Q(-318859,838860800)),
    ("G", "G[1,1]", -1, "G[-2,-3]", 1, -1, Q(-925667,3355443200), Q(-462833,1677721600)),
)


LOCAL_ORBIT = (
    ("G:E", Q(0), Q(1,100000), "W[0,0]", 1, "G[1,1]", "id"),
    ("G:W", Q(0), Q(1,100000), "W[-1,0]", -1, "G[-1,1]", "Jx"),
    ("G:E", Q(-1,100000), Q(0), "W[0,-1]", -1, "G[1,-1]", "Jy"),
    ("G:W", Q(-1,100000), Q(0), "W[-1,-1]", 1, "G[-1,-1]", "JxJy"),
)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()


def verify_predecessors() -> dict[str, Any]:
    assert sha256_path(PREDECESSOR) == PREDECESSOR_SHA256
    assert sha256_path(PREDECESSOR_SHA_MANIFEST) == PREDECESSOR_SHA_MANIFEST_SHA256
    assert sha256_path(V52_MANIFEST) == V52_MANIFEST_SHA256
    assert sha256_path(RESOLVER_MANIFEST) == RESOLVER_MANIFEST_SHA256
    assert sha256_path(RESOLVER_SHA_MANIFEST) == RESOLVER_SHA_MANIFEST_SHA256
    data = json.loads(PREDECESSOR.read_text(encoding="utf-8"))
    assert data["full_window_first_pass"]["initial_unresolved_descriptor_count"] == 288
    adaptive = data["adaptive_endpoint_completion"]
    assert adaptive["descriptors_fully_resolved_after_subdivision"] == 284
    assert adaptive["merged_transition_collar_count"] == 4
    assert adaptive["exact_third_target_tangency_vertices"] == 0
    assert adaptive["numerically_unresolved_transition_collar_count"] == 0
    completion = data["global_completion"]
    assert completion["retracted_sixteen_physical_transition_vertex_claim"] is True
    assert completion["corrected_physical_transition_vertex_count"] == 0
    resolver = json.loads(RESOLVER_MANIFEST.read_text(encoding="utf-8"))
    assert resolver["status"] == "CERTIFIED_320_PHYSICALLY_EMPTY_UNRESOLVED_ZERO"
    verdict = resolver["verdict"]
    assert verdict["empty"] == 320
    assert verdict["unresolved"] == 0
    assert sum(verdict[key] for key in (
        "physical_boundary", "physical_duplicate", "physical_earlier",
        "physical_later", "physical_joint",
    )) == 0
    return data


def forward_time_retraction_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for source, target, eps_t, other, eps_b, branch, s0, s1 in RETRACTED_SEEDS:
        initial, geometry = frozen.common_tangent_source_geometry(
            source, target, eps_t, other, eps_b, branch, s0, s1,
        )
        assert initial == "source_intersection" and geometry is not None
        _s, _qx, _qy, _ux, _uy, ell_t, ell_other, *_rest = geometry
        assert bool(ell_t > 0) and bool(ell_t < base.arbq(base.TAU_MAX))
        assert bool(ell_other < 0)
        rows.append({
            "source": source,
            "target": target,
            "epsilon_target": eps_t,
            "other": other,
            "epsilon_other": eps_b,
            "line_branch": branch,
            "s_collar": [str(s0), str(s1)],
            "forward_target_time": str(ell_t),
            "other_time": str(ell_other),
            "classification": "NONPHYSICAL_OTHER_CONTACT_BEHIND_SOURCE",
        })
    assert len(rows) == 16
    return {
        "replayed_retracted_seed_count": len(rows),
        "uniform_forward_target_count": len(rows),
        "uniform_other_behind_source_count": len(rows),
        "physical_forward_joint_vertex_count": 0,
        "rows_sha256": canonical_digest(rows),
        "conclusion": (
            "the sixteen exact algebraic common-tangent roots are not "
            "physical forward event vertices"
        ),
    }


def immutable_local_orbit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for chart, t0, t1, target, epsilon, miss, symmetry in LOCAL_ORBIT:
        row = frozen.certify_miss_seed(chart, t0, t1, target, epsilon, miss)
        assert row["parameter_coarea_polarity"] in (-1, 1)
        row.update({
            "symmetry": symmetry,
            "connectedness_witness": (
                "continuous tangency graph over the connected closed "
                "rational (t,s) rectangle"
            ),
            "row_status": "CERTIFIED_COMPACT_IMMUTABLE_PHYSICAL_SUBROW",
        })
        rows.append(row)
    assert [row["parameter_coarea_polarity"] for row in rows] == [1,-1,1,-1]
    assert len({row["miss_owner"] for row in rows}) == 4
    representative = rows[0]
    assert rows[1]["target"] == frozen.reflected_target_fast(
        "G", "vertical", representative["target"]
    )
    assert rows[2]["target"] == frozen.reflected_target_fast(
        "G", "horizontal", representative["target"]
    )
    assert rows[1]["miss_owner"] == frozen.reflected_target_fast(
        "G", "vertical", representative["miss_owner"]
    )
    assert rows[2]["miss_owner"] == frozen.reflected_target_fast(
        "G", "horizontal", representative["miss_owner"]
    )
    assert rows[0]["signed_p_coarea_interval"] == rows[2]["signed_p_coarea_interval"]
    assert rows[1]["signed_p_coarea_interval"] == rows[3]["signed_p_coarea_interval"]
    return {
        "orbit_representative": "G:W[0,0]:epsilon=+1",
        "symmetry_group": "{id,Jx,Jy,JxJy}",
        "row_count": len(rows),
        "full_parameter_window_on_every_row": True,
        "constant_miss_trace_on_every_row": True,
        "constant_nonzero_parameter_coarea_polarity_on_every_row": True,
        "polarity_pattern": [1,-1,1,-1],
        "symmetry_invariant_scalar_current_cancels_pairwise": True,
        "arbitrary_test_distributional_cancellation": False,
        "rows": rows,
        "rows_sha256": canonical_digest(rows),
        "maximal_connected_sheet_components": False,
    }


def finite_global_reduction() -> dict[str, Any]:
    active: set[tuple[str,str,int]] = set()
    inactive = 0
    for source in ("G", "W"):
        for target in frozen.GLOBAL_CANDIDATES[source]:
            for epsilon in (-1,1):
                if TARGET_BY_ID[target].obstacle != source:
                    active.add((source,target,epsilon))
                else:
                    inactive += 1
    assert len(active) == 128 and inactive == 160
    target_target = sum(
        4 * (len(frozen.GLOBAL_CANDIDATES[source]) - 1)
        for source, _target, _epsilon in active
    )
    source_grazing = 2 * len(active)
    parameter_boundary = 2 * len(active)
    polarity = len(active)
    assert (target_target,source_grazing,parameter_boundary,polarity) == (
        36352,256,256,128
    )
    seen: set[tuple[str,str,int]] = set()
    orbits: list[list[tuple[str,str,int]]] = []
    for sheet in sorted(active):
        if sheet in seen:
            continue
        source,target,epsilon = sheet
        jx = (source,frozen.reflected_target_fast(source,"vertical",target),-epsilon)
        jy = (source,frozen.reflected_target_fast(source,"horizontal",target),-epsilon)
        jxy = (source,frozen.reflected_target_fast(source,"horizontal",jx[1]),epsilon)
        orbit = {sheet,jx,jy,jxy}
        assert len(orbit) == 4 and orbit <= active
        seen.update(orbit)
        orbits.append(sorted(orbit))
    assert seen == active and len(orbits) == 32
    return {
        "global_signed_sheets": len(active)+inactive,
        "parameter_active_cross_color_sheets": len(active),
        "inactive_same_color_sheets": inactive,
        "active_Jx_Jy_orbits": len(orbits),
        "active_sheet_orbits_sha256": canonical_digest(orbits),
        "raw_active_endpoint_descriptors": (
            target_target+source_grazing+parameter_boundary+polarity
        ),
        "raw_active_endpoint_breakdown": {
            "target_target": target_target,
            "source_grazing": source_grazing,
            "parameter_boundary": parameter_boundary,
            "polarity_split": polarity,
        },
        "remaining_problem": (
            "enumerate connected visible components, quotient all physical "
            "duplicate endpoints, and emit maximal constant-label rows"
        ),
    }


def full_summary() -> dict[str, Any]:
    verify_predecessors()
    return {
        "predecessor_manifest_sha256": PREDECESSOR_SHA256,
        "resolver_manifest_sha256": RESOLVER_MANIFEST_SHA256,
        "full_320_descriptor_resolution": {
            "status": "CERTIFIED_PHYSICALLY_EMPTY",
            "descriptor_count": 320,
            "empty": 320,
            "physical": 0,
            "unresolved": 0,
        },
        "corrected_forward_time_audit": forward_time_retraction_audit(),
        "certified_immutable_local_orbit": immutable_local_orbit(),
        "global_finite_reduction": finite_global_reduction(),
        "completion": {
            "sixteen_nonforward_vertex_claims_retracted_and_replayed": True,
            "one_complete_Jx_Jy_immutable_subrow_orbit": True,
            "all_288_sheet_connected_components": None,
            "global_duplicate_endpoint_quotient": None,
            "global_immutable_physical_event_rows": None,
            "global_dq": None,
            "global_scalar_matching": None,
        },
    }


def main() -> None:
    summary = full_summary()
    print("GATE3_RETRACTED_16_NONFORWARD_VERTEX_AUDIT: CERTIFIED")
    print("GATE3_ONE_COMPLETE_JX_JY_IMMUTABLE_SUBROW_ORBIT: CERTIFIED")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("GATE3_ALL_288_CONNECTED_EVENT_ROWS: NOT_CERTIFIED")
    print("GATE3_GLOBAL_DQ_SCALAR_MATCHING: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
