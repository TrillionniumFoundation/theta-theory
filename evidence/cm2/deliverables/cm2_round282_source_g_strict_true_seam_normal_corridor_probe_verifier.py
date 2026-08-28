#!/usr/bin/env python3
"""Independent verifier for the Round282 strict seam-normal corridor probe.

The Round282 producer is pinned as inert bytes and is never imported.  Starting
from the frozen Round280 patch channels and the complete Round275 region
certificate, this verifier independently reconstructs every one of the 304
directed patch sides, extends each eligible strict region to the algebraic
seam, reruns the frozen Round174 evaluator on the whole rational outer
corridor, and recomputes the exact p-by-s union area.

This verification is deliberately ZERO-CREDIT.  In particular, full normal
coverage is not interpreted as a same-point cross-chart component edge.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import sys
from typing import Any, Callable

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174


HERE = Path(__file__).resolve().parent
PRODUCER = HERE / "cm2_round282_source_g_strict_true_seam_normal_corridor_probe.py"
LEDGER = HERE / "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_ledger.json.gz"
RESULT = HERE / "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_result.json"
PATCH_CHANNELS = HERE / (
    "cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_"
    "patch_channels.json.gz"
)
R275 = HERE / "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json"
OUTPUT = HERE / "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_verification.json"
SCHEMA = "cm2.round282.source-g-strict-true-seam-normal-corridor-probe.verification.v1"

PINS = {
    PRODUCER.name: "61e30d129ff27762abcf25eb074c0ba147027df08aa3cd3860496323f79306fe",
    LEDGER.name: "6d94bce99b3ea57b8a568707705d9f16833cfba28b242a6dabb2de5933f6509e",
    RESULT.name: "cd054a7036d9c482357611e9af11d028179e0f34a828dca2fbe91332b178f532",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py":
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    "cm2_round273_source_g_reverse_rechart_probe.py":
        "40b18650a1fe8d797daf776cb9305686c21fa2eb5a7886c48ce91d697c93105c",
    "cm2_round274_source_g_reverse_rechart_tail_arrangement_probe.py":
        "677813e132d62732900a26edc3fae5d562049d8d1fac2cea59f7c65d41735292",
    R275.name: "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    PATCH_CHANNELS.name: "074b27dd062844331d2d43a91283f5d467fe957123294719e32237fece05d814",
}

PRODUCER_INPUT_PINS = {
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py":
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    "cm2_round273_source_g_reverse_rechart_probe.py":
        "40b18650a1fe8d797daf776cb9305686c21fa2eb5a7886c48ce91d697c93105c",
    "cm2_round274_source_g_reverse_rechart_tail_arrangement_probe.py":
        "677813e132d62732900a26edc3fae5d562049d8d1fac2cea59f7c65d41735292",
    R275.name: "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    PATCH_CHANNELS.name: "074b27dd062844331d2d43a91283f5d467fe957123294719e32237fece05d814",
}

ZERO_RESULT_FIELDS = (
    "expanded_occurrence_credit",
    "component_edge_credit",
    "maximality_credit",
    "exact_key_fibre_credit",
    "global_disposition_credit",
    "Jx_Jy_same_point_glue_credit",
)

ENC = json.JSONEncoder(
    sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
)


class VerificationError(RuntimeError):
    pass


def need(ok: bool, label: str) -> None:
    if not ok:
        raise VerificationError(label)


def canonical(value: Any) -> bytes:
    return ENC.encode(value).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("rb") as f:
        return json.load(f)


def read_gzip_json(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rb") as f:
        return json.load(f)


def gzip_bytes(value: Any) -> bytes:
    out = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=out, mtime=0) as f:
        f.write(canonical(value))
    return out.getvalue()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def rect_area(rect: tuple[Q, Q, Q, Q]) -> Q:
    return (rect[1] - rect[0]) * (rect[3] - rect[2])


def union_area(rectangles: list[tuple[Q, Q, Q, Q]]) -> Q:
    """Exact area of a not-necessarily-disjoint rational rectangle union."""
    if not rectangles:
        return Q(0)
    ps = sorted({value for rect in rectangles for value in rect[:2]})
    ss = sorted({value for rect in rectangles for value in rect[2:]})
    total = Q(0)
    for p0, p1 in zip(ps, ps[1:]):
        for s0, s1 in zip(ss, ss[1:]):
            if any(
                rect[0] <= p0 and p1 <= rect[1]
                and rect[2] <= s0 and s1 <= rect[3]
                for rect in rectangles
            ):
                total += (p1 - p0) * (s1 - s0)
    return total


def sqrt_dyadic_bounds(value: Q, bits: int) -> tuple[Q, Q]:
    """Independent exact enclosing dyadic interval for sqrt(value)."""
    need(value >= 0 and bits > 0, "sqrt domain")
    scale = 1 << bits
    scaled_numerator = value.numerator * scale * scale
    k = math.isqrt(scaled_numerator // value.denominator)
    while (k + 1) ** 2 * value.denominator <= scaled_numerator:
        k += 1
    while k * k * value.denominator > scaled_numerator:
        k -= 1
    lower = Q(k, scale)
    upper = lower if lower * lower == value else Q(k + 1, scale)
    need(lower * lower <= value <= upper * upper, "sqrt enclosure")
    return lower, upper


def signature_payload(signature: dict[str, Any], chart: str) -> dict[str, Any]:
    """Locally reconstruct the frozen ten-field Round275 payload."""
    return {
        "official_key_id": signature["key"]["identifier"],
        "official_key_ordinal": signature["key"]["ordinal"],
        "official_key_row": signature["key"]["row"],
        "ordered_integer_wall_events": signature["events"],
        "outgoing_cell": signature["outgoing_cell"],
        "roof": signature["roof"],
        "signed_wall_word": list(signature["pattern"]),
        "source_chart": chart,
        "target_chart": signature["target_chart"],
        "target_lift": signature["target"],
    }


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row["row_sha256"] = digest(row)
    return row


def verify_closed_ledger(name: str, ledger: dict[str, Any]) -> list[dict[str, Any]]:
    rows = ledger["rows"]
    need(ledger["row_count"] == len(rows), f"{name}:row count")
    need(ledger["rows_sha256"] == digest(rows), f"{name}:rows digest")
    ids = [
        row.get("reverse_rechart_region_row_id")
        or row.get("Round268_patch_channel_row_id")
        or row.get("Round282_seam_corridor_row_id")
        for row in rows
    ]
    need(len(ids) == len(set(ids)), f"{name}:unique ids")
    if "row_ids_sha256" in ledger:
        need(ledger["row_ids_sha256"] == digest(ids), f"{name}:id digest")
    hashes = []
    for row in rows:
        payload = dict(row)
        stored = payload.pop("row_sha256")
        need(stored == digest(payload), f"{name}:row closure")
        hashes.append(stored)
    if "row_hashes_sha256" in ledger:
        need(ledger["row_hashes_sha256"] == digest(hashes), f"{name}:hash digest")
    return rows


def load_frozen_inputs() -> tuple[
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, Any],
]:
    channels = read_gzip_json(PATCH_CHANNELS)
    patches = verify_closed_ledger("Round280 patch channels", channels)
    need(len(patches) == 152, "Round280 patch census")
    for patch in patches:
        need(len(patch["side_channel_rows"]) == 2, "two directed sides")
        pr = tuple(map(Q, [
            *patch["exact_common_p_interval"],
            *patch["exact_common_s_interval"],
        ]))
        need(rect_area(pr) == Q(patch["exact_positive_common_area"]) > 0, "patch area")
        for side in patch["side_channel_rows"]:
            ids = side["candidate_Round275_region_ids"]
            need(side["candidate_Round275_region_count"] == len(ids), "candidate count")
            need(side["candidate_Round275_region_ids_sha256"] == digest(ids), "candidate ids")

    wrapper = read_json(R275)
    need(set(wrapper) == {"result", "result_sha256"}, "Round275 wrapper")
    need(wrapper["result_sha256"] == digest(wrapper["result"]), "Round275 digest")
    r275 = wrapper["result"]
    strict_rows = verify_closed_ledger("Round275 strict regions", r275["strict_region_ledger"])
    arrangement_rows = verify_closed_ledger(
        "Round275 arrangement regions", r275["arrangement_region_ledger"]
    )
    need(len(strict_rows) == 5288 and len(arrangement_rows) == 8500, "Round275 census")
    strict = {row["reverse_rechart_region_row_id"]: row for row in strict_rows}
    arrangement = {
        row["reverse_rechart_region_row_id"]: row for row in arrangement_rows
    }
    need(set(strict).isdisjoint(arrangement), "Round275 disjoint region ids")
    for row in (*strict_rows, *arrangement_rows):
        need(
            row["complete_10_field_return_signature_sha256"]
            == digest(row["local_return_signature"]),
            "Round275 signature digest",
        )
        need(
            row["occurrence_credit"] == row["component_credit"]
            == row["maximality_credit"] == 0,
            "Round275 zero credit",
        )

    tables = r174.registry_tables(r174.load_inputs()["gate5"])
    return patches, strict, arrangement, tables


def reconstruct() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    patches, strict, arrangement, tables = load_frozen_inputs()
    lower, upper = sqrt_dyadic_bounds(Q(1, 2), 128)
    need(lower < upper and lower * lower < Q(1, 2) < upper * upper, "nonexact root")
    side_hist: Counter[str] = Counter()
    patch_hist: Counter[str] = Counter()
    accepted_total = 0
    rejected_total = 0
    rebuilt: list[dict[str, Any]] = []

    for patch in patches:
        patch_rect = tuple(map(Q, [
            *patch["exact_common_p_interval"],
            *patch["exact_common_s_interval"],
        ]))
        side_rows = []
        for side in patch["side_channel_rows"]:
            accepted = []
            failures: Counter[str] = Counter()
            arrangement_count = 0
            for region_id in side["candidate_Round275_region_ids"]:
                need(region_id in strict or region_id in arrangement, "known Round275 region")
                if region_id in arrangement:
                    arrangement_count += 1
                    failures["EXPLICIT_OUTGOING_OR_WALL_ARRANGEMENT_REGION"] += 1
                    continue
                region = strict[region_id]
                need(
                    region["source_guard_row_id"]
                    in side["candidate_guard_row_ids"],
                    "region guard belongs to channel",
                )
                need(
                    region["adjacent_chart"] == side["adjacent_chart"],
                    "region adjacent chart",
                )
                box = tuple(map(Q, region["adjacent_rational_region_box"]))
                footprint = (
                    max(patch_rect[0], box[2]),
                    min(patch_rect[1], box[3]),
                    max(patch_rect[2], box[4]),
                    min(patch_rect[3], box[5]),
                )
                if rect_area(footprint) <= 0:
                    continue

                positive_root = box[0] >= 0
                if positive_root:
                    need(box[0] < lower <= upper, "positive corridor crosses seam")
                    corridor = r174.atlas.AtlasBox(
                        box[0], upper,
                        footprint[0], footprint[1], footprint[2], footprint[3],
                        0, "independent-seam-corridor",
                    )
                else:
                    need(-upper <= -lower < box[1], "negative corridor crosses seam")
                    corridor = r174.atlas.AtlasBox(
                        -upper, box[1],
                        footprint[0], footprint[1], footprint[2], footprint[3],
                        0, "independent-seam-corridor",
                    )
                signature, reasons = r174.dynamic_signature(
                    region["adjacent_chart"], corridor, region["owner_target"], tables
                )
                if signature is None:
                    failures.update(f"DYNAMIC_SIGNATURE:{reason}" for reason in reasons)
                    continue
                local = signature_payload(signature, region["adjacent_chart"])
                need(local == region["local_return_signature"], "dynamic signature match")
                accepted.append({
                    "Round275_region_id": region_id,
                    "source_guard_row_id": region["source_guard_row_id"],
                    "source_round": region["source_round"],
                    "parent_id": region["parent_id"],
                    "owner_target": region["owner_target"],
                    "adjacent_chart": region["adjacent_chart"],
                    "corridor_rational_outer_box": [
                        qstr(corridor.t0), qstr(corridor.t1),
                        qstr(corridor.p0), qstr(corridor.p1),
                        qstr(corridor.s0), qstr(corridor.s1),
                    ],
                    "seam_root_sign": "POSITIVE" if positive_root else "NEGATIVE",
                    "seam_algebraic_endpoint":
                        "t=+sqrt(1/2)" if positive_root else "t=-sqrt(1/2)",
                    "seam_dyadic_outer_endpoint": qstr(upper if positive_root else -upper),
                    "positive_ps_footprint": [qstr(value) for value in footprint],
                    "positive_ps_area": qstr(rect_area(footprint)),
                    "complete_10_field_return_signature_sha256":
                        region["complete_10_field_return_signature_sha256"],
                    "whole_outer_corridor_dynamic_signature_strict": True,
                    "analytic_half_open_restriction_touches_true_seam": True,
                })

            covered = union_area([
                tuple(map(Q, row["positive_ps_footprint"])) for row in accepted
            ])
            need(Q(0) <= covered <= rect_area(patch_rect), "covered area range")
            full = covered == rect_area(patch_rect)
            classification = (
                "FULL_STRICT_NORMAL_CORRIDOR_COVER"
                if full else
                "PARTIAL_STRICT_COVER__ARRANGEMENT_TAIL_FAIL_CLOSED"
            )
            side_hist[classification] += 1
            accepted_total += len(accepted)
            rejected_total += sum(failures.values())
            side_rows.append({
                "side": side["side"],
                "source_chart": side["source_chart"],
                "adjacent_chart": side["adjacent_chart"],
                "local_t_root": side["local_t_root"],
                "classification": classification,
                "patch_area": qstr(rect_area(patch_rect)),
                "strict_corridor_covered_area": qstr(covered),
                "unresolved_area": qstr(rect_area(patch_rect) - covered),
                "accepted_strict_corridor_count": len(accepted),
                "accepted_strict_corridors": accepted,
                "rejected_or_deferred_candidate_count": sum(failures.values()),
                "rejected_or_deferred_reason_histogram":
                    dict(sorted(failures.items())),
                "arrangement_candidate_count": arrangement_count,
                "component_edge_credit": 0,
            })

        patch_class = (
            "FULL_BIDIRECTIONAL_STRICT_NORMAL_CORRIDOR_COVER"
            if all(side["classification"] == "FULL_STRICT_NORMAL_CORRIDOR_COVER"
                   for side in side_rows)
            else "SEAM_PATCH_REMAINS_FAIL_CLOSED_FOR_ARRANGEMENT_TAIL"
        )
        patch_hist[patch_class] += 1
        rebuilt.append(close_row({
            "Round282_seam_corridor_row_id":
                "round282-seam-corridor:"
                + digest(patch["Round268_true_seam_patch_row_id"]),
            "Round268_true_seam_patch_row_id":
                patch["Round268_true_seam_patch_row_id"],
            "cyclic_transition_identity": patch["cyclic_transition_identity"],
            "exact_common_p_interval": patch["exact_common_p_interval"],
            "exact_common_s_interval": patch["exact_common_s_interval"],
            "exact_positive_common_area": patch["exact_positive_common_area"],
            "classification": patch_class,
            "side_corridors": side_rows,
            "cross_chart_component_edge_credit": 0,
            "maximality_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
        }))

    rebuilt.sort(key=lambda row: row["Round282_seam_corridor_row_id"])
    census = {
        "input_patch_count": 152,
        "directed_patch_side_count": 304,
        "side_classification_histogram": dict(sorted(side_hist.items())),
        "patch_classification_histogram": dict(sorted(patch_hist.items())),
        "accepted_strict_corridor_candidate_count": accepted_total,
        "rejected_or_deferred_candidate_count": rejected_total,
        "fully_resolved_patch_count":
            patch_hist["FULL_BIDIRECTIONAL_STRICT_NORMAL_CORRIDOR_COVER"],
        "remaining_arrangement_tail_patch_count":
            patch_hist["SEAM_PATCH_REMAINS_FAIL_CLOSED_FOR_ARRANGEMENT_TAIL"],
    }
    need(
        census == {
            "input_patch_count": 152,
            "directed_patch_side_count": 304,
            "side_classification_histogram": {
                "FULL_STRICT_NORMAL_CORRIDOR_COVER": 264,
                "PARTIAL_STRICT_COVER__ARRANGEMENT_TAIL_FAIL_CLOSED": 40,
            },
            "patch_classification_histogram": {
                "FULL_BIDIRECTIONAL_STRICT_NORMAL_CORRIDOR_COVER": 128,
                "SEAM_PATCH_REMAINS_FAIL_CLOSED_FOR_ARRANGEMENT_TAIL": 24,
            },
            "accepted_strict_corridor_candidate_count": 2660,
            "rejected_or_deferred_candidate_count": 7264,
            "fully_resolved_patch_count": 128,
            "remaining_arrangement_tail_patch_count": 24,
        },
        "reconstructed census",
    )
    return rebuilt, census


def audit_candidate(
    ledger: dict[str, Any],
    result: dict[str, Any],
    expected_rows: list[dict[str, Any]],
    expected_census: dict[str, Any],
) -> None:
    rows = verify_closed_ledger("Round282 ledger", ledger)
    need(len(rows) == 152, "Round282 ledger census")
    need(rows == expected_rows, "exact independent row reconstruction")
    need(result["schema"] == "cm2.round282.source-g-strict-true-seam-normal-corridor-probe.v1", "result schema")
    need(
        result["status"]
        == "PASS_ROUND282_STRICT_TRUE_SEAM_NORMAL_CORRIDOR_COVER__24_PATCHES_FAIL_CLOSED__ZERO_CREDIT",
        "result status",
    )
    need(
        result["result_sha256"]
        == digest({key: value for key, value in result.items() if key != "result_sha256"}),
        "result closure",
    )
    need(result["pins"] == PRODUCER_INPUT_PINS, "producer input pins")
    need(result["census"] == expected_census, "result census")
    need(
        result["ledger"]["filename"] == LEDGER.name
        and result["ledger"]["row_count"] == len(rows)
        and result["ledger"]["rows_sha256"] == ledger["rows_sha256"]
        and result["ledger"]["file_sha256"]
        == hashlib.sha256(gzip_bytes(ledger)).hexdigest(),
        "result ledger binding",
    )
    nonpromotion = result["strict_nonpromotion"]
    need(all(nonpromotion[field] == 0 for field in ZERO_RESULT_FIELDS), "zero promotion")
    need(
        nonpromotion["quotient"] == 63224
        and nonpromotion["expanded_occurrences"] == 126468
        and nonpromotion["Gate5"] == "10/18"
        and nonpromotion["D02"] == "BLOCKED"
        and nonpromotion["CM2"] == "NO-GO_FOR_CLAIM",
        "frozen baseline",
    )
    for row in rows:
        need(
            row["cross_chart_component_edge_credit"]
            == row["maximality_credit"]
            == row["Jx_Jy_same_point_glue_credit"] == 0,
            "row zero credit",
        )
        for side in row["side_corridors"]:
            need(side["component_edge_credit"] == 0, "side zero credit")
            need(
                Q(side["strict_corridor_covered_area"]) + Q(side["unresolved_area"])
                == Q(side["patch_area"]),
                "side area conservation",
            )
            need(
                side["accepted_strict_corridor_count"]
                == len(side["accepted_strict_corridors"]),
                "accepted corridor count",
            )
            need(
                side["rejected_or_deferred_candidate_count"]
                == sum(side["rejected_or_deferred_reason_histogram"].values()),
                "rejection histogram",
            )


def reclose(ledger: dict[str, Any], result: dict[str, Any]) -> None:
    for row in ledger["rows"]:
        payload = dict(row)
        payload.pop("row_sha256", None)
        row["row_sha256"] = digest(payload)
    ledger["row_count"] = len(ledger["rows"])
    ledger["rows_sha256"] = digest(ledger["rows"])
    ledger["row_ids_sha256"] = digest([
        row["Round282_seam_corridor_row_id"] for row in ledger["rows"]
    ])
    ledger["row_hashes_sha256"] = digest([
        row["row_sha256"] for row in ledger["rows"]
    ])
    result["ledger"]["row_count"] = len(ledger["rows"])
    result["ledger"]["rows_sha256"] = ledger["rows_sha256"]
    result["ledger"]["file_sha256"] = hashlib.sha256(gzip_bytes(ledger)).hexdigest()
    result["result_sha256"] = digest({
        key: value for key, value in result.items() if key != "result_sha256"
    })


def run_attacks(
    ledger: dict[str, Any],
    result: dict[str, Any],
    expected_rows: list[dict[str, Any]],
    expected_census: dict[str, Any],
) -> dict[str, Any]:
    attacks: list[tuple[str, Callable[[dict[str, Any], dict[str, Any]], None]]] = [
        ("DELETE_PATCH_ROW", lambda l, r: l["rows"].pop()),
        ("DUPLICATE_PATCH_ROW", lambda l, r: l["rows"].append(deepcopy(l["rows"][0]))),
        ("FORGE_PATCH_CLASS", lambda l, r: l["rows"][0].__setitem__(
            "classification", "SEAM_PATCH_REMAINS_FAIL_CLOSED_FOR_ARRANGEMENT_TAIL"
        )),
        ("FORGE_SIDE_CLASS", lambda l, r: l["rows"][0]["side_corridors"][0].__setitem__(
            "classification", "PARTIAL_STRICT_COVER__ARRANGEMENT_TAIL_FAIL_CLOSED"
        )),
        ("FORGE_CORRIDOR_ENDPOINT", lambda l, r:
            l["rows"][0]["side_corridors"][0]["accepted_strict_corridors"][0][
                "corridor_rational_outer_box"
            ].__setitem__(0, "0")),
        ("FORGE_CORRIDOR_FOOTPRINT", lambda l, r:
            l["rows"][0]["side_corridors"][0]["accepted_strict_corridors"][0][
                "positive_ps_footprint"
            ].__setitem__(0, "0")),
        ("FORGE_SIGNATURE_DIGEST", lambda l, r:
            l["rows"][0]["side_corridors"][0]["accepted_strict_corridors"][0].__setitem__(
                "complete_10_field_return_signature_sha256", "0" * 64
            )),
        ("ERASE_UNRESOLVED_AREA", lambda l, r: next(
            side for row in l["rows"] for side in row["side_corridors"]
            if Q(side["unresolved_area"]) > 0
        ).__setitem__("unresolved_area", "0")),
        ("PROMOTE_COMPONENT_EDGE", lambda l, r:
            l["rows"][0].__setitem__("cross_chart_component_edge_credit", 1)),
        ("PROMOTE_JX_JY_GLUE", lambda l, r:
            l["rows"][0].__setitem__("Jx_Jy_same_point_glue_credit", 1)),
        ("FORGE_RESOLVED_CENSUS", lambda l, r:
            r["census"].__setitem__("fully_resolved_patch_count", 152)),
        ("FORGE_QUOTIENT", lambda l, r:
            r["strict_nonpromotion"].__setitem__("quotient", 63223)),
        ("FORGE_GO_STATUS", lambda l, r:
            r.__setitem__("status", "PASS_UNCONDITIONAL_CM2_GO")),
    ]
    rejected = []
    for name, mutate in attacks:
        attacked_ledger, attacked_result = deepcopy(ledger), deepcopy(result)
        mutate(attacked_ledger, attacked_result)
        reclose(attacked_ledger, attacked_result)
        try:
            audit_candidate(
                attacked_ledger, attacked_result, expected_rows, expected_census
            )
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected.append(name)
        else:
            raise VerificationError(f"attack accepted:{name}")
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_attacks_rejected": len(rejected) == len(attacks),
        "rejected_attack_ids": rejected,
    }


def verify() -> dict[str, Any]:
    for name, expected in PINS.items():
        need(file_sha(HERE / name) == expected, f"pin:{name}")
    need(PRODUCER.stem not in sys.modules, "producer imported")

    stored_ledger = read_gzip_json(LEDGER)
    stored_result = read_json(RESULT)
    need(gzip_bytes(stored_ledger) == LEDGER.read_bytes(), "deterministic gzip")
    expected_rows, expected_census = reconstruct()
    audit_candidate(stored_ledger, stored_result, expected_rows, expected_census)
    attacks = run_attacks(
        stored_ledger, stored_result, expected_rows, expected_census
    )

    verification = {
        "schema": SCHEMA,
        "status": (
            "PASS_INDEPENDENT_ROUND282_STRICT_TRUE_SEAM_NORMAL_CORRIDOR_PROBE__"
            "24_PATCHES_FAIL_CLOSED__ZERO_CREDIT"
        ),
        "seed_policy": (
            "The verifier is order-deterministic and seed-independent; --seed "
            "is accepted only for cold-replay identity testing."
        ),
        "pins": PINS,
        "producer_imported_or_executed": False,
        "census": expected_census,
        "reconstruction": {
            "verified_patch_row_count": len(expected_rows),
            "verified_directed_side_count": sum(
                len(row["side_corridors"]) for row in expected_rows
            ),
            "whole_outer_corridor_dynamic_signatures_recomputed":
                expected_census["accepted_strict_corridor_candidate_count"],
            "exact_patch_area_union_recomputed_on_every_side": True,
            "algebraic_seam_enclosed_by_independent_128_bit_dyadic_bounds": True,
            "all_24_residual_patches_remain_fail_closed": True,
        },
        "attacks": attacks,
        "strict_nonpromotion": stored_result["strict_nonpromotion"],
    }
    verification["verification_sha256"] = digest(verification)
    return verification


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--seed", default="282071")
    args = parser.parse_args()
    value = verify()
    args.output.write_bytes(canonical(value) + b"\n")


if __name__ == "__main__":
    main()
