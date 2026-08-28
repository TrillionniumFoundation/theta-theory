#!/usr/bin/env python3
"""Exact horizontal-reflection ledger for all conservative Gate-3 rows.

This is a finite, exact label/affine-geometry certificate.  It proves the
reflection-pairing *schema* and the scalar roof-current cancellation at the
centred parameter.  It deliberately does not claim that the unresolved
Gate-3 collars are physical event rows, nor does it type their DQ currents.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction

import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas


Q = Fraction
CHARTS = ("G:E", "G:W", "G:N", "G:S", "W:E", "W:W", "W:N", "W:S")
CELL_JX = {"E": "W", "W": "E", "N": "N", "S": "S"}


def canonical_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def jx_chart(chart: str) -> str:
    source, cell = chart.split(":")
    return f"{source}:{CELL_JX[cell]}"


def jx_row(row: tuple[str, str]) -> tuple[str, str]:
    chart, target = row
    source, _cell = chart.split(":")
    return jx_chart(chart), atlas.reflected_target(source, "vertical", target)


def source_coordinate_rule(cell: str) -> tuple[str, str]:
    # The first entry is t', the second p', in terms of the old coordinates.
    if cell in {"E", "W"}:
        return "t", "-p"
    return "-t", "-p"


def certify() -> dict[str, object]:
    rows: list[tuple[str, str]] = []
    chart_rows: dict[str, int] = {}
    affine_rows: list[dict[str, object]] = []

    for chart in CHARTS:
        source, cell = chart.split(":")
        candidates = tuple(base.candidate_ids(chart))
        mapped_chart = jx_chart(chart)
        mapped = tuple(atlas.reflected_target(source, "vertical", target) for target in candidates)
        assert len(mapped) == len(set(mapped))
        assert set(mapped) == set(base.candidate_ids(mapped_chart))
        chart_rows[chart] = len(candidates)

        for old, new in zip(candidates, mapped):
            a, b, c, d = atlas.affine_displacement(source, old)
            aa, bb, cc, dd = atlas.affine_displacement(source, new)
            # If s'=-s and Jx(dx,dy)=(-dx,dy), then
            # d'_x(s')=-a+b*s' and d'_y(s')=c-d*s'.
            assert (aa, bb, cc, dd) == (-a, b, c, -d)
            row = (chart, old)
            image = (mapped_chart, new)
            assert jx_row(image) == row
            rows.append(row)
            affine_rows.append(
                {
                    "row": row,
                    "image": image,
                    "old_displacement": [str(a), b, str(c), d],
                    "new_displacement": [str(aa), bb, str(cc), dd],
                    "source_coordinate_rule": source_coordinate_rule(cell),
                }
            )

    row_set = set(rows)
    assert len(row_set) == 448
    assert all(jx_row(row) in row_set and jx_row(jx_row(row)) == row for row in row_set)

    fixed = sorted(row for row in row_set if jx_row(row) == row)
    seen: set[tuple[str, str]] = set()
    two_orbits: list[list[tuple[str, str]]] = []
    for row in sorted(row_set):
        if row in seen:
            continue
        image = jx_row(row)
        seen.add(row)
        seen.add(image)
        if image != row:
            two_orbits.append(sorted((row, image)))

    assert len(fixed) == 12
    assert len(two_orbits) == 218
    assert 12 + 2 * 218 == 448

    # Exact calculus layer.  For every event function chosen compatibly with
    # the conjugacy T_s Jx = Jx T_{-s},
    #     H_{Jx(e),s}(Jx z) = H_{e,-s}(z).
    # Hence d_s H changes sign at zero, while the absolute coarea Jacobian and
    # collision flux are preserved.  Two-cycles cancel in pairs.  On the 12
    # fixed labels the coordinate involution (t,p)->(-t,-p) pairs the row with
    # itself; the signed density is anti-invariant and its scalar integral is
    # zero.  This proves only the scalar test-1 identity.
    result = {
        "model": "cm2-centered-two-disk-standard-N",
        "parameter_conjugacy": "Jx T_s = T_{-s} Jx",
        "candidate_row_count": len(row_set),
        "two_row_orbit_count": len(two_orbits),
        "fixed_label_orbit_count": len(fixed),
        "chart_row_counts": chart_rows,
        "fixed_rows": fixed,
        "row_involution_digest": canonical_digest(
            [{"row": row, "image": jx_row(row)} for row in sorted(row_set)]
        ),
        "affine_conjugacy_digest": canonical_digest(affine_rows),
        "global_scalar_roof_mass_cancellation": True,
        "immutable_physical_event_registry": False,
        "eventwise_dq_typing": False,
        "global_single_charge_recovery": False,
        "four_term_kac_typing": False,
        "phase_cm2_norm_lifts": False,
        "gate4_certified": False,
        "gate5_certified": False,
    }
    return result


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GLOBAL_JX_ROW_INVOLUTION: CERTIFIED")
    print("GLOBAL_SCALAR_ROOF_MASS_CANCELLATION: CERTIFIED")
    print("IMMUTABLE_PHYSICAL_EVENT_REGISTRY: NOT_CERTIFIED")
    print("EVENTWISE_DQ_AND_SINGLE_CHARGE_RECOVERY: NOT_CERTIFIED")
    print("FOUR_TERM_KAC_AND_PHASE_CM2_NORMS: NOT_CERTIFIED")
    print("GATE_4: NOT_CERTIFIED")
    print("GATE_5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
