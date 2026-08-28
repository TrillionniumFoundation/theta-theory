#!/usr/bin/env python3
"""Independent verifier for Round268 true-seam candidate exhaustion.

The producer is pinned as inert bytes.  This verifier independently rebuilds
the full 13,924-pair pool and expected certificate before opening the
candidate; it never imports or executes the producer.

This round is deliberately geometry-only.  It proves the complete pool of
positive-area same-point cyclic chart overlaps, but awards no component edge
until both incident Round182 closed collars have side-specific exact-key
signatures.  Jx/Jy remain physical symmetries and are never chart transitions.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Iterable


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion"
PRODUCER = HERE / f"{PREFIX}.py"
CANDIDATE = HERE / f"{PREFIX}_certificate.json"
OUTPUT = HERE / f"{PREFIX}_verification.json"
SCHEMA = "cm2.round268.source-g-true-seam-candidate-geometry-exhaustion.v1"
VERIFICATION_SCHEMA = "cm2.round268.source-g-true-seam-candidate-geometry-exhaustion-verification.v1"
PRODUCER_SHA256 = "d79f5e8b360fa494dd44968aa84ea1f108ced1645f05f6024a65e862686db71d"
CANDIDATE_SHA256 = "10d5e42f4353e981e7e8d5aacc002bed119453ee14a13398c524d5cb4ac2f7b9"
CANDIDATE_RESULT_SHA256 = "ce8718d74189e678b7ebc7ac9beeec44305d01091cafcfde012f6bb3a882cf24"
CANDIDATE_SIZE = 157_477

R171 = "cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json"
R174 = "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
R182 = "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
R267 = "cm2_round267_source_g_lower_stratum_terminal_lineage_certificate.json"

PINS = {
    R171: ("1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5", "ffac0e2e16829c1a3ffc4783af2c224288265d02cf53c1d041aaf02013b52957", "cm2.round171.compact-gate3-source-g-coordinate-bridge.v1"),
    R174: ("9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54", "002ca6631edd39c2325c63a1e8f9717d111f4d10c6d2585077d665a0ff128d18", "cm2.round174.source-g-unique-first-dynamic-occurrence-rows.v1"),
    R182: ("ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c", "9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269", "cm2.round182.source-g-clipped-graph-and-pair-arrangement-rows.v1"),
    R267: ("66879215e0250a4a462fea9837c24bccf49a936ce3c5e66da2707e1a66fafc8f", "deaee59586be2f324fbedfe7a97d8ee54b7962f818a3d12ff1d4935d881b0c35", "cm2.round267.source-g-lower-stratum-terminal-lineage.v1"),
}

TRANSITIONS = (
    ("G:E", "+", "G:N", "+", "E:+kappa=N:-kappa"),
    ("G:N", "-", "G:W", "+", "N:+kappa=W:-kappa"),
    ("G:W", "-", "G:S", "-", "W:+kappa=S:-kappa"),
    ("G:S", "+", "G:E", "-", "S:+kappa=E:-kappa"),
)


class Round268Error(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Round268Error(label)


ENCODER = json.JSONEncoder(sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value):
        yield chunk.encode()


def canonical(value: Any) -> bytes:
    return b"".join(chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in chunks(value):
        state.update(chunk)
    return state.hexdigest()


def closed(row: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in row, "unclosed row")
    output = dict(row)
    output["row_sha256"] = digest(output)
    return output


def ledger(rows: list[dict[str, Any]], id_field: str) -> dict[str, Any]:
    need(len(rows) == len({row[id_field] for row in rows}), "unique row ids")
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def regular_bytes(path: Path, maximum: int = 1_200_000_000) -> bytes:
    need(path.parent == HERE, f"input parent:{path.name}")
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and not path.is_symlink() and before.st_nlink == 1 and 0 < before.st_size <= maximum, f"regular input:{path.name}")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
    try:
        opened = os.fstat(fd)
        need((opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns) == (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns), f"stable open:{path.name}")
        parts, total = [], 0
        while True:
            part = os.read(fd, 1024 * 1024)
            if not part:
                break
            total += len(part)
            need(total <= maximum, f"bounded read:{path.name}")
            parts.append(part)
        after = os.fstat(fd)
        need((after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns) == (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns), f"stable read:{path.name}")
        return b"".join(parts)
    finally:
        os.close(fd)


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\0" not in raw, f"encoding:{label}")
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in items:
            need(key not in result, f"duplicate key:{label}:{key}")
            result[key] = value
        return result
    def reject(token: str) -> None:
        raise Round268Error(f"nonintegral JSON:{label}:{token}")
    value = json.loads(raw.decode(), object_pairs_hook=pairs, parse_float=reject, parse_constant=reject)
    need(isinstance(value, dict), f"object:{label}")
    return value


def load(name: str) -> dict[str, Any]:
    file_pin, result_pin, schema = PINS[name]
    raw = regular_bytes(HERE / name)
    need(hashlib.sha256(raw).hexdigest() == file_pin, f"file pin:{name}")
    document = strict_json(raw, name)
    need(set(document) == {"schema", "result", "result_sha256"}, f"envelope:{name}")
    need(document["schema"] == schema and document["result_sha256"] == result_pin and digest(document["result"]) == result_pin, f"result pin:{name}")
    return document["result"]


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = result["row_column_schemas"][table]
    rows = result[table]
    expected = result["table_census_and_sha256"][table]
    need(len(rows) == expected["row_count"] and digest(rows) == expected["rows_sha256"], f"packed table:{table}")
    return [dict(zip(columns, row, strict=True)) for row in rows]


def qtext(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def build(producer_sha256: str) -> dict[str, Any]:
    r171, r174, r182, r267 = load(R171), load(R174), load(R182), load(R267)
    need(r267["census"]["post_Round267_component_count"] == 63_224 and r267["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM", "Round267 baseline")
    seam_contract = r171["exact_source_G_coordinate_bridge"]["seam_rows"]
    need(len(seam_contract) == 4 and all(row["normal_glues_exactly"] and row["quarter_turn_and_velocity_glue_for_every_q"] and row["source_G_position_glues_exactly"] for row in seam_contract), "Round171 exact seams")

    residuals = {row["row_id"]: row for row in unpack(r174, "residual_3d_tube_rows")}
    seam_rows = unpack(r182, "source_chart_seam_owner_rows")
    need(len(seam_rows) == 472, "complete Round182 seam rows")
    classified: list[dict[str, Any]] = []
    for row in seam_rows:
        need(row["origin_row_id"] in residuals and row["equation"] == "2*t^2-1=0" and row["exact_dimension"] == 2, "seam identity")
        need(row["lower_t_face_sign"] != row["upper_t_face_sign"] and row["strict_t_derivative_sign"] in {"STRICT_POSITIVE", "STRICT_NEGATIVE"}, "seam root isolation")
        box = tuple(Fraction(value) for value in residuals[row["origin_row_id"]]["box"])
        root = "+" if row["strict_t_derivative_sign"] == "STRICT_POSITIVE" else "-"
        classified.append({"row": row, "box": box, "root": root})
    need(Counter((item["row"]["chart"], item["root"]) for item in classified) == Counter({(chart, root): 59 for chart in ("G:E", "G:N", "G:W", "G:S") for root in ("+", "-")}), "chart/root census")

    patches: list[dict[str, Any]] = []
    pair_histogram: Counter[str] = Counter()
    tested = 0
    for left_chart, left_root, right_chart, right_root, identity in TRANSITIONS:
        left = [item for item in classified if item["row"]["chart"] == left_chart and item["root"] == left_root]
        right = [item for item in classified if item["row"]["chart"] == right_chart and item["root"] == right_root]
        need(len(left) == len(right) == 59, f"transition pool:{identity}")
        for a in left:
            for b in right:
                tested += 1
                plo, phi = max(a["box"][2], b["box"][2]), min(a["box"][3], b["box"][3])
                slo, shi = max(a["box"][4], b["box"][4]), min(a["box"][5], b["box"][5])
                if not (plo < phi and slo < shi):
                    continue
                need(a["row"]["is_half_open_owner"] != b["row"]["is_half_open_owner"], "owner/shadow pair")
                area = (phi - plo) * (shi - slo)
                descriptor = [a["row"]["row_id"], b["row"]["row_id"], qtext(plo), qtext(phi), qtext(slo), qtext(shi)]
                patches.append(closed({
                    "true_seam_patch_row_id": "round268-true-seam-patch:" + digest(descriptor),
                    "left_Round182_source_seam_row_id": a["row"]["row_id"],
                    "right_Round182_source_seam_row_id": b["row"]["row_id"],
                    "cyclic_transition_identity": identity,
                    "left_chart": left_chart,
                    "left_local_t_root": left_root,
                    "right_chart": right_chart,
                    "right_local_t_root": right_root,
                    "exact_common_p_interval": [qtext(plo), qtext(phi)],
                    "exact_common_s_interval": [qtext(slo), qtext(shi)],
                    "exact_positive_common_area": qtext(area),
                    "same_physical_source_point": True,
                    "Round171_normal_position_velocity_identity": True,
                    "owner_shadow_half_open_pair": True,
                    "side_specific_exact_key_signatures_available": False,
                    "component_edge_credit": 0,
                    "maximality_credit": 0,
                    "global_exact_key_disposition_credit": 0,
                    "Jx_Jy_same_point_glue_credit": 0,
                }))
                pair_histogram[f"{left_chart}|{right_chart}"] += 1
    patches.sort(key=lambda row: row["true_seam_patch_row_id"])
    need(tested == 13_924 and len(patches) == 152 and pair_histogram == Counter({"G:E|G:N": 38, "G:N|G:W": 38, "G:W|G:S": 38, "G:S|G:E": 38}), "complete candidate census")
    area_sum = sum((Fraction(row["exact_positive_common_area"]) for row in patches), Fraction())
    need(area_sum == Fraction(1, 80), "exact area sum")

    return {
        "status": "CERTIFIED_COMPLETE_ROUND182_TRUE_SOURCE_SEAM_GEOMETRY_EXHAUSTION__152_POSITIVE_AREA_OWNER_SHADOW_PATCHES__13772_EXACT_EMPTY_PAIRS__ZERO_PREMATURE_COMPONENT_CREDIT",
        "census": {
            "Round182_source_seam_row_count": 472,
            "source_chart_root_bucket_count": 8,
            "source_chart_root_bucket_size": 59,
            "cyclic_true_seam_transition_count": 4,
            "complete_candidate_pair_count": tested,
            "strict_positive_area_same_point_patch_count": len(patches),
            "exact_empty_p_or_s_overlap_pair_count": tested - len(patches),
            "transition_positive_patch_histogram": dict(sorted(pair_histogram.items())),
            "exact_positive_common_area_sum": qtext(area_sum),
            "side_specific_signature_ready_patch_count": 0,
            "new_component_edge_credit": 0,
            "post_Round268_component_count": 63_224,
            "expanded_occurrence_frontier_count": 126_468,
            "exact_key_frontier_count": 116,
            "valid_virtual_node_frontier_count": 133_284,
            "maximal_component_assignment_count": 0,
            "globally_exhausted_exact_key_fibre_count": 0,
            "global_exact_key_disposition_count": 0,
        },
        "formal_true_source_seam_positive_patch_ledger": ledger(patches, "true_seam_patch_row_id"),
        "scope_contract": {
            "all_13924_cyclic_adjacent_chart_pairs_exhausted": True,
            "all_152_positive_patches_are_true_same_point_source_chart_transitions": True,
            "all_13772_other_pairs_have_exact_empty_p_or_s_overlap": True,
            "Round171_exact_normal_position_and_velocity_seam_identity_pinned": True,
            "Jx_Jy_are_physical_symmetries_not_same_point_chart_transitions": True,
            "geometry_without_side_specific_signatures_is_not_component_glue": True,
            "Round267_quotient_and_frontier_counts_preserved": True,
        },
        "strict_nonpromotion": {
            "new_physical_glue_credit": 0,
            "new_component_union_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED",
            "Gate5_filled_field_slot_count": 10,
            "Gate5_total_field_slot_count": 18,
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": "materialize side-specific exact-key return signatures on all 184,452 Round182 closed collar leaves, attach each of the 152 frozen true-seam patches to its two incident signed components, reverse-rechart all 880 positive-volume chart guards, then continue maximality and 116-fibre exhaustion",
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_version": sys.version.split()[0],
            "exact_arithmetic": "fractions.Fraction",
            "upstream_producer_imported_or_executed": False,
            "seed_affects_output": False,
        },
    }


def safe_write(data: bytes) -> None:
    if OUTPUT.exists() or OUTPUT.is_symlink():
        info = OUTPUT.lstat()
        need(stat.S_ISREG(info.st_mode) and not OUTPUT.is_symlink() and info.st_nlink == 1, "safe output")
    fd, name = tempfile.mkstemp(prefix=f".{OUTPUT.name}.", suffix=".tmp", dir=HERE)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data); handle.flush(); os.fsync(handle.fileno())
        os.replace(temporary, OUTPUT)
    finally:
        if temporary.exists(): temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=268_929)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    need(isinstance(args.seed, int) and not isinstance(args.seed, bool), "seed")
    need(hashlib.sha256(regular_bytes(PRODUCER, 5_000_000)).hexdigest() == PRODUCER_SHA256, "producer pin")
    expected = build(PRODUCER_SHA256)
    need(digest(expected) == CANDIDATE_RESULT_SHA256, "expected result pin")
    raw = regular_bytes(CANDIDATE, 5_000_000)
    need(len(raw) == CANDIDATE_SIZE and hashlib.sha256(raw).hexdigest() == CANDIDATE_SHA256, "candidate byte pin")
    candidate = strict_json(raw, CANDIDATE.name)
    need(set(candidate) == {"schema", "result", "result_sha256"} and candidate["schema"] == SCHEMA, "candidate envelope")
    need(candidate["result_sha256"] == CANDIDATE_RESULT_SHA256 and digest(candidate["result"]) == CANDIDATE_RESULT_SHA256, "candidate closure")
    need(candidate["result"] == expected, "complete expected equality")
    attacks = [
        ("positive_count", "strict_positive_area_same_point_patch_count", 151),
        ("empty_count", "exact_empty_p_or_s_overlap_pair_count", 13771),
        ("pair_count", "complete_candidate_pair_count", 13923),
        ("area", "exact_positive_common_area_sum", "0"),
        ("edge_credit", "new_component_edge_credit", 1),
        ("maximality", "maximal_component_assignment_count", 1),
        ("fibre", "globally_exhausted_exact_key_fibre_count", 1),
        ("disposition", "global_exact_key_disposition_count", 1),
    ]
    rejected = []
    for label, key, replacement in attacks:
        original = candidate["result"]["census"][key]
        candidate["result"]["census"][key] = replacement
        need(candidate["result"] != expected, f"attack rejected:{label}")
        candidate["result"]["census"][key] = original
        need(candidate["result"] == expected, f"attack restored:{label}")
        rejected.append(label)
    for label, key, replacement in [("jx_jy", "Jx_Jy_same_point_glue_credit", 1), ("cm2", "CM2", "GO_FOR_CLAIM")]:
        original = candidate["result"]["strict_nonpromotion"][key]
        candidate["result"]["strict_nonpromotion"][key] = replacement
        need(candidate["result"] != expected, f"attack rejected:{label}")
        candidate["result"]["strict_nonpromotion"][key] = original
        rejected.append(label)
    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status": "PASS_INDEPENDENT_ROUND268",
        "producer_sha256": PRODUCER_SHA256,
        "candidate_sha256": CANDIDATE_SHA256,
        "candidate_result_sha256": CANDIDATE_RESULT_SHA256,
        "independent_reconstruction": {"producer_imported_or_executed": False, "complete_candidate_pair_count": 13_924, "positive_patch_count": 152, "exact_empty_pair_count": 13_772, "exact_area_sum": "1/80", "seed_affects_output": False},
        "semantic_attack_suite": {"attack_count": len(rejected), "rejected_count": len(rejected), "attack_labels": rejected},
        "strict_nonpromotion": expected["strict_nonpromotion"],
    }
    encoded = canonical(verification) + b"\n"
    if not args.no_write: safe_write(encoded)
    print(verification["status"])
    print(f"verification_sha256={hashlib.sha256(encoded).hexdigest()}")
    print(f"attacks_rejected={len(rejected)}/{len(rejected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
