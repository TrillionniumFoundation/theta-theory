#!/usr/bin/env python3
"""Standalone cacheless verifier for the Round290 inner-support closure.

The Round290 producer is pinned and hashed only as inert bytes.  It is never
imported or executed.  Starting from the byte-pinned Round174/Round179/
Round182/Round204/Round208/Round269/Round270/Round271/Round272/Round279 and
Round288 inputs, this verifier independently:

* finds the 21,160 isolated Round288 atoms and rebinds their unique source row,
  Round182 leaf, collar, complete ten-field signature, chart and target;
* repeats the finite ordered rational search (Rounds269/270) or the nested
  dyadic witness expansion (Rounds271/272);
* dynamically evaluates the complete signature and independently evaluates
  the active signed factor/graph side on every whole candidate box;
* rebuilds every exact Round290 ledger row without consulting the candidate
  ledger;
* reconstructs the complete 126,468-row existing occurrence frontier and
  reruns both the existing-overlap and same-chart/same-signature pair audits;
* checks exact JSON-object commitments and deterministic gzip bytes; and
* rejects targeted attacks even when the attacker recomputes row, ledger and
  result hashes.

All rows remain ZERO-CREDIT.  Verification of inner supports is not an
occurrence promotion, component union, maximality proof, fibre proof, global
disposition, true seam, or Jx/Jy same-point glue.
"""

from __future__ import annotations

import argparse
import collections
from copy import deepcopy
from fractions import Fraction as Q
import gc
import gzip
import hashlib
import importlib
import importlib.abc
import importlib.util
import io
from itertools import product
import json
import multiprocessing as mp
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Callable

from flint import ctx, __version__ as FLINT_VERSION


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round290_source_g_isolated_atom_inner_support_closure"
PRODUCER = HERE / f"{PREFIX}.py"
RESULT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_inner_support_ledger.json.gz"
OUTPUT = HERE / f"{PREFIX}_verification.json"

SCHEMA = "cm2.round290.source-g-isolated-atom-inner-support-closure.v1"
LEDGER_SCHEMA = "cm2.round290.isolated-atom-inner-support-ledger.v1"
VERIFICATION_SCHEMA = SCHEMA + ".verification.v1"

R174_ROWS = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
)
R179_ROWS = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R182_ROWS = "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
R204_CERT = (
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
)
R208_CERT = (
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
)
R269_CERT = (
    "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json"
)
R270_CERT = (
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json"
)
R271_CERT = (
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json"
)
R272_CERT = (
    "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json"
)
R279_ATOMS = "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz"
R288_RESULT = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_result.json"
)
R288_DISPOSITIONS = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_"
    "atom_dispositions.json.gz"
)

UPSTREAM_PINS = {
    R174_ROWS:
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    R179_ROWS:
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R182_ROWS:
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    R204_CERT:
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    R208_CERT:
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    R269_CERT:
        "472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3",
    R270_CERT:
        "72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea",
    R271_CERT:
        "c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747",
    R272_CERT:
        "16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2",
    R279_ATOMS:
        "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
    R288_RESULT:
        "9b5875777f3937efe05a4d871a8c8b76c92ca69d0f636eb014542f59dfe49569",
    R288_DISPOSITIONS:
        "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a",
}

UPSTREAM_SOURCE_PINS = {
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py":
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    "cm2_round179_source_g_residual_tube_arrangement_verifier.py":
        "292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679",
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization.py":
        "0ed0df9e4873e93b03ba11e8ad8ce6274d3b9de01875363c1a1818fdbc8867df",
}

# Complete static transitive import closure of the three direct evaluator
# modules.  Every byte string is hashed before any of these module names may
# execute.  A source-only loader below compiles these pinned bytes directly,
# bypassing __pycache__ and rejecting every preloaded module in this closure.
EVALUATOR_MODULE_PINS = {
    "cm2_gate3_candidate_first_hit_cert":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_gate3_eight_cell_symmetry_atlas_cert":
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "cm2_gate3_ge_interval_atlas_cert":
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization":
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier":
        "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
    "cm2_round179_source_g_residual_tube_arrangement_verifier":
        "292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement":
        "8638f2722e68bd5c6e0eb5932dc76780728998f21a47b1d8c02c28449e984d56",
    "cm2_round186_source_g_factor_face_probe":
        "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64",
    "cm2_round188_source_g_factor_face_boundary_arrangement_probe":
        "11e033c726a51bab875f42c371682814a84f46871f1a45797d5c68aa3b3149de",
    "cm2_round189_source_g_endpoint_p_refinement_probe":
        "118f0ec0333562026294ba4667cf7498403c4b6274378921afaa3819ef9323e4",
    "cm2_round191_source_g_stereographic_endpoint_chart_probe":
        "b37c0a06a392107d7d859c65ab323cf04c7f06cdd4f51cba59c2049c53f70b9f",
    "cm2_round195_source_g_outgoing_assembly_and_u2_order_probe":
        "f70734937ed2630f4357b9e1d860e862c1a932c573c1f93c45788cd5697ee4e1",
    "cm2_round198_source_g_outgoing_return_signature_probe":
        "59dac5b6e2d79e1612dad51780174f97f71dc1223c01a21b502805d6e9510fbf",
    "cm2_round203_source_g_outgoing_signature_component_probe":
        "86214ed1d37400cdde787c915b4467c7d081e018a7c7522470bdcb5d1abc351f",
    "cm2_round207_source_g_whole_region_direct_signature_probe":
        "0262235b43d74084c37b742b8b4fc435b82e752663d5f816e092faf14e64404a",
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization":
        "0ed0df9e4873e93b03ba11e8ad8ce6274d3b9de01875363c1a1818fdbc8867df",
}

EVALUATOR_SOURCE_PINS = {
    module_name + ".py": expected_hash
    for module_name, expected_hash in EVALUATOR_MODULE_PINS.items()
}

CANDIDATE_PINS = {
    PRODUCER.name:
        "b528acc2d71fd71a141d4067e6dd1f172d49a23a6c44ef19dc991a57da753418",
    RESULT.name:
        "1c2412da9fd28f6838eab1abb3b3e70773a4ca4f0ea28fafcda8c8342e881d59",
    LEDGER.name:
        "9c2a596f3b981d24baa039e02c72e5270889d145dc146963532f3dedebc94025",
}

ARTIFACT_PINS = {
    **UPSTREAM_PINS,
    **EVALUATOR_SOURCE_PINS,
    **CANDIDATE_PINS,
}

PRE_CANDIDATE_PINS = {
    **UPSTREAM_PINS,
    **EVALUATOR_SOURCE_PINS,
    PRODUCER.name: CANDIDATE_PINS[PRODUCER.name],
}

SOURCE_SPECS = {
    269: (R269_CERT, "formal_direct_side_signature_ledger"),
    270: (R270_CERT, "formal_direct_side_signature_ledger"),
    271: (R271_CERT, "formal_side_signature_ledger"),
    272: (R272_CERT, "formal_side_signature_ledger"),
}

SIGNATURE_FIELDS = {
    "official_key_id",
    "official_key_ordinal",
    "official_key_row",
    "ordered_integer_wall_events",
    "outgoing_cell",
    "roof",
    "signed_wall_word",
    "source_chart",
    "target_chart",
    "target_lift",
}
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
UNRESOLVED_STATE = (
    "NEW_DISJOINT_CANDIDATE__"
    "POSITIVE_VOLUME_RATIONAL_INNER_SUPPORT_NOT_MATERIALIZED"
)

# This order, including its non-monotone extremes, is part of the frozen
# deterministic search contract.
SEARCH_FRACTIONS = (
    Q(1, 1_048_576),
    Q(1_048_575, 1_048_576),
    Q(1, 4_096),
    Q(4_095, 4_096),
    Q(1, 64),
    Q(63, 64),
    Q(1, 2),
    Q(1, 8),
    Q(7, 8),
    Q(1, 4),
    Q(3, 4),
)
SEARCH_CATALOGUE_SIZE = len(SEARCH_FRACTIONS) ** 3

EXPECTED_STATUS = (
    "PASS_ROUND290_ALL_21160_ISOLATED_ATOMS_HAVE_STRICT_"
    "POSITIVE_VOLUME_RATIONAL_INNER_SUPPORTS__"
    "FULL_DYNAMIC_SIGNATURE_AND_ACTIVE_SIDE_RECHECK__"
    "EXISTING_AND_PAIRWISE_OVERLAP_RESIDUAL_ZERO__ZERO_CREDIT"
)

EXPECTED_SUPPORT_CONTRACT = {
    "every_inner_box_has_strictly_positive_exact_rational_volume": True,
    "every_inner_box_is_strictly_inside_its_atom_envelope": True,
    "every_inner_box_is_strictly_inside_the_chart_guard": True,
    "no_inner_box_touches_a_half_open_or_excluded_face": True,
    "complete_ten_field_signature_recomputed_on_every_whole_box": True,
    "official_exact_key_recomputed_on_every_whole_box": True,
    "owner_target_and_source_chart_recomputed_and_equal": True,
    "source_signed_region_active_factor_or_graph_side_rechecked_separately":
        True,
    "return_signature_coincidence_alone_never_proves_signed_region_side": True,
    "whole_leaf_envelope_never_used_as_inner_support": True,
    "point_witness_never_used_as_inner_support": True,
    "Round269_Round270_search_is_finite_ordered_and_seed_inert": True,
    "Round271_Round272_nested_dyadic_expansion_records_largest_successful_box_depth":
        True,
    "existing_frontier_overlap_reaudited": True,
    "same_chart_same_signature_pairwise_duplicate_reaudited": True,
    "any_search_failure_is_preserved_verbatim_and_receives_zero_credit": True,
}

EXPECTED_NONPROMOTION = {
    "formal_new_expanded_occurrence_credit": 0,
    "formal_occurrence_alias_credit": 0,
    "formal_component_union_credit": 0,
    "formal_DSU_rank_reduction_credit": 0,
    "maximality_credit": 0,
    "fibre_credit": 0,
    "global_disposition_credit": 0,
    "true_seam_credit": 0,
    "Jx_Jy_same_point_glue_credit": 0,
    "expanded_occurrences": 126_468,
    "quotient_components": 63_224,
    "maximality": "0/63224",
    "exact_key_fibres": "0/116",
    "global_dispositions": "0/224580",
    "Gate5": "10/18",
    "D02": "BLOCKED",
    "CM2": "NO-GO_FOR_CLAIM",
}

EXPECTED_REQUIRED_NEXT = [
    "Run a standalone cacheless Round290 verifier without importing or executing this producer.",
    "Keep the 21,160 rows zero-credit until that verifier independently rebuilds every inner box, dynamic signature, signed-region side and overlap audit.",
    "Combine a verified Round288 corridor partition and verified Round290 isolated partition only in a later explicit occurrence-promotion round.",
    "The 152 true seams, final DSU, maximality, 116 fibres and 224,580 dispositions remain downstream gates.",
]

ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


