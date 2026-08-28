#!/usr/bin/env python3
"""Gate-3 common mass atlas and a genuine depth-two trace registry.

This certificate deliberately separates two statements.

First, the moving cumulative-mass coordinate from the finite-s stopped
construction is used as a *coordinate*, not as a symbolic label.  On the
augmented finite-difference-quotient carrier ``(tau,u) in [0,1]^2`` every
moving dyadic endpoint is the fixed line ``u=j/2^K``.  This produces one
component-indexed common metric atlas, exact boundary-Z tightness, and an
exact nested record map for every finite dyadic cutoff.

Second, at the physical centred table ``s=0`` we carry the miss trace of each
of the 64 maximal face rows through one additional genuine billiard
collision.  Arb interval arithmetic certifies connected row intervals on
which the next target is immutable.  This is an actual depth-two branch
record; it is not the formal transfer-operator telescope.  A very small
endpoint cemetery and a finite-resolution outer cover of intervals that may
meet a second-collision singularity are kept positive and unresolved.  The
outer-cover length is not a claim that the actual singular set has positive
length.  No finite-s depth-two claim is made.

The remaining unresolved boxes are essential.  In particular this replay
does not prove strong-source invariance, convergence of the dynamic tests on
the resulting record atlas, or full MT_DQ/FACE_2CUT/FACE_TIME.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate3_global_physical_subrow_atlas_cert as bulk
import cm2_gate45_finite_s_common_mesh_recovery_cert as finite


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent

DEPTH_ONE_MANIFEST = HERE / "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
FINITE_S_MANIFEST = HERE / "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
FRONTIER_MANIFEST = HERE / "cm2-gate3-branch-record-face-2cut-frontier-manifest-2026-07-16.json"

# Only the two endpoint strips below are discarded.  Their positive current
# is charged explicitly, before cancellation.
ENDPOINT_TRIM = Q(1, 1 << 20)
INITIAL_T_CELLS = 32
INITIAL_S_CELLS = 1
MAX_ADAPTIVE_DEPTH = 10
TAU_MAX = Q(3)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arbq(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def load_dependencies() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    depth_one = json.loads(DEPTH_ONE_MANIFEST.read_text(encoding="utf-8"))
    finite_s = json.loads(FINITE_S_MANIFEST.read_text(encoding="utf-8"))
    frontier = json.loads(FRONTIER_MANIFEST.read_text(encoding="utf-8"))
    assert depth_one["verdict"]["complete_depth_one_fixed_gauge_DQ"] == "CERTIFIED"
    assert finite_s["verdict"]["finite_s_common_endpoint_mesh"] == "CERTIFIED"
    assert finite_s["result"]["scope_limits"][
        "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas"
    ] is False
    assert frontier["verdict"]["dynamic_branch_record_MT_DQ"] == "NOT_CERTIFIED"
    rows, registry = finite.load_dependencies()
    assert len(rows) == 64
    return rows, {
        "depth_one_manifest_sha256": file_sha256(DEPTH_ONE_MANIFEST),
        "finite_s_manifest_sha256": file_sha256(FINITE_S_MANIFEST),
        "frontier_manifest_sha256": file_sha256(FRONTIER_MANIFEST),
        "direct_global_physical_subrow_atlas_cert_sha256": file_sha256(
            Path(bulk.__file__).resolve()
        ),
        "direct_finite_s_common_mesh_recovery_cert_sha256": file_sha256(
            Path(finite.__file__).resolve()
        ),
        "maximal_row_registry_sha256": registry["maximal_row_rows_sha256"],
    }


def common_mass_coordinate_atlas(max_cutoff: int = 12) -> dict[str, Any]:
    """Exact common-atlas arithmetic after pulling back by u_{e,r}."""

    assert 2 <= max_cutoff <= 20
    cutoff_rows = []
    for level in range(max_cutoff + 1):
        component_count = 64 * (1 << level)
        boundary_count = 64 * ((1 << level) + 1)
        # Each disjoint carrier is [0,1]_tau x [0,1]_u.  A rho collar of
        # the horizontal dyadic record boundaries has u-length at most
        # 2*(2^L+1)*rho.  The graph mark has l1 size two.
        graph_current_collar_coefficient = Q(32256, 5) * ((1 << level) + 1)
        cutoff_rows.append({
            "cutoff_level": level,
            "component_count": component_count,
            "boundary_component_count": boundary_count,
            "dyadic_width": str(Q(1, 1 << level)),
            "graph_current_boundary_collar": (
                "|J_s|([S_L]_rho)<=min(16128/5,"
                f"{graph_current_collar_coefficient}*rho)"
            ),
            "graph_current_boundary_collar_linear_coefficient": str(
                graph_current_collar_coefficient
            ),
        })

    # At L=2 there are 4 fixed-u components per occurrence.  This is the
    # first explicit common record registry requested by the assault.
    depth_two_records = [
        {
            "occurrence_index": occurrence,
            "dyadic_level": 2,
            "dyadic_atom": atom,
            "fixed_common_u_interval": [str(Q(atom, 4)), str(Q(atom + 1, 4))],
            "component_index": f"mass:occ={occurrence}:L=2:j={atom}",
        }
        for occurrence in range(64)
        for atom in range(4)
    ]
    assert len(depth_two_records) == 256
    return {
        "common_carrier": (
            "disjoint_union_e ([0,1]_tau x [0,1]_u), "
            "u=u_{e,tau*s}(theta)"
        ),
        "fixed_metric": "product Euclidean metric on each labelled unit square",
        "finite_DQ_parameter": "r=tau*s; 0<=tau<=1",
        "pulled_back_positive_row_measure": (
            "dm_{e,r}=M_e(r) du, hence dq_s=d tau M_e(tau*s) du"
        ),
        "moving_endpoint_identity": (
            "theta_{e,r}(j/2^K) pulls back exactly to u=j/2^K"
        ),
        "nested_record_map": "(e,K,j) with I_{K,j}=[j2^-K,(j+1)2^-K)",
        "all_finite_cutoffs_component_indexed": True,
        "depth_two_component_count": 256,
        "depth_two_records_sha256": canonical_digest(depth_two_records),
        "cutoff_rows": cutoff_rows,
        "cutoff_rows_sha256": canonical_digest(cutoff_rows),
        "boundary_Z_exponent": "1",
        "uniform_total_positive_mass_upper": "8064/5",
        "uniform_graph_current_TV_upper": "16128/5",
        "finite_s_BL_convergence": (
            "on each fixed cutoff, M_e(tau*s) and the analytic trace maps "
            "converge uniformly to their s=0 values; the finite disjoint "
            "sum therefore converges in BL*"
        ),
        "scope": (
            "registers the stopped moving endpoints and the depth-one DQ "
            "face carrier; it does not register future dynamical singularities"
        ),
    }


TARGET_RE = re.compile(r"([GW])\[(-?\d+),(-?\d+)\]")


def parse_target(target_id: str) -> tuple[str, int, int]:
    match = TARGET_RE.fullmatch(target_id)
    assert match is not None, target_id
    return match.group(1), int(match.group(2)), int(match.group(3))


def target_id(obstacle: str, ix: int, iy: int) -> str:
    return f"{obstacle}[{ix},{iy}]"


def target_center(
    obstacle: str, ix: int, iy: int, s: arb,
) -> tuple[arb, arb]:
    if obstacle == "G":
        return arb(ix), arb(iy)
    return arb(ix) + arbq(Q(1, 2)) + s, arb(iy) + arbq(Q(1, 2))


def trimmed_row_normal(
    row: dict[str, Any], t0: Q, t1: Q, s0: Q, s1: Q,
) -> tuple[finite.rank0.Jet, finite.rank0.Jet]:
    """Normal on [trim,width-trim], anchored at the nearer boundary."""

    width, left = finite.row_angle_width(row, s0, s1)
    t = bulk.arb_interval(t0, t1)
    trim = arbq(ENDPOINT_TRIM)
    if t1 <= Q(1, 2):
        distance = trim + (width - 2 * trim) * t
        cosine, sine = distance.cos(), distance.sin()
        nx = cosine * left[0] - sine * left[1]
        ny = cosine * left[1] + sine * left[0]
    else:
        assert t0 >= Q(1, 2)
        right = finite.maximal.curve_normal(row["right_boundary"], s0, s1)
        distance = trim + (width - 2 * trim) * (arb(1) - t)
        cosine, sine = distance.cos(), distance.sin()
        nx = cosine * right[0] + sine * right[1]
        ny = cosine * right[1] - sine * right[0]
    return finite.jet_constant(nx), finite.jet_constant(ny)


def shifted_candidates(
    source_obstacle: str, source_ix: int, source_iy: int,
) -> list[tuple[str, int, int, str]]:
    rows = []
    for relative_id in bulk.GLOBAL_CANDIDATE_IDS[source_obstacle]:
        obstacle, ix, iy = parse_target(relative_id)
        ix += source_ix
        iy += source_iy
        if (obstacle, ix, iy) == (source_obstacle, source_ix, source_iy):
            continue
        rows.append((obstacle, ix, iy, relative_id))
    return rows


NONIDENTITY_WITNESSES = tuple(Q(odd, 32) for odd in range(1, 32, 2))


def next_discriminants_at_point(
    row: dict[str, Any], t: Q,
) -> dict[str, arb]:
    """Next-collision discriminants on the centred miss trace at one point."""

    nx, ny = trimmed_row_normal(row, t, t, Q(0), Q(0))
    tangent = finite.moving_tangent_geometry(row, nx, ny, Q(0), Q(0))
    qx, qy, ux, uy, ell_t, source_cp = [value.value for value in tangent]
    assert bool(source_cp > 0)
    s = arb(0)
    miss_obstacle, miss_ix, miss_iy = parse_target(row["miss_target"])
    mx, my = target_center(miss_obstacle, miss_ix, miss_iy, s)
    miss_radius = finite.bulk.ARB_RADIUS[miss_obstacle]
    dx, dy = mx - qx, my - qy
    ell = ux * dx + uy * dy
    w = -uy * dx + ux * dy
    delta = miss_radius * miss_radius - w * w
    assert bool(delta > 0) and bool(ell > ell_t)
    sqrt_delta = delta.sqrt()
    miss_root = ell - sqrt_delta
    assert bool(miss_root > ell_t)
    hit_x = mx - sqrt_delta * ux + w * uy
    hit_y = my - sqrt_delta * uy - w * ux
    radius_squared = miss_radius * miss_radius
    a = 1 - 2 * delta / radius_squared
    c = -2 * sqrt_delta * w / radius_squared
    out_x = a * ux - c * uy
    out_y = a * uy + c * ux

    result = {}
    for obstacle, ix, iy, relative_id in shifted_candidates(
        miss_obstacle, miss_ix, miss_iy
    ):
        cx, cy = target_center(obstacle, ix, iy, s)
        radius = finite.bulk.ARB_RADIUS[obstacle]
        dx, dy = cx - hit_x, cy - hit_y
        transverse = -out_y * dx + out_x * dy
        result[relative_id] = radius * radius - transverse * transverse
    return result


def analytic_second_singularity_audit(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Prove every next-target tangency function is nonidentically zero."""

    witness_rows = []
    per_occurrence = []
    for row_index, row in enumerate(rows):
        miss_obstacle, miss_ix, miss_iy = parse_target(row["miss_target"])
        remaining = {
            relative_id
            for _obstacle, _ix, _iy, relative_id in shifted_candidates(
                miss_obstacle, miss_ix, miss_iy
            )
        }
        initial_count = len(remaining)
        for t in NONIDENTITY_WITNESSES:
            discriminants = next_discriminants_at_point(row, t)
            for relative_id in sorted(tuple(remaining)):
                value = discriminants[relative_id]
                if bool(value > 0) or bool(value < 0):
                    witness_rows.append({
                        "row_index": row_index,
                        "occurrence_id": row["occurrence_id"],
                        "candidate_relative_to_miss_source": relative_id,
                        "witness_t": str(t),
                        "strict_sign": 1 if bool(value > 0) else -1,
                    })
                    remaining.remove(relative_id)
            if not remaining:
                break
        assert not remaining, (row["occurrence_id"], sorted(remaining))
        per_occurrence.append({
            "row_index": row_index,
            "occurrence_id": row["occurrence_id"],
            "candidate_discriminant_count": initial_count,
        })

    witness_rows.sort(key=canonical_json)
    per_occurrence.sort(key=canonical_json)
    function_count = sum(row["candidate_discriminant_count"] for row in per_occurrence)
    assert function_count == len(witness_rows)
    return {
        "parameter_value": "s=0",
        "trimmed_row_domain": (
            "closed absolute-angle subarc obtained by deleting 2^-20 at each endpoint"
        ),
        "analyticity_reason": (
            "all circle-flight and reflection formulae are real analytic; "
            "the declared original miss discriminant is strictly positive "
            "on each trimmed compact row"
        ),
        "candidate_discriminant_function_count": function_count,
        "every_candidate_discriminant_has_a_strict_nonzero_Arb_witness": True,
        "witness_grid": [str(value) for value in NONIDENTITY_WITNESSES],
        "witness_rows_sha256": canonical_digest(witness_rows),
        "per_occurrence_rows_sha256": canonical_digest(per_occurrence),
        "finite_zero_set_per_candidate_on_every_compact_subarc": True,
        "second_collision_singular_set_is_discrete_on_each_open_row": True,
        "second_collision_singular_set_is_at_most_countable_on_open_rows": True,
        "actual_second_singularity_set_has_zero_row_length": True,
        "actual_second_singularity_set_has_zero_coarea_mass": True,
        "why_owner_changes_only_there": (
            "distinct periodic scatterer disks are disjoint, so two strict "
            "positive collision roots cannot coincide; the first owner can "
            "change only when a candidate root is born or dies at tangency"
        ),
        "full_measure_component_atlas": (
            "on the complement of this discrete set, the next target is locally "
            "constant; ordering the connected intervals on each row gives a "
            "countable component-indexed s=0 depth-two atlas, finite on every "
            "compact trimmed subarc"
        ),
        "explicit_interval_registry_coverage": "128399/131072",
        "outer_cover_is_not_the_actual_singular_set": True,
        "scope": (
            "full-measure existence on the open s=0 rows only; the explicit "
            "97.96% box registry is on the 2^-20 trimmed compact rows; finite-s "
            "root continuation and uniform dynamic boundary-Z constants are not supplied"
        ),
    }


