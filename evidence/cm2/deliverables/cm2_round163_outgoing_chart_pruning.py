#!/usr/bin/env python3
"""Round163: resolve outgoing dominant charts on owner-matching leaves."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_gate3_candidate_first_hit_cert as base


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round163_outgoing_chart_pruning_certificate.json"
SCHEMA = "cm2.round163.outgoing-chart-pruning.v1"
FROZEN_OWNER = "W[1,0]"
FROZEN_OUTGOING_CHART = "W"
SOURCE_W_CHARTS = ("W:E", "W:W", "W:N", "W:S")
ATLAS_SOURCE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
BASE_SOURCE = "cm2_gate3_candidate_first_hit_cert.py"
PRIOR_CERTIFICATE = (
    "cm2_round162_exterior_unique_owner_pruning_certificate.json"
)
PRIOR_VERIFICATION = (
    "cm2_round162_exterior_unique_owner_pruning_verification.json"
)
PINS = {
    ATLAS_SOURCE:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    BASE_SOURCE:
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    PRIOR_CERTIFICATE:
        "9cf6e0a65659a6c835e476d283b48d3fcd3b29f450ca2bf1b71d66dfb695f97f",
    PRIOR_VERIFICATION:
        "c7dda884faa817e5dbafc94756f01023eafe00def62de1676fa830d605e45b79",
}
PRIOR_RESULT_SHA256 = (
    "744ca0ca17bcb51077d154d1a3bb6b8055918acae519ad9c640b12bae54e2ea7"
)
PRIOR_VERIFICATION_RESULT_SHA256 = (
    "c649ab13186bf1ce261b63a0576a2e5d79debf67cdd71f24d5786ea57d1605f0"
)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_load(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "encoding",
    )

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, "duplicate key")
            result[key] = value
        return result

    value = json.loads(
        raw.decode(),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )

    def strings(item: Any) -> None:
        if type(item) is str:
            require(
                "\x00" not in item
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in item
                ),
                "decoded string encoding",
            )
        elif type(item) is list:
            for child in item:
                strings(child)
        elif type(item) is dict:
            for key, child in item.items():
                strings(key)
                strings(child)

    strings(value)
    require(type(value) is dict, "top object")
    return value


def check_pins() -> tuple[dict[str, Any], dict[str, Any]]:
    require(
        Path(atlas.__file__).resolve() == (HERE / ATLAS_SOURCE).resolve(),
        "atlas module identity",
    )
    require(
        Path(base.__file__).resolve() == (HERE / BASE_SOURCE).resolve(),
        "base module identity",
    )
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            == expected,
            f"pin:{name}",
        )
    prior = strict_load(HERE / PRIOR_CERTIFICATE)
    verification = strict_load(HERE / PRIOR_VERIFICATION)
    require(
        prior["result_sha256"] == PRIOR_RESULT_SHA256
        and verification["result_sha256"]
        == PRIOR_VERIFICATION_RESULT_SHA256
        and verification["result"]["status"] == "PASS"
        and verification["result"]["certificate_result_sha256"]
        == prior["result_sha256"],
        "prior chain",
    )
    return prior, verification


def outgoing_chart(
    chart_id: str,
    leaf: atlas.Leaf,
) -> tuple[str | None, Any, Any]:
    record = atlas.root_record(chart_id, leaf.box, FROZEN_OWNER)
    require(
        record.classification == "strict_future_root"
        and record.near is not None,
        "owner root classification",
    )
    qx, qy, ux, uy, s, _radical_p = atlas.geometry(
        chart_id,
        leaf.box,
    )
    target = base.target_by_id(FROZEN_OWNER)
    center_x, center_y = base.target_center(target, s)
    radius = base.arbq(base.RADIUS[target.obstacle])
    normal_x = (qx + record.near * ux - center_x) / radius
    normal_y = (qy + record.near * uy - center_y) / radius
    candidates = {
        "E": (normal_x - normal_y, normal_x + normal_y),
        "W": (-normal_x - normal_y, -normal_x + normal_y),
        "N": (normal_y - normal_x, normal_y + normal_x),
        "S": (-normal_y - normal_x, -normal_y + normal_x),
    }
    for cell in ("E", "W", "N", "S"):
        first, second = candidates[cell]
        if bool(first > 0) and bool(second > 0):
            return cell, first, second
    return None, normal_x, normal_y


def leaf_key(chart_id: str, leaf: atlas.Leaf) -> str:
    return f"{chart_id}:{leaf.box.path}"


def build_result() -> dict[str, Any]:
    prior, verification = check_pins()
    direct = {
        "W:E": atlas.build_atlas("W:E"),
        "W:N": atlas.build_atlas("W:N"),
    }
    atlases = {
        **direct,
        "W:W": [
            atlas.reflect_leaf("W:E", "vertical", leaf)
            for leaf in direct["W:E"]
        ],
        "W:S": [
            atlas.reflect_leaf("W:N", "horizontal", leaf)
            for leaf in direct["W:N"]
        ],
    }
    prior_charts = {
        row["chart_id"]: row
        for row in prior["result"]["unique_first_owner_pruning"]["charts"]
    }
    chart_rows: list[dict[str, Any]] = []
    all_rows: list[dict[str, Any]] = []
    mismatch_total = 0
    match_total = 0
    unresolved_total = 0
    for chart_id in SOURCE_W_CHARTS:
        leaves = [
            leaf for leaf in atlases[chart_id]
            if leaf.classification == "unique_first"
            and leaf.owner_target == FROZEN_OWNER
        ]
        require(
            len(leaves)
            == prior_charts[chart_id][
                "owner_match_outgoing_chart_unresolved_count"
            ],
            f"prior owner-match count:{chart_id}",
        )
        rows: list[dict[str, Any]] = []
        for leaf in sorted(leaves, key=lambda item: item.box.path):
            cell, first_margin, second_margin = outgoing_chart(
                chart_id,
                leaf,
            )
            disposition = (
                "EARLIEST_PREFIX_EXCLUDED_OUTGOING_CHART_MISMATCH"
                if cell is not None and cell != FROZEN_OUTGOING_CHART
                else (
                    "PREFIX_STAGE_ONE_MATCH"
                    if cell == FROZEN_OUTGOING_CHART
                    else "OUTGOING_CHART_SEAM_UNRESOLVED"
                )
            )
            row = {
                "leaf_key": leaf_key(chart_id, leaf),
                "owner": FROZEN_OWNER,
                "outgoing_chart": cell,
                "disposition": disposition,
                "strict_margin_one_arb": str(first_margin),
                "strict_margin_two_arb": str(second_margin),
            }
            rows.append(row)
            all_rows.append(row)
        mismatch = sum(
            row["disposition"]
            == "EARLIEST_PREFIX_EXCLUDED_OUTGOING_CHART_MISMATCH"
            for row in rows
        )
        match = sum(
            row["disposition"] == "PREFIX_STAGE_ONE_MATCH"
            for row in rows
        )
        unresolved = len(rows) - mismatch - match
        mismatch_total += mismatch
        match_total += match
        unresolved_total += unresolved
        chart_rows.append({
            "chart_id": chart_id,
            "owner_match_leaf_count": len(rows),
            "outgoing_chart_mismatch_excluded_count": mismatch,
            "prefix_stage_one_match_count": match,
            "outgoing_chart_seam_unresolved_count": unresolved,
            "disposition_rows_sha256": digest(rows),
        })
    require(len(all_rows) == 1176, "owner-match total")
    prior_combined = prior["result"]["combined_frozen_prefix_census"]
    newly_excluded = mismatch_total
    remaining = prior_combined["remaining_leaf_count"] - newly_excluded
    return {
        "status": (
            "CERTIFIED_FROZEN_PREFIX_OUTGOING_CHART_PRUNING__"
            "EXTERIOR_AND_D02_STILL_BLOCKED"
        ),
        "frozen_prefix": {
            "collision_index": 1,
            "required_owner": FROZEN_OWNER,
            "required_outgoing_chart": FROZEN_OUTGOING_CHART,
        },
        "outgoing_chart_pruning": {
            "owner_match_input_count": len(all_rows),
            "outgoing_chart_mismatch_excluded_count": mismatch_total,
            "prefix_stage_one_match_count": match_total,
            "outgoing_chart_seam_unresolved_count": unresolved_total,
            "all_disposition_rows_sha256": digest(all_rows),
            "charts": chart_rows,
        },
        "combined_frozen_prefix_census": {
            "prior_recordwise_excluded_leaf_count":
                prior_combined["combined_recordwise_excluded_leaf_count"],
            "new_outgoing_chart_mismatch_excluded_count": newly_excluded,
            "combined_recordwise_excluded_leaf_count":
                prior_combined["combined_recordwise_excluded_leaf_count"]
                + newly_excluded,
            "remaining_leaf_count": remaining,
            "remaining_prefix_stage_one_match": match_total,
            "remaining_outgoing_chart_seam_unresolved": unresolved_total,
            "remaining_tangency_graph":
                prior_combined["remaining_tangency_graph"],
            "remaining_multi_candidate":
                prior_combined["remaining_multi_candidate"],
            "frozen_prefix_unresolved_leaves_zero": False,
        },
        "scope": {
            "record_identity": "chart_id plus leaf path",
            "dominant_chart_test_is_strict_on_each_closed_leaf": True,
            "seam_overwrap_is_not_classified": True,
            "not_full_exterior_sheet_exhaustion": True,
            "not_all_return_signatures": True,
            "not_D02_closure": True,
        },
        "provenance": {
            "dependency_sha256": PINS,
            "prior_certificate_result_sha256": prior["result_sha256"],
            "prior_verification_result_sha256":
                verification["result_sha256"],
            "source_W_atlas_replayed_at_192_bits": True,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "subdivide any outgoing-chart seam leaves, type the 32 "
            "outside-W:W tangency strata, and resolve the 38,180 "
            "outside-W:W multi-candidate leaves"
        ),
    }


def build() -> dict[str, Any]:
    result = build_result()
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    document = build()
    arguments.output.write_text(
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    print(document["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
