#!/usr/bin/env python3
"""Independent high-precision verifier for the Round-88 Gate-3 collars."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_round85_gate3_s0_two_sided_material_window_cert as round85
import cm2_round88_gate3_finite_root_collar_extension_cert as cert


HERE = Path(__file__).resolve().parent
INPUT = HERE / "cm2-round88-gate3-finite-root-collar-extension-2026-07-22.json"


def strict_load(path: Path) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate key: {key}")
            result[key] = value
        return result
    value = json.loads(
        path.read_text(), object_pairs_hook=unique,
        parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if not isinstance(value, dict):
        raise ValueError("top-level object")
    return value


def aq(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def interval(values: list[str]) -> arb:
    lo, hi = map(Q, values)
    return arb(Q(lo + hi, 2).numerator) / Q(lo + hi, 2).denominator + arb(0, Q(hi - lo, 2))


def chart_coordinates(cell: str, nx: arb, ny: arb) -> tuple[arb, list[bool], list[bool]]:
    ax, ay = abs(nx), abs(ny)
    if cell == "E":
        return ny, [bool(nx > 0), bool(ax > ay)], [bool(nx < 0), bool(ax < ay)]
    if cell == "W":
        return ny, [bool(nx < 0), bool(ax > ay)], [bool(nx > 0), bool(ax < ay)]
    if cell == "N":
        return nx, [bool(ny > 0), bool(ay > ax)], [bool(ny < 0), bool(ay < ax)]
    if cell == "S":
        return nx, [bool(ny < 0), bool(ay > ax)], [bool(ny > 0), bool(ay < ax)]
    raise ValueError(cell)


def independent_physics(row: dict[str, Any], cores: tuple[Any, ...]) -> dict[str, Any]:
    source = cores[row["source_core_index"]]
    t0, t1 = map(Q, row["collar"]["t"])
    p0, p1 = map(Q, row["collar"]["p"])
    s0, s1 = map(Q, row["collar"]["s"])
    margins = [t0 - source.t0, source.t1 - t1, p0 - source.p0, source.p1 - p1]
    if min(margins) <= 0 or (s0, s1) != (-cert.S_RADIUS, cert.S_RADIUS):
        raise ValueError("source containment")
    phase_box = first_hit.PhaseBox(source.chart_id, t0, t1, p0, p1, s0, s1)
    qx, qy, ux, uy, s = first_hit.phase_geometry(phase_box)
    target = first_hit.target_by_id(source.target_id)
    ax, ay = first_hit.target_center(target, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = aq(first_hit.RADIUS[target.obstacle])
    discriminant = radius * radius - transverse * transverse
    if not bool(discriminant > 0):
        raise ValueError("radicand")
    radical = discriminant.sqrt()
    near = ell - radical
    if not bool(near > 0) or not bool(near < aq(first_hit.TAU_MAX)):
        raise ValueError("flight order")
    nx = (-radical * ux + transverse * uy) / radius
    ny = (-radical * uy - transverse * ux) / radius
    p_target = transverse / radius

    inside: list[str] = []
    unresolved: list[str] = []
    for destination in cores:
        if destination.source != target.obstacle:
            continue
        t_target, chart_inside, chart_outside = chart_coordinates(
            destination.chart_id.split(":")[1], nx, ny
        )
        bounds_inside = [
            bool(t_target > aq(destination.t0)), bool(t_target < aq(destination.t1)),
            bool(p_target > aq(destination.p0)), bool(p_target < aq(destination.p1)),
        ]
        identifier = "core:" + core_cert.canonical_digest({
            "chart_id": destination.chart_id,
            "t": [str(destination.t0), str(destination.t1)],
            "p": [str(destination.p0), str(destination.p1)],
            "target_id": destination.target_id,
            "crossings": list(destination.crossings),
        })
        if all(chart_inside + bounds_inside):
            inside.append(identifier)
            continue
        separated = any(chart_outside + [
            bool(t_target < aq(destination.t0)), bool(t_target > aq(destination.t1)),
            bool(p_target < aq(destination.p0)), bool(p_target > aq(destination.p1)),
        ])
        if not separated:
            unresolved.append(identifier)
    if unresolved or inside != [row["destination_core_id"]]:
        raise ValueError("destination classification")
    return {
        "minimum_source_margin": min(margins),
        "discriminant": str(discriminant),
        "flight_time": str(near),
        "normal_x": str(nx),
        "normal_y": str(ny),
        "p_target": str(p_target),
    }


def independent_recompute(value: dict[str, Any]) -> dict[str, Any]:
    ctx.prec = 768
    cores = core_cert.physical_cores()
    old85 = round85.strict_load(cert.ROUND85)
    full = round85.strict_load(round85.FULL_CORE)
    all_rows: list[dict[str, Any]] = []
    round85.collect(full, all_rows)
    by_id = {row["atom_id"]: row for row in all_rows}
    positive_ids = {x["positive_atom_id"] for x in old85["result"]["evidence"]["unmatched_rows"]}
    negative_ids = {x["negative_atom_id"] for x in old85["result"]["evidence"]["negative_unmatched_rows"]}
    rows = value["result"]["evidence"]["collar_rows"]
    if {x["unmatched_atom_id"] for x in rows if x["side"] == "POSITIVE_OWNER"} != positive_ids:
        raise ValueError("positive coverage")
    if {x["unmatched_atom_id"] for x in rows if x["side"] == "NEGATIVE_SIDE"} != negative_ids:
        raise ValueError("negative coverage")

    physical = []
    for item in rows:
        source_row = by_id[item["unmatched_atom_id"]]
        opposite_row = by_id[item["selected_opposite_atom_id"]]
        if round85.edge(source_row) != round85.edge(opposite_row):
            raise ValueError("branch key")
        relation, dt, dp = round85.relation(source_row, opposite_row)
        if relation != item["contact_relation"]:
            raise ValueError("contact relation")
        t0, t1 = map(Q, item["collar"]["t"])
        p0, p1 = map(Q, item["collar"]["p"])
        if t1 - t0 != 2 * cert.TP_RADIUS or p1 - p0 != 2 * cert.TP_RADIUS:
            raise ValueError("collar radius")
        for contact in (source_row, opposite_row):
            box = round85.box(contact)
            if min(min(t1, box[1]) - max(t0, box[0]), min(p1, box[3]) - max(p0, box[2])) <= 0:
                raise ValueError("positive area incidence")
        physical.append(independent_physics(item, cores))

    indices = sorted({item["source_core_index"] for item in rows})
    owner_rows = [core_cert.certify_core(cores[index]) for index in indices]
    if not all(row["strict_first_hit"] for row in owner_rows):
        raise ValueError("independent owner replay")
    unique = {
        cert.canonical({
            "source": item["source_core_id"],
            "destination": item["destination_core_id"],
            "collar": item["collar"],
        }) for item in rows
    }
    return {
        "precision_bits": 768,
        "collar_rows": len(rows),
        "unique_collars": len(unique),
        "positive_owner_rows_closed": len(positive_ids),
        "negative_side_rows_closed": len(negative_ids),
        "contact_histogram": dict(sorted(Counter(x["contact_relation"] for x in rows).items())),
        "minimum_source_margin": str(min(x["minimum_source_margin"] for x in physical)),
        "parent_owner_core_count": len(owner_rows),
        "all_radicand_flight_destination_tests_strict": True,
    }


def validate(value: dict[str, Any], expected: dict[str, Any]) -> None:
    if set(value) != {"schema", "pins", "result", "result_sha256"}:
        raise ValueError("closed top-level schema")
    if value["schema"] != cert.SCHEMA or value["pins"] != cert.PINS:
        raise ValueError("schema or pins")
    if value["result_sha256"] != cert.digest(value["result"]):
        raise ValueError("result digest")
    if value["result"]["evidence_sha256"] != cert.digest(value["result"]["evidence"]):
        raise ValueError("evidence digest")
    if value != expected:
        raise ValueError("fresh producer reconstruction")


def rejected(value: dict[str, Any], expected: dict[str, Any]) -> bool:
    try:
        validate(value, expected)
    except (ValueError, KeyError, TypeError, IndexError):
        return True
    return False


def main(argv: list[str]) -> int:
    path = Path(argv[1]).resolve() if len(argv) > 1 else INPUT
    value = strict_load(path)
    expected = cert.build()
    validate(value, expected)
    independent = independent_recompute(value)
    required = {
        "precision_bits": 768,
        "collar_rows": 48,
        "unique_collars": 40,
        "positive_owner_rows_closed": 24,
        "negative_side_rows_closed": 24,
        "contact_histogram": {"CORNER_CONTACT_ONLY": 8, "EDGE_CONTACT_ONLY": 40},
        "minimum_source_margin": "7/102400",
        "parent_owner_core_count": 16,
        "all_radicand_flight_destination_tests_strict": True,
    }
    if independent != required:
        raise ValueError("independent frontier")

    mutations = (
        lambda x: x["result"].__setitem__("Gate3", "CERTIFIED"),
        lambda x: x["result"].__setitem__("finite_root_local_two_sided_material_windows", "175/176"),
        lambda x: x["result"]["evidence"].__setitem__("unique_physical_collar_count", 39),
        lambda x: x["result"]["evidence"]["collar_rows"][0]["collar"].__setitem__("t", ["0", "1"]),
        lambda x: x["result"]["evidence"]["collar_rows"][0].__setitem__("destination_core_id", "forged"),
        lambda x: x["result"]["strict_nonclaims"].clear(),
        lambda x: x.__setitem__("extra_claim", "CERTIFIED"),
    )
    attacks = []
    for mutation in mutations:
        hostile = copy.deepcopy(value)
        mutation(hostile)
        hostile["result"]["evidence_sha256"] = cert.digest(hostile["result"]["evidence"])
        hostile["result_sha256"] = cert.digest(hostile["result"])
        attacks.append(rejected(hostile, expected))
    pin_attacks = []
    for key in value["pins"]:
        hostile = copy.deepcopy(value)
        hostile["pins"][key] = "0" * 64
        hostile["result_sha256"] = cert.digest(hostile["result"])
        pin_attacks.append(rejected(hostile, expected))
    if not all(attacks) or not all(pin_attacks):
        raise ValueError("hostile mutation accepted")

    strict_rejected = 0
    for raw in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '{"x":1e9999}'):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            handle.write(raw)
            temporary = Path(handle.name)
        try:
            strict_load(temporary)
        except ValueError:
            strict_rejected += 1
        finally:
            temporary.unlink(missing_ok=True)
    if strict_rejected != 4:
        raise ValueError("strict JSON suite")

    result = {
        "independent_768_bit_recomputation": independent,
        "fresh_producer_reconstruction": "EXACT_EQUALITY_VERIFIED",
        "hostile_mutations_rejected": f"{sum(attacks)}/{len(attacks)}",
        "coordinated_pin_mutations_rejected": f"{sum(pin_attacks)}/{len(pin_attacks)}",
        "strict_json_attacks_rejected": f"{strict_rejected}/4",
        "verdict": "PASS",
    }
    audit = {
        "schema": "cm2.round88.gate3-finite-root-collar-extension-audit.v1",
        "result": result,
        "result_sha256": cert.digest(result),
    }
    json.dump(audit, sys.stdout, sort_keys=True, indent=2, allow_nan=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
