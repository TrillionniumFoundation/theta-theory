#!/usr/bin/env python3
"""Primary read-only replay of the Round306B0 primitive-source partition.

This is reproducibility evidence.  It proves source-set and join
exhaustion, not normalized-full-support theorems.  In particular, witness and
outer boxes remain non-formal until the appropriate R2/G2/source-geometry
equivalence kernels are independently reconstructed.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any, Iterator


D = Path(__file__).resolve().parent

B0 = D / "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz"
R1_UNION = D / "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz"
G_SHEET = D / "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz"
G_SIDE = D / "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz"
R245 = D / "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json"
R246 = D / "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json"
R247 = D / "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json"
R248 = D / "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
R266 = D / "cm2_round266_source_g_expanded_curved_face_closure_certificate.json"
R294 = D / "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz"


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def jq_rows(path: Path, expression: str) -> Iterator[dict[str, Any]]:
    gzip_process: subprocess.Popen[bytes] | None = None
    if path.suffix == ".gz":
        gzip_process = subprocess.Popen(["gzip", "-cd", str(path)], stdout=subprocess.PIPE)
        assert gzip_process.stdout is not None
        process = subprocess.Popen(
            ["jq", "-c", expression],
            stdin=gzip_process.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        gzip_process.stdout.close()
    else:
        process = subprocess.Popen(
            ["jq", "-c", expression, str(path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    assert process.stdout is not None
    for line in process.stdout:
        yield json.loads(line)
    stderr = process.stderr.read() if process.stderr is not None else ""
    jq_status = process.wait()
    gzip_status = gzip_process.wait() if gzip_process is not None else 0
    if jq_status != 0 or gzip_status != 0:
        raise RuntimeError(
            f"pipeline failed for {path.name}: gzip={gzip_status}, jq={jq_status}: {stderr.strip()}"
        )


def unique_insert(mapping: dict[str, Any], key: str, value: Any, label: str) -> None:
    if key in mapping:
        raise ValueError(f"duplicate {label}: {key}")
    mapping[key] = value


def load_virtual_sources() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    specs = (
        (R245, ".result.formal_retained_stratum_node_ledger.rows[]", "retained_stratum_node_id", "R245"),
        (R246, ".result.formal_new_whole_signature_retained_stratum_node_ledger.rows[]", "retained_stratum_node_id", "R246"),
        (R247, ".result.formal_new_crossing_and_source_seam_retained_stratum_node_ledger.rows[]", "retained_stratum_node_id", "R247"),
    )
    for path, expression, id_field, package in specs:
        for row in jq_rows(path, expression):
            unique_insert(result, row[id_field], {
                "package": package,
                "row_sha256": row["row_sha256"],
                "local_dimension": row["local_dimension"],
                "stratum_kind": row["stratum_kind"],
            }, "virtual source row")
    for row in jq_rows(R248, ".result.formal_wall_positive_volume_bulk_ledger.rows[]"):
        unique_insert(result, row["wall_bulk_node_id"], {
            "package": "R248",
            "row_sha256": row["row_sha256"],
            "local_dimension": 3,
            "stratum_kind": row["source_partition_kind"],
            "proof_kind": row["positive_volume_proof_kind"],
            "branch_label": row["branch_label"],
        }, "virtual source row")
    for row in jq_rows(R248, ".result.formal_wall_half_open_sheet_owner_ledger.rows[]"):
        unique_insert(result, row["wall_sheet_node_id"], {
            "package": "R248",
            "row_sha256": row["row_sha256"],
            "local_dimension": 2,
            "stratum_kind": row["source_partition_kind"],
        }, "virtual source row")
    return result


def load_r266() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    expanded: dict[str, Any] = {}
    valid: dict[str, Any] = {}
    component: dict[str, Any] = {}
    expression = """
      (.result.formal_post_Round266_expanded_occurrence_frontier_ledger.rows[] |
       {tag:"expanded", row:.}),
      (.result.formal_post_Round266_valid_virtual_node_frontier_ledger.rows[] |
       {tag:"valid", row:.}),
      (.result.formal_post_Round266_component_member_frontier_ledger.rows[] |
       select(.component_member_kind=="VALID_VIRTUAL_STRATUM") |
       {tag:"component", row:.})
    """
    for tagged in jq_rows(R266, expression):
        row = tagged["row"]
        if tagged["tag"] == "expanded":
            unique_insert(expanded, row["post_Round266_expanded_occurrence_frontier_row_id"], {
                "row_sha256": row["row_sha256"],
                "member_id": row["local_occurrence_row_id"],
                "occurrence_source": row["occurrence_source"],
                "source_geometry_row_id": row["source_geometry_row_id"],
                "source_geometry_row_sha256": row["source_geometry_row_sha256"],
            }, "R266 expanded row")
        elif tagged["tag"] == "valid":
            unique_insert(valid, row["valid_virtual_stratum_node_id"], {
                "row_id": row["post_Round266_valid_virtual_node_frontier_row_id"],
                "row_sha256": row["row_sha256"],
                "virtual_node_kind": row["virtual_node_kind"],
            }, "R266 valid virtual member")
        else:
            unique_insert(component, row["post_Round266_component_member_frontier_row_id"], {
                "row_sha256": row["row_sha256"],
                "member_id": row["component_member_id"],
                "source_kind": row["component_member_source_kind"],
                "frontier_row_id": row["source_Round266_frontier_row_id"],
                "frontier_row_sha256": row["source_Round266_frontier_row_sha256"],
            }, "R266 virtual component member")
    return expanded, valid, component


def load_r294(expanded: dict[str, Any]) -> tuple[dict[str, Any], Counter[str]]:
    result: dict[str, Any] = {}
    preserved_sources: Counter[str] = Counter()
    for row in jq_rows(R294, ".rows[]"):
        kind = row["registry_entry_kind"]
        family: str
        if kind == "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE":
            source = expanded.get(row["source_row_id"])
            if source is None or source["row_sha256"] != row["source_row_sha256"]:
                raise ValueError("R294 preserved source does not bind R266")
            if (
                source["member_id"] != row["registry_occurrence_id"]
                or source["source_geometry_row_id"] != row["source_geometry_row_id"]
                or source["source_geometry_row_sha256"] != row["source_geometry_row_sha256"]
            ):
                raise ValueError("R294 preserved geometry backbinding mismatch")
            family = "PRESERVED_" + source["occurrence_source"]
            preserved_sources[source["occurrence_source"]] += 1
        elif kind == "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM":
            support_kind = row["support_representation_kind"]
            if support_kind == "ROUND279_DYNAMIC_STRICT_INWARD_CORRIDOR_INNER_SUPPORT":
                family = "R288_DYNAMIC_ATOM_REQUIRES_R2_FULL_SUPPORT_UNION"
            elif support_kind == "ROUND290_ISOLATED_ATOM_RATIONAL_INNER_SUPPORT":
                family = "R288_ISOLATED_ATOM_REQUIRES_R2_FULL_SUPPORT_UNION"
            else:
                raise ValueError("unknown R288 support representation")
        elif kind == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT":
            if row["support_representation_kind"] != "EXACT_T2_P_S_CONNECTED_UNCOVERED_REFINEMENT_CELL_UNION":
                raise ValueError("unknown R292 support representation")
            family = "R292_EXACT_T2PS_REFINEMENT_CELL_UNION"
        else:
            raise ValueError("unknown R294 registry entry kind")
        unique_insert(result, row["Round294_occurrence_registry_row_id"], {
            "row_sha256": row["row_sha256"],
            "member_id": row["registry_occurrence_id"],
            "family": family,
        }, "R294 registry row")
    return result, preserved_sources


def load_graph_joins(
    virtual_sources: dict[str, Any],
) -> tuple[Counter[str], set[str], dict[str, str], dict[str, str]]:
    side_multiplicity: Counter[str] = Counter()
    side_b0_rows: dict[str, str] = {}
    side_join_family: Counter[str] = Counter()
    for row in jq_rows(G_SIDE, ".graph_side_join_rows[]"):
        member = row["side_member_id"]
        source = virtual_sources.get(member)
        if source is None or source["row_sha256"] != row["side_source_row_sha256"]:
            raise ValueError("G side source row mismatch")
        side_multiplicity[member] += 1
        b0_row_id = row["Round306B0_member_support_source_row_id"]
        if b0_row_id in side_b0_rows and side_b0_rows[b0_row_id] != member:
            raise ValueError("G2b B0 row binds multiple members")
        side_b0_rows[b0_row_id] = member
        side_join_family[row["graph_family"]] += 1
    if side_join_family != Counter({
        "R235_SINGLE_ENDPOINT_GRAPH": 76_256,
        "R236_DOUBLE_ENDPOINT_GRAPH": 64,
        "R242_UNIQUE_TRANSITION_GRAPH": 528,
    }):
        raise ValueError("G2b family census mismatch")

    sheet_members: set[str] = set()
    sheet_b0_rows: dict[str, str] = {}
    for row in jq_rows(G_SHEET, ".graph_sheet_join_rows[]"):
        member = row["sheet_member_id"]
        source = virtual_sources.get(member)
        if source is None or source["row_sha256"] != row["sheet_source_row_sha256"]:
            raise ValueError("G sheet source row mismatch")
        if member in sheet_members:
            raise ValueError("duplicate G sheet member")
        sheet_members.add(member)
        sheet_b0_rows[row["Round306B0_member_support_source_row_id"]] = member
    return side_multiplicity, sheet_members, side_b0_rows, sheet_b0_rows


def load_r1_unions() -> tuple[dict[str, str], Counter[int]]:
    member_to_b0_row: dict[str, str] = {}
    multiplicity: Counter[int] = Counter()
    for row in jq_rows(R1_UNION, ".member_union_rows[]"):
        member = row["member_id"]
        unique_insert(
            member_to_b0_row,
            member,
            row["Round306B0_member_source_row_id"],
            "R2 member union",
        )
        multiplicity[row["predicate_source_cell_multiplicity"]] += 1
    return member_to_b0_row, multiplicity

def main() -> None:
    virtual_sources = load_virtual_sources()
    expanded, valid_virtual, virtual_components = load_r266()
    registry, preserved_sources = load_r294(expanded)
    registry_member_family = {
        value["member_id"]: value["family"] for value in registry.values()
    }
    if len(registry_member_family) != len(registry):
        raise ValueError("duplicate R294 member identity")
    side_multiplicity, sheet_members, side_b0_rows, sheet_b0_rows = load_graph_joins(
        virtual_sources
    )
    r2_members, r2_multiplicity = load_r1_unions()

    counts: Counter[str] = Counter()
    b0_member_ids: set[str] = set()
    b0_occurrence_ids: set[str] = set()
    b0_virtual_ids: set[str] = set()
    b0_row_to_member: dict[str, str] = {}
    partition_commitment = hashlib.sha256()
    for row in jq_rows(B0, ".member_support_source_rows[]"):
        member = row["member_id"]
        if member in b0_member_ids:
            raise ValueError("duplicate B0 member")
        b0_member_ids.add(member)
        b0_row_to_member[row["Round306B0_member_support_source_row_id"]] = member
        if row["primary_source_package"] == "R294":
            source = registry.get(row["primary_source_row_id"])
            if source is None or source["row_sha256"] != row["primary_source_row_sha256"]:
                raise ValueError("B0/R294 primary binding mismatch")
            if source["member_id"] != member:
                raise ValueError("B0/R294 member mismatch")
            family = source["family"]
            b0_occurrence_ids.add(member)
        elif row["primary_source_package"] == "R266":
            source = virtual_components.get(row["primary_source_row_id"])
            if source is None or source["row_sha256"] != row["primary_source_row_sha256"]:
                raise ValueError("B0/R266 primary binding mismatch")
            if source["member_id"] != member or member not in valid_virtual:
                raise ValueError("B0/R266 virtual member mismatch")
            valid_source = valid_virtual[member]
            if (
                source["frontier_row_id"] != valid_source["row_id"]
                or source["frontier_row_sha256"] != valid_source["row_sha256"]
            ):
                raise ValueError("R266 component/valid-frontier backbinding mismatch")
            upstream = virtual_sources.get(member)
            if upstream is None:
                raise ValueError("missing virtual primitive source row")
            package = upstream["package"]
            dimension = upstream["local_dimension"]
            if row["inherited_virtual_source_package"] is not None:
                if (
                    package != row["inherited_virtual_source_package"]
                    or member != row["inherited_virtual_source_row_id"]
                    or upstream["row_sha256"] != row["inherited_virtual_source_row_sha256"]
                ):
                    raise ValueError("B0 inherited virtual source mismatch")
            if dimension == 2:
                if member not in sheet_members:
                    raise ValueError("virtual sheet missing G2a join")
                family = f"{package}_GRAPH_SHEET_REQUIRES_G2A_SUPPORT"
            elif member in side_multiplicity:
                family = f"{package}_GRAPH_SIDE_MEMBER_REQUIRES_G2B_SUPPORT"
            else:
                family = f"{package}_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION"
            b0_virtual_ids.add(member)
        else:
            raise ValueError("unknown B0 primary source package")
        counts[family] += 1
        partition_commitment.update(canonical([member, family]) + b"\n")

    if b0_occurrence_ids != {value["member_id"] for value in registry.values()}:
        raise ValueError("B0/R294 occurrence set mismatch")
    if b0_virtual_ids != set(valid_virtual):
        raise ValueError("B0/R266 virtual set mismatch")
    if set(r2_members) != {
        member for member, family in registry_member_family.items()
        if family.startswith("R288_")
    }:
        raise ValueError("R2/B0 R288 member set mismatch")
    for b0_row_id, member in side_b0_rows.items():
        if b0_row_to_member.get(b0_row_id) != member:
            raise ValueError("G2b/B0 row backbinding mismatch")
    for b0_row_id, member in sheet_b0_rows.items():
        if b0_row_to_member.get(b0_row_id) != member:
            raise ValueError("G2a/B0 row backbinding mismatch")
    for member, b0_row_id in r2_members.items():
        if b0_row_to_member.get(b0_row_id) != member:
            raise ValueError("R2/B0 row backbinding mismatch")

    side_histogram = Counter(side_multiplicity.values())
    r248_final = {
        member for member, row in valid_virtual.items()
        if row["virtual_node_kind"].startswith("ROUND248_")
    }
    r248_raw = {
        member for member, row in virtual_sources.items() if row["package"] == "R248"
    }
    excluded_r248 = r248_raw - r248_final
    if len(excluded_r248) != 400:
        raise ValueError("R248/R264 exclusion count mismatch")

    expected_counts = Counter({
        "PRESERVED_ROUND174_RESOLVED": 72_500,
        "PRESERVED_ROUND179_RESOLVED": 17_192,
        "PRESERVED_ROUND204_REGION": 736,
        "PRESERVED_ROUND208_REGION": 36_040,
        "R288_DYNAMIC_ATOM_REQUIRES_R2_FULL_SUPPORT_UNION": 274_176,
        "R288_ISOLATED_ATOM_REQUIRES_R2_FULL_SUPPORT_UNION": 21_160,
        "R292_EXACT_T2PS_REFINEMENT_CELL_UNION": 9_404,
        "R245_GRAPH_SHEET_REQUIRES_G2A_SUPPORT": 264,
        "R248_GRAPH_SHEET_REQUIRES_G2A_SUPPORT": 38_360,
        "R245_GRAPH_SIDE_MEMBER_REQUIRES_G2B_SUPPORT": 528,
        "R248_GRAPH_SIDE_MEMBER_REQUIRES_G2B_SUPPORT": 76_304,
        "R245_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION": 2_872,
        "R246_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION": 2_220,
        "R247_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION": 504,
        "R248_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION": 12_232,
    })
    if counts != expected_counts:
        raise ValueError("primitive partition mismatch: " + repr(counts - expected_counts))
    if r2_multiplicity != Counter({1: 295_332, 2: 4}):
        raise ValueError("R2 multiplicity histogram mismatch")
    if side_histogram != Counter({1: 76_816, 2: 16}):
        raise ValueError("G2b member multiplicity histogram mismatch")
    if len(sheet_members) != 38_624 or len(side_multiplicity) != 76_832:
        raise ValueError("G member exhaustion mismatch")
    if sum(counts.values()) != 564_492:
        raise ValueError("B0 member total mismatch")

    groups = {
        "direct_preserved_source_geometry": sum(
            value for key, value in counts.items() if key.startswith("PRESERVED_")
        ),
        "R2_predicate_union_members": sum(
            value for key, value in counts.items() if key.startswith("R288_")
        ),
        "R292_transformed_cell_union_members": counts[
            "R292_EXACT_T2PS_REFINEMENT_CELL_UNION"
        ],
        "G2a_graph_sheet_members": len(sheet_members),
        "G2b_graph_side_members": len(side_multiplicity),
        "non_graph_virtual_bulk_members": sum(
            value for key, value in counts.items() if "NON_GRAPH_BULK" in key
        ),
    }
    result = {
        "schema": "cm2.round306b1af2.source-g-primitive-support-source-partition.replay-result.v1",
        "input_pin_set_sha256": "5a42c479d0785794e67d6fa1d7dbeffad8d0fba41a7cbc22faf889ec02843966",
        "table_commitments_sha256": "38bbb15e0d6885f3cb9a681f1b625adcf8dba608e6722edf4fea09220640dee8",
        "table_locators_sha256": "8605cdcd72980733925931b9fa6904ac5e91a3ef98c755dae4494c5c50660de6",
        "partition_algorithm_sha256": "ad8cbb6907a4f6ee19e70c983f0df9cac83f0f6d54cb1b41d8e9868b2782acee",
        "status": "PASS_EXACT_564492_MEMBER_SOURCE_PARTITION__FORMAL_FULL_SUPPORT_NO_GO",
        "member_count": len(b0_member_ids),
        "fine_partition": [
            {"family": key, "member_count": counts[key]}
            for key in sorted(counts)
        ],
        "coarse_partition": groups,
        "G2b": {
            "reference_count": sum(side_multiplicity.values()),
            "distinct_member_count": len(side_multiplicity),
            "member_reference_multiplicity_histogram": {
                str(key): side_histogram[key] for key in sorted(side_histogram)
            },
        },
        "R2": {
            "predicate_cell_reference_count": sum(
                multiplicity * count
                for multiplicity, count in r2_multiplicity.items()
            ),
            "distinct_member_count": len(r2_members),
            "member_cell_multiplicity_histogram": {
                str(key): r2_multiplicity[key] for key in sorted(r2_multiplicity)
            },
        },
        "partition_stream": {
            "order": "ROUND306B0_MEMBER_LEDGER_ORDER",
            "wire": "canonical_json([member_id,family])+LF",
            "sha256": partition_commitment.hexdigest(),
        },
        "R248_raw_virtual_count": len(r248_raw),
        "R248_final_virtual_count": len(r248_final),
        "R248_raw_minus_final_virtual_count": len(excluded_r248),
        "formal_credit": 0,
    }
    print(canonical(result).decode("ascii"))


if __name__ == "__main__":
    main()
