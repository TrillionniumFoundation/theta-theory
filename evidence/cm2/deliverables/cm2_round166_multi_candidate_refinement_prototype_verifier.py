#!/usr/bin/env python3
"""Independent limited verifier for the Round166 multi-candidate prototype.

The verifier deliberately does not import the Round166 producer.  It:

* pins the producer, statistics, upstream atlas sources, and Round164 v2;
* independently reconstructs the pinned W:E/W:N/W:S atlas leaves;
* independently rebuilds all 35,564 immediate frozen-owner impossibility
  witnesses;
* checks every reported dyadic parent-volume conservation identity;
* rejects semantic and strict-JSON attacks.

It does not replay the six-level targeted refinement tree, so it verifies a
prototype baseline and its accounting, not a promotable completed atlas.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import time
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable

from flint import arb, ctx

import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_gate3_ge_interval_atlas_cert as ge


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round166_multi_candidate_refinement_prototype_verification.json"
)
SCHEMA = (
    "cm2.round166.multi-candidate-refinement-prototype."
    "limited-independent-verification.v1"
)
STATS_SCHEMA = "cm2.round166.multi-candidate-refinement-prototype.v1"
FROZEN_OWNER = "W[1,0]"
CHARTS = ("W:E", "W:N", "W:S")

PINS = {
    "cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_gate3_eight_cell_symmetry_atlas_cert.py":
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "cm2_gate3_ge_interval_atlas_cert.py":
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    "cm2_round164_tangency_strata_pruning_certificate.json":
        "2f1fcb72224f39c8d4a9d9f666a8579f71d77542e31552aa7c9dbc4b7338f092",
    "cm2_round164_tangency_strata_pruning_verification.json":
        "850bd24ae60979aaaea3f6819dcab665a1f7228d0c104014bfe8cce9e91299b0",
    "cm2_round166_multi_candidate_refinement_prototype.py":
        "6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c",
    # Filled after the final producer replay.
    "cm2_round166_multi_candidate_refinement_prototype_stats.json":
        "ffa028ff9e46219a48b3950a49a7c8f8d111fb54e7c3322aa4387366a2870999",
}
EXPECTED_STATS_RESULT_SHA256 = (
    "6972926f909815e041842fe5582f89898d1589ab69b54a801f5e28fdfa19e548"
)
ROUND164_RESULT_SHA256 = (
    "0f6d7f47ac20734ed294dd04cd7720ccbb9c0a1d4236980f814dd2ea2d5e79d9"
)
ROUND164_VERIFICATION_RESULT_SHA256 = (
    "bb2e51bdbbd457a5782038efc527000cbf89b73c8645fd6facd126fa453af8c4"
)
CANDIDATE_SHA256 = {
    "W:E": "ebeeae12ba192d7808031ebf4be3537fb49e73e17295404adcad371045e7c2e7",
    "W:N": "4719c19ccb8c63288e8815c4b8961f64d9d096dd4377641acafbec59c00769e5",
    "W:S": "89d699755e74a71b2771fb907e3f1bcf0e13d96621a977a4731c563cb928a5f8",
}
LEAF_SHA256 = {
    "W:E": "248c0b77c22594ceb69f475978bcc9d7867530fcfaeefe1518e3538938c268e2",
    "W:N": "728dbce4e414bc859d050b3fa5619febcddd277d3354b2af6c32f3414212ea82",
    "W:S": "e3fbab0ef15d6b9fd06e1b78da40050eb29b8bb724ceb4ad5408926f7eeaa373",
}
EXPECTED_CHARTS = {
    "W:E": (12388, 11260, 1128),
    "W:N": (12896, 12152, 744),
    "W:S": (12896, 12152, 744),
}
EXPECTED_WITNESSES = {
    "owner_dominated_by_strict_future_root": 76,
    "owner_intersection_behind": 1178,
    "owner_no_real_intersection": 34310,
}
EXPECTED_DOMINATORS = {"G[1,0]": 38, "G[1,1]": 38}


def canonical(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_load_raw(raw: bytes, label: str) -> dict[str, Any]:
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"encoding:{label}",
    )

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate key:{label}")
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
                f"decoded string encoding:{label}",
            )
        elif type(item) is list:
            for child in item:
                strings(child)
        elif type(item) is dict:
            for key, child in item.items():
                strings(key)
                strings(child)

    strings(value)
    require(type(value) is dict, f"top object:{label}")
    return value


def strict_load(path: Path) -> dict[str, Any]:
    return strict_load_raw(path.read_bytes(), path.name)


_candidate_cache = {
    chart_id: tuple(base.candidate_ids(chart_id))
    for chart_id in CHARTS
}
_target_cache = {target.target_id: target for target in base.TARGETS}


def root_from_geometry(
    geometry: tuple[arb, arb, arb, arb, arb, arb],
    target_id: str,
) -> ge.RootRecord:
    qx, qy, ux, uy, s, _radical_p = geometry
    target = _target_cache[target_id]
    ax, ay = base.target_center(target, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = base.arbq(base.RADIUS[target.obstacle])
    discriminant = radius * radius - transverse * transverse
    if bool(discriminant < 0):
        return ge.RootRecord(
            target_id, "no_real_intersection", ell, discriminant,
            None, None, transverse,
        )
    if not bool(discriminant > 0):
        return ge.RootRecord(
            target_id, "unresolved_discriminant", ell, discriminant,
            None, None, transverse,
        )
    radical = discriminant.sqrt()
    near, far = ell - radical, ell + radical
    if bool(far < 0):
        classification = "intersection_behind"
    elif bool(near > 0):
        classification = "strict_future_root"
    else:
        classification = "unresolved_root_sign"
    return ge.RootRecord(
        target_id, classification, ell, discriminant,
        near, far, transverse,
    )


def root_fast(
    chart_id: str,
    box: ge.AtlasBox,
    target_id: str,
) -> ge.RootRecord:
    return root_from_geometry(atlas.geometry(chart_id, box), target_id)


def records_for(
    chart_id: str,
    box: ge.AtlasBox,
    target_ids: Iterable[str],
) -> list[ge.RootRecord]:
    geometry = atlas.geometry(chart_id, box)
    return [
        root_from_geometry(geometry, target_id)
        for target_id in target_ids
    ]


def records_full(chart_id: str, box: ge.AtlasBox) -> list[ge.RootRecord]:
    return records_for(chart_id, box, _candidate_cache[chart_id])


def install_fast_replay() -> None:
    for chart_id, candidates in _candidate_cache.items():
        require(
            base.canonical_digest(list(candidates))
            == CANDIDATE_SHA256[chart_id],
            f"candidate digest:{chart_id}",
        )

    def candidate_ids(chart_id: str) -> list[str]:
        return list(_candidate_cache[chart_id])

    def target_by_id(target_id: str) -> base.Target:
        return _target_cache[target_id]

    base.candidate_ids = candidate_ids
    base.target_by_id = target_by_id
    atlas.records = records_full
    atlas.root_record = root_fast


def rebuild_baseline() -> dict[str, list[ge.Leaf]]:
    direct_e = atlas.build_atlas("W:E")
    direct_n = atlas.build_atlas("W:N")
    charts = {
        "W:E": direct_e,
        "W:N": direct_n,
        "W:S": [
            atlas.reflect_leaf("W:N", "horizontal", leaf)
            for leaf in direct_n
        ],
    }
    for chart_id, leaves in charts.items():
        rows = [
            atlas.leaf_row(chart_id, leaf)
            for leaf in sorted(leaves, key=lambda item: item.box.path)
        ]
        require(
            atlas.canonical_digest(rows) == LEAF_SHA256[chart_id],
            f"leaf digest:{chart_id}",
        )
    return charts


def immediate_census(
    charts: dict[str, list[ge.Leaf]],
) -> dict[str, Any]:
    witnesses: Counter[str] = Counter()
    dominators: Counter[str] = Counter()
    chart_rows: dict[str, dict[str, int]] = {}
    for chart_id, leaves in charts.items():
        multi = [
            leaf for leaf in leaves
            if leaf.classification == "multi_candidate"
        ]
        owner_active = 0
        owner_absent = 0
        for leaf in multi:
            require(leaf.box.depth == atlas.MAX_DEPTH, "multi max depth")
            if FROZEN_OWNER in leaf.active_targets:
                owner_active += 1
                continue
            owner_absent += 1
            owner = root_fast(chart_id, leaf.box, FROZEN_OWNER)
            if owner.classification in {
                "no_real_intersection", "intersection_behind",
            }:
                witnesses[f"owner_{owner.classification}"] += 1
                continue
            lower = ge.earliest_possible_root_lower(owner)
            require(lower is not None, "inactive owner lower")
            records = records_full(chart_id, leaf.box)
            strict = [
                row for row in records
                if row.target_id != FROZEN_OWNER
                and row.classification == "strict_future_root"
                and row.near is not None
                and bool(row.near < lower)
            ]
            require(bool(strict), "inactive owner dominator")
            witnesses["owner_dominated_by_strict_future_root"] += 1
            dominators[strict[0].target_id] += 1
        expected = EXPECTED_CHARTS[chart_id]
        require(
            (len(multi), owner_absent, owner_active) == expected,
            f"chart immediate census:{chart_id}",
        )
        chart_rows[chart_id] = {
            "multi_candidate": len(multi),
            "frozen_owner_absent_exact_prefix_exclusion": owner_absent,
            "frozen_owner_in_active": owner_active,
        }
    require(dict(witnesses) == EXPECTED_WITNESSES, "witness counts")
    require(dict(dominators) == EXPECTED_DOMINATORS, "dominator counts")
    return {
        "charts": chart_rows,
        "witness_types": dict(sorted(witnesses.items())),
        "dominator_targets": dict(sorted(dominators.items())),
        "multi_count": sum(row["multi_candidate"] for row in chart_rows.values()),
        "owner_absent": sum(
            row["frozen_owner_absent_exact_prefix_exclusion"]
            for row in chart_rows.values()
        ),
        "owner_active": sum(
            row["frozen_owner_in_active"]
            for row in chart_rows.values()
        ),
    }


def check_round164_v2() -> None:
    certificate = strict_load(
        HERE / "cm2_round164_tangency_strata_pruning_certificate.json"
    )
    verification = strict_load(
        HERE / "cm2_round164_tangency_strata_pruning_verification.json"
    )
    require(
        certificate["result_sha256"] == ROUND164_RESULT_SHA256
        and verification["result_sha256"]
        == ROUND164_VERIFICATION_RESULT_SHA256
        and verification["result"]["status"] == "PASS"
        and verification["result"]["certificate_result_sha256"]
        == certificate["result_sha256"],
        "Round164 v2 chain",
    )
    result = certificate["result"]
    typing = result["tangency_graph_typing"]
    ambient = result["ambient_frozen_prefix_census"]
    require(
        typing["ambient_parameter_dimension"] == 3
        and typing["ambient_parent_leaf_count"] == 32
        and typing["new_full_dimensional_parent_leaf_exclusion_count"] == 0
        and typing["remaining_off_graph_ambient_parent_count"] == 32
        and all(
            row["ambient_parameter_dimension"] == 3
            and row["typed_graph_dimension"] == 2
            and row["credit_scope"] == "CODIMENSION_ONE_GRAPH_ONLY"
            and row["ambient_leaf_bulk_disposition"]
            == "UNRESOLVED_OFF_GRAPH_BULK"
            for row in typing["rows"]
        )
        and ambient["combined_recordwise_excluded_ambient_leaf_count"] == 37480
        and ambient["remaining_ambient_unresolved_leaf_count"] == 39348
        and ambient["remaining_multi_candidate"] == 38180
        and ambient["new_full_dimensional_ambient_leaf_exclusion_count"] == 0,
        "Round164 v2 dimension and census",
    )


def validate_stats(document: dict[str, Any]) -> None:
    require(document["schema"] == STATS_SCHEMA, "stats schema")
    require(document["result_sha256"] == digest(document["result"]), "stats digest")
    require(
        document["result_sha256"] == EXPECTED_STATS_RESULT_SHA256,
        "stats result identity",
    )
    result = document["result"]
    require(
        result["status"]
        == "NONPROMOTIONAL_PROTOTYPE__VALID_ROUND163_AMBIENT_BASELINE",
        "stats status",
    )
    require(
        result["provenance"]["round166_producer_sha256"]
        == PINS["cm2_round166_multi_candidate_refinement_prototype.py"],
        "producer provenance",
    )
    require(
        result["round164_v2_dimension_safe_chain"] == {
            "ambient_parameter_dimension": 3,
            "ambient_parent_leaf_count": 32,
            "ambient_recordwise_excluded_leaf_count": 37480,
            "ambient_remaining_leaf_count": 39348,
            "certificate_file_sha256": PINS[
                "cm2_round164_tangency_strata_pruning_certificate.json"
            ],
            "certificate_result_sha256": ROUND164_RESULT_SHA256,
            "full_dimensional_leaf_exclusion_count": 0,
            "typed_graph_dimension": 2,
            "verification_file_sha256": PINS[
                "cm2_round164_tangency_strata_pruning_verification.json"
            ],
            "verification_result_sha256":
                ROUND164_VERIFICATION_RESULT_SHA256,
        },
        "stats Round164 v2 chain",
    )
    baseline = result["baseline"]
    require(
        baseline["outside_W_W_multi_candidate_count"] == 38180
        and baseline["all_multi_leaves_at_pinned_maximum_depth"] == 8
        and baseline["immediate_exact_prefix_exclusion_witness_types"]
        == EXPECTED_WITNESSES
        and baseline["immediate_dominator_targets"]
        == EXPECTED_DOMINATORS,
        "stats baseline",
    )
    for chart_id, (multi, absent, active) in EXPECTED_CHARTS.items():
        require(
            baseline["charts"][chart_id] == {
                "multi_candidate": multi,
                "frozen_owner_absent_exact_prefix_exclusion": absent,
                "frozen_owner_in_active": active,
            },
            f"stats chart:{chart_id}",
        )
    refinement = result["refinement"]
    require(
        refinement["maximum_extra_depth"] == 6
        and refinement["evaluated_box_count"] == 167984
        and refinement["evaluated_target_record_count"] == 415570,
        "stats refinement work",
    )
    snapshots = refinement["snapshots"]
    require(len(snapshots) == 7, "snapshot count")
    for index, row in enumerate(snapshots):
        require(
            row["extra_depth"] == index
            and row["absolute_max_depth"] == 8 + index,
            f"snapshot depth:{index}",
        )
        unresolved = Q(row["unresolved_parent_box_volume_equivalent"])
        terminal = Q(row["terminal_parent_box_volume_equivalent_cumulative"])
        require(unresolved + terminal == 2616, f"snapshot conservation:{index}")
        require(
            unresolved
            == Q(row["unresolved_subbox_count"], 2 ** index),
            f"snapshot dyadic volume:{index}",
        )
    summary = refinement["parent_box_equivalent_summary"]
    require(
        summary == {
            "classified_fraction_of_38180": "119337/122176",
            "classified_multi_parent_equivalent": "596685/16",
            "final_unresolved_subbox_volume": "14195/16",
            "immediate_whole_parent_exclusions": "35564",
            "owner_active_input": "2616",
            "terminal_classified_subbox_volume": "27661/16",
            "unresolved_fraction_of_38180": "2839/122176",
        },
        "summary identity",
    )
    terminal = refinement["terminal_parent_box_volume_by_disposition"]
    require(
        terminal == {
            "EXCLUDED_OUTGOING_CHART_MISMATCH": "11437/32",
            "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH": "12649/16",
            "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH": "18587/32",
        }
        and sum((Q(value) for value in terminal.values()), Q(0))
        == Q(27661, 16),
        "terminal conservation",
    )
    require(
        Q(summary["immediate_whole_parent_exclusions"])
        + Q(summary["terminal_classified_subbox_volume"])
        + Q(summary["final_unresolved_subbox_volume"])
        == 38180,
        "global multi conservation",
    )
    require(
        all(type(value) is str for value in result["runtime_seconds"].values()),
        "runtime strings",
    )
    strict = result["strict_nonpromotion"]
    require(
        strict["prototype_not_an_independent_verifier"]
        and strict["valid_round163_combined_excluded_leaf_records"] == 37480
        and strict["valid_round163_remaining_leaf_records"] == 39348
        and strict["D02"] == "BLOCKED"
        and strict["D03_negative_oracle"] == "UNAUTHORIZED"
        and strict["CM2"] == "NO-GO_FOR_CLAIM",
        "strict nonpromotion",
    )


def semantic_attacks(document: dict[str, Any]) -> tuple[int, int]:
    attacks = []

    def mutate(path: tuple[Any, ...], value: Any) -> None:
        candidate = copy.deepcopy(document)
        cursor: Any = candidate
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        candidate["result_sha256"] = digest(candidate["result"])
        attacks.append(candidate)

    mutate(("result", "status"), "CERTIFIED")
    mutate(("result", "baseline", "outside_W_W_multi_candidate_count"), 38179)
    mutate(
        (
            "result", "baseline",
            "immediate_exact_prefix_exclusion_witness_types",
            "owner_no_real_intersection",
        ),
        34311,
    )
    mutate(
        (
            "result", "baseline", "charts", "W:E",
            "frozen_owner_in_active",
        ),
        1129,
    )
    mutate(
        (
            "result", "round164_v2_dimension_safe_chain",
            "typed_graph_dimension",
        ),
        3,
    )
    mutate(
        (
            "result", "round164_v2_dimension_safe_chain",
            "full_dimensional_leaf_exclusion_count",
        ),
        12,
    )
    mutate(("result", "refinement", "maximum_extra_depth"), 5)
    mutate(
        (
            "result", "refinement", "snapshots", 6,
            "unresolved_parent_box_volume_equivalent",
        ),
        "14194/16",
    )
    mutate(
        (
            "result", "refinement", "parent_box_equivalent_summary",
            "classified_fraction_of_38180",
        ),
        "1",
    )
    mutate(
        (
            "result", "refinement",
            "terminal_parent_box_volume_by_disposition",
            "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH",
        ),
        "18589/32",
    )
    mutate(
        (
            "result", "strict_nonpromotion",
            "valid_round163_remaining_leaf_records",
        ),
        39336,
    )
    mutate(("result", "strict_nonpromotion", "D02"), "CLOSED")
    rejected = 0
    for candidate in attacks:
        try:
            validate_stats(candidate)
        except Exception:
            rejected += 1
    return rejected, len(attacks)


def json_attacks() -> tuple[int, int]:
    attacks = [
        b'{"a":1,"a":2}',
        b'{"a":1.0}',
        b'{"a":NaN}',
        b'\xef\xbb\xbf{"a":1}',
        b'{"a":"x\\u0000y"}',
        b'{"a":"\\ud800"}',
        b'{"a":1} trailing',
        b'[1]',
    ]
    rejected = 0
    for index, raw in enumerate(attacks):
        try:
            strict_load_raw(raw, f"attack-{index}")
        except Exception:
            rejected += 1
    return rejected, len(attacks)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    ctx.prec = 192
    started = time.perf_counter()
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )
    require(
        "cm2_round166_multi_candidate_refinement_prototype"
        not in __import__("sys").modules,
        "producer not imported",
    )
    check_round164_v2()
    stats = strict_load(
        HERE / "cm2_round166_multi_candidate_refinement_prototype_stats.json"
    )
    validate_stats(stats)
    install_fast_replay()
    charts = rebuild_baseline()
    census = immediate_census(charts)
    require(census["multi_count"] == 38180, "independent multi total")
    require(census["owner_absent"] == 35564, "independent absent total")
    require(census["owner_active"] == 2616, "independent active total")
    semantic_rejected, semantic_total = semantic_attacks(stats)
    json_rejected, json_total = json_attacks()
    require(semantic_rejected == semantic_total, "semantic attacks")
    require(json_rejected == json_total, "JSON attacks")
    result = {
        "status": "PASS_LIMITED_BASELINE_WITNESS_AND_CONSERVATION_VERIFICATION",
        "producer_imported": False,
        "certificate_result_sha256": stats["result_sha256"],
        "independent_baseline_replay": {
            "candidate_sha256": CANDIDATE_SHA256,
            "leaf_rows_sha256": LEAF_SHA256,
            "multi_candidate_count": census["multi_count"],
            "immediate_whole_parent_prefix_exclusion_count":
                census["owner_absent"],
            "owner_active_subdivision_input_count": census["owner_active"],
            "witness_types": census["witness_types"],
            "dominator_targets": census["dominator_targets"],
        },
        "dimension_safe_chain": {
            "round164_v2_certificate_result_sha256":
                ROUND164_RESULT_SHA256,
            "round164_v2_verification_result_sha256":
                ROUND164_VERIFICATION_RESULT_SHA256,
            "ambient_dimension": 3,
            "typed_graph_dimension": 2,
            "full_dimensional_leaf_exclusion_count": 0,
        },
        "conservation": {
            "all_seven_depth_snapshots_checked": True,
            "terminal_plus_unresolved_owner_active_input": "2616",
            "immediate_plus_terminal_plus_unresolved_multi_total": "38180",
            "valid_ambient_recordwise_census": "37480 excluded / 39348 remaining",
        },
        "attacks": {
            "semantic_rejected": semantic_rejected,
            "semantic_total": semantic_total,
            "strict_json_rejected": json_rejected,
            "strict_json_total": json_total,
        },
        "scope": {
            "six_level_refinement_tree_independently_replayed": False,
            "prototype_fully_promoted": False,
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "dependency_sha256": PINS,
    }
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    args.output.write_text(
        json.dumps(
            document, sort_keys=True, indent=2,
            ensure_ascii=False, allow_nan=False,
        ) + "\n"
    )
    print(document["result_sha256"])
    print(canonical(result["independent_baseline_replay"]))
    print(canonical(result["attacks"]))
    print(
        "wall_clock_seconds_stdout_only="
        + format(time.perf_counter() - started, ".6f")
    )


if __name__ == "__main__":
    main()