class VerificationError(RuntimeError):
    """A frozen input, independent reconstruction, or candidate check failed."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def secure_regular_file(path: Path, maximum: int = 1_200_000_000) -> bytes:
    info = path.lstat()
    need(
        path.parent == HERE
        and stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        f"secure regular file:{path.name}",
    )
    return path.read_bytes()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(secure_regular_file(path))
    need(isinstance(value, dict), f"top-level object:{path.name}")
    return value


def read_gzip_json(path: Path) -> dict[str, Any]:
    raw = secure_regular_file(path)
    with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as handle:
        decoded = handle.read(1_200_000_001)
    need(len(decoded) <= 1_200_000_000, f"gzip expansion bound:{path.name}")
    value = json.loads(decoded)
    need(isinstance(value, dict), f"gzip top-level object:{path.name}")
    return value


def closed_result(filename: str) -> dict[str, Any]:
    document = read_json(HERE / filename)
    need(
        set(document) >= {"result", "result_sha256"}
        and document["result_sha256"] == digest(document["result"]),
        f"closed upstream result:{filename}",
    )
    need(isinstance(document["result"], dict), f"result object:{filename}")
    return document["result"]


def verify_direct_result(document: dict[str, Any], label: str) -> None:
    stored = document.get("result_sha256")
    payload = {
        key: value for key, value in document.items()
        if key != "result_sha256"
    }
    need(stored == digest(payload), f"direct result closure:{label}")


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    rows = result[table]
    columns = result["row_column_schemas"][table]
    census = result["table_census_and_sha256"][table]
    need(
        isinstance(rows, list)
        and len(rows) == census["row_count"]
        and digest(rows) == census["rows_sha256"],
        f"packed upstream table:{table}",
    )
    return [dict(zip(columns, row, strict=True)) for row in rows]


def validate_closed_rows(
    document: dict[str, Any],
    id_field: str,
    expected_count: int,
    label: str,
    *,
    verify_each_row: bool = True,
) -> list[dict[str, Any]]:
    rows = document["rows"]
    need(
        isinstance(rows, list)
        and document["row_count"] == len(rows) == expected_count,
        f"{label}:row count",
    )
    need(document["rows_sha256"] == digest(rows), f"{label}:rows digest")
    ids = [row[id_field] for row in rows]
    hashes = [row["row_sha256"] for row in rows]
    need(len(ids) == len(set(ids)), f"{label}:unique ids")
    if "row_ids_sha256" in document:
        need(document["row_ids_sha256"] == digest(ids), f"{label}:id digest")
    if "row_hashes_sha256" in document:
        need(
            document["row_hashes_sha256"] == digest(hashes),
            f"{label}:hash digest",
        )
    if verify_each_row:
        for row in rows:
            validate_row_closure(row, label)
    return rows


def qbox(values: list[str] | tuple[str, ...]) -> tuple[Q, ...]:
    box = tuple(Q(value) for value in values)
    need(
        len(box) == 6
        and all(box[2 * axis] < box[2 * axis + 1] for axis in range(3)),
        "strict positive rational box",
    )
    return box


def box_text(box: tuple[Q, ...]) -> list[str]:
    return [str(value) for value in box]


def volume(box: tuple[Q, ...]) -> Q:
    return (
        (box[1] - box[0])
        * (box[3] - box[2])
        * (box[5] - box[4])
    )


def strict_inside(inner: tuple[Q, ...], outer: tuple[Q, ...]) -> bool:
    return all(
        outer[2 * axis] < inner[2 * axis]
        < inner[2 * axis + 1] < outer[2 * axis + 1]
        for axis in range(3)
    )


def positive_overlap(left: tuple[Q, ...], right: tuple[Q, ...]) -> bool:
    return all(
        max(left[2 * axis], right[2 * axis])
        < min(left[2 * axis + 1], right[2 * axis + 1])
        for axis in range(3)
    )


def signature_payload(signature: dict[str, Any], chart: str) -> dict[str, Any]:
    result = {
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
    need(set(result) == SIGNATURE_FIELDS, "dynamic ten-field signature")
    return result


def signature_from_geometry(row: dict[str, Any]) -> dict[str, Any]:
    result = {
        "official_key_id": row["official_key_id"],
        "official_key_ordinal": row["official_key_ordinal"],
        "official_key_row": row["official_key_row"],
        "ordered_integer_wall_events": row["ordered_integer_wall_events"],
        "outgoing_cell": row["outgoing_cell"],
        "roof": row["roof"],
        "signed_wall_word": row["signed_wall_word"],
        "source_chart": row["chart"],
        "target_chart": row["target_chart"],
        "target_lift": row["owner_target"],
    }
    need(set(result) == SIGNATURE_FIELDS, "geometry ten-field signature")
    return result


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    need("row_sha256" not in row, "unclosed row")
    row["row_sha256"] = digest(row)
    return row


def validate_row_closure(row: dict[str, Any], label: str) -> None:
    payload = dict(row)
    row_hash = payload.pop("row_sha256")
    need(row_hash == digest(payload), f"{label}:row closure")


def ledger_object(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": LEDGER_SCHEMA,
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest(
            [row["Round290_inner_support_row_id"] for row in rows]
        ),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def deterministic_gzip_bytes(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=buffer, mtime=0
    ) as handle:
        handle.write(canonical(value) + b"\n")
    return buffer.getvalue()


class IntervalNode:
    """Exact one-dimensional interval index used only as a shortlist."""

    __slots__ = ("center", "cross_lower", "cross_upper", "left", "right")

    def __init__(self, rows: list[tuple[Any, ...]]):
        need(bool(rows), "nonempty interval node")
        midpoints = sorted((row[4][0] + row[4][1]) / 2 for row in rows)
        self.center = midpoints[len(midpoints) // 2]
        left: list[tuple[Any, ...]] = []
        right: list[tuple[Any, ...]] = []
        cross: list[tuple[Any, ...]] = []
        for row in rows:
            if row[4][1] <= self.center:
                left.append(row)
            elif row[4][0] >= self.center:
                right.append(row)
            else:
                cross.append(row)
        if not cross:
            ordered = sorted(rows, key=lambda row: (row[4][0], row[4][1], row[0]))
            middle = len(ordered) // 2
            cross = [ordered[middle]]
            left = ordered[:middle]
            right = ordered[middle + 1:]
            self.center = (cross[0][4][0] + cross[0][4][1]) / 2
        self.cross_lower = sorted(cross, key=lambda row: row[4][0])
        self.cross_upper = sorted(
            cross, key=lambda row: row[4][1], reverse=True
        )
        self.left = IntervalNode(left) if left else None
        self.right = IntervalNode(right) if right else None

    def query(
        self,
        lower: Q,
        upper: Q,
        output: list[tuple[Any, ...]],
    ) -> None:
        if upper <= self.center:
            for row in self.cross_lower:
                if row[4][0] >= upper:
                    break
                output.append(row)
            if self.left is not None:
                self.left.query(lower, upper, output)
        elif lower >= self.center:
            for row in self.cross_upper:
                if row[4][1] <= lower:
                    break
                output.append(row)
            if self.right is not None:
                self.right.query(lower, upper, output)
        else:
            output.extend(self.cross_lower)
            if self.left is not None:
                self.left.query(lower, upper, output)
            if self.right is not None:
                self.right.query(lower, upper, output)


# Evaluators are deliberately imported only after their source-byte pins have
# been checked.  Fork workers inherit these read-only registries.
R174: Any = None
R179WALL: Any = None
R270: Any = None
TABLES: Any = None
R198: Any = None
R195: Any = None
R186: Any = None
W_FACTOR_GEOMETRY: Any = None
TASKS: list[dict[str, Any]] = []


class PinnedSourceOnlyLoader(importlib.abc.Loader):
    """Compile one already-pinned source file directly, never a .pyc."""

    def __init__(self, module_name: str, path: Path, expected_hash: str):
        self.module_name = module_name
        self.path = path
        self.expected_hash = expected_hash

    def create_module(self, spec: Any) -> None:
        del spec
        return None

    def exec_module(self, module: Any) -> None:
        raw = secure_regular_file(self.path, maximum=10_000_000)
        need(
            hashlib.sha256(raw).hexdigest() == self.expected_hash,
            f"source-only loader pin:{self.module_name}",
        )
        module.__file__ = str(self.path)
        module.__cached__ = None
        code = compile(
            raw,
            str(self.path),
            "exec",
            dont_inherit=True,
            optimize=sys.flags.optimize,
        )
        exec(code, module.__dict__)


class PinnedSourceOnlyFinder(importlib.abc.MetaPathFinder):
    """Resolve the complete evaluator closure only to pinned HERE sources."""

    def find_spec(
        self,
        fullname: str,
        path: Any = None,
        target: Any = None,
    ) -> Any:
        del path, target
        expected = EVALUATOR_MODULE_PINS.get(fullname)
        if expected is None:
            return None
        source = (HERE / (fullname + ".py")).resolve()
        loader = PinnedSourceOnlyLoader(fullname, source, expected)
        return importlib.util.spec_from_loader(
            fullname,
            loader,
            origin=str(source),
        )


def verify_loaded_evaluator_module(
    module_name: str,
    expected_hash: str,
) -> None:
    module = sys.modules.get(module_name)
    need(module is not None, f"evaluator module loaded:{module_name}")
    expected_path = (HERE / (module_name + ".py")).resolve()
    module_path = Path(module.__file__).resolve()
    origin = Path(module.__spec__.origin).resolve()
    need(
        module_path == expected_path
        and origin == expected_path
        and isinstance(module.__loader__, PinnedSourceOnlyLoader)
        and getattr(module, "__cached__", None) is None
        and file_sha256(expected_path) == expected_hash,
        f"evaluator module source identity:{module_name}",
    )


def load_pinned_evaluators() -> dict[str, Any]:
    global R174, R179WALL, R270, TABLES, R198, R195, R186
    global W_FACTOR_GEOMETRY
    need(PRODUCER.stem not in sys.modules, "Round290 producer already imported")
    preloaded = sorted(
        module_name for module_name in EVALUATOR_MODULE_PINS
        if module_name in sys.modules
    )
    need(not preloaded, "preloaded evaluator modules:" + ",".join(preloaded))
    for module_name, expected in EVALUATOR_MODULE_PINS.items():
        filename = module_name + ".py"
        need(
            hashlib.sha256(
                secure_regular_file(HERE / filename, maximum=10_000_000)
            ).hexdigest()
            == expected,
            f"upstream evaluator source pin:{filename}",
        )
    finder = PinnedSourceOnlyFinder()
    sys.meta_path.insert(0, finder)
    try:
        R174 = importlib.import_module(
            "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization"
        )
        R179WALL = importlib.import_module(
            "cm2_round179_source_g_residual_tube_arrangement_verifier"
        )
        R270 = importlib.import_module(
            "cm2_round270_source_g_outgoing_g_factor_signature_materialization"
        )
    finally:
        need(
            sys.meta_path and sys.meta_path[0] is finder,
            "pinned source finder precedence retained",
        )
        sys.meta_path.pop(0)
    unexpected = sorted(
        module_name for module_name in sys.modules
        if module_name.startswith("cm2_")
        and module_name not in EVALUATOR_MODULE_PINS
        and module_name != __name__
    )
    need(
        not unexpected,
        "unexpected transitive evaluator modules:" + ",".join(unexpected),
    )
    for module_name, expected in EVALUATOR_MODULE_PINS.items():
        verify_loaded_evaluator_module(module_name, expected)
    need(PRODUCER.stem not in sys.modules, "Round290 producer imported indirectly")

    need(FLINT_VERSION == "0.9.0", "python-flint 0.9.0")
    ctx.prec = 256
    need(ctx.prec == 256, "fixed 256-bit FLINT precision")
    chain = R270.r207.check_inputs()
    R198 = R270.r207.r203.r198
    R195 = R198.r195
    R186 = R195.r191.r189.r188.r186
    W_FACTOR_GEOMETRY = R186.factor_geometry
    factor_r174 = R186.r179.r174
    need(
        factor_r174.__name__
        == "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier",
        "independent pinned factor evaluator",
    )
    R270.R174 = factor_r174
    R270.R195 = R195
    TABLES = R174.registry_tables(R174.load_inputs()["gate5"])
    need(PRODUCER.stem not in sys.modules, "Round290 producer imported")
    return chain


def atlas_box(values: tuple[Q, ...], label: str) -> Any:
    return R174.atlas.AtlasBox(*values, 0, label)


def dynamic_signature(
    task: dict[str, Any],
    values: tuple[Q, ...],
    label: str,
) -> dict[str, Any] | None:
    box = atlas_box(values, label)
    if R174.chart_domain_status(box) != "STRICT_INSIDE_TRUE_SOURCE_CHART":
        return None
    signature, _rejected = R174.dynamic_signature(
        task["source_chart"],
        box,
        task["owner_target"],
        TABLES,
    )
    if signature is None:
        return None
    payload = signature_payload(signature, task["source_chart"])
    if (
        payload != task["expected_signature"]
        or digest(payload) != task["expected_signature_sha256"]
        or payload["source_chart"] != task["source_chart"]
        or payload["target_lift"] != task["owner_target"]
        or payload["official_key_id"] != task["official_key_id"]
        or payload["official_key_ordinal"] != task["official_key_ordinal"]
        or payload["official_key_row"] != task["official_key_row"]
    ):
        return None
    return payload


def independently_evaluate_active_side(
    task: dict[str, Any],
    values: tuple[Q, ...],
    label: str,
) -> dict[str, Any] | None:
    """Evaluate the signed-region side separately from return signature."""

    round_number = task["source_round"]
    box = atlas_box(values, label)
    source = task["source_row"]
    if round_number in {269, 270}:
        R186.factor_geometry = (
            W_FACTOR_GEOMETRY
            if round_number == 269
            else R270.factor_geometry_g
        )
        profiles = R198.selected_factor_profiles(task["collar"], box)
        hplus = profiles["HPLUS"]["selected_sign"]
        hminus = profiles["HMINUS"]["selected_sign"]
        if (
            hplus != source["HPLUS_sign"]
            or hminus != source["HMINUS_sign"]
            or hplus not in STRICT_SIGNS
            or hminus not in STRICT_SIGNS
        ):
            return None
        product_sign = R195.multiply_signs(hplus, hminus)
        if product_sign != source["region_factor_sign"]:
            return None
        return {
            "factor_model": (
                "PINNED_ROUND269_W_FACTOR_GEOMETRY"
                if round_number == 269
                else "PINNED_ROUND270_EXACT_G_FACTOR_GEOMETRY"
            ),
            "HPLUS_sign": hplus,
            "HMINUS_sign": hminus,
            "region_product_sign": product_sign,
            "graph_classification": source["graph_classification"],
            "active_factor_or_graph_side_strict_on_whole_inner_box": True,
        }

    collar = task["collar"]
    geometry = R179WALL.independent_geometry(
        collar["chart"], collar["owner_target"], box
    )
    reason_parts = collar["reason_label"].split(":")
    need(len(reason_parts) == 3, "wall reason label")
    _, axis, wall_text = reason_parts
    need(axis in {"X", "Y"}, "wall axis")
    wall = int(wall_text)
    source_value = (
        geometry["source_x" if axis == "X" else "source_y"][0] - wall
    )
    target_value = geometry["hit_x" if axis == "X" else "hit_y"][0] - wall
    source_sign = R179WALL.arb_sign(source_value)
    target_sign = R179WALL.arb_sign(target_value)
    if (
        source_sign != source["witness_source_factor_sign"]
        or target_sign != source["witness_target_factor_sign"]
        or source_sign not in STRICT_SIGNS
        or target_sign not in STRICT_SIGNS
    ):
        return None
    product_sign = R195.multiply_signs(source_sign, target_sign)
    if product_sign != source["region_product_sign"]:
        return None
    return {
        "factor_model": "PINNED_ROUND179_INDEPENDENT_WALL_FACTOR_GEOMETRY",
        "wall_axis": axis,
        "wall_coordinate": wall,
        "source_factor_sign": source_sign,
        "target_factor_sign": target_sign,
        "region_product_sign": product_sign,
        "graph_classification": source["graph_classification"],
        "active_factor_or_graph_side_strict_on_whole_inner_box": True,
    }


def centered_box(
    envelope: tuple[Q, ...],
    fractions: tuple[Q, Q, Q],
) -> tuple[Q, ...]:
    values: list[Q] = []
    for axis, fraction in enumerate(fractions):
        lower, upper = envelope[2 * axis:2 * axis + 2]
        width = upper - lower
        center = lower + width * fraction
        radius = min(
            center - lower,
            upper - center,
            width / (2**20),
        ) / 4
        need(radius > 0, "positive catalogue radius")
        values.extend((center - radius, center + radius))
    result = tuple(values)
    need(strict_inside(result, envelope), "catalogue box strict interior")
    return result


def witness_expansion_box(
    envelope: tuple[Q, ...],
    point: tuple[Q, Q, Q],
    depth: int,
) -> tuple[Q, ...]:
    values: list[Q] = []
    for axis, center in enumerate(point):
        lower, upper = envelope[2 * axis:2 * axis + 2]
        need(lower < center < upper, "strict witness interior")
        margin = min(center - lower, upper - center)
        radius = margin / (2 ** (depth + 1))
        need(radius > 0, "positive witness expansion radius")
        values.extend((center - radius, center + radius))
    result = tuple(values)
    need(strict_inside(result, envelope), "witness box strict interior")
    return result


def reconstruct_worker(index: int) -> dict[str, Any]:
    """Rebuild one row from upstream provenance and fresh whole-box tests."""

    task = TASKS[index]
    envelope = tuple(Q(value) for value in task["envelope"])
    found: tuple[
        tuple[Q, ...],
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
    ] | None = None

    if task["source_round"] in {271, 272}:
        point = tuple(Q(value) for value in task["source_row"]["witness_point"])
        need(len(point) == 3, "three-dimensional wall witness")
        for depth in range(61):
            values = witness_expansion_box(envelope, point, depth)
            signature = dynamic_signature(
                task,
                values,
                f"round290-verifier-wall-signature:{index}:{depth}",
            )
            if signature is None:
                continue
            side = independently_evaluate_active_side(
                task,
                values,
                f"round290-verifier-wall-side:{index}:{depth}",
            )
            if side is None:
                continue
            found = (
                values,
                signature,
                side,
                {
                    "search_method":
                        "NESTED_DYADIC_EXPANSION_AROUND_PINNED_STRICT_WITNESS",
                    "largest_successful_dyadic_box_depth": depth,
                    "maximum_permitted_dyadic_depth": 60,
                    "point_witness_used_only_as_search_center": True,
                    "point_witness_itself_used_as_inner_support": False,
                    "witness_generation_path": (
                        f"{task['source_signature_row_id']}:"
                        f"nested-dyadic-depth:{depth}"
                    ),
                },
            )
            break
    else:
        for ordinal, fractions in enumerate(
            product(SEARCH_FRACTIONS, repeat=3)
        ):
            values = centered_box(envelope, fractions)
            signature = dynamic_signature(
                task,
                values,
                f"round290-verifier-factor-signature:{index}:{ordinal}",
            )
            if signature is None:
                continue
            side = independently_evaluate_active_side(
                task,
                values,
                f"round290-verifier-factor-side:{index}:{ordinal}",
            )
            if side is None:
                continue
            found = (
                values,
                signature,
                side,
                {
                    "search_method":
                        "FINITE_ORDERED_RATIONAL_FACTOR_SIDE_CATALOGUE",
                    "catalogue_size": SEARCH_CATALOGUE_SIZE,
                    "selected_catalogue_ordinal_zero_based": ordinal,
                    "selected_relative_center_fractions": [
                        str(value) for value in fractions
                    ],
                    "catalogue_order_sha256": digest(
                        [str(value) for value in SEARCH_FRACTIONS]
                    ),
                    "failure_requires_complete_catalogue_exhaustion": True,
                    "witness_generation_path": (
                        f"{task['source_signature_row_id']}:"
                        f"ordered-rational-catalogue-ordinal:{ordinal}"
                    ),
                },
            )
            break

    need(found is not None, f"independent search failure:{task['canonical_atom_id']}")
    values, actual_signature, side_proof, search_proof = found
    leaf_box = qbox(task["Round182_leaf_exact_box"])
    need(
        volume(values) > 0
        and strict_inside(values, envelope)
        and strict_inside(values, leaf_box)
        and R174.chart_domain_status(
            atlas_box(
                values,
                f"round290-verifier-final-chart-guard:{index}",
            )
        )
        == "STRICT_INSIDE_TRUE_SOURCE_CHART"
        and actual_signature == task["expected_signature"]
        and digest(actual_signature) == task["expected_signature_sha256"],
        "freshly accepted whole inner support",
    )

    return close_row(
        {
            "Round290_inner_support_row_id":
                "round290-isolated-inner-support:"
                + digest(
                    [
                        task["canonical_atom_id"],
                        box_text(values),
                        task["expected_signature_sha256"],
                    ]
                ),
            "canonical_atom_id": task["canonical_atom_id"],
            "Round288_atom_disposition_row_id":
                task["Round288_atom_disposition_row_id"],
            "Round182_leaf_row_id": task["Round182_leaf_row_id"],
            "source_signature_row_id": task["source_signature_row_id"],
            "source_round": task["source_round"],
            "source_chart": task["source_chart"],
            "owner_target": task["owner_target"],
            "canonical_atom_frozen_support_envelope": task["envelope"],
            "Round182_leaf_exact_box": task["Round182_leaf_exact_box"],
            "exact_positive_volume_rational_inner_support_box":
                box_text(values),
            "exact_inner_support_volume": str(volume(values)),
            "strictly_inside_canonical_atom_frozen_support_envelope": True,
            "strictly_inside_original_Round182_leaf": True,
            "strictly_inside_true_source_chart_guard": True,
            "touches_half_open_or_excluded_face": False,
            "expected_complete_10_field_return_signature":
                task["expected_signature"],
            "dynamically_recomputed_complete_10_field_return_signature":
                actual_signature,
            "complete_10_field_return_signature_sha256":
                task["expected_signature_sha256"],
            "official_key_id": actual_signature["official_key_id"],
            "official_key_ordinal": actual_signature["official_key_ordinal"],
            "official_key_row": actual_signature["official_key_row"],
            "dynamic_signature_constant_on_whole_inner_box": True,
            "independent_source_signed_region_side_proof": side_proof,
            "deterministic_inner_support_search_proof": search_proof,
            "whole_leaf_envelope_used_as_inner_support": False,
            "point_witness_used_as_inner_support": False,
            "formal_new_occurrence_credit": 0,
            "formal_component_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
        }
    )


def verify_atom_document(
    document: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = validate_closed_rows(
        document,
        "canonical_atom_id",
        332_016,
        "Round279 atom ledger",
        verify_each_row=False,
    )
    need(
        document["schema"]
        == "cm2.round279.canonical-collar-atom-ledger.v1"
        and document["strict_subbox_atom_count"] == 4
        and document["source_signature_row_count"] == 332_020,
        "Round279 atom ledger contract",
    )
    return rows


def load_tasks_from_upstream() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Resolve the 21,160 tasks without reading any Round290 candidate row."""

    round288 = read_json(HERE / R288_RESULT)
    verify_direct_result(round288, "Round288")
    need(
        round288["status"].startswith(
            "PASS_ROUND288_CACHELESS_ATOM_IDENTITY_GATE_AUDIT"
        )
        and round288["census"][
            "isolated_new_candidate_inner_support_residual_count"
        ] == 21_160
        and round288["census"][
            "conditional_occurrence_total_if_all_inner_supports_later_pass"
        ] == 421_804
        and round288["strict_nonpromotion"][
            "formal_new_expanded_occurrence_credit"
        ] == 0,
        "Round288 frozen isolated residual baseline",
    )

    disposition_document = read_gzip_json(HERE / R288_DISPOSITIONS)
    dispositions = validate_closed_rows(
        disposition_document,
        "Round288_atom_disposition_row_id",
        332_016,
        "Round288 disposition ledger",
        verify_each_row=False,
    )
    need(
        disposition_document["schema"]
        == "cm2.round288.canonical-atom-occurrence-disposition-ledger.v1",
        "Round288 disposition schema",
    )
    unresolved = [
        row for row in dispositions
        if row["occurrence_identity_disposition"] == UNRESOLVED_STATE
    ]
    need(len(unresolved) == 21_160, "Round288 unresolved row census")
    for row in unresolved:
        validate_row_closure(row, "selected Round288 unresolved disposition")
    unresolved_by_atom = {
        row["canonical_atom_id"]: row for row in unresolved
    }
    need(
        len(unresolved_by_atom) == 21_160,
        "Round288 unique unresolved atoms",
    )
    del dispositions, disposition_document
    gc.collect()

    atom_document = read_gzip_json(HERE / R279_ATOMS)
    atoms = verify_atom_document(atom_document)
    selected_atoms = {
        row["canonical_atom_id"]: row
        for row in atoms
        if row["canonical_atom_id"] in unresolved_by_atom
    }
    need(len(selected_atoms) == 21_160, "Round279 selected isolated atoms")
    for row in selected_atoms.values():
        validate_row_closure(row, "selected Round279 isolated atom")
    del atoms, atom_document
    gc.collect()

    round182 = closed_result(R182_ROWS)
    leaf_rows = unpack(round182, "collar_leaf_rows")
    collar_rows = unpack(round182, "collar_occurrence_rows")
    needed_leaf_ids = {
        atom["Round182_leaf_row_id"] for atom in selected_atoms.values()
    }
    leaves = {
        row["row_id"]: row for row in leaf_rows
        if row["row_id"] in needed_leaf_ids
    }
    needed_occurrences = {row["occurrence_row_id"] for row in leaves.values()}
    collars = {
        row["Round179_occurrence_row_id"]: row for row in collar_rows
        if row["Round179_occurrence_row_id"] in needed_occurrences
    }
    need(
        len(leaf_rows) == 202_840
        and len(collar_rows) == 54_220
        and len(leaves) == 20_484
        and len(collars) == 20_484,
        "Round182 isolated leaf/collar reconstruction",
    )
    del round182, leaf_rows, collar_rows, needed_occurrences, needed_leaf_ids
    gc.collect()

    needed_source_ids: dict[int, set[str]] = collections.defaultdict(set)
    for atom in selected_atoms.values():
        need(
            len(atom["source_rounds"]) == 1
            and len(atom["source_signature_row_ids"]) == 1
            and len(atom["frozen_true_support_boxes"]) == 1,
            "isolated atom singleton provenance",
        )
        round_number = atom["source_rounds"][0]
        need(round_number in SOURCE_SPECS, "isolated atom source round")
        needed_source_ids[round_number].add(
            atom["source_signature_row_ids"][0]
        )

    source_maps: dict[int, dict[str, dict[str, Any]]] = {}
    expected_source_counts = {
        269: 187_128,
        270: 37_712,
        271: 70_420,
        272: 720,
    }
    for round_number, (filename, ledger_name) in SOURCE_SPECS.items():
        source_result = closed_result(filename)
        source_ledger = source_result[ledger_name]
        source_rows = validate_closed_rows(
            source_ledger,
            "signed_region_row_id",
            expected_source_counts[round_number],
            f"Round{round_number} source ledger",
            verify_each_row=False,
        )
        source_maps[round_number] = {
            row["signed_region_row_id"]: row
            for row in source_rows
            if row["signed_region_row_id"]
            in needed_source_ids[round_number]
        }
        need(
            set(source_maps[round_number]) == needed_source_ids[round_number],
            f"Round{round_number} complete selected source map",
        )
        for row in source_maps[round_number].values():
            validate_row_closure(row, f"selected Round{round_number} source")
        del source_result, source_ledger, source_rows
        gc.collect()

    tasks: list[dict[str, Any]] = []
    source_round_histogram: collections.Counter[int] = collections.Counter()
    for canonical_atom_id in sorted(unresolved_by_atom):
        disposition = unresolved_by_atom[canonical_atom_id]
        atom = selected_atoms[canonical_atom_id]
        round_number = atom["source_rounds"][0]
        source_id = atom["source_signature_row_ids"][0]
        source = source_maps[round_number][source_id]
        leaf = leaves[atom["Round182_leaf_row_id"]]
        collar = collars[leaf["occurrence_row_id"]]
        signature = atom["complete_10_field_return_signature"]
        envelope = qbox(atom["frozen_true_support_boxes"][0])
        leaf_box = qbox(leaf["box"])

        need(
            disposition["source_rounds"] == atom["source_rounds"]
            and disposition["source_signature_row_ids"]
            == atom["source_signature_row_ids"]
            and disposition["frozen_positive_rational_support_envelopes"]
            == atom["frozen_true_support_boxes"]
            and disposition["complete_10_field_return_signature_sha256"]
            == atom["complete_10_field_return_signature_sha256"]
            and source["Round182_leaf_row_id"] == leaf["row_id"]
            and source["local_return_signature"] == signature
            and source["complete_10_field_return_signature_sha256"]
            == atom["complete_10_field_return_signature_sha256"]
            and digest(signature)
            == atom["complete_10_field_return_signature_sha256"]
            and disposition["source_chart"] == atom["source_chart"]
            == collar["chart"] == signature["source_chart"]
            and disposition["owner_target"] == atom["owner_target"]
            == collar["owner_target"] == signature["target_lift"]
            and envelope == leaf_box
            and volume(envelope) > 0
            and disposition["formal_new_occurrence_credit"] == 0
            and disposition["formal_component_credit"] == 0
            and disposition["formal_maximality_credit"] == 0
            and disposition["Jx_Jy_same_point_glue_credit"] == 0,
            "isolated disposition/atom/source/leaf/collar binding",
        )
        if round_number in {269, 270}:
            need(
                source["chart"] == atom["source_chart"]
                and source["owner_target"] == atom["owner_target"]
                and source["side_specific_signature_credit"] == 1
                and source["expanded_occurrence_credit"] == 0,
                "factor-source zero-credit signature binding",
            )
        else:
            need(
                source["collar_kind"] == "WALL"
                and source["side_signature_credit"] == 1
                and source["expanded_occurrence_credit"] == 0
                and len(source["witness_point"]) == 3,
                "wall-source zero-credit witness binding",
            )

        tasks.append(
            {
                "canonical_atom_id": canonical_atom_id,
                "Round288_atom_disposition_row_id":
                    disposition["Round288_atom_disposition_row_id"],
                "Round182_leaf_row_id": leaf["row_id"],
                "source_round": round_number,
                "source_signature_row_id": source_id,
                "source_row": source,
                "collar": collar,
                "source_chart": atom["source_chart"],
                "owner_target": atom["owner_target"],
                "envelope": atom["frozen_true_support_boxes"][0],
                "Round182_leaf_exact_box": leaf["box"],
                "expected_signature": signature,
                "expected_signature_sha256":
                    atom["complete_10_field_return_signature_sha256"],
                "official_key_id": signature["official_key_id"],
                "official_key_ordinal": signature["official_key_ordinal"],
                "official_key_row": signature["official_key_row"],
            }
        )
        source_round_histogram[round_number] += 1

    need(
        source_round_histogram
        == {269: 3_968, 270: 6_728, 271: 10_448, 272: 16},
        "isolated source-round census",
    )
    need(len(tasks) == 21_160, "complete independent task list")
    del (
        unresolved_by_atom,
        selected_atoms,
        leaves,
        collars,
        source_maps,
        needed_source_ids,
    )
    gc.collect()
    return tasks, {
        "source_round_histogram": dict(source_round_histogram),
        "Round288_unresolved_disposition_count": 21_160,
        "Round279_isolated_atom_count": 21_160,
        "Round182_unique_isolated_leaf_count": 20_484,
    }


