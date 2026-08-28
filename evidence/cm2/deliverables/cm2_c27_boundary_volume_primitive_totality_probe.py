#!/usr/bin/env python3
"""Fail-closed primitive audit of three C27-independent support terminals.

The program never reads a Round306C27 artifact or an edge ledger.  It starts
from the six box/cell kernels which cover the non-graph, preserved, R2 and
R292 support atoms, binds them to the frozen C15 member components and the C25
typed support ledger, and audits the complete C26 feature ledger.

What can be proved from these sources is deliberately separated from what
cannot.  Positive three-coordinate measure and the six oriented coordinate
faces of every atom are exact arithmetic facts.  The sources do *not* contain
(a) the six endpoint ownership bits for C19C half-open boxes, or (b) a
primitive selection theorem assigning a face/pair/carrier to exactly one of
SIGNED_BOUNDARY_FACES, COMPLETE_BOUNDARY_FACES, POSITIVE_VOLUME_CARRIERS.
Consequently this is a truthful zero-credit REJECT, with an exact materialized
ledger for the smallest row-local authority gap.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import random
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent

C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C26 = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz"

SOURCES = {
    "C19A": "cm2_round306c19a_source_g_5596_legacy_nongraph_exact_box_support_kernel_ledger.jsonl.gz",
    "C19B": "cm2_round306c19b_source_g_12232_r248_exact_positive_box_support_kernel_ledger.jsonl.gz",
    "C19C": "cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel_ledger.jsonl.gz",
    "C20A": "cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz",
    "C22A": "cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_ledger.jsonl.gz",
    "C23A": "cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_ledger.jsonl.gz",
}

PINS = {
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    SOURCES["C19A"]: "9da9f54fc21ae59be3e9ea0ec3eb636f37c1445ecf759dbe6e2eea358cb262b3",
    SOURCES["C19B"]: "ee23ebba0e90728ad7b16bccd34d90ba0c2ce701db240c63ba50cbc04e896798",
    SOURCES["C19C"]: "1f0f3f89cac5b10881b4b31a56b86d168ef901ca29bda6ad9eda87fc5f48ff84",
    SOURCES["C20A"]: "bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922",
    SOURCES["C22A"]: "e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb",
    SOURCES["C23A"]: "230d8081c31c200e1adc1d74f57724b4767380fcaa0ab09c00bca9d20444c528",
    C25: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    C26: "fc6d1a31e9e7c476bde73336c18d7ad4fb92deed71c3f7b7c58638c0ffc8e88e",
}

EXPECTED_SOURCE_COUNTS = {
    "C19A": 5_596,
    "C19B": 12_232,
    "C19C": 33_344,
    "C20A": 126_468,
    "C22A": 295_340,
    "C23A": 10_252,
}
EXPECTED_KINDS = {
    "C19A": "OPEN_RATIONAL_BOX",
    "C19B": "OPEN_RATIONAL_BOX",
    "C19C": "HALF_OPEN_RATIONAL_BOX",
    "C20A": "OPEN_RATIONAL_BOX",
    "C22A": "OPEN_RATIONAL_BOX",
    "C23A": "T2PS_BRANCH_OPEN_RATIONAL_BOX",
}
C25_KERNEL = {
    "C19A": "C19A", "C19B": "C19B", "C19C": "C19C",
    "C20A": "C20A", "C22A": "C22B", "C23A": "C23B",
}
EXPECTED_C26_KINDS = {
    "A1_R204_TARGET_SHEET": 224,
    "A1_R211_OWNER_SHEET": 17_716,
    "A2_R204_SOURCE_TARGET_CURVE": 504,
    "A2_R204_SOURCE_TARGET_ENDPOINT": 280,
    "A2_R211_OWNER_CURVE": 20_456,
    "A2_R211_OWNER_ENDPOINT": 40_912,
    "G1_EXACT_GRAPH_DEFINITION": 5_264,
    "G2A_GRAPH_TO_SHEET_IDENTIFICATION": 5_264,
    "G2B_GRAPH_TO_SIDE_EXACT_NONINCIDENCE": 168,
    "G2B_GRAPH_TO_SIDE_PHYSICAL_INCIDENCE": 9_960,
    "R1_SOURCE_FREE_PREDICATE_CELL_DEFINITION": 295_340,
    "R2_MEMBER_FULL_SUPPORT_UNION": 295_336,
}
TERMINALS = (
    "SIGNED_BOUNDARY_FACES",
    "COMPLETE_BOUNDARY_FACES",
    "POSITIVE_VOLUME_CARRIERS",
)
MISSING_BITS = (
    "axis_0_lower_included", "axis_0_upper_included",
    "axis_1_lower_included", "axis_1_upper_included",
    "axis_2_lower_included", "axis_2_upper_included",
)


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            state.update(block)
    return state.hexdigest()


def checked_rows(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for line_number, line in enumerate(stream, 1):
            need(line.endswith(b"\n"), f"newline:{path.name}:{line_number}")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw,
                 f"canonical row:{path.name}:{line_number}")
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(type(claimed) is str and claimed == digest(body),
                 f"row closure:{path.name}:{line_number}")
            yield row


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical(value) + b"\n")


def write_gzip_rows(path: Path, values: list[dict[str, Any]]) -> tuple[str, str]:
    rows_state = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as stream:
            for value in values:
                payload = canonical(value)
                rows_state.update(payload)
                stream.write(payload + b"\n")
    return file_hash(path), rows_state.hexdigest()


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=False)

    for name, expected in PINS.items():
        need(file_hash(ROOT / name) == expected, f"input pin:{name}")

    c15: dict[str, tuple[str, str]] = {}
    for ordinal, row in enumerate(checked_rows(ROOT / C15)):
        need(row["member_ordinal"] == ordinal, "C15 ordinal")
        member = row["registry_member_id"]
        need(member not in c15, "C15 unique member")
        c15[member] = (row["fresh_component_id"], row["row_sha256"])
    need(len(c15) == 502_204, "C15 census")

    c25: dict[str, tuple[str, str, str, str, str]] = {}
    for ordinal, row in enumerate(checked_rows(ROOT / C25)):
        need(row["member_ordinal"] == ordinal, "C25 ordinal")
        member = row["member_id"]
        need(member not in c25, "C25 unique member")
        c25[member] = (
            row["fresh_component_id"],
            row["source_bindings"]["C15_member_row_sha256"],
            row["source_bindings"]["support_kernel"],
            row["source_bindings"]["support_kernel_row_sha256"],
            row["normalized_support_ast_sha256"],
        )
        need(member in c15, "C25 member in C15")
        need(c15[member] == (row["fresh_component_id"], row["source_bindings"]["C15_member_row_sha256"]),
             "C15/C25 exact binding")
    need(len(c25) == 502_204, "C25 census")

    source_names = list(SOURCES)
    random.Random(args.seed).shuffle(source_names)
    source_census: Counter[str] = Counter()
    kind_census: Counter[str] = Counter()
    owner_ids: set[str] = set()
    atom_commitments: list[str] = []
    atom_face_commitments: list[str] = []
    c22a_row_hashes: set[str] = set()
    unresolved: list[dict[str, Any]] = []
    exact_volume_field_count = 0
    t2ps_analytic_positive_count = 0
    open_atom_count = 0

    for source in source_names:
        for ordinal, row in enumerate(checked_rows(ROOT / SOURCES[source])):
            need(row["ordinal"] == ordinal, f"{source} ordinal")
            member = row.get("member_id", row.get("owner_member_id"))
            component = row.get("fresh_component_id", row.get("owner_fresh_component_id"))
            need(type(member) is str and type(component) is str, f"{source} owner fields")
            need(member in c15 and member in c25, f"{source} owner joins")
            need(c15[member][0] == component and c25[member][0] == component,
                 f"{source} component join")
            need(c25[member][1] == c15[member][1], f"{source} C15 row join")
            need(c25[member][2] == C25_KERNEL[source], f"{source} C25 kernel")
            if source in {"C19A", "C19B", "C19C", "C20A"}:
                need(c25[member][3] == row["row_sha256"], f"{source} C25 source-row binding")
                need(c25[member][4] == row["support_ast_sha256"], f"{source} C25 support binding")

            support = row["support_ast"]
            need(row["support_ast_sha256"] == digest(support), f"{source} support closure")
            need(support["kind"] == EXPECTED_KINDS[source], f"{source} kind")
            need(support["coordinates"] in (["t", "p", "s"], ["t_squared", "p", "s"]),
                 f"{source} coordinates")
            need(len(support["bounds"]) == 6, f"{source} six bounds")
            bounds = [Fraction(value) for value in support["bounds"]]
            widths = [bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4]]
            need(all(width > 0 for width in widths), f"{source} positive widths")
            coordinate_volume = widths[0] * widths[1] * widths[2]
            need(coordinate_volume > 0, f"{source} positive coordinate volume")
            if "exact_volume" in support:
                need(Fraction(support["exact_volume"]) == coordinate_volume,
                     f"{source} exact volume")
                exact_volume_field_count += 1
            if source == "C23A":
                theorem = row["theorem_ast"]
                need(theorem["boundary_faces_excluded_by_open_interval_semantics"] is True,
                     "C23A open boundary theorem")
                need(theorem["branch_map_is_analytic_bijection_for_strictly_positive_t_squared_interval"] is True,
                     "C23A analytic branch theorem")
                need(bounds[0] > 0 and support["physical_t_sign"] in {-1, 1},
                     "C23A positive t2 branch")
                t2ps_analytic_positive_count += 1
            if source == "C22A":
                need(row["theorem_ast"]["boundary_faces_excluded_by_open_interval_semantics"] is True,
                     "C22A open boundary theorem")
                c22a_row_hashes.add(row["row_sha256"])

            atom_id = f"{source}:{row['row_sha256']}"
            source_census[source] += 1
            kind_census[support["kind"]] += 1
            owner_ids.add(member)
            face_rows = []
            for axis in range(3):
                tangential = [index for index in range(3) if index != axis]
                area = widths[tangential[0]] * widths[tangential[1]]
                need(area > 0, f"{source} positive face area")
                for side, outward_sign, endpoint in (
                    ("LOWER", -1, bounds[2 * axis]),
                    ("UPPER", 1, bounds[2 * axis + 1]),
                ):
                    face_rows.append({
                        "axis": axis,
                        "coordinate": support["coordinates"][axis],
                        "fixed_value": fraction_text(endpoint),
                        "outward_orientation_sign": outward_sign,
                        "positive_coordinate_area": fraction_text(area),
                        "side": side,
                    })
            atom_face_commitments.append(digest({"atom_id": atom_id, "faces": face_rows}))
            atom_commitments.append(digest({
                "atom_id": atom_id,
                "component": component,
                "coordinate_volume": fraction_text(coordinate_volume),
                "member": member,
                "support_ast_sha256": row["support_ast_sha256"],
            }))

            if support["kind"] in {"OPEN_RATIONAL_BOX", "T2PS_BRANCH_OPEN_RATIONAL_BOX"}:
                open_atom_count += 1
            else:
                need(source == "C19C", "only C19C may be half-open")
                gap = {
                    "atom_id": atom_id,
                    "bounds": support["bounds"],
                    "fresh_component_id": component,
                    "member_id": member,
                    "minimal_missing_authority": "ROW_BOUND_SIX_ENDPOINT_OWNERSHIP_BITS_OR_AN_EQUIVALENT_HALF_OPEN_PARTITION_RULE",
                    "missing_endpoint_ownership_fields": list(MISSING_BITS),
                    "source": source,
                    "source_row_sha256": row["row_sha256"],
                    "support_ast_sha256": row["support_ast_sha256"],
                }
                gap["row_sha256"] = digest(gap)
                unresolved.append(gap)

    need(dict(source_census) == EXPECTED_SOURCE_COUNTS, "source census")
    atom_count = sum(source_census.values())
    need(atom_count == 483_232 and len(atom_commitments) == atom_count, "atom census")
    need(len(owner_ids) == 482_380, "distinct owner census")
    need(open_atom_count == 449_888 and len(unresolved) == 33_344,
         "open/half-open partition")
    need(exact_volume_field_count == 177_640 and t2ps_analytic_positive_count == 10_252,
         "positive-volume proof-route census")

    c26_census: Counter[str] = Counter()
    c26_r1_source_rows: set[str] = set()
    terminal_assignment_rows = 0
    for ordinal, row in enumerate(checked_rows(ROOT / C26)):
        need(row["feature_ordinal"] == ordinal, "C26 ordinal")
        kind = row["obligation_kind"]
        c26_census[kind] += 1
        if kind in TERMINALS or row["node_id"] in TERMINALS:
            terminal_assignment_rows += 1
        if kind == "R1_SOURCE_FREE_PREDICATE_CELL_DEFINITION":
            need(row["source_bindings"]["source_kernel"] == "C22A", "C26 R1 kernel")
            c26_r1_source_rows.add(row["source_bindings"]["source_row_sha256"])
    need(dict(c26_census) == EXPECTED_C26_KINDS, "C26 complete census")
    need(c26_r1_source_rows == c22a_row_hashes, "C22A/C26 R1 exact cover")
    need(terminal_assignment_rows == 0, "no primitive terminal assignment rows")

    unresolved.sort(key=lambda row: row["atom_id"])
    unresolved_path = out / "half_open_endpoint_ownership_unresolved.jsonl.gz"
    unresolved_file_sha, unresolved_rows_sha = write_gzip_rows(unresolved_path, unresolved)

    atom_commitments.sort()
    atom_face_commitments.sort()
    atom_commitment_sha = digest(atom_commitments)
    face_commitment_sha = digest(atom_face_commitments)
    face_count = atom_count * 6
    open_excluded_face_count = open_atom_count * 6
    unknown_face_membership_count = len(unresolved) * 6

    result: dict[str, Any] = {
        "C27_C28_C29": "REJECT",
        "CM2": "NO-GO_FOR_CLAIM",
        "C27_FAMILIES_imported_or_read": False,
        "edge_ledger_used_as_candidate_universe": False,
        "formal_credit": 0,
        "input_pins": dict(sorted(PINS.items())),
        "primitive_atom_universe": {
            "atom_count": atom_count,
            "atom_commitments_sha256": atom_commitment_sha,
            "distinct_owner_member_count": len(owner_ids),
            "source_census": dict(sorted(source_census.items())),
            "support_kind_census": dict(sorted(kind_census.items())),
            "C15_member_component_join_gap": 0,
            "C25_typed_support_join_gap": 0,
        },
        "positive_volume_census": {
            "positive_coordinate_volume_atom_count": atom_count,
            "nonpositive_coordinate_volume_atom_count": 0,
            "exact_volume_field_verified_count": exact_volume_field_count,
            "T2PS_positive_physical_measure_via_analytic_branch_count": t2ps_analytic_positive_count,
            "local_geometry_status": "PASS_ALL_483232_ATOMS_HAVE_STRICTLY_POSITIVE_THREE_COORDINATE_MEASURE",
            "terminal_totality_state": "REJECT_MISSING_PRIMITIVE_PAIR_CANDIDATE_PREDICATE_AND_UNIQUE_TERMINAL_ASSIGNMENT_THEOREM",
        },
        "boundary_face_census": {
            "geometric_oriented_face_count": face_count,
            "hierarchical_face_commitment_sha256": face_commitment_sha,
            "positive_coordinate_area_face_count": face_count,
            "geometric_outward_orientation_sign_known_count": face_count,
            "open_interval_explicitly_excluded_face_count": open_excluded_face_count,
            "half_open_endpoint_membership_unknown_face_count": unknown_face_membership_count,
            "support_factor_or_predicate_signed_face_authority_count": 0,
            "support_factor_or_predicate_signed_face_authority_gap_count": face_count,
        },
        "C26_audit": {
            "feature_count": sum(c26_census.values()),
            "obligation_kind_census": dict(sorted(c26_census.items())),
            "C22A_R1_exact_source_row_cover_count": len(c26_r1_source_rows),
            "direct_boundary_or_volume_terminal_assignment_row_count": terminal_assignment_rows,
            "atoms_without_direct_boundary_or_volume_terminal_assignment_row_count": atom_count,
        },
        "minimal_missing_authority": {
            "half_open_endpoint_ownership": {
                "atom_count": len(unresolved),
                "face_bit_count": unknown_face_membership_count,
                "ledger_filename": unresolved_path.name,
                "ledger_file_sha256": unresolved_file_sha,
                "ledger_rows_sha256": unresolved_rows_sha,
                "missing_fields": list(MISSING_BITS),
            },
            "three_terminal_selection": {
                "affected_atom_count": atom_count,
                "assigned_atom_count": 0,
                "required_authority": "A_PRIMITIVE_ROW_BOUND_EXHAUSTIVE_MUTUALLY_EXCLUSIVE_SELECTION_PREDICATE_FOR_SIGNED_BOUNDARY_FACES_COMPLETE_BOUNDARY_FACES_POSITIVE_VOLUME_CARRIERS_PLUS_PAIR_ROUTING",
                "terminal_names": list(TERMINALS),
            },
        },
        "terminal_states": {
            "SIGNED_BOUNDARY_FACES": "REJECT_GEOMETRIC_ORIENTATION_IS_NOT_A_SUPPORT_SIGN_THEOREM_AND_NO_UNIQUE_SELECTION_PREDICATE_EXISTS",
            "COMPLETE_BOUNDARY_FACES": "REJECT_33344_HALF_OPEN_ATOMS_LACK_200064_ENDPOINT_OWNERSHIP_BITS_AND_NO_UNIQUE_SELECTION_PREDICATE_EXISTS",
            "POSITIVE_VOLUME_CARRIERS": "REJECT_LOCAL_POSITIVE_MEASURE_PROVED_BUT_PAIR_CANDIDATE_TOTALITY_AND_UNIQUE_TERMINAL_ASSIGNMENT_ARE_UNAUTHORIZED",
        },
        "status": "PASS_LOCAL_PRIMITIVE_CENSUS__REJECT_THREE_TERMINAL_TOTALITY_WITH_EXACT_MINIMAL_AUTHORITY_GAPS__ZERO_CREDIT",
    }
    result["result_sha256"] = digest(result)
    write_json(out / "result.json", result)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print(f"FAIL:{error}")
        raise SystemExit(2)
