#!/usr/bin/env python3
"""Independent verifier for the Round279 zero-credit collar freeze.

The verifier does not import the Round279 producer.  It independently:

* reconstructs the 332,016 canonical ``(Round182 leaf, signature)`` atoms
  from the five pinned signature certificates;
* rechecks the four Round271 artificial-split aliases with the pinned
  Round179 interval geometry evaluator;
* rebuilds the complete 330,724 true-support common-face candidate universe;
* checks exact, disjoint membership in the four frozen witness partitions;
* dynamically evaluates every positive-area face patch and both inward
  corridors with the pinned Round174 evaluator.

All verified rows remain zero-credit.  This verifier neither materializes new
expanded occurrences nor performs a DSU union.
"""
from __future__ import annotations

import argparse
import ast
import collections
import gzip
import hashlib
import json
import multiprocessing as mp
import os
import stat
import tempfile
import zlib
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174
import cm2_round179_source_g_residual_tube_arrangement_verifier as r179v


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round279_source_g_collar_atom_and_face_edge_freeze"
CERTIFICATE = HERE / f"{PREFIX}_certificate.json"
ATOM_LEDGER = HERE / f"{PREFIX}_atoms.json.gz"
EDGE_LEDGER = HERE / f"{PREFIX}_edges.json.gz"
VERIFICATION = HERE / f"{PREFIX}_verification.json"
SCHEMA = "cm2.round279.source-g-collar-atom-and-face-edge-freeze.v1"
PRODUCER_SOURCE = f"{PREFIX}.py"
DEPTH4_MATERIALIZER_SOURCE = (
    "cm2_round279_source_g_depth4_face_edge_witness_materialization.py"
)

R182 = "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
R208 = (
    "cm2_round208_source_g_outgoing_direct_signature_"
    "materialization_certificate.json"
)
R269 = (
    "cm2_round269_source_g_closed_collar_direct_signature_"
    "materialization_certificate.json"
)
R270 = (
    "cm2_round270_source_g_outgoing_g_factor_signature_"
    "materialization_certificate.json"
)
R271 = (
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_"
    "materialization_certificate.json"
)
R272 = (
    "cm2_round272_source_g_boundary_dual_factor_wall_"
    "closure_certificate.json"
)
DEPTH4 = "cm2_round279_source_g_depth4_face_edge_witnesses_zero_credit.json.gz"
DEPTH8 = "cm2_round277_source_g_depth8_new_match_patches_zero_credit.json.gz"
ACTIVE = (
    "cm2_round277_source_g_depth8_active_graph_"
    "face_edge_witnesses_zero_credit.json.gz"
)
R278_SOURCE = (
    "cm2_round278_source_g_round271_w_tail_"
    "artificial_split_alias_probe.py"
)
R174_SOURCE = (
    "cm2_round174_source_g_unique_first_dynamic_"
    "occurrence_materialization.py"
)
R179_EVALUATOR = "cm2_round179_source_g_residual_tube_arrangement_verifier.py"

SOURCES = (
    (208, R208, "formal_local_open_3D_signature_ledger", "leaf_row_id", "region_row_id"),
    (
        269,
        R269,
        "formal_direct_side_signature_ledger",
        "Round182_leaf_row_id",
        "signed_region_row_id",
    ),
    (
        270,
        R270,
        "formal_direct_side_signature_ledger",
        "Round182_leaf_row_id",
        "signed_region_row_id",
    ),
    (
        271,
        R271,
        "formal_side_signature_ledger",
        "Round182_leaf_row_id",
        "signed_region_row_id",
    ),
    (
        272,
        R272,
        "formal_side_signature_ledger",
        "Round182_leaf_row_id",
        "signed_region_row_id",
    ),
)

# The file pins make the source documents themselves inert bytes.  Result pins
# additionally document the intended frozen result object in each certificate.
RESULT_INPUT_PINS = {
    R182: (
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
        "9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269",
    ),
    R208: (
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
        "d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8",
    ),
    R269: (
        "472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3",
        "2e8071d2a99a206177f5293747bc7c7c9b1716184f4084c4f22fd3cf5bf45b7d",
    ),
    R270: (
        "72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea",
        "5c9c0585bf2cb664df493224f1005d4ef078d5e2f2e3044283019053b5e39add",
    ),
    R271: (
        "c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747",
        "30f509eb10b1a25c5195e672e980d7e4e651dadc3defd5e150245c6798060506",
    ),
    R272: (
        "16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2",
        "96eb126f34d819c97b9d50857d3207efad013a3c4e65d085f5b55270e8522354",
    ),
}

NONRESULT_INPUT_PINS = {
    DEPTH4: "26fb7aa461864a37e0b97ae5a4bbc419cf26dbdbc3378fcf2bd7644485a64ab9",
    DEPTH8: "fe6ea98eb8a374448378940677899360f5bb3d86c3fd5e32c4f994f05a1d603e",
    ACTIVE: "8a29604c937ea63fd1274ded5b131a3de8717b026aa576926e0d035754985f43",
    R278_SOURCE: "cc0a6885e402e40ae1255e538e18cb15ba71c4e311535feee251ee726a71dc83",
    R174_SOURCE: "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    R179_EVALUATOR: "292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679",
    DEPTH4_MATERIALIZER_SOURCE: (
        "e386a9ba5472205492def3e5f6cb622d12572e6d872acf765ab479fc9890c624"
    ),
}

PARTITION_COUNTS = {
    "DEPTH4_ADAPTIVE_STRICT_PATCH": 240_932,
    "DEPTH8_SAFE_PRUNED_STRICT_PATCH": 57_124,
    "ACTIVE_GRAPH_SIDE_STRICT_PATCH": 32_416,
    "P_ENDPOINT_WEDGE_STRICT_PATCH": 252,
}


class VerificationError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def duplicate_rejecting_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_json_constant(value: str) -> None:
    raise VerificationError(f"nonfinite JSON constant:{value}")


def strict_json_bytes(raw: bytes, label: str, maximum: int) -> Any:
    need(len(raw) <= maximum, f"{label}:JSON size limit")
    try:
        text = raw.decode("utf-8", errors="strict")
        decoder = json.JSONDecoder(
            object_pairs_hook=duplicate_rejecting_object,
            parse_constant=reject_json_constant,
        )
        value, end = decoder.raw_decode(text)
    except VerificationError:
        raise
    except Exception as error:
        raise VerificationError(f"{label}:strict JSON:{error}") from error
    need(not text[end:].strip(), f"{label}:trailing JSON bytes")
    return value


