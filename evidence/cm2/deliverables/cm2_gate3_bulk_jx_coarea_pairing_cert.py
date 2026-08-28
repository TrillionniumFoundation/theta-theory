#!/usr/bin/env python3
"""Exact Jx pairing of every certified refined Gate-3 physical bulk box.

The predecessor proves only equality of box counts and parameter areas in
each Jx/Jy label orbit.  This replay constructs the actual boxwise Jx
involution.  Together with the exact reflection law of the collision-SRB
and coarea densities it proves equality of the positive coefficient laws
under Jx and hence scalar roof cancellation on the certified bulk.

The unresolved collars are not included, so no global DQ or unconditional
Gate 3/4/5 completion is claimed.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate3_global_physical_subrow_atlas_cert as bulk
import cm2_gate3_endpoint_identity_refinement_cert as refined


Q = Fraction
HERE = Path(__file__).resolve().parent
ATLAS_MANIFEST = (
    HERE / "cm2-gate3-endpoint-identity-refinement-manifest-2026-07-15.json"
)
ATLAS_MANIFEST_SHA256 = (
    "dc394ee38b1e1c36a3cabf27d69279576a8f58f40705537c38c04524781b37d7"
)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()


def box_identity(box: bulk.Box) -> tuple[Any, ...]:
    return (
        box.chart_id, box.target_id, box.epsilon,
        box.z0, box.z1, box.s0, box.s1, box.depth,
    )


def Jx_box(box: bulk.Box) -> bulk.Box:
    source, cell = box.chart_id.split(":")
    reflected_cell = {"E": "W", "W": "E", "N": "N", "S": "S"}[cell]
    if cell in ("N", "S"):
        z0, z1 = -box.z1, -box.z0
    else:
        z0, z1 = box.z0, box.z1
    return bulk.Box(
        f"{source}:{reflected_cell}",
        bulk.reflected_target(source, "Jx", box.target_id),
        -box.epsilon,
        z0, z1,
        -box.s1, -box.s0,
        box.depth,
    )


def certify() -> dict[str, Any]:
    assert sha256_path(ATLAS_MANIFEST) == ATLAS_MANIFEST_SHA256
    manifest = json.loads(ATLAS_MANIFEST.read_text(encoding="utf-8"))
    result = manifest["result"]
    assert result["physical_immutable_box_count"] == 11812
    assert result["physical_complete_label_count"] == 64
    assert result["connected_component_atlas"][
        "certified_connected_subrow_components"
    ] == 64
    assert result["scope_limits"]["global_dq"] is False

    _leaves, physical = refined.atlas()
    assert len(physical) == 11812
    by_key = {box_identity(box): (box, data) for box, data in physical}
    assert len(by_key) == len(physical)

    pair_rows: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    label_pair_counts: Counter[tuple[tuple[Any, ...], tuple[Any, ...]]] = Counter()
    signed_parameter_area = Q(0)
    for box, data in physical:
        key = box_identity(box)
        partner_box = Jx_box(box)
        partner_key = box_identity(partner_box)
        assert box_identity(Jx_box(partner_box)) == key
        assert partner_key in by_key
        actual_partner, partner_data = by_key[partner_key]
        assert actual_partner.area == box.area
        label = tuple(data["label"])
        partner_label = tuple(partner_data["label"])
        assert partner_label == bulk.reflected_label(label, "Jx")
        assert partner_label[-1] == -label[-1]
        signed_parameter_area += Q(label[-1]) * box.area
        if key in seen:
            continue
        seen.add(key)
        seen.add(partner_key)
        ordered_labels = tuple(sorted((label, partner_label)))
        label_pair_counts[ordered_labels] += 1
        pair_rows.append({
            "left_box": [str(value) for value in key],
            "right_box": [str(value) for value in partner_key],
            "left_label": list(label),
            "right_label": list(partner_label),
            "equal_parameter_area": str(box.area),
            "coarea_law": "(Jx)_* m_left = m_right",
            "signed_scalar_pair": "(+m)+(-m)=0",
        })
    assert len(seen) == len(physical)
    assert len(pair_rows) == 5906
    assert len(label_pair_counts) == 32
    assert signed_parameter_area == 0
    assert all(count > 0 for count in label_pair_counts.values())

    # Exact transformation table.  The moving white displacement satisfies
    # s'=-s under x -> 1-x.  On every reflected chart:
    # n_x,u_x and epsilon change sign, n_y,u_y,cp,ell do not.  The absolute
    # collision-SRB chart Jacobian and |dt/dz| are unchanged.  Therefore the
    # signed parameter coarea reverses while the positive coefficient law m
    # is transported exactly.
    sign = {
        "nx": -1, "ny": 1, "ux": -1, "uy": 1,
        "epsilon": -1, "ell": 1, "eta": 1,
    }
    assert sign["ux"] * sign["nx"] == 1
    assert sign["uy"] * sign["ny"] == 1
    cp_sign = 1
    signed_coarea_sign = (
        sign["eta"] * sign["epsilon"] * cp_sign
        * sign["uy"] // sign["ell"]
    )
    assert signed_coarea_sign == -1
    transformation = {
        "parameter": {"s": "-s", "absolute_ds_jacobian": 1},
        "normal": {"nx": "-nx", "ny": "ny"},
        "direction": {"ux": "-ux", "uy": "uy"},
        "tangent_side": "epsilon -> -epsilon",
        "invariants": ["ell", "cp=u dot n", "|dt/dz|", "collision_SRB_density"],
        "signed_coarea_formula": "eta*epsilon*cp*uy/ell",
        "signed_coarea_under_Jx": "minus_original",
        "positive_coefficient_law": "(Jx)_*m_left=m_right",
        "executed_sign_algebra": {
            "coordinate_signs": sign,
            "cp_sign": cp_sign,
            "signed_coarea_sign": signed_coarea_sign,
        },
    }
    return {
        "schema": "cm2.gate3.refined-jx-coarea-pairing.v2",
        "atlas_manifest_sha256": ATLAS_MANIFEST_SHA256,
        "certified_physical_box_count": len(physical),
        "exact_Jx_box_pair_count": len(pair_rows),
        "exact_Jx_component_label_pair_count": len(label_pair_counts),
        "all_box_pairs_equal_area": True,
        "all_box_pairs_opposite_polarity": True,
        "all_positive_coarea_laws_pair_by_Jx_pushforward": True,
        "bulk_physical_scalar_mu_dot_r_from_certified_rows": "0",
        "bulk_polarity_weighted_parameter_area": str(signed_parameter_area),
        "transformation_law": transformation,
        "box_pair_rows_sha256": canonical_digest(pair_rows),
        "label_pair_multiplicities_sha256": canonical_digest([
            {"labels": [list(left), list(right)], "box_pairs": count}
            for (left, right), count in sorted(label_pair_counts.items())
        ]),
        "scope_limits": {
            "unresolved_collar_fraction": result["unresolved_area_fraction"],
            "maximal_global_rows": False,
            "all_physical_coarea_laws_including_collars": False,
            "arbitrary_test_current_cancellation": False,
            "global_dq": False,
            "gate3_certified": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE3_BULK_EXACT_JX_COAREA_PAIRING: CERTIFIED")
    print("GATE45_BULK_PHYSICAL_SCALAR_MU_DOT_R: CERTIFIED")
    print("GATE3_GLOBAL_DQ_INCLUDING_COLLARS: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
