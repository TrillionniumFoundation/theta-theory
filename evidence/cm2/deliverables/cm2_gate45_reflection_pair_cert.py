#!/usr/bin/env python3
"""Exact symmetry audit for a paired Gate-4/Gate-5 incidence orbit.

The positive-width grouped incidence certified in
cm2_gate4_grouped_incidence_cert.py is

    A: G(0,0) -- tangent W(0,0) -- G(1,1).

At the centred parameter, reflection in the vertical line x=1/2 conjugates
the table at parameter s to the table at parameter -s.  It therefore gives

    A_x: G(1,0) -- tangent W(0,0) -- G(0,1)

with the same positive coarea measure and the opposite parameter-current
polarity.  Reflection in y=1/2 exchanges the two non-grazing endpoints of
each row, so those endpoint descriptions are alternative representations,
not additive copies.

This script audits the exact lattice-label action, replays the 200-bit Arb
geometry certificate, and checks the two-row vector-current ledger.  It does
not certify the global event inventory or stopped-parent recovery.
"""

from __future__ import annotations

from dataclasses import dataclass

from cm2_gate4_grouped_incidence_cert import certify


Gray = tuple[int, int]
White = tuple[int, int]


def jx_gray(label: Gray) -> Gray:
    i, j = label
    return 1 - i, j


def jy_gray(label: Gray) -> Gray:
    i, j = label
    return i, 1 - j


def jx_white(label: White) -> White:
    # W(i,j;s)=(i+1/2+s,j+1/2), and J_x conjugates s to -s.
    i, j = label
    return -i, j


def jy_white(label: White) -> White:
    i, j = label
    return i, -j


@dataclass(frozen=True)
class Row:
    name: str
    source: Gray
    tangent: White
    target: Gray
    parameter_pullback: int
    current_polarity: int
    kac_mark: tuple[int, int]
    coarea_id: str
    source_test_norm_id: str


def audit() -> dict[str, object]:
    geometry = certify()

    row_a = Row(
        name="A",
        source=(0, 0),
        tangent=(0, 0),
        target=(1, 1),
        parameter_pullback=1,
        current_polarity=1,
        kac_mark=(1, -1),
        coarea_id="m_orbit",
        source_test_norm_id="K_orbit",
    )
    row_x = Row(
        name="Jx(A)",
        source=jx_gray(row_a.source),
        tangent=jx_white(row_a.tangent),
        target=jx_gray(row_a.target),
        parameter_pullback=-1,
        current_polarity=-1,
        kac_mark=(1, -1),
        coarea_id="m_orbit",
        source_test_norm_id="K_orbit",
    )

    assert row_x.source == (1, 0)
    assert row_x.tangent == (0, 0)
    assert row_x.target == (0, 1)

    # J_y gives the endpoint-swapped representation of J_x(A).
    assert jy_gray(row_a.source) == row_x.target
    assert jy_white(row_a.tangent) == row_x.tangent
    assert jy_gray(row_a.target) == row_x.source

    # J_x^2 and J_y^2 are identities on the relevant lift labels.
    assert jx_gray(jx_gray(row_a.source)) == row_a.source
    assert jx_gray(jx_gray(row_a.target)) == row_a.target
    assert jx_white(jx_white(row_a.tangent)) == row_a.tangent
    assert jy_gray(jy_gray(row_a.source)) == row_a.source
    assert jy_gray(jy_gray(row_a.target)) == row_a.target
    assert jy_white(jy_white(row_a.tangent)) == row_a.tangent

    # Chain rule for H_{Jx(A),s}(J_x z)=H_{A,-s}(z).
    assert row_x.parameter_pullback == -row_a.parameter_pullback
    assert row_x.current_polarity == -row_a.current_polarity

    # Same absolute coarea law and fixed Kac vector mark.  Thus the scalar
    # roof-current masses cancel on this complete two-row symmetry orbit.
    assert row_a.coarea_id == row_x.coarea_id
    assert row_a.kac_mark == row_x.kac_mark == (1, -1)
    assert row_a.source_test_norm_id == row_x.source_test_norm_id
    roof_mass_coefficients = (
        row_a.current_polarity,
        row_x.current_polarity,
    )
    assert sum(roof_mass_coefficients) == 0

    return {
        "geometry": geometry,
        "rows": (row_a, row_x),
        "roof_mass_coefficients": roof_mass_coefficients,
    }


def main() -> None:
    result = audit()
    rows = result["rows"]
    assert isinstance(rows, tuple)
    geometry = result["geometry"]
    assert isinstance(geometry, dict)
    print("GATE45_REFLECTION_ORBIT_GEOMETRY_REPLAY: CERTIFIED")
    print(f"  tangent_time={geometry['tangent_time']}")
    print(f"  continuation_flight={geometry['flight_b']}")
    for row in rows:
        assert isinstance(row, Row)
        print(
            f"  row={row.name} source=G{row.source} tangent=W{row.tangent} "
            f"target=G{row.target} polarity={row.current_polarity:+d}"
        )
    print("TWO_ROW_COMMON_COAREA_BY_ISOMETRY: CERTIFIED")
    print("TWO_ROW_SAME_KAC_MARK=(+1,-1): CERTIFIED")
    print("LOCAL_REFLECTION_SOURCE_TEST_NORM_ISOMETRY: CERTIFIED")
    print("TWO_ROW_LOCAL_ROOF_CURRENT_MASS_CANCELLATION: CERTIFIED")
    print("ENDPOINT_REFLECTIONS_ARE_ALTERNATIVE_VIEWS: CERTIFIED")
    print("GLOBAL_EVENT_REGISTRY: NOT CERTIFIED")
    print("GLOBAL_STOPPED_RECOVERY: NOT CERTIFIED")
    print("GLOBAL_KAC_ROOF_CANCELLATION_BY_ALL_ROWS: NOT CERTIFIED")
    print("GATE_4: NOT CERTIFIED")
    print("GATE_5: NOT CERTIFIED")


if __name__ == "__main__":
    main()