def strict_gzip_json_bytes(
    raw: bytes,
    label: str,
    maximum_compressed: int,
    maximum_uncompressed: int,
) -> Any:
    need(len(raw) <= maximum_compressed, f"{label}:compressed size limit")
    stream = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        decoded = stream.decompress(raw, maximum_uncompressed + 1)
        need(
            len(decoded) <= maximum_uncompressed,
            f"{label}:uncompressed size limit",
        )
        decoded += stream.flush()
    except VerificationError:
        raise
    except Exception as error:
        raise VerificationError(f"{label}:strict GZIP:{error}") from error
    need(
        len(decoded) <= maximum_uncompressed,
        f"{label}:uncompressed size limit after flush",
    )
    need(stream.eof, f"{label}:truncated GZIP member")
    need(not stream.unconsumed_tail, f"{label}:unconsumed GZIP bytes")
    need(not stream.unused_data, f"{label}:trailing/concatenated GZIP bytes")
    return strict_json_bytes(decoded, label, maximum_uncompressed)


def secure_local_regular(path: Path, label: str) -> Path:
    """Reject path escape, symlink, hardlink, directory, and special files."""

    absolute = path if path.is_absolute() else (Path.cwd() / path)
    need(not absolute.is_symlink(), f"{label}:symlink rejected")
    try:
        resolved = absolute.resolve(strict=True)
        metadata = os.lstat(absolute)
    except Exception as error:
        raise VerificationError(f"{label}:path resolution:{error}") from error
    need(resolved.parent == HERE.resolve(), f"{label}:path escape rejected")
    need(stat.S_ISREG(metadata.st_mode), f"{label}:regular file required")
    need(metadata.st_nlink == 1, f"{label}:hardlink rejected")
    return resolved


def secure_output_path(path: Path, label: str) -> Path:
    absolute = path if path.is_absolute() else (Path.cwd() / path)
    resolved_parent = absolute.parent.resolve(strict=True)
    need(resolved_parent == HERE.resolve(), f"{label}:output path escape")
    if absolute.exists() or absolute.is_symlink():
        secure_local_regular(absolute, label)
    return absolute.resolve(strict=False)


