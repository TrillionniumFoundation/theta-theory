#!/usr/bin/env python3
"""Independently verify the Round226 chart-transition frontier census.

This package materializes contracts, not physical glues.  Same-chart rows get
the identity coordinate contract; cross-chart rows remain fail-closed unless
an exact transformed-face and event-trace restriction is subsequently proved.
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
PREFIX = "cm2_round226_source_g_chart_transition_contract_census"
OUTPUT = HERE / f"{PREFIX}_verification.json"
SCHEMA = "cm2.round226.source-g-chart-transition-contract-census.v1"
VERIFICATION_SCHEMA = f"{SCHEMA}.verification.v1"
CANDIDATE = f"{PREFIX}_certificate.json"
CANDIDATE_SHA256 = "226e1f350c53fe4d7357ba9a74850e21d5aee5d720c0ea714c460181a6c797e8"
CANDIDATE_RESULT_SHA256 = "8c2a8f0393b4d3d5b4b103e670e2e76b8c1a41f239c0cdc9f35c21ffc90bb088"
PRODUCER = f"{PREFIX}.py"
PRODUCER_SHA256 = "f39e37f410d586a7589ba942b4846b164f38ac06b447b63cf5be9db2f96ac457"
R220 = "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json"
R220_SHA256 = "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"
R220_RESULT_SHA256 = "4d8168cb25bd389f16b332798fcf9b57951deedd8d328bc5a1dac9024508669b"
R173 = "cm2_round173_source_g_exact_return_signature_transport_certificate.json"
R173_SHA256 = "5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a"
R173_RESULT_SHA256 = "948ab0a8539b08adc96c9493de415b44a5ffb75a1ee3ef47a4742902c211c11f"
CHARTS = ("G:E", "G:N", "G:S", "G:W")


class VerificationError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


ENCODER = json.JSONEncoder(sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value):
        yield chunk.encode()


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in chunks(value):
        state.update(chunk)
    return state.hexdigest()


def canonical(value: Any) -> bytes:
    return b"".join(chunks(value))


def closed(value: dict[str, Any]) -> dict[str, Any]:
    row = dict(value)
    row["row_sha256"] = digest(row)
    return row


def table(rows: list[dict[str, Any]], id_key: str) -> dict[str, Any]:
    need(len({row[id_key] for row in rows}) == len(rows), f"unique {id_key}")
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_key] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def regular_bytes(path: Path, maximum: int) -> bytes:
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and not path.is_symlink() and before.st_nlink == 1, f"regular:{path.name}")
    need(0 < before.st_size <= maximum, f"bounded:{path.name}")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
    try:
        opened = os.fstat(descriptor)
        need((opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns) == (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns), f"stable open:{path.name}")
        parts: list[bytes] = []
        size = 0
        while True:
            part = os.read(descriptor, 1024 * 1024)
            if not part:
                break
            size += len(part)
            need(size <= maximum, f"bounded read:{path.name}")
            parts.append(part)
        after = os.fstat(descriptor)
        need((after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns) == (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns), f"stable read:{path.name}")
        return b"".join(parts)
    finally:
        os.close(descriptor)


def strict_json(raw: bytes) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, f"duplicate key:{key}")
            result[key] = value
        return result
    def reject(token: str) -> None:
        raise VerificationError(f"non-integral number:{token}")
    result = json.loads(raw, object_pairs_hook=pairs, parse_float=reject, parse_constant=reject)
    need(isinstance(result, dict), "JSON object")
    try:
        canonical(result).decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError) as error:
        raise VerificationError("invalid Unicode") from error
    return result


def unpack(value: dict[str, Any]) -> list[dict[str, Any]]:
    columns = value["columns"]
    rows = [dict(zip(columns, row, strict=True)) for row in value["rows"]]
    need(value["row_count"] == len(rows), "table count")
    return rows


def transition_kind(source: str, destination: str) -> str:
    if source == destination:
        return "IDENTITY"
    jx = {"G:E": "G:W", "G:W": "G:E", "G:N": "G:N", "G:S": "G:S"}
    jy = {"G:E": "G:E", "G:W": "G:W", "G:N": "G:S", "G:S": "G:N"}
    if jx[source] == destination:
        return "Jx"
    if jy[source] == destination:
        return "Jy"
    if jx[jy[source]] == destination:
        return "JxJy"
    return "NO_PINNED_KLEIN_GENERATOR"


def face_region(face: dict[str, Any]) -> dict[str, tuple[Fraction, Fraction]]:
    region = {face["axis"]: (Fraction(face["fixed_coordinate"]), Fraction(face["fixed_coordinate"]))}
    box = face["tangential_half_open_box"]
    for index, axis in enumerate(face["tangential_axes"]):
        region[axis] = (Fraction(box[2 * index]), Fraction(box[2 * index + 1]))
    return region


def negate_interval(value: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return (-value[1], -value[0])


def transformed_region(source: str, destination: str, face: dict[str, Any]) -> dict[str, tuple[Fraction, Fraction]] | None:
    region = face_region(face)
    kind = transition_kind(source, destination)
    if kind == "IDENTITY":
        return region
    if kind == "Jx":
        region["p"] = negate_interval(region["p"])
        region["s"] = negate_interval(region["s"])
        return region
    if kind == "Jy":
        region["p"] = negate_interval(region["p"])
        return region
    if kind == "JxJy":
        region["s"] = negate_interval(region["s"])
        return region
    return None


def build(producer_sha256: str) -> dict[str, Any]:
    raw173 = regular_bytes(HERE / R173, 200_000_000)
    need(hashlib.sha256(raw173).hexdigest() == R173_SHA256, "Round173 file pin")
    envelope173 = strict_json(raw173)
    need(envelope173["result_sha256"] == R173_RESULT_SHA256 and digest(envelope173["result"]) == R173_RESULT_SHA256, "Round173 result pin")
    generators = {row["generator"]: row for row in envelope173["result"]["exact_transport_generators"]}
    need(generators["Jx"]["source_chart_dictionary"] == {"G:E": "G:W", "G:N": "G:N", "G:S": "G:S", "G:W": "G:E"}, "Jx chart map")
    need(generators["Jy"]["source_chart_dictionary"] == {"G:E": "G:E", "G:N": "G:S", "G:S": "G:N", "G:W": "G:W"}, "Jy chart map")
    need(generators["Jx"]["Gate3_parameter_map"]["p"] == "-p" and generators["Jx"]["Gate3_parameter_map"]["s"] == "-s", "Jx parameter map")
    need(generators["Jy"]["Gate3_parameter_map"]["p"] == "-p" and generators["Jy"]["Gate3_parameter_map"]["s"] == "s", "Jy parameter map")
    raw = regular_bytes(HERE / R220, 400_000_000)
    need(hashlib.sha256(raw).hexdigest() == R220_SHA256, "Round220 file pin")
    envelope = strict_json(raw)
    need(envelope["result_sha256"] == R220_RESULT_SHA256 and digest(envelope["result"]) == R220_RESULT_SHA256, "Round220 result pin")
    tables = envelope["result"]["coordinate_boundary_atlas"]["tables"]
    rejected = unpack(tables["rejected_exact_coordinate_coincidence_rows"])
    faces = {row["face_id"]: row for row in unpack(tables["coordinate_face_rows"])}
    children = dict(enumerate(unpack(tables["resolved_child_rows"])))
    need(len(rejected) == 9_830 and len(faces) == 103_152 and len(children) == 17_192, "Round220 census")

    pair_counts = Counter((row["negative_chart"], row["positive_chart"]) for row in rejected)
    transformed_matches = Counter()
    for row in rejected:
        transformed = transformed_region(row["negative_chart"], row["positive_chart"], faces[row["negative_side_face_id"]])
        if transformed is not None and transformed == face_region(faces[row["positive_side_face_id"]]):
            transformed_matches[(row["negative_chart"], row["positive_chart"])] += 1
    contracts: list[dict[str, Any]] = []
    for source in CHARTS:
        for destination in CHARTS:
            kind = transition_kind(source, destination)
            count = pair_counts[(source, destination)]
            contracts.append(closed({
                "transition_contract_id": f"round226-chart-contract:{source}->{destination}",
                "source_chart": source,
                "destination_chart": destination,
                "candidate_count": count,
                "coordinate_transform_kind": kind,
                "coordinate_transform_formula_materialized": kind == "IDENTITY",
                "transformed_face_equality_proved_candidate_count": transformed_matches[(source, destination)],
                "event_trace_restriction_proved": False,
                "Round211_sheet_pair_mapped": False,
                "physical_glue_credit": 0,
                "component_credit": 0,
            }))

    candidates: list[dict[str, Any]] = []
    identity = pinned_generator = no_generator = transformed_cross_chart = 0
    for source in rejected:
        negative_face = faces[source["negative_side_face_id"]]
        positive_face = faces[source["positive_side_face_id"]]
        negative_child = children[negative_face["child_ordinal"]]
        positive_child = children[positive_face["child_ordinal"]]
        need(negative_face["event_sheet_incidence_count"] == 0 and positive_face["event_sheet_incidence_count"] == 0, "candidate face event-sheet absence")
        need(negative_child["event_sheet_incidence_count"] == 0 and positive_child["event_sheet_incidence_count"] == 0, "candidate child event-sheet absence")
        need(negative_face["coordinate_stratum_only"] is True and positive_face["coordinate_stratum_only"] is True, "coordinate-only candidate faces")
        kind = transition_kind(source["negative_chart"], source["positive_chart"])
        identity_contract = kind == "IDENTITY"
        transformed = transformed_region(source["negative_chart"], source["positive_chart"], negative_face)
        transformed_equal = transformed is not None and transformed == face_region(positive_face)
        identity += identity_contract
        pinned_generator += kind in {"Jx", "Jy", "JxJy"}
        no_generator += kind == "NO_PINNED_KLEIN_GENERATOR"
        transformed_cross_chart += transformed_equal and not identity_contract
        if identity_contract:
            disposition = "IDENTITY_REGION__TRACE_AND_SHEET_MAPPING_OPEN"
        elif transformed_equal:
            disposition = "TRANSFORMED_REGION_EQUAL__TRACE_AND_SHEET_MAPPING_OPEN"
        elif kind in {"Jx", "Jy", "JxJy"}:
            disposition = "PINNED_TRANSFORM_APPLIED__REGIONS_NOT_EQUAL"
        else:
            disposition = "TRANSFORM_NOT_MATERIALIZED"
        candidates.append(closed({
            "transformed_face_candidate_id": f"round226-transformed-face:{source['candidate_id'].split(':', 1)[1]}",
            "Round220_candidate_id": source["candidate_id"],
            "transition_contract_id": f"round226-chart-contract:{source['negative_chart']}->{source['positive_chart']}",
            "negative_face_id": source["negative_side_face_id"],
            "positive_face_id": source["positive_side_face_id"],
            "negative_child_ordinal": negative_face["child_ordinal"],
            "positive_child_ordinal": positive_face["child_ordinal"],
            "negative_official_key_id": negative_child["official_key_id"],
            "positive_official_key_id": positive_child["official_key_id"],
            "same_official_key": source["same_official_key"],
            "coordinate_transform_kind": kind,
            "coordinate_region_identity_proved": transformed_equal,
            "event_trace_restriction_proved": False,
            "event_trace_absence_proved_on_both_resolved_child_faces": True,
            "Round211_sheet_pair_mapped": False,
            "Round211_sheet_pair_mapping_disposition": "NOT_APPLICABLE__NO_EVENT_SHEET_ENDPOINT",
            "candidate_disposition": disposition,
            "physical_glue_credit": 0,
            "component_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
    need(identity == 328 and pinned_generator == 276 and no_generator == 9_226 and transformed_cross_chart == 16, "transition-kind split")
    need(sum(pair_counts.values()) == 9_830 and len(pair_counts) == 16, "16-contract exhaustion")

    return {
        "status": "COMPLETE_16_CONTRACT_AND_9830_CANDIDATE_CENSUS__TRANSITION_GLUE_STILL_OPEN",
        "formal_input_binding": {
            "Round173_certificate_sha256": R173_SHA256,
            "Round173_result_sha256": R173_RESULT_SHA256,
            "Round220_certificate_sha256": R220_SHA256,
            "Round220_result_sha256": R220_RESULT_SHA256,
        },
        "chart_transition_contract_ledger": table(contracts, "transition_contract_id"),
        "transformed_face_candidate_ledger": table(candidates, "transformed_face_candidate_id"),
        "census": {
            "chart_transition_contract_count": 16,
            "transformed_face_candidate_count": 9_830,
            "same_chart_identity_region_count": 328,
            "cross_chart_pinned_Klein_generator_available_count": 276,
            "cross_chart_no_pinned_generator_count": 9_226,
            "cross_chart_transformed_face_equality_proved_count": 16,
            "cross_chart_pinned_transform_region_mismatch_count": 260,
            "all_coordinate_region_identity_candidate_count": 344,
            "event_trace_restriction_proved_count": 0,
            "Round211_sheet_pair_mapped_count": 0,
            "Round211_sheet_pair_mapping_not_applicable_no_endpoint_count": 9_830,
            "both_endpoint_faces_coordinate_stratum_only_count": 9_830,
            "both_endpoint_faces_event_sheet_incidence_zero_count": 9_830,
            "event_trace_candidate_absence_proved_within_Round220_rejected_pool_count": 9_830,
            "coordinate_region_identity_candidates_remaining_eligible_for_event_trace_glue": 0,
            "physical_glue_credit_count": 0,
        },
        "strict_nonpromotion": {
            "known_connectivity_blocks": 7_404,
            "known_connectivity_blocks_are_maximal_physical_components": False,
            "component_credit": 0,
            "whole_origin_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": "the complete Round220 rejected-coordinate pool is now excluded from event-trace glue because all 9830 endpoint faces are coordinate-only with zero event-sheet incidence; construct an independent transformed-face census from retained/event-sheet-bearing strata rather than recycling this rejected resolved-child pool",
        "provenance": {"schema": SCHEMA, "producer_sha256": producer_sha256, "python_version": sys.version.split()[0], "upstream_modified": False},
    }


def safe_write(path: Path, data: bytes) -> None:
    absolute = Path(os.path.abspath(path))
    need(absolute.parent == HERE and absolute.name == OUTPUT.name, "output allowlist")
    descriptor, name = tempfile.mkstemp(prefix=f".{OUTPUT.name}.", suffix=".tmp", dir=HERE)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, absolute)
    finally:
        if temporary.exists():
            temporary.unlink()


def candidate_accepts(candidate: dict[str, Any], expected: dict[str, Any]) -> bool:
    try:
        need(set(candidate) == {"schema", "result", "result_sha256"}, "candidate envelope")
        need(candidate["schema"] == SCHEMA, "candidate schema")
        need(candidate["result_sha256"] == digest(candidate["result"]), "candidate closure")
        need(candidate["result_sha256"] == CANDIDATE_RESULT_SHA256, "candidate result pin")
        need(candidate["result"] == expected, "full semantic equality")
        return True
    except (VerificationError, KeyError, TypeError):
        return False


def semantic_attacks(candidate: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    paths = [
        ("census", "chart_transition_contract_count"),
        ("census", "transformed_face_candidate_count"),
        ("census", "same_chart_identity_region_count"),
        ("census", "cross_chart_transformed_face_equality_proved_count"),
        ("census", "cross_chart_pinned_transform_region_mismatch_count"),
        ("census", "cross_chart_no_pinned_generator_count"),
        ("census", "event_trace_candidate_absence_proved_within_Round220_rejected_pool_count"),
        ("census", "coordinate_region_identity_candidates_remaining_eligible_for_event_trace_glue"),
        ("strict_nonpromotion", "component_credit"),
        ("strict_nonpromotion", "global_exact_key_disposition_credit"),
        ("strict_nonpromotion", "D02"),
        ("strict_nonpromotion", "CM2"),
    ]
    rejected = 0
    for outer, inner in paths:
        original = candidate["result"][outer][inner]
        candidate["result"][outer][inner] = original + 1 if isinstance(original, int) and not isinstance(original, bool) else f"FORGED::{original}"
        candidate["result_sha256"] = digest(candidate["result"])
        rejected += not candidate_accepts(candidate, expected)
        candidate["result"][outer][inner] = original
        candidate["result_sha256"] = digest(candidate["result"])
    need(rejected == len(paths), "semantic attacks")
    return {"attempted": len(paths), "rejected": rejected, "all_resigned": True}


def json_attacks() -> dict[str, Any]:
    cases = [
        b'{"a":1,"a":2}', b'{"a":1.0}', b'{"a":NaN}', b'{"a":Infinity}',
        b'{"a":-Infinity}', b'[]', b'null', b'true', b'{"a":1} trailing',
        b'{"a":01}', b'{"a":1e0}', b'{"a":0.0}', b'{"a":"\\ud800"}',
        b'{"a":"\\udfff"}', b'{"a":}', b'{"a":1,}',
    ]
    rejected = 0
    for raw in cases:
        try:
            strict_json(raw)
        except (VerificationError, json.JSONDecodeError, UnicodeError):
            rejected += 1
    need(rejected == len(cases), "JSON attacks")
    return {"attempted": len(cases), "rejected": rejected}


def file_attacks() -> dict[str, Any]:
    rejected = 0
    attempted = 0
    def reject(action: Any) -> None:
        nonlocal rejected, attempted
        attempted += 1
        try:
            action()
        except (VerificationError, FileNotFoundError, IsADirectoryError):
            rejected += 1
    with tempfile.TemporaryDirectory(prefix=".round226-attacks-", dir=HERE) as directory:
        root = Path(directory)
        regular = root / "regular"; regular.write_bytes(b"abcd")
        symlink = root / "symlink"; symlink.symlink_to(regular)
        hardlink = root / "hardlink"; os.link(regular, hardlink)
        fifo = root / "fifo"; os.mkfifo(fifo)
        empty = root / "empty"; empty.touch()
        reject(lambda: regular_bytes(symlink, 10))
        reject(lambda: regular_bytes(hardlink, 10))
        reject(lambda: regular_bytes(fifo, 10))
        reject(lambda: regular_bytes(root, 10))
        reject(lambda: regular_bytes(root / "missing", 10))
        reject(lambda: regular_bytes(empty, 10))
        reject(lambda: regular_bytes(regular, 3))
        reject(lambda: safe_write(HERE / CANDIDATE, b"x"))
    need(rejected == attempted == 8, "file attacks")
    return {"attempted": attempted, "rejected": rejected}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    need(hashlib.sha256(regular_bytes(HERE / PRODUCER, 5_000_000)).hexdigest() == PRODUCER_SHA256, "producer pin")
    candidate_raw = regular_bytes(HERE / CANDIDATE, 100_000_000)
    need(hashlib.sha256(candidate_raw).hexdigest() == CANDIDATE_SHA256, "candidate file pin")
    candidate = strict_json(candidate_raw)
    expected = build(PRODUCER_SHA256)
    need(candidate_accepts(candidate, expected), "candidate semantics")
    semantic = semantic_attacks(candidate, expected)
    json_suite = json_attacks()
    file_suite = file_attacks()
    verifier_sha256 = hashlib.sha256(regular_bytes(Path(__file__), 5_000_000)).hexdigest()
    result = {
        "status": "PASS_PARTIAL_FORMAL_ROUND226",
        "candidate_file_sha256": CANDIDATE_SHA256,
        "candidate_result_sha256": CANDIDATE_RESULT_SHA256,
        "producer_sha256": PRODUCER_SHA256,
        "verifier_sha256": verifier_sha256,
        "producer_imported_or_executed": False,
        "independent_reconstruction": {
            "contracts": 16, "candidates": 9830, "same_chart_identity": 328,
            "transformed_cross_chart_equal": 16, "pinned_transform_mismatch": 260,
            "no_pinned_generator": 9226, "coordinate_only_no_event_sheet_endpoints": 9830,
            "event_trace_glue_eligible_from_this_pool": 0,
        },
        "attack_suite": {"resigned_semantic": semantic, "strict_JSON": json_suite, "path_and_file": file_suite},
        "strict_nonpromotion_reconfirmed": expected["strict_nonpromotion"],
    }
    envelope = {"schema": VERIFICATION_SCHEMA, "result": result, "result_sha256": digest(result)}
    encoded = canonical(envelope) + b"\n"
    if not arguments.no_write:
        safe_write(OUTPUT, encoded)
    print(result["status"])
    print(f"result_sha256={envelope['result_sha256']}")
    print(f"verification_sha256={hashlib.sha256(encoded).hexdigest()}")
    print("semantic_attacks=12/12_rejected strict_JSON=16/16_rejected file_attacks=8/8_rejected")
    print("contracts=16 candidates=9830 coordinate_only_no_event_sheet_endpoints=9830")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
