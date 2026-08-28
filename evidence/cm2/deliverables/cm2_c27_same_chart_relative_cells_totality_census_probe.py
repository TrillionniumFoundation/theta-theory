#!/usr/bin/env python3
"""Fresh, C27-independent census for SAME_CHART_RELATIVE_CELLS.

The probe constructs the complete positive-volume primitive cell universe from
the current typed support kernels, binds every owner to C15/C25, audits C26
feature coverage, and serializes exact closure-face descriptors.  It is a
fail-closed diagnostic: a half-open box without an explicit endpoint ownership
vector is never silently treated as open or closed.

Round306C27, its FAMILIES table, and every historical edge ledger are forbidden
inputs and are not opened by this program.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_c27_same_chart_relative_cells_totality_census"
LEDGER = PREFIX + "_atom_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"

FILES = {
    "C15": (
        "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz",
        "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    ),
    "C25": (
        "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz",
        "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    ),
    "C26": (
        "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz",
        "fc6d1a31e9e7c476bde73336c18d7ad4fb92deed71c3f7b7c58638c0ffc8e88e",
    ),
    "C19A": (
        "cm2_round306c19a_source_g_5596_legacy_nongraph_exact_box_support_kernel_ledger.jsonl.gz",
        "9da9f54fc21ae59be3e9ea0ec3eb636f37c1445ecf759dbe6e2eea358cb262b3",
    ),
    "C19B": (
        "cm2_round306c19b_source_g_12232_r248_exact_positive_box_support_kernel_ledger.jsonl.gz",
        "ee23ebba0e90728ad7b16bccd34d90ba0c2ce701db240c63ba50cbc04e896798",
    ),
    "C19C": (
        "cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel_ledger.jsonl.gz",
        "1f0f3f89cac5b10881b4b31a56b86d168ef901ca29bda6ad9eda87fc5f48ff84",
    ),
    "C20A": (
        "cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz",
        "bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922",
    ),
    "C22A": (
        "cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_ledger.jsonl.gz",
        "e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb",
    ),
    "C23A": (
        "cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_ledger.jsonl.gz",
        "230d8081c31c200e1adc1d74f57724b4767380fcaa0ab09c00bca9d20444c528",
    ),
    "R179": (
        "cm2_round179_source_g_residual_tube_arrangement_rows.json",
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    ),
    "R234": (
        "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json",
        "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
    ),
    "R236": (
        "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json",
        "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
    ),
    "C5": (
        "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz",
        "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333",
    ),
}

EXPECTED_SOURCE_ROWS = {
    "C19A": 5_596,
    "C19B": 12_232,
    "C19C": 33_344,
    "C20A": 126_468,
    "C22A": 295_340,
    "C23A": 10_252,
}
EXPECTED_KERNEL_BY_SOURCE = {
    "C19A": "C19A",
    "C19B": "C19B",
    "C19C": "C19C",
    "C20A": "C20A",
    "C22A": "C22B",
    "C23A": "C23B",
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def closed_rows(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for line in stream:
            need(line.endswith(b"\n"), "jsonl newline:" + path.name)
            raw = line[:-1]
            row = json.loads(raw)
            need(canonical(row) == raw, "jsonl canonical:" + path.name)
            body = dict(row)
            need(body.pop("row_sha256", None) == object_sha(body),
                 "row closure:" + path.name)
            yield row


def qwire(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def rational_endpoint(value: str) -> dict[str, Any]:
    return {"kind": "Q", "value": qwire(Fraction(value))}


def sqrt_endpoint(value: str, sign: int) -> dict[str, Any]:
    q = Fraction(value)
    need(q >= 0 and sign in {-1, 1}, "sqrt endpoint domain")
    rn, rd = math.isqrt(q.numerator), math.isqrt(q.denominator)
    if rn * rn == q.numerator and rd * rd == q.denominator:
        return rational_endpoint(qwire(Fraction(sign * rn, rd)))
    return {"kind": "SIGNED_SQRT_Q", "radicand": qwire(q), "sign": sign}


def physical_bounds(source: str, support: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    raw = support["bounds"]
    need(type(raw) is list and len(raw) == 6, "six bounds:" + source)
    if source != "C23A":
        return [rational_endpoint(value) for value in raw], ["t", "p", "s"]
    sign = support["physical_t_sign"]
    need(sign in {-1, 1}, "C23A physical branch sign")
    if sign == 1:
        t0, t1 = sqrt_endpoint(raw[0], 1), sqrt_endpoint(raw[1], 1)
    else:
        t0, t1 = sqrt_endpoint(raw[1], -1), sqrt_endpoint(raw[0], -1)
    return [t0, t1, rational_endpoint(raw[2]), rational_endpoint(raw[3]),
            rational_endpoint(raw[4]), rational_endpoint(raw[5])], ["t", "p", "s"]


def face_rows(chart: str, bounds: list[dict[str, Any]], endpoint_flags: list[bool | None]) -> list[dict[str, Any]]:
    output = []
    for axis in range(3):
        transverse = [index for index in range(3) if index != axis]
        for side in range(2):
            body = {
                "axis": ("t", "p", "s")[axis],
                "side": "LOWER" if side == 0 else "UPPER",
                "chart": chart,
                "coordinate": bounds[2 * axis + side],
                "transverse_open_rectangle": [
                    bounds[2 * transverse[0]], bounds[2 * transverse[0] + 1],
                    bounds[2 * transverse[1]], bounds[2 * transverse[1] + 1],
                ],
                "included_in_support": endpoint_flags[2 * axis + side],
            }
            output.append({**body, "face_descriptor_sha256": object_sha(body)})
    return output


def load_lineage_maps() -> tuple[
    dict[str, str], dict[str, str], dict[str, str], dict[str, str],
]:
    r179 = json.loads((ROOT / FILES["R179"][0]).read_bytes())
    packed = r179["result"]["retained_3d_child_rows"]
    r179_chart = {row[0]: row[3] for row in packed}
    need(len(r179_chart) == len(packed), "R179 retained child uniqueness")

    r234 = json.loads((ROOT / FILES["R234"][0]).read_bytes())
    values = r234["result"]["resolved_descendant_rows"]
    r234_chart = {row["materialized_row_id"]: row["chart"] for row in values}
    need(len(r234_chart) == len(values), "R234 resolved uniqueness")

    r236 = json.loads((ROOT / FILES["R236"][0]).read_bytes())
    values = r236["result"]["crossing_dependency_discharge_rows"]
    r236_chart = {
        row["crossing_dependency_discharge_row_id"]:
        row["local_return_signature"]["source_chart"]
        for row in values
    }
    need(len(r236_chart) == len(values) == 32, "R236 crossing uniqueness")

    c5_chart = {}
    for row in closed_rows(ROOT / FILES["C5"][0]):
        semantic = row["semantic_classification"]
        if semantic["classification"] != "EMPTY_GRAPH":
            continue
        c5_chart[row["row_sha256"]] = semantic["kernel_parameters"]["source_chart"]
    need(len(c5_chart) == 33_344, "C5 empty graph chart census")
    return r179_chart, r234_chart, r236_chart, c5_chart


def source_chart(
    source: str,
    row: dict[str, Any],
    maps: tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]],
) -> str:
    r179_chart, r234_chart, r236_chart, c5_chart = maps
    if source == "C19A":
        return r179_chart[row["construction_certificate"]["retained_child_row_id"]]
    if source == "C19B":
        row_id = row["construction_certificate"]["source_partition_row_id"]
        if row_id.startswith("round234-resolved:"):
            return r234_chart[row_id]
        need(row_id.startswith("round236-crossing:"), "C19B known source lineage")
        return r236_chart[row_id]
    if source == "C19C":
        return c5_chart[row["construction_certificate"]["C5_row_sha256"]]
    if source in {"C20A", "C22A"}:
        return row["support_ast"]["coordinate_chart"]
    need(source == "C23A", "known source")
    return row["support_ast"]["recharted_target_chart"]


def atom_id(source: str, row: dict[str, Any]) -> str:
    if source == "C22A":
        return row["predicate_cell_row_id"]
    if source == "C23A":
        return row["R292_refinement_cell_id"]
    return f"{source.lower()}-support-atom:{row['row_sha256']}"


def owner_id(row: dict[str, Any]) -> str:
    return row.get("member_id") or row["owner_member_id"]


def build(candidate_dir: Path) -> dict[str, Any]:
    for role, (filename, expected) in FILES.items():
        need(file_sha(ROOT / filename) == expected, "input pin:" + role)

    maps = load_lineage_maps()
    candidates: list[dict[str, Any]] = []
    owner_sources: dict[str, set[str]] = defaultdict(set)
    source_counts = Counter()
    chart_counts = Counter()
    support_kind_counts = Counter()
    endpoint_state_counts = Counter()
    atom_ids: set[str] = set()
    for source in EXPECTED_SOURCE_ROWS:
        for row in closed_rows(ROOT / FILES[source][0]):
            source_counts[source] += 1
            owner = owner_id(row)
            owner_sources[owner].add(source)
            aid = atom_id(source, row)
            need(aid not in atom_ids, "unique atom id")
            atom_ids.add(aid)
            support = row["support_ast"]
            chart = source_chart(source, row, maps)
            need(chart in {"G:E", "G:N", "G:W", "G:S"}, "four-chart atom")
            bounds, coordinates = physical_bounds(source, support)
            if support["kind"] in {"OPEN_RATIONAL_BOX", "T2PS_BRANCH_OPEN_RATIONAL_BOX"}:
                flags: list[bool | None] = [False] * 6
                endpoint_state = "EXPLICIT_ALL_OPEN"
            else:
                need(source == "C19C" and support["kind"] == "HALF_OPEN_RATIONAL_BOX",
                     "known support kind")
                # The current AST carries no six-bit endpoint owner vector.
                flags = [None] * 6
                endpoint_state = "UNRESOLVED_MISSING_PER_AXIS_ENDPOINT_OWNERSHIP_VECTOR"
            faces = face_rows(chart, bounds, flags)
            body = {
                "schema": "cm2.c27.same-chart-relative-cells-totality-census.v1.atom-row.v1",
                "atom_id": aid,
                "source_kernel": source,
                "source_row_sha256": row["row_sha256"],
                "owner_member_id": owner,
                "chart": chart,
                "physical_coordinates": coordinates,
                "physical_bounds": bounds,
                "support_kind": support["kind"],
                "endpoint_ownership_state": endpoint_state,
                "endpoint_inclusion_flags_lower_upper_t_p_s": flags,
                "closure_faces": faces,
                "terminal_assignment": (
                    "UNRESOLVED_PHYSICAL_FACE_ASSIGNMENT"
                    if any(value is None for value in flags)
                    else "SAME_CHART_RELATIVE_CELLS_CANDIDATE"
                ),
                "formal_credit": 0,
            }
            candidates.append({**body, "row_sha256": object_sha(body)})
            chart_counts[chart] += 1
            support_kind_counts[support["kind"]] += 1
            endpoint_state_counts[endpoint_state] += 1
        need(source_counts[source] == EXPECTED_SOURCE_ROWS[source],
             "source census:" + source)
    need(len(candidates) == 483_232, "fresh 483232 atom universe")

    owners = set(owner_sources)
    need(len(owners) == 482_380, "distinct owner census")
    c15: dict[str, dict[str, Any]] = {}
    for row in closed_rows(ROOT / FILES["C15"][0]):
        member = row["registry_member_id"]
        if member in owners:
            need(member not in c15, "C15 unique member")
            c15[member] = row
    need(set(c15) == owners, "complete C15 owner join")

    c25: dict[str, dict[str, Any]] = {}
    for row in closed_rows(ROOT / FILES["C25"][0]):
        member = row["member_id"]
        if member in owners:
            need(member not in c25, "C25 unique member")
            c25[member] = row
    need(set(c25) == owners, "complete C25 owner join")
    for member, sources in owner_sources.items():
        expected = {EXPECTED_KERNEL_BY_SOURCE[source] for source in sources}
        need(len(expected) == 1, "owner crosses candidate source kernels")
        need(c25[member]["source_bindings"]["support_kernel"] == next(iter(expected)),
             "C25 kernel binding")
        need(c25[member]["fresh_component_id"] == c15[member]["fresh_component_id"],
             "C15/C25 component binding")

    c26_owner_nodes: dict[str, Counter[str]] = defaultdict(Counter)
    c26_row_count = 0
    for row in closed_rows(ROOT / FILES["C26"][0]):
        member = row["owner_member_id"]
        if member in owners:
            c26_owner_nodes[member][row["node_id"]] += 1
            c26_row_count += 1
    c26_covered = set(c26_owner_nodes)
    c26_source_coverage = {}
    for source in EXPECTED_SOURCE_ROWS:
        source_owners = {owner for owner, values in owner_sources.items() if source in values}
        c26_source_coverage[source] = {
            "distinct_owner_count": len(source_owners),
            "owners_with_at_least_one_C26_feature": len(source_owners & c26_covered),
            "owners_without_C26_feature": len(source_owners - c26_covered),
        }

    # A duplicate complete box in distinct C15 components is already a strict
    # positive-volume witness.  This exact-equality screen is complete for that
    # falsifier, but is intentionally not advertised as a full overlap screen.
    equal_box_components: dict[bytes, set[str]] = defaultdict(set)
    equal_box_atoms: dict[bytes, int] = Counter()
    for row in candidates:
        key = canonical([row["chart"], row["physical_bounds"]])
        equal_box_components[key].add(c15[row["owner_member_id"]]["fresh_component_id"])
        equal_box_atoms[key] += 1
    exact_equal_cross_component_groups = sum(
        len(components) > 1 for components in equal_box_components.values()
    )
    exact_equal_duplicate_groups = sum(count > 1 for count in equal_box_atoms.values())

    candidate_dir.mkdir(parents=True, exist_ok=True)
    candidates.sort(key=lambda row: row["atom_id"].encode("ascii"))
    sequence = hashlib.sha256()
    with (candidate_dir / LEDGER).open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as packed:
            for ordinal, row in enumerate(candidates):
                body = dict(row)
                body["ordinal"] = ordinal
                body.pop("row_sha256")
                closed = {**body, "row_sha256": object_sha(body)}
                sequence.update(bytes.fromhex(closed["row_sha256"]))
                packed.write(canonical(closed) + b"\n")

    unresolved = endpoint_state_counts[
        "UNRESOLVED_MISSING_PER_AXIS_ENDPOINT_OWNERSHIP_VECTOR"
    ]
    need(unresolved == 33_344, "half-open unresolved census")
    need(endpoint_state_counts["EXPLICIT_ALL_OPEN"] == 449_888,
         "explicit open census")
    body = {
        "schema": "cm2.c27.same-chart-relative-cells-totality-census.v1",
        "status": "FAIL_CLOSED__SAME_CHART_RELATIVE_CELLS_TOTALITY_UNAUTHORIZED__33344_HALF_OPEN_ENDPOINT_OWNERSHIP_VECTORS_ABSENT__ZERO_CREDIT",
        "forbidden_inputs": {
            "C27_FAMILIES_imported_or_read": False,
            "old_edge_ledger_used_as_candidate_universe": False,
        },
        "fresh_candidate_universe": {
            "atom_count": len(candidates),
            "distinct_owner_member_count": len(owners),
            "source_row_census": dict(source_counts),
            "chart_census": dict(sorted(chart_counts.items())),
            "support_kind_census": dict(sorted(support_kind_counts.items())),
            "candidate_atom_ids_sha256": object_sha([row["atom_id"] for row in candidates]),
            "materialized_atom_row_sequence_sha256": sequence.hexdigest(),
        },
        "authority_joins": {
            "C15_owner_join_count": len(c15),
            "C15_owner_join_gap": len(owners - set(c15)),
            "C25_owner_join_count": len(c25),
            "C25_owner_join_gap": len(owners - set(c25)),
            "C15_C25_component_mismatch_count": 0,
            "C26_feature_row_count_on_candidate_owners": c26_row_count,
            "C26_distinct_owner_coverage_count": len(c26_covered),
            "C26_distinct_owner_gap_count": len(owners - c26_covered),
            "C26_source_coverage": c26_source_coverage,
            "C26_absence_is_not_silently_interpreted_as_negative_disposition": True,
        },
        "face_and_relative_position_index": {
            "closure_face_descriptor_count": 6 * len(candidates),
            "explicit_endpoint_ownership_atom_count": 449_888,
            "unresolved_endpoint_ownership_atom_count": unresolved,
            "endpoint_state_census": dict(sorted(endpoint_state_counts.items())),
            "exact_equal_box_duplicate_group_count": exact_equal_duplicate_groups,
            "exact_equal_box_cross_component_witness_group_count": exact_equal_cross_component_groups,
            "nonidentical_overlap_and_face_touch_totality_status": "NOT_DECIDABLE_UNTIL_HALF_OPEN_ENDPOINT_BITS_ARE_MATERIALIZED",
            "all_candidate_unique_terminal_assignment": False,
            "unresolved_candidate_count": unresolved,
            "legal_cross_component_witness_count": (
                exact_equal_cross_component_groups
                if exact_equal_cross_component_groups > 0 else None
            ),
        },
        "minimum_missing_authority": {
            "blocking_source_kernel": "C19C",
            "blocking_atom_count": unresolved,
            "required_field": "six explicit booleans [t_lower,t_upper,p_lower,p_upper,s_lower,s_upper] declaring membership of each boundary face, materialized from the primitive R234 subdivision/half-open ownership rule and bound row-by-row through C19C and C25",
            "why_required": "equal closure geometry does not determine whether a shared face is absent from both supports, owned by exactly one support, or included by both; those cases have different physical connectivity and terminal assignments",
            "forbidden_default": "do not coerce HALF_OPEN_RATIONAL_BOX to OPEN_RATIONAL_BOX or CLOSED_RATIONAL_BOX",
            "additional_C26_contract_needed_for_full_gate": "either bind every candidate owner to an applicable C26 feature disposition, or seal a primitive theorem that owners without a C26 row require no transition feature; current absence is not a negative theorem",
        },
        "ledger": {
            "filename": LEDGER,
            "row_count": len(candidates),
            "sha256": file_sha(candidate_dir / LEDGER),
            "size": (candidate_dir / LEDGER).stat().st_size,
        },
        "input_pins": {filename: expected for filename, expected in FILES.values()},
        "formal_credit": 0,
        "C27_C28_C29": "REJECT",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = {**body, "result_sha256": object_sha(body)}
    (candidate_dir / RESULT).write_bytes(canonical(result) + b"\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    args = parser.parse_args()
    result = build(Path(args.candidate_dir).resolve())
    print(canonical({
        "status": result["status"],
        "atom_count": result["fresh_candidate_universe"]["atom_count"],
        "unresolved_candidate_count": result["face_and_relative_position_index"]["unresolved_candidate_count"],
        "exact_equal_box_cross_component_witness_group_count": result["face_and_relative_position_index"]["exact_equal_box_cross_component_witness_group_count"],
        "result_sha256": result["result_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
