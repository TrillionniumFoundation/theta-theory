#!/usr/bin/env python3
"""Fail-closed v2 routing audit for three support-stratum terminals.

This program is intentionally independent of Round306C27.  It never opens a
C27 FAMILIES object or an old edge ledger.  It reconstructs the *explicitly
proved upstream witness surface* for

  * SIGNED_BOUNDARY_FACES (Round299 independent signed-face inventory),
  * COMPLETE_BOUNDARY_FACES (Round300B complete face inventory), and
  * POSITIVE_VOLUME_CARRIERS (Round300C positive-volume witness inventory),

then crosswalks every endpoint to the complete C15/C25 member universe.  The
three upstream surfaces are not naturally disjoint: every one of the 25,452
signed pairs is also present in the 36,140 complete-face pair set.  A declared
SIGNED -> COMPLETE -> POSITIVE priority produces a deterministic disjoint
assignment of 25,452 / 10,688 / 6,322 pairs.

That assignment is only a routing of the explicit upstream witness surface.
It is not, and is never reported as, the primitive candidate universe.  The
Round300C source explicitly says its scope is nonexhaustive; C25/C26 contain no
row-bound three-terminal selection theorem; 51,172 current primitive support
rows require an external chart/sign crosswalk; and all 483,232 primitive atoms
lack a direct terminal binding.  The result therefore materializes the exact
remaining authority gap and returns zero formal credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import random
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent

C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C26 = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz"
SIGNED = "cm2_round299_source_g_r292_signed_support_face_classifier_independent_probe_ledger.json.gz"
SIGNED_RESULT = "cm2_round299_source_g_r292_signed_support_face_classifier_independent_probe_result.json"
COMPLETE = "cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure_face_inventory.json.gz"
COMPLETE_RESULT = "cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure_result.json"
POSITIVE = "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_volume_edge_promotion_witness_ledger.json.gz"
POSITIVE_RESULT = "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_volume_edge_promotion_result.json"

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
    C25: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    C26: "fc6d1a31e9e7c476bde73336c18d7ad4fb92deed71c3f7b7c58638c0ffc8e88e",
    SIGNED: "9797d486eaf96ce8352883093c24637b5eb9cb27af60fd79e5ee03a6585d27a9",
    SIGNED_RESULT: "07427f743ace170d6d7d832c67658d8d27eca2d51092049625c117abfc8efcdb",
    COMPLETE: "443f26bdbed929d873972be0d2232809bf022feed1a5709001ee8f2dda49ac2d",
    COMPLETE_RESULT: "142a5bd878f0e52ee994e41fa7e1b59863cc70ce609a8ed8a8a15f1be346e82d",
    POSITIVE: "bbb690ba8236230bb99fa8c2dcf569f97c758d546c1ec56ae6d3f6c9d880c7e2",
    POSITIVE_RESULT: "415705e38662fa12260320ae0daf77e5e154c38ee9a886ea82f03f22894b44ad",
    SOURCES["C19A"]: "9da9f54fc21ae59be3e9ea0ec3eb636f37c1445ecf759dbe6e2eea358cb262b3",
    SOURCES["C19B"]: "ee23ebba0e90728ad7b16bccd34d90ba0c2ce701db240c63ba50cbc04e896798",
    SOURCES["C19C"]: "1f0f3f89cac5b10881b4b31a56b86d168ef901ca29bda6ad9eda87fc5f48ff84",
    SOURCES["C20A"]: "bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922",
    SOURCES["C22A"]: "e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb",
    SOURCES["C23A"]: "230d8081c31c200e1adc1d74f57724b4767380fcaa0ab09c00bca9d20444c528",
}

EXPECTED_SOURCE_COUNTS = {
    "C19A": 5_596,
    "C19B": 12_232,
    "C19C": 33_344,
    "C20A": 126_468,
    "C22A": 295_340,
    "C23A": 10_252,
}

TERMINALS = (
    "SIGNED_BOUNDARY_FACES",
    "COMPLETE_BOUNDARY_FACES",
    "POSITIVE_VOLUME_CARRIERS",
)


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


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            state.update(block)
    return state.hexdigest()


def closed_row(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label + ":row closure")


def jsonl_rows(name: str) -> Iterator[dict[str, Any]]:
    with gzip.open(ROOT / name, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"{name}:newline:{ordinal}")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw,
                 f"{name}:canonical:{ordinal}")
            closed_row(row, f"{name}:{ordinal}")
            yield row


def document_rows(name: str) -> Iterator[dict[str, Any]]:
    """Stream the canonical rows array without loading multi-GB proofs."""
    with gzip.open(ROOT / name, "rt", encoding="utf-8") as stream:
        buffer = ""
        while '"rows":[' not in buffer:
            piece = stream.read(1 << 20)
            need(bool(piece), name + ":rows marker")
            buffer += piece
        buffer = buffer.split('"rows":[', 1)[1]
        decoder = json.JSONDecoder()
        ordinal = 0
        while True:
            buffer = buffer.lstrip()
            if not buffer:
                piece = stream.read(1 << 20)
                need(bool(piece), name + ":unexpected EOF")
                buffer = piece
                continue
            if buffer[0] == ",":
                buffer = buffer[1:]
                continue
            if buffer[0] == "]":
                return
            try:
                row, end = decoder.raw_decode(buffer)
            except json.JSONDecodeError:
                piece = stream.read(1 << 20)
                need(bool(piece), name + ":malformed row")
                buffer += piece
                continue
            need(type(row) is dict, f"{name}:row object:{ordinal}")
            closed_row(row, f"{name}:{ordinal}")
            yield row
            ordinal += 1
            buffer = buffer[end:]


def result_object(name: str) -> dict[str, Any]:
    value = json.loads((ROOT / name).read_bytes())
    need(type(value) is dict, name + ":result object")
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    need(type(claimed) is str and claimed == digest(body), name + ":result closure")
    return value


def unordered(left: str, right: str) -> tuple[str, str]:
    need(type(left) is str and type(right) is str and left != right,
         "nonself member pair")
    return (left, right) if left < right else (right, left)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical(value) + b"\n")


def write_gzip_rows(path: Path, rows: Iterable[dict[str, Any]]) -> tuple[str, str, int]:
    rows_state = hashlib.sha256()
    count = 0
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as stream:
            for row in rows:
                payload = canonical(row)
                rows_state.update(payload)
                stream.write(payload + b"\n")
                count += 1
    return file_hash(path), rows_state.hexdigest(), count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=False)

    for name, expected in PINS.items():
        need(file_hash(ROOT / name) == expected, "input pin:" + name)

    signed_result = result_object(SIGNED_RESULT)
    complete_result = result_object(COMPLETE_RESULT)
    positive_result = result_object(POSITIVE_RESULT)
    need(
        signed_result["status"]
        == "PASS_ZERO_CREDIT__ALL_43092_SIGNED_FACE_CONTACTS_CLASSIFIED",
        "signed result status",
    )
    need(
        complete_result["status"]
        == "PASS_FORMAL_FULL_FACE_INVENTORY_CLOSED__10416_CANONICAL_NOVEL_COMPONENT_EDGES__ZERO_DSU_RANK_CREDIT",
        "complete result status",
    )
    need(
        positive_result["status"]
        == "PASS_ROUND300C_EXACT_POSITIVE_VOLUME_EDGE_PROMOTION__6322_WITNESSES__6314_CANONICAL_EDGES__SCOPE_REMAINS_NONEXHAUSTIVE"
        and positive_result["strict_nonpromotion"]["complete_virtual_new_occurrence_frontier_claimed"] is False,
        "positive result explicitly nonexhaustive",
    )

    # C15/C25 complete identity and exact-support crosswalk.
    c15: dict[str, dict[str, str]] = {}
    component_sizes: Counter[str] = Counter()
    for ordinal, row in enumerate(jsonl_rows(C15)):
        need(row["member_ordinal"] == ordinal, "C15 ordinal")
        member = row["registry_member_id"]
        need(member not in c15, "C15 member unique")
        c15[member] = {
            "component": row["fresh_component_id"],
            "official_key": row["official_key_id"],
            "row_sha256": row["row_sha256"],
        }
        component_sizes[row["fresh_component_id"]] += 1
    need(len(c15) == 502_204, "C15 census")

    c25: dict[str, dict[str, str]] = {}
    support_semantics: Counter[str] = Counter()
    support_kernels: Counter[str] = Counter()
    for ordinal, row in enumerate(jsonl_rows(C25)):
        need(row["member_ordinal"] == ordinal, "C25 ordinal")
        member = row["member_id"]
        need(member in c15 and member not in c25, "C25 member join/unique")
        need(
            row["fresh_component_id"] == c15[member]["component"]
            and row["source_bindings"]["C15_member_row_sha256"]
            == c15[member]["row_sha256"],
            "C15/C25 exact join",
        )
        c25[member] = {
            "kernel": row["source_bindings"]["support_kernel"],
            "semantic": row["support_semantic_kind"],
            "support_sha256": row["normalized_support_ast_sha256"],
        }
        support_semantics[row["support_semantic_kind"]] += 1
        support_kernels[row["source_bindings"]["support_kernel"]] += 1
    need(len(c25) == len(c15), "C25 census")

    c26_kinds: Counter[str] = Counter()
    direct_terminal_rows = 0
    for ordinal, row in enumerate(jsonl_rows(C26)):
        need(row["feature_ordinal"] == ordinal, "C26 ordinal")
        c26_kinds[row["obligation_kind"]] += 1
        if row["node_id"] in TERMINALS or row["obligation_kind"] in TERMINALS:
            direct_terminal_rows += 1
    need(sum(c26_kinds.values()) == 691_424, "C26 census")
    need(direct_terminal_rows == 0, "C26 has no direct three-terminal assignment")

    pair_evidence: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    signed_decisions: Counter[str] = Counter()
    signed_self = 0
    signed_rows = 0
    for row in document_rows(SIGNED):
        signed_rows += 1
        decision = row["decision"]
        signed_decisions[decision] += 1
        if decision.startswith("ACCEPT_"):
            need(Fraction(row["exact_transformed_coordinate_face_area"]) > 0,
                 "signed positive face area")
            need(row["left_corridor"] is not None and row["right_corridor"] is not None,
                 "signed two corridors")
            left = row["left_formal_occurrence_id"]
            right = row["right_formal_occurrence_id"]
            if left == right:
                signed_self += 1
            else:
                pair_evidence[unordered(left, right)]["R299_SIGNED_ACCEPTED_FACE"] += 1
        else:
            need(decision == "REJECT_NO_COMMON_POSITIVE_AREA_SIGNED_FACE_PATCH",
                 "signed known rejection")
            need(row["exclusion_evidence"] is not None, "signed exclusion evidence")
    need(
        signed_rows == 43_092
        and signed_decisions
        == {
            "ACCEPT_STRICT_POSITIVE_AREA_FACE_PATCH_AND_TWO_SIDED_CORRIDOR": 29_948,
            "REJECT_NO_COMMON_POSITIVE_AREA_SIGNED_FACE_PATCH": 13_144,
        }
        and signed_self == 2_092,
        "signed complete census",
    )
    signed_pairs = {
        pair for pair, evidence in pair_evidence.items()
        if evidence["R299_SIGNED_ACCEPTED_FACE"]
    }
    need(len(signed_pairs) == 25_452, "signed pair census")

    complete_decisions: Counter[str] = Counter()
    complete_self = 0
    complete_raw_nonself = 0
    complete_rows = 0
    for row in document_rows(COMPLETE):
        complete_rows += 1
        key = row["face_channel"] + "|" + row["decision"]
        complete_decisions[key] += 1
        if row["decision"].startswith("ACCEPT_"):
            need(Fraction(row["exact_coordinate_face_area"]) > 0,
                 "complete positive face area")
            need(row["left_corridor"] is not None and row["right_corridor"] is not None,
                 "complete two corridors")
            for left in row["left_formal_occurrence_endpoints"]:
                for right in row["right_formal_occurrence_endpoints"]:
                    if left == right:
                        complete_self += 1
                    else:
                        complete_raw_nonself += 1
                        pair_evidence[unordered(left, right)]["R300B_COMPLETE_ACCEPTED_FACE"] += 1
        else:
            need(row["exclusion_evidence"] is not None, "complete exclusion evidence")
    need(
        complete_rows == 62_548
        and complete_self == 15_056
        and complete_raw_nonself == 91_760,
        "complete face expansion census",
    )
    complete_pairs = {
        pair for pair, evidence in pair_evidence.items()
        if evidence["R300B_COMPLETE_ACCEPTED_FACE"]
    }
    need(len(complete_pairs) == 36_140, "complete pair census")

    positive_rows = 0
    positive_classes: Counter[str] = Counter()
    for row in document_rows(POSITIVE):
        positive_rows += 1
        need(
            row["positive_volume_physical_overlap"] is True
            and Fraction(row["exact_positive_intersection_volume"]) > 0,
            "positive-volume witness",
        )
        positive_classes[row["witness_class"]] += 1
        pair_evidence[unordered(
            row["virtual_stratum_node_id"],
            row["Round294_registry_occurrence_id"],
        )]["R300C_POSITIVE_VOLUME_WITNESS"] += 1
    need(
        positive_rows == 6_322
        and positive_classes
        == {
            "ROUND288_RATIONAL_INNER_BOX_OVERLAP": 6_214,
            "ROUND292_EXACT_TRANSFORMED_CELL_OVERLAP": 108,
        },
        "positive witness census",
    )
    positive_pairs = {
        pair for pair, evidence in pair_evidence.items()
        if evidence["R300C_POSITIVE_VOLUME_WITNESS"]
    }
    need(len(positive_pairs) == 6_322, "positive member-pair census")

    need(
        len(signed_pairs & complete_pairs) == 25_452
        and signed_pairs <= complete_pairs
        and not (positive_pairs & signed_pairs)
        and not (positive_pairs & complete_pairs),
        "exact three-surface overlaps",
    )

    # Explicit priority makes the upstream surface disjoint.  It does not
    # claim that the surface is a complete primitive candidate universe.
    assigned: dict[tuple[str, str], str] = {}
    for pair in signed_pairs:
        assigned[pair] = "SIGNED_BOUNDARY_FACES"
    for pair in complete_pairs - signed_pairs:
        assigned[pair] = "COMPLETE_BOUNDARY_FACES"
    for pair in positive_pairs - complete_pairs - signed_pairs:
        assigned[pair] = "POSITIVE_VOLUME_CARRIERS"
    assigned_census = Counter(assigned.values())
    need(
        assigned_census
        == {
            "SIGNED_BOUNDARY_FACES": 25_452,
            "COMPLETE_BOUNDARY_FACES": 10_688,
            "POSITIVE_VOLUME_CARRIERS": 6_322,
        }
        and len(assigned) == 42_462,
        "priority assignment census",
    )

    routed_members: set[str] = set()
    same_component = 0
    cross_component = 0
    route_rows: list[dict[str, Any]] = []
    for left, right in sorted(assigned):
        need(left in c15 and right in c15 and left in c25 and right in c25,
             "upstream endpoint current C15/C25 crosswalk")
        routed_members.update((left, right))
        if c15[left]["component"] == c15[right]["component"]:
            same_component += 1
        else:
            cross_component += 1
        evidence = pair_evidence[(left, right)]
        body: dict[str, Any] = {
            "assigned_terminal": assigned[(left, right)],
            "current_C15_components": [
                c15[left]["component"], c15[right]["component"],
            ],
            "current_C25_support_kernels": [
                c25[left]["kernel"], c25[right]["kernel"],
            ],
            "current_C25_support_semantics": [
                c25[left]["semantic"], c25[right]["semantic"],
            ],
            "left_member_id": left,
            "pair_assignment_rule": "FIRST_MATCH_SIGNED_THEN_COMPLETE_THEN_POSITIVE",
            "right_member_id": right,
            "upstream_evidence_multiplicity": dict(sorted(evidence.items())),
            "upstream_surface_only_not_total_universe": True,
        }
        body["row_sha256"] = digest(body)
        route_rows.append(body)

    route_path = out / "explicit_upstream_surface_unique_pair_routes.jsonl.gz"
    route_file_sha, route_rows_sha, route_count = write_gzip_rows(route_path, route_rows)
    need(route_count == 42_462, "route ledger count")

    # Primitive current-support inventory.  These rows establish exact support
    # geometry but do not carry the missing pair-selection authority.
    source_order = list(SOURCES)
    random.Random(args.seed).shuffle(source_order)
    primitive_owner_ids: set[str] = set()
    source_summaries: dict[str, dict[str, Any]] = {}
    primitive_atoms_without_direct_terminal_binding = 0
    atoms_requiring_external_chart_crosswalk = 0
    half_open_atoms_without_row_bound_endpoint_bits = 0
    for source in source_order:
        rows_count = 0
        owners: set[str] = set()
        routed_owner_rows = 0
        explicit_chart_rows = 0
        for ordinal, row in enumerate(jsonl_rows(SOURCES[source])):
            need(row["ordinal"] == ordinal, source + ":ordinal")
            member = row.get("member_id", row.get("owner_member_id"))
            component = row.get("fresh_component_id", row.get("owner_fresh_component_id"))
            need(member in c15 and member in c25, source + ":owner join")
            need(c15[member]["component"] == component, source + ":component join")
            support = row["support_ast"]
            need(row["support_ast_sha256"] == digest(support), source + ":support closure")
            bounds = [Fraction(value) for value in support["bounds"]]
            need(len(bounds) == 6 and all(bounds[2*i] < bounds[2*i+1] for i in range(3)),
                 source + ":positive box")
            need(not any(key in row for key in ("terminal", "assigned_terminal", "transition_family")),
                 source + ":no direct terminal field")
            rows_count += 1
            owners.add(member)
            primitive_owner_ids.add(member)
            primitive_atoms_without_direct_terminal_binding += 1
            if member in routed_members:
                routed_owner_rows += 1
            if "coordinate_chart" in support or "recharted_target_chart" in support:
                explicit_chart_rows += 1
            else:
                atoms_requiring_external_chart_crosswalk += 1
            if support["kind"] == "HALF_OPEN_RATIONAL_BOX":
                need(source == "C19C", "half-open source")
                endpoint_fields = {
                    f"axis_{axis}_{side}_included"
                    for axis in range(3) for side in ("lower", "upper")
                }
                if not endpoint_fields <= set(support):
                    half_open_atoms_without_row_bound_endpoint_bits += 1
        need(rows_count == EXPECTED_SOURCE_COUNTS[source], source + ":census")
        source_summaries[source] = {
            "atom_count": rows_count,
            "distinct_owner_count": len(owners),
            "explicit_chart_row_count": explicit_chart_rows,
            "owner_participates_in_explicit_upstream_routed_surface_row_count": routed_owner_rows,
            "row_bound_direct_terminal_assignment_count": 0,
        }
    need(
        primitive_atoms_without_direct_terminal_binding == 483_232
        and len(primitive_owner_ids) == 482_380
        and atoms_requiring_external_chart_crosswalk == 51_172
        and half_open_atoms_without_row_bound_endpoint_bits == 33_344,
        "primitive blocker census",
    )

    blocker_rows: list[dict[str, Any]] = []
    for source in sorted(source_summaries):
        body = {
            "blocker_class": "CURRENT_PRIMITIVE_FULL_SUPPORT_TO_THREE_TERMINAL_PAIR_SELECTION_CROSSWALK_ABSENT",
            "source": source,
            **source_summaries[source],
            "required_authority": (
                "ROW_BOUND_EXHAUSTIVE_PAIR_CANDIDATE_GENERATION_AND_UNIQUE_"
                "THREE_TERMINAL_SELECTION_PREDICATE"
            ),
        }
        body["row_sha256"] = digest(body)
        blocker_rows.append(body)
    nonexhaustive = {
        "blocker_class": "EXPLICIT_UPSTREAM_POSITIVE_VOLUME_SCOPE_NONEXHAUSTIVE",
        "Round300C_nonincident_new_occurrence_count": positive_result["strict_nonpromotion"]["nonincident_new_occurrence_count"],
        "Round300C_withheld_Round248_wall_sheet_count": positive_result["strict_nonpromotion"]["withheld_Round248_wall_sheet_count"],
        "Round300C_withheld_inherited_2D_sheet_count": positive_result["strict_nonpromotion"]["withheld_inherited_2D_sheet_count"],
        "complete_virtual_new_occurrence_frontier_claimed": False,
        "required_authority": "CURRENT_FULL_SUPPORT_EXHAUSTION_BEYOND_THE_EXPLICIT_R300C_WITNESS_SCOPE",
    }
    nonexhaustive["row_sha256"] = digest(nonexhaustive)
    blocker_rows.append(nonexhaustive)
    blocker_path = out / "minimal_full_support_totality_blockers.jsonl.gz"
    blocker_file_sha, blocker_rows_sha, blocker_count = write_gzip_rows(
        blocker_path, blocker_rows
    )
    need(blocker_count == 7, "blocker ledger count")

    current_cross_pair_denominator = (
        len(c15) * (len(c15) - 1) // 2
        - sum(size * (size - 1) // 2 for size in component_sizes.values())
    )
    semantic_projection = {
        "assigned_census": dict(sorted(assigned_census.items())),
        "assigned_pair_count": len(assigned),
        "blocker_file_sha256": blocker_file_sha,
        "blocker_rows_sha256": blocker_rows_sha,
        "route_file_sha256": route_file_sha,
        "route_rows_sha256": route_rows_sha,
    }
    result: dict[str, Any] = {
        "C27_FAMILIES_imported_or_read": False,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
        "edge_ledger_used_as_candidate_universe": False,
        "formal_credit": 0,
        "input_pins": dict(sorted(PINS.items())),
        "invocation_seed": args.seed,
        "current_universe": {
            "C15_member_count": len(c15),
            "C15_component_count": len(component_sizes),
            "C15_cross_component_pair_denominator_diagnostic_only": current_cross_pair_denominator,
            "C25_support_kernel_census": dict(sorted(support_kernels.items())),
            "C25_support_semantic_census": dict(sorted(support_semantics.items())),
            "C26_feature_count": sum(c26_kinds.values()),
            "C26_direct_three_terminal_assignment_row_count": direct_terminal_rows,
            "primitive_atom_count": primitive_atoms_without_direct_terminal_binding,
            "primitive_distinct_owner_count": len(primitive_owner_ids),
        },
        "explicit_upstream_surface": {
            "SIGNED_distinct_pair_count": len(signed_pairs),
            "COMPLETE_distinct_pair_count": len(complete_pairs),
            "POSITIVE_distinct_member_pair_count": len(positive_pairs),
            "SIGNED_intersection_COMPLETE_pair_count": len(signed_pairs & complete_pairs),
            "SIGNED_is_subset_of_COMPLETE": signed_pairs <= complete_pairs,
            "POSITIVE_intersection_SIGNED_pair_count": len(positive_pairs & signed_pairs),
            "POSITIVE_intersection_COMPLETE_pair_count": len(positive_pairs & complete_pairs),
            "naturally_mutually_exclusive": False,
            "priority_rule": [
                "SIGNED_BOUNDARY_FACES",
                "COMPLETE_BOUNDARY_FACES",
                "POSITIVE_VOLUME_CARRIERS",
            ],
            "priority_disjoint_assignment_census": dict(sorted(assigned_census.items())),
            "priority_disjoint_pair_count": len(assigned),
            "route_ledger_filename": route_path.name,
            "route_ledger_file_sha256": route_file_sha,
            "route_ledger_rows_sha256": route_rows_sha,
            "route_endpoint_C15_C25_crosswalk_gap": 0,
            "routed_distinct_member_count": len(routed_members),
            "routed_pair_same_current_C15_component_count": same_component,
            "routed_pair_cross_current_C15_component_count": cross_component,
            "is_total_primitive_candidate_universe": False,
        },
        "minimal_totality_blockers": {
            "all_483232_primitive_atoms_have_direct_terminal_binding": False,
            "primitive_atoms_without_direct_terminal_binding": primitive_atoms_without_direct_terminal_binding,
            "current_support_rows_requiring_external_chart_or_sign_crosswalk": atoms_requiring_external_chart_crosswalk,
            "C19C_half_open_atoms_without_row_bound_endpoint_ownership_bits": half_open_atoms_without_row_bound_endpoint_bits,
            "R300C_scope_explicitly_nonexhaustive": True,
            "R300C_nonincident_new_occurrence_count": positive_result["strict_nonpromotion"]["nonincident_new_occurrence_count"],
            "R300C_withheld_Round248_wall_sheet_count": positive_result["strict_nonpromotion"]["withheld_Round248_wall_sheet_count"],
            "R300C_withheld_inherited_2D_sheet_count": positive_result["strict_nonpromotion"]["withheld_inherited_2D_sheet_count"],
            "blocker_ledger_filename": blocker_path.name,
            "blocker_ledger_file_sha256": blocker_file_sha,
            "blocker_ledger_rows_sha256": blocker_rows_sha,
        },
        "semantic_projection_sha256": digest(semantic_projection),
        "strict_nonpromotion": {
            "the_42462_priority_routed_pairs_are_total_universe": False,
            "three_terminal_totality_closed": False,
            "unique_assignment_closed_for_explicit_upstream_surface_only": True,
            "C27_transition_totality": 0,
            "C28_pair_routing": 0,
            "C29_physical_maximality": 0,
        },
        "status": (
            "PASS_EXPLICIT_UPSTREAM_SURFACE_PRIORITY_ROUTING_25452_10688_6322__"
            "REJECT_PRIMITIVE_FULL_SUPPORT_TOTALITY__ZERO_CREDIT"
        ),
    }
    result["result_sha256"] = digest(result)
    write_json(out / "result.json", result)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print("FAIL:" + str(error))
        raise SystemExit(2)
