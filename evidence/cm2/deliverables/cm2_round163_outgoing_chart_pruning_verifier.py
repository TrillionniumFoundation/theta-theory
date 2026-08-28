#!/usr/bin/env python3
"""Independent verifier for the Round163 outgoing-chart certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_gate3_candidate_first_hit_cert as base


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2_round163_outgoing_chart_pruning_certificate.json"
OUTPUT = HERE / "cm2_round163_outgoing_chart_pruning_verification.json"
CERTIFICATE_SCHEMA = "cm2.round163.outgoing-chart-pruning.v1"
SCHEMA = "cm2.round163.outgoing-chart-pruning.verification.v1"
PRODUCER = "cm2_round163_outgoing_chart_pruning.py"
ATLAS_SOURCE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
BASE_SOURCE = "cm2_gate3_candidate_first_hit_cert.py"
PRIOR_CERTIFICATE = (
    "cm2_round162_exterior_unique_owner_pruning_certificate.json"
)
PRIOR_VERIFICATION = (
    "cm2_round162_exterior_unique_owner_pruning_verification.json"
)
FROZEN_OWNER = "W[1,0]"
FROZEN_OUTGOING_CHART = "W"
SOURCE_W_CHARTS = ("W:E", "W:W", "W:N", "W:S")
PINS = {
    PRODUCER:
        "96a3ad9a1e0cf60f9d32d67b662584669b77cbf613ffbd7e08e827f4494c8581",
    ATLAS_SOURCE:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    BASE_SOURCE:
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    PRIOR_CERTIFICATE:
        "9cf6e0a65659a6c835e476d283b48d3fcd3b29f450ca2bf1b71d66dfb695f97f",
    PRIOR_VERIFICATION:
        "c7dda884faa817e5dbafc94756f01023eafe00def62de1676fa830d605e45b79",
}
DEPENDENCY_PINS = {
    key: value for key, value in PINS.items() if key != PRODUCER
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


def strict_load_raw(raw: bytes) -> dict[str, Any]:
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


def strict_load(path: Path) -> dict[str, Any]:
    return strict_load_raw(path.read_bytes())


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


def classify_outgoing(
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
    tests = {
        "E": (normal_x - normal_y, normal_x + normal_y),
        "W": (-normal_x - normal_y, -normal_x + normal_y),
        "N": (normal_y - normal_x, normal_y + normal_x),
        "S": (-normal_y - normal_x, -normal_y + normal_x),
    }
    for cell in ("E", "W", "N", "S"):
        first, second = tests[cell]
        if bool(first > 0) and bool(second > 0):
            return cell, first, second
    return None, normal_x, normal_y


def rebuild_expected() -> dict[str, Any]:
    prior, verification = check_pins()
    direct_e = atlas.build_atlas("W:E")
    direct_n = atlas.build_atlas("W:N")
    atlases = {
        "W:E": direct_e,
        "W:W": [
            atlas.reflect_leaf("W:E", "vertical", leaf)
            for leaf in direct_e
        ],
        "W:N": direct_n,
        "W:S": [
            atlas.reflect_leaf("W:N", "horizontal", leaf)
            for leaf in direct_n
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
            cell, first_margin, second_margin = classify_outgoing(
                chart_id,
                leaf,
            )
            if cell is None:
                disposition = "OUTGOING_CHART_SEAM_UNRESOLVED"
            elif cell == FROZEN_OUTGOING_CHART:
                disposition = "PREFIX_STAGE_ONE_MATCH"
            else:
                disposition = (
                    "EARLIEST_PREFIX_EXCLUDED_OUTGOING_CHART_MISMATCH"
                )
            row = {
                "leaf_key": f"{chart_id}:{leaf.box.path}",
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
    result = {
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
            "remaining_leaf_count":
                prior_combined["remaining_leaf_count"] - newly_excluded,
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
            "dependency_sha256": DEPENDENCY_PINS,
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
    return {
        "schema": CERTIFICATE_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def validate(document: dict[str, Any], expected: dict[str, Any]) -> None:
    require(
        set(document) == {"schema", "result", "result_sha256"}
        and document["schema"] == CERTIFICATE_SCHEMA
        and type(document["result"]) is dict
        and type(document["result_sha256"]) is str
        and document["result_sha256"] == digest(document["result"])
        and canonical(document) == canonical(expected),
        "certificate mismatch",
    )


def mutate(
    document: dict[str, Any],
    path: tuple[Any, ...],
    value: Any,
) -> dict[str, Any]:
    candidate = copy.deepcopy(document)
    cursor: Any = candidate
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    candidate["result_sha256"] = digest(candidate["result"])
    return candidate


def semantic_attacks(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    cases = {
        "promote D02": mutate(
            document, ("result", "strict_nonpromotion", "D02"), "CLOSED"
        ),
        "promote CM2": mutate(
            document,
            ("result", "strict_nonpromotion", "CM2"),
            "GO_FOR_CLAIM",
        ),
        "zero unresolved": mutate(
            document,
            (
                "result", "combined_frozen_prefix_census",
                "frozen_prefix_unresolved_leaves_zero",
            ),
            True,
        ),
        "change mismatch count": mutate(
            document,
            (
                "result", "outgoing_chart_pruning",
                "outgoing_chart_mismatch_excluded_count",
            ),
            41,
        ),
        "change seam count": mutate(
            document,
            (
                "result", "outgoing_chart_pruning",
                "outgoing_chart_seam_unresolved_count",
            ),
            0,
        ),
        "change match count": mutate(
            document,
            (
                "result", "outgoing_chart_pruning",
                "prefix_stage_one_match_count",
            ),
            519,
        ),
        "change row digest": mutate(
            document,
            (
                "result", "outgoing_chart_pruning",
                "all_disposition_rows_sha256",
            ),
            "0" * 64,
        ),
        "change chart": mutate(
            document,
            (
                "result", "outgoing_chart_pruning", "charts", 0,
                "chart_id",
            ),
            "W:W",
        ),
        "remove strict seam policy": mutate(
            document,
            ("result", "scope", "seam_overwrap_is_not_classified"),
            False,
        ),
        "fake all signatures": mutate(
            document,
            ("result", "scope", "not_all_return_signatures"),
            False,
        ),
        "change dependency pin": mutate(
            document,
            (
                "result", "provenance", "dependency_sha256",
                ATLAS_SOURCE,
            ),
            "0" * 64,
        ),
        "extra field": mutate(document, ("result", "extra"), True),
    }
    rejected = 0
    for label, candidate in cases.items():
        try:
            validate(candidate, expected)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError(f"semantic attack accepted:{label}")
    return {
        "attack_count": len(cases),
        "rejected_count": rejected,
        "all_rejected": rejected == len(cases),
    }


def strict_json_attacks() -> dict[str, Any]:
    attacks = [
        b'{"x":1,"x":2}',
        b'{"x":1.0}',
        b'{"x":NaN}',
        b'\xef\xbb\xbf{"x":1}',
        b'{"x":"\\u0000"}',
        b'{"x":"\\ud800"}',
        b'{"x":1}\x00',
    ]
    rejected = 0
    for raw in attacks:
        try:
            strict_load_raw(raw)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError("strict JSON attack accepted")
    return {
        "attack_count": len(attacks),
        "rejected_count": rejected,
        "all_rejected": rejected == len(attacks),
    }


def build() -> dict[str, Any]:
    document = strict_load(CERTIFICATE)
    expected = rebuild_expected()
    validate(document, expected)
    result = {
        "status": "PASS",
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_result_sha256": document["result_sha256"],
        "round163_producer_imported_or_executed": False,
        "all_1176_owner_matching_leaves_reconstructed": True,
        "strict_outgoing_dominant_chart_tests_recomputed": True,
        "all_disposition_digests_recomputed": True,
        "semantic_attack_suite": semantic_attacks(document, expected),
        "strict_json_attack_suite": strict_json_attacks(),
        "strict_nonpromotion_recomputed": True,
    }
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
