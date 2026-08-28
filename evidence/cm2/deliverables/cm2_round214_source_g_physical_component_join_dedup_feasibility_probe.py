#!/usr/bin/env python3
"""Bounded physical-component join probe for the Round211 source-G strata.

This is deliberately not a component certificate.  It computes the strongest
duplicate-incidence quotient supported by explicit Round208/Round211 data:
exact t-face curve carriers and exact endpoint carriers are identified only
inside one frozen occurrence.  It separately probes wider p/s and
cross-occurrence contacts with strict Arb zero witnesses, but those witnesses
are feasibility evidence only because no p/s internal-face incidence IDs or
cross-occurrence glue rows are carried by Round208/Round211.

No whole-leaf, whole-origin, whole-tube, global component, or exact-key
disposition credit is issued.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable

from flint import ctx

import cm2_round186_source_g_factor_face_probe as r186
import cm2_round209_source_g_outgoing_half_open_owner_probe as r209


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round214.source-g-physical-component-join-dedup-probe.v1"
STATUS = (
    "BOUNDED_DUPLICATE_INCIDENCE_QUOTIENT__PHYSICAL_COMPONENT_JOIN_"
    "INCOMPLETE__ZERO_PROMOTION"
)
MAX_INPUT_BYTES = 300 * 1024 * 1024

R211_SOURCE = (
    "cm2_round211_source_g_outgoing_half_open_owner_materialization.py"
)
R211_CERTIFICATE = (
    "cm2_round211_source_g_outgoing_half_open_owner_materialization"
    "_certificate.json"
)
R211_SOURCE_SHA256 = (
    "9e8874672150d7585316524a7724070f4543e231de5481d1c1dfbd00ddc65a02"
)
R211_CERTIFICATE_SHA256 = (
    "bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f"
)
R211_RESULT_SHA256 = (
    "3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b"
)

R204_CERTIFICATE = (
    "cm2_round204_source_g_wall_return_signature_local_replacement"
    "_certificate.json"
)
R204_CERTIFICATE_SHA256 = (
    "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818"
)
R204_RESULT_SHA256 = (
    "ef106d06399094a453eb5e66d73a0022a9bb5343f8c4788b3a3fbc9177d45ccd"
)

R209_SOURCE = "cm2_round209_source_g_outgoing_half_open_owner_probe.py"
R209_SOURCE_SHA256 = (
    "dcd8d6d2354151a0aa1c45db8f1ce78f1385b665741ee5a79521bf261cebc13f"
)
R186_SOURCE = "cm2_round186_source_g_factor_face_probe.py"
R186_SOURCE_SHA256 = (
    "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64"
)

EXPECTED_SHEETS = 17_716
EXPECTED_CURVES = 20_456
EXPECTED_ENDPOINTS = 40_912
EXPECTED_U2 = 88
EXPECTED_OUTGOING_ORDINALS = 24
EXPECTED_WALL_ORDINALS = 12
EXPECTED_LOCAL_ORDINAL_UNION = 36
EXPECTED_SOURCE_G_EXACT_KEYS = 224_580
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}


class Round214Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round214Error(label)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def regular_bytes(path: Path, maximum: int = MAX_INPUT_BYTES) -> bytes:
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(before.st_nlink == 1, f"hardlink:{path.name}")
    require(0 < before.st_size <= maximum, f"size:{path.name}")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns)
            == (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            ),
            f"stable-open:{path.name}",
        )
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            require(total <= maximum, f"bounded-read:{path.name}")
            chunks.append(chunk)
        after = os.fstat(descriptor)
        require(
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            == (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            ),
            f"stable-read:{path.name}",
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def pinned_bytes(path: Path, expected: str, maximum: int) -> bytes:
    raw = regular_bytes(path, maximum)
    require(
        hashlib.sha256(raw).hexdigest() == expected,
        f"SHA256:{path.name}",
    )
    return raw


def histogram(values: Iterable[Any]) -> dict[str, int]:
    return dict(sorted(Counter(str(value) for value in values).items()))


class UnionFind:
    def __init__(self, nodes: Iterable[str]) -> None:
        self.parent = {node: node for node in nodes}
        self.size = {node: 1 for node in self.parent}

    def find(self, node: str) -> str:
        root = node
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[node] != node:
            following = self.parent[node]
            self.parent[node] = root
            node = following
        return root

    def join(self, left: str, right: str) -> bool:
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return False
        if self.size[left] < self.size[right]:
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]
        return True

    def groups(self) -> dict[str, list[str]]:
        result: dict[str, list[str]] = defaultdict(list)
        for node in self.parent:
            result[self.find(node)].append(node)
        for rows in result.values():
            rows.sort()
        return dict(result)


def validate_inputs() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[int],
    dict[str, str],
]:
    require(
        Path(r209.__file__).resolve() == (HERE / R209_SOURCE).resolve(),
        "Round209 module identity",
    )
    require(
        Path(r186.__file__).resolve() == (HERE / R186_SOURCE).resolve(),
        "Round186 module identity",
    )
    pinned_bytes(HERE / R211_SOURCE, R211_SOURCE_SHA256, 5_000_000)
    raw211 = pinned_bytes(
        HERE / R211_CERTIFICATE,
        R211_CERTIFICATE_SHA256,
        MAX_INPUT_BYTES,
    )
    pinned_bytes(HERE / R209_SOURCE, R209_SOURCE_SHA256, 5_000_000)
    pinned_bytes(HERE / R186_SOURCE, R186_SOURCE_SHA256, 5_000_000)
    raw204 = pinned_bytes(
        HERE / R204_CERTIFICATE,
        R204_CERTIFICATE_SHA256,
        20_000_000,
    )

    certificate211 = json.loads(raw211)
    require(
        certificate211["result_sha256"] == R211_RESULT_SHA256
        and digest(certificate211["result"]) == R211_RESULT_SHA256,
        "Round211 result closure",
    )
    certificate204 = json.loads(raw204)
    require(
        certificate204["result_sha256"] == R204_RESULT_SHA256
        and digest(certificate204["result"]) == R204_RESULT_SHA256,
        "Round204 result closure",
    )

    _r173, r208, input_hashes = r209.validate_inputs()
    leaves, regions, _faces, u2_rows = r209.validate_round195_geometry(r208)
    sheets, curves, endpoints, _owner_audit = r209.build_lineages(
        leaves,
        regions,
    )
    require(
        len(sheets) == EXPECTED_SHEETS
        and len(curves) == EXPECTED_CURVES
        and len(endpoints) == EXPECTED_ENDPOINTS
        and len(u2_rows) == EXPECTED_U2,
        "Round209 reconstructed dimensional census",
    )

    ledgers = (
        (
            certificate211["result"]["formal_2D_sheet_owner_ledger"]["rows"],
            sheets,
            "probe_sheet_row_id",
            "sheet_row_id",
        ),
        (
            certificate211["result"][
                "formal_1D_curve_incidence_owner_ledger"
            ]["rows"],
            curves,
            "probe_curve_row_id",
            "curve_row_id",
        ),
        (
            certificate211["result"][
                "formal_0D_endpoint_incidence_owner_ledger"
            ]["rows"],
            endpoints,
            "probe_endpoint_row_id",
            "endpoint_row_id",
        ),
    )
    for formal_rows, probe_rows, probe_id_key, raw_id_key in ledgers:
        formal = {
            row[probe_id_key]: row["probe_" + raw_id_key.split("_", 1)[0]
                                        + "_row_sha256"]
            for row in formal_rows
        }
        expected = {
            row[raw_id_key]: row["row_sha256"] for row in probe_rows
        }
        require(formal == expected, f"Round211 exact probe lineage:{raw_id_key}")
        require(
            all(
                row["component_deduplication_credit"] == 0
                and row["whole_leaf_credit"] == 0
                and row["whole_origin_credit"] == 0
                and row["whole_original_tube_credit"] == 0
                and row["global_exact_key_disposition_credit"] == 0
                for row in formal_rows
            ),
            f"Round211 zero component promotion:{raw_id_key}",
        )

    wall_ordinals = certificate204["result"][
        "exact_key_local_join_ledger"
    ]["official_key_ordinals"]
    require(
        len(wall_ordinals) == EXPECTED_WALL_ORDINALS
        and len(set(wall_ordinals)) == EXPECTED_WALL_ORDINALS,
        "Round204 ordinal census",
    )
    hashes = {
        "Round211_source_sha256": R211_SOURCE_SHA256,
        "Round211_certificate_sha256": R211_CERTIFICATE_SHA256,
        "Round211_result_sha256": R211_RESULT_SHA256,
        "Round209_probe_source_sha256": R209_SOURCE_SHA256,
        "Round186_factor_evaluator_source_sha256": R186_SOURCE_SHA256,
        "Round204_certificate_sha256": R204_CERTIFICATE_SHA256,
        "Round204_result_sha256": R204_RESULT_SHA256,
        "Round208_certificate_sha256":
            input_hashes["Round208_certificate_sha256"],
        "Round208_result_sha256": input_hashes["Round208_result_sha256"],
    }
    return (
        leaves,
        regions,
        u2_rows,
        sheets,
        curves,
        endpoints,
        wall_ordinals,
        hashes,
    )


def component_digest(groups: dict[str, list[str]]) -> str:
    rows = sorted(sorted(members) for members in groups.values())
    return digest(rows)


def build_result(probe_source_sha256: str) -> dict[str, Any]:
    print("Round214 validating pinned R211/R208/R204 boundary", file=sys.stderr)
    (
        leaves,
        regions,
        u2_rows,
        sheets,
        curves,
        endpoints,
        wall_ordinals,
        input_hashes,
    ) = validate_inputs()

    leaf_by_id = {row["leaf_row_id"]: row for row in leaves}
    region_by_id = {row["region_row_id"]: row for row in regions}
    sheet_by_leaf = {row["leaf_row_id"]: row for row in sheets}
    curves_by_leaf: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in curves:
        curves_by_leaf[row["leaf_row_id"]].append(row)
    boxes = {
        leaf_id: tuple(Q(value) for value in leaf_by_id[leaf_id]["box"])
        for leaf_id in sheet_by_leaf
    }
    parent_by_leaf = {
        row["leaf_row_id"]: row["parent_id"] for row in regions
        if row["leaf_row_id"] in sheet_by_leaf
    }
    occurrence_by_leaf = {
        leaf_id: row["occurrence_row_id"]
        for leaf_id, row in sheet_by_leaf.items()
    }
    origin_by_leaf = {
        leaf_id: row["origin_row_id"]
        for leaf_id, row in sheet_by_leaf.items()
    }

    identity_by_leaf: dict[str, tuple[Any, ...]] = {}
    ordinal_by_leaf: dict[str, int] = {}
    evaluator_by_leaf: dict[str, tuple[str, str, str]] = {}
    for leaf_id, sheet in sheet_by_leaf.items():
        owner = region_by_id[sheet["owner_region_row_id"]]
        signature = owner["local_return_signature"]
        identity_by_leaf[leaf_id] = (
            parent_by_leaf[leaf_id],
            signature["source_chart"],
            signature["target_lift"],
            tuple(signature["signed_wall_word"]),
            signature["roof"],
            sheet["active_factor"],
            sheet["owner_outgoing_cell"],
            sheet["owner_signature_core_sha256"],
        )
        ordinal_by_leaf[leaf_id] = signature["official_key_ordinal"]
        evaluator_by_leaf[leaf_id] = (
            signature["source_chart"],
            signature["target_lift"],
            sheet["active_factor"],
        )

    def curve_carrier(row: dict[str, Any]) -> tuple[Any, ...]:
        leaf_id = row["leaf_row_id"]
        box = boxes[leaf_id]
        t_value = box[0] if row["face_side"] == "LOWER" else box[1]
        return identity_by_leaf[leaf_id] + (
            t_value,
            box[2],
            box[3],
            box[4],
            box[5],
        )

    def endpoint_carrier(row: dict[str, Any]) -> tuple[Any, ...]:
        leaf_id = row["leaf_row_id"]
        box = boxes[leaf_id]
        t_value = box[0] if row["face_side"] == "LOWER" else box[1]
        edge = row["boundary_edge"]
        if edge == "S":
            geometry = ("s", box[4], box[2], box[3])
        elif edge == "N":
            geometry = ("s", box[5], box[2], box[3])
        elif edge == "W":
            geometry = ("p", box[2], box[4], box[5])
        else:
            require(edge == "E", "endpoint edge")
            geometry = ("p", box[3], box[4], box[5])
        return identity_by_leaf[leaf_id] + (t_value,) + geometry

    global_curve_carriers: dict[tuple[Any, ...], list[dict[str, Any]]] = (
        defaultdict(list)
    )
    global_endpoint_carriers: dict[tuple[Any, ...], list[dict[str, Any]]] = (
        defaultdict(list)
    )
    for row in curves:
        global_curve_carriers[curve_carrier(row)].append(row)
    for row in endpoints:
        global_endpoint_carriers[endpoint_carrier(row)].append(row)

    sheet_uf = UnionFind(sheet_by_leaf)
    curve_uf = UnionFind(row["curve_row_id"] for row in curves)
    endpoint_uf = UnionFind(row["endpoint_row_id"] for row in endpoints)
    safe_curve_groups: dict[tuple[Any, ...], list[dict[str, Any]]] = (
        defaultdict(list)
    )
    safe_endpoint_groups: dict[tuple[Any, ...], list[dict[str, Any]]] = (
        defaultdict(list)
    )
    for row in curves:
        safe_curve_groups[
            curve_carrier(row)
            + (occurrence_by_leaf[row["leaf_row_id"]],)
        ].append(row)
    for row in endpoints:
        safe_endpoint_groups[
            endpoint_carrier(row)
            + (occurrence_by_leaf[row["leaf_row_id"]],)
        ].append(row)

    for rows in safe_curve_groups.values():
        first = rows[0]
        for row in rows[1:]:
            curve_uf.join(first["curve_row_id"], row["curve_row_id"])
            sheet_uf.join(first["leaf_row_id"], row["leaf_row_id"])
    for rows in safe_endpoint_groups.values():
        first = rows[0]
        for row in rows[1:]:
            endpoint_uf.join(first["endpoint_row_id"], row["endpoint_row_id"])
            curve_uf.join(first["curve_row_id"], row["curve_row_id"])
            sheet_uf.join(first["leaf_row_id"], row["leaf_row_id"])

    global_endpoint_leaf_pairs: set[tuple[str, str]] = set()
    for rows in global_endpoint_carriers.values():
        leaf_ids = sorted({row["leaf_row_id"] for row in rows})
        for index, left in enumerate(leaf_ids):
            for right in leaf_ids[index + 1:]:
                global_endpoint_leaf_pairs.add((left, right))

    lower_faces: dict[tuple[str, str, Q], list[str]] = defaultdict(list)
    upper_faces: dict[tuple[str, str, Q], list[str]] = defaultdict(list)
    for leaf_id, box in boxes.items():
        for axis_index, axis in enumerate("tps"):
            lower_faces[
                (parent_by_leaf[leaf_id], axis, box[2 * axis_index])
            ].append(leaf_id)
            upper_faces[
                (parent_by_leaf[leaf_id], axis, box[2 * axis_index + 1])
            ].append(leaf_id)

    ctx.prec = 256
    atlas_box = r186.r179.r174.atlas.AtlasBox
    arb_sign = r186.r179.arb_sign

    def strict_bracket(
        leaf_id: str,
        axis: str,
        fixed: Q,
        interval: tuple[Q, Q],
        other: Q,
    ) -> tuple[bool, tuple[str, str, str]]:
        chart, target, active = evaluator_by_leaf[leaf_id]
        lower, upper = interval
        if axis == "p":
            def make(a: Q, b: Q) -> Any:
                return atlas_box(a, b, fixed, fixed, other, other, 0, "r214")
            derivative_index = 0
        elif axis == "s":
            def make(a: Q, b: Q) -> Any:
                return atlas_box(a, b, other, other, fixed, fixed, 0, "r214")
            derivative_index = 0
        elif axis == "tp":
            def make(a: Q, b: Q) -> Any:
                return atlas_box(fixed, fixed, a, b, other, other, 0, "r214")
            derivative_index = 1
        else:
            require(axis == "ts", "strict bracket axis")
            def make(a: Q, b: Q) -> Any:
                return atlas_box(fixed, fixed, other, other, a, b, 0, "r214")
            derivative_index = 2
        lower_dual = r186.factor_geometry(chart, target, make(lower, lower))[
            active
        ]
        upper_dual = r186.factor_geometry(chart, target, make(upper, upper))[
            active
        ]
        line_dual = r186.factor_geometry(chart, target, make(lower, upper))[
            active
        ]
        signs = (
            arb_sign(lower_dual[0]),
            arb_sign(upper_dual[0]),
            arb_sign(line_dual[1][derivative_index]),
        )
        return (
            signs[0] in STRICT_SIGNS
            and signs[1] in STRICT_SIGNS
            and signs[0] != signs[1]
            and signs[2] in STRICT_SIGNS,
            signs,
        )

    touch_counts: Counter[str] = Counter()
    feasibility_counts: Counter[str] = Counter()
    unresolved_rows: list[dict[str, Any]] = []
    positive_face_count = 0
    safe_explicit_t_face_count = 0

    print("Round214 enumerating exact and partial contacts", file=sys.stderr)
    for key, lower_leaf_ids in lower_faces.items():
        _parent, axis, coordinate = key
        axis_index = "tps".index(axis)
        other_axes = [index for index in range(3) if index != axis_index]
        for upper_leaf in upper_faces.get(key, []):
            for lower_leaf in lower_leaf_ids:
                if (
                    upper_leaf == lower_leaf
                    or identity_by_leaf[upper_leaf]
                    != identity_by_leaf[lower_leaf]
                ):
                    continue
                upper_box = boxes[upper_leaf]
                lower_box = boxes[lower_leaf]
                overlaps = [
                    (
                        max(upper_box[2 * index], lower_box[2 * index]),
                        min(
                            upper_box[2 * index + 1],
                            lower_box[2 * index + 1],
                        ),
                    )
                    for index in other_axes
                ]
                if any(lower > upper for lower, upper in overlaps):
                    continue
                dimension = sum(lower < upper for lower, upper in overlaps)
                exact = all(
                    upper_box[2 * index:2 * index + 2]
                    == lower_box[2 * index:2 * index + 2]
                    for index in other_axes
                )
                if occurrence_by_leaf[upper_leaf] == occurrence_by_leaf[
                    lower_leaf
                ]:
                    relation = "SAME_OCCURRENCE"
                elif origin_by_leaf[upper_leaf] == origin_by_leaf[lower_leaf]:
                    relation = "SAME_ORIGIN_DIFFERENT_OCCURRENCE"
                else:
                    relation = "CROSS_ORIGIN"
                touch_counts[
                    f"{axis}|dimension={dimension}|"
                    f"{'EXACT' if exact else 'PARTIAL'}|{relation}"
                ] += 1
                if dimension != 2:
                    continue
                positive_face_count += 1

                method = "UNRESOLVED"
                signs: tuple[str, str, str] | None = None
                same_occurrence = (
                    occurrence_by_leaf[upper_leaf]
                    == occurrence_by_leaf[lower_leaf]
                )
                if axis == "t" and exact:
                    shared = (
                        {curve_carrier(row)
                         for row in curves_by_leaf[upper_leaf]}
                        & {curve_carrier(row)
                           for row in curves_by_leaf[lower_leaf]}
                    )
                    require(bool(shared), "exact t face curve carrier")
                    if same_occurrence:
                        method = "SAFE_EXPLICIT_T_FACE_CURVE_DUPLICATE"
                        safe_explicit_t_face_count += 1
                    else:
                        method = (
                            "CROSS_OCCURRENCE_EXACT_CURVE_CARRIER_CANDIDATE"
                        )
                else:
                    if axis == "p":
                        (t0, t1), (s0, s1) = overlaps
                        proved, signs = strict_bracket(
                            upper_leaf,
                            "p",
                            coordinate,
                            (t0, t1),
                            (s0 + s1) / 2,
                        )
                    elif axis == "s":
                        (t0, t1), (p0, p1) = overlaps
                        proved, signs = strict_bracket(
                            upper_leaf,
                            "s",
                            coordinate,
                            (t0, t1),
                            (p0 + p1) / 2,
                        )
                    else:
                        (p0, p1), (s0, s1) = overlaps
                        proved, signs = strict_bracket(
                            upper_leaf,
                            "tp",
                            coordinate,
                            (p0, p1),
                            (s0 + s1) / 2,
                        )
                        if not proved:
                            proved, signs = strict_bracket(
                                upper_leaf,
                                "ts",
                                coordinate,
                                (s0, s1),
                                (p0 + p1) / 2,
                            )
                    if proved:
                        method = "NONPROMOTIONAL_STRICT_ZERO_WITNESS"
                    elif tuple(sorted((upper_leaf, lower_leaf))) in (
                        global_endpoint_leaf_pairs
                    ):
                        method = (
                            "NONPROMOTIONAL_EXACT_ENDPOINT_CARRIER_CANDIDATE"
                        )

                feasibility_counts[
                    f"{axis}|{'EXACT' if exact else 'PARTIAL'}|"
                    f"{relation}|{method}"
                ] += 1
                if method == "UNRESOLVED":
                    unresolved_rows.append({
                        "axis": axis,
                        "relation": relation,
                        "exact_full_face": exact,
                        "upper_leaf_row_id": upper_leaf,
                        "lower_leaf_row_id": lower_leaf,
                        "shared_coordinate": str(coordinate),
                        "positive_overlap_intervals": [
                            [str(lower), str(upper)]
                            for lower, upper in overlaps
                        ],
                        "midline_signs": list(signs) if signs else None,
                        "reason": (
                            "NO_STRICT_MIDLINE_ZERO_WITNESS_AND_NO_EXACT_"
                            "ENDPOINT_CARRIER;_PHYSICAL_JOIN_UNDECIDED"
                        ),
                    })

    require(positive_face_count == 15_540, "positive face census")
    require(safe_explicit_t_face_count == 4_260, "safe t-face census")
    require(len(unresolved_rows) == 264, "bounded unresolved face census")

    sheet_groups = sheet_uf.groups()
    curve_groups = curve_uf.groups()
    endpoint_groups = endpoint_uf.groups()
    outgoing_ordinals = sorted(set(ordinal_by_leaf.values()))
    wall_ordinals = sorted(wall_ordinals)
    require(
        len(outgoing_ordinals) == EXPECTED_OUTGOING_ORDINALS
        and set(outgoing_ordinals).isdisjoint(wall_ordinals)
        and len(set(outgoing_ordinals) | set(wall_ordinals))
        == EXPECTED_LOCAL_ORDINAL_UNION,
        "36 local ordinal disjoint union",
    )
    impure_sheet_blocks = 0
    blocks_per_ordinal: Counter[int] = Counter()
    for members in sheet_groups.values():
        ordinals = {ordinal_by_leaf[leaf_id] for leaf_id in members}
        if len(ordinals) != 1:
            impure_sheet_blocks += 1
        else:
            blocks_per_ordinal[next(iter(ordinals))] += 1
    require(impure_sheet_blocks == 0, "safe sheet block ordinal purity")

    u2_bad_joins: list[str] = []
    u2_two_curve_count = 0
    for row in u2_rows:
        curve_ids = [
            curve["curve_row_id"]
            for curve in curves_by_leaf[row["leaf_row_id"]]
        ]
        if len(curve_ids) == 2:
            u2_two_curve_count += 1
            if curve_uf.find(curve_ids[0]) == curve_uf.find(curve_ids[1]):
                u2_bad_joins.append(row["leaf_row_id"])
    require(
        u2_two_curve_count == 76 and not u2_bad_joins,
        "U|U strict curve-pair separation",
    )

    def carrier_audit(
        groups: dict[tuple[Any, ...], list[dict[str, Any]]],
    ) -> dict[str, Any]:
        occurrence_multiplicity: Counter[str] = Counter()
        cross_occurrence_groups = 0
        for rows in groups.values():
            occurrences = {
                occurrence_by_leaf[row["leaf_row_id"]] for row in rows
            }
            occurrence_multiplicity[
                f"rows={len(rows)}|occurrences={len(occurrences)}"
            ] += 1
            cross_occurrence_groups += len(occurrences) > 1
        return {
            "exact_carrier_count": len(groups),
            "row_multiplicity_histogram":
                histogram(len(rows) for rows in groups.values()),
            "row_and_occurrence_multiplicity_count":
                dict(sorted(occurrence_multiplicity.items())),
            "cross_occurrence_exact_carrier_count":
                cross_occurrence_groups,
        }

    return {
        "status": STATUS,
        "verdict": (
            "BOUNDED_PROBE_ONLY__SAFE_SAME_OCCURRENCE_DUPLICATE_INCIDENCE_"
            "QUOTIENT_EXISTS__FULL_PHYSICAL_COMPONENT_JOIN_NOT_YET_FORMAL"
        ),
        "input_binding": {
            **input_hashes,
            "Round211_rows_joined_back_to_pinned_Round209_lineages": True,
            "Round211_producer_imported_or_executed": False,
            "Round204_used_only_for_12_ordinal_disjoint_union_audit": True,
            "Round186_used_as_nonpromotional_factor_evaluator": True,
            "probe_is_formal_certificate": False,
        },
        "raw_dimensional_incidence_census": {
            "sheet_rows": len(sheets),
            "curve_rows": len(curves),
            "endpoint_rows": len(endpoints),
            "U_pipe_U_rows": len(u2_rows),
        },
        "exact_carrier_audit": {
            "curve": carrier_audit(global_curve_carriers),
            "endpoint": carrier_audit(global_endpoint_carriers),
            "same_occurrence_curve_carrier_partition_count":
                len(safe_curve_groups),
            "same_occurrence_endpoint_carrier_partition_count":
                len(safe_endpoint_groups),
        },
        "safe_duplicate_incidence_quotient": {
            "scope": (
                "EXACT_T_FACE_CURVE_AND_ENDPOINT_CARRIERS_PARTITIONED_BY_"
                "FROZEN_OCCURRENCE;NOT_FULL_PHYSICAL_COMPONENTS"
            ),
            "explicit_safe_t_face_curve_duplicate_count":
                safe_explicit_t_face_count,
            "sheet_block_count": len(sheet_groups),
            "sheet_block_size_histogram":
                histogram(len(rows) for rows in sheet_groups.values()),
            "sheet_block_membership_sha256": component_digest(sheet_groups),
            "curve_block_count": len(curve_groups),
            "curve_block_size_histogram":
                histogram(len(rows) for rows in curve_groups.values()),
            "curve_block_membership_sha256": component_digest(curve_groups),
            "endpoint_block_count": len(endpoint_groups),
            "endpoint_block_size_histogram":
                histogram(len(rows) for rows in endpoint_groups.values()),
            "endpoint_block_membership_sha256":
                component_digest(endpoint_groups),
            "physical_component_count_claimed": False,
        },
        "contact_and_feasibility_audit": {
            "all_box_touch_count":
                dict(sorted(touch_counts.items())),
            "positive_area_face_contact_count": positive_face_count,
            "positive_area_method_count":
                dict(sorted(feasibility_counts.items())),
            "formal_or_promotional_use_of_strict_zero_witnesses": False,
            "p_or_s_internal_face_incidence_rows_available": False,
            "cross_occurrence_glue_rows_available": False,
            "unresolved_positive_area_candidate_join_count":
                len(unresolved_rows),
            "unresolved_candidate_rows_sha256": digest(unresolved_rows),
            "unresolved_candidate_rows": unresolved_rows,
        },
        "U_pipe_U_nonmerge_audit": {
            "sheet_count": EXPECTED_U2,
            "two_curve_strictly_ordered_and_disjoint_leaf_count": 76,
            "one_curve_other_t_face_absent_leaf_count": 12,
            "lower_upper_curve_pair_joined_by_safe_quotient_count": 0,
            "curve_pair_intersection_credit": 0,
        },
        "local_ordinal_audit": {
            "outgoing_Round211_ordinal_count": len(outgoing_ordinals),
            "outgoing_Round211_ordinals_sha256": digest(outgoing_ordinals),
            "separate_Round204_wall_ordinal_count": len(wall_ordinals),
            "separate_Round204_wall_ordinals_sha256": digest(wall_ordinals),
            "sets_are_disjoint": True,
            "local_ordinal_union_count": EXPECTED_LOCAL_ORDINAL_UNION,
            "local_ordinal_union_sha256":
                digest(sorted(outgoing_ordinals + wall_ordinals)),
            "safe_sheet_block_cross_ordinal_join_count":
                impure_sheet_blocks,
            "safe_sheet_blocks_per_outgoing_ordinal_histogram":
                histogram(blocks_per_ordinal.values()),
            "global_ordinal_fibre_exhaustion_claimed": False,
        },
        "first_missing_frontier": {
            "missing_p_or_s_internal_face_trace_rows": True,
            "missing_cross_occurrence_boundary_glue_rows": True,
            "partial_positive_area_face_contacts": 644,
            "strict_or_exact_endpoint_feasibility_closed_partial_contacts":
                380,
            "still_unresolved_partial_positive_area_contacts": 264,
            "required_new_rows": [
                "p/s internal-face active-factor zero-trace incidence IDs",
                "cross-occurrence common-refinement/glue IDs",
                "partial-face curve restriction and endpoint-to-interior joins",
            ],
            "no_component_may_be_promoted_from_signature_core_or_box_"
            "contact_alone": True,
        },
        "zero_promotion_contract": {
            "probe_only": True,
            "formal_component_deduplication_credit": 0,
            "whole_leaf_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_component_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator":
                EXPECTED_SOURCE_G_EXACT_KEYS,
            "D02": "UNCHANGED_BLOCKED",
            "Gate5": "UNCHANGED_10/18",
            "CM2": "UNCHANGED_NO_GO",
        },
        "required_next": (
            "materialize p/s internal-face zero-trace incidences and explicit "
            "cross-occurrence common-refinement glue, then independently "
            "verify the resulting sheet/curve/endpoint component graph; the "
            "current quotient blocks must not be called physical components"
        ),
        "provenance": {
            "schema": SCHEMA,
            "probe_source_sha256": probe_source_sha256,
            "python_version": sys.version.split()[0],
            "python_flint_version": getattr(
                __import__("flint"), "__version__", "unknown"
            ),
            "effective_Arb_precision_bits": ctx.prec,
            "probe_only": True,
            "formal_upstream_files_modified": False,
        },
    }


def main() -> int:
    source_sha256 = hashlib.sha256(
        regular_bytes(Path(__file__), 5_000_000)
    ).hexdigest()
    result = build_result(source_sha256)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    sys.stdout.buffer.write(canonical_bytes(envelope) + b"\n")
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