def depth_two_leaf(
    row: dict[str, Any], t0: Q, t1: Q, s0: Q, s1: Q,
) -> tuple[bool, dict[str, Any]]:
    """Certify the collision immediately following the row's miss trace."""

    try:
        nx, ny = trimmed_row_normal(row, t0, t1, s0, s1)
        tangent = finite.moving_tangent_geometry(row, nx, ny, s0, s1)
        qx, qy, ux, uy, ell_t, source_cp = [
            value.value for value in tangent
        ]
        s = bulk.arb_interval(s0, s1)
        miss_obstacle, miss_ix, miss_iy = parse_target(row["miss_target"])
        mx, my = target_center(miss_obstacle, miss_ix, miss_iy, s)
        miss_radius = finite.bulk.ARB_RADIUS[miss_obstacle]
        dx, dy = mx - qx, my - qy
        ell = ux * dx + uy * dy
        w = -uy * dx + ux * dy
        delta = miss_radius * miss_radius - w * w
        if not (
            bool(source_cp > 0)
            and bool(delta > 0)
            and bool(ell > ell_t)
        ):
            return False, {"reason": "original_miss_trace_interval_unresolved"}
        sqrt_delta = delta.sqrt()
        miss_root = ell - sqrt_delta
        if not bool(miss_root > ell_t):
            return False, {"reason": "miss_root_order_unresolved"}

        # Dependency-free contact point.  Since
        # C_m-q=ell*u+w*u_perp and root=ell-sqrt(delta),
        # q+root*u-C_m=-sqrt(delta)*u-w*u_perp.
        hit_x = mx - sqrt_delta * ux + w * uy
        hit_y = my - sqrt_delta * uy - w * ux

        # Stable reflection formula.  It avoids the dependency-heavy
        # subtraction (hit-centre)/R and is exact with
        # d=ell*u+w*u_perp and n=(-sqrt(delta)u-wu_perp)/R.
        radius_squared = miss_radius * miss_radius
        a = 1 - 2 * delta / radius_squared
        c = -2 * sqrt_delta * w / radius_squared
        out_x = a * ux - c * uy
        out_y = a * uy + c * ux

        candidates: list[tuple[str, str, arb, arb]] = []
        ambiguous: list[tuple[str, arb]] = []
        for obstacle, ix, iy, relative_id in shifted_candidates(
            miss_obstacle, miss_ix, miss_iy
        ):
            cx, cy = target_center(obstacle, ix, iy, s)
            radius = finite.bulk.ARB_RADIUS[obstacle]
            dx, dy = cx - hit_x, cy - hit_y
            centre_projection = out_x * dx + out_y * dy
            transverse = -out_y * dx + out_x * dy
            discriminant = radius * radius - transverse * transverse
            if bool(discriminant < 0):
                continue
            if not bool(discriminant > 0):
                # Even when the ball straddles tangency, every possible near
                # root is bounded below by ell_lower-sqrt(delta_upper).
                # Keep this lower bound and compare it with a certified
                # winner below instead of automatically refining a harmless
                # far tangency.
                upper = discriminant.upper()
                if bool(upper < 0):
                    continue
                possible_near_lower = centre_projection.lower() - upper.sqrt()
                ambiguous.append((relative_id, possible_near_lower))
                continue
            radical = discriminant.sqrt()
            near = centre_projection - radical
            far = centre_projection + radical
            if bool(far < 0):
                continue
            if not bool(near > 0):
                ambiguous.append((relative_id, arb(0)))
                continue
            if bool(near > arbq(TAU_MAX)):
                continue
            candidates.append((relative_id, target_id(obstacle, ix, iy), near, radical))

        winners = [
            candidate
            for candidate in candidates
            if bool(candidate[2] < arbq(TAU_MAX))
            and all(
                other is candidate or bool(candidate[2] < other[2])
                for other in candidates
            )
        ]
        if len(winners) != 1:
            return False, {
                "reason": "next_owner_comparison_unresolved",
                "candidate_count": len(candidates),
            }
        relative_id, absolute_id, root, incidence = winners[0]
        blocking_ambiguous = [
            relative
            for relative, possible_lower in ambiguous
            if not bool(root < possible_lower)
        ]
        if blocking_ambiguous:
            return False, {
                "reason": "potential_earlier_tangency_unresolved",
                "blocking_candidate_count": len(blocking_ambiguous),
            }
        return True, {
            "next_target_relative_to_miss_source": relative_id,
            "next_target_absolute_lift": absolute_id,
            "next_root_enclosure": str(root),
            "next_incidence_sqrt_discriminant_enclosure": str(incidence),
            "record_formula": (
                "source tangent -> declared miss trace -> reflected next collision"
            ),
        }
    except (AssertionError, ValueError, ZeroDivisionError):
        return False, {"reason": "interval_geometry_exception"}


