#!/usr/bin/env python3
"""Independent verifier for the Round131 fail-closed typed crosswalk.

This verifier never imports or executes the Round131 producer.  It rebuilds
the 24 physical cores and the four-way Round71/72/128 component join from the
frozen witnesses, replays the Round28/Round67/Round69 carrier obstruction,
reconstructs all 53 closed Round131 rows, and rejects semantic and strict-JSON
mutations.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import stat
import tempfile
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = HERE / "cm2_round131_round67_r1_typed_incidence_crosswalk.py"
CERTIFICATE = (
    HERE
    / "cm2-round131-round67-r1-typed-incidence-crosswalk-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round131-round67-r1-typed-incidence-crosswalk-verification-2026-07-24.json"
)

CERTIFICATE_SCHEMA = "cm2.round131.round67-r1-typed-incidence-crosswalk.v1"
VERIFICATION_SCHEMA = (
    "cm2.round131.round67-r1-typed-incidence-crosswalk-verification.v1"
)
PRODUCER_SHA256 = (
    "8e7b2bae965be128a288ae38768bf746f5c33c0744449f8edea48014bd22d611"
)
CERTIFICATE_SHA256 = (
    "a8e4b9dabb30396469f28d4df252c9f5de1d9d1620c0a18d252ef23a12f1f3d6"
)
CERTIFICATE_RESULT_SHA256 = (
    "0fd7f419d5a0afa3fbc20db3757803ee5c2982b4428ba52a97798a6fcc28a0ab"
)

R67P = "cm2_round67_fixed_j_occurrence_owner_root_time_potential_frontier_cert.py"
R67 = (
    "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-"
    "manifest-2026-07-21.json"
)
R28P = "cm2_gate5_round28_limiting_physical_face_atlas_frontier_cert.py"
R28 = "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json"
R69 = "cm2-round69-base-s-return-incidence-all-gate-manifest-2026-07-21.json"
R71P = "cm2_round71_r1_nonempty_face_germs_cert.py"
R71W = "cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json"
R71 = "cm2-round71-r1-nonempty-face-germs-manifest-2026-07-21.json"
R72P = "cm2_round72_r1_full_atlas_f10_f13_f16_cert.py"
R72F = "cm2-round72-r1-component-f10-f13-f16-proof-2026-07-21.json"
R72 = "cm2-round72-r1-full-atlas-f10-f13-f16-manifest-2026-07-21.json"
R128P = "cm2_round128_base_r1_component_global_word_incidence.py"
R128 = "cm2-round128-base-r1-component-global-word-incidence-2026-07-24.json"
R128V = "cm2_round128_base_r1_component_global_word_incidence_verifier.py"
R128A = (
    "cm2-round128-base-r1-component-global-word-incidence-verification-"
    "2026-07-24.json"
)

BYTE_PINS = {
    R67P: "cfb501aff4f321742e3fead9895c596e9105b2a89d064d917646b70c6f91ee8f",
    R67: "97cb410b9e960d8331a37ef9203b040c9b1d86c3ed3d1ba6ba66a28c4e4ff400",
    R28P: "b0dda23ec7e8c9dbe82aff861be6b4e1d38ecf281a82165949537b923150ba27",
    R28: "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140",
    R69: "08d996d52d6aa8ea3b716a46b51d6ae8f0a6b4b9e24c9fab402afe88059bc838",
    R71P: "ec5b229a7a624ca37f93884d938e26a5e946ff4254edf24cd9a7e7d98d8c6c72",
    R71W: "3226044b8d0718a0d565c7ff9dd6c4736d2b1d28fa784c46443da92e85b61cc6",
    R71: "fb7fd4233d14834ca6a3efc488c2e8f1fcdf97bdeb410a1b93eda8d9b59d50f9",
    R72P: "bf0a9ced0b66174b100dfe195666312215ce9a873558c48787669e0f77da04f9",
    R72F: "12c1f1db87030cf63552621a24ac0ebb1adb39933dc420497b425fb3c1f8e8a9",
    R72: "4bb012ae54db337cbdaa8cdc02aee55025dd522ccc566a7fb343b57010d4f6f9",
    R128P: "d218d92a6aa7a929e734c86110e67ec8ebea75b3c57bf74e5a7d3b3e33d32e35",
    R128: "7c5f513ba9bac5c5381e5504870b783159ebbb622ca155f649429cb65ad7b10e",
    R128V: "2745ccccdab9869c4754bab37f13ece70f32c7b59063bf0aed4f59cdd81af544",
    R128A: "3798cb3e38b7f26de0a5361234d57ef626bd7f990e26d6c787f0abf62647a76d",
}

SCHEMA_PINS = {
    R67: "cm2.round67.fixed-j-occurrence-owner-root-time-potential.v1.manifest.v1",
    R28: "cm2.gate5.round28-limiting-physical-face-atlas-frontier.manifest.v3",
    R69: "cm2.round69.base-s-return-incidence-all-gate.v1.manifest.v1",
    R71W: "cm2.round71.r1-nonempty-face-witnesses.v1",
    R71: "cm2.round71.r1-nonempty-face-germs.v1.manifest.v1",
    R72F: "cm2.round72.r1-component-f10-f13-f16.v1",
    R72: "cm2.round72.r1-full-atlas-f10-f13-f16.v1.manifest.v1",
    R128: "cm2.round128.base-r1-component-global-word-incidence.v1",
    R128A: "cm2.round128.base-r1-component-global-word-incidence-verification.v1",
}

CANONICAL_PINS = {
    R67: ("result", "c1fd3e486d671b83c6ae6a0c6da8c4d50bd2796842cfe1c8d8d5985001e5a57f"),
    R28: ("result", "282d73b9146a38ff41f78ab6d0fd619c1b955eda32ed3dd5cdae2fd170b340b6"),
    R69: ("result", "8cac8aead2506fddd6c8e9ee0941d3f46a06d390c7913cc3deca42812810e5c7"),
    R71W: ("document", "519e22b33df9aab7e8ea39b1aff45c3c03eb1d06223259dec0774ec87d70b849"),
    R71: ("result", "59a66d6206619d8195b6bc2ccd60d85f90b9a9a581764f7160902eeec3b95107"),
    R72F: ("result", "d48f78a39d51ebafe17e0288d7d2ba9f3d8127bab09b45749dc62e1c1bde94ad"),
    R72: ("result", "055725862200741853145ed70c2176e807dba675a7f1a2f17e827765e07e740b"),
    R128: ("result", "46601ee43c7ca8051dac51fd608605a814abfb755092ea8225fd3f0f2c755815"),
    R128A: ("result", "2037fb4ad60901824b9a107e51b6092f761dcb9b2d47da1c2f76e2cb06926b45"),
}

REQUIRED_FIELDS = [
    "restriction_id",
    "return_component",
    "insertion_time",
    "collision_index",
    "event_signature",
    "primitive_key",
    "owner_key",
    "rank_zero_component",
    "plaque_side",
    "word_cell",
    "endpoint_coordinate",
    "root_coordinate",
]

EVIDENCE_BY_FIELD = {
    "restriction_id": [],
    "return_component": ["component_id", "path_cell_id"],
    "insertion_time": ["time_j=1"],
    "collision_index": [],
    "event_signature": [],
    "primitive_key": ["candidate_family_id"],
    "owner_key": ["source_core_id", "destination_core_id"],
    "rank_zero_component": ["component_id", "connected_rank=0"],
    "plaque_side": ["component_face_side", "inside/outside trace IDs"],
    "word_cell": [
        "path_cell_id",
        "source_official_word_key_id",
        "destination_official_word_key_id",
    ],
    "endpoint_coordinate": ["component_coordinate_germ"],
    "root_coordinate": ["component_coordinate_germ"],
}

ROUND67_TOKEN_BY_FIELD = {
    "restriction_id": "restriction-id",
    "return_component": None,
    "insertion_time": "time-j",
    "collision_index": None,
    "event_signature": "physical-event-signature",
    "primitive_key": "primitive-key",
    "owner_key": "owner view q_j, but no retained recordwise owner-key token",
    "rank_zero_component": "connected-rank-0",
    "plaque_side": "side-label",
    "word_cell": "word-cell",
    "endpoint_coordinate": "endpoint/root coordinates",
    "root_coordinate": "endpoint/root coordinates",
}

GROUPS = [
    "round67_unmaterialized_root_schema_rows",
    "required_field_status_rows",
    "carrier_type_status_rows",
    "typed_incidence_match_rows",
    "unmatched_round72_component_rows",
    "obstruction_witness_rows",
]


class VerificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise VerificationError(f"non-finite JSON constant:{token}")


def strict_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    require(len(raw) <= 4_000_000, f"oversized JSON:{label}")
    require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM:{label}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"invalid UTF-8:{label}") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=strict_object,
            parse_constant=reject_constant,
        )
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
        raise VerificationError(f"strict JSON:{label}") from exc
    require(isinstance(value, dict), f"top-level object:{label}")
    return value


def strict_json_path(path: Path) -> dict[str, Any]:
    return strict_json_bytes(path.read_bytes(), path.name)


def closed_row(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "row already closed")
    return {**row, "row_sha256": digest(row)}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class Core:
    chart_id: str
    t0: Q
    t1: Q
    p0: Q
    p1: Q
    target_id: str
    crossings: tuple[str, ...]

    @property
    def source(self) -> str:
        return self.chart_id.split(":")[0]


def physical_cores() -> tuple[Core, ...]:
    rows: list[Core] = []
    axes = {
        "E": (1, 0, "X+"),
        "W": (-1, 0, "X-"),
        "N": (0, 1, "Y+"),
        "S": (0, -1, "Y-"),
    }
    for source in ("G", "W"):
        for cell in ("E", "W", "N", "S"):
            ix, iy, token = axes[cell]
            rows.append(
                Core(
                    f"{source}:{cell}",
                    Q(1, 100),
                    Q(1, 50),
                    -Q(1, 500),
                    Q(1, 500),
                    f"{source}[{ix},{iy}]",
                    () if source == "G" else (token,),
                )
            )
    diagonals = {
        "G": {
            "NE": (("E", 1), ("N", 1), "W[0,0]"),
            "NW": (("W", 1), ("N", -1), "W[-1,0]"),
            "SE": (("E", -1), ("S", 1), "W[0,-1]"),
            "SW": (("W", -1), ("S", -1), "W[-1,-1]"),
        },
        "W": {
            "NE": (("E", 1), ("N", 1), "G[1,1]"),
            "NW": (("W", 1), ("N", -1), "G[0,1]"),
            "SE": (("E", -1), ("S", 1), "G[1,0]"),
            "SW": (("W", -1), ("S", -1), "G[0,0]"),
        },
    }
    for source in ("G", "W"):
        for direction in ("NE", "NW", "SE", "SW"):
            first, second, target = diagonals[source][direction]
            for cell, sign in (first, second):
                t0, t1 = (
                    (Q(69, 100), Q(7, 10))
                    if sign > 0
                    else (-Q(7, 10), -Q(69, 100))
                )
                rows.append(
                    Core(
                        f"{source}:{cell}",
                        t0,
                        t1,
                        -Q(1, 50),
                        Q(1, 50),
                        target,
                        (),
                    )
                )
    rows.sort(
        key=lambda row: (
            row.chart_id,
            row.target_id,
            row.crossings,
            row.t0,
            row.t1,
            row.p0,
            row.p1,
        )
    )
    require(len(rows) == 24, "24 independently reconstructed cores")
    return tuple(rows)


def core_payload(core: Core) -> dict[str, Any]:
    return {
        "chart_id": core.chart_id,
        "t": [qstr(core.t0), qstr(core.t1)],
        "p": [qstr(core.p0), qstr(core.p1)],
        "target_id": core.target_id,
        "crossings": list(core.crossings),
    }


def core_id(core: Core) -> str:
    return "core:" + digest(core_payload(core))


def face_id(core: Core, side: str) -> str:
    require(side in {"t_lower", "t_upper", "p_lower", "p_upper"}, "face side")
    value = (
        core.t0
        if side == "t_lower"
        else core.t1
        if side == "t_upper"
        else core.p0
        if side == "p_lower"
        else core.p1
    )
    return "physical-core-face:" + digest(
        {
            "core_id": core_id(core),
            "core_chart_id": core.chart_id,
            "core_source_obstacle": core.source,
            "side": side,
            "coordinate": side[0],
            "coordinate_value": qstr(value),
            "outward_normal_sign": -1 if side.endswith("lower") else 1,
        }
    )


def witness_component_id(witness: dict[str, Any]) -> str:
    return "physical-r1-face-component:" + digest(
        {
            "candidate_family_id": witness["candidate_family_id"],
            "base_parameter": "s=0",
            "witness_minus": witness["witness_minus"],
            "witness_plus": witness["witness_plus"],
        }
    )


def path_cell_id(source: str, destination: str) -> str:
    return "base-r1-edge-cell:" + digest(
        {
            "source_core_id": source,
            "destination_core_id": destination,
            "s": "0",
        }
    )


def load_upstreams(check_files: bool = True) -> dict[str, dict[str, Any]]:
    if check_files:
        require(sha256_path(PRODUCER) == PRODUCER_SHA256, "producer byte pin")
    documents: dict[str, dict[str, Any]] = {}
    for name, expected in BYTE_PINS.items():
        path = HERE / name
        if check_files:
            require(path.is_file(), f"missing upstream:{name}")
            require(sha256_path(path) == expected, f"upstream byte pin:{name}")
        if name.endswith(".json"):
            document = strict_json_path(path)
            require(document.get("schema") == SCHEMA_PINS[name], f"schema pin:{name}")
            scope, expected_canonical = CANONICAL_PINS[name]
            selected = document if scope == "document" else document.get("result")
            require(selected is not None, f"canonical scope:{name}")
            require(digest(selected) == expected_canonical, f"canonical pin:{name}")
            documents[name] = document
    r128 = documents[R128]
    a128 = documents[R128A]
    require(r128["result_sha256"] == CANONICAL_PINS[R128][1], "Round128 result pin")
    require(a128["result_sha256"] == CANONICAL_PINS[R128A][1], "Round128 audit result pin")
    require(a128["result"]["status"] == "PASS", "Round128 audit PASS")
    require(a128["result"]["certificate_sha256"] == BYTE_PINS[R128], "Round128 audited cert")
    require(
        a128["result"]["certificate_result_sha256"] == r128["result_sha256"],
        "Round128 audited result",
    )
    return documents


def verify_word_id(row: list[Any], identifier: str, ordinal: int) -> None:
    require(
        identifier == f"gate5-word:{ordinal:06d}:{digest(row)}",
        "official word ID closure",
    )
    require(
        isinstance(row, list)
        and len(row) == 4
        and isinstance(row[0], str)
        and isinstance(row[1], str)
        and isinstance(row[2], list)
        and type(row[3]) is int,
        "official word row shape",
    )


def reconstruct_source_rows(
    documents: dict[str, dict[str, Any]],
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    list[dict[str, Any]],
]:
    r67 = documents[R67]["result"]
    r28 = documents[R28]["result"]
    r69 = documents[R69]["result"]
    r71w = documents[R71W]
    r71 = documents[R71]["result"]
    r72f = documents[R72F]["result"]
    r72 = documents[R72]["result"]
    r128 = documents[R128]["result"]
    a128 = documents[R128A]["result"]

    fixed = r67["actual_fixed_j_subroot"]
    require(fixed["status"] == "CERTIFIED_GRAPH_SUPPORTED_PHYSICAL_SUBROOT", "Round67 root")
    require(
        fixed["root"] == "Omega_j={(a,x):x in E_(j,a)^owner intersect R_(j,a)^reg}",
        "Round67 root formula",
    )
    require(
        fixed["base_law"] == "finite standard-Borel endpoint-coarea occurrence law m_occ",
        "Round67 base law",
    )
    prefixes = re.compile(
        r"^(?:restriction:|rn-restriction:|core:|occ:|"
        r"physical-moving-occurrence-face-seed:|physical-r1-face-component:"
        r"|physical-r1-trace:|base-r1-edge-cell:|path-cell:|gate5-word:)"
    )

    def scan(value: Any) -> list[str]:
        found: list[str] = []
        if isinstance(value, dict):
            for child in value.values():
                found.extend(scan(child))
        elif isinstance(value, list):
            for child in value:
                found.extend(scan(child))
        elif isinstance(value, str) and prefixes.match(value):
            found.append(value)
        return found

    require(scan(r67) == [], "Round67 no recordwise identifier rows")

    occurrence = r28["moving_occurrence_coarea_DQ_face_seed_registry"]
    require(occurrence["materialized_physical_moving_occurrence_face_seed_count"] == 64, "64 occurrence seeds")
    require(occurrence["materialized_oriented_hit_miss_trace_seed_count"] == 128, "128 occurrence traces")
    require(
        occurrence["face_ids_sha256"]
        == "17dd59a93d8c5fcfca49687b5c6dfe037a037787c55fff3924f71250f95eef21",
        "occurrence seed ID digest",
    )
    require(
        occurrence["trace_seed_ids_sha256"]
        == "c3607a44db1a8faf5531ef91af7d2b99066ddfa1f004cdf4441d68eedfc8c75a",
        "occurrence trace ID digest",
    )
    require(occurrence["moving_occurrence_faces_are_internal_R1_boundary_faces"] is False, "occurrence non-internal")
    require(len(occurrence["representative_face_rows"]) == 4, "four occurrence representatives")
    require(
        all(
            row["physical_carrier_type"] == "moving_first_event_grazing_occurrence_face"
            for row in occurrence["representative_face_rows"]
        ),
        "occurrence carrier type",
    )

    obstruction = r69["direct_equality_obstruction"]
    correction = r69["typed_incidence_correction"]
    histogram = obstruction["full_core_occurrence_reason_histogram"]
    require(obstruction["full_core_occurrence_pair_count"] == 24 * 64 == 1536, "full pair count")
    require(sum(histogram.values()) == 1536, "full separation histogram")
    require(
        histogram
        == {
            "different_collision_section_component": 768,
            "different_first_target_excluded_by_strict_first_owner": 656,
            "same_target_grazing_abs_p_1_disjoint_from_core_abs_p_lt_3_over_10": 112,
        },
        "full separation histogram values",
    )
    require(Q(3, 10) < Q(1), "exact grazing/core momentum separation")
    require(obstruction["full_core_occurrence_intersection_count"] == 0, "full intersection zero")
    require(obstruction["selected_base_root_occurrence_pair_count"] == 176 * 64 == 11264, "selected pair count")
    require(obstruction["selected_base_root_occurrence_intersection_count"] == 0, "selected intersection zero")
    require(obstruction["recordwise_source_point_equality_is_correct_join"] is False, "not equality")
    require(correction["R1_inner_moving_occurrence_incidence"] == "CERTIFIED_EMPTY", "R1 occurrence empty")
    require(correction["arbitrary_Rn_occurrence_pullback_component_ids_materialized"] == 0, "no Rn occurrence components")
    require(correction["arbitrary_Rn_connected_ranks_materialized"] == 0, "no Rn ranks")
    require(
        correction["edge_semantics"]
        == "FACE_IS_BOUNDARY_OR_PULLBACK_CARRIER_INCIDENT_TO_PATH_CELL__NOT_EQUAL_TO_INTERIOR_POINT",
        "typed edge",
    )

    fail_closed = r128["B_Round67_occurrence_owner_crosswalk_fail_closed"]
    require(fail_closed["required_recordwise_composite_key_fields"] == REQUIRED_FIELDS, "12-field order")
    require(fail_closed["round67_materialized_recordwise_identifier_count"] == 0, "Round67 row zero")
    require(fail_closed["round67_to_round72_component_crosswalk_row_count"] == 0, "crosswalk zero")
    require(a128["replay_audit"]["Round67_joined_fields"] == "0/12", "Round128 verified 0/12")

    atlas = r72["complete_base_fibre_terminal_preimage_family_atlas"]
    component_summary = r72["complete_positive_component_registry"]
    numeric = r72["numeric_local_field_registry"]
    require(
        (
            atlas["candidate_family_count"],
            atlas["positive_family_count"],
            atlas["certified_empty_family_count"],
            atlas["unresolved_family_count"],
        )
        == (1152, 32, 1120, 0),
        "Round72 family census",
    )
    require(
        (
            component_summary["component_count"],
            component_summary["connected_rank"],
            component_summary["one_sided_trace_count"],
        )
        == (32, 0, 64),
        "Round72 component census",
    )
    require(
        numeric["F10_numeric_rows"]
        == numeric["F13_numeric_rows"]
        == numeric["F16_numeric_rows"]
        == 32,
        "Round72 field census",
    )
    require(r72f["component_count"] == len(r72f["rows"]) == 32, "Round72 proof rows")
    require(r72f["F10_integer_sum"] == 480, "Round72 F10 sum")

    witnesses = r71w["rows"]
    component_rows = r71["base_fibre_nonempty_face_witness_registry"]["component_rows"]
    field_rows = r72f["rows"]
    incidence_rows = r128["A_base_R1_component_to_global_word_incidence"]["component_incidence_rows"]
    require(len(witnesses) == len(component_rows) == len(field_rows) == len(incidence_rows) == 32, "32-way inputs")

    cores = physical_cores()
    witness_map = {witness_component_id(row): row for row in witnesses}
    component_map = {row["component_id"]: row for row in component_rows}
    field_map = {row["component_id"]: row for row in field_rows}
    incidence_map = {row["component_id"]: row for row in incidence_rows}
    ids = set(witness_map)
    require(ids == set(component_map) == set(field_map) == set(incidence_map), "four-way component ID join")
    require(len(ids) == 32, "32 unique component IDs")

    rebuilt: list[dict[str, Any]] = []
    path_ids: set[str] = set()
    trace_ids: set[str] = set()
    source_words: set[str] = set()
    for identifier in sorted(ids):
        witness = witness_map[identifier]
        component = component_map[identifier]
        field = field_map[identifier]
        source = incidence_map[identifier]
        source_index = witness["source_core_index"]
        destination_index = witness["destination_core_index"]
        require(type(source_index) is int and 0 <= source_index < 24, "source index")
        require(type(destination_index) is int and 0 <= destination_index < 24, "destination index")
        source_core = cores[source_index]
        destination_core = cores[destination_index]
        source_core_identifier = core_id(source_core)
        destination_core_identifier = core_id(destination_core)
        destination_face_identifier = face_id(destination_core, witness["side"])
        path_identifier = path_cell_id(source_core_identifier, destination_core_identifier)
        require(component["component_id"] == identifier, "component identity")
        require(component["candidate_family_id"] == witness["candidate_family_id"] == field["candidate_family_id"], "candidate family join")
        require(component["source_core_id"] == witness["source_core_id"] == source_core_identifier, "source core join")
        require(component["destination_core_id"] == witness["destination_core_id"] == destination_core_identifier, "destination core join")
        require(component["destination_face_id"] == witness["destination_face_id"] == destination_face_identifier, "destination face join")
        require(component["path_cell_id"] == path_identifier, "path ID")
        require(component["time_j"] == 1 and component["connected_rank"] == 0, "component time/rank")
        require(component["candidate_family_id"].startswith("physical-r1-core-preimage-family:"), "terminal family grammar")
        require(
            component["incidence_relation"]
            == "TERMINAL_CORE_PREIMAGE_FACE_GERM_INCIDENT_TO_BASE_R1_EDGE_CELL",
            "terminal component relation",
        )
        require([row["side_label"] for row in component["trace_rows"]] == ["inside", "outside"], "trace labels")
        for trace in component["trace_rows"]:
            require(
                trace["trace_id"]
                == "physical-r1-trace:"
                + digest({"component_id": identifier, "side": trace["side_label"]}),
                "trace ID",
            )
            trace_ids.add(trace["trace_id"])
        require(source["row_sha256"] == digest({k: v for k, v in source.items() if k != "row_sha256"}), "Round128 source row closure")
        require(source["source_round71_component_row_sha256"] == digest(component), "Round71 source row digest")
        require(source["source_round72_field_row_sha256"] == digest(field), "Round72 source row digest")
        for key in (
            "component_id",
            "candidate_family_id",
            "source_core_id",
            "destination_core_id",
            "destination_face_id",
            "path_cell_id",
            "trace_rows",
        ):
            require(source[key] == component[key], f"Round128/component:{key}")
        require(source["base_parameter"] == "s=0", "base parameter")
        require(source["time_j"] == 1 and source["connected_rank"] == 0, "incidence time/rank")
        require(source["source_and_destination_roof_level_count"] == 1, "roof count")
        require(source["source_and_destination_roof_level_j"] == 0, "roof j")
        require(source["component_face_side"] == field["side"], "field side")
        require(
            source["component_coordinate_germ"]
            == {
                "t_center": field["t_center"],
                "t_radius": field["t_radius"],
                "p_center": field["p_center"],
                "p_bracket_radius": field["p_bracket_radius"],
                "s_radius": field["s_radius"],
            },
            "coordinate germ",
        )
        require(
            source["numeric_local_fields"]
            == {
                "F10_integer_upper": field["F10_integer_upper"],
                "F13_current_variation_strict_upper": field["F13_current_variation_strict_upper"],
                "F16_Piola_flux_cost_strict_upper": field["F16_Piola_flux_cost_strict_upper"],
            },
            "numeric fields",
        )
        verify_word_id(
            source["source_official_word_row"],
            source["source_official_word_key_id"],
            source["source_official_word_ordinal"],
        )
        verify_word_id(
            source["destination_official_word_row"],
            source["destination_official_word_key_id"],
            source["destination_official_word_ordinal"],
        )
        path_ids.add(path_identifier)
        source_words.add(source["source_official_word_key_id"])
        rebuilt.append(source)
    require(len(path_ids) == len(source_words) == 16, "16 paths/source words")
    require(len(trace_ids) == 64, "64 traces")
    require(
        r128["A_base_R1_component_to_global_word_incidence"]["directed_source_destination_word_edge_count"]
        == 16,
        "16 directed edges",
    )
    require(
        r128["A_base_R1_component_to_global_word_incidence"]["reciprocal_unordered_word_pair_count"]
        == 8,
        "8 reciprocal pairs",
    )
    return fixed, occurrence, correction, rebuilt


def build_expected(check_files: bool = True) -> dict[str, Any]:
    documents = load_upstreams(check_files)
    fixed, occurrence, correction, incidence_rows = reconstruct_source_rows(documents)
    r69 = documents[R69]["result"]
    obstruction = r69["direct_equality_obstruction"]
    a128 = documents[R128A]["result"]

    unmatched_rows: list[dict[str, Any]] = []
    for source in sorted(incidence_rows, key=lambda row: row["component_id"]):
        unmatched_id = "round131-unmatched-round72-component:" + digest(
            [
                "round131-unmatched-round72-component-v1",
                source["component_id"],
                source["path_cell_id"],
                source["source_official_word_key_id"],
                source["destination_official_word_key_id"],
            ]
        )
        unmatched_rows.append(
            closed_row(
                {
                    "unmatched_row_id": unmatched_id,
                    "join_status": "UNMATCHED__ROUND67_RECORD_AND_EXACT_COORDINATE_MAP_ABSENT",
                    "round67_occurrence_record_id": None,
                    "typed_incidence_id": None,
                    "all_twelve_round67_recordwise_values": {
                        field: None for field in REQUIRED_FIELDS
                    },
                    "missing_round67_required_fields": list(REQUIRED_FIELDS),
                    "missing_round67_required_field_count": 12,
                    "component_id": source["component_id"],
                    "candidate_family_id": source["candidate_family_id"],
                    "Round71_Round72_physical_carrier_type": "regular_branch_pullback_of_stationary_destination_core_face",
                    "eligible_as_Round67_occurrence_pullback_face": False,
                    "component_coordinate_germ": source["component_coordinate_germ"],
                    "component_face_side": source["component_face_side"],
                    "base_parameter": source["base_parameter"],
                    "connected_rank": source["connected_rank"],
                    "time_j": source["time_j"],
                    "return_depth": source["time_j"],
                    "roof_level_j": source["source_and_destination_roof_level_j"],
                    "source_core_id": source["source_core_id"],
                    "destination_core_id": source["destination_core_id"],
                    "destination_face_id": source["destination_face_id"],
                    "path_cell_id": source["path_cell_id"],
                    "source_official_word_key_id": source["source_official_word_key_id"],
                    "destination_official_word_key_id": source["destination_official_word_key_id"],
                    "source_official_word_row": source["source_official_word_row"],
                    "destination_official_word_row": source["destination_official_word_row"],
                    "trace_rows": source["trace_rows"],
                    "numeric_local_fields": source["numeric_local_fields"],
                    "source_round71_component_row_sha256": source["source_round71_component_row_sha256"],
                    "source_round72_field_row_sha256": source["source_round72_field_row_sha256"],
                    "source_round128_incidence_row_id": source["incidence_row_id"],
                    "source_round128_incidence_row_sha256": source["row_sha256"],
                    "candidate_family_id_is_not_Round67_primitive_key": True,
                    "source_or_destination_core_id_is_not_Round67_owner_key": True,
                    "coordinate_face_side_is_not_Round67_plaque_side": True,
                    "word_membership_is_not_same_physical_root": True,
                    "endpoint_root_to_s_t_p_coordinate_map_id": None,
                    "Round72_F10_F13_F16_attached_to_Round67_root": False,
                }
            )
        )

    field_rows = [
        closed_row(
            {
                "field_index": index,
                "required_field": field,
                "Round67_declared_token_or_semantic_source": ROUND67_TOKEN_BY_FIELD[field],
                "Round67_recordwise_value_materialized": False,
                "Round71_Round72_Round128_evidence_tokens": EVIDENCE_BY_FIELD[field],
                "same_semantic_key_join_proven": False,
                "field_status": "UNMATCHED",
            }
        )
        for index, field in enumerate(REQUIRED_FIELDS, start=1)
    ]
    root_rows = [
        closed_row(
            {
                "root_schema_row_id": "round131-round67-unmaterialized-root-schema:"
                + digest(
                    [
                        "round131-round67-unmaterialized-root-schema-v1",
                        fixed["root"],
                        fixed["base_law"],
                        fixed["retained_keys"],
                    ]
                ),
                "Round67_root": fixed["root"],
                "Round67_root_measure": fixed["root_measure"],
                "Round67_base_law": fixed["base_law"],
                "Round67_owner_law": fixed["owner_law"],
                "Round67_retained_key_schema": fixed["retained_keys"],
                "Round67_materialized_recordwise_identifier_count": 0,
                "Round67_materialized_twelve_field_record_count": 0,
                "status": "ABSTRACT_PHYSICAL_SUBROOT_CERTIFIED__RECORDWISE_ROWS_ABSENT",
            }
        )
    ]
    carrier_rows = [
        closed_row(
            {
                "carrier_type_row_id": "ROUND67_UNDERLYING_OCCURRENCE_SEEDS",
                "carrier_type": "moving_first_event_grazing_occurrence_face",
                "materialized_seed_count_in_Round28": 64,
                "materialized_oriented_hit_miss_trace_seed_count_in_Round28": 128,
                "internal_R1_boundary_face": False,
                "R1_inner_typed_incidence_status": "CERTIFIED_EMPTY",
                "arbitrary_Rn_occurrence_pullback_component_count": 0,
                "role": "source carrier seeds for a future occurrence-pullback family",
            }
        ),
        closed_row(
            {
                "carrier_type_row_id": "ROUND71_ROUND72_TERMINAL_CORE_PREIMAGE_COMPONENTS",
                "carrier_type": "regular_branch_pullback_of_stationary_destination_core_face",
                "materialized_component_count": 32,
                "materialized_one_sided_trace_count": 64,
                "R1_path_cell_count": 16,
                "eligible_as_Round67_occurrence_pullback_face": False,
                "role": "numeric terminal-preimage F10/F13/F16 components only",
            }
        ),
    ]
    obstruction_rows = [
        closed_row(
            {
                "obstruction_id": "ROUND67_RECORDS_NOT_MATERIALIZED",
                "evidence": {
                    "Round67_materialized_recordwise_identifier_count": 0,
                    "required_field_count": 12,
                    "joined_field_count": 0,
                },
                "blocks": "any typed-incidence match row",
            }
        ),
        closed_row(
            {
                "obstruction_id": "DIRECT_SOURCE_POINT_EQUALITY_IS_EMPTY",
                "evidence": {
                    "pair_audit_count": 11264,
                    "intersection_count": 0,
                    "occurrence_carrier_type": obstruction["raw_occurrence_carrier_type"],
                    "return_carrier_type": obstruction["return_carrier_type"],
                },
                "blocks": "recordwise point-equality join",
            }
        ),
        closed_row(
            {
                "obstruction_id": "TYPED_INCIDENCE_NOT_POINT_EQUALITY",
                "evidence": {
                    "node_sorts": correction["node_sorts"],
                    "edge_semantics": correction["edge_semantics"],
                },
                "blocks": "reusing equality as incidence",
            }
        ),
        closed_row(
            {
                "obstruction_id": "R1_MOVING_OCCURRENCE_TYPED_INCIDENCE_CERTIFIED_EMPTY",
                "evidence": {
                    "Round28_occurrence_seed_count": 64,
                    "Round28_occurrence_carrier_type": "moving_first_event_grazing_occurrence_face",
                    "Round69_R1_inner_moving_occurrence_incidence": "CERTIFIED_EMPTY",
                    "Round71_Round72_terminal_component_count": 32,
                    "terminal_component_carrier_type": "regular_branch_pullback_of_stationary_destination_core_face",
                    "carrier_type_compatible_direct_match_row_count": 0,
                },
                "blocks": "using a Round71/72 terminal-preimage component as a Round67 occurrence-pullback face",
            }
        ),
        closed_row(
            {
                "obstruction_id": "EXACT_COORDINATE_MAP_ABSENT",
                "evidence": {
                    "required_domain": "Round67 endpoint/root coordinates",
                    "required_codomain": "Round72 component germ (s,t,p)",
                    "materialized_map_count": 0,
                },
                "blocks": "Gamma subset Omega_1 x physical_face x path_cell",
            }
        ),
        closed_row(
            {
                "obstruction_id": "SURROGATE_IDENTIFIERS_FORBIDDEN",
                "evidence": {
                    "candidate_family_id_is_not_primitive_key": True,
                    "core_id_is_not_owner_key": True,
                    "coordinate_face_side_is_not_plaque_side": True,
                    "equal_time_rank_or_word_is_not_same_root": True,
                },
                "blocks": "field-name or identifier-shape join",
            }
        ),
    ]
    match_rows: list[dict[str, Any]] = []

    result = {
        "status": "CERTIFIED_FAIL_CLOSED_TYPED_INCIDENCE_CROSSWALK_0_MATCHES_32_UNMATCHED",
        "provenance": {
            "producer_sha256": PRODUCER_SHA256,
            "input_byte_pins": {name: BYTE_PINS[name] for name in sorted(BYTE_PINS)},
            "input_canonical_document_pins": {
                name: {"scope": CANONICAL_PINS[name][0], "sha256": CANONICAL_PINS[name][1]}
                for name in sorted(CANONICAL_PINS)
            },
            "input_schema_pins": {name: SCHEMA_PINS[name] for name in sorted(SCHEMA_PINS)},
            "Round128_independent_verification_status": a128["status"],
            "append_only": True,
        },
        "source_census": {
            "Round67_fixed_j_physical_subroot_status": fixed["status"],
            "Round67_materialized_recordwise_identifier_count": 0,
            "Round67_materialized_twelve_field_record_count": 0,
            "Round28_moving_first_event_grazing_occurrence_seed_count": 64,
            "Round28_oriented_hit_miss_occurrence_trace_seed_count": 128,
            "Round71_nonempty_component_count": 32,
            "Round72_candidate_family_count": 1152,
            "Round72_certified_empty_family_count": 1120,
            "Round72_positive_component_count": 32,
            "Round72_one_sided_trace_count": 64,
            "Round72_F10_F13_F16_numeric_row_count_each": 32,
            "Round128_path_cell_count": 16,
            "Round128_source_official_word_count": 16,
            "direct_source_point_equality_pair_audit_count": 11264,
            "direct_source_point_equality_intersection_count": 0,
            "R1_inner_moving_occurrence_typed_incidence_status": "CERTIFIED_EMPTY",
            "carrier_type_compatible_direct_match_row_count": 0,
        },
        "round67_unmaterialized_root_schema_rows": root_rows,
        "round67_unmaterialized_root_schema_rows_sha256": digest(root_rows),
        "required_field_status_rows": field_rows,
        "required_field_status_rows_sha256": digest(field_rows),
        "carrier_type_status_rows": carrier_rows,
        "carrier_type_status_rows_sha256": digest(carrier_rows),
        "typed_incidence_match_rows": match_rows,
        "typed_incidence_match_rows_sha256": digest(match_rows),
        "unmatched_round72_component_rows": unmatched_rows,
        "unmatched_round72_component_rows_sha256": digest(unmatched_rows),
        "obstruction_witness_rows": obstruction_rows,
        "obstruction_witness_rows_sha256": digest(obstruction_rows),
        "crosswalk_census": {
            "required_recordwise_field_count": 12,
            "required_recordwise_fields": list(REQUIRED_FIELDS),
            "currently_joined_required_fields": "0/12",
            "typed_incidence_match_row_count": 0,
            "carrier_type_status_row_count": 2,
            "carrier_type_compatible_direct_match_row_count": 0,
            "unmatched_round72_component_row_count": 32,
            "unmatched_round67_record_row_count": None,
            "unmatched_round67_record_row_count_is_null_because_records_are_not_materialized": True,
            "obstruction_witness_row_count": 6,
            "finite_Round131_row_count": 53,
        },
        "minimum_nonempty_typed_incidence_row_contract": {
            "graph_symbol": "Gamma",
            "ambient_product": "Omega_j x occurrence_pullback_face x R_n_path_cell",
            "required_face_carrier_type": "pullback of a Round28 moving_first_event_grazing_occurrence_face seed",
            "R1_inner_occurrence_pullback_target_certified_empty": True,
            "first_return_depth_not_ruled_out_by_the_R1_empty_theorem": "n>=2",
            "Round71_Round72_terminal_preimage_components_are_direct_match_candidates": False,
            "row_identity_payload": [
                "round67_occurrence_record_id",
                "occurrence_pullback_component_id",
                "path_cell_id",
                "exact_coordinate_map_id",
            ],
            "required_Round67_recordwise_fields": list(REQUIRED_FIELDS),
            "required_occurrence_pullback_path_word_fields": [
                "occurrence_face_seed_id",
                "occurrence_pullback_family_id",
                "occurrence_pullback_component_id",
                "base_parameter",
                "source_core_id",
                "destination_core_id",
                "path_cell_id",
                "source_official_word_key_id",
                "destination_official_word_key_id",
                "inside_trace_id",
                "outside_trace_id",
                "time_j",
                "return_depth",
                "connected_rank",
            ],
            "required_exact_coordinate_map_fields": [
                "coordinate_map_id",
                "domain_chart_and_restriction",
                "endpoint_coordinate_formula",
                "root_coordinate_formula",
                "s_t_p_formula",
                "inverse_or_fibre_formula",
                "Jacobian_or_transversality_nonzero_proof",
                "orientation_and_side_reconciliation",
                "Borel_graph_proof",
            ],
            "required_nonempty_evidence": [
                "one exact matched row",
                "physical incidence proof not point equality",
                "nonempty occurrence-pullback component germ or positive conditional mass witness",
            ],
            "fail_closed_rule": "if any required value or exact coordinate map is absent, emit an unmatched row and no match row",
            "future_match_row_count_required_for_nonempty_crosswalk": 1,
            "separate_later_quotient_needed_to_attach_Round72_numeric_fields": True,
        },
        "same_root_anti_splice_contract": {
            "candidate_family_id_may_replace_primitive_key": False,
            "source_or_destination_core_id_may_replace_owner_key": False,
            "component_coordinate_face_side_may_replace_plaque_side": False,
            "official_word_membership_may_replace_same_physical_root": False,
            "time_j_and_connected_rank_may_replace_twelve_field_key": False,
            "direct_source_point_equality_may_replace_typed_incidence": False,
            "Round72_component_germ_may_replace_exact_endpoint_root_map": False,
            "Round71_Round72_terminal_preimage_may_replace_occurrence_pullback_face": False,
            "Round72_numeric_fields_attached_to_Round67_owner_root": False,
        },
        "field_impact": {
            "F10": "32 nonempty base-R1 numeric rows exist but remain Round72 component-local and are not attached to the Round67 owner root",
            "F14": "NOT_INSTALLED_ON_A_JOINED_NONEMPTY_PHYSICAL_ROOT",
            "F15": "NOT_INSTALLED_ON_A_JOINED_NONEMPTY_PHYSICAL_ROOT; no positive pre-regularization or all-time cemetery payment",
            "F17": "NOT_INSTALLED_ON_A_JOINED_NONEMPTY_PHYSICAL_ROOT",
            "F18": "NO_COMMON_PHYSICAL_BLOCK_EXISTS",
        },
        "global_safety": {
            "Round67_to_Round72_crosswalk_row_count": 0,
            "global_complete_18_field_block_count": 0,
            "complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "gate5_global_maturity": "10/18",
            "gate5_status": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
            "arbitrary_return_depth_certified": False,
            "all_time_positive_potential_certified": False,
        },
        "strict_nonclaims": [
            "no Round67 recordwise occurrence or owner row is materialized",
            "no Round67 row is joined to a Round71 or Round72 component",
            "the 32 unmatched rows are not match rows or global coverage rows",
            "Round71/72 terminal-core preimages are not Round67 occurrence-pullback faces",
            "strict inner R1 moving-occurrence typed incidence is certified empty",
            "terminal-preimage face incidence is not interior point equality",
            "equal time, connected rank, word or similarly shaped IDs do not prove a same-root join",
            "Round72 F10/F13/F16 rows are not promoted to the Round67 owner root",
            "no F14/F15/F17/F18 common nonempty physical block is installed",
            "no arbitrary-depth, all-time positive-potential, Gate5 or CM2 claim",
        ],
    }
    return json.loads(json.dumps(result, sort_keys=True))


def validate_row_closures(result: dict[str, Any]) -> None:
    expected_counts = [1, 12, 2, 0, 32, 6]
    all_hashes: list[str] = []
    for group, count in zip(GROUPS, expected_counts):
        rows = result.get(group)
        require(isinstance(rows, list) and len(rows) == count, f"group count:{group}")
        require(result.get(group + "_sha256") == digest(rows), f"group digest:{group}")
        for row in rows:
            require(isinstance(row, dict), f"row object:{group}")
            copy_row = dict(row)
            recorded = copy_row.pop("row_sha256", None)
            require(recorded == digest(copy_row), f"row digest:{group}")
            all_hashes.append(recorded)
    require(len(all_hashes) == len(set(all_hashes)) == 53, "53 unique row digests")
    census = result["crosswalk_census"]
    require(census["finite_Round131_row_count"] == 53, "finite census")
    require(census["typed_incidence_match_row_count"] == 0, "zero matches")
    require(census["unmatched_round72_component_row_count"] == 32, "32 unmatched")
    require(census["required_recordwise_field_count"] == 12, "12 fields")
    require(census["obstruction_witness_row_count"] == 6, "six obstructions")


def evaluate_document(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    require(set(document) == {"schema", "result", "result_sha256"}, "closed certificate envelope")
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(isinstance(result, dict), "result object")
    require(document["result_sha256"] == digest(result), "outer result digest")
    validate_row_closures(result)
    require(result == expected, "independent expected result equality")
    require(document["result_sha256"] == CERTIFICATE_RESULT_SHA256, "frozen result digest")


def close_mutated_row(result: dict[str, Any], group: str, index: int) -> None:
    row = result[group][index]
    row.pop("row_sha256", None)
    row["row_sha256"] = digest(row)
    result[group + "_sha256"] = digest(result[group])


def resign(document: dict[str, Any]) -> None:
    document["result_sha256"] = digest(document["result"])


def semantic_mutations(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    def simple(path: tuple[str, ...], value: Any) -> Callable[[dict[str, Any]], None]:
        def mutate(document: dict[str, Any]) -> None:
            target: Any = document
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            resign(document)
        return mutate

    def mutate_row(
        group: str,
        index: int,
        operation: Callable[[dict[str, Any]], None],
    ) -> Callable[[dict[str, Any]], None]:
        def mutate(document: dict[str, Any]) -> None:
            operation(document["result"][group][index])
            close_mutated_row(document["result"], group, index)
            resign(document)
        return mutate

    def invent_match(document: dict[str, Any]) -> None:
        result = document["result"]
        row = closed_row(
            {
                "typed_incidence_id": "round131-typed-incidence:" + "0" * 64,
                "round67_occurrence_record_id": "restriction:" + "0" * 64,
                "occurrence_pullback_component_id": "face:" + "0" * 64,
                "path_cell_id": "path-cell:" + "0" * 64,
                "exact_coordinate_map_id": "coordinate-map:" + "0" * 64,
            }
        )
        result["typed_incidence_match_rows"].append(row)
        result["typed_incidence_match_rows_sha256"] = digest(
            result["typed_incidence_match_rows"]
        )
        result["crosswalk_census"]["typed_incidence_match_row_count"] = 1
        result["crosswalk_census"]["finite_Round131_row_count"] = 54
        resign(document)

    def delete_field(document: dict[str, Any]) -> None:
        result = document["result"]
        result["required_field_status_rows"].pop()
        result["required_field_status_rows_sha256"] = digest(
            result["required_field_status_rows"]
        )
        result["crosswalk_census"]["required_recordwise_field_count"] = 11
        result["crosswalk_census"]["required_recordwise_fields"].pop()
        result["crosswalk_census"]["finite_Round131_row_count"] = 52
        resign(document)

    def delete_unmatched(document: dict[str, Any]) -> None:
        result = document["result"]
        result["unmatched_round72_component_rows"].pop()
        result["unmatched_round72_component_rows_sha256"] = digest(
            result["unmatched_round72_component_rows"]
        )
        result["crosswalk_census"]["unmatched_round72_component_row_count"] = 31
        result["crosswalk_census"]["finite_Round131_row_count"] = 52
        resign(document)

    mutations.extend(
        [
            ("certificate schema altered", lambda d: (d.__setitem__("schema", "bad"), resign(d))),
            ("producer pin altered", simple(("result", "provenance", "producer_sha256"), "0" * 64)),
            ("Round28 input pin altered", simple(("result", "provenance", "input_byte_pins", R28), "0" * 64)),
            ("Round128 audit status altered", simple(("result", "provenance", "Round128_independent_verification_status"), "FAIL")),
            ("fake typed match invented and re-signed", invent_match),
            ("required field row deleted and census re-signed", delete_field),
            ("unmatched component deleted and census re-signed", delete_unmatched),
            (
                "primitive-key surrogate installed and re-signed",
                mutate_row(
                    "unmatched_round72_component_rows",
                    0,
                    lambda row: (
                        row["all_twelve_round67_recordwise_values"].__setitem__(
                            "primitive_key", row["candidate_family_id"]
                        ),
                        row.__setitem__(
                            "candidate_family_id_is_not_Round67_primitive_key",
                            False,
                        ),
                    ),
                ),
            ),
            (
                "core owner-key surrogate installed and re-signed",
                mutate_row(
                    "unmatched_round72_component_rows",
                    0,
                    lambda row: (
                        row["all_twelve_round67_recordwise_values"].__setitem__(
                            "owner_key", row["source_core_id"]
                        ),
                        row.__setitem__(
                            "source_or_destination_core_id_is_not_Round67_owner_key",
                            False,
                        ),
                    ),
                ),
            ),
            (
                "coordinate side used as plaque side and re-signed",
                mutate_row(
                    "unmatched_round72_component_rows",
                    0,
                    lambda row: (
                        row["all_twelve_round67_recordwise_values"].__setitem__(
                            "plaque_side", row["component_face_side"]
                        ),
                        row.__setitem__(
                            "coordinate_face_side_is_not_Round67_plaque_side",
                            False,
                        ),
                    ),
                ),
            ),
            (
                "terminal face promoted to occurrence pullback and re-signed",
                mutate_row(
                    "unmatched_round72_component_rows",
                    0,
                    lambda row: row.__setitem__(
                        "eligible_as_Round67_occurrence_pullback_face", True
                    ),
                ),
            ),
            (
                "coordinate map fabricated and re-signed",
                mutate_row(
                    "unmatched_round72_component_rows",
                    0,
                    lambda row: row.__setitem__(
                        "endpoint_root_to_s_t_p_coordinate_map_id",
                        "coordinate-map:" + "0" * 64,
                    ),
                ),
            ),
            (
                "base parameter altered and re-signed",
                mutate_row(
                    "unmatched_round72_component_rows",
                    0,
                    lambda row: row.__setitem__("base_parameter", "s=1"),
                ),
            ),
            (
                "return depth altered and re-signed",
                mutate_row(
                    "unmatched_round72_component_rows",
                    0,
                    lambda row: row.__setitem__("return_depth", 2),
                ),
            ),
            (
                "roof level altered and re-signed",
                mutate_row(
                    "unmatched_round72_component_rows",
                    0,
                    lambda row: row.__setitem__("roof_level_j", 1),
                ),
            ),
            (
                "component path orphaned and re-signed",
                mutate_row(
                    "unmatched_round72_component_rows",
                    0,
                    lambda row: row.__setitem__("path_cell_id", "base-r1-edge-cell:" + "0" * 64),
                ),
            ),
            (
                "component source word orphaned and re-signed",
                mutate_row(
                    "unmatched_round72_component_rows",
                    0,
                    lambda row: row.__setitem__("source_official_word_key_id", "gate5-word:000000:" + "0" * 64),
                ),
            ),
            (
                "component source row digest altered and re-signed",
                mutate_row(
                    "unmatched_round72_component_rows",
                    0,
                    lambda row: row.__setitem__("source_round128_incidence_row_sha256", "0" * 64),
                ),
            ),
            (
                "moving occurrence carrier renamed and re-signed",
                mutate_row(
                    "carrier_type_status_rows",
                    0,
                    lambda row: row.__setitem__("carrier_type", "regular_branch_pullback_of_stationary_destination_core_face"),
                ),
            ),
            (
                "terminal carrier renamed and re-signed",
                mutate_row(
                    "carrier_type_status_rows",
                    1,
                    lambda row: row.__setitem__("carrier_type", "moving_first_event_grazing_occurrence_face"),
                ),
            ),
            (
                "R1 occurrence emptiness erased and re-signed",
                mutate_row(
                    "carrier_type_status_rows",
                    0,
                    lambda row: row.__setitem__("R1_inner_typed_incidence_status", "CERTIFIED_NONEMPTY"),
                ),
            ),
            (
                "occurrence seed count altered and re-signed",
                mutate_row(
                    "carrier_type_status_rows",
                    0,
                    lambda row: row.__setitem__("materialized_seed_count_in_Round28", 63),
                ),
            ),
            (
                "direct intersection invented and re-signed",
                mutate_row(
                    "obstruction_witness_rows",
                    1,
                    lambda row: row["evidence"].__setitem__("intersection_count", 1),
                ),
            ),
            (
                "typed incidence changed to equality and re-signed",
                mutate_row(
                    "obstruction_witness_rows",
                    2,
                    lambda row: row["evidence"].__setitem__(
                        "edge_semantics", "FACE_EQUALS_PATH_INTERIOR_POINT"
                    ),
                ),
            ),
            (
                "carrier-type obstruction erased and re-signed",
                mutate_row(
                    "obstruction_witness_rows",
                    3,
                    lambda row: row["evidence"].__setitem__(
                        "carrier_type_compatible_direct_match_row_count", 1
                    ),
                ),
            ),
            (
                "coordinate map obstruction erased and re-signed",
                mutate_row(
                    "obstruction_witness_rows",
                    4,
                    lambda row: row["evidence"].__setitem__("materialized_map_count", 1),
                ),
            ),
            (
                "surrogate guard erased and re-signed",
                mutate_row(
                    "obstruction_witness_rows",
                    5,
                    lambda row: row["evidence"].__setitem__(
                        "candidate_family_id_is_not_primitive_key", False
                    ),
                ),
            ),
            ("joined fields promoted", simple(("result", "crosswalk_census", "currently_joined_required_fields"), "12/12")),
            ("carrier-compatible count promoted", simple(("result", "crosswalk_census", "carrier_type_compatible_direct_match_row_count"), 1)),
            (
                "future R1 target falsely opened",
                simple(
                    (
                        "result",
                        "minimum_nonempty_typed_incidence_row_contract",
                        "R1_inner_occurrence_pullback_target_certified_empty",
                    ),
                    False,
                ),
            ),
            (
                "future depth falsely reduced",
                simple(
                    (
                        "result",
                        "minimum_nonempty_typed_incidence_row_contract",
                        "first_return_depth_not_ruled_out_by_the_R1_empty_theorem",
                    ),
                    "n>=1",
                ),
            ),
            (
                "terminal faces promoted as direct candidates",
                simple(
                    (
                        "result",
                        "minimum_nonempty_typed_incidence_row_contract",
                        "Round71_Round72_terminal_preimage_components_are_direct_match_candidates",
                    ),
                    True,
                ),
            ),
            (
                "anti-splice candidate guard promoted",
                simple(
                    (
                        "result",
                        "same_root_anti_splice_contract",
                        "candidate_family_id_may_replace_primitive_key",
                    ),
                    True,
                ),
            ),
            (
                "anti-splice carrier guard promoted",
                simple(
                    (
                        "result",
                        "same_root_anti_splice_contract",
                        "Round71_Round72_terminal_preimage_may_replace_occurrence_pullback_face",
                    ),
                    True,
                ),
            ),
            ("Round72 fields attached to Round67", simple(("result", "same_root_anti_splice_contract", "Round72_numeric_fields_attached_to_Round67_owner_root"), True)),
            ("global complete block invented", simple(("result", "global_safety", "global_complete_18_field_block_count"), 1)),
            ("complete block invented", simple(("result", "global_safety", "complete_18_field_block_count"), 1)),
            ("Gate5 block invented", simple(("result", "global_safety", "gate5_block_count"), 1)),
            ("global maturity promoted", simple(("result", "global_safety", "gate5_global_maturity"), "18/18")),
            ("Gate5 promoted", simple(("result", "global_safety", "gate5_status"), "CERTIFIED")),
            ("CM2 promoted", simple(("result", "global_safety", "CM2"), "GO_FOR_CLAIM")),
            ("arbitrary return depth promoted", simple(("result", "global_safety", "arbitrary_return_depth_certified"), True)),
            ("all-time potential promoted", simple(("result", "global_safety", "all_time_positive_potential_certified"), True)),
            (
                "strict nonclaim deleted",
                lambda d: (
                    d["result"]["strict_nonclaims"].pop(),
                    resign(d),
                ),
            ),
            (
                "unknown result key added",
                lambda d: (
                    d["result"].__setitem__("unknown", True),
                    resign(d),
                ),
            ),
        ]
    )

    accepted: list[str] = []
    for label, mutation in mutations:
        candidate = copy.deepcopy(certificate)
        mutation(candidate)
        try:
            evaluate_document(candidate, expected)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            accepted.append(label)
        else:
            raise VerificationError(f"semantic mutation accepted:{label}")
    return accepted


def strict_json_attacks(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    raw = canonical(certificate).encode("utf-8")
    attacks: list[tuple[str, bytes]] = [
        (
            "duplicate top-level schema key",
            raw.replace(b'{"result":', b'{"schema":"duplicate","result":', 1),
        ),
        (
            "duplicate nested status key",
            raw.replace(
                b'"status":"CERTIFIED_FAIL_CLOSED_TYPED_INCIDENCE_CROSSWALK_0_MATCHES_32_UNMATCHED"',
                b'"status":"duplicate","status":"CERTIFIED_FAIL_CLOSED_TYPED_INCIDENCE_CROSSWALK_0_MATCHES_32_UNMATCHED"',
                1,
            ),
        ),
        (
            "floating-point count",
            raw.replace(b'"finite_Round131_row_count":53', b'"finite_Round131_row_count":53.0', 1),
        ),
        (
            "NaN constant",
            raw.replace(b'"finite_Round131_row_count":53', b'"finite_Round131_row_count":NaN', 1),
        ),
        (
            "positive Infinity",
            raw.replace(b'"finite_Round131_row_count":53', b'"finite_Round131_row_count":Infinity', 1),
        ),
        (
            "negative Infinity",
            raw.replace(b'"finite_Round131_row_count":53', b'"finite_Round131_row_count":-Infinity', 1),
        ),
        ("UTF-8 BOM", b"\xef\xbb\xbf" + raw),
        ("invalid UTF-8", raw[:-1] + b"\xff}"),
        ("top-level array", b"[]"),
        ("top-level null", b"null"),
        ("trailing second document", raw + b"{}"),
        (
            "oversized integer",
            raw.replace(
                b'"finite_Round131_row_count":53',
                b'"finite_Round131_row_count":' + b"9" * 5000,
                1,
            ),
        ),
        (
            "negative zero",
            raw.replace(b'"finite_Round131_row_count":53', b'"finite_Round131_row_count":-0', 1),
        ),
        (
            "leading-zero integer",
            raw.replace(b'"finite_Round131_row_count":53', b'"finite_Round131_row_count":053', 1),
        ),
        (
            "unpaired surrogate",
            raw.replace(
                b'"schema":"cm2.round131.round67-r1-typed-incidence-crosswalk.v1"',
                b'"schema":"\\ud800"',
                1,
            ),
        ),
    ]
    extra_top = copy.deepcopy(certificate)
    extra_top["unknown"] = True
    attacks.append(("closed envelope extra key", canonical(extra_top).encode("utf-8")))
    extra_result = copy.deepcopy(certificate)
    extra_result["result"]["unknown"] = True
    resign(extra_result)
    attacks.append(("closed result extra key", canonical(extra_result).encode("utf-8")))
    stale = copy.deepcopy(certificate)
    stale["result"]["status"] = "tampered"
    attacks.append(("stale outer result digest", canonical(stale).encode("utf-8")))

    rejected: list[str] = []
    for label, attack in attacks:
        try:
            document = strict_json_bytes(attack, label)
            evaluate_document(document, expected)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected.append(label)
        else:
            raise VerificationError(f"strict JSON attack accepted:{label}")
    return rejected


def build_verification(
    certificate: dict[str, Any],
    expected: dict[str, Any],
    mutations: list[str],
    strict_attacks: list[str],
) -> dict[str, Any]:
    result = {
        "status": "PASS",
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
        "certificate_schema": CERTIFICATE_SCHEMA,
        "verifier_sha256": sha256_path(VERIFIER),
        "independence_contract": {
            "Round131_producer_imported": False,
            "Round131_producer_executed": False,
            "Round67_Round28_Round69_obstruction_independently_replayed": True,
            "physical_core_definitions_independently_reconstructed": True,
            "Round71_Round72_Round128_four_way_component_join_independently_rebuilt": True,
            "all_53_Round131_rows_independently_reconstructed": True,
        },
        "replay_audit": {
            "Round28_moving_occurrence_seed_count": 64,
            "Round28_oriented_trace_seed_count": 128,
            "Round67_materialized_recordwise_row_count": 0,
            "Round69_full_core_occurrence_pairs": 1536,
            "Round69_full_core_occurrence_intersections": 0,
            "Round69_selected_base_occurrence_pairs": 11264,
            "Round69_selected_base_occurrence_intersections": 0,
            "Round69_R1_inner_moving_occurrence_incidence": "CERTIFIED_EMPTY",
            "Round71_Round72_terminal_component_count": 32,
            "Round71_Round72_terminal_trace_count": 64,
            "Round128_base_R1_path_cell_count": 16,
            "required_field_count": 12,
            "carrier_type_row_count": 2,
            "typed_incidence_match_row_count": 0,
            "unmatched_terminal_component_count": 32,
            "obstruction_row_count": 6,
            "finite_row_count": 53,
            "row_group_counts": [1, 12, 2, 0, 32, 6],
            "all_row_and_aggregate_hashes_rebuilt": True,
            "future_direct_occurrence_pullback_depth_lower_bound": "n>=2",
        },
        "semantic_mutation_test_count": len(mutations),
        "semantic_mutation_rejection_labels": mutations,
        "strict_json_attack_count": len(strict_attacks),
        "strict_json_attack_rejection_labels": strict_attacks,
        "determinism_contract": {
            "canonical_JSON_sort_keys": True,
            "no_hash_iteration_controls_output": True,
            "verification_replay_is_PYTHONHASHSEED_independent": True,
        },
        "safety": {
            "Round67_to_Round72_crosswalk_row_count": 0,
            "global_complete_18_field_block_count": 0,
            "complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "gate5_global_maturity": "10/18",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    require(certificate["result"] == expected, "valid certificate expected equality")
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def safe_input_path(path: Path) -> Path:
    expanded = path.expanduser()
    require(expanded.exists(), "certificate missing")
    require(not expanded.is_symlink(), "certificate must not be a symlink")
    metadata = expanded.lstat()
    require(stat.S_ISREG(metadata.st_mode), "certificate must be regular")
    require(metadata.st_nlink == 1, "certificate must not have hardlinks")
    return expanded.resolve()


def safe_output_path(path: Path, certificate_path: Path) -> Path:
    expanded = path.expanduser()
    protected = {
        VERIFIER,
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        certificate_path.resolve(),
        *((HERE / name).resolve() for name in BYTE_PINS),
    }
    require(not expanded.is_symlink(), "output must not be a symlink")
    if expanded.exists():
        metadata = expanded.lstat()
        require(stat.S_ISREG(metadata.st_mode), "existing output must be regular")
        require(metadata.st_nlink == 1, "existing output must not have hardlinks")
        for item in protected:
            try:
                require(not os.path.samefile(expanded, item), "output aliases protected input")
            except FileNotFoundError:
                pass
    resolved = expanded.resolve()
    require(resolved not in protected, "output overwrites protected input")
    require(resolved.parent.is_dir(), "output parent directory")
    return resolved


def write_document(path: Path, document: dict[str, Any]) -> None:
    payload = (
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.tmp-",
        dir=path.parent,
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        certificate_path = safe_input_path(args.certificate)
        raw = certificate_path.read_bytes()
        require(sha256_bytes(raw) == CERTIFICATE_SHA256, "certificate byte pin")
        certificate = strict_json_bytes(raw, certificate_path.name)
        expected = build_expected(check_files=True)
        evaluate_document(certificate, expected)
        mutations = semantic_mutations(certificate, expected)
        strict_attacks = strict_json_attacks(certificate, expected)
        verification = build_verification(
            certificate,
            expected,
            mutations,
            strict_attacks,
        )
        output = safe_output_path(args.output, certificate_path)
        write_document(output, verification)
        print(
            canonical(
                {
                    "output": str(output),
                    "semantic_mutations": len(mutations),
                    "status": "PASS",
                    "strict_json_attacks": len(strict_attacks),
                }
            )
        )
        return 0
    except (
        VerificationError,
        OSError,
        ValueError,
        KeyError,
        IndexError,
        TypeError,
        ArithmeticError,
    ) as exc:
        print(f"VerificationError: {exc}", file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