def reconstruct_inner_support_rows(
    tasks: list[dict[str, Any]],
    processes: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    global TASKS
    TASKS = tasks
    need(1 <= processes <= 64, "process count in [1,64]")
    rows: list[dict[str, Any]] = []
    if processes == 1:
        iterator = map(reconstruct_worker, range(len(TASKS)))
        for done, row in enumerate(iterator, 1):
            rows.append(row)
            if done % 2_000 == 0:
                print(
                    json.dumps(
                        {"round290_verifier_progress": done, "total": len(TASKS)},
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                    flush=True,
                )
    else:
        with mp.get_context("fork").Pool(processes) as pool:
            for done, row in enumerate(
                pool.imap_unordered(
                    reconstruct_worker,
                    range(len(TASKS)),
                    chunksize=8,
                ),
                1,
            ):
                rows.append(row)
                if done % 2_000 == 0:
                    print(
                        json.dumps(
                            {
                                "round290_verifier_progress": done,
                                "total": len(TASKS),
                            },
                            sort_keys=True,
                        ),
                        file=sys.stderr,
                        flush=True,
                    )
    rows.sort(key=lambda row: row["Round290_inner_support_row_id"])
    need(len(rows) == 21_160, "all independent worker rows accepted")
    ids = [row["Round290_inner_support_row_id"] for row in rows]
    atoms = [row["canonical_atom_id"] for row in rows]
    need(
        len(ids) == len(set(ids)) == 21_160
        and len(atoms) == len(set(atoms)) == 21_160,
        "unique rebuilt row and atom ids",
    )

    method_histogram: collections.Counter[str] = collections.Counter()
    factor_model_histogram: collections.Counter[str] = collections.Counter()
    selected_ordinal_histogram: collections.Counter[int] = collections.Counter()
    wall_depth_histogram: collections.Counter[int] = collections.Counter()
    for row in rows:
        validate_row_closure(row, "independent rebuilt row")
        box = qbox(row["exact_positive_volume_rational_inner_support_box"])
        envelope = qbox(row["canonical_atom_frozen_support_envelope"])
        leaf = qbox(row["Round182_leaf_exact_box"])
        need(
            Q(row["exact_inner_support_volume"]) == volume(box) > 0
            and strict_inside(box, envelope)
            and strict_inside(box, leaf)
            and row["expected_complete_10_field_return_signature"]
            == row[
                "dynamically_recomputed_complete_10_field_return_signature"
            ]
            and digest(
                row["expected_complete_10_field_return_signature"]
            )
            == row["complete_10_field_return_signature_sha256"]
            and row["source_chart"]
            == row["expected_complete_10_field_return_signature"]["source_chart"]
            and row["owner_target"]
            == row["expected_complete_10_field_return_signature"]["target_lift"],
            "rebuilt row exact support/signature semantics",
        )
        method = row["deterministic_inner_support_search_proof"][
            "search_method"
        ]
        model = row["independent_source_signed_region_side_proof"][
            "factor_model"
        ]
        method_histogram[method] += 1
        factor_model_histogram[model] += 1
        proof = row["deterministic_inner_support_search_proof"]
        if "selected_catalogue_ordinal_zero_based" in proof:
            selected_ordinal_histogram[
                proof["selected_catalogue_ordinal_zero_based"]
            ] += 1
        if "largest_successful_dyadic_box_depth" in proof:
            wall_depth_histogram[
                proof["largest_successful_dyadic_box_depth"]
            ] += 1

    need(
        method_histogram
        == {
            "FINITE_ORDERED_RATIONAL_FACTOR_SIDE_CATALOGUE": 10_696,
            "NESTED_DYADIC_EXPANSION_AROUND_PINNED_STRICT_WITNESS": 10_464,
        }
        and factor_model_histogram
        == {
            "PINNED_ROUND269_W_FACTOR_GEOMETRY": 3_968,
            "PINNED_ROUND270_EXACT_G_FACTOR_GEOMETRY": 6_728,
            "PINNED_ROUND179_INDEPENDENT_WALL_FACTOR_GEOMETRY": 10_464,
        }
        and wall_depth_histogram == {0: 10_464},
        "independent search and factor model census",
    )
    return rows, {
        "search_method_histogram": dict(sorted(method_histogram.items())),
        "factor_model_histogram": dict(sorted(factor_model_histogram.items())),
        "selected_ordinal_histogram_sha256":
            digest(sorted(selected_ordinal_histogram.items())),
        "wall_depth_histogram": {
            str(key): value for key, value in sorted(wall_depth_histogram.items())
        },
        "fresh_whole_box_dynamic_signature_count": 21_160,
        "fresh_whole_box_active_side_count": 21_160,
        "fresh_strict_chart_guard_count": 21_160,
        "half_open_or_excluded_face_touch_count": 0,
    }


def load_existing_occurrences() -> list[tuple[Any, ...]]:
    """Reconstruct the complete pre-Round290 positive-open frontier."""

    rows: list[tuple[Any, ...]] = []
    round174 = closed_result(R174_ROWS)
    for row in unpack(round174, "resolved_3d_occurrence_rows"):
        signature = signature_from_geometry(row)
        box = qbox(row["box"])
        need(
            row["ambient_dimension"] == 3
            and row["physical_open_subset_positive"] is True
            and Q(row["coordinate_volume"]) == volume(box) > 0,
            "Round174 existing occurrence geometry",
        )
        rows.append(
            (
                row["row_id"],
                "ROUND174_RESOLVED",
                row["chart"],
                digest(signature),
                box,
            )
        )
    del round174
    gc.collect()

    round179 = closed_result(R179_ROWS)
    for row in unpack(round179, "resolved_3d_child_rows"):
        signature = signature_from_geometry(row)
        box = qbox(row["box"])
        need(
            row["ambient_dimension"] == 3
            and row["credit_kind"] == "LOCAL_POSITIVE_3D_OCCURRENCE_ONLY"
            and Q(row["coordinate_volume"]) == volume(box) > 0,
            "Round179 existing occurrence geometry",
        )
        rows.append(
            (
                row["row_id"],
                "ROUND179_RESOLVED",
                row["chart"],
                digest(signature),
                box,
            )
        )
    del round179
    gc.collect()

    round204 = closed_result(R204_CERT)
    ledger204 = round204["formal_local_open_3D_region_ledger"]
    rows204 = validate_closed_rows(
        ledger204,
        "region_row_id",
        736,
        "Round204 existing occurrence ledger",
        verify_each_row=False,
    )
    for row in rows204:
        signature = signature_from_geometry(row)
        box = qbox(row["leaf_exact_box"])
        need(
            row["ambient_dimension"] == 3
            and row["strict_open_region"] is True
            and row["positive_coordinate_volume"] is True
            and row["formal_local_signature_credit"] == 1,
            "Round204 existing occurrence geometry",
        )
        rows.append(
            (
                row["region_row_id"],
                "ROUND204_REGION",
                row["chart"],
                digest(signature),
                box,
            )
        )
    del round204, ledger204, rows204
    gc.collect()

    round208 = closed_result(R208_CERT)
    ledger208 = round208["formal_local_open_3D_signature_ledger"]
    rows208 = validate_closed_rows(
        ledger208,
        "region_row_id",
        36_040,
        "Round208 existing occurrence ledger",
        verify_each_row=False,
    )
    for row in rows208:
        signature = row["local_return_signature"]
        need(set(signature) == SIGNATURE_FIELDS, "Round208 ten-field signature")
        box = qbox(row["Round182_leaf_box"])
        need(
            row["strict_open_3D_region_exists"] is True
            and row["formal_local_open_3D_signature_credit"] == 1,
            "Round208 existing occurrence geometry",
        )
        rows.append(
            (
                row["region_row_id"],
                "ROUND208_REGION",
                signature["source_chart"],
                digest(signature),
                box,
            )
        )
    del round208, ledger208, rows208
    gc.collect()

    source_histogram = collections.Counter(row[1] for row in rows)
    need(
        source_histogram
        == {
            "ROUND174_RESOLVED": 72_500,
            "ROUND179_RESOLVED": 17_192,
            "ROUND204_REGION": 736,
            "ROUND208_REGION": 36_040,
        }
        and len(rows) == 126_468,
        "complete reconstructed existing occurrence frontier",
    )
    return rows


def audit_existing_and_pairwise_overlap(
    rows: list[dict[str, Any]],
    existing: list[tuple[Any, ...]],
) -> dict[str, Any]:
    """Rerun exact positive-volume overlap tests on independently found boxes."""

    existing_by_chart: dict[
        str, list[tuple[Any, ...]]
    ] = collections.defaultdict(list)
    for item in existing:
        existing_by_chart[item[2]].append(item)
    existing_trees = {
        chart: IntervalNode(items)
        for chart, items in existing_by_chart.items()
    }

    existing_shortlist = 0
    existing_overlaps: list[tuple[str, str, str, str]] = []
    row_boxes: list[tuple[str, str, str, str, tuple[Q, ...]]] = []
    for row in rows:
        box = qbox(row["exact_positive_volume_rational_inner_support_box"])
        item = (
            row["canonical_atom_id"],
            "ROUND290_INNER_SUPPORT",
            row["source_chart"],
            row["complete_10_field_return_signature_sha256"],
            box,
        )
        row_boxes.append(item)
        candidates: list[tuple[Any, ...]] = []
        tree = existing_trees.get(row["source_chart"])
        need(tree is not None, "existing frontier chart")
        tree.query(box[0], box[1], candidates)
        existing_shortlist += len(candidates)
        for candidate in candidates:
            if positive_overlap(box, candidate[4]):
                existing_overlaps.append(
                    (
                        row["canonical_atom_id"],
                        candidate[0],
                        row["complete_10_field_return_signature_sha256"],
                        candidate[3],
                    )
                )
    need(
        not existing_overlaps,
        "Round290 positive-volume overlap with existing frontier",
    )

    groups: dict[
        tuple[str, str], list[tuple[Any, ...]]
    ] = collections.defaultdict(list)
    for item in row_boxes:
        groups[(item[2], item[3])].append(item)
    pair_shortlist = 0
    duplicate_pairs: list[tuple[str, str]] = []
    for items in groups.values():
        ordered = sorted(
            items,
            key=lambda item: (item[4][0], item[4][1], item[0]),
        )
        active: list[tuple[Any, ...]] = []
        for item in ordered:
            active = [
                other for other in active
                if other[4][1] > item[4][0]
            ]
            for other in active:
                pair_shortlist += 1
                if positive_overlap(item[4], other[4]):
                    duplicate_pairs.append((other[0], item[0]))
            active.append(item)
    need(
        not duplicate_pairs,
        "Round290 same-chart/same-signature positive-volume duplicate",
    )
    need(
        existing_shortlist == 2_307_614
        and pair_shortlist == 25_564,
        "exact independently reconstructed overlap shortlist census",
    )

    pair_attack_rows: tuple[dict[str, Any], dict[str, Any]] | None = None
    row_by_atom = {row["canonical_atom_id"]: row for row in rows}
    for items in groups.values():
        if len(items) >= 2:
            pair_attack_rows = (
                row_by_atom[items[0][0]],
                row_by_atom[items[1][0]],
            )
            break
    need(pair_attack_rows is not None, "pair attack fixture")
    existing_attack_base = rows[0]
    existing_attack_item = next(
        item for item in existing
        if item[2] == existing_attack_base["source_chart"]
    )
    return {
        "existing_occurrence_count": len(existing),
        "existing_interval_shortlist_comparison_count": existing_shortlist,
        "existing_positive_volume_overlap_count": len(existing_overlaps),
        "same_chart_same_signature_group_count": len(groups),
        "pairwise_shortlist_comparison_count": pair_shortlist,
        "same_chart_same_signature_positive_volume_duplicate_pair_count":
            len(duplicate_pairs),
        "existing_attack_fixture":
            (existing_attack_base, existing_attack_item),
        "pair_attack_fixture": pair_attack_rows,
    }


def expected_census(
    task_metadata: dict[str, Any],
    row_metadata: dict[str, Any],
    overlap_metadata: dict[str, Any],
) -> dict[str, Any]:
    source_round_histogram = task_metadata["source_round_histogram"]
    need(
        row_metadata["selected_ordinal_histogram_sha256"]
        == "6dfc1d54d52ebb078bde2279c9e43c91d6cf709fa9b9fc39a9a537aea0258968",
        "factor catalogue ordinal histogram",
    )
    return {
        "Round288_isolated_inner_support_residual_input_count": 21_160,
        "strict_positive_volume_inner_support_count": 21_160,
        "failure_residual_count": 0,
        "source_round_histogram": {
            str(key): value
            for key, value in sorted(source_round_histogram.items())
        },
        "search_method_histogram": row_metadata["search_method_histogram"],
        "factor_model_histogram": row_metadata["factor_model_histogram"],
        "largest_successful_wall_dyadic_depth_histogram":
            row_metadata["wall_depth_histogram"],
        "factor_catalogue_selected_ordinal_histogram_sha256":
            row_metadata["selected_ordinal_histogram_sha256"],
        "factor_catalogue_size_per_task": SEARCH_CATALOGUE_SIZE,
        "factor_catalogue_failure_residual_count": 0,
        "wall_dyadic_expansion_failure_residual_count": 0,
        "dynamic_signature_constant_whole_box_count": 21_160,
        "independent_active_factor_or_graph_side_whole_box_count": 21_160,
        "strict_chart_guard_interior_count": 21_160,
        "half_open_or_excluded_face_touch_count": 0,
        "existing_Round266_occurrence_count":
            overlap_metadata["existing_occurrence_count"],
        "existing_frontier_interval_shortlist_comparison_count":
            overlap_metadata["existing_interval_shortlist_comparison_count"],
        "existing_frontier_positive_volume_overlap_count":
            overlap_metadata["existing_positive_volume_overlap_count"],
        "same_chart_same_signature_pairwise_shortlist_comparison_count":
            overlap_metadata["pairwise_shortlist_comparison_count"],
        "same_chart_same_signature_positive_volume_duplicate_pair_count":
            overlap_metadata[
                "same_chart_same_signature_positive_volume_duplicate_pair_count"
            ],
        "conditional_distinct_new_atom_total": 295_336,
        "conditional_occurrence_total_if_Round288_and_Round290_later_promoted":
            421_804,
    }


def audit_candidate_ledger_object(
    candidate: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    need(set(candidate) == set(expected), "candidate ledger top-level fields")
    rows = validate_closed_rows(
        candidate,
        "Round290_inner_support_row_id",
        21_160,
        "Round290 candidate ledger",
    )
    need(
        candidate["schema"] == LEDGER_SCHEMA
        and candidate["every_row_closed_by_own_SHA256"] is True,
        "Round290 candidate ledger schema/closure flag",
    )
    need(
        candidate["rows_sha256"] == expected["rows_sha256"]
        and candidate["row_ids_sha256"] == expected["row_ids_sha256"]
        and candidate["row_hashes_sha256"] == expected["row_hashes_sha256"],
        "Round290 candidate ledger commitments equal reconstruction",
    )
    for expected_row, candidate_row in zip(
        expected["rows"], rows, strict=True
    ):
        need(
            candidate_row == expected_row,
            "Round290 candidate exact row differs from reconstruction:"
            + expected_row["Round290_inner_support_row_id"],
        )


def audit_candidate_result_object(
    document: dict[str, Any],
    census: dict[str, Any],
    expected_ledger: dict[str, Any],
    evaluator_chain: dict[str, Any],
) -> dict[str, Any]:
    verify_direct_result(document, "Round290 candidate")
    need(
        set(document)
        == {
            "schema",
            "status",
            "input_file_pins",
            "input_source_pins",
            "census",
            "support_contract",
            "strict_nonpromotion",
            "required_next",
            "inner_support_ledger",
            "failure_residual_ledger",
            "provenance",
            "result_sha256",
        },
        "Round290 candidate result top-level contract",
    )
    need(
        document["schema"] == SCHEMA
        and document["status"] == EXPECTED_STATUS
        and document["input_file_pins"] == dict(sorted(UPSTREAM_PINS.items()))
        and document["input_source_pins"]
        == dict(sorted(UPSTREAM_SOURCE_PINS.items()))
        and document["census"] == census,
        "Round290 candidate schema/status/pins/census",
    )
    need(
        document["support_contract"] == EXPECTED_SUPPORT_CONTRACT
        and document["strict_nonpromotion"] == EXPECTED_NONPROMOTION
        and document["required_next"] == EXPECTED_REQUIRED_NEXT,
        "Round290 support/nonpromotion/required-next contract",
    )
    failure = document["failure_residual_ledger"]
    empty_digest = digest([])
    need(
        failure
        == {
            "row_count": 0,
            "rows_sha256": empty_digest,
            "row_ids_sha256": empty_digest,
            "row_hashes_sha256": empty_digest,
            "every_row_closed_by_own_SHA256": True,
            "rows": [],
        },
        "Round290 empty failure residual ledger",
    )
    ledger_metadata = {
        "filename": LEDGER.name,
        "row_count": expected_ledger["row_count"],
        "rows_sha256": expected_ledger["rows_sha256"],
        "row_ids_sha256": expected_ledger["row_ids_sha256"],
        "row_hashes_sha256": expected_ledger["row_hashes_sha256"],
        "file_sha256": CANDIDATE_PINS[LEDGER.name],
    }
    need(
        document["inner_support_ledger"] == ledger_metadata,
        "Round290 result-to-ledger exact commitment",
    )
    provenance = document["provenance"]
    need(
        set(provenance)
        == {
            "producer_sha256",
            "python_version",
            "python_flint_version",
            "precision_bits",
            "process_count",
            "seed_affects_output",
            "cache_or_pickle_input_used",
            "pinned_evaluator_chain",
        }
        and provenance["producer_sha256"] == CANDIDATE_PINS[PRODUCER.name]
        and provenance["python_version"] == sys.version.split()[0]
        and provenance["python_flint_version"] == str(ctx)
        and provenance["precision_bits"] == 256
        and provenance["process_count"] == 40
        and provenance["seed_affects_output"] is False
        and provenance["cache_or_pickle_input_used"] is False
        and provenance["pinned_evaluator_chain"] == evaluator_chain,
        "Round290 candidate provenance",
    )
    return {
        "candidate_schema": document["schema"],
        "candidate_status": document["status"],
        "candidate_result_sha256": document["result_sha256"],
        "candidate_file_sha256": CANDIDATE_PINS[RESULT.name],
        "candidate_census_exactly_reconstructed": True,
        "candidate_ledger_binding_exactly_reconstructed": True,
        "candidate_failure_residual_exactly_reconstructed": True,
        "candidate_zero_credit_contract_preserved": True,
    }


def read_and_audit_candidate(
    expected_ledger: dict[str, Any],
    census: dict[str, Any],
    evaluator_chain: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Read candidate rows only after all expected geometry has been rebuilt."""

    raw_ledger = secure_regular_file(LEDGER)
    raw_result = secure_regular_file(RESULT)
    need(
        hashlib.sha256(raw_ledger).hexdigest() == CANDIDATE_PINS[LEDGER.name],
        "Round290 candidate ledger file pin",
    )
    need(
        hashlib.sha256(raw_result).hexdigest() == CANDIDATE_PINS[RESULT.name],
        "Round290 candidate result file pin",
    )
    candidate_ledger = read_gzip_json_from_bytes(raw_ledger)
    candidate_result = json.loads(raw_result)
    need(
        isinstance(candidate_result, dict),
        "Round290 candidate result top-level object",
    )
    need(
        deterministic_gzip_bytes(candidate_ledger) == raw_ledger,
        "Round290 deterministic gzip byte commitment",
    )
    need(
        canonical(candidate_result) + b"\n" == raw_result,
        "Round290 canonical result bytes",
    )
    audit_candidate_ledger_object(candidate_ledger, expected_ledger)
    result_audit = audit_candidate_result_object(
        candidate_result,
        census,
        expected_ledger,
        evaluator_chain,
    )
    return candidate_ledger, candidate_result, result_audit


def resigned_row(
    row: dict[str, Any],
    mutation: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    payload = deepcopy(row)
    payload.pop("row_sha256")
    mutation(payload)
    return close_row(payload)


def recompute_ledger_commitments(ledger: dict[str, Any]) -> None:
    rows = ledger["rows"]
    ledger["row_count"] = len(rows)
    ledger["rows_sha256"] = digest(rows)
    ledger["row_ids_sha256"] = digest(
        [row["Round290_inner_support_row_id"] for row in rows]
    )
    ledger["row_hashes_sha256"] = digest(
        [row["row_sha256"] for row in rows]
    )


def reclose_result(
    result: dict[str, Any],
    ledger: dict[str, Any],
    ledger_bytes: bytes | None = None,
) -> None:
    result["inner_support_ledger"].update(
        {
            "row_count": ledger["row_count"],
            "rows_sha256": ledger["rows_sha256"],
            "row_ids_sha256": ledger["row_ids_sha256"],
            "row_hashes_sha256": ledger["row_hashes_sha256"],
            "file_sha256": hashlib.sha256(
                ledger_bytes
                if ledger_bytes is not None
                else deterministic_gzip_bytes(ledger)
            ).hexdigest(),
        }
    )
    result.pop("result_sha256", None)
    result["result_sha256"] = digest(result)


def run_targeted_attacks(
    expected_ledger: dict[str, Any],
    candidate_result: dict[str, Any],
    census: dict[str, Any],
    evaluator_chain: dict[str, Any],
    overlap_metadata: dict[str, Any],
) -> dict[str, Any]:
    """Reject re-signed forgeries against the independent reconstruction."""

    rows = expected_ledger["rows"]
    expected_by_id = {
        row["Round290_inner_support_row_id"]: row for row in rows
    }
    by_round = {
        round_number: next(
            row for row in rows if row["source_round"] == round_number
        )
        for round_number in (269, 270, 271, 272)
    }

    def accept_rebuilt_row(row: dict[str, Any]) -> None:
        validate_row_closure(row, "attacked Round290 row")
        expected = expected_by_id.get(row["Round290_inner_support_row_id"])
        need(
            expected is not None and row == expected,
            "attacked row differs from independent exact rebuild",
        )

    def changed_lower_bound(row: dict[str, Any]) -> None:
        box = row["exact_positive_volume_rational_inner_support_box"]
        lower, upper = Q(box[0]), Q(box[1])
        box[0] = str((lower + upper) / 2)

    def expected_signature_roof(row: dict[str, Any]) -> None:
        row["expected_complete_10_field_return_signature"]["roof"] += 1

    def dynamic_signature_roof(row: dict[str, Any]) -> None:
        row[
            "dynamically_recomputed_complete_10_field_return_signature"
        ]["roof"] += 1

    row_attacks: list[
        tuple[str, dict[str, Any], Callable[[dict[str, Any]], None]]
    ] = [
        ("FORGE_EXACT_BOX", by_round[269], changed_lower_bound),
        (
            "FORGE_EXACT_VOLUME",
            by_round[269],
            lambda row: row.__setitem__("exact_inner_support_volume", "1"),
        ),
        (
            "FORGE_ATOM_ENVELOPE",
            by_round[270],
            lambda row: row.__setitem__(
                "canonical_atom_frozen_support_envelope",
                row["exact_positive_volume_rational_inner_support_box"],
            ),
        ),
        (
            "FORGE_EXPECTED_SIGNATURE",
            by_round[269],
            expected_signature_roof,
        ),
        (
            "FORGE_DYNAMIC_SIGNATURE",
            by_round[270],
            dynamic_signature_roof,
        ),
        (
            "FORGE_SIGNATURE_DIGEST",
            by_round[271],
            lambda row: row.__setitem__(
                "complete_10_field_return_signature_sha256", "0" * 64
            ),
        ),
        (
            "FORGE_OFFICIAL_KEY",
            by_round[272],
            lambda row: row.__setitem__("official_key_id", "forged-key"),
        ),
        (
            "FORGE_SOURCE_CHART",
            by_round[269],
            lambda row: row.__setitem__("source_chart", "G:FORGED"),
        ),
        (
            "FORGE_OWNER_TARGET",
            by_round[270],
            lambda row: row.__setitem__("owner_target", "G[999,999]"),
        ),
        (
            "FLIP_FACTOR_SIDE_SIGN",
            by_round[269],
            lambda row: row["independent_source_signed_region_side_proof"].__setitem__(
                "HPLUS_sign",
                "STRICT_NEGATIVE"
                if row["independent_source_signed_region_side_proof"][
                    "HPLUS_sign"
                ] == "STRICT_POSITIVE"
                else "STRICT_POSITIVE",
            ),
        ),
        (
            "REMOVE_ACTIVE_SIDE_STRICTNESS",
            by_round[271],
            lambda row: row["independent_source_signed_region_side_proof"].__setitem__(
                "active_factor_or_graph_side_strict_on_whole_inner_box",
                False,
            ),
        ),
        (
            "FORGE_CATALOGUE_ORDINAL",
            by_round[270],
            lambda row: row["deterministic_inner_support_search_proof"].__setitem__(
                "selected_catalogue_ordinal_zero_based", 1330
            ),
        ),
        (
            "FORGE_CATALOGUE_FRACTIONS",
            by_round[269],
            lambda row: row["deterministic_inner_support_search_proof"].__setitem__(
                "selected_relative_center_fractions", ["1/2", "1/2", "1/2"]
            ),
        ),
        (
            "FORGE_WALL_DYADIC_DEPTH",
            by_round[271],
            lambda row: row["deterministic_inner_support_search_proof"].__setitem__(
                "largest_successful_dyadic_box_depth", 60
            ),
        ),
        (
            "REMOVE_CHART_GUARD",
            by_round[272],
            lambda row: row.__setitem__(
                "strictly_inside_true_source_chart_guard", False
            ),
        ),
        (
            "CLAIM_EXCLUDED_FACE_TOUCH",
            by_round[271],
            lambda row: row.__setitem__(
                "touches_half_open_or_excluded_face", True
            ),
        ),
        (
            "USE_POINT_WITNESS_AS_SUPPORT",
            by_round[272],
            lambda row: row.__setitem__(
                "point_witness_used_as_inner_support", True
            ),
        ),
        (
            "PROMOTE_OCCURRENCE_CREDIT",
            by_round[269],
            lambda row: row.__setitem__("formal_new_occurrence_credit", 1),
        ),
        (
            "PROMOTE_COMPONENT_CREDIT",
            by_round[270],
            lambda row: row.__setitem__("formal_component_credit", 1),
        ),
        (
            "PROMOTE_JX_JY_GLUE",
            by_round[271],
            lambda row: row.__setitem__("Jx_Jy_same_point_glue_credit", 1),
        ),
        (
            "FORGE_SOURCE_SIGNATURE_ROW_ID",
            by_round[272],
            lambda row: row.__setitem__(
                "source_signature_row_id", "round272-forged"
            ),
        ),
        (
            "FORGE_ROUND182_LEAF",
            by_round[269],
            lambda row: row.__setitem__(
                "Round182_leaf_row_id", "round182-forged"
            ),
        ),
        (
            "FORGE_ROW_ID",
            by_round[270],
            lambda row: row.__setitem__(
                "Round290_inner_support_row_id",
                "round290-isolated-inner-support:" + "0" * 64,
            ),
        ),
    ]

    rejected: list[str] = []
    for attack_id, base, mutate in row_attacks:
        attacked = resigned_row(base, mutate)
        need(attacked != base, f"effective row attack:{attack_id}")
        try:
            accept_rebuilt_row(attacked)
        except (
            VerificationError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ):
            rejected.append(attack_id)
        else:
            raise VerificationError(f"re-signed row attack accepted:{attack_id}")

    pair_left, pair_right = overlap_metadata["pair_attack_fixture"]
    attacked_pair = resigned_row(
        pair_right,
        lambda row: row.__setitem__(
            "exact_positive_volume_rational_inner_support_box",
            deepcopy(pair_left["exact_positive_volume_rational_inner_support_box"]),
        ),
    )
    need(
        positive_overlap(
            qbox(pair_left["exact_positive_volume_rational_inner_support_box"]),
            qbox(attacked_pair["exact_positive_volume_rational_inner_support_box"]),
        ),
        "pair duplicate attack is geometrically effective",
    )
    try:
        accept_rebuilt_row(attacked_pair)
    except VerificationError:
        rejected.append("INJECT_SAME_CHART_SAME_SIGNATURE_PAIR_DUPLICATE")
    else:
        raise VerificationError("pair duplicate attack accepted")

    existing_attack_base, existing_fixture = overlap_metadata[
        "existing_attack_fixture"
    ]
    attacked_existing = resigned_row(
        existing_attack_base,
        lambda row: row.__setitem__(
            "exact_positive_volume_rational_inner_support_box",
            box_text(existing_fixture[4]),
        ),
    )
    need(
        positive_overlap(
            qbox(attacked_existing[
                "exact_positive_volume_rational_inner_support_box"
            ]),
            existing_fixture[4],
        ),
        "existing-overlap attack is geometrically effective",
    )
    try:
        accept_rebuilt_row(attacked_existing)
    except VerificationError:
        rejected.append("INJECT_EXISTING_FRONTIER_POSITIVE_OVERLAP")
    else:
        raise VerificationError("existing-overlap attack accepted")

    def accept_ledger(candidate: dict[str, Any]) -> None:
        audit_candidate_ledger_object(candidate, expected_ledger)

    ledger_attacks: list[
        tuple[str, Callable[[dict[str, Any]], None]]
    ] = [
        (
            "REORDER_ROWS_AND_RECOMMIT",
            lambda ledger: ledger["rows"].__setitem__(
                slice(0, 2), list(reversed(ledger["rows"][:2]))
            ),
        ),
        (
            "DROP_ROW_AND_RECOMMIT",
            lambda ledger: ledger["rows"].pop(),
        ),
        (
            "DUPLICATE_ROW_AND_RECOMMIT",
            lambda ledger: ledger["rows"].append(ledger["rows"][-1]),
        ),
    ]
    for attack_id, mutate in ledger_attacks:
        attacked_ledger = dict(expected_ledger)
        attacked_ledger["rows"] = list(expected_ledger["rows"])
        mutate(attacked_ledger)
        recompute_ledger_commitments(attacked_ledger)
        try:
            accept_ledger(attacked_ledger)
        except (
            VerificationError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ):
            rejected.append(attack_id)
        else:
            raise VerificationError(f"recommitted ledger attack accepted:{attack_id}")

    def accept_result(candidate: dict[str, Any]) -> None:
        audit_candidate_result_object(
            candidate,
            census,
            expected_ledger,
            evaluator_chain,
        )

    result_attacks: list[
        tuple[str, Callable[[dict[str, Any]], None]]
    ] = [
        (
            "FORGE_EXISTING_OVERLAP_CENSUS",
            lambda result: result["census"].__setitem__(
                "existing_frontier_positive_volume_overlap_count", 1
            ),
        ),
        (
            "FORGE_PAIR_DUPLICATE_CENSUS",
            lambda result: result["census"].__setitem__(
                "same_chart_same_signature_positive_volume_duplicate_pair_count",
                1,
            ),
        ),
        (
            "FORGE_LEDGER_OBJECT_COMMITMENT",
            lambda result: result["inner_support_ledger"].__setitem__(
                "rows_sha256", "0" * 64
            ),
        ),
        (
            "FORGE_RESULT_STATUS",
            lambda result: result.__setitem__(
                "status", "PASS_FORGED_ROUND290"
            ),
        ),
        (
            "DISABLE_WHOLE_BOX_SIDE_CONTRACT",
            lambda result: result["support_contract"].__setitem__(
                "source_signed_region_active_factor_or_graph_side_rechecked_separately",
                False,
            ),
        ),
        (
            "PROMOTE_RESULT_OCCURRENCE_CREDIT",
            lambda result: result["strict_nonpromotion"].__setitem__(
                "formal_new_expanded_occurrence_credit", 1
            ),
        ),
        (
            "PROMOTE_RESULT_CM2",
            lambda result: result["strict_nonpromotion"].__setitem__(
                "CM2", "UNCONDITIONAL_GO"
            ),
        ),
        (
            "FORGE_PROVENANCE_RUNTIME",
            lambda result: result["provenance"].__setitem__(
                "python_version", "forged-runtime"
            ),
        ),
    ]
    for attack_id, mutate in result_attacks:
        attacked_result = deepcopy(candidate_result)
        mutate(attacked_result)
        attacked_result.pop("result_sha256", None)
        attacked_result["result_sha256"] = digest(attacked_result)
        try:
            accept_result(attacked_result)
        except (
            VerificationError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ):
            rejected.append(attack_id)
        else:
            raise VerificationError(f"reclosed result attack accepted:{attack_id}")

    # One coordinated attack is re-signed through all three layers: row,
    # ledger object/bytes, and result object.  Independent reconstruction,
    # rather than any self-reported digest, must reject it.
    attacked_chain_ledger = dict(expected_ledger)
    attacked_chain_ledger["rows"] = list(expected_ledger["rows"])
    attacked_chain_ledger["rows"][0] = resigned_row(
        attacked_chain_ledger["rows"][0],
        lambda row: row.__setitem__("exact_inner_support_volume", "1"),
    )
    recompute_ledger_commitments(attacked_chain_ledger)
    attacked_chain_bytes = deterministic_gzip_bytes(attacked_chain_ledger)
    attacked_chain_result = deepcopy(candidate_result)
    reclose_result(
        attacked_chain_result,
        attacked_chain_ledger,
        attacked_chain_bytes,
    )
    need(
        attacked_chain_result["result_sha256"]
        != candidate_result["result_sha256"],
        "coordinated attack is effective",
    )
    try:
        audit_candidate_ledger_object(
            attacked_chain_ledger,
            expected_ledger,
        )
        audit_candidate_result_object(
            attacked_chain_result,
            census,
            expected_ledger,
            evaluator_chain,
        )
    except (
        VerificationError,
        KeyError,
        IndexError,
        TypeError,
        ValueError,
    ):
        rejected.append("COORDINATED_ROW_LEDGER_GZIP_RESULT_RESIGN")
    else:
        raise VerificationError("coordinated full-chain attack accepted")

    nondeterministic = io.BytesIO()
    with gzip.GzipFile(
        filename="forged.json",
        mode="wb",
        fileobj=nondeterministic,
        mtime=1,
    ) as handle:
        handle.write(canonical(expected_ledger) + b"\n")
    forged_bytes = nondeterministic.getvalue()
    need(
        read_gzip_json_from_bytes(forged_bytes) == expected_ledger,
        "gzip-header attack preserves decoded object",
    )
    try:
        need(
            forged_bytes == deterministic_gzip_bytes(expected_ledger),
            "deterministic gzip byte equality",
        )
    except VerificationError:
        rejected.append("FORGE_GZIP_HEADER_WITH_SAME_JSON_OBJECT")
    else:
        raise VerificationError("gzip header attack accepted")

    expected_attack_count = len(row_attacks) + 2 + len(ledger_attacks) + len(
        result_attacks
    ) + 2
    need(
        len(rejected) == expected_attack_count,
        "all targeted attacks rejected",
    )
    return {
        "attack_count": expected_attack_count,
        "rejected_attack_count": len(rejected),
        "all_targeted_attacks_rejected": True,
        "row_attacks_reclosed_by_own_SHA256": True,
        "ledger_attacks_recommitted_at_object_level": True,
        "result_attacks_reclosed_at_result_SHA256_level": True,
        "coordinated_row_ledger_gzip_result_attack_reclosed": True,
        "same_JSON_nondeterministic_gzip_header_rejected": True,
        "rejected_attack_ids": rejected,
    }


def read_gzip_json_from_bytes(payload: bytes) -> dict[str, Any]:
    with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as handle:
        value = json.load(handle)
    need(isinstance(value, dict), "in-memory gzip object")
    return value


def atomic_write(path: Path, payload: bytes) -> None:
    target = path if path.is_absolute() else Path.cwd() / path
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + target.name + ".",
        dir=target.parent,
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


def verify(processes: int) -> dict[str, Any]:
    for filename, expected_hash in PRE_CANDIDATE_PINS.items():
        need(
            file_sha256(HERE / filename) == expected_hash,
            f"pre-candidate artifact pin:{filename}",
        )
    need(PRODUCER.stem not in sys.modules, "Round290 producer imported")
    evaluator_chain = load_pinned_evaluators()

    tasks, task_metadata = load_tasks_from_upstream()
    rows, row_metadata = reconstruct_inner_support_rows(tasks, processes)
    expected_ledger = ledger_object(rows)
    need(
        expected_ledger["rows_sha256"]
        == "3ab9344c1fa492d87eee4937d11659872ea848c6ff9bf02419c10ae77a0636cd"
        and expected_ledger["row_ids_sha256"]
        == "90364fbc92c8ec21100eba1d7ba5cb8ceeb616506f138dfdc21315e63709edb1"
        and expected_ledger["row_hashes_sha256"]
        == "925b4c51ea0c6ee2142a4b4fdf4c20cedb351fb24044c953fa5faf3652cefc81",
        "independent ledger object commitments",
    )
    expected_gzip = deterministic_gzip_bytes(expected_ledger)
    need(
        hashlib.sha256(expected_gzip).hexdigest()
        == CANDIDATE_PINS[LEDGER.name],
        "independently reconstructed ledger byte commitment",
    )

    existing = load_existing_occurrences()
    overlap_metadata = audit_existing_and_pairwise_overlap(rows, existing)
    census = expected_census(task_metadata, row_metadata, overlap_metadata)
    candidate_ledger, candidate_result, result_audit = read_and_audit_candidate(
        expected_ledger,
        census,
        evaluator_chain,
    )
    attacks = run_targeted_attacks(
        expected_ledger,
        candidate_result,
        census,
        evaluator_chain,
        overlap_metadata,
    )
    need(
        candidate_ledger == expected_ledger,
        "candidate ledger exact final equality",
    )
    need(PRODUCER.stem not in sys.modules, "Round290 producer imported")

    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status": (
            "PASS_INDEPENDENT_CACHELESS_ROUND290__"
            "21160_EXACT_INNER_SUPPORTS_FRESHLY_REBUILT__"
            "21160_WHOLE_BOX_SIGNATURES_AND_ACTIVE_SIDES_FRESHLY_RECHECKED__"
            "126468_EXISTING_FRONTIER_REBUILT__"
            "EXISTING_AND_PAIR_DUPLICATE_RESIDUAL_ZERO__"
            "EXACT_LEDGER_BYTES_AND_OBJECT_COMMITMENTS__ZERO_CREDIT"
        ),
        "artifact_pins": dict(sorted(ARTIFACT_PINS.items())),
        "independence_contract": {
            "Round290_producer_imported_or_executed": False,
            "Round290_producer_treated_only_as_pinned_inert_bytes": True,
            "candidate_ledger_read_only_after_complete_expected_row_reconstruction":
                True,
            "candidate_ledger_read_only_after_existing_and_pair_overlap_reconstruction":
                True,
            "candidate_result_and_ledger_bytes_unopened_before_expected_geometry_and_overlap_complete":
                True,
            "cache_or_pickle_input_used": False,
            "complete_16_module_evaluator_transitive_source_closure_pinned_before_import":
                True,
            "all_16_evaluator_modules_rejected_if_preloaded": True,
            "all_16_evaluator_modules_compiled_directly_from_pinned_source_bytes":
                True,
            "python_bytecode_cache_bypassed_for_all_evaluator_modules": True,
            "every_evaluator_module_resolved_file_and_spec_origin_rebound_to_pinned_source":
                True,
            "exact_box_arithmetic": "fractions.Fraction",
            "whole_box_interval_arithmetic": "python-flint Arb at 256 bits",
            "return_signature_and_active_side_evaluated_separately": True,
        },
        "independent_reconstruction": {
            **task_metadata,
            "strict_positive_volume_inner_support_count": len(rows),
            "exact_inner_support_rows_sha256":
                expected_ledger["rows_sha256"],
            "exact_inner_support_row_ids_sha256":
                expected_ledger["row_ids_sha256"],
            "exact_inner_support_row_hashes_sha256":
                expected_ledger["row_hashes_sha256"],
            "deterministic_inner_support_ledger_file_sha256":
                hashlib.sha256(expected_gzip).hexdigest(),
            "search_method_histogram": row_metadata["search_method_histogram"],
            "factor_model_histogram": row_metadata["factor_model_histogram"],
            "factor_catalogue_selected_ordinal_histogram_sha256":
                row_metadata["selected_ordinal_histogram_sha256"],
            "largest_successful_wall_dyadic_depth_histogram":
                row_metadata["wall_depth_histogram"],
            "fresh_whole_box_dynamic_signature_count":
                row_metadata["fresh_whole_box_dynamic_signature_count"],
            "fresh_whole_box_active_side_count":
                row_metadata["fresh_whole_box_active_side_count"],
            "fresh_strict_chart_guard_count":
                row_metadata["fresh_strict_chart_guard_count"],
            "half_open_or_excluded_face_touch_count": 0,
            "independent_search_failure_residual_count": 0,
        },
        "overlap_reconstruction": {
            "existing_occurrence_count":
                overlap_metadata["existing_occurrence_count"],
            "existing_interval_shortlist_comparison_count":
                overlap_metadata[
                    "existing_interval_shortlist_comparison_count"
                ],
            "existing_positive_volume_overlap_count":
                overlap_metadata["existing_positive_volume_overlap_count"],
            "same_chart_same_signature_group_count":
                overlap_metadata["same_chart_same_signature_group_count"],
            "pairwise_shortlist_comparison_count":
                overlap_metadata["pairwise_shortlist_comparison_count"],
            "same_chart_same_signature_positive_volume_duplicate_pair_count":
                overlap_metadata[
                    "same_chart_same_signature_positive_volume_duplicate_pair_count"
                ],
        },
        "ledger_commitment_audit": {
            "row_count": expected_ledger["row_count"],
            "rows_sha256": expected_ledger["rows_sha256"],
            "row_ids_sha256": expected_ledger["row_ids_sha256"],
            "row_hashes_sha256": expected_ledger["row_hashes_sha256"],
            "deterministic_gzip_file_sha256":
                hashlib.sha256(expected_gzip).hexdigest(),
            "candidate_object_exactly_equals_independent_reconstruction": True,
            "candidate_gzip_bytes_exactly_equal_independent_reconstruction":
                True,
            "every_row_closed_by_own_SHA256": True,
        },
        "candidate_result_audit": result_audit,
        "targeted_reclosed_attacks": attacks,
        "replay_contract": {
            "seed_argument_affects_output": False,
            "verification_output_excludes_process_count": True,
            "verification_output_excludes_current_seed": True,
            "external_PYTHONHASHSEED_replay_expected_byte_identical": True,
        },
        "dynamic_evaluator": {
            "python_flint_version": FLINT_VERSION,
            "precision_bits": ctx.prec,
            "transitive_source_module_count": len(EVALUATOR_MODULE_PINS),
            "transitive_source_file_pins":
                dict(sorted(EVALUATOR_SOURCE_PINS.items())),
            "source_only_loader_used": True,
            "preloaded_module_count": 0,
            "pinned_evaluator_chain": evaluator_chain,
        },
        "strict_nonpromotion": EXPECTED_NONPROMOTION,
        "provenance": {
            "Round290_producer_imported_or_executed": False,
            "cache_or_pickle_input_used": False,
            "candidate_ledger_used_as_search_or_geometry_oracle": False,
            "candidate_result_used_as_search_or_geometry_oracle": False,
            "Round290_inner_support_geometry_unverified_residual_count": 0,
        },
    }
    verification["verification_sha256"] = digest(verification)
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--processes",
        type=int,
        default=min(40, os.cpu_count() or 1),
    )
    parser.add_argument(
        "--seed",
        default="290071",
        help=(
            "Accepted for external cold replay; deliberately excluded from "
            "the canonical verification output."
        ),
    )
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    need(arguments.processes >= 1, "positive process count")
    del arguments.seed
    verification = verify(arguments.processes)
    atomic_write(arguments.output, canonical(verification) + b"\n")
    print(verification["status"])
    print("verification_sha256=" + verification["verification_sha256"])
    print("verification_file_sha256=" + file_sha256(arguments.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
