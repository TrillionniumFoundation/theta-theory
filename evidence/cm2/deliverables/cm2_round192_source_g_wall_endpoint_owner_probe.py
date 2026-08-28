#!/usr/bin/env python3
"""Read-only feasibility spike for the 64 Round182 wall-G residual leaves.

The narrow question is whether the remaining wall-G tail is merely a
duplicated source-wall boundary sheet which can be glued by an outcome-blind
half-open t-owner.  The source wall factor is checked symbolically and
interval-wise.  The target wall factor is checked on the full leaf, the
common t=0 face, its exact t=p=0 edge, and the two relevant outer faces.

This is deliberately a zero-promotion probe.  It writes diagnostic JSON only
to stdout, progress only to stderr, has no output-path option, materializes no
return signature, and issues no whole-tube or global exact-key credit.

Probe-only trust boundary: importing Round182 imports the Round179 verifier
before this module can pin either file.  Both imported module identities and
the complete Round179/Round182 manifest chains are pinned immediately after
import.  This is suitable for a frozen-workspace feasibility spike, not an
adversarial verifier.  A formal verifier must hash inert producer bytes before
loading an independently implemented evaluator.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import gc
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

from flint import arb, ctx

import cm2_round182_source_g_clipped_graph_and_pair_arrangement as r182


HERE = Path(__file__).resolve().parent
PROBE = Path(__file__).resolve()
SCHEMA = "cm2.round192.source-g-wall-endpoint-owner-probe.v1"

R179_PREFIX = "cm2_round179_source_g_residual_tube_arrangement"
R182_PREFIX = "cm2_round182_source_g_clipped_graph_and_pair_arrangement"

R179_PINS = {
    f"{R179_PREFIX}.py":
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    f"{R179_PREFIX}_certificate.json":
        "edc2c538dc04a93c2b873f53e07b5c97c6b395a1d107e7ed2de4cf2c4bd35111",
    f"{R179_PREFIX}_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    f"{R179_PREFIX}_verifier.py":
        "292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679",
    f"{R179_PREFIX}_verification.json":
        "37eaa14cd870df64a12c2434deafe5fdead5cec303f5530208f07c11836736bc",
    f"{R179_PREFIX}_report.md":
        "c656cd3106fbe6c0562ff8ba00205e9d6bb6beac7883094d8f400f33c0389053",
    f"{R179_PREFIX}_cold_replay.md":
        "125cf5447fb99404b48c5bae27963f935ed19005e55e38f0aa84c89e6898fef1",
}
R179_MANIFEST = f"{R179_PREFIX}_manifest.sha256"
R179_MANIFEST_SHA256 = (
    "8fd5ae3a0cdd0c3321c0f8ffe6183ab57d31088b96523fa41ce0ebbe10d78b76"
)
R179_CERTIFICATE_RESULT_SHA256 = (
    "0f57284c11c617349fe66877552c401f426efafbc75faa08948f099166e9cde3"
)
R179_ATTACHMENT_RESULT_SHA256 = (
    "a5468800c1d89cd307a5a26c608550b04db79c64c562fb12bedb22d6cec308cb"
)
R179_VERIFICATION_RESULT_SHA256 = (
    "ca2ec32d84edf55919a26f556fd8e9dfc39566ad876b0cb5537168fee2b28229"
)
R179_ATTACHMENT_SCHEMA = (
    "cm2.round179.source-g-residual-tube-arrangement-rows.v1"
)

R182_PINS = {
    f"{R182_PREFIX}.py":
        "8638f2722e68bd5c6e0eb5932dc76780728998f21a47b1d8c02c28449e984d56",
    f"{R182_PREFIX}_certificate.json":
        "27491e3943e88772ec15cee110cd983b14ad82a2a56f8a07d605c3cd8fb49f08",
    f"{R182_PREFIX}_rows.json":
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    f"{R182_PREFIX}_verifier.py":
        "790b17cf6dadebc37b889fff63c6ecde985cccf53c95523cd6c2bc39d12db566",
    f"{R182_PREFIX}_verification.json":
        "b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36",
    f"{R182_PREFIX}_report.md":
        "708272e9425bef74f3f4639c76fd17078f509d3acc5d324325c224e743985f0c",
    f"{R182_PREFIX}_cold_replay.md":
        "c0fd075a0ba56de5380c6cc89620dc82fa640c0466b118565cf1755aedf61f99",
}
R182_MANIFEST = f"{R182_PREFIX}_manifest.sha256"
R182_MANIFEST_SHA256 = (
    "32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5"
)
R182_CERTIFICATE_RESULT_SHA256 = (
    "e07da794eed6dbb404de8913f5b871621f9f1b59b355172a37192791ae28911d"
)
R182_ATTACHMENT_RESULT_SHA256 = (
    "9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269"
)
R182_VERIFICATION_RESULT_SHA256 = (
    "61715ef39e232937d821ba1c634181f905454b758abbe98d889c768ddc809797"
)
R182_ATTACHMENT_SCHEMA = (
    "cm2.round182.source-g-clipped-graph-and-pair-arrangement-rows.v1"
)

EXPECTED_WALL_RESIDUAL_LEAVES = 64
EXPECTED_WALL_RESIDUAL_ORIGINS = 64
EXPECTED_PAIR_COUNT = 32
EXPECTED_WALL_RESIDUAL_VOLUME = Q(177, 204_800_000)
EXPECTED_SINGLE_LEAF_VOLUME = Q(177, 13_107_200_000)
EXPECTED_ORIGIN_RETAINED_VOLUME = Q(177, 102_400_000)
EXPECTED_ORIGIN_CLOSED_VOLUME = Q(22_479, 13_107_200_000)
EXPECTED_ALL_ORIGIN_RETAINED_VOLUME = Q(177, 1_600_000)
EXPECTED_ALL_ORIGIN_CLOSED_VOLUME = Q(22_479, 204_800_000)
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}

CHART_CONTRACT = {
    "G:E": ("G[1,0]", "Y", "source_y"),
    "G:W": ("G[-1,0]", "Y", "source_y"),
    "G:N": ("G[0,1]", "X", "source_x"),
    "G:S": ("G[0,-1]", "X", "source_x"),
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


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


def regular_file_bytes(path: Path, maximum: int = 200_000_000) -> bytes:
    """Read one immutable-looking, single-link regular file via O_NOFOLLOW."""

    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), f"not regular:{path.name}")
    require(before.st_nlink == 1, f"unexpected link count:{path.name}")
    require(0 < before.st_size <= maximum, f"input size:{path.name}")
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        require(
            (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            )
            == (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            ),
            f"file changed before read:{path.name}",
        )
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        require(
            (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            )
            == (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            ),
            f"file changed during read:{path.name}",
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def pinned_bytes(path: Path, expected: str) -> bytes:
    raw = regular_file_bytes(path)
    require(
        hashlib.sha256(raw).hexdigest() == expected,
        f"sha256 pin:{path.name}",
    )
    return raw


def strict_decode(raw: bytes) -> dict[str, Any]:
    require(
        raw
        and len(raw) <= 200_000_000
        and not raw.startswith(b"\xef\xbb\xbf")
        and b"\x00" not in raw,
        "strict JSON bytes",
    )

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key:{key}")
            result[key] = value
        return result

    def reject(token: str) -> None:
        raise ValueError(token)

    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )

    def walk(item: Any) -> None:
        if type(item) is str:
            require(
                "\x00" not in item
                and not any(0xD800 <= ord(char) <= 0xDFFF for char in item),
                "strict decoded string",
            )
        elif type(item) is list:
            for child in item:
                walk(child)
        elif type(item) is dict:
            for key, child in item.items():
                walk(key)
                walk(child)

    walk(value)
    require(type(value) is dict, "JSON top-level object")
    return value


def strict_load(path: Path, expected_file_sha256: str) -> dict[str, Any]:
    return strict_decode(pinned_bytes(path, expected_file_sha256))


def manifest_entries(raw: bytes) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        value, name = line.split("  ", 1)
        require(
            len(value) == 64
            and all(character in "0123456789abcdef" for character in value),
            f"manifest digest:{name}",
        )
        require(name not in result, f"manifest duplicate:{name}")
        result[name] = value
    return result


def check_wrapper(
    prefix: str,
    pins: dict[str, str],
    certificate_result_sha256: str,
    verification_result_sha256: str,
) -> None:
    certificate = strict_load(
        HERE / f"{prefix}_certificate.json",
        pins[f"{prefix}_certificate.json"],
    )
    verification = strict_load(
        HERE / f"{prefix}_verification.json",
        pins[f"{prefix}_verification.json"],
    )
    require(
        set(certificate) == {"schema", "result", "result_sha256"}
        and certificate["result_sha256"] == certificate_result_sha256
        and digest(certificate["result"]) == certificate_result_sha256,
        f"{prefix} certificate result",
    )
    require(
        set(verification) == {"schema", "result", "result_sha256"}
        and verification["result_sha256"] == verification_result_sha256
        and digest(verification["result"]) == verification_result_sha256
        and verification["result"]["status"] == "PASS"
        and verification["result"]["full_attachment_byte_for_byte_matched"]
        is True
        and verification["result"]["producer_imported_or_executed"] is False,
        f"{prefix} verification result",
    )


def check_inputs() -> dict[str, Any]:
    """Pin imported identities and all files in both frozen manifests."""

    r179 = r182.r179
    require(
        Path(r182.__file__).resolve() == (HERE / f"{R182_PREFIX}.py").resolve(),
        "Round182 imported module identity",
    )
    require(
        Path(r179.__file__).resolve()
        == (HERE / f"{R179_PREFIX}_verifier.py").resolve(),
        "Round179 imported verifier identity",
    )
    for name, expected in R179_PINS.items():
        pinned_bytes(HERE / name, expected)
    for name, expected in R182_PINS.items():
        pinned_bytes(HERE / name, expected)
    r179_manifest_raw = pinned_bytes(
        HERE / R179_MANIFEST,
        R179_MANIFEST_SHA256,
    )
    r182_manifest_raw = pinned_bytes(
        HERE / R182_MANIFEST,
        R182_MANIFEST_SHA256,
    )
    require(
        manifest_entries(r179_manifest_raw) == R179_PINS,
        "Round179 manifest exact entries",
    )
    require(
        manifest_entries(r182_manifest_raw) == R182_PINS,
        "Round182 manifest exact entries",
    )
    check_wrapper(
        R179_PREFIX,
        R179_PINS,
        R179_CERTIFICATE_RESULT_SHA256,
        R179_VERIFICATION_RESULT_SHA256,
    )
    check_wrapper(
        R182_PREFIX,
        R182_PINS,
        R182_CERTIFICATE_RESULT_SHA256,
        R182_VERIFICATION_RESULT_SHA256,
    )
    return {
        "Round179_manifest_sha256": R179_MANIFEST_SHA256,
        "Round179_certificate_result_sha256":
            R179_CERTIFICATE_RESULT_SHA256,
        "Round179_attachment_file_sha256":
            R179_PINS[f"{R179_PREFIX}_rows.json"],
        "Round179_attachment_result_sha256":
            R179_ATTACHMENT_RESULT_SHA256,
        "Round179_verification_result_sha256":
            R179_VERIFICATION_RESULT_SHA256,
        "Round182_manifest_sha256": R182_MANIFEST_SHA256,
        "Round182_certificate_result_sha256":
            R182_CERTIFICATE_RESULT_SHA256,
        "Round182_attachment_file_sha256":
            R182_PINS[f"{R182_PREFIX}_rows.json"],
        "Round182_attachment_result_sha256":
            R182_ATTACHMENT_RESULT_SHA256,
        "Round182_verification_result_sha256":
            R182_VERIFICATION_RESULT_SHA256,
        "complete_manifest_entry_count":
            len(R179_PINS) + len(R182_PINS),
        "probe_only_import_before_pin_boundary": True,
    }


def unpack_one(columns: list[str], packed: list[Any]) -> dict[str, Any]:
    require(len(columns) == len(packed), "packed row width")
    return dict(zip(columns, packed, strict=True))


def load_attachment(
    prefix: str,
    pins: dict[str, str],
    schema: str,
    expected_result_sha256: str,
) -> dict[str, Any]:
    wrapper = strict_load(
        HERE / f"{prefix}_rows.json",
        pins[f"{prefix}_rows.json"],
    )
    require(
        set(wrapper) == {"schema", "result", "result_sha256"}
        and wrapper["schema"] == schema
        and wrapper["result_sha256"] == expected_result_sha256,
        f"{prefix} attachment wrapper",
    )
    require(
        digest(wrapper["result"]) == expected_result_sha256,
        f"{prefix} attachment result digest",
    )
    return wrapper["result"]


def extract_round182_scope() -> dict[str, Any]:
    source = load_attachment(
        R182_PREFIX,
        R182_PINS,
        R182_ATTACHMENT_SCHEMA,
        R182_ATTACHMENT_RESULT_SHA256,
    )
    schemas = source["row_column_schemas"]
    collar_columns = schemas["collar_occurrence_rows"]
    leaf_columns = schemas["collar_leaf_rows"]
    origin_columns = schemas["origin_replacement_rows"]

    collars_by_occurrence: dict[str, dict[str, Any]] = {}
    for packed in source["collar_occurrence_rows"]:
        row = unpack_one(collar_columns, packed)
        occurrence = row["Round179_occurrence_row_id"]
        require(
            occurrence not in collars_by_occurrence,
            f"duplicate collar occurrence:{occurrence}",
        )
        collars_by_occurrence[occurrence] = row

    residual_leaves: list[dict[str, Any]] = []
    for packed in source["collar_leaf_rows"]:
        if Q(packed[14]) <= 0:
            continue
        collar = collars_by_occurrence[packed[1]]
        if collar["kind"] != "WALL":
            continue
        residual_leaves.append(unpack_one(leaf_columns, packed))

    require(
        len(residual_leaves) == EXPECTED_WALL_RESIDUAL_LEAVES,
        "Round182 residual wall leaf census",
    )
    occurrences = {row["occurrence_row_id"] for row in residual_leaves}
    relevant_collars = {
        occurrence: collars_by_occurrence[occurrence]
        for occurrence in occurrences
    }
    origin_ids = {
        row["origin_row_id"] for row in relevant_collars.values()
    }
    require(
        len(occurrences) == EXPECTED_WALL_RESIDUAL_LEAVES
        and len(origin_ids) == EXPECTED_WALL_RESIDUAL_ORIGINS,
        "wall occurrence/origin census",
    )

    all_leaves_by_occurrence: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for packed in source["collar_leaf_rows"]:
        if packed[1] in occurrences:
            all_leaves_by_occurrence[packed[1]].append(
                unpack_one(leaf_columns, packed)
            )
    relevant_origins: dict[str, dict[str, Any]] = {}
    for packed in source["origin_replacement_rows"]:
        if packed[1] in origin_ids:
            row = unpack_one(origin_columns, packed)
            relevant_origins[row["Round179_origin_row_id"]] = row
    require(
        set(relevant_origins) == origin_ids,
        "Round182 origin replacement support",
    )

    pattern_count = Counter(
        row["lower_t_face_status"] + "|" + row["upper_t_face_status"]
        for row in residual_leaves
    )
    require(
        pattern_count == Counter({"S-|U": 32, "U|S+": 32}),
        "Round182 wall residual face patterns",
    )
    total_volume = sum(
        (Q(row["residual_3d_collar_volume"]) for row in residual_leaves),
        Q(0),
    )
    require(
        total_volume == EXPECTED_WALL_RESIDUAL_VOLUME
        and all(
            Q(row["residual_3d_collar_volume"])
            == EXPECTED_SINGLE_LEAF_VOLUME
            for row in residual_leaves
        ),
        "Round182 wall residual exact volume",
    )

    for occurrence, collar in relevant_collars.items():
        leaves = sorted(
            all_leaves_by_occurrence[occurrence],
            key=lambda row: row["row_id"],
        )
        packed = [
            [row[column] for column in leaf_columns]
            for row in leaves
        ]
        require(
            len(leaves) == 8
            and sum(
                Q(row["closed_3d_side_union_volume"]) > 0
                for row in leaves
            ) == 7
            and sum(
                Q(row["residual_3d_collar_volume"]) > 0
                for row in leaves
            ) == 1
            and collar["closed_leaf_count"] == 7
            and collar["residual_leaf_count"] == 1
            and Q(collar["closed_coordinate_volume"])
            == EXPECTED_ORIGIN_CLOSED_VOLUME
            and Q(collar["residual_coordinate_volume"])
            == EXPECTED_SINGLE_LEAF_VOLUME
            and digest(packed) == collar["leaf_rows_sha256"],
            f"Round182 collar leaf ledger:{occurrence}",
        )

    for origin_id, row in relevant_origins.items():
        require(
            row["collar_occurrence_count"] == 1
            and row["pair_arrangement_count"] == 0
            and row["source_chart_seam_count"] == 0
            and row["Round179_retained_child_count"] == 2
            and Q(row["Round179_retained_coordinate_volume"])
            == EXPECTED_ORIGIN_RETAINED_VOLUME
            and Q(row["closed_Round182_retained_coordinate_volume"])
            == EXPECTED_ORIGIN_CLOSED_VOLUME
            and Q(row["residual_Round182_retained_coordinate_volume"])
            == EXPECTED_SINGLE_LEAF_VOLUME
            and row["fully_geometrically_replaced_original_tube"] is False
            and row["Round182_released_global_exact_key_count"] == 0
            and row["global_exact_key_disposition_credit"] == 0,
            f"Round182 origin ledger:{origin_id}",
        )

    result = {
        "residual_leaves": residual_leaves,
        "collars": relevant_collars,
        "origins": relevant_origins,
        "occurrences": occurrences,
        "origin_ids": origin_ids,
        "pattern_count": dict(sorted(pattern_count.items())),
        "total_volume": total_volume,
    }
    del source, collars_by_occurrence, all_leaves_by_occurrence
    gc.collect()
    return result


def extract_round179_scope(
    occurrence_ids: set[str],
    origin_ids: set[str],
) -> dict[str, Any]:
    source = load_attachment(
        R179_PREFIX,
        R179_PINS,
        R179_ATTACHMENT_SCHEMA,
        R179_ATTACHMENT_RESULT_SHA256,
    )
    schemas = source["row_column_schemas"]
    wall_columns = schemas["wall_normal_form_rows"]
    origin_columns = schemas["origin_tube_rows"]
    retained_columns = schemas["retained_3d_child_rows"]

    walls: dict[str, dict[str, Any]] = {}
    for packed in source["wall_normal_form_rows"]:
        if packed[0] in occurrence_ids:
            row = unpack_one(wall_columns, packed)
            walls[row["row_id"]] = row
    origins: dict[str, dict[str, Any]] = {}
    for packed in source["origin_tube_rows"]:
        if packed[0] in origin_ids:
            row = unpack_one(origin_columns, packed)
            origins[row["origin_row_id"]] = row
    retained: dict[str, dict[str, Any]] = {}
    for packed in source["retained_3d_child_rows"]:
        if packed[1] in origin_ids:
            row = unpack_one(retained_columns, packed)
            retained[row["row_id"]] = row

    require(set(walls) == occurrence_ids, "Round179 wall row support")
    require(set(origins) == origin_ids, "Round179 origin row support")
    require(
        len(retained) == 2 * EXPECTED_WALL_RESIDUAL_ORIGINS
        and Counter(row["origin_row_id"] for row in retained.values())
        == Counter({origin_id: 2 for origin_id in origin_ids}),
        "Round179 retained support",
    )
    del source
    gc.collect()
    return {"walls": walls, "origins": origins, "retained": retained}


def atlas_box(row: dict[str, Any]) -> Any:
    return r182.r179.r174.atlas.AtlasBox(
        *(Q(value) for value in row["box"]),
        len(row["base_refinement_path"]),
        row["row_id"],
    )


def fixed_box(
    box: Any,
    *,
    t: Q | None = None,
    p: Q | None = None,
) -> Any:
    return r182.r179.r174.atlas.AtlasBox(
        box.t0 if t is None else t,
        box.t1 if t is None else t,
        box.p0 if p is None else p,
        box.p1 if p is None else p,
        box.s0,
        box.s1,
        box.depth,
        box.path,
    )


def qarb(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def sign(value: arb) -> str:
    return r182.r179.arb_sign(value)


def analyze_leaf(
    leaf: dict[str, Any],
    collar: dict[str, Any],
    wall: dict[str, Any],
    origin179: dict[str, Any],
    origin182: dict[str, Any],
    retained: dict[str, Any],
) -> dict[str, Any]:
    r179 = r182.r179
    box = atlas_box(leaf)
    cell_contract = CHART_CONTRACT.get(collar["chart"])
    require(cell_contract is not None, f"chart support:{collar['chart']}")
    expected_owner, expected_axis, source_name = cell_contract
    require(
        collar["owner_target"] == expected_owner
        and collar["target_obstacle"] == "G"
        and collar["kind"] == "WALL"
        and wall["origin_row_id"] == collar["origin_row_id"]
        and wall["axis"] == expected_axis
        and wall["integer_wall"] == 0
        and wall["source_factor_classification"] == "REGULAR_GRAPH"
        and wall["source_gradient_axis"] == "t"
        and wall["source_gradient_sign"] == "STRICT_POSITIVE"
        and wall["target_factor_classification"] == "REGULAR_GRAPH"
        and wall["target_gradient_axis"] == "t"
        and wall["target_gradient_sign"] == "STRICT_POSITIVE",
        f"wall symbolic contract:{leaf['row_id']}",
    )
    require(
        origin179["origin_row_id"] == collar["origin_row_id"]
        and origin179["chart"] == collar["chart"]
        and origin179["owner_target"] == collar["owner_target"]
        and origin179["original_reason_labels"]
        == [collar["reason_label"]]
        and origin182["Round179_origin_row_id"] == collar["origin_row_id"]
        and retained["origin_row_id"] == collar["origin_row_id"]
        and retained["row_id"] == leaf["retained_child_row_id"],
        f"origin lineage:{leaf['row_id']}",
    )

    lower_u = leaf["lower_t_face_status"] == "U"
    upper_u = leaf["upper_t_face_status"] == "U"
    require(
        lower_u != upper_u,
        f"one unresolved t face:{leaf['row_id']}",
    )
    if lower_u:
        require(
            box.t0 == 0
            and box.t1 > 0
            and leaf["upper_t_face_status"] == "S+",
            f"positive t boundary pattern:{leaf['row_id']}",
        )
        side = "POSITIVE_T"
        outer_t = box.t1
        expected_outer_sign = "STRICT_POSITIVE"
    else:
        require(
            box.t1 == 0
            and box.t0 < 0
            and leaf["lower_t_face_status"] == "S-",
            f"negative t boundary pattern:{leaf['row_id']}",
        )
        side = "NEGATIVE_T"
        outer_t = box.t0
        expected_outer_sign = "STRICT_NEGATIVE"
    require(
        (box.p0 == 0) != (box.p1 == 0),
        f"exactly one p=0 boundary:{leaf['row_id']}",
    )
    outer_p = box.p1 if box.p0 == 0 else box.p0

    geometry = r179.independent_geometry(
        collar["chart"],
        collar["owner_target"],
        box,
    )
    source = r179.subtract_wall(geometry[source_name], 0)
    exact_dt = qarb(Q(9, 25))
    expected_source_value = (
        r179.r174.first_hit.arb_interval(box.t0, box.t1) * exact_dt
    )
    require(
        source[0].contains(expected_source_value)
        and expected_source_value.contains(source[0])
        and source[1][0].contains(exact_dt)
        and sign(source[1][0]) == "STRICT_POSITIVE"
        and source[1][1].is_zero()
        and source[1][2].is_zero(),
        f"exact source factor interval identity:{leaf['row_id']}",
    )
    zero_face = fixed_box(box, t=Q(0))
    source_zero = r179.subtract_wall(
        r179.independent_geometry(
            collar["chart"],
            collar["owner_target"],
            zero_face,
        )[source_name],
        0,
    )
    source_outer = r179.subtract_wall(
        r179.independent_geometry(
            collar["chart"],
            collar["owner_target"],
            fixed_box(box, t=outer_t),
        )[source_name],
        0,
    )
    require(
        source_zero[0].is_zero()
        and sign(source_outer[0]) == expected_outer_sign,
        f"source exact t=0 sheet:{leaf['row_id']}",
    )

    target_name = "hit_x" if wall["axis"] == "X" else "hit_y"

    def target_function(child: Any) -> tuple[Any, tuple[Any, ...]]:
        target_geometry = r179.independent_geometry(
            collar["chart"],
            collar["owner_target"],
            child,
        )
        return r179.subtract_wall(
            target_geometry[target_name],
            wall["integer_wall"],
        )

    target = target_function(box)
    target_zero_face = target_function(zero_face)
    corner = fixed_box(box, t=Q(0), p=Q(0))
    target_corner = target_function(corner)
    zero_outer_p = fixed_box(box, t=Q(0), p=outer_p)
    target_zero_outer_p = target_function(zero_outer_p)
    outer_t_face = fixed_box(box, t=outer_t)
    target_outer_t = target_function(outer_t_face)

    dt_sign = sign(target[1][0])
    dp_sign = sign(target[1][1])
    ds_exact_zero = target[1][2].is_zero()
    zero_outer_p_sign = sign(target_zero_outer_p[0])
    outer_t_sign = sign(target_outer_t[0])
    require(
        sign(target[0]) == "OVERWRAP"
        and sign(target_zero_face[0]) == "OVERWRAP"
        and dt_sign == "STRICT_POSITIVE"
        and dp_sign in STRICT_SIGNS
        and ds_exact_zero
        and target_corner[0].is_zero()
        and zero_outer_p_sign in STRICT_SIGNS
        and outer_t_sign == expected_outer_sign,
        f"target factor boundary evidence:{leaf['row_id']}",
    )

    if zero_outer_p_sign == outer_t_sign:
        target_class = "EXACT_T0_P0_S_EDGE_ONLY__NO_OFF_SOURCE_TARGET_ZERO"
        target_sheet_count = 0
        target_open_region_count = 1
        interval_newton_interior = None
        interval_newton_image = None
        product_zero_set = "EXACT_SOURCE_T0_SHEET"
    else:
        p_outer_face = fixed_box(box, p=outer_p)
        interval_newton_interior, interval_newton_image = (
            r182.interval_newton_image(
                target_function,
                p_outer_face,
                "t",
            )
        )
        require(
            interval_newton_interior is True,
            f"target p-outer edge Newton inclusion:{leaf['row_id']}",
        )
        target_class = (
            "UNIQUE_CLIPPED_TARGET_2D_GRAPH__"
            "T_BRACKET_MONOTONICITY_AND_P_OUTER_INTERVAL_NEWTON"
        )
        target_sheet_count = 1
        target_open_region_count = 2
        product_zero_set = (
            "SOURCE_T0_SHEET_UNION_UNIQUE_TARGET_2D_GRAPH__"
            "INTERSECTION_T0_P0_S_LINE"
        )

    pair_key = [
        collar["chart"],
        collar["owner_target"],
        wall["axis"],
        wall["integer_wall"],
        str(box.p0),
        str(box.p1),
        str(box.s0),
        str(box.s1),
    ]
    common_face = [
        "0",
        "0",
        str(box.p0),
        str(box.p1),
        str(box.s0),
        str(box.s1),
    ]
    target_intersection_edge = [
        "0",
        "0",
        "0",
        "0",
        str(box.s0),
        str(box.s1),
    ]
    return {
        "leaf_row_id": leaf["row_id"],
        "origin_row_id": collar["origin_row_id"],
        "parent_id": collar["parent_id"],
        "retained_child_row_id": leaf["retained_child_row_id"],
        "chart": collar["chart"],
        "owner_target": collar["owner_target"],
        "wall_axis": wall["axis"],
        "integer_wall": wall["integer_wall"],
        "t_side": side,
        "half_open_source_sheet_owner": side == "POSITIVE_T",
        "pair_key": pair_key,
        "pair_key_sha256": digest(pair_key),
        "leaf_box": leaf["box"],
        "coordinate_volume": leaf["residual_3d_collar_volume"],
        "unresolved_face": (
            "LOWER_T_FACE" if lower_u else "UPPER_T_FACE"
        ),
        "common_t0_face_exact_bounds": common_face,
        "common_t0_face_canonical_sha256": digest(common_face),
        "source_wall_factor_name": source_name,
        "source_wall_factor_exact": "(9/25)*t",
        "source_wall_factor_exact_zero_set": "t=0",
        "source_wall_strict_outer_t_sign": sign(source_outer[0]),
        "source_2D_sheet_count": 1,
        "source_sheet_1D_boundary_edge_incidence_count": 4,
        "source_sheet_0D_corner_incidence_count": 4,
        "target_wall_factor_name": target_name,
        "target_wall_full_leaf_sign": sign(target[0]),
        "target_wall_t0_face_sign": sign(target_zero_face[0]),
        "target_wall_exact_t0_p0_s_edge_zero": True,
        "target_t_derivative_sign": dt_sign,
        "target_t_derivative_interval": target[1][0].str(40),
        "target_p_derivative_sign": dp_sign,
        "target_p_derivative_interval": target[1][1].str(40),
        "target_s_derivative_exact_zero": ds_exact_zero,
        "target_t0_p_outer_sign": zero_outer_p_sign,
        "target_t0_p_outer_interval": target_zero_outer_p[0].str(40),
        "target_outer_t_face_sign": outer_t_sign,
        "target_outer_t_face_interval": target_outer_t[0].str(40),
        "target_zero_classification": target_class,
        "target_2D_sheet_count": target_sheet_count,
        "target_open_3D_region_count": target_open_region_count,
        "target_p_outer_interval_newton_interior":
            interval_newton_interior,
        "target_p_outer_interval_newton_image": interval_newton_image,
        "source_target_1D_intersection_exact_bounds":
            target_intersection_edge,
        "source_target_1D_intersection_endpoint_incidence_count": 2,
        "wall_product_zero_set": product_zero_set,
        "wall_product_equivalent_to_source_t0_sheet_only":
            target_sheet_count == 0,
        "whole_tube_credit": 0,
        "global_exact_key_disposition_credit": 0,
    }


def analyze_pairs(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[row["pair_key_sha256"]].append(row)
    require(
        len(groups) == EXPECTED_PAIR_COUNT,
        "exact wall boundary pair census",
    )
    pairs: list[dict[str, Any]] = []
    for key_sha256, pair_rows in sorted(groups.items()):
        pair_rows.sort(key=lambda row: row["t_side"])
        require(len(pair_rows) == 2, f"pair size:{key_sha256}")
        by_side = {row["t_side"]: row for row in pair_rows}
        require(
            set(by_side) == {"NEGATIVE_T", "POSITIVE_T"},
            f"pair signed sides:{key_sha256}",
        )
        negative = by_side["NEGATIVE_T"]
        positive = by_side["POSITIVE_T"]
        require(
            negative["pair_key"] == positive["pair_key"]
            and negative["common_t0_face_exact_bounds"]
            == positive["common_t0_face_exact_bounds"]
            and canonical(negative["common_t0_face_exact_bounds"]).encode()
            == canonical(positive["common_t0_face_exact_bounds"]).encode()
            and negative["common_t0_face_canonical_sha256"]
            == positive["common_t0_face_canonical_sha256"],
            f"byte/exact common face:{key_sha256}",
        )
        owners = [
            row for row in pair_rows
            if row["half_open_source_sheet_owner"]
        ]
        require(
            len(owners) == 1 and owners[0]["t_side"] == "POSITIVE_T",
            f"outcome-blind positive-t owner:{key_sha256}",
        )
        graph_rows = [
            row for row in pair_rows
            if row["target_2D_sheet_count"] == 1
        ]
        boundary_only_rows = [
            row for row in pair_rows
            if row["target_2D_sheet_count"] == 0
        ]
        require(
            len(graph_rows) == 1 and len(boundary_only_rows) == 1,
            f"one target graph side per pair:{key_sha256}",
        )
        pair_payload = [
            negative["pair_key"],
            negative["leaf_row_id"],
            positive["leaf_row_id"],
        ]
        pairs.append({
            "pair_row_id": f"round192-wall-owner-pair:{digest(pair_payload)}",
            "pair_key": negative["pair_key"],
            "pair_key_sha256": key_sha256,
            "negative_t_leaf_row_id": negative["leaf_row_id"],
            "negative_t_origin_row_id": negative["origin_row_id"],
            "positive_t_leaf_row_id": positive["leaf_row_id"],
            "positive_t_origin_row_id": positive["origin_row_id"],
            "common_t0_face_exact_bounds":
                negative["common_t0_face_exact_bounds"],
            "common_t0_face_byte_for_byte_equal": True,
            "common_t0_face_canonical_sha256":
                negative["common_t0_face_canonical_sha256"],
            "half_open_owner_policy":
                "OUTCOME_BLIND_POSITIVE_T_SIDE_OWNS__"
                "NEGATIVE_T_SIDE_IS_SHADOW",
            "half_open_owner_leaf_row_id": positive["leaf_row_id"],
            "half_open_shadow_leaf_row_id": negative["leaf_row_id"],
            "owner_count": 1,
            "source_2D_sheet_count_after_pair_deduplication": 1,
            "source_sheet_1D_boundary_edge_incidence_count": 4,
            "source_sheet_0D_corner_incidence_count": 4,
            "target_2D_sheet_count": 1,
            "target_graph_side": graph_rows[0]["t_side"],
            "target_graph_leaf_row_id": graph_rows[0]["leaf_row_id"],
            "target_boundary_only_side":
                boundary_only_rows[0]["t_side"],
            "source_target_1D_intersection_segment_count": 1,
            "source_target_0D_endpoint_incidence_count": 2,
            "paired_wall_product_zero_set":
                "SOURCE_T0_SHEET_UNION_ONE_CLIPPED_TARGET_2D_SHEET",
            "paired_wall_product_equivalent_to_source_t0_sheet_only":
                False,
            "whole_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
    return pairs


def main() -> int:
    ctx.prec = 256
    print("pinning Round179/Round182 chains", file=sys.stderr, flush=True)
    pins = check_inputs()
    print("loading and filtering Round182", file=sys.stderr, flush=True)
    scope182 = extract_round182_scope()
    print("loading and filtering Round179", file=sys.stderr, flush=True)
    scope179 = extract_round179_scope(
        scope182["occurrences"],
        scope182["origin_ids"],
    )

    rows: list[dict[str, Any]] = []
    for index, leaf in enumerate(
        sorted(scope182["residual_leaves"], key=lambda row: row["row_id"]),
        1,
    ):
        occurrence = leaf["occurrence_row_id"]
        collar = scope182["collars"][occurrence]
        origin_id = collar["origin_row_id"]
        retained = scope179["retained"][leaf["retained_child_row_id"]]
        rows.append(analyze_leaf(
            leaf,
            collar,
            scope179["walls"][occurrence],
            scope179["origins"][origin_id],
            scope182["origins"][origin_id],
            retained,
        ))
        if index % 16 == 0 or index == EXPECTED_WALL_RESIDUAL_LEAVES:
            print(
                f"wall leaves {index}/{EXPECTED_WALL_RESIDUAL_LEAVES}",
                file=sys.stderr,
                flush=True,
            )

    pairs = analyze_pairs(rows)
    target_classes = Counter(
        row["target_zero_classification"] for row in rows
    )
    graph_side_count = Counter(
        pair["target_graph_side"] for pair in pairs
    )
    require(
        Counter(row["t_side"] for row in rows)
        == Counter({"NEGATIVE_T": 32, "POSITIVE_T": 32}),
        "signed leaf census",
    )
    require(
        sum(row["target_2D_sheet_count"] for row in rows) == 32
        and sum(
            row["wall_product_equivalent_to_source_t0_sheet_only"]
            for row in rows
        ) == 32
        and graph_side_count["NEGATIVE_T"]
        + graph_side_count["POSITIVE_T"] == 32,
        "target sheet census",
    )
    require(
        all(
            row["target_wall_full_leaf_sign"] == "OVERWRAP"
            and row["target_wall_t0_face_sign"] == "OVERWRAP"
            and row["target_wall_exact_t0_p0_s_edge_zero"]
            for row in rows
        ),
        "target nonzero hypothesis exact refutation",
    )

    total_residual_volume = sum(
        (Q(row["coordinate_volume"]) for row in rows),
        Q(0),
    )
    total_closed_volume = sum(
        (
            Q(row["closed_Round182_retained_coordinate_volume"])
            for row in scope182["origins"].values()
        ),
        Q(0),
    )
    total_origin_volume = sum(
        (
            Q(row["Round179_retained_coordinate_volume"])
            for row in scope182["origins"].values()
        ),
        Q(0),
    )
    require(
        total_residual_volume == EXPECTED_WALL_RESIDUAL_VOLUME
        and total_closed_volume == EXPECTED_ALL_ORIGIN_CLOSED_VOLUME
        and total_origin_volume == EXPECTED_ALL_ORIGIN_RETAINED_VOLUME
        and total_closed_volume + total_residual_volume
        == total_origin_volume,
        "64-origin exact positive-volume conservation",
    )

    source_sheet_count = len(pairs)
    target_sheet_count = sum(
        pair["target_2D_sheet_count"] for pair in pairs
    )
    candidate_signature_regions = sum(
        row["target_open_3D_region_count"] for row in rows
    )
    require(
        source_sheet_count == 32
        and target_sheet_count == 32
        and candidate_signature_regions == 96,
        "dimension-safe arrangement census",
    )

    probe_result = {
        "status":
            "READ_ONLY_ZERO_PROMOTION_WALL_G_ENDPOINT_OWNER_PROBE",
        "question":
            "Are the 64 Round182 wall-G residual leaves only 32 duplicated "
            "t=0 source-wall sheets with a strictly nonzero target factor, "
            "so that outcome-blind half-open ownership closes the tail?",
        "verdict": "PARTIAL",
        "verdict_reason":
            "The 64 leaves pair exactly into 32 common t=0 source sheets "
            "and positive-t ownership is valid, but the target factor is "
            "exactly zero on every t=p=0 edge and one side of every pair "
            "contains an additional unique clipped target 2D graph.  The "
            "source-only zero-set and whole-tail closure hypotheses fail.",
        "subverdicts": {
            "frozen_tail_reconstruction": "VALIDATED",
            "exact_source_factor_t0_sheet": "VALIDATED",
            "32_pair_common_face_glue": "VALIDATED",
            "positive_t_half_open_owner": "VALIDATED",
            "target_factor_strictly_nonzero_on_full_leaf": "INVALIDATED",
            "target_factor_strictly_nonzero_on_t0_face": "INVALIDATED",
            "wall_product_zero_set_equals_source_t0_sheet_only":
                "INVALIDATED",
            "whole_tail_ready_for_credit": "INVALIDATED",
        },
        "probe": {
            "filename": PROBE.name,
            "sha256": hashlib.sha256(
                regular_file_bytes(PROBE, 2_000_000)
            ).hexdigest(),
            "precision_bits": 256,
            "runtime_filesystem_writes": 0,
            "output_path_option_exists": False,
        },
        "input_chain": pins,
        "frozen_scope": {
            "residual_wall_G_leaf_count": len(rows),
            "residual_wall_G_origin_count":
                len(scope182["origin_ids"]),
            "face_pattern_count": scope182["pattern_count"],
            "negative_t_leaf_count": sum(
                row["t_side"] == "NEGATIVE_T" for row in rows
            ),
            "positive_t_leaf_count": sum(
                row["t_side"] == "POSITIVE_T" for row in rows
            ),
            "pair_count": len(pairs),
            "single_leaf_exact_coordinate_volume":
                str(EXPECTED_SINGLE_LEAF_VOLUME),
            "tail_exact_coordinate_volume":
                str(total_residual_volume),
        },
        "source_wall_factor": {
            "E_or_W_coordinate": "source_y",
            "N_or_S_coordinate": "source_x",
            "integer_wall": 0,
            "exact_factorization": "(9/25)*t",
            "exact_zero_set": "t=0",
            "strict_t_derivative": "9/25",
            "paired_source_2D_sheet_count": source_sheet_count,
            "paired_source_sheet_1D_boundary_edge_incidence_count":
                4 * source_sheet_count,
            "paired_source_sheet_0D_corner_incidence_count":
                4 * source_sheet_count,
        },
        "target_wall_factor": {
            "full_leaf_strict_nonzero_count": sum(
                row["target_wall_full_leaf_sign"] in STRICT_SIGNS
                for row in rows
            ),
            "t0_face_strict_nonzero_count": sum(
                row["target_wall_t0_face_sign"] in STRICT_SIGNS
                for row in rows
            ),
            "exact_t0_p0_s_zero_edge_count": sum(
                row["target_wall_exact_t0_p0_s_edge_zero"]
                for row in rows
            ),
            "classification_count": dict(sorted(target_classes.items())),
            "additional_clipped_target_2D_sheet_count":
                target_sheet_count,
            "source_target_1D_intersection_segment_count":
                len(pairs),
            "source_target_0D_endpoint_incidence_count":
                2 * len(pairs),
            "target_graph_side_count":
                dict(sorted(graph_side_count.items())),
        },
        "ownership": {
            "pairing_key":
                "(chart,owner_target,wall_axis,integer_wall,"
                "p0,p1,s0,s1)",
            "common_face_byte_for_byte_equal_pair_count": sum(
                pair["common_t0_face_byte_for_byte_equal"]
                for pair in pairs
            ),
            "policy":
                "OUTCOME_BLIND_POSITIVE_T_SIDE_OWNS__"
                "NEGATIVE_T_SIDE_IS_SHADOW",
            "owner_count": sum(pair["owner_count"] for pair in pairs),
            "shadow_count": len(pairs),
            "each_face_has_exactly_one_owner": True,
        },
        "dimension_safe_ledger": {
            "ambient_3D": {
                "64_origin_Round179_retained_coordinate_volume":
                    str(total_origin_volume),
                "Round182_already_closed_coordinate_volume":
                    str(total_closed_volume),
                "wall_tail_positive_coordinate_volume":
                    str(total_residual_volume),
                "exact_conservation":
                    total_closed_volume + total_residual_volume
                    == total_origin_volume,
                "other_Round182_closed_leaf_count": 7 * len(rows),
                "candidate_strict_open_region_count_after_arrangement":
                    candidate_signature_regions,
                "newly_credited_coordinate_volume": "0",
            },
            "regular_2D": {
                "deduplicated_source_t0_sheet_count":
                    source_sheet_count,
                "additional_target_clipped_sheet_count":
                    target_sheet_count,
                "no_3D_volume_subtraction": True,
            },
            "intersection_1D": {
                "source_target_segment_count": len(pairs),
                "source_sheet_boundary_edge_incidence_count":
                    4 * source_sheet_count,
                "not_counted_as_2D_or_3D_credit": True,
            },
            "boundary_0D": {
                "source_target_endpoint_incidence_count":
                    2 * len(pairs),
                "source_sheet_corner_incidence_count":
                    4 * source_sheet_count,
                "incidences_not_global_component_counts": True,
            },
        },
        "side_specific_local_signature_feasibility": {
            "boundary_only_residual_leaf_count": sum(
                row["target_2D_sheet_count"] == 0 for row in rows
            ),
            "one_open_region_candidate_on_boundary_only_leaf_count": 32,
            "target_graph_residual_leaf_count": sum(
                row["target_2D_sheet_count"] == 1 for row in rows
            ),
            "two_open_region_candidates_on_target_graph_leaf_count": 32,
            "candidate_region_total": candidate_signature_regions,
            "geometry_partition_feasible": True,
            "return_signatures_materialized": 0,
            "whole_original_tubes_certified": 0,
            "required_formal_work":
                "materialize the 32 clipped target sheets, their t=0,p=0 "
                "intersection lines and endpoints, then evaluate and glue "
                "side-specific local return signatures for all 96 open "
                "regions with an independent verifier",
        },
        "leaf_evidence_row_count": len(rows),
        "leaf_evidence_rows_sha256": digest(rows),
        "leaf_evidence_rows": rows,
        "pair_evidence_row_count": len(pairs),
        "pair_evidence_rows_sha256": digest(pairs),
        "pair_evidence_rows": pairs,
        "zero_promotion_contract": {
            "probe_only": True,
            "whole_tube_credit_issued": 0,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator": 224580,
            "D02": "UNCHANGED_BLOCKED",
            "global_Gate5_fields": "UNCHANGED_10/18",
            "CM2": "UNCHANGED_NO_GO",
        },
        "recommendation":
            "Do not certify the tail as a source-sheet-only boundary glue. "
            "Formalize a two-sheet wall-product arrangement per pair: one "
            "owned source t=0 sheet plus one clipped target graph ending on "
            "their p=0 intersection line, followed by side-specific return "
            "signature reconstruction and independent verification.",
    }
    document = {
        "schema": SCHEMA,
        "probe_result": probe_result,
        "probe_result_sha256": digest(probe_result),
    }
    sys.stdout.write(
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