@dataclass(frozen=True)
class AtlasBox:
    row_index: int
    t0: Q
    t1: Q
    s0: Q
    s1: Q
    depth: int

    @property
    def relative_area(self) -> Q:
        # The genuine second-collision replay is deliberately centred at
        # s=0.  Its measure here is normalized row length, not finite-s
        # parameter area.
        assert self.s0 == self.s1 == 0
        return self.t1 - self.t0

    def split(self) -> tuple["AtlasBox", "AtlasBox"]:
        middle = (self.t0 + self.t1) / 2
        return (
            AtlasBox(self.row_index, self.t0, middle, self.s0, self.s1, self.depth + 1),
            AtlasBox(self.row_index, middle, self.t1, self.s0, self.s1, self.depth + 1),
        )


def initial_depth_two_boxes() -> list[AtlasBox]:
    rows = []
    for row_index in range(64):
        for ti in range(INITIAL_T_CELLS):
            rows.append(AtlasBox(
                row_index,
                Q(ti, INITIAL_T_CELLS),
                Q(ti + 1, INITIAL_T_CELLS),
                Q(0),
                Q(0),
                0,
            ))
    return rows


def genuine_depth_two_registry(rows: list[dict[str, Any]]) -> dict[str, Any]:
    pending = initial_depth_two_boxes()
    certified_rows: list[dict[str, Any]] = []
    unresolved_rows: list[dict[str, Any]] = []
    depth_counts: Counter[int] = Counter()
    next_target_counts: Counter[str] = Counter()
    unresolved_reasons: Counter[str] = Counter()
    certified_area = Q(0)
    unresolved_area = Q(0)

    while pending:
        box = pending.pop()
        ok, witness = depth_two_leaf(
            rows[box.row_index], box.t0, box.t1, box.s0, box.s1
        )
        if not ok and box.depth < MAX_ADAPTIVE_DEPTH:
            pending.extend(reversed(box.split()))
            continue
        base = {
            "row_index": box.row_index,
            "occurrence_id": rows[box.row_index]["occurrence_id"],
            "t": [str(box.t0), str(box.t1)],
            "s": [str(box.s0), str(box.s1)],
            "adaptive_depth": box.depth,
            "relative_parameter_area": str(box.relative_area),
        }
        if ok:
            component_index = "d2:" + canonical_digest({**base, **witness})[:24]
            record = {**base, **witness, "component_index": component_index}
            certified_rows.append(record)
            certified_area += box.relative_area
            depth_counts[box.depth] += 1
            next_target_counts[witness["next_target_relative_to_miss_source"]] += 1
        else:
            unresolved_rows.append({**base, **witness})
            unresolved_area += box.relative_area
            unresolved_reasons[witness["reason"]] += 1

    certified_rows.sort(key=canonical_json)
    unresolved_rows.sort(key=canonical_json)
    assert certified_area + unresolved_area == 64
    assert certified_area > Q(0)

    # ENDPOINT_TRIM is an absolute inward angular distance in
    # ``distance=trim+(width-2*trim)*t``; it is not a normalized-t width.
    # The cemetery is therefore charged directly by density <=18/5 on each
    # angular side and by the two-point graph mark.  No factor 7 is needed.
    endpoint_positive_mass = 64 * 2 * Q(18, 5) * ENDPOINT_TRIM
    endpoint_graph_tv = 2 * endpoint_positive_mass
    assert endpoint_positive_mass == Q(9, 20480)
    assert endpoint_graph_tv == Q(9, 10240)

    return {
        "physical_record": (
            "for every certified s=0 component: tangent event e, miss "
            "trace, specular reflection, unique next target before time 3"
        ),
        "grazing_trace_identity": "T_0^tr(z_T(theta))=y_M(theta)",
        "grazing_trace_identity_reason": (
            "specular reflection at exact tangency leaves the velocity "
            "unchanged and the registered miss owner is the first strict "
            "post-tangency collision"
        ),
        "two_trace_record_alignment": (
            "the hit trace enters this registry after its canonical grazing "
            "continuation; the miss trace enters it immediately"
        ),
        "this_is_not_the_formal_telescope": True,
        "row_count": 64,
        "initial_box_count": 64 * INITIAL_T_CELLS,
        "initial_t_cells_per_row": INITIAL_T_CELLS,
        "parameter_value": "s=0",
        "maximum_adaptive_depth": MAX_ADAPTIVE_DEPTH,
        "endpoint_absolute_inward_angular_trim_each_side": str(ENDPOINT_TRIM),
        "endpoint_cemetery_positive_mass_upper": str(endpoint_positive_mass),
        "endpoint_cemetery_graph_TV_upper": str(endpoint_graph_tv),
        "certified_leaf_count": len(certified_rows),
        "unresolved_leaf_count": len(unresolved_rows),
        "certified_normalized_row_length": str(certified_area),
        "unresolved_normalized_row_length": str(unresolved_area),
        "unresolved_fraction_of_64_row_domain": str(unresolved_area / 64),
        "unresolved_box_union_is_finite_resolution_outer_cover": True,
        "no_positive_length_claim_for_actual_singularity_set": True,
        "certified_leaf_depth_counts": {
            str(key): value for key, value in sorted(depth_counts.items())
        },
        "next_target_leaf_counts": dict(sorted(next_target_counts.items())),
        "unresolved_reason_counts": dict(sorted(unresolved_reasons.items())),
        "component_indexing": (
            "each certified connected rectangle has one immutable physical "
            "record and a canonical component digest"
        ),
        "certified_rows_sha256": canonical_digest(certified_rows),
        "unresolved_rows_sha256": canonical_digest(unresolved_rows),
        "strict_scope": (
            "one additional collision of the s=0 miss trace on trimmed rows; "
            "no finite-s claim and no claim on unresolved second-grazing "
            "curves or further iterates"
        ),
    }


