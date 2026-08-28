#!/usr/bin/env python3
"""Read-only probe for the Round182 source-G outgoing-W residual faces."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import json
from pathlib import Path
import sys

from flint import arb, ctx

import cm2_round179_source_g_residual_tube_arrangement_verifier as r179
import cm2_round182_source_g_clipped_graph_and_pair_arrangement as r182


HERE = Path(__file__).resolve().parent
ROWS = HERE / (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
)


def unpack(table, columns):
    return [dict(zip(columns, row, strict=True)) for row in table]


def factor_geometry(chart, target_id, box):
    t = (
        r179.r174.first_hit.arb_interval(box.t0, box.t1),
        (arb(1), arb(0), arb(0)),
    )
    p = (
        r179.r174.first_hit.arb_interval(box.p0, box.p1),
        (arb(0), arb(1), arb(0)),
    )
    s = (
        r179.r174.first_hit.arb_interval(box.s0, box.s1),
        (arb(0), arb(0), arb(1)),
    )
    rt_value = r179.r174.atlas.ge.sqrt_one_minus_square(box.t0, box.t1)
    rp_value = r179.r174.atlas.ge.sqrt_one_minus_square(box.p0, box.p1)
    rt = (rt_value, (-t[0] / rt_value, arb(0), arb(0)))
    rp = (
        rp_value,
        (
            arb(0),
            None if not bool(rp_value > 0) else -p[0] / rp_value,
            arb(0),
        ),
    )
    cell = chart.split(":")[1]
    if cell == "E":
        nx, ny = rt, t
    elif cell == "W":
        nx, ny = r179.dneg(rt), t
    elif cell == "N":
        nx, ny = t, rt
    else:
        nx, ny = t, r179.dneg(rt)
    ux = r179.dsub(r179.dmul(rp, nx), r179.dmul(p, ny))
    uy = r179.dadd(r179.dmul(rp, ny), r179.dmul(p, nx))
    source_x = r179.dscale(nx, arb(9) / 25)
    source_y = r179.dscale(ny, arb(9) / 25)
    target = r179.r174.first_hit.target_by_id(target_id)
    if target.obstacle != "W":
        raise RuntimeError("factor geometry requires a W target")
    cx = r179.dadd(r179.dconstant(arb(target.ix) + arb(1) / 2), s)
    cy = r179.dconstant(arb(target.iy) + arb(1) / 2)
    dx = r179.dsub(cx, source_x)
    dy = r179.dsub(cy, source_y)
    transverse = r179.dadd(
        r179.dneg(r179.dmul(uy, dx)), r179.dmul(ux, dy)
    )
    radius_q = r179.r174.first_hit.RADIUS[target.obstacle]
    radius = arb(radius_q.numerator) / radius_q.denominator
    discriminant = r179.dsub(
        r179.dconstant(radius * radius),
        r179.dmul(transverse, transverse),
    )
    if not bool(discriminant[0] > 0):
        raise RuntimeError("strict discriminant")
    radical_value = discriminant[0].sqrt()
    radical = (
        radical_value,
        tuple(
            None if derivative is None
            else derivative / (2 * radical_value)
            for derivative in discriminant[1]
        ),
    )
    out_x = r179.dscale(
        r179.dadd(
            r179.dneg(r179.dmul(radical, ux)),
            r179.dmul(transverse, uy),
        ),
        1 / radius,
    )
    out_y = r179.dscale(
        r179.dsub(
            r179.dneg(r179.dmul(radical, uy)),
            r179.dmul(transverse, ux),
        ),
        1 / radius,
    )
    return {
        "HPLUS": r179.dadd(out_x, out_y),
        "HMINUS": r179.dsub(out_x, out_y),
        "NX": out_x,
        "NY": out_y,
    }


def centered_value(chart, target, box, kind):
    center = (
        (box.t0 + box.t1) / 2,
        (box.p0 + box.p1) / 2,
        (box.s0 + box.s1) / 2,
    )
    point = r179.r174.atlas.AtlasBox(
        center[0], center[0],
        center[1], center[1],
        center[2], center[2],
        box.depth,
        box.path + ".center",
    )
    point_value = factor_geometry(chart, target, point)[kind][0]
    full = factor_geometry(chart, target, box)[kind]
    result = point_value
    for index, (lower, upper, midpoint) in enumerate((
        (box.t0, box.t1, center[0]),
        (box.p0, box.p1, center[1]),
        (box.s0, box.s1, center[2]),
    )):
        derivative = full[1][index]
        if derivative is None:
            return full[0]
        displacement = (
            r179.r174.first_hit.arb_interval(lower, upper)
            - arb(midpoint.numerator) / midpoint.denominator
        )
        result += derivative * displacement
    return result


def face_profile(chart, target, box, upper):
    face = r179.face_box(box, "t", upper)
    factors = factor_geometry(chart, target, face)
    result = {}
    for kind in ("HPLUS", "HMINUS"):
        dual = factors[kind]
        direct_raw = r179.arb_sign(dual[0])
        centered_raw = r179.arb_sign(
            centered_value(chart, target, face, kind)
        )
        direct = (
            direct_raw if direct_raw != "OVERWRAP" else centered_raw
        )
        axes = []
        for axis in ("p", "s"):
            index = "tps".index(axis)
            derivative = dual[1][index]
            derivative_sign = (
                None
                if derivative is None
                else r179.arb_sign(derivative)
            )
            if derivative_sign in (None, "OVERWRAP"):
                continue
            lower_box = r179.face_box(face, axis, False)
            upper_box = r179.face_box(face, axis, True)
            lower_direct = factor_geometry(
                chart, target, lower_box
            )[kind][0]
            upper_direct = factor_geometry(
                chart, target, upper_box
            )[kind][0]
            lower_centered = centered_value(
                chart, target, lower_box, kind
            )
            upper_centered = centered_value(
                chart, target, upper_box, kind
            )
            lower_sign = r179.arb_sign(lower_direct)
            if lower_sign == "OVERWRAP":
                lower_sign = r179.arb_sign(lower_centered)
            upper_sign = r179.arb_sign(upper_direct)
            if upper_sign == "OVERWRAP":
                upper_sign = r179.arb_sign(upper_centered)
            axes.append((
                axis,
                derivative_sign,
                lower_sign,
                upper_sign,
                (
                    "FULL_BASE_UNIQUE_GRAPH"
                    if {
                        lower_sign, upper_sign
                    } == {
                        "STRICT_NEGATIVE", "STRICT_POSITIVE"
                    }
                    else "STRICT_ZERO_ABSENT"
                    if (
                        lower_sign == upper_sign
                        and lower_sign != "OVERWRAP"
                    )
                    else "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT"
                ),
            ))
        result[kind] = (direct, tuple(axes), direct_raw, centered_raw)
    normal_zero_excluded = bool(
        factors["NX"][0] * factors["NX"][0]
        + factors["NY"][0] * factors["NY"][0] > 0
    )
    return result, normal_zero_excluded


def resolution(profile):
    strict = {
        kind: data[0] != "OVERWRAP"
        for kind, data in profile.items()
    }
    if all(strict.values()):
        return "BOTH_FACTORS_STRICT"
    if sum(strict.values()) == 1:
        active = next(kind for kind in strict if not strict[kind])
        classes = {row[-1] for row in profile[active][1]}
        if {
            "FULL_BASE_UNIQUE_GRAPH", "STRICT_ZERO_ABSENT"
        } <= classes:
            raise RuntimeError("conflicting active-factor normal forms")
        if "FULL_BASE_UNIQUE_GRAPH" in classes:
            return "ONE_ACTIVE_FACTOR_FULL_GRAPH"
        if "STRICT_ZERO_ABSENT" in classes:
            return "ONE_ACTIVE_FACTOR_ABSENT"
        if profile[active][1]:
            return "ONE_ACTIVE_FACTOR_STRICT_DERIVATIVE_NO_BRACKET"
        return "ONE_ACTIVE_FACTOR_NO_STRICT_BASE_DERIVATIVE"
    classes = {
        kind: {row[-1] for row in profile[kind][1]}
        for kind in profile
    }
    if any(
        {"FULL_BASE_UNIQUE_GRAPH", "STRICT_ZERO_ABSENT"} <= value
        for value in classes.values()
    ):
        raise RuntimeError("conflicting two-factor normal forms")
    if all("FULL_BASE_UNIQUE_GRAPH" in value for value in classes.values()):
        return "TWO_ACTIVE_FACTOR_GRAPHS"
    if any("FULL_BASE_UNIQUE_GRAPH" in value for value in classes.values()):
        return "TWO_ACTIVE_ONE_FACTOR_GRAPH"
    if all("STRICT_ZERO_ABSENT" in value for value in classes.values()):
        return "TWO_ACTIVE_BOTH_ABSENT"
    if any(value for value in classes.values()):
        return "TWO_ACTIVE_STRICT_DERIVATIVE_NO_COMPLETE_BRACKET"
    return "TWO_ACTIVE_NO_STRICT_BASE_DERIVATIVE"


def combined_face_resolution(collar, box, upper):
    original = r182.face_status(
        {
            "chart": collar["chart"],
            "owner_target": collar["owner_target"],
        },
        "OUTGOING",
        {},
        box,
        upper,
    )
    if original["kind"] != "UNRESOLVED":
        return "ROUND182_" + original["kind"]
    profile, normal_excluded = face_profile(
        collar["chart"], collar["owner_target"], box, upper
    )
    if not normal_excluded:
        raise RuntimeError("target normal zero not excluded")
    return resolution(profile)


def is_resolved(label):
    return (
        label in {
            "ROUND182_STRICT",
            "ROUND182_CURVE",
            "ROUND182_ABSENT",
        }
        or label in {
            "BOTH_FACTORS_STRICT",
            "ONE_ACTIVE_FACTOR_ABSENT",
            "ONE_ACTIVE_FACTOR_FULL_GRAPH",
        }
    )


def adaptive_p_probe(outgoing, collar_by_occurrence, maximum_depth):
    terminal_classes = Counter()
    face_classes = Counter()
    closed_original_leaves = 0
    residual_original_leaves = 0
    closed_volume = Q(0)
    residual_volume = Q(0)
    input_volume = Q(0)
    terminal_count = 0
    for index, row in enumerate(outgoing):
        collar = collar_by_occurrence[row["occurrence_row_id"]]
        initial = r179.r174.atlas.AtlasBox(
            *(Q(value) for value in row["box"]),
            0,
            row["row_id"],
        )
        initial_unresolved = tuple(
            upper
            for status, upper in (
                (row["lower_t_face_status"], False),
                (row["upper_t_face_status"], True),
            )
            if status == "U"
        )
        input_volume += r179.r174.volume(initial)
        queue = [(initial, 0, initial_unresolved)]
        parent_residual = False
        while queue:
            box, depth, unresolved_sides = queue.pop()
            next_unresolved = []
            for upper in unresolved_sides:
                label = combined_face_resolution(collar, box, upper)
                face_classes[label] += 1
                if not is_resolved(label):
                    next_unresolved.append(upper)
            if not next_unresolved:
                terminal_classes[("CLOSED", depth)] += 1
                terminal_count += 1
                closed_volume += r179.r174.volume(box)
            elif depth == maximum_depth:
                terminal_classes[("RESIDUAL", depth)] += 1
                terminal_count += 1
                residual_volume += r179.r174.volume(box)
                parent_residual = True
            else:
                left, right = r179.r174.bisect(box, 1)
                inherited = tuple(next_unresolved)
                queue.append((right, depth + 1, inherited))
                queue.append((left, depth + 1, inherited))
        if parent_residual:
            residual_original_leaves += 1
        else:
            closed_original_leaves += 1
        if index and index % 2000 == 0:
            print(
                f"adaptive-p {index}/{len(outgoing)}",
                file=sys.stderr,
                flush=True,
            )
    if closed_volume + residual_volume != input_volume:
        raise RuntimeError("adaptive exact volume conservation")
    return {
        "maximum_depth": maximum_depth,
        "input_original_leaf_count": len(outgoing),
        "closed_original_leaf_count": closed_original_leaves,
        "residual_original_leaf_count": residual_original_leaves,
        "terminal_count": terminal_count,
        "terminal_classes_by_depth": {
            f"{kind}@{depth}": count
            for (kind, depth), count in sorted(terminal_classes.items())
        },
        "face_resolution_classes": dict(sorted(face_classes.items())),
        "input_volume": str(input_volume),
        "closed_volume": str(closed_volume),
        "residual_volume": str(residual_volume),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--adaptive-p-depth", type=int, default=0)
    args = parser.parse_args()
    if not 0 <= args.adaptive_p_depth <= 8:
        parser.error("--adaptive-p-depth must be between 0 and 8")
    ctx.prec = 256
    wrapper = json.loads(ROWS.read_text())
    source = wrapper["result"]
    schemas = source["row_column_schemas"]
    collars = unpack(
        source["collar_occurrence_rows"],
        schemas["collar_occurrence_rows"],
    )
    collar_by_occurrence = {
        row["Round179_occurrence_row_id"]: row for row in collars
    }
    leaves = unpack(
        source["collar_leaf_rows"],
        schemas["collar_leaf_rows"],
    )
    residual = [
        row for row in leaves
        if Q(row["residual_3d_collar_volume"]) > 0
    ]
    outgoing = [
        row for row in residual
        if collar_by_occurrence[row["occurrence_row_id"]]["kind"]
        == "OUTGOING"
    ]
    if args.adaptive_p_depth:
        print(json.dumps(
            adaptive_p_probe(
                outgoing,
                collar_by_occurrence,
                args.adaptive_p_depth,
            ),
            indent=2,
            sort_keys=True,
        ))
        return
    counts = Counter()
    patterns = Counter()
    axis_profiles = Counter()
    normal_exclusion_failures = 0
    one_split = {
        axis: Counter()
        for axis in ("p", "s")
    }
    for index, row in enumerate(outgoing):
        collar = collar_by_occurrence[row["occurrence_row_id"]]
        box = r179.r174.atlas.AtlasBox(
            *(Q(value) for value in row["box"]),
            0,
            row["row_id"],
        )
        faces = (
            ("LOWER", row["lower_t_face_status"], False),
            ("UPPER", row["upper_t_face_status"], True),
        )
        patterns[faces[0][1] + "|" + faces[1][1]] += 1
        for side, status, upper in faces:
            if status != "U":
                continue
            profile, normal_excluded = face_profile(
                collar["chart"], collar["owner_target"], box, upper
            )
            normal_exclusion_failures += not normal_excluded
            label = resolution(profile)
            counts[(side, label)] += 1
            counts[("ALL", label)] += 1
            axis_profiles[(
                profile["HPLUS"][0],
                tuple(item[-1] for item in profile["HPLUS"][1]),
                profile["HMINUS"][0],
                tuple(item[-1] for item in profile["HMINUS"][1]),
                profile["HPLUS"][2],
                profile["HPLUS"][3],
                profile["HMINUS"][2],
                profile["HMINUS"][3],
            )] += 1
        for axis, axis_index in (("p", 1), ("s", 2)):
            children = r179.r174.bisect(box, axis_index)
            child_labels = []
            for child in children:
                child_labels.append(tuple(
                    (
                        combined_face_resolution(collar, child, upper)
                        if status == "U"
                        else "ROUND182_INHERITED_RESTRICTION"
                    )
                    for _, status, upper in faces
                ))
            residual_children = sum(
                not all(is_resolved(label) for label in labels)
                for labels in child_labels
            )
            one_split[axis][
                "fully_closed_parent"
                if residual_children == 0
                else "residual_parent"
            ] += 1
            one_split[axis]["closed_child"] += 2 - residual_children
            one_split[axis]["residual_child"] += residual_children
        if index and index % 2000 == 0:
            print(
                f"probe {index}/{len(outgoing)}",
                file=sys.stderr,
                flush=True,
            )
    print(json.dumps({
        "outgoing_residual_leaves": len(outgoing),
        "face_status_patterns": {
            key: value for key, value in sorted(patterns.items())
        },
        "factor_resolution": {
            "|".join(key): value for key, value in sorted(counts.items())
        },
        "normal_exclusion_failures": normal_exclusion_failures,
        "axis_profile_count": len(axis_profiles),
        "top_axis_profiles": [
            [list(key), value]
            for key, value in axis_profiles.most_common(40)
        ],
        "one_split_probe": {
            axis: dict(sorted(counts.items()))
            for axis, counts in one_split.items()
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
