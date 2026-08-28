#!/usr/bin/env python3
"""Fail-closed verifier for Round162 unique-owner prefix pruning.

The verifier never imports or executes the Round162 producer.  It replays
the pinned upstream 192-bit Gate3 atlas, reconstructs every unique-owner
disposition digest, and compares the entire certificate result.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas


HERE = Path(__file__).resolve().parent
CERTIFICATE = (
    HERE
    / "cm2_round162_exterior_unique_owner_pruning_certificate.json"
)
OUTPUT = (
    HERE
    / "cm2_round162_exterior_unique_owner_pruning_verification.json"
)
CERTIFICATE_SCHEMA = "cm2.round162.exterior-unique-owner-pruning.v1"
SCHEMA = "cm2.round162.exterior-unique-owner-pruning.verification.v1"
STATUS = (
    "CERTIFIED_FROZEN_PREFIX_UNIQUE_FIRST_OWNER_PRUNING__"
    "EXTERIOR_AND_D02_STILL_BLOCKED"
)
FROZEN_OWNER = "W[1,0]"
SOURCE_W_CHARTS = ("W:E", "W:W", "W:N", "W:S")

PRODUCER = "cm2_round162_exterior_unique_owner_pruning.py"
ATLAS_SOURCE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
ATLAS_MANIFEST = (
    "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json"
)
PRIOR_CERTIFICATE = (
    "cm2_round162_exterior_frozen_prefix_pruning_certificate.json"
)
PRIOR_VERIFICATION = (
    "cm2_round162_exterior_frozen_prefix_pruning_verification.json"
)
PINS = {
    PRODUCER:
        "b32d2fc2a67613bf89ec6a2818a4564a01f7a4c964a545f655759bb88d12d355",
    ATLAS_SOURCE:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    ATLAS_MANIFEST:
        "f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987",
    PRIOR_CERTIFICATE:
        "927bc20ca139e5bd1756c0b35bb10a8dbdddad1dde09bb4e6f2f3e73ddd88980",
    PRIOR_VERIFICATION:
        "a86f898d7457cec8a2f221a5ce257236cba065f58d1699e2caeacbddf44c42f3",
}
DEPENDENCY_PINS = {
    key: value for key, value in PINS.items() if key != PRODUCER
}
PRIOR_RESULT_SHA256 = (
    "9ee6d81996bc9c3886c3d48ac011b68e4ed51c7ea8ca6d34224d0911f9b39eb0"
)
PRIOR_VERIFICATION_RESULT_SHA256 = (
    "31bb4b16709ef6eec2d23b2cd338d6072c873fbff93fa642c5c5554a082be2ca"
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
        "raw encoding",
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


def check_pins() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    require(
        Path(atlas.__file__).resolve() == (HERE / ATLAS_SOURCE).resolve(),
        "atlas module identity",
    )
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )
    manifest = strict_load(HERE / ATLAS_MANIFEST)
    prior = strict_load(HERE / PRIOR_CERTIFICATE)
    verification = strict_load(HERE / PRIOR_VERIFICATION)
    require(
        manifest["schema"] == "cm2.gate3.eight-cell-symmetry-atlas.v1"
        and manifest["coverage"]["global_leaf_count"] == 143248,
        "atlas manifest",
    )
    require(
        prior["result_sha256"] == PRIOR_RESULT_SHA256
        == digest(prior["result"]),
        "prior certificate",
    )
    require(
        verification["result_sha256"] == PRIOR_VERIFICATION_RESULT_SHA256
        == digest(verification["result"])
        and verification["result"]["status"] == "PASS"
        and verification["result"]["certificate_result_sha256"]
        == PRIOR_RESULT_SHA256,
        "prior verification",
    )
    return manifest, prior, verification


def disposition_row(chart_id: str, leaf: Any) -> dict[str, Any]:
    require(
        leaf.classification == "unique_first"
        and type(leaf.owner_target) is str,
        "unique owner",
    )
    return {
        "chart_id": chart_id,
        "leaf_id": leaf.box.path,
        "owner_target": leaf.owner_target,
        "disposition": (
            "OWNER_MATCH_REQUIRES_OUTGOING_CHART"
            if leaf.owner_target == FROZEN_OWNER
            else "EARLIEST_PREFIX_EXCLUDED_OWNER_MISMATCH"
        ),
    }


def rebuild_expected() -> dict[str, Any]:
    manifest, prior, _verification = check_pins()
    reflection_digests = {
        "G:E->G:W": atlas.verify_reflection("G:E", "vertical"),
        "W:E->W:W": atlas.verify_reflection("W:E", "vertical"),
        "G:N->G:S": atlas.verify_reflection("G:N", "horizontal"),
        "W:N->W:S": atlas.verify_reflection("W:N", "horizontal"),
    }
    atlases = {
        "W:E": atlas.build_atlas("W:E"),
        "W:N": atlas.build_atlas("W:N"),
    }
    atlases["W:W"] = [
        atlas.reflect_leaf("W:E", "vertical", leaf)
        for leaf in atlases["W:E"]
    ]
    atlases["W:S"] = [
        atlas.reflect_leaf("W:N", "horizontal", leaf)
        for leaf in atlases["W:N"]
    ]
    charts: list[dict[str, Any]] = []
    mismatch_total = 0
    match_total = 0
    mismatch_volume_total = Q(0)
    match_volume_total = Q(0)

    for chart_id in SOURCE_W_CHARTS:
        leaves = atlases[chart_id]
        upstream = manifest["charts"][chart_id]
        rows = [
            atlas.leaf_row(chart_id, leaf)
            for leaf in sorted(leaves, key=lambda item: item.box.path)
        ]
        require(
            len(leaves) == upstream["leaf_count"]
            and atlas.canonical_digest(rows)
            == upstream["leaf_rows_sha256"],
            f"leaf replay:{chart_id}",
        )
        unique = [
            leaf for leaf in leaves
            if leaf.classification == "unique_first"
        ]
        mismatch = [
            leaf for leaf in unique
            if leaf.owner_target != FROZEN_OWNER
        ]
        match = [
            leaf for leaf in unique
            if leaf.owner_target == FROZEN_OWNER
        ]
        disposition = [
            disposition_row(chart_id, leaf)
            for leaf in sorted(unique, key=lambda item: item.box.path)
        ]
        mismatch_volume = sum(
            (atlas.box_volume(leaf.box) for leaf in mismatch), Q(0)
        )
        match_volume = sum(
            (atlas.box_volume(leaf.box) for leaf in match), Q(0)
        )
        require(
            len(unique) == upstream["counts"]["unique_first"]
            and len(mismatch) + len(match) == len(unique),
            f"unique census:{chart_id}",
        )
        charts.append({
            "chart_id": chart_id,
            "upstream_leaf_count": len(leaves),
            "upstream_leaf_rows_sha256": upstream["leaf_rows_sha256"],
            "unique_first_count": len(unique),
            "owner_mismatch_excluded_count": len(mismatch),
            "owner_match_outgoing_chart_unresolved_count": len(match),
            "owner_mismatch_excluded_volume_exact":
                str(mismatch_volume),
            "owner_match_unresolved_volume_exact": str(match_volume),
            "unique_disposition_rows_sha256": digest(disposition),
            "provenance": upstream["provenance"],
        })
        mismatch_total += len(mismatch)
        match_total += len(match)
        mismatch_volume_total += mismatch_volume
        match_volume_total += match_volume

    ww_row = next(row for row in charts if row["chart_id"] == "W:W")
    require(
        mismatch_total + match_total == 26204
        and ww_row["unique_first_count"] == 6518
        and ww_row["owner_mismatch_excluded_count"] == 6518
        and ww_row[
            "owner_match_outgoing_chart_unresolved_count"
        ] == 0,
        "aggregate unique-owner census",
    )
    prior_ww_excluded = prior["result"][
        "certified_open_cell_block"
    ]["frozen_prefix_excluded_leaf_count"]
    prior_ww_unique = prior["result"][
        "certified_open_cell_block"
    ]["covered_atlas_counts"]["unique_first"]
    additional = (
        mismatch_total
        - ww_row["owner_mismatch_excluded_count"]
    )
    combined = prior_ww_excluded + additional
    remaining = 76828 - combined
    require(
        prior_ww_excluded == 18930
        and prior_ww_unique == 6518
        and prior_ww_unique
        == ww_row["owner_mismatch_excluded_count"]
        and remaining == match_total + 32 + 38180,
        "combined frozen-prefix census",
    )

    return {
        "status": STATUS,
        "scope": {
            "signature_scope":
                "only the pinned Round139 first-collision frozen prefix",
            "source_scope":
                "Gate3 source obstacle W; unique-first leaves on four "
                "conservative chart covers",
            "disposition_rule":
                "unique first owner unequal to W[1,0] is an earliest "
                "prefix exclusion",
            "owner_match_does_not_imply_prefix_match": True,
            "outgoing_chart_not_checked_for_owner_matches": True,
            "counts_are_conservative_atlas_leaf_records": True,
            "record_identity": "chart_id plus leaf_id",
            "cross_chart_guard_band_overlap_quotiented": False,
            "not_all_return_signatures": True,
            "not_full_exterior_sheet_exhaustion": True,
            "not_D02_closure": True,
        },
        "provenance": {
            "dependency_sha256": DEPENDENCY_PINS,
            "prior_exterior_certificate_result_sha256":
                PRIOR_RESULT_SHA256,
            "prior_exterior_verification_result_sha256":
                PRIOR_VERIFICATION_RESULT_SHA256,
            "upstream_reflection_row_digests": reflection_digests,
            "source_W_atlas_replayed_at_192_bits": True,
            "old_artifacts_modified": False,
        },
        "frozen_prefix": {
            "collision_index": 1,
            "required_owner": FROZEN_OWNER,
            "required_outgoing_chart": "W",
            "prefix_length_used_here": 1,
        },
        "unique_first_owner_pruning": {
            "charts": charts,
            "source_W_unique_first_count": 26204,
            "owner_mismatch_excluded_count": mismatch_total,
            "owner_match_outgoing_chart_unresolved_count": match_total,
            "owner_mismatch_excluded_volume_exact":
                str(mismatch_volume_total),
            "owner_match_unresolved_volume_exact":
                str(match_volume_total),
            "all_unique_disposition_rows_sha256": digest(charts),
        },
        "combined_frozen_prefix_census": {
            "source_W_leaf_count": 76828,
            "prior_W_W_all_class_excluded_leaf_count":
                prior_ww_excluded,
            "prior_W_W_unique_overlap_count": prior_ww_unique,
            "new_additional_outside_W_W_unique_owner_mismatch_count":
                additional,
            "combined_recordwise_excluded_leaf_count": combined,
            "remaining_leaf_count": remaining,
            "remaining_unique_owner_match_outgoing_chart_unresolved":
                match_total,
            "remaining_tangency_graph": 32,
            "remaining_multi_candidate": 38180,
            "frozen_prefix_unresolved_leaves_zero": False,
            "physical_disjoint_cell_count_claimed": False,
        },
        "global_all_signature_queue": {
            "unchanged_source_W_unique_first_total": 26204,
            "unchanged_source_W_tangency_graph_total": 56,
            "unchanged_source_W_multi_candidate_total": 50568,
            "all_signature_unresolved_leaves_zero": False,
            "reason":
                "a mismatch against one frozen prefix does not remove a "
                "leaf from other return-signature searches",
        },
        "strict_nonpromotion": {
            "all_disconnected_exterior_sheets_excluded": False,
            "all_chart_and_grazing_strata_glued_or_typed": False,
            "all_return_signatures_excluded_or_connected": False,
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "resolve outgoing chart on the 1,176 owner-matching unique "
            "leaves, type the 32 outside-W:W tangency strata, and "
            "subdivide the 38,180 outside-W:W multi-candidate leaves; "
            "then extend across source-G and every relevant return signature"
        ),
    }


def validate(document: dict[str, Any], expected: dict[str, Any]) -> None:
    require(
        set(document) == {"schema", "result", "result_sha256"}
        and document["schema"] == CERTIFICATE_SCHEMA
        and type(document["result"]) is dict
        and type(document["result_sha256"]) is str
        and document["result_sha256"] == digest(document["result"])
        and canonical(document["result"]) == canonical(expected),
        "certificate exact reconstruction",
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
        "status promoted": mutate(
            document, ("result", "status"), "PASS"
        ),
        "frozen owner changed": mutate(
            document,
            ("result", "frozen_prefix", "required_owner"),
            "W[0,0]",
        ),
        "outgoing chart invented": mutate(
            document,
            (
                "result", "scope",
                "outgoing_chart_not_checked_for_owner_matches",
            ),
            False,
        ),
        "mismatch inflated": mutate(
            document,
            (
                "result", "unique_first_owner_pruning",
                "owner_mismatch_excluded_count",
            ),
            26204,
        ),
        "match erased": mutate(
            document,
            (
                "result", "unique_first_owner_pruning",
                "owner_match_outgoing_chart_unresolved_count",
            ),
            0,
        ),
        "chart count altered": mutate(
            document,
            (
                "result", "unique_first_owner_pruning", "charts", 0,
                "owner_mismatch_excluded_count",
            ),
            5633,
        ),
        "chart digest altered": mutate(
            document,
            (
                "result", "unique_first_owner_pruning", "charts", 1,
                "unique_disposition_rows_sha256",
            ),
            "0" * 64,
        ),
        "leaf digest altered": mutate(
            document,
            (
                "result", "unique_first_owner_pruning", "charts", 2,
                "upstream_leaf_rows_sha256",
            ),
            "0" * 64,
        ),
        "combined overlap erased": mutate(
            document,
            (
                "result", "combined_frozen_prefix_census",
                "prior_W_W_unique_overlap_count",
            ),
            0,
        ),
        "combined excluded inflated": mutate(
            document,
            (
                "result", "combined_frozen_prefix_census",
                "combined_distinct_excluded_leaf_count",
            ),
            76828,
        ),
        "remaining zero invented": mutate(
            document,
            (
                "result", "combined_frozen_prefix_census",
                "frozen_prefix_unresolved_leaves_zero",
            ),
            True,
        ),
        "remaining multi erased": mutate(
            document,
            (
                "result", "combined_frozen_prefix_census",
                "remaining_multi_candidate",
            ),
            0,
        ),
        "all signatures promoted": mutate(
            document,
            (
                "result", "global_all_signature_queue",
                "all_signature_unresolved_leaves_zero",
            ),
            True,
        ),
        "D02 promoted": mutate(
            document,
            ("result", "strict_nonpromotion", "D02"),
            "READY",
        ),
        "exterior promoted": mutate(
            document,
            (
                "result", "strict_nonpromotion",
                "all_disconnected_exterior_sheets_excluded",
            ),
            True,
        ),
        "dependency pin altered": mutate(
            document,
            (
                "result", "provenance", "dependency_sha256",
                ATLAS_SOURCE,
            ),
            "0" * 64,
        ),
        "bool-int confusion": mutate(
            document,
            (
                "result", "scope",
                "owner_match_does_not_imply_prefix_match",
            ),
            1,
        ),
        "extra field": mutate(
            document, ("result", "extra"), True
        ),
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
    semantic = semantic_attacks(document, expected)
    strict_attacks = strict_json_attacks()
    result = {
        "status": "PASS",
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_result_sha256": document["result_sha256"],
        "round162_producer_imported_or_executed": False,
        "pinned_upstream_192_bit_atlas_replayed": True,
        "all_26204_unique_dispositions_reconstructed": True,
        "per_chart_leaf_and_disposition_digests_reconstructed": True,
        "combined_overlap_safe_frozen_prefix_census_reconstructed": True,
        "semantic_attack_suite": semantic,
        "strict_json_attack_suite": strict_attacks,
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
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    document = build()
    if not arguments.self_test:
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