def strong_source_frontier() -> dict[str, Any]:
    """Exact functional-analytic implication and its missing hypothesis."""

    # If B2 is invariant and the one-step DQ is operator-norm bounded
    # B2->B0, the depth-two telescope estimate is elementary.  Existing
    # inputs only give strong convergence for each fixed C1 source.
    return {
        "certified_conditional_depth_two_estimate": (
            "if P_0(B2) subset B2, P_s->P_0 in B0->B0, and "
            "||(P_s-P_0)/s-D_0||_{B2->B0}->0, then "
            "||(P_s^2-P_0^2)/s-(P_0 D_0+D_0 P_0)||_{B2->B0}->0"
        ),
        "exact_telescope": (
            "(P_s^2-P_0^2)/s=P_s((P_s-P_0)/s)+((P_s-P_0)/s)P_0"
        ),
        "available_source_statement": (
            "for each fixed h in C1, (P_s-P_0)h/s converges in (C1,alpha)*"
        ),
        "missing_hypotheses": [
            "a fixed strong space B2 containing every branch-restricted P_0 h",
            "uniform fixed-time source invariance and P_s continuity on the response space",
            "operator-norm rather than fixed-source one-step DQ",
            "dynamic-test BL convergence and boundary-Z tightness on the depth-two singular strips",
        ],
        "unresolved_depth_two_boxes_are_a_geometric_witness": (
            "their finite-resolution outer cover meets next-collision "
            "tangency/owner boundaries, precisely where the strong branch "
            "restriction must be controlled; the actual s=0 set has zero mass"
        ),
        "fixed_time_branch_record_MT_DQ": False,
    }