def atomic_write_json(path: Path, value: Any) -> None:
    target = secure_output_path(path, "verification output")
    payload = json.dumps(value, indent=2, sort_keys=True).encode() + b"\n"
    descriptor, temporary = tempfile.mkstemp(
        prefix=target.name + ".", dir=target.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def verify_cacheless_source_text(source: str, label: str) -> None:
    tree = ast.parse(source, filename=label)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            need(
                all(alias.name != "pickle" for alias in node.names),
                f"{label}:pickle import rejected",
            )
        if isinstance(node, ast.ImportFrom):
            need(node.module != "pickle", f"{label}:pickle import rejected")
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            need(
                "candidate_runtime_cache" not in node.value,
                f"{label}:runtime-cache path rejected",
            )


def verify_cacheless_source(path: Path, label: str) -> None:
    """Reject executable reads of the historical unpinned pickle cache."""

    verify_cacheless_source_text(path.read_text(encoding="utf-8"), label)


def verify_cacheless_source_text_for_attack(source: str) -> None:
    verify_cacheless_source_text(source, "attack poisoned runtime cache")


def load_pinned_result(name: str) -> dict[str, Any]:
    path = secure_local_regular(HERE / name, f"pinned input:{name}")
    raw = path.read_bytes()
    expected_file, expected_result = RESULT_INPUT_PINS[name]
    need(hashlib.sha256(raw).hexdigest() == expected_file, f"file pin:{name}")
    # These large historical sources are byte-pinned.  Strict parsing is
    # nevertheless retained with a bounded 512 MiB ceiling.
    document = strict_json_bytes(raw, name, 512 * 1024 * 1024)
    need(document["result_sha256"] == expected_result, f"result pin:{name}")
    return document["result"]


def load_pinned_gzip(name: str) -> dict[str, Any]:
    path = secure_local_regular(HERE / name, f"pinned input:{name}")
    need(file_sha256(path) == NONRESULT_INPUT_PINS[name], f"file pin:{name}")
    return strict_gzip_json_bytes(
        path.read_bytes(),
        name,
        maximum_compressed=256 * 1024 * 1024,
        maximum_uncompressed=512 * 1024 * 1024,
    )


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = result["row_column_schemas"][table]
    entry = result["table_census_and_sha256"][table]
    rows = result[table]
    need(len(rows) == entry["row_count"], f"table count:{table}")
    need(digest(rows) == entry["rows_sha256"], f"table digest:{table}")
    return [dict(zip(columns, row, strict=True)) for row in rows]


def qbox(values: list[str] | tuple[str, ...]) -> tuple[Q, ...]:
    result = tuple(Q(value) for value in values)
    need(len(result) == 6, "six box coordinates")
    return result


def positive_box(values: tuple[Q, ...]) -> bool:
    return all(values[2 * axis] < values[2 * axis + 1] for axis in range(3))


def merge_boxes(boxes: list[tuple[Q, ...]]) -> list[tuple[Q, ...]]:
    """Normalize an exact rectangular union without enlarging it."""

    work = sorted(set(boxes))
    changed = True
    while changed:
        changed = False
        for i, left in enumerate(work):
            for j in range(i + 1, len(work)):
                right = work[j]
                for axis in range(3):
                    if any(
                        left[2 * other : 2 * other + 2]
                        != right[2 * other : 2 * other + 2]
                        for other in range(3)
                        if other != axis
                    ):
                        continue
                    if left[2 * axis + 1] == right[2 * axis]:
                        merged = list(left)
                        merged[2 * axis + 1] = right[2 * axis + 1]
                    elif right[2 * axis + 1] == left[2 * axis]:
                        merged = list(right)
                        merged[2 * axis + 1] = left[2 * axis + 1]
                    else:
                        continue
                    work = [
                        item for k, item in enumerate(work) if k not in (i, j)
                    ] + [tuple(merged)]
                    work.sort()
                    changed = True
                    break
                if changed:
                    break
            if changed:
                break
    return work


def validate_closed_row(row: dict[str, Any], label: str) -> None:
    need("row_sha256" in row, f"{label}:row hash present")
    body = {key: value for key, value in row.items() if key != "row_sha256"}
    need(row["row_sha256"] == digest(body), f"{label}:row self hash")


def validate_attachment_ledger(
    payload: dict[str, Any],
    attachment: dict[str, Any],
    path: Path,
    id_field: str,
    label: str,
) -> list[dict[str, Any]]:
    need(file_sha256(path) == attachment["file_sha256"], f"{label}:file attachment")
    rows = payload["rows"]
    need(payload["row_count"] == attachment["row_count"] == len(rows), f"{label}:count")
    need(payload["rows_sha256"] == attachment["rows_sha256"] == digest(rows), f"{label}:rows digest")
    ids = [row[id_field] for row in rows]
    hashes = [row["row_sha256"] for row in rows]
    need(payload["row_ids_sha256"] == attachment["row_ids_sha256"] == digest(ids), f"{label}:ids digest")
    need(payload["row_hashes_sha256"] == attachment["row_hashes_sha256"] == digest(hashes), f"{label}:hashes digest")
    need(len(set(ids)) == len(ids), f"{label}:unique ids")
    for row in rows:
        validate_closed_row(row, label)
    return rows


def source_signature_rows() -> tuple[
    dict[tuple[str, str], list[tuple[int, str, dict[str, Any]]]],
    dict[str, dict[str, Any]],
]:
    grouped: dict[
        tuple[str, str], list[tuple[int, str, dict[str, Any]]]
    ] = collections.defaultdict(list)
    by_id: dict[str, dict[str, Any]] = {}
    count = 0
    for round_number, name, ledger, leaf_field, id_field in SOURCES:
        result = load_pinned_result(name)
        rows = result[ledger]["rows"]
        for row in rows:
            signature = row["local_return_signature"]
            signature_sha256 = row.get(
                "complete_10_field_return_signature_sha256", digest(signature)
            )
            need(signature_sha256 == digest(signature), "source signature digest")
            source_id = row[id_field]
            need(source_id not in by_id, "globally unique source row id")
            by_id[source_id] = row
            grouped[(row[leaf_field], signature_sha256)].append(
                (round_number, source_id, row)
            )
            count += 1
        del result
    need(count == 332_020, "source signature census")
    need(len(grouped) == 332_016, "canonical source grouping census")
    need(
        collections.Counter(len(rows) for rows in grouped.values())
        == {1: 332_012, 2: 4},
        "alias multiplicity census",
    )
    return grouped, by_id


def build_expected_atoms_and_candidates() -> tuple[
    dict[str, dict[str, Any]],
    dict[tuple[str, str], str],
    list[tuple[Any, ...]],
    dict[str, tuple[Q, ...]],
    dict[tuple[str, str], list[tuple[Q, ...]]],
    dict[tuple[str, str], list[tuple[int, str, dict[str, Any]]]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    grouped, source_by_id = source_signature_rows()
    round182 = load_pinned_result(R182)
    leaf_rows = unpack(round182, "collar_leaf_rows")
    occurrence_rows = unpack(round182, "collar_occurrence_rows")
    del round182
    leaf_by_id = {row["row_id"]: row for row in leaf_rows}
    occurrences = {
        row["Round179_occurrence_row_id"]: row for row in occurrence_rows
    }
    whole_boxes = {
        leaf_id: qbox(row["box"]) for leaf_id, row in leaf_by_id.items()
    }
    expected: dict[str, dict[str, Any]] = {}
    atom_by_node: dict[tuple[str, str], str] = {}
    supports: dict[tuple[str, str], list[tuple[Q, ...]]] = {}
    faces: dict[tuple[Any, ...], list[list[tuple[Any, ...]]]] = (
        collections.defaultdict(lambda: [[], []])
    )
    for node, sources in grouped.items():
        leaf_id, signature_sha256 = node
        leaf = leaf_by_id[leaf_id]
        occurrence = occurrences[leaf["occurrence_row_id"]]
        signature = sources[0][2]["local_return_signature"]
        need(
            all(row["local_return_signature"] == signature for _, _, row in sources),
            "group signature identity",
        )
        boxes = []
        for round_number, _source_id, row in sources:
            if (
                round_number == 271
                and row["signed_region_row_id"].startswith(
                    "round271-W-tail-side:"
                )
            ):
                boxes.append(qbox(row["t_child_box"]))
            else:
                boxes.append(whole_boxes[leaf_id])
        normalized = merge_boxes(boxes)
        supports[node] = normalized
        direct_ids = sorted(
            source_id
            for round_number, source_id, _row in sources
            if round_number == 208
        )
        need(len(direct_ids) <= 1, "at most one Round208 backing row")
        strict_support = normalized != [whole_boxes[leaf_id]]
        atom_id = "round279-collar-atom:" + digest(
            [leaf_id, signature_sha256]
        )
        atom_by_node[node] = atom_id
        expected[atom_id] = {
            "canonical_atom_id": atom_id,
            "Round182_leaf_row_id": leaf_id,
            "Round182_occurrence_row_id": leaf["occurrence_row_id"],
            "origin_row_id": occurrence["origin_row_id"],
            "source_chart": occurrence["chart"],
            "owner_target": occurrence["owner_target"],
            "complete_10_field_return_signature": signature,
            "complete_10_field_return_signature_sha256": signature_sha256,
            "source_rounds": sorted(
                {round_number for round_number, _id, _row in sources}
            ),
            "source_signature_row_ids": sorted(
                source_id for _round, source_id, _row in sources
            ),
            "source_alias_multiplicity": len(sources),
            "frozen_true_support_boxes": [
                [str(value) for value in box] for box in normalized
            ],
            "whole_Round182_leaf_box": [
                str(value) for value in whole_boxes[leaf_id]
            ],
            "support_classification": (
                "STRICT_FROZEN_SUBBOX"
                if strict_support
                else "WHOLE_ROUND182_LEAF"
            ),
            "existing_Round208_occurrence_row_ids": direct_ids,
            "new_occurrence_region_atom_candidate": not bool(direct_ids),
            "expanded_occurrence_credit": 0,
            "component_credit": 0,
            "maximality_credit": 0,
        }
        for support_index, box in enumerate(normalized):
            for axis in range(3):
                tangent = tuple(
                    (box[2 * other], box[2 * other + 1])
                    for other in range(3)
                    if other != axis
                )
                for side in (0, 1):
                    key = (
                        occurrence["origin_row_id"],
                        occurrence["chart"],
                        occurrence["owner_target"],
                        signature_sha256,
                        axis,
                        box[2 * axis + side],
                    )
                    faces[key][side].append(
                        (node, tangent, support_index)
                    )

    candidate_set: set[tuple[Any, ...]] = set()
    audit_set: set[tuple[Any, ...]] = set()
    for (
        origin,
        chart,
        target,
        signature_sha256,
        axis,
        coordinate,
    ), (lower, upper) in faces.items():
        # Upper face => negative-side box.  Lower face => positive-side box.
        for negative_node, negative_tangent, _ in upper:
            for positive_node, positive_tangent, _ in lower:
                if negative_node == positive_node:
                    continue
                overlap = tuple(
                    (max(left[0], right[0]), min(left[1], right[1]))
                    for left, right in zip(
                        negative_tangent, positive_tangent, strict=True
                    )
                )
                if not all(lower < upper for lower, upper in overlap):
                    continue
                negative_leaf, _ = negative_node
                positive_leaf, _ = positive_node
                a, b = sorted((negative_leaf, positive_leaf))
                candidate_set.add(
                    (
                        a,
                        b,
                        signature_sha256,
                        chart,
                        target,
                        axis,
                        coordinate,
                        overlap,
                    )
                )
                low, high = sorted((negative_node, positive_node))
                audit_set.add(
                    (
                        low,
                        high,
                        origin,
                        chart,
                        axis,
                        str(coordinate),
                        tuple(
                            (str(lower), str(upper))
                            for lower, upper in overlap
                        ),
                    )
                )
    candidates = sorted(candidate_set, key=str)
    need(len(candidates) == 330_724, "candidate edge census")
    need(
        digest(sorted(audit_set, key=str))
        == "8e6a26f93f954a89b37db293bd46c16ca087762e19758fafb6b0fc95864aebbb",
        "true-support candidate universe digest",
    )
    return (
        expected,
        atom_by_node,
        candidates,
        whole_boxes,
        supports,
        grouped,
        source_by_id,
        leaf_by_id,
    )


def verify_atom_ledger(
    rows: list[dict[str, Any]],
    payload: dict[str, Any],
    expected: dict[str, dict[str, Any]],
) -> None:
    need(
        payload["schema"] == "cm2.round279.canonical-collar-atom-ledger.v1",
        "atom ledger schema",
    )
    need(len(rows) == len(expected) == 332_016, "atom row census")
    need(
        [row["canonical_atom_id"] for row in rows]
        == sorted(expected),
        "atom deterministic order and exact coverage",
    )
    source_ids: list[str] = []
    for row in rows:
        atom_id = row["canonical_atom_id"]
        wanted = expected[atom_id]
        need(
            set(row) == set(wanted) | {"row_sha256"},
            "atom exact field schema",
        )
        for key, value in wanted.items():
            need(row[key] == value, f"atom recomputation:{key}")
        source_ids.extend(row["source_signature_row_ids"])
    need(len(source_ids) == len(set(source_ids)) == 332_020, "source row exact partition")
    need(payload["source_signature_row_count"] == 332_020, "atom source census")
    need(payload["artificial_alias_contraction_count"] == 4, "atom alias census")
    need(
        payload["existing_Round208_occurrence_backed_atom_count"] == 36_040,
        "Round208 atom census",
    )
    need(
        payload["new_occurrence_region_atom_candidate_count"] == 295_976,
        "new candidate atom census",
    )
    need(payload["strict_subbox_atom_count"] == 4, "strict support atom census")
    need(
        payload["strict_nonpromotion"]
        == {
            "expanded_occurrence_credit": 0,
            "component_credit": 0,
            "maximality_credit": 0,
        },
        "atom nonpromotion",
    )


def outgoing_sign(
    chart: str, target: str, values: tuple[Q, ...], label: str
) -> str:
    box = r179v.r174.atlas.AtlasBox(*values, 0, label)
    equality = r179v.independent_geometry(chart, target, box)[
        "outgoing_equality"
    ][0]
    return r179v.arb_sign(equality)


def verify_aliases(
    ledger: dict[str, Any],
    grouped: dict[
        tuple[str, str], list[tuple[int, str, dict[str, Any]]]
    ],
    leaf_by_id: dict[str, dict[str, Any]],
) -> None:
    rows = ledger["rows"]
    need(ledger["row_count"] == len(rows) == 4, "alias row census")
    need(ledger["rows_sha256"] == digest(rows), "alias rows digest")
    need(
        ledger["row_hashes_sha256"]
        == digest([row["row_sha256"] for row in rows]),
        "alias row-hash digest",
    )
    expected_nodes = {
        node for node, sources in grouped.items() if len(sources) == 2
    }
    seen = set()
    for row in rows:
        validate_closed_row(row, "alias")
        leaf_id = row["Round182_parent_leaf_row_id"]
        signature_sha256 = row[
            "complete_10_field_return_signature_sha256"
        ]
        node = (leaf_id, signature_sha256)
        need(node in expected_nodes and node not in seen, "alias exact coverage")
        seen.add(node)
        sources = sorted(
            grouped[node], key=lambda item: item[2]["t_child"]
        )
        need([item[0] for item in sources] == [271, 271], "alias source rounds")
        need(
            [item[2]["t_child"] for item in sources] == [0, 1],
            "alias child labels",
        )
        left = qbox(sources[0][2]["t_child_box"])
        right = qbox(sources[1][2]["t_child_box"])
        parent = qbox(leaf_by_id[leaf_id]["box"])
        split = left[1]
        need(
            left[0] == parent[0]
            and split == right[0]
            and right[1] == parent[1]
            and left[2:] == right[2:] == parent[2:],
            "alias exact child partition",
        )
        face = (split, split, *parent[2:])
        need(
            row["source_signed_region_row_ids"]
            == [sources[0][1], sources[1][1]],
            "alias source row ids",
        )
        need(row["child_boxes"] == [[str(x) for x in left], [str(x) for x in right]], "alias child boxes")
        need(row["parent_box"] == [str(x) for x in parent], "alias parent box")
        need(row["artificial_split_t"] == str(split), "alias split")
        need(
            row["complete_common_p_s_face_box"] == [str(x) for x in face],
            "alias face",
        )
        signature = sources[0][2]["local_return_signature"]
        need(
            sources[1][2]["local_return_signature"] == signature
            and row["complete_10_field_return_signature"] == signature
            and digest(signature) == signature_sha256,
            "alias signature identity",
        )
        chart = row["chart"]
        target = row["owner_target"]
        need(
            outgoing_sign(chart, target, face, f"r279-alias:{leaf_id}:face")
            == "STRICT_NEGATIVE",
            "alias strict-negative common face",
        )
        corridors = row["strict_negative_inward_corridors"]
        need(len(corridors) == 2, "alias corridor count")
        for corridor in corridors:
            values = qbox(corridor["box"])
            need(positive_box(values), "alias positive corridor")
            need(
                outgoing_sign(
                    chart,
                    target,
                    values,
                    f"r279-alias:{leaf_id}:{corridor['side']}",
                )
                == "STRICT_NEGATIVE",
                "alias strict-negative corridor",
            )
        for credit in (
            "expanded_occurrence_credit",
            "component_edge_credit",
            "maximality_credit",
        ):
            need(row[credit] == 0, f"alias zero credit:{credit}")
    need(seen == expected_nodes, "all aliases verified")


def expected_partition_membership() -> dict[int, str]:
    depth4 = load_pinned_gzip(DEPTH4)
    depth8 = load_pinned_gzip(DEPTH8)
    active = load_pinned_gzip(ACTIVE)
    membership: dict[int, str] = {}

    def add(index: int, partition: str) -> None:
        need(0 <= index < 330_724, "partition index range")
        need(index not in membership, "partition pairwise disjointness")
        membership[index] = partition

    need(depth4["row_count"] == len(depth4["rows"]) == 240_932, "depth4 input census")
    need(depth4["rows_sha256"] == digest(depth4["rows"]), "depth4 rows digest")
    for row in depth4["rows"]:
        add(row["candidate_index"], "DEPTH4_ADAPTIVE_STRICT_PATCH")
    need(
        depth8["accepted_patch_and_corridor_count"]
        == len(depth8["rows"])
        == 57_124,
        "depth8 input census",
    )
    for row in depth8["rows"]:
        add(row["candidate_index"], "DEPTH8_SAFE_PRUNED_STRICT_PATCH")
    need(active["row_count"] == len(active["rows"]) == 32_668, "active input census")
    need(active["rows_sha256"] == digest(active["rows"]), "active rows digest")
    for row in active["rows"]:
        classification = row["witness_classification"]
        partition = (
            "P_ENDPOINT_WEDGE_STRICT_PATCH"
            if classification
            == "PASS_P_ENDPOINT_WEDGE_PATCH_AND_TWO_CORRIDORS"
            else "ACTIVE_GRAPH_SIDE_STRICT_PATCH"
        )
        need(
            classification
            in {
                "PASS_P_ENDPOINT_WEDGE_PATCH_AND_TWO_CORRIDORS",
                "PASS_REGULAR_ACTIVE_SIDE_PATCH_AND_TWO_CORRIDORS",
            },
            "active witness classification",
        )
        add(row["candidate_index"], partition)
    need(set(membership) == set(range(330_724)), "partition exact coverage")
    need(
        collections.Counter(membership.values()) == PARTITION_COUNTS,
        "partition exact counts",
    )
    return membership


def signature_payload(signature: dict[str, Any], chart: str) -> dict[str, Any]:
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


TABLES: Any = None
EDGE_ROWS: list[dict[str, Any]] = []
CANDIDATES: list[tuple[Any, ...]] = []
WHOLE_BOXES: dict[str, tuple[Q, ...]] = {}
SUPPORTS: dict[tuple[str, str], list[tuple[Q, ...]]] = {}
ATOM_BY_NODE: dict[tuple[str, str], str] = {}
PARTITIONS: dict[int, str] = {}


def dynamic_signature_hash(
    chart: str, target: str, values: tuple[Q, ...], label: str
) -> str | None:
    box = r174.atlas.AtlasBox(*values, 0, label)
    signature, _rejected = r174.dynamic_signature(chart, box, target, TABLES)
    if signature is None:
        return None
    return digest(signature_payload(signature, chart))


def contained_in(values: tuple[Q, ...], bounds: tuple[Q, ...]) -> bool:
    return all(
        bounds[2 * axis]
        <= values[2 * axis]
        <= values[2 * axis + 1]
        <= bounds[2 * axis + 1]
        for axis in range(3)
    )


def endpoint_orientation(
    leaf_id: str,
    signature_sha256: str,
    axis: int,
    coordinate: Q,
    overlap: tuple[tuple[Q, Q], tuple[Q, Q]],
) -> str:
    orientations = set()
    for support in SUPPORTS[(leaf_id, signature_sha256)]:
        tangential = tuple(
            (support[2 * other], support[2 * other + 1])
            for other in range(3)
            if other != axis
        )
        actual_overlap = tuple(
            (max(a[0], b[0]), min(a[1], b[1]))
            for a, b in zip(tangential, overlap, strict=True)
        )
        if not all(a < b for a, b in actual_overlap):
            continue
        if support[2 * axis + 1] == coordinate:
            orientations.add("NEGATIVE")
        if support[2 * axis] == coordinate:
            orientations.add("POSITIVE")
    need(len(orientations) == 1, "unique endpoint orientation")
    return next(iter(orientations))


EDGE_ROW_FIELDS = {
    "formal_face_edge_witness_row_id",
    "candidate_index",
    "witness_partition",
    "endpoint_atoms",
    "complete_10_field_return_signature_sha256",
    "source_chart",
    "owner_target",
    "common_face_axis",
    "common_face_coordinate",
    "candidate_overlap_rectangle",
    "exact_positive_area_face_patch",
    "two_inward_corridors",
    "expanded_occurrence_credit",
    "component_edge_credit",
    "maximality_credit",
    "row_sha256",
}


def verify_edge_row(
    row: dict[str, Any], row_index: int, dynamic: bool
) -> None:
    validate_closed_row(row, "edge")
    need(set(row) == EDGE_ROW_FIELDS, "edge exact field schema")
    index = row["candidate_index"]
    need(index == row_index, "edge candidate deterministic order")
    (
        a,
        b,
        signature_sha256,
        chart,
        target,
        axis,
        coordinate,
        overlap,
    ) = CANDIDATES[index]
    need(
        row["formal_face_edge_witness_row_id"]
        == "round279-face-edge:" + digest([index, signature_sha256]),
        "edge id",
    )
    need(row["witness_partition"] == PARTITIONS[index], "edge partition membership")
    need(
        row["complete_10_field_return_signature_sha256"]
        == signature_sha256,
        "edge signature hash",
    )
    need(row["source_chart"] == chart, "edge source chart")
    need(row["owner_target"] == target, "edge owner target")
    need(row["common_face_axis"] == axis, "edge axis")
    need(row["common_face_coordinate"] == str(coordinate), "edge coordinate")
    need(
        row["candidate_overlap_rectangle"]
        == [[str(lower), str(upper)] for lower, upper in overlap],
        "edge overlap",
    )
    expected_endpoints = []
    for leaf_id in (a, b):
        side = endpoint_orientation(
            leaf_id, signature_sha256, axis, coordinate, overlap
        )
        expected_endpoints.append(
            {
                "leaf_row_id": leaf_id,
                "canonical_atom_id": ATOM_BY_NODE[
                    (leaf_id, signature_sha256)
                ],
                "geometric_side": side,
            }
        )
    expected_endpoints.sort(key=lambda item: item["geometric_side"])
    need(row["endpoint_atoms"] == expected_endpoints, "edge endpoints")
    need(
        all(
            set(endpoint)
            == {"leaf_row_id", "canonical_atom_id", "geometric_side"}
            for endpoint in row["endpoint_atoms"]
        ),
        "endpoint exact field schema",
    )

    patch = qbox(row["exact_positive_area_face_patch"])
    need(
        patch[2 * axis] == patch[2 * axis + 1] == coordinate,
        "face coordinate",
    )
    tangent_index = 0
    for other in range(3):
        if other == axis:
            continue
        lower, upper = overlap[tangent_index]
        need(
            lower
            <= patch[2 * other]
            < patch[2 * other + 1]
            <= upper,
            "positive contained tangential patch",
        )
        tangent_index += 1
    if dynamic:
        need(
            dynamic_signature_hash(
                chart, target, patch, f"r279-independent-face:{index}"
            )
            == signature_sha256,
            "dynamic face signature",
        )

    corridors = row["two_inward_corridors"]
    need(len(corridors) == 2, "two corridor rows")
    need(
        {item["leaf_row_id"] for item in corridors} == {a, b},
        "corridor endpoint set",
    )
    seen_sides = collections.Counter()
    for corridor in corridors:
        need(
            set(corridor)
            == {
                "leaf_row_id",
                "geometric_side",
                "dyadic_normal_depth",
                "exact_corridor_box",
            },
            "corridor exact field schema",
        )
        leaf_id = corridor["leaf_row_id"]
        values = qbox(corridor["exact_corridor_box"])
        need(positive_box(values), "positive corridor volume")
        need(
            any(
                contained_in(values, support)
                for support in SUPPORTS[(leaf_id, signature_sha256)]
            ),
            "corridor contained in frozen true support",
        )
        for other in range(3):
            if other != axis:
                need(
                    values[2 * other : 2 * other + 2]
                    == patch[2 * other : 2 * other + 2],
                    "corridor tangential patch identity",
                )
        side = endpoint_orientation(
            leaf_id, signature_sha256, axis, coordinate, overlap
        )
        expected_side = side + "_SIDE_INWARD"
        need(
            corridor["geometric_side"] == expected_side,
            "corridor side label",
        )
        if side == "NEGATIVE":
            need(
                values[2 * axis]
                < values[2 * axis + 1]
                == coordinate,
                "negative-side inward corridor",
            )
        else:
            need(
                coordinate
                == values[2 * axis]
                < values[2 * axis + 1],
                "positive-side inward corridor",
            )
        depth = corridor["dyadic_normal_depth"]
        need(isinstance(depth, int) and depth >= 1, "corridor depth")
        whole = WHOLE_BOXES[leaf_id]
        need(
            values[2 * axis + 1] - values[2 * axis]
            == (whole[2 * axis + 1] - whole[2 * axis]) / (2**depth),
            "dyadic normal width",
        )
        if dynamic:
            need(
                dynamic_signature_hash(
                    chart,
                    target,
                    values,
                    f"r279-independent-corridor:{index}:{side}",
                )
                == signature_sha256,
                "dynamic corridor signature",
            )
        seen_sides[side] += 1
    need(seen_sides == {"NEGATIVE": 1, "POSITIVE": 1}, "two-sided corridors")
    for credit in (
        "expanded_occurrence_credit",
        "component_edge_credit",
        "maximality_credit",
    ):
        need(row[credit] == 0, f"edge zero credit:{credit}")


def verify_edge_worker(row_index: int) -> str:
    try:
        verify_edge_row(EDGE_ROWS[row_index], row_index, dynamic=True)
        return "PASS"
    except Exception as error:
        return "FAIL:" + str(error)


def verify_edge_ledger_structure(
    rows: list[dict[str, Any]],
    payload: dict[str, Any],
    membership: dict[int, str],
) -> None:
    need(
        payload["schema"]
        == "cm2.round279.formal-common-face-edge-witness-ledger.v1",
        "edge ledger schema",
    )
    need(len(rows) == 330_724, "edge row census")
    indices = [row["candidate_index"] for row in rows]
    need(indices == list(range(330_724)), "edge exact ordered index coverage")
    histogram = collections.Counter(row["witness_partition"] for row in rows)
    need(histogram == PARTITION_COUNTS, "edge partition histogram")
    need(
        payload["witness_partition_histogram"]
        == dict(sorted(PARTITION_COUNTS.items())),
        "edge payload partition histogram",
    )
    expected_partition_sha = {
        partition: digest(
            sorted(
                index
                for index, actual_partition in membership.items()
                if actual_partition == partition
            )
        )
        for partition in sorted(PARTITION_COUNTS)
    }
    need(
        payload["candidate_index_partition_sha256"]
        == expected_partition_sha,
        "edge exact partition membership digests",
    )
    need(
        payload["candidate_indices_sha256"] == digest(indices),
        "edge candidate index digest",
    )
    need(
        payload["strict_nonpromotion"]
        == {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
        },
        "edge nonpromotion",
    )


def verify_result_structure(
    result: dict[str, Any],
    atom_payload: dict[str, Any],
    edge_payload: dict[str, Any],
) -> None:
    need(result["schema"] == SCHEMA, "certificate schema")
    need(
        result["status"] == "PASS_PRODUCER_ROUND279__FORMAL_ZERO_CREDIT_FREEZE",
        "producer status",
    )
    need(
        result["census"]
        == {
            "source_signature_row_count": 332_020,
            "canonical_atom_count": 332_016,
            "artificial_alias_contraction_count": 4,
            "alias_witness_row_count": 4,
            "existing_Round208_occurrence_backed_atom_count": 36_040,
            "new_occurrence_region_atom_candidate_count": 295_976,
            "formal_common_face_edge_witness_count": 330_724,
            "formal_inward_corridor_witness_count": 661_448,
            "remaining_common_face_candidate_edge_count": 0,
        },
        "certificate census",
    )
    need(
        result["formal_common_face_edge_witness_ledger_attachment"][
            "witness_partition_histogram"
        ]
        == dict(sorted(PARTITION_COUNTS.items())),
        "certificate partition histogram",
    )
    need(
        result["exact_partition_contract"]
        == {
            "canonical_atoms_are_exact_quotient_of_332020_source_rows_by_four_proven_aliases": True,
            "candidate_edge_indices_are_exactly_0_through_330723": True,
            "edge_partitions_are_pairwise_disjoint": True,
            "edge_partitions_cover_the_complete_true_support_candidate_universe": True,
            "each_edge_has_one_positive_area_face_patch": True,
            "each_edge_has_exactly_two_geometrically_oriented_inward_corridors": True,
            "Jx_Jy_same_point_edges_included": False,
            "Round268_true_seam_edges_included": False,
        },
        "partition contract",
    )
    need(
        result["strict_nonpromotion"]
        == {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "DSU_rank_reduction_credit": 0,
            "maximality_credit": 0,
            "exact_key_fibre_credit": 0,
            "global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "certificate strict nonpromotion",
    )
    expected_producer_inputs = {
        name: pins[0] for name, pins in RESULT_INPUT_PINS.items()
    }
    expected_producer_inputs.update(
        {
            name: NONRESULT_INPUT_PINS[name]
            for name in (DEPTH4, DEPTH8, ACTIVE, R278_SOURCE, R174_SOURCE)
        }
    )
    need(
        result["provenance"]["input_file_sha256"]
        == dict(sorted(expected_producer_inputs.items())),
        "certificate input pins",
    )
    need(result["provenance"]["seed_is_order_irrelevant"], "seed order irrelevance")
    producer_path = secure_local_regular(
        HERE / PRODUCER_SOURCE, "Round279 producer source"
    )
    need(
        result["provenance"]["producer_file_sha256"]
        == file_sha256(producer_path),
        "certificate producer source pin",
    )
    verify_cacheless_source(producer_path, "Round279 producer")
    verify_cacheless_source(
        secure_local_regular(
            HERE / DEPTH4_MATERIALIZER_SOURCE,
            "Round279 depth4 materializer source",
        ),
        "Round279 depth4 materializer",
    )
    atom_attachment = result["canonical_atom_ledger_attachment"]
    edge_attachment = result[
        "formal_common_face_edge_witness_ledger_attachment"
    ]
    for field in ("row_count", "rows_sha256", "row_ids_sha256", "row_hashes_sha256"):
        need(atom_attachment[field] == atom_payload[field], f"atom attachment:{field}")
    for field in (
        "row_count",
        "witness_partition_histogram",
        "candidate_index_partition_sha256",
        "candidate_indices_sha256",
        "rows_sha256",
        "row_ids_sha256",
        "row_hashes_sha256",
    ):
        need(edge_attachment[field] == edge_payload[field], f"edge attachment:{field}")


def attack_tests(
    result: dict[str, Any],
    atom_rows: list[dict[str, Any]],
    edge_rows: list[dict[str, Any]],
) -> dict[str, str]:
    outcomes: dict[str, str] = {}

    def expect_reject(name: str, function) -> None:
        try:
            function()
        except Exception:
            outcomes[name] = "REJECTED"
        else:
            outcomes[name] = "ACCEPTED_IN_ERROR"

    forged_atom = dict(atom_rows[0])
    forged_atom["source_alias_multiplicity"] = 2
    expect_reject(
        "ATOM_ROW_FORGERY",
        lambda: validate_closed_row(forged_atom, "attack atom"),
    )

    forged_edge = dict(edge_rows[0])
    forged_edge["candidate_index"] = 1
    expect_reject(
        "EDGE_ROW_FORGERY",
        lambda: validate_closed_row(forged_edge, "attack edge"),
    )

    forged_alias = dict(
        result["artificial_alias_witness_ledger"]["rows"][0]
    )
    forged_alias["component_edge_credit"] = 1
    expect_reject(
        "ALIAS_ROW_FORGERY",
        lambda: validate_closed_row(forged_alias, "attack alias"),
    )

    forged = dict(edge_rows[0])
    forged["component_edge_credit"] = 1
    forged["row_sha256"] = digest(
        {key: value for key, value in forged.items() if key != "row_sha256"}
    )
    expect_reject(
        "FORGED_NONZERO_CREDIT",
        lambda: verify_edge_row(forged, 0, dynamic=False),
    )

    reordered_indices = [row["candidate_index"] for row in edge_rows]
    reordered_indices[0], reordered_indices[1] = (
        reordered_indices[1],
        reordered_indices[0],
    )
    expect_reject(
        "EDGE_ROW_REORDER",
        lambda: need(
            reordered_indices == list(range(330_724)), "attack row reorder"
        ),
    )

    dropped_indices = [row["candidate_index"] for row in edge_rows[:-1]]
    expect_reject(
        "EDGE_ROW_DROP",
        lambda: need(
            dropped_indices == list(range(330_724)), "attack row drop"
        ),
    )

    forged = json.loads(json.dumps(edge_rows[0]))
    forged["endpoint_atoms"][0]["canonical_atom_id"] = "round279-orphan"
    forged["row_sha256"] = digest(
        {key: value for key, value in forged.items() if key != "row_sha256"}
    )
    expect_reject(
        "ORPHAN_ENDPOINT_ATOM",
        lambda: verify_edge_row(forged, 0, dynamic=False),
    )

    forged = json.loads(json.dumps(edge_rows[0]))
    forged["two_inward_corridors"][0]["geometric_side"] = (
        forged["two_inward_corridors"][1]["geometric_side"]
    )
    forged["row_sha256"] = digest(
        {key: value for key, value in forged.items() if key != "row_sha256"}
    )
    expect_reject(
        "CORRIDOR_SIDE_SWAP",
        lambda: verify_edge_row(forged, 0, dynamic=False),
    )

    forged = json.loads(json.dumps(edge_rows[0]))
    axis = forged["common_face_axis"]
    tangent = next(other for other in range(3) if other != axis)
    forged["exact_positive_area_face_patch"][2 * tangent + 1] = (
        forged["exact_positive_area_face_patch"][2 * tangent]
    )
    forged["row_sha256"] = digest(
        {key: value for key, value in forged.items() if key != "row_sha256"}
    )
    expect_reject(
        "ZERO_AREA_FACE_PATCH",
        lambda: verify_edge_row(forged, 0, dynamic=False),
    )

    expect_reject(
        "DUPLICATE_JSON_KEY",
        lambda: strict_json_bytes(
            b'{"x":1,"x":2}', "attack duplicate JSON", 64
        ),
    )
    expect_reject(
        "NONFINITE_JSON_CONSTANT",
        lambda: strict_json_bytes(b'{"x":NaN}', "attack NaN JSON", 64),
    )
    expect_reject(
        "TRAILING_JSON_DOCUMENT",
        lambda: strict_json_bytes(b'{}{}', "attack trailing JSON", 64),
    )
    tiny_gzip = gzip.compress(b"{}", mtime=0)
    expect_reject(
        "TRAILING_GZIP_BYTES",
        lambda: strict_gzip_json_bytes(
            tiny_gzip + b"X", "attack trailing GZIP", 128, 128
        ),
    )
    expect_reject(
        "GZIP_COMPRESSED_OVERSIZE",
        lambda: strict_gzip_json_bytes(
            tiny_gzip, "attack compressed oversize", 1, 128
        ),
    )
    large_gzip = gzip.compress(b'{"x":"' + b"a" * 256 + b'"}', mtime=0)
    expect_reject(
        "GZIP_UNCOMPRESSED_OVERSIZE",
        lambda: strict_gzip_json_bytes(
            large_gzip, "attack uncompressed oversize", 1024, 32
        ),
    )

    expect_reject(
        "POISONED_RUNTIME_CACHE_SOURCE",
        lambda: verify_cacheless_source_text_for_attack(
            "import pickle\npickle.loads(open('/tmp/"
            "cm2_round277_candidate_runtime_cache.pkl','rb').read())"
        ),
    )

    # Files are placed directly in HERE so each policy branch is exercised
    # rather than being rejected merely because it lives in a nested temp dir.
    descriptor, base_name = tempfile.mkstemp(
        prefix=".round279-path-attack.", dir=HERE
    )
    os.close(descriptor)
    base = Path(base_name)
    symlink = HERE / (base.name + ".symlink")
    hardlink = HERE / (base.name + ".hardlink")
    outside_descriptor, outside_name = tempfile.mkstemp(
        prefix=".round279-path-escape."
    )
    os.close(outside_descriptor)
    outside = Path(outside_name)
    try:
        symlink.symlink_to(base)
        expect_reject(
            "SYMLINK_INPUT_PATH",
            lambda: secure_local_regular(symlink, "attack symlink"),
        )
        os.link(base, hardlink)
        expect_reject(
            "HARDLINK_INPUT_PATH",
            lambda: secure_local_regular(base, "attack hardlink"),
        )
        expect_reject(
            "PATH_ESCAPE_INPUT",
            lambda: secure_local_regular(outside, "attack path escape"),
        )
    finally:
        for path in (symlink, hardlink, base, outside):
            try:
                path.unlink()
            except FileNotFoundError:
                pass
    return outcomes


def main() -> int:
    global TABLES, EDGE_ROWS, CANDIDATES, WHOLE_BOXES, SUPPORTS
    global ATOM_BY_NODE, PARTITIONS

    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=CERTIFICATE)
    parser.add_argument("--atom-ledger", type=Path, default=ATOM_LEDGER)
    parser.add_argument("--edge-ledger", type=Path, default=EDGE_LEDGER)
    parser.add_argument("--output", type=Path, default=VERIFICATION)
    parser.add_argument("--processes", type=int, default=min(40, mp.cpu_count()))
    parser.add_argument(
        "--structural-only",
        action="store_true",
        help="debug-only: skip the 992,172 dynamic face/corridor evaluations",
    )
    args = parser.parse_args()

    for name, expected in NONRESULT_INPUT_PINS.items():
        path = secure_local_regular(HERE / name, f"nonresult input:{name}")
        need(file_sha256(path) == expected, f"nonresult input pin:{name}")
    ctx.prec = 256
    need(ctx.prec == 256, "fixed FLINT precision")

    certificate_path = secure_local_regular(
        args.certificate, "candidate certificate"
    )
    atom_path = secure_local_regular(args.atom_ledger, "candidate atom ledger")
    edge_path = secure_local_regular(args.edge_ledger, "candidate edge ledger")
    document = strict_json_bytes(
        certificate_path.read_bytes(),
        "candidate certificate",
        maximum=4 * 1024 * 1024,
    )
    result = document["result"]
    need(document["result_sha256"] == digest(result), "certificate result digest")
    atom_payload = strict_gzip_json_bytes(
        atom_path.read_bytes(),
        "candidate atom ledger",
        maximum_compressed=256 * 1024 * 1024,
        maximum_uncompressed=768 * 1024 * 1024,
    )
    edge_payload = strict_gzip_json_bytes(
        edge_path.read_bytes(),
        "candidate edge ledger",
        maximum_compressed=256 * 1024 * 1024,
        maximum_uncompressed=768 * 1024 * 1024,
    )
    atom_rows = validate_attachment_ledger(
        atom_payload,
        result["canonical_atom_ledger_attachment"],
        atom_path,
        "canonical_atom_id",
        "atom",
    )
    edge_rows = validate_attachment_ledger(
        edge_payload,
        result["formal_common_face_edge_witness_ledger_attachment"],
        edge_path,
        "formal_face_edge_witness_row_id",
        "edge",
    )
    verify_result_structure(result, atom_payload, edge_payload)

    (
        expected_atoms,
        ATOM_BY_NODE,
        CANDIDATES,
        WHOLE_BOXES,
        SUPPORTS,
        grouped,
        _source_by_id,
        leaf_by_id,
    ) = build_expected_atoms_and_candidates()
    verify_atom_ledger(atom_rows, atom_payload, expected_atoms)
    verify_aliases(
        result["artificial_alias_witness_ledger"], grouped, leaf_by_id
    )
    PARTITIONS = expected_partition_membership()
    verify_edge_ledger_structure(edge_rows, edge_payload, PARTITIONS)

    dynamic_histogram = {"SKIPPED_STRUCTURAL_ONLY": len(edge_rows)}
    if not args.structural_only:
        TABLES = r174.registry_tables(r174.load_inputs()["gate5"])
        EDGE_ROWS = edge_rows
        counts: collections.Counter[str] = collections.Counter()
        with mp.get_context("fork").Pool(args.processes) as pool:
            for status in pool.imap_unordered(
                verify_edge_worker, range(len(EDGE_ROWS)), chunksize=16
            ):
                counts[status] += 1
                done = sum(counts.values())
                if done % 20_000 == 0:
                    print(
                        json.dumps(
                            {
                                "verification_progress": done,
                                "total": len(EDGE_ROWS),
                                "histogram": dict(sorted(counts.items())),
                            },
                            sort_keys=True,
                        ),
                        flush=True,
                    )
        need(counts == {"PASS": 330_724}, "dynamic edge verification")
        dynamic_histogram = dict(sorted(counts.items()))

    attack_outcomes = attack_tests(result, atom_rows, edge_rows)
    rejected = sum(value == "REJECTED" for value in attack_outcomes.values())
    total = len(attack_outcomes)
    need(rejected == total, "all attack tests rejected")
    verification = {
        "status": (
            "PASS_INDEPENDENT_ROUND279_STRUCTURAL_ONLY"
            if args.structural_only
            else "PASS_INDEPENDENT_ROUND279"
        ),
        "certificate_result_sha256": document["result_sha256"],
        "canonical_atom_count": 332_016,
        "artificial_alias_witness_count": 4,
        "formal_common_face_edge_witness_count": 330_724,
        "formal_inward_corridor_witness_count": 661_448,
        "witness_partition_histogram": dict(sorted(PARTITION_COUNTS.items())),
        "dynamic_verification_histogram": dynamic_histogram,
        "remaining_common_face_candidate_edge_count": 0,
        "attack_tests_rejected": rejected,
        "attack_tests_total": total,
        "attack_test_outcomes": dict(sorted(attack_outcomes.items())),
        "input_path_policy": {
            "must_resolve_inside_deliverables_directory": True,
            "regular_file_required": True,
            "symlink_rejected": True,
            "hardlink_rejected": True,
        },
        "strict_serialization_policy": {
            "duplicate_JSON_keys_rejected": True,
            "NaN_and_Infinity_rejected": True,
            "trailing_JSON_documents_rejected": True,
            "trailing_or_concatenated_GZIP_members_rejected": True,
            "compressed_and_uncompressed_size_limits_enforced": True,
        },
        "runtime_cache_policy": {
            "producer_pickle_import_rejected": True,
            "candidate_runtime_cache_path_rejected": True,
            "verifier_rebuilds_from_pinned_frozen_inputs": True,
        },
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "DSU_rank_reduction_credit": 0,
            "maximality_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    output = args.output
    if args.structural_only and output == VERIFICATION:
        output = HERE / f"{PREFIX}_structural_only_verification.json"
    atomic_write_json(output, verification)
    print(json.dumps(verification, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
