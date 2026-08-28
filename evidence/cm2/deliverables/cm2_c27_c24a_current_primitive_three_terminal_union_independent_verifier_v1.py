#!/usr/bin/env python3
"""Independent verifier for the scoped primitive three-terminal union.

This file is intentionally self-contained and imports only the Python
standard library.  It does not import or execute the comparator/producer.  It
reconstructs the pair sets, key crosswalk, unique ownership, component-edge
union, and DSU rank contributions directly from pinned input ledgers.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent


class Reject(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(message)


def encode(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def object_hash(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def verify_row(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claim = body.pop("row_sha256", None)
    require(type(claim) is str and claim == object_hash(body), label + ":closure")


def fp(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
        value.st_mode,
        value.st_uid,
        value.st_gid,
    )


@dataclass
class FileView:
    label: str
    path: Path
    fd: int
    initial: tuple[int, ...]
    sha256: str

    @classmethod
    def acquire(cls, label: str, path: Path, expected: str) -> "FileView":
        require(type(expected) is str and len(expected) == 64, label + ":expected digest")
        resolved = path.resolve()
        fd = os.open(
            resolved,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        )
        try:
            before = os.fstat(fd)
            require(stat.S_ISREG(before.st_mode), label + ":regular")
            state = hashlib.sha256()
            while data := os.read(fd, 4 << 20):
                state.update(data)
            observed = state.hexdigest()
            require(observed == expected, label + ":sha256")
            require(fp(os.fstat(fd)) == fp(before), label + ":hash fstat")
            os.lseek(fd, 0, os.SEEK_SET)
            return cls(label, resolved, fd, fp(before), observed)
        except BaseException:
            os.close(fd)
            raise

    def stable(self, phase: str) -> None:
        require(fp(os.fstat(self.fd)) == self.initial, self.label + ":" + phase + ":fstat")

    def bytes(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while data := os.read(self.fd, 4 << 20):
            chunks.append(data)
        self.stable("bytes")
        return b"".join(chunks)

    def document(self, canonical_file: bool = True) -> dict[str, Any]:
        raw = self.bytes()
        value = json.loads(raw)
        require(type(value) is dict, self.label + ":object")
        if canonical_file:
            require(encode(value) + b"\n" == raw, self.label + ":canonical")
        closure_names = [name for name in ("result_sha256", "receipt_sha256") if name in value]
        require(len(closure_names) == 1, self.label + ":closure name")
        body = dict(value)
        claim = body.pop(closure_names[0])
        require(type(claim) is str and claim == object_hash(body), self.label + ":closure")
        return value

    def jsonl(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for index, line in enumerate(stream):
                    require(line.endswith(b"\n"), f"{self.label}:{index}:newline")
                    payload = line[:-1]
                    row = json.loads(payload)
                    require(type(row) is dict and encode(row) == payload,
                            f"{self.label}:{index}:canonical")
                    verify_row(row, f"{self.label}:{index}")
                    yield row
        self.stable("jsonl")

    def receipt(self) -> dict[str, Any]:
        self.stable("receipt")
        try:
            name = str(self.path.relative_to(ROOT))
        except ValueError:
            name = str(self.path)
        return {
            "path": name,
            "sha256": self.sha256,
            "size": self.initial[2],
            "stat_fingerprint": list(self.initial),
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
        }

    def release(self) -> None:
        os.close(self.fd)


def pair(left: str, right: str) -> tuple[str, str]:
    require(type(left) is str and type(right) is str and left != right, "nonself pair")
    return (left, right) if left < right else (right, left)


def edge(values: Any, label: str) -> tuple[str, str]:
    require(type(values) is list and len(values) == 2
            and all(type(item) is str for item in values), label + ":edge")
    return pair(values[0], values[1])


def disk_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


class Forest:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}
        self.reductions = 0

    def root(self, value: str) -> str:
        self.parent.setdefault(value, value)
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def join(self, left: str, right: str) -> bool:
        a, b = self.root(left), self.root(right)
        if a == b:
            return False
        self.parent[b] = a
        self.reductions += 1
        return True


def rank_data(values: set[tuple[str, str]]) -> dict[str, int]:
    forest = Forest()
    cycles = 0
    for left, right in sorted(values):
        if not forest.join(left, right):
            cycles += 1
    return {
        "edge_count": len(values),
        "vertex_count": len(forest.parent),
        "rank_reduction": forest.reductions,
        "cycle_edge_count": cycles,
        "component_count_on_incident_vertices": len(forest.parent) - forest.reductions,
    }


def addition_contributors(
    base: set[tuple[str, str]], additions: set[tuple[str, str]]
) -> set[tuple[str, str]]:
    forest = Forest()
    for left, right in sorted(base):
        forest.join(left, right)
    answer: set[tuple[str, str]] = set()
    for left, right in sorted(additions):
        if forest.join(left, right):
            answer.add((left, right))
    return answer


def ledger_descriptor(view: FileView) -> dict[str, Any]:
    count = 0
    sequence = hashlib.sha256()
    for row in view.jsonl():
        sequence.update(bytes.fromhex(row["row_sha256"]))
        count += 1
    return {
        "filename": view.path.name,
        "row_count": count,
        "file_sha256": view.sha256,
        "row_sequence_sha256": sequence.hexdigest(),
    }


def acquire_sources(args: argparse.Namespace) -> dict[str, FileView]:
    specifications = {
        "g2a_contacts": (args.g2a_contacts, args.g2a_contacts_sha256),
        "g2a_reverse_empty": (args.g2a_reverse_empty, args.g2a_reverse_empty_sha256),
        "g2a_edges": (args.g2a_edges, args.g2a_edges_sha256),
        "g2a_scoped_result": (args.g2a_scoped_result, args.g2a_scoped_result_sha256),
        "g2b_terminal_receipt": (args.g2b_terminal_receipt, args.g2b_terminal_receipt_sha256),
        "g2b_exact": (args.g2b_exact, args.g2b_exact_sha256),
        "g2b_priority": (args.g2b_priority, args.g2b_priority_sha256),
        "g2b_edges": (args.g2b_edges, args.g2b_edges_sha256),
        "current_routes": (args.current_routes, args.current_routes_sha256),
        "current_seed2_routes": (
            args.current_seed2_routes,
            args.current_seed2_routes_sha256,
        ),
        "current_dual_seed_authority": (
            args.current_dual_seed_authority,
            args.current_dual_seed_authority_sha256,
        ),
        "c19c_endpoint_v3_receipt": (
            args.c19c_endpoint_v3_receipt,
            args.c19c_endpoint_v3_receipt_sha256,
        ),
        "strict_validation_edges": (
            args.strict_validation_edges,
            args.strict_validation_edges_sha256,
        ),
        "comparator_result": (args.comparator_result, args.comparator_result_sha256),
    }
    return {
        name: FileView.acquire(name, Path(filename), sha)
        for name, (filename, sha) in specifications.items()
    }


def verify(args: argparse.Namespace) -> dict[str, Any]:
    output = Path(args.out_file)
    require(not output.exists(), "fresh verifier output")
    views = acquire_sources(args)
    try:
        result = views["comparator_result"].document()
        require(result["schema"]
                == "cm2.c27-independent.c24a-current-primitive-three-terminal-union-comparator.v1",
                "comparator result schema")
        require(result["status"].endswith("GLOBAL_TOTALITY_FAIL_CLOSED__ZERO_CREDIT"),
                "comparator fail-closed status")
        projection = {key: value for key, value in result.items()
                      if key not in {"invocation_seed", "root_input_capture",
                                     "semantic_projection_sha256", "result_sha256"}}
        require(result["semantic_projection_sha256"] == object_hash(projection),
                "semantic projection closure")

        for name, view in views.items():
            if name == "comparator_result":
                continue
            attestation = result["root_input_capture"]["attestations"][name]
            require(attestation["sha256"] == view.sha256, name + ":result input binding")

        terminal = views["g2b_terminal_receipt"].document()
        require(terminal["formal_state_unchanged"]["formal_credit"] == 0
                and terminal["formal_state_unchanged"]["manifest_authorized"] is False,
                "G2B receipt zero credit")
        c19c = views["c19c_endpoint_v3_receipt"].document(canonical_file=False)
        require(c19c["authority"]["direct_rule"]
                == "oriented [lower,upper) on internal faces"
                and c19c["source_W_transition_authorized"] is False
                and c19c["formal_credit"] == 0,
                "C19C half-open authority")
        g2a_authority = views["g2a_scoped_result"].document()
        require(g2a_authority["status"].endswith(
                    "POSITIVE_C19_OPEN__CAPTURED_SOURCE_EXECUTION_BOUND__ZERO_CREDIT"
                )
                and g2a_authority["global_three_terminal_unique_assignment"] is False
                and g2a_authority["formal_credit"] == 0,
                "G2A source-exec-bound scoped authority")
        dual_current = views["current_dual_seed_authority"].document()
        require(dual_current["primary_priority_ledgers_byte_identical"] is True
                and dual_current["primary_positive_ledgers_byte_identical"] is True
                and dual_current["priority_ledger_sha256"]
                    == views["current_routes"].sha256
                    == views["current_seed2_routes"].sha256
                and dual_current["formal_credit"] == 0,
                "current dual-seed normalized authority")

        a_positive: dict[tuple[str, str], dict[str, Any]] = {}
        a_graph_pairs: set[tuple[str, str]] = set()
        a_edges_derived: set[tuple[str, str]] = set()
        for row in views["g2a_contacts"].jsonl():
            authority_key = pair(row["positive_side_member_id"], row["target_member_id"])
            require(authority_key not in a_positive, "G2A positive authority uniqueness")
            require(row["formal_credit"] == 0
                    and row["g2a_component_id"] == row["positive_side_component_id"],
                    "G2A alias semantics")
            a_positive[authority_key] = row
            a_graph_pairs.add(pair(row["g2a_member_id"], row["target_member_id"]))
            if row["g2a_component_id"] != row["target_component_id"]:
                a_edges_derived.add(pair(row["g2a_component_id"], row["target_component_id"]))
        require(len(a_positive) == len(a_graph_pairs) == 9_408, "G2A positive census")

        a_empty: dict[tuple[str, str], dict[str, Any]] = {}
        for row in views["g2a_reverse_empty"].jsonl():
            authority_key = pair(row["empty_reverse_side_member_id"], row["target_member_id"])
            require(authority_key not in a_empty, "G2A empty authority uniqueness")
            a_empty[authority_key] = row
        require(len(a_empty) == 9_392 and not (set(a_positive) & set(a_empty)),
                "G2A positive/empty partition")

        a_edges_published: set[tuple[str, str]] = set()
        for row in views["g2a_edges"].jsonl():
            value = edge(row["unordered_component_pair"], "G2A edge")
            require(value not in a_edges_published, "G2A edge uniqueness")
            a_edges_published.add(value)
        require(a_edges_published == a_edges_derived and len(a_edges_published) == 144,
                "G2A edge equality")

        b_positive: dict[tuple[str, str], dict[str, Any]] = {}
        b_empty: dict[tuple[str, str], dict[str, Any]] = {}
        b_edges_derived: set[tuple[str, str]] = set()
        for row in views["g2b_exact"].jsonl():
            authority_key = pair(row["c24_member_id"], row["target_member_id"])
            destination = (b_positive if row["disposition"] == "EXACT_POSITIVE_SUPPORT"
                           else b_empty)
            require(row["disposition"] in {"EXACT_POSITIVE_SUPPORT", "EXACT_EMPTY_INTERSECTION"}
                    and authority_key not in b_positive and authority_key not in b_empty,
                    "G2B exact partition")
            destination[authority_key] = row
            components = row["current_C15_components"]
            if destination is b_positive and components[0] != components[1]:
                b_edges_derived.add(pair(components[0], components[1]))
        require(len(b_positive) == 9_408 and len(b_empty) == 9_392,
                "G2B exact census")
        require(set(a_positive) == set(b_positive) and set(a_empty) == set(b_empty),
                "G2A/G2B authority pair equality")

        b_priority: dict[tuple[str, str], dict[str, Any]] = {}
        for row in views["g2b_priority"].jsonl():
            authority_key = pair(row["left_member_id"], row["right_member_id"])
            require(authority_key not in b_priority
                    and row["assigned_terminal"] == "C24A_G2B_EXACT_FACTOR_SIGN_POSITIVE"
                    and not row["raw_signed_exact_pair"]
                    and not row["raw_complete_exact_pair"], "G2B priority semantics")
            b_priority[authority_key] = row
        require(set(b_priority) == set(b_positive), "G2B exact/priority equality")

        b_edges_published: set[tuple[str, str]] = set()
        for row in views["g2b_edges"].jsonl():
            value = edge(row["ordered_C15_component_pair"], "G2B edge")
            require(value not in b_edges_published, "G2B edge uniqueness")
            b_edges_published.add(value)
        require(b_edges_published == b_edges_derived == a_edges_published,
                "G2A/G2B edge equality")

        current: dict[tuple[str, str], dict[str, Any]] = {}
        by_terminal: dict[str, set[tuple[str, str]]] = defaultdict(set)
        current_edges: set[tuple[str, str]] = set()
        edge_terminal_rows: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
        for row in views["current_routes"].jsonl():
            route_key = pair(row["left_member_id"], row["right_member_id"])
            require(route_key not in current, "current route uniqueness")
            current[route_key] = row
            terminal_name = row["assigned_terminal"]
            by_terminal[terminal_name].add(route_key)
            components = row["current_C15_components"]
            if components[0] != components[1]:
                value = pair(components[0], components[1])
                current_edges.add(value)
                edge_terminal_rows[value][terminal_name] += 1
        require({name: len(keys) for name, keys in by_terminal.items()} == {
            "SIGNED_BOUNDARY_FACES": 25_452,
            "COMPLETE_BOUNDARY_FACES": 10_688,
            "POSITIVE_VOLUME_CARRIERS": 55_532,
        } and len(current) == 91_672 and len(current_edges) == 14_620,
                "current census")
        require(not (set(b_positive) & set(current))
                and not (set(b_empty) & set(current))
                and not (a_graph_pairs & set(current)), "C24A/current disjointness")

        strict_edges: set[tuple[str, str]] = set()
        for row in views["strict_validation_edges"].jsonl():
            value = edge(row["ordered_round306c15_component_pair"], "strict edge")
            require(value not in strict_edges, "strict validation edge uniqueness")
            strict_edges.add(value)
        require(len(strict_edges) == 14_772 and current_edges <= strict_edges
                and b_edges_published <= strict_edges, "strict validation containment")

        candidate_pairs = set(current) | set(b_priority)
        candidate_edges = current_edges | b_edges_published
        contributors = addition_contributors(current_edges, b_edges_published)
        require(len(candidate_pairs) == 101_080 and len(candidate_edges) == 14_724
                and len(current_edges & b_edges_published) == 40
                and len(contributors) == 104, "union and rank census")

        comparator_dir = Path(args.comparator_result).resolve().parent
        output_views: dict[str, FileView] = {}
        ledger_key_to_label = {
            "C24A_key_comparison": "key_comparison",
            "unique_ownership": "ownership",
            "cross_C15_edge_union": "edge_union",
        }
        try:
            for ledger_key, label in ledger_key_to_label.items():
                descriptor = result["ledgers"][ledger_key]
                output_views[label] = FileView.acquire(
                    label,
                    comparator_dir / descriptor["filename"],
                    descriptor["file_sha256"],
                )
                require(ledger_descriptor(output_views[label]) == descriptor,
                        label + ":descriptor")

            seen_key_rows: set[tuple[str, str]] = set()
            disposition_count: Counter[str] = Counter()
            for row in output_views["key_comparison"].jsonl():
                authority_key = edge(row["authority_pair_key"], "key comparison pair")
                require(authority_key not in seen_key_rows, "key comparison uniqueness")
                seen_key_rows.add(authority_key)
                positive = authority_key in b_positive
                source_a = a_positive[authority_key] if positive else a_empty[authority_key]
                source_b = b_positive[authority_key] if positive else b_empty[authority_key]
                require(row["formal_credit"] == 0
                        and row["disposition"] == source_b["disposition"]
                        and row["g2a_diagnostic_row_sha256"] == source_a["row_sha256"]
                        and row["g2b_exact_row_sha256"] == source_b["row_sha256"]
                        and row["included_in_scoped_candidate_union"] is positive
                        and row["current_assigned_terminal"] is None,
                        "key comparison source binding")
                expected_priority = b_priority[authority_key]["row_sha256"] if positive else None
                require(row["g2b_priority_row_sha256"] == expected_priority,
                        "key comparison priority binding")
                disposition_count[row["disposition"]] += 1
            require(seen_key_rows == set(b_positive) | set(b_empty)
                    and disposition_count == {
                        "EXACT_POSITIVE_SUPPORT": 9_408,
                        "EXACT_EMPTY_INTERSECTION": 9_392,
                    }, "key comparison totality")

            seen_ownership: set[tuple[str, str]] = set()
            terminal_count: Counter[str] = Counter()
            branch_count: Counter[str] = Counter()
            for row in output_views["ownership"].jsonl():
                route_key = edge(row["pair_key"], "ownership pair")
                require(route_key not in seen_ownership, "ownership uniqueness")
                seen_ownership.add(route_key)
                require(row["formal_credit"] == 0, "ownership zero credit")
                if route_key in current:
                    source = current[route_key]
                    expected_terminal = source["assigned_terminal"]
                    expected_branch = (
                        "CURRENT_C19_PHYSICAL_SUPPORT"
                        if expected_terminal == "POSITIVE_VOLUME_CARRIERS" else None
                    )
                    require(row["source_row_sha256"] == source["row_sha256"]
                            and row["current_source_terminal"] == source["assigned_terminal"]
                            and row["C24A_G2B_exact_row_sha256"] is None
                            and row["G2A_diagnostic_alias_row_sha256"] is None,
                            "current ownership binding")
                else:
                    require(route_key in b_priority, "C24 ownership source")
                    expected_terminal = "POSITIVE_VOLUME_CARRIERS"
                    expected_branch = (
                        "C24A_G2B_EXACT_FACTOR_SIGN_POSITIVE_WITH_G2A_RELATIVE_BOUNDARY_DIAGNOSTIC"
                    )
                    require(row["source_row_sha256"] == b_priority[route_key]["row_sha256"]
                            and row["C24A_G2B_exact_row_sha256"]
                                == b_positive[route_key]["row_sha256"]
                            and row["G2A_diagnostic_alias_row_sha256"]
                                == a_positive[route_key]["row_sha256"],
                            "C24 ownership binding")
                require(row["assigned_terminal"] == expected_terminal
                        and row["positive_support_branch"] == expected_branch,
                        "ownership terminal/branch")
                terminal_count[expected_terminal] += 1
                if expected_branch is not None:
                    branch_count[expected_branch] += 1
            require(seen_ownership == candidate_pairs and terminal_count == {
                "SIGNED_BOUNDARY_FACES": 25_452,
                "COMPLETE_BOUNDARY_FACES": 10_688,
                "POSITIVE_VOLUME_CARRIERS": 64_940,
            } and branch_count == {
                "CURRENT_C19_PHYSICAL_SUPPORT": 55_532,
                "C24A_G2B_EXACT_FACTOR_SIGN_POSITIVE_WITH_G2A_RELATIVE_BOUNDARY_DIAGNOSTIC": 9_408,
            }, "ownership totality")

            seen_edges: set[tuple[str, str]] = set()
            for row in output_views["edge_union"].jsonl():
                value = edge(row["unordered_component_pair"], "edge union pair")
                require(value not in seen_edges, "edge union uniqueness")
                seen_edges.add(value)
                expected_rows = dict(sorted(edge_terminal_rows.get(value, Counter()).items()))
                require(row["formal_credit"] == 0
                        and row["present_in_current_support_primitive"]
                            is (value in current_edges)
                        and row["current_cross_pair_row_census_by_terminal"] == expected_rows
                        and row["present_in_G2A_scoped_authority"]
                            is (value in a_edges_published)
                        and row["present_in_G2B_terminal_authority"]
                            is (value in b_edges_published)
                        and row["novel_against_current_support"]
                            is (value in (b_edges_published - current_edges))
                        and row["incremental_rank_contribution_after_current_support"]
                            is (value in contributors)
                        and row["present_in_strict_volume_validation_only_set"] is True
                        and row["strict_volume_used_as_candidate_source"] is False,
                        "edge union semantics")
            require(seen_edges == candidate_edges, "edge union totality")
        finally:
            for view in output_views.values():
                view.release()

        expected_current_rank = rank_data(current_edges)
        expected_c24_rank = rank_data(b_edges_published)
        expected_union_rank = rank_data(candidate_edges)
        expected_strict_rank = rank_data(strict_edges)
        summary = result["cross_C15_edge_overlap_and_rank"]
        require(summary["current_graph"] == expected_current_rank
                and summary["C24A_graph"] == expected_c24_rank
                and summary["candidate_union_graph"] == expected_union_rank
                and summary["strict_volume_validation"]["graph"] == expected_strict_rank,
                "result rank summaries")
        key_summary = result["C24A_G2A_G2B_key_by_key"]
        require(key_summary["G2A_positive_contact_keys"] == 9_408
                and key_summary["G2B_exact_positive_keys"] == 9_408
                and key_summary["positive_key_intersection"] == 9_408
                and key_summary["positive_G2A_only"] == 0
                and key_summary["positive_G2B_only"] == 0
                and key_summary["G2A_reverse_empty_keys"] == 9_392
                and key_summary["G2B_exact_empty_keys"] == 9_392
                and key_summary["empty_key_intersection"] == 9_392
                and key_summary["empty_G2A_only"] == 0
                and key_summary["empty_G2B_only"] == 0
                and key_summary["G2B_exact_positive_equals_G2B_priority"] is True
                and key_summary["G2A_G2B_positive_empty_cross_intersections"] == 0,
                "result key summary")
        intersections = result["pair_intersections_with_current_by_terminal"]
        require(all(value == 0
                    for section in intersections.values()
                    for value in section.values()), "result pair intersections")
        union_summary = result["scoped_candidate_union"]
        require(union_summary["current_support_pair_count"] == 91_672
                and union_summary["C24A_G2B_positive_pair_count"] == 9_408
                and union_summary["C24A_G2B_empty_excluded_count"] == 9_392
                and union_summary["current_intersection_C24A_positive"] == 0
                and union_summary["current_intersection_C24A_empty"] == 0
                and union_summary["union_pair_count"] == 101_080
                and union_summary["unique_ownership_row_count"] == 101_080
                and union_summary["normalized_terminal_census"] == {
                    "SIGNED_BOUNDARY_FACES": 25_452,
                    "COMPLETE_BOUNDARY_FACES": 10_688,
                    "POSITIVE_VOLUME_CARRIERS": 64_940,
                }
                and union_summary["G2A_graph_alias_counted_as_independent_candidate"] is False
                and union_summary["scoped_unique_assignment_closed"] is True,
                "result scoped union summary")
        governance = result["candidate_governance"]
        require(governance["G2A_scoped_authority_role"]
                    == "DIAGNOSTIC_ALIAS_AND_KEY_CROSSWALK_ONLY"
                and governance["strict_volume_edge_role"]
                    == "POST_CONSTRUCTION_VALIDATION_ONLY"
                and governance["historical_edge_ledger_used_as_candidate_universe"] is False
                and governance["C19C_endpoint_v3_used_as_candidate_source"] is False
                and governance["C27_FAMILIES_imported_or_read"] is False
                and governance["old_transition_ledger_imported_or_read"] is False
                and governance["C28_imported_or_read"] is False
                and governance["C29_imported_or_read"] is False
                and governance["producer_module_imported"] is False,
                "result candidate governance")
        gate = result["global_claim_gate"]
        require(gate["primitive_support_atom_denominator"] == 483_232
                and gate["atom_to_pair_incidence_ledger_materialized_here"] is False
                and gate["atom_without_pair_complement_census_materialized_here"] is False
                and gate["current_only_atom_incidence_count"] == 62_240
                and gate["current_only_atom_complement_count"] == 420_992
                and gate["current_only_complement_accepted_as_global_complement"] is False
                and gate["C24A_G2B_positive_C22_target_atom_incidence_joined"] is False
                and gate["C24A_G2B_positive_pair_count_requiring_atom_join"] == 9_408
                and gate["C24A_atom_terminal_normalization"]
                    == "G2B_POSITIVE_VOLUME_CARRIERS__G2A_ALIAS_NO_SECOND_ASSIGNMENT"
                and gate["C24A_same_chart_positive_double_count_forbidden"] is True
                and gate["full_union_atom_join_required"] is True
                and gate["primitive_row_bound_terminal_selection_exhaustive"] is False
                and gate["primitive_row_bound_terminal_selection_mutually_exclusive"] is False
                and gate["pair_routing_total_on_483232_atom_denominator"] is False
                and gate["global_candidate_totality_proved"] is False
                and gate["global_unique_assignment_proved"] is False
                and gate["decision"] == "FAIL_CLOSED_NO_PROMOTION",
                "global atom-denominator fail-closed gate")
        require(result["formal_credit"] == 0
                and result["manifest_authorized"] is False
                and result["strict_nonpromotion"] == {
                    "C27_transition_totality": 0,
                    "C28_pair_routing": 0,
                    "C29_physical_maximality": 0,
                    "CM2": "NO-GO_FOR_CLAIM",
                }, "result zero-credit nonpromotion")

        verifier_source_sha = disk_hash(Path(__file__).resolve())
        body = {
            "schema": "cm2.c27-independent.c24a-current-primitive-three-terminal-union-verification.v1",
            "status": (
                "PASS_NO_PRODUCER_IMPORT_INDEPENDENT_RECONSTRUCTION__"
                "SCOPED_101080_UNION__GLOBAL_TOTALITY_FAIL_CLOSED__ZERO_CREDIT"
            ),
            "verification_seed": args.seed,
            "reconstructed": {
                "G2A_G2B_positive_key_intersection": len(set(a_positive) & set(b_positive)),
                "G2A_G2B_empty_key_intersection": len(set(a_empty) & set(b_empty)),
                "current_C24A_positive_pair_intersection": len(set(current) & set(b_positive)),
                "scoped_candidate_union": len(candidate_pairs),
                "unique_ownership": len(candidate_pairs),
                "current_edges": len(current_edges),
                "C24A_edges": len(b_edges_published),
                "edge_overlap": len(current_edges & b_edges_published),
                "edge_union": len(candidate_edges),
                "incremental_rank_reduction": len(contributors),
            },
            "implementation_independence": {
                "comparator_or_producer_module_imported": False,
                "workspace_module_imported": False,
                "stdlib_only": True,
                "verifier_source_sha256": verifier_source_sha,
            },
            "global_gate": {
                "primitive_support_atom_denominator": 483_232,
                "atom_to_pair_incidence_totality_verified": False,
                "decision": "FAIL_CLOSED_NO_PROMOTION",
            },
            "formal_credit": 0,
            "manifest_authorized": False,
            "strict_nonpromotion": result["strict_nonpromotion"],
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {name: view.receipt() for name, view in sorted(views.items())},
            },
        }
        verification = dict(body)
        verification["semantic_projection_sha256"] = object_hash({
            key: value for key, value in body.items()
            if key not in {"verification_seed", "root_input_capture"}
        })
        verification["verification_sha256"] = object_hash(verification)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(encode(verification) + b"\n")
        return verification
    finally:
        for view in views.values():
            view.release()


def add_root(parser: argparse.ArgumentParser, name: str) -> None:
    parser.add_argument("--" + name, required=True)
    parser.add_argument("--" + name + "-sha256", required=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    for name in (
        "g2a-contacts",
        "g2a-reverse-empty",
        "g2a-edges",
        "g2a-scoped-result",
        "g2b-terminal-receipt",
        "g2b-exact",
        "g2b-priority",
        "g2b-edges",
        "current-routes",
        "current-seed2-routes",
        "current-dual-seed-authority",
        "c19c-endpoint-v3-receipt",
        "strict-validation-edges",
        "comparator-result",
    ):
        add_root(parser, name)
    parser.add_argument("--out-file", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    try:
        verification = verify(args)
    except (Reject, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(encode({
        "status": verification["status"],
        "semantic_projection_sha256": verification["semantic_projection_sha256"],
        "verification_sha256": verification["verification_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