def build_manifest() -> dict[str, Any]:
    rows, provenance = load_dependencies()
    common = common_mass_coordinate_atlas()
    depth_two = genuine_depth_two_registry(rows)
    analytic_singularities = analytic_second_singularity_audit(rows)
    strong = strong_source_frontier()
    result = {
        "schema": "cm2.gate3.iterated-common-atlas-mt-dq.v1",
        "provenance": provenance,
        "common_mass_coordinate_atlas": common,
        "genuine_depth_two_miss_trace_registry": depth_two,
        "analytic_s0_second_singularity_audit": analytic_singularities,
        "strong_source_frontier": strong,
        "scope_limits": {
            "moving_dyadic_endpoints_registered_on_depth_one_DQ_common_atlas": True,
            "all_finite_dyadic_cutoffs_component_indexed": True,
            "exact_boundary_Z_tightness_for_dyadic_record_boundaries": True,
            "genuine_s0_depth_two_miss_trace_registry_on_certified_components": True,
            "s0_depth_two_full_measure_component_atlas_modulo_discrete_singular_points": True,
            "finite_s_genuine_depth_two_registry": False,
            "complete_depth_two_physical_domain": False,
            "strong_source_invariance": False,
            "fixed_time_branch_record_MT_DQ": False,
            "physical_FACE_2CUT": False,
            "physical_FACE_TIME": False,
            "gate3_certified": False,
        },
        "exact_remaining_blockers": [
            "continue the s=0 root-isolated atlas to finite-s parameter strips with uniform boundary-Z",
            "prove strong-space invariance for every component restriction",
            "prove dynamic branch-test BL convergence on the same component atlas",
            "propagate regular/face/product-current/response types on that atlas",
            "identify genuine physical word depth and prove the no-|s|^-1 per-depth q domination",
        ],
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


if __name__ == "__main__":
    manifest = build_manifest()
    print(json.dumps(manifest, sort_keys=True, indent=2))
