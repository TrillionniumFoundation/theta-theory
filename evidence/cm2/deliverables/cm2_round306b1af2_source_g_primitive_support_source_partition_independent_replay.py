#!/usr/bin/env python3
"""Independent, read-only replay of the Round306B1A primitive-source partition.

This program does not import or execute the primary probe, the B1AF1/F2
contract, or any producer.  It binds the exact source bytes, reconstructs the
member-to-source joins directly from the frozen ledgers, and emits one
canonical JSON result on stdout.  It grants no normalized-full-support or
formal theorem credit.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any, Iterator


WORKSPACE = Path(__file__).resolve().parents[1]
DELIVERABLES = WORKSPACE / "deliverables"


# Exact bytes consumed by this replay.  Size and SHA-256 are checked before
# any semantic row is admitted.
FILE_PINS: dict[str, tuple[int, str]] = {
    "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json": (
        20_683_081,
        "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1",
    ),
    "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json": (
        18_283_721,
        "a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9",
    ),
    "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json": (
        13_400_149,
        "72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7",
    ),
    "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json": (
        205_148_977,
        "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    ),
    "cm2_round266_source_g_expanded_curved_face_closure_certificate.json": (
        934_776_249,
        "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf",
    ),
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz": (
        262_951_902,
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    ),
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz": (
        162_499_140,
        "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af",
    ),
    "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz": (
        123_019_951,
        "4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7",
    ),
    "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz": (
        13_922_080,
        "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3",
    ),
    "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz": (
        25_932_945,
        "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1",
    ),
}


B0 = "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz"
R294 = "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz"
R266 = "cm2_round266_source_g_expanded_curved_face_closure_certificate.json"
R245 = "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json"
R246 = "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json"
R247 = "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json"
R248 = "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
R2_MEMBER = "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz"
G2A = "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz"
G2B = "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz"


EXPECTED_FINE = {
    "PRESERVED_ROUND174_RESOLVED": 72_500,
    "PRESERVED_ROUND179_RESOLVED": 17_192,
    "PRESERVED_ROUND204_REGION": 736,
    "PRESERVED_ROUND208_REGION": 36_040,
    "R245_GRAPH_SHEET_REQUIRES_G2A_SUPPORT": 264,
    "R245_GRAPH_SIDE_MEMBER_REQUIRES_G2B_SUPPORT": 528,
    "R245_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION": 2_872,
    "R246_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION": 2_220,
    "R247_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION": 504,
    "R248_GRAPH_SHEET_REQUIRES_G2A_SUPPORT": 38_360,
    "R248_GRAPH_SIDE_MEMBER_REQUIRES_G2B_SUPPORT": 76_304,
    "R248_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION": 12_232,
    "R288_DYNAMIC_ATOM_REQUIRES_R2_FULL_SUPPORT_UNION": 274_176,
    "R288_ISOLATED_ATOM_REQUIRES_R2_FULL_SUPPORT_UNION": 21_160,
    "R292_EXACT_T2PS_REFINEMENT_CELL_UNION": 9_404,
}


EXPECTED_RESULT_SHA256 = "2d311625d3aa2170aa508ff4a20259c31ac91ddc3c700d7c5ba95c11276205ba"


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_source_files() -> None:
    for name, (expected_size, expected_sha256) in FILE_PINS.items():
        path = DELIVERABLES / name
        metadata = os.lstat(path)
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError(f"source is not a regular file: {name}")
        if metadata.st_size != expected_size:
            raise ValueError(f"source size mismatch: {name}")
        if sha256_file(path) != expected_sha256:
            raise ValueError(f"source SHA-256 mismatch: {name}")


def rows(name: str, expression: str) -> Iterator[dict[str, Any]]:
    path = DELIVERABLES / name
    gzip_process: subprocess.Popen[bytes] | None = None
    if name.endswith(".gz"):
        gzip_process = subprocess.Popen(
            ["gzip", "-cd", str(path)], stdout=subprocess.PIPE
        )
        assert gzip_process.stdout is not None
        jq_process = subprocess.Popen(
            ["jq", "-c", expression],
            stdin=gzip_process.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        gzip_process.stdout.close()
    else:
        jq_process = subprocess.Popen(
            ["jq", "-c", expression, str(path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    assert jq_process.stdout is not None
    for line in jq_process.stdout:
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"non-object row from {name}")
        yield value
    stderr = jq_process.stderr.read() if jq_process.stderr is not None else ""
    jq_status = jq_process.wait()
    gzip_status = gzip_process.wait() if gzip_process is not None else 0
    if jq_status != 0 or gzip_status != 0:
        raise RuntimeError(
            f"row pipeline failed: {name}: gzip={gzip_status}, "
            f"jq={jq_status}: {stderr.strip()}"
        )


def put_unique(mapping: dict[str, Any], key: str, value: Any, label: str) -> None:
    if key in mapping:
        raise ValueError(f"duplicate {label}: {key}")
    mapping[key] = value


def virtual_primitive_rows() -> dict[str, tuple[str, str, int]]:
    result: dict[str, tuple[str, str, int]] = {}
    for name, expression, package in (
        (R245, ".result.formal_retained_stratum_node_ledger.rows[]", "R245"),
        (
            R246,
            ".result.formal_new_whole_signature_retained_stratum_node_ledger.rows[]",
            "R246",
        ),
        (
            R247,
            ".result.formal_new_crossing_and_source_seam_retained_stratum_node_ledger.rows[]",
            "R247",
        ),
    ):
        for row in rows(name, expression):
            put_unique(
                result,
                row["retained_stratum_node_id"],
                (package, row["row_sha256"], row["local_dimension"]),
                "virtual primitive",
            )
    for expression, id_field, dimension in (
        (
            ".result.formal_wall_positive_volume_bulk_ledger.rows[]",
            "wall_bulk_node_id",
            3,
        ),
        (
            ".result.formal_wall_half_open_sheet_owner_ledger.rows[]",
            "wall_sheet_node_id",
            2,
        ),
    ):
        for row in rows(R248, expression):
            put_unique(
                result,
                row[id_field],
                ("R248", row["row_sha256"], dimension),
                "virtual primitive",
            )
    return result


def r266_indexes() -> tuple[dict[str, tuple[str, str, str, str, str]], dict[str, tuple[str, str, str]], dict[str, tuple[str, str, str, str]]]:
    expanded: dict[str, tuple[str, str, str, str, str]] = {}
    valid: dict[str, tuple[str, str, str]] = {}
    component: dict[str, tuple[str, str, str, str]] = {}
    expression = """
      (.result.formal_post_Round266_expanded_occurrence_frontier_ledger.rows[] |
       {kind:"expanded",value:.}),
      (.result.formal_post_Round266_valid_virtual_node_frontier_ledger.rows[] |
       {kind:"valid",value:.}),
      (.result.formal_post_Round266_component_member_frontier_ledger.rows[] |
       select(.component_member_kind=="VALID_VIRTUAL_STRATUM") |
       {kind:"component",value:.})
    """
    for tagged in rows(R266, expression):
        row = tagged["value"]
        if tagged["kind"] == "expanded":
            put_unique(
                expanded,
                row["post_Round266_expanded_occurrence_frontier_row_id"],
                (
                    row["row_sha256"],
                    row["local_occurrence_row_id"],
                    row["occurrence_source"],
                    row["source_geometry_row_id"],
                    row["source_geometry_row_sha256"],
                ),
                "R266 expanded row",
            )
        elif tagged["kind"] == "valid":
            put_unique(
                valid,
                row["valid_virtual_stratum_node_id"],
                (
                    row["post_Round266_valid_virtual_node_frontier_row_id"],
                    row["row_sha256"],
                    row["virtual_node_kind"],
                ),
                "R266 valid virtual member",
            )
        else:
            put_unique(
                component,
                row["post_Round266_component_member_frontier_row_id"],
                (
                    row["row_sha256"],
                    row["component_member_id"],
                    row["source_Round266_frontier_row_id"],
                    row["source_Round266_frontier_row_sha256"],
                ),
                "R266 virtual component row",
            )
    if (len(expanded), len(valid), len(component)) != (126_468, 133_284, 133_284):
        raise ValueError("R266 source census mismatch")
    return expanded, valid, component


def registry_index(
    expanded: dict[str, tuple[str, str, str, str, str]],
) -> dict[str, tuple[str, str, str]]:
    result: dict[str, tuple[str, str, str]] = {}
    for row in rows(R294, ".rows[]"):
        kind = row["registry_entry_kind"]
        if kind == "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE":
            source = expanded.get(row["source_row_id"])
            if source is None:
                raise ValueError("R294 preserved source is absent from R266")
            source_sha, member, source_family, geometry_id, geometry_sha = source
            if (
                source_sha != row["source_row_sha256"]
                or member != row["registry_occurrence_id"]
                or geometry_id != row["source_geometry_row_id"]
                or geometry_sha != row["source_geometry_row_sha256"]
            ):
                raise ValueError("R294/R266 preserved backbinding mismatch")
            family = "PRESERVED_" + source_family
        elif kind == "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM":
            representation = row["support_representation_kind"]
            if representation == "ROUND279_DYNAMIC_STRICT_INWARD_CORRIDOR_INNER_SUPPORT":
                family = "R288_DYNAMIC_ATOM_REQUIRES_R2_FULL_SUPPORT_UNION"
            elif representation == "ROUND290_ISOLATED_ATOM_RATIONAL_INNER_SUPPORT":
                family = "R288_ISOLATED_ATOM_REQUIRES_R2_FULL_SUPPORT_UNION"
            else:
                raise ValueError("unknown R288 representation")
        elif kind == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT":
            if row["support_representation_kind"] != "EXACT_T2_P_S_CONNECTED_UNCOVERED_REFINEMENT_CELL_UNION":
                raise ValueError("unknown R292 representation")
            family = "R292_EXACT_T2PS_REFINEMENT_CELL_UNION"
        else:
            raise ValueError("unknown R294 registry kind")
        put_unique(
            result,
            row["Round294_occurrence_registry_row_id"],
            (row["row_sha256"], row["registry_occurrence_id"], family),
            "R294 registry row",
        )
    if len(result) != 431_208:
        raise ValueError("R294 registry census mismatch")
    return result


def graph_indexes(
    primitives: dict[str, tuple[str, str, int]],
) -> tuple[Counter[str], set[str], dict[str, str], dict[str, str]]:
    side_multiplicity: Counter[str] = Counter()
    side_b0_rows: dict[str, str] = {}
    side_families: Counter[str] = Counter()
    for row in rows(G2B, ".graph_side_join_rows[]"):
        member = row["side_member_id"]
        source = primitives.get(member)
        if source is None or source[1] != row["side_source_row_sha256"]:
            raise ValueError("G2b/source-row mismatch")
        side_multiplicity[member] += 1
        b0_row_id = row["Round306B0_member_support_source_row_id"]
        prior = side_b0_rows.setdefault(b0_row_id, member)
        if prior != member:
            raise ValueError("G2b B0 row binds different members")
        side_families[row["graph_family"]] += 1
    if side_families != Counter(
        {
            "R235_SINGLE_ENDPOINT_GRAPH": 76_256,
            "R236_DOUBLE_ENDPOINT_GRAPH": 64,
            "R242_UNIQUE_TRANSITION_GRAPH": 528,
        }
    ):
        raise ValueError("G2b graph-family census mismatch")

    sheet_members: set[str] = set()
    sheet_b0_rows: dict[str, str] = {}
    for row in rows(G2A, ".graph_sheet_join_rows[]"):
        member = row["sheet_member_id"]
        source = primitives.get(member)
        if source is None or source[1] != row["sheet_source_row_sha256"]:
            raise ValueError("G2a/source-row mismatch")
        if member in sheet_members:
            raise ValueError("duplicate G2a member")
        sheet_members.add(member)
        b0_row_id = row["Round306B0_member_support_source_row_id"]
        if b0_row_id in sheet_b0_rows:
            raise ValueError("duplicate G2a B0 row")
        sheet_b0_rows[b0_row_id] = member
    return side_multiplicity, sheet_members, side_b0_rows, sheet_b0_rows


def r2_index() -> tuple[dict[str, str], Counter[int]]:
    members: dict[str, str] = {}
    histogram: Counter[int] = Counter()
    for row in rows(R2_MEMBER, ".member_union_rows[]"):
        put_unique(
            members,
            row["member_id"],
            row["Round306B0_member_source_row_id"],
            "R2 member union",
        )
        histogram[row["predicate_source_cell_multiplicity"]] += 1
    return members, histogram


def replay() -> dict[str, Any]:
    verify_source_files()
    primitives = virtual_primitive_rows()
    expanded, valid_virtual, components = r266_indexes()
    registry = registry_index(expanded)
    side_multiplicity, sheets, side_b0_rows, sheet_b0_rows = graph_indexes(primitives)
    r2_members, r2_histogram = r2_index()

    registry_members = {value[1]: value[2] for value in registry.values()}
    if len(registry_members) != len(registry):
        raise ValueError("duplicate R294 member identity")

    member_ids: set[str] = set()
    occurrence_members: set[str] = set()
    virtual_members: set[str] = set()
    b0_row_to_member: dict[str, str] = {}
    fine: Counter[str] = Counter()
    stream_digest = hashlib.sha256()

    for row in rows(B0, ".member_support_source_rows[]"):
        member = row["member_id"]
        if member in member_ids:
            raise ValueError("duplicate B0 member")
        member_ids.add(member)
        b0_row_id = row["Round306B0_member_support_source_row_id"]
        if b0_row_id in b0_row_to_member:
            raise ValueError("duplicate B0 row ID")
        b0_row_to_member[b0_row_id] = member

        if row["primary_source_package"] == "R294":
            source = registry.get(row["primary_source_row_id"])
            if (
                source is None
                or source[0] != row["primary_source_row_sha256"]
                or source[1] != member
            ):
                raise ValueError("B0/R294 binding mismatch")
            family = source[2]
            occurrence_members.add(member)
        elif row["primary_source_package"] == "R266":
            component = components.get(row["primary_source_row_id"])
            frontier = valid_virtual.get(member)
            if (
                component is None
                or frontier is None
                or component[0] != row["primary_source_row_sha256"]
                or component[1] != member
                or component[2] != frontier[0]
                or component[3] != frontier[1]
            ):
                raise ValueError("B0/R266 binding mismatch")
            primitive = primitives.get(member)
            if primitive is None:
                raise ValueError("missing virtual primitive source")
            package, primitive_sha, dimension = primitive
            if row["inherited_virtual_source_package"] is not None and (
                row["inherited_virtual_source_package"] != package
                or row["inherited_virtual_source_row_id"] != member
                or row["inherited_virtual_source_row_sha256"] != primitive_sha
            ):
                raise ValueError("B0/inherited-virtual binding mismatch")
            if dimension == 2:
                if member not in sheets:
                    raise ValueError("sheet member lacks G2a join")
                family = package + "_GRAPH_SHEET_REQUIRES_G2A_SUPPORT"
            elif member in side_multiplicity:
                family = package + "_GRAPH_SIDE_MEMBER_REQUIRES_G2B_SUPPORT"
            else:
                family = package + "_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION"
            virtual_members.add(member)
        else:
            raise ValueError("unknown B0 primary source package")

        fine[family] += 1
        stream_digest.update(canonical([member, family]) + b"\n")

    if occurrence_members != set(registry_members):
        raise ValueError("B0/R294 member-set mismatch")
    if virtual_members != set(valid_virtual):
        raise ValueError("B0/R266 virtual-member-set mismatch")
    expected_r2_members = {
        member for member, family in registry_members.items() if family.startswith("R288_")
    }
    if set(r2_members) != expected_r2_members:
        raise ValueError("R2/R288 member-set mismatch")
    for mapping, label in (
        (side_b0_rows, "G2b"),
        (sheet_b0_rows, "G2a"),
    ):
        for b0_row_id, member in mapping.items():
            if b0_row_to_member.get(b0_row_id) != member:
                raise ValueError(f"{label}/B0 row backbinding mismatch")
    for member, b0_row_id in r2_members.items():
        if b0_row_to_member.get(b0_row_id) != member:
            raise ValueError("R2/B0 row backbinding mismatch")

    if fine != Counter(EXPECTED_FINE):
        raise ValueError(f"fine partition mismatch: {fine}")
    if r2_histogram != Counter({1: 295_332, 2: 4}):
        raise ValueError("R2 multiplicity mismatch")
    side_histogram = Counter(side_multiplicity.values())
    if side_histogram != Counter({1: 76_816, 2: 16}):
        raise ValueError("G2b multiplicity mismatch")
    if len(sheets) != 38_624 or len(side_multiplicity) != 76_832:
        raise ValueError("G2 member census mismatch")
    if len(member_ids) != 564_492:
        raise ValueError("B0 member census mismatch")

    raw_r248 = {member for member, value in primitives.items() if value[0] == "R248"}
    final_r248 = {
        member for member, value in valid_virtual.items() if value[2].startswith("ROUND248_")
    }
    if len(raw_r248 - final_r248) != 400:
        raise ValueError("R248 raw/final virtual difference mismatch")

    coarse = {
        "direct_preserved_source_geometry": sum(
            count for family, count in fine.items() if family.startswith("PRESERVED_")
        ),
        "G2a_graph_sheet_members": len(sheets),
        "G2b_graph_side_members": len(side_multiplicity),
        "non_graph_virtual_bulk_members": sum(
            count for family, count in fine.items() if "NON_GRAPH_BULK" in family
        ),
        "R2_predicate_union_members": sum(
            count for family, count in fine.items() if family.startswith("R288_")
        ),
        "R292_transformed_cell_union_members": fine[
            "R292_EXACT_T2PS_REFINEMENT_CELL_UNION"
        ],
    }
    if sum(coarse.values()) != 564_492:
        raise ValueError("coarse partition mismatch")

    return {
        "schema": "cm2.round306b1af2.source-g-primitive-support-source-partition.replay-result.v1",
        "input_pin_set_sha256": "5a42c479d0785794e67d6fa1d7dbeffad8d0fba41a7cbc22faf889ec02843966",
        "table_commitments_sha256": "38bbb15e0d6885f3cb9a681f1b625adcf8dba608e6722edf4fea09220640dee8",
        "table_locators_sha256": "8605cdcd72980733925931b9fa6904ac5e91a3ef98c755dae4494c5c50660de6",
        "partition_algorithm_sha256": "ad8cbb6907a4f6ee19e70c983f0df9cac83f0f6d54cb1b41d8e9868b2782acee",
        "status": "PASS_EXACT_564492_MEMBER_SOURCE_PARTITION__FORMAL_FULL_SUPPORT_NO_GO",
        "member_count": 564_492,
        "fine_partition": [
            {"family": family, "member_count": fine[family]}
            for family in sorted(fine)
        ],
        "coarse_partition": coarse,
        "G2b": {
            "reference_count": sum(side_multiplicity.values()),
            "distinct_member_count": len(side_multiplicity),
            "member_reference_multiplicity_histogram": {
                str(key): side_histogram[key] for key in sorted(side_histogram)
            },
        },
        "R2": {
            "predicate_cell_reference_count": sum(
                multiplicity * count for multiplicity, count in r2_histogram.items()
            ),
            "distinct_member_count": len(r2_members),
            "member_cell_multiplicity_histogram": {
                str(key): r2_histogram[key] for key in sorted(r2_histogram)
            },
        },
        "partition_stream": {
            "order": "ROUND306B0_MEMBER_LEDGER_ORDER",
            "wire": "canonical_json([member_id,family])+LF",
            "sha256": stream_digest.hexdigest(),
        },
        "R248_raw_virtual_count": len(raw_r248),
        "R248_final_virtual_count": len(final_r248),
        "R248_raw_minus_final_virtual_count": len(raw_r248 - final_r248),
        "formal_credit": 0,
    }


def main() -> None:
    if len(sys.argv) != 1:
        raise SystemExit("usage: independent_replay.py")
    result = replay()
    wire = canonical(result)
    result_sha256 = hashlib.sha256(wire).hexdigest()
    if result_sha256 != EXPECTED_RESULT_SHA256:
        raise ValueError(
            f"independent result SHA-256 mismatch: {result_sha256}"
        )
    sys.stdout.buffer.write(wire + b"\n")


if __name__ == "__main__":
    main()
