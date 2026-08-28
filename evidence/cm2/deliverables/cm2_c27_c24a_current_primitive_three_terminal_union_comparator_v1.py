#!/usr/bin/env python3
"""Primitive-only C24A/current-support scoped union comparator.

The candidate universe is built only from the current-support priority ledger
and the terminal-authorized C24A G2B positive-priority ledger.  G2A r3 rows
are diagnostic aliases: they prove the positive-side/reverse-side key
crosswalk but never add a second candidate.  The historical strict-volume
edge ledger is accepted only as an after-the-fact component-edge validation
set and is structurally excluded from candidate construction.

This is deliberately a zero-credit, fail-closed diagnostic.  It does not read
or import C27 FAMILIES, a transition ledger, C28, or C29.
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
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent.parent


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def closed(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "fresh closed row")
    return {**body, "row_sha256": digest(body)}


def check_closed(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label + ":row closure")


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
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
class Capture:
    label: str
    path: Path
    fd: int
    pre: tuple[int, ...]
    sha256: str

    @classmethod
    def open(cls, label: str, path: Path, expected: str) -> "Capture":
        need(type(expected) is str and len(expected) == 64, label + ":expected sha")
        resolved = path.resolve()
        fd = os.open(
            resolved,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        )
        try:
            before = os.fstat(fd)
            need(stat.S_ISREG(before.st_mode), label + ":regular file")
            state = hashlib.sha256()
            while block := os.read(fd, 4 << 20):
                state.update(block)
            observed = state.hexdigest()
            need(observed == expected, label + ":file sha256")
            need(fingerprint(os.fstat(fd)) == fingerprint(before), label + ":hash fstat")
            os.lseek(fd, 0, os.SEEK_SET)
            return cls(label, resolved, fd, fingerprint(before), observed)
        except BaseException:
            os.close(fd)
            raise

    def unchanged(self, phase: str) -> None:
        need(fingerprint(os.fstat(self.fd)) == self.pre, self.label + ":" + phase + ":fstat")

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        pieces: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            pieces.append(block)
        self.unchanged("raw")
        return b"".join(pieces)

    def document(self, require_canonical: bool = True) -> dict[str, Any]:
        raw = self.raw()
        value = json.loads(raw)
        need(type(value) is dict, self.label + ":document object")
        if require_canonical:
            need(canonical(value) + b"\n" == raw, self.label + ":canonical")
        body = dict(value)
        closure_keys = [key for key in ("result_sha256", "receipt_sha256") if key in body]
        need(len(closure_keys) == 1, self.label + ":single document closure key")
        closure_key = closure_keys[0]
        claimed = body.pop(closure_key)
        need(type(claimed) is str and claimed == digest(body), self.label + ":document closure")
        return value

    def rows(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    need(line.endswith(b"\n"), f"{self.label}:{ordinal}:newline")
                    encoded = line[:-1]
                    row = json.loads(encoded)
                    need(type(row) is dict and canonical(row) == encoded,
                         f"{self.label}:{ordinal}:canonical")
                    check_closed(row, f"{self.label}:{ordinal}")
                    yield row
        self.unchanged("rows")

    def attestation(self) -> dict[str, Any]:
        self.unchanged("attestation")
        try:
            rendered = str(self.path.relative_to(ROOT))
        except ValueError:
            rendered = str(self.path)
        return {
            "path": rendered,
            "sha256": self.sha256,
            "size": self.pre[2],
            "stat_fingerprint": list(self.pre),
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
        }

    def close(self) -> None:
        os.close(self.fd)


def unordered(left: str, right: str) -> tuple[str, str]:
    need(type(left) is str and type(right) is str and left != right, "nonself pair")
    return (left, right) if left < right else (right, left)


def component_edge(values: Any, label: str) -> tuple[str, str]:
    need(type(values) is list and len(values) == 2
         and all(type(item) is str for item in values), label + ":component pair")
    return unordered(values[0], values[1])


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def write_rows(path: Path, rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    count = 0
    sequence = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as stream:
            for row in rows:
                check_closed(row, path.name + f":{count}")
                stream.write(canonical(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
                count += 1
    return {
        "filename": path.name,
        "row_count": count,
        "file_sha256": file_sha(path),
        "row_sequence_sha256": sequence.hexdigest(),
    }


class DSU:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}
        self.rank_reduction = 0

    def find(self, item: str) -> str:
        self.parent.setdefault(item, item)
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, left: str, right: str) -> bool:
        a, b = self.find(left), self.find(right)
        if a == b:
            return False
        self.parent[b] = a
        self.rank_reduction += 1
        return True


def dsu_stats(edges: set[tuple[str, str]]) -> dict[str, int]:
    dsu = DSU()
    cycle_edges = 0
    for left, right in sorted(edges):
        if not dsu.union(left, right):
            cycle_edges += 1
    return {
        "edge_count": len(edges),
        "vertex_count": len(dsu.parent),
        "rank_reduction": dsu.rank_reduction,
        "cycle_edge_count": cycle_edges,
        "component_count_on_incident_vertices": len(dsu.parent) - dsu.rank_reduction,
    }


def incremental_rank(
    base: set[tuple[str, str]], additions: set[tuple[str, str]]
) -> tuple[int, set[tuple[str, str]]]:
    dsu = DSU()
    for left, right in sorted(base):
        dsu.union(left, right)
    before = dsu.rank_reduction
    contributing: set[tuple[str, str]] = set()
    for left, right in sorted(additions):
        if dsu.union(left, right):
            contributing.add((left, right))
    return dsu.rank_reduction - before, contributing


def terminal_intersections(
    pairs: set[tuple[str, str]], current_by_terminal: dict[str, set[tuple[str, str]]]
) -> dict[str, int]:
    return {terminal: len(pairs & terminal_pairs)
            for terminal, terminal_pairs in sorted(current_by_terminal.items())}


def validate_terminal_receipt(
    receipt: dict[str, Any], captures: dict[str, Capture]
) -> None:
    need(receipt["schema"] == "cm2.c27-independent.c24a-g2b-terminal-zero-credit.v1",
         "G2B terminal receipt schema")
    need(receipt["status"] == "PASS_TERMINAL_DIAGNOSTIC_C24A_G2B_EXACT_ROUTE__ZERO_FORMAL_CREDIT",
         "G2B terminal receipt status")
    need(receipt["G2B_closed_diagnostic"] == {
        "candidate_pairs": 18_800,
        "cross_current_C15_positive_member_pairs": 596,
        "edges_already_in_C27R1D": 144,
        "exact_empty": 9_392,
        "exact_positive": 9_408,
        "incremental_rank_reduction_after_C27R1D": 0,
        "new_component_edges_after_C27R1D": 0,
        "unique_old_C15_component_edges": 144,
        "unresolved": 0,
    }, "G2B terminal receipt census")
    state = receipt["formal_state_unchanged"]
    need(state["formal_credit"] == 0 and state["manifest_authorized"] is False
         and state["C27_transition_totality"] == 0
         and state["C28_pair_routing"] == 0
         and state["C29_physical_maximality"] == 0
         and state["CM2"] == "NO-GO_FOR_CLAIM", "G2B zero-credit authority")
    authorities = receipt["root_input_capture"]["authorities"]
    mapping = {
        "primary_seed1_ledger": "g2b_exact",
        "priority_ledger": "g2b_priority",
        "edge_ledger": "g2b_edges",
    }
    for authority_label, capture_label in mapping.items():
        authority = authorities[authority_label]
        capture = captures[capture_label]
        need((ROOT / authority["path"]).resolve() == capture.path,
             authority_label + ":authorized path")
        need(authority["sha256"] == capture.sha256,
             authority_label + ":authorized sha256")


def validate_g2a_scoped_result(
    result: dict[str, Any], captures: dict[str, Capture]
) -> None:
    need(result["schema"]
             == "cm2.c27-independent.g2a-relative2d-primitive-totality-theorem.v2"
         and result["status"].endswith(
             "POSITIVE_C19_OPEN__CAPTURED_SOURCE_EXECUTION_BOUND__ZERO_CREDIT"
         ), "G2A source-exec-bound scoped authority")
    need(result["formal_credit"] == 0
         and result["global_three_terminal_unique_assignment"] is False
         and result["positive_C19_91672_intersection_gate"]
             == "OPEN__FRESH_LEDGER_NOT_CONSUMED_BY_THIS_THEOREM"
         and result["strict_nonpromotion"] == {
             "C27_transition_totality": 0,
             "C28_pair_routing": 0,
             "C29_physical_maximality": 0,
             "CM2": "NO-GO_FOR_CLAIM",
         }, "G2A scoped nonpromotion")
    mapping = {
        "contacts": "g2a_contacts",
        "reverse_empty": "g2a_reverse_empty",
        "unique_cross_C15_component_edges": "g2a_edges",
    }
    for ledger_key, capture_key in mapping.items():
        descriptor = result["ledgers"][ledger_key]
        capture = captures[capture_key]
        need((captures["g2a_scoped_result"].path.parent / descriptor["filename"]).resolve()
                 == capture.path,
             "G2A " + ledger_key + ":authorized path")
        need(descriptor["file_sha256"] == capture.sha256,
             "G2A " + ledger_key + ":authorized sha256")


def validate_c19c_half_open_receipt(receipt: dict[str, Any]) -> None:
    need(receipt["schema"] == "cm2.c19c-endpoint-ownership-v3.terminal-receipt.v1"
         and receipt["status"]
             == "PASS_APPEND_ONLY_V3_AUTHORITY_DUAL_SEED_DUAL_VERIFIER_ATTACK_SEALED",
         "C19C endpoint-v3 receipt authority")
    need(receipt["formal_credit"] == 0
         and receipt["source_W_transition_authorized"] is False
         and receipt["C27_C28_C29"] == "UNAUTHORIZED_PENDING_REBUILD"
         and receipt["CM2"] == "NO-GO_FOR_CLAIM",
         "C19C endpoint-v3 nonpromotion")
    authority = receipt["authority"]
    need(authority["direct_rule"] == "oriented [lower,upper) on internal faces"
         and authority["closed_physical_outer_rule"]
             == "both p endpoints and both s endpoints included"
         and authority["source_chart_seam_rule"] == "E or W owns; N or S excludes",
         "C19C half-open boundary policy")


def validate_current_dual_seed_authority(
    authority: dict[str, Any], captures: dict[str, Capture]
) -> None:
    need(authority["schema"]
             == "cm2.c27-independent.current-support-91672.dual-seed-comparison.v1"
         and authority["status"]
             == "PASS_EXACT_WHITELISTED_NORMALIZATION_AND_BYTE_IDENTICAL_LEDGERS__ZERO_CREDIT"
         and authority["formal_credit"] == 0
         and authority["manifest_authorized"] is False
         and authority["primary_priority_ledgers_byte_identical"] is True
         and authority["primary_positive_ledgers_byte_identical"] is True
         and authority["priority_ledger_sha256"] == captures["current_routes"].sha256
             == captures["current_seed2_routes"].sha256
         and authority["CM2"] == "NO-GO_FOR_CLAIM",
         "current-support dual-seed normalized authority")
    attestations = authority["root_input_capture"]["attestations"]
    for authority_key, capture_key in (
        ("seed1_priority", "current_routes"),
        ("seed2_priority", "current_seed2_routes"),
    ):
        item = attestations[authority_key]
        capture = captures[capture_key]
        need((ROOT / item["path"]).resolve() == capture.path
             and item["sha256"] == capture.sha256,
             "current " + authority_key + ":path/sha authority")


def parse_g2a(
    captures: dict[str, Capture],
) -> tuple[
    dict[tuple[str, str], dict[str, Any]],
    dict[tuple[str, str], dict[str, Any]],
    set[tuple[str, str]],
    dict[str, Any],
]:
    contacts_by_authority_pair: dict[tuple[str, str], dict[str, Any]] = {}
    contacts_by_semantic_key: dict[tuple[str, str], dict[str, Any]] = {}
    graph_endpoint_pairs: set[tuple[str, str]] = set()
    derived_edges: set[tuple[str, str]] = set()
    cross_rows = 0
    for ordinal, row in enumerate(captures["g2a_contacts"].rows()):
        label = f"G2A contact:{ordinal}"
        need(row["schema"] == "cm2.c27-independent.g2a-relative2d.exact-contact-alias-route.row.v2",
             label + ":schema")
        need(row["formal_credit"] == 0
             and row["assigned_unique_terminal"] == "SAME_CHART_RELATIVE_CELLS"
             and row["g2a_and_positive_side_same_C15_component"] is True
             and not row["raw_SIGNED_pair"] and not row["raw_COMPLETE_pair"]
             and not row["raw_positive_side_SIGNED_pair"]
             and not row["raw_positive_side_COMPLETE_pair"], label + ":scoped semantics")
        semantic_key = (row["graph_id"], row["target_member_id"])
        authority_pair = unordered(row["positive_side_member_id"], row["target_member_id"])
        graph_pair = unordered(row["g2a_member_id"], row["target_member_id"])
        need(semantic_key not in contacts_by_semantic_key, label + ":semantic uniqueness")
        need(authority_pair not in contacts_by_authority_pair, label + ":authority uniqueness")
        need(graph_pair not in graph_endpoint_pairs, label + ":graph endpoint uniqueness")
        contacts_by_semantic_key[semantic_key] = row
        contacts_by_authority_pair[authority_pair] = row
        graph_endpoint_pairs.add(graph_pair)
        need(row["g2a_component_id"] == row["positive_side_component_id"],
             label + ":component alias")
        if row["g2a_component_id"] != row["target_component_id"]:
            cross_rows += 1
            derived_edges.add(unordered(row["g2a_component_id"], row["target_component_id"]))
    need(len(contacts_by_semantic_key) == len(contacts_by_authority_pair)
         == len(graph_endpoint_pairs) == 9_408, "G2A contact census")

    reverse_by_authority_pair: dict[tuple[str, str], dict[str, Any]] = {}
    reverse_semantic_keys: set[tuple[str, str]] = set()
    for ordinal, row in enumerate(captures["g2a_reverse_empty"].rows()):
        label = f"G2A reverse empty:{ordinal}"
        need(row["schema"] == "cm2.c27-independent.g2a-relative2d.reverse-side-empty-binding.row.v2"
             and row["formal_credit"] == 0
             and row["unique_positive_side_among_envelope_candidates"] is True,
             label + ":schema/semantics")
        semantic_key = (row["graph_id"], row["target_member_id"])
        authority_pair = unordered(row["empty_reverse_side_member_id"], row["target_member_id"])
        need(semantic_key in contacts_by_semantic_key, label + ":positive semantic parent")
        parent = contacts_by_semantic_key[semantic_key]
        need(row["g2a_member_id"] == parent["g2a_member_id"]
             and row["positive_side_member_id"] == parent["positive_side_member_id"]
             and row["positive_factor_row_sha256"]
                 == parent["positive_factor_disposition_row_sha256"],
             label + ":positive parent binding")
        need(semantic_key not in reverse_semantic_keys, label + ":semantic uniqueness")
        need(authority_pair not in reverse_by_authority_pair, label + ":authority uniqueness")
        reverse_semantic_keys.add(semantic_key)
        reverse_by_authority_pair[authority_pair] = row
    need(len(reverse_by_authority_pair) == len(reverse_semantic_keys) == 9_392,
         "G2A reverse-empty census")
    need(not (set(contacts_by_authority_pair) & set(reverse_by_authority_pair)),
         "G2A positive/reverse authority pair disjointness")

    published_edges: set[tuple[str, str]] = set()
    for ordinal, row in enumerate(captures["g2a_edges"].rows()):
        label = f"G2A edge:{ordinal}"
        need(row["schema"] == "cm2.c27-independent.g2a-relative2d.unique-cross-c15-component-edge.row.v2"
             and row["formal_credit"] == 0, label + ":schema/credit")
        edge = component_edge(row["unordered_component_pair"], label)
        need(row["component_a"] == edge[0] and row["component_b"] == edge[1]
             and row["unique_edge_key"] == edge[0] + "|" + edge[1], label + ":edge key")
        need(edge not in published_edges, label + ":unique")
        published_edges.add(edge)
    need(cross_rows == 596 and len(derived_edges) == 144
         and published_edges == derived_edges, "G2A cross-component edge derivation")
    return (
        contacts_by_authority_pair,
        reverse_by_authority_pair,
        published_edges,
        {
            "semantic_contact_key_count": len(contacts_by_semantic_key),
            "reverse_semantic_key_count": len(reverse_semantic_keys),
            "single_side_no_reverse_count": len(set(contacts_by_semantic_key) - reverse_semantic_keys),
            "graph_endpoint_pairs": graph_endpoint_pairs,
            "cross_contact_row_count": cross_rows,
        },
    )


def parse_g2b(
    captures: dict[str, Capture],
) -> tuple[
    dict[tuple[str, str], dict[str, Any]],
    dict[tuple[str, str], dict[str, Any]],
    dict[tuple[str, str], dict[str, Any]],
    set[tuple[str, str]],
]:
    positive: dict[tuple[str, str], dict[str, Any]] = {}
    empty: dict[tuple[str, str], dict[str, Any]] = {}
    derived_edges: set[tuple[str, str]] = set()
    cross_positive = 0
    for ordinal, row in enumerate(captures["g2b_exact"].rows()):
        label = f"G2B exact:{ordinal}"
        need(row["formal_credit"] == 0, label + ":credit")
        pair = unordered(row["c24_member_id"], row["target_member_id"])
        need(pair not in positive and pair not in empty, label + ":unique pair")
        need(row["disposition"] in {"EXACT_POSITIVE_SUPPORT", "EXACT_EMPTY_INTERSECTION"},
             label + ":disposition")
        expected_positive = row["disposition"] == "EXACT_POSITIVE_SUPPORT"
        need((row["signed_factor_value_on_target_open_box"]
              == row["predicate_required_sign"]) is expected_positive,
             label + ":factor sign/disposition")
        target = positive if expected_positive else empty
        target[pair] = row
        components = row["current_C15_components"]
        need(type(components) is list and len(components) == 2
             and row["current_C15_components_equal"] is (components[0] == components[1]),
             label + ":components")
        if expected_positive and components[0] != components[1]:
            cross_positive += 1
            derived_edges.add(unordered(components[0], components[1]))
    need(len(positive) == 9_408 and len(empty) == 9_392
         and not (set(positive) & set(empty)), "G2B 9408/9392 exact partition")
    need(cross_positive == 596 and len(derived_edges) == 144,
         "G2B cross-positive edge derivation")

    priority: dict[tuple[str, str], dict[str, Any]] = {}
    for ordinal, row in enumerate(captures["g2b_priority"].rows()):
        label = f"G2B priority:{ordinal}"
        need(row["schema"] == "cm2.audit.c24a-positive-priority-disposition.row.v1"
             and row["formal_credit"] == 0
             and row["assigned_terminal"] == "C24A_G2B_EXACT_FACTOR_SIGN_POSITIVE"
             and row["priority_rule"]
                 == "SIGNED_THEN_COMPLETE_THEN_C24A_G2B_EXACT_FACTOR_SIGN_POSITIVE"
             and row["raw_signed_exact_pair"] is False
             and row["raw_complete_exact_pair"] is False,
             label + ":semantics")
        pair = unordered(row["left_member_id"], row["right_member_id"])
        need(pair not in priority, label + ":unique")
        priority[pair] = row
    need(set(priority) == set(positive), "G2B exact-positive/priority key equality")

    published_edges: set[tuple[str, str]] = set()
    for ordinal, row in enumerate(captures["g2b_edges"].rows()):
        label = f"G2B edge:{ordinal}"
        need(row["schema"] == "cm2.audit.c24a-cross-positive-unique-component-edge.row.v1"
             and row["formal_credit"] == 0, label + ":schema/credit")
        edge = component_edge(row["ordered_C15_component_pair"], label)
        need(edge not in published_edges, label + ":unique")
        published_edges.add(edge)
    need(published_edges == derived_edges, "G2B published/derived edge equality")
    return positive, empty, priority, published_edges


def parse_current(
    capture: Capture,
) -> tuple[
    dict[tuple[str, str], dict[str, Any]],
    dict[str, set[tuple[str, str]]],
    set[tuple[str, str]],
    dict[tuple[str, str], Counter[str]],
    Counter[str],
]:
    routes: dict[tuple[str, str], dict[str, Any]] = {}
    by_terminal: dict[str, set[tuple[str, str]]] = defaultdict(set)
    edges: set[tuple[str, str]] = set()
    edge_terminal_rows: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    cross_rows: Counter[str] = Counter()
    allowed = {
        "SIGNED_BOUNDARY_FACES",
        "COMPLETE_BOUNDARY_FACES",
        "POSITIVE_VOLUME_CARRIERS",
    }
    for ordinal, row in enumerate(capture.rows()):
        label = f"current route:{ordinal}"
        terminal = row["assigned_terminal"]
        need(row["schema"] == "cm2.c27-independent.current-support-91672-priority.row.v1"
             and row["formal_credit"] == 0 and terminal in allowed
             and row["pair_assignment_rule"] == "FIRST_MATCH_SIGNED_THEN_COMPLETE_THEN_POSITIVE",
             label + ":schema/terminal")
        pair = unordered(row["left_member_id"], row["right_member_id"])
        need(pair not in routes, label + ":unique pair")
        signed = row["raw_signed_face_evidence"]
        complete = row["raw_complete_face_evidence"]
        positive = row["raw_positive_C19_physical_support_evidence"]
        need(type(signed) is bool and type(complete) is bool and type(positive) is bool,
             label + ":evidence typing")
        expected = (
            "SIGNED_BOUNDARY_FACES" if signed else
            "COMPLETE_BOUNDARY_FACES" if complete else
            "POSITIVE_VOLUME_CARRIERS"
        )
        need(terminal == expected and (signed or complete or positive), label + ":priority")
        if terminal == "SIGNED_BOUNDARY_FACES":
            need(complete and not positive, label + ":signed evidence")
        elif terminal == "COMPLETE_BOUNDARY_FACES":
            need(not signed and complete and not positive, label + ":complete evidence")
        else:
            need(not signed and not complete and positive, label + ":positive evidence")
        routes[pair] = row
        by_terminal[terminal].add(pair)
        components = row["current_C15_components"]
        need(type(components) is list and len(components) == 2
             and row["same_current_C15_component"] is (components[0] == components[1]),
             label + ":components")
        if components[0] != components[1]:
            edge = unordered(components[0], components[1])
            edges.add(edge)
            edge_terminal_rows[edge][terminal] += 1
            cross_rows[terminal] += 1
    need(len(routes) == 91_672, "current route census")
    need({key: len(value) for key, value in by_terminal.items()} == {
        "SIGNED_BOUNDARY_FACES": 25_452,
        "COMPLETE_BOUNDARY_FACES": 10_688,
        "POSITIVE_VOLUME_CARRIERS": 55_532,
    }, "current unique terminal census")
    need(cross_rows == {"POSITIVE_VOLUME_CARRIERS": 32_012}
         and len(edges) == 14_620, "current cross-C15 census")
    return routes, dict(by_terminal), edges, dict(edge_terminal_rows), cross_rows


def parse_strict_validation(capture: Capture) -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    for ordinal, row in enumerate(capture.rows()):
        label = f"strict-volume validation:{ordinal}"
        need(row["schema"]
                 == "cm2.round306c27r1d.strict-volume-provisional-edge-application-row.v1"
             and row["formal_credit"] == 0
             and row["both_endpoints_bound_to_C15"] is True,
             label + ":validation schema")
        edge = component_edge(row["ordered_round306c15_component_pair"], label)
        need(edge not in edges, label + ":unique")
        edges.add(edge)
    need(len(edges) == 14_772, "strict-volume validation edge census")
    return edges


def run(args: argparse.Namespace) -> dict[str, Any]:
    output = Path(args.out_dir)
    need(not output.exists(), "fresh output directory")
    specs = {
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
    }
    captures: dict[str, Capture] = {}
    try:
        for label, (path, expected) in specs.items():
            captures[label] = Capture.open(label, Path(path), expected)
        g2a_result = captures["g2a_scoped_result"].document()
        validate_g2a_scoped_result(g2a_result, captures)
        receipt = captures["g2b_terminal_receipt"].document()
        validate_terminal_receipt(receipt, captures)
        c19c_receipt = captures["c19c_endpoint_v3_receipt"].document(require_canonical=False)
        validate_c19c_half_open_receipt(c19c_receipt)
        current_dual = captures["current_dual_seed_authority"].document()
        validate_current_dual_seed_authority(current_dual, captures)

        g2a_positive, g2a_empty, g2a_edges, g2a_meta = parse_g2a(captures)
        g2b_positive, g2b_empty, g2b_priority, g2b_edges = parse_g2b(captures)
        need(set(g2a_positive) == set(g2b_positive),
             "G2A positive-side/G2B positive key equality")
        need(set(g2a_empty) == set(g2b_empty),
             "G2A reverse-side/G2B empty key equality")
        need(g2a_edges == g2b_edges, "G2A/G2B component-edge equality")

        current, current_by_terminal, current_edges, edge_terminal_rows, cross_rows = (
            parse_current(captures["current_routes"])
        )
        current_keys = set(current)
        positive_keys, empty_keys = set(g2b_positive), set(g2b_empty)
        graph_endpoint_pairs = g2a_meta["graph_endpoint_pairs"]
        need(not (positive_keys & current_keys)
             and not (empty_keys & current_keys)
             and not (graph_endpoint_pairs & current_keys),
             "C24A role-specific/current pair disjointness")

        # Candidate construction is complete before the historical validation
        # set is parsed.  Only current routes and G2B terminal-priority rows can
        # enter this set.
        candidate_keys = current_keys | set(g2b_priority)
        need(len(candidate_keys) == 101_080, "scoped candidate union census")

        strict_edges = parse_strict_validation(captures["strict_validation_edges"])
        candidate_edges = current_edges | g2b_edges
        need(current_edges <= strict_edges and g2b_edges <= strict_edges
             and candidate_edges <= strict_edges, "strict-volume validation containment")

        current_rank = dsu_stats(current_edges)
        c24_rank = dsu_stats(g2b_edges)
        candidate_rank = dsu_stats(candidate_edges)
        strict_rank = dsu_stats(strict_edges)
        increment, contributing = incremental_rank(current_edges, g2b_edges)
        increment_after_strict, _ = incremental_rank(strict_edges, g2b_edges)
        need(current_rank == {
            "edge_count": 14_620,
            "vertex_count": 14_172,
            "rank_reduction": 13_952,
            "cycle_edge_count": 668,
            "component_count_on_incident_vertices": 220,
        }, "current edge rank census")
        need(c24_rank == {
            "edge_count": 144,
            "vertex_count": 216,
            "rank_reduction": 144,
            "cycle_edge_count": 0,
            "component_count_on_incident_vertices": 72,
        }, "C24A edge rank census")
        need(candidate_rank == {
            "edge_count": 14_724,
            "vertex_count": 14_313,
            "rank_reduction": 14_056,
            "cycle_edge_count": 668,
            "component_count_on_incident_vertices": 257,
        }, "candidate edge rank census")
        need(strict_rank == {
            "edge_count": 14_772,
            "vertex_count": 14_409,
            "rank_reduction": 14_104,
            "cycle_edge_count": 668,
            "component_count_on_incident_vertices": 305,
        }, "strict validation edge rank census")
        need(len(g2b_edges & current_edges) == 40
             and len(g2b_edges - current_edges) == 104
             and increment == len(contributing) == 104
             and increment_after_strict == 0,
             "C24A/current edge overlap and rank contribution")

        key_rows: list[dict[str, Any]] = []
        for pair in sorted(positive_keys | empty_keys):
            if pair in positive_keys:
                arow = g2a_positive[pair]
                brow = g2b_positive[pair]
                prow = g2b_priority[pair]
                kind = "G2A_POSITIVE_SIDE_CONTACT_ALIAS_EQUALS_G2B_EXACT_POSITIVE"
                role_member = arow["positive_side_member_id"]
                included = True
                priority_sha: str | None = prow["row_sha256"]
            else:
                arow = g2a_empty[pair]
                brow = g2b_empty[pair]
                kind = "G2A_REVERSE_SIDE_EMPTY_BINDING_EQUALS_G2B_EXACT_EMPTY"
                role_member = arow["empty_reverse_side_member_id"]
                included = False
                priority_sha = None
            key_rows.append(closed({
                "schema": "cm2.c27-independent.c24a-g2a-g2b-key-comparison.row.v1",
                "authority_pair_key": list(pair),
                "disposition": brow["disposition"],
                "g2a_diagnostic_kind": kind,
                "g2a_diagnostic_row_sha256": arow["row_sha256"],
                "g2a_graph_id": arow["graph_id"],
                "g2a_graph_member_id": arow["g2a_member_id"],
                "g2a_graph_target_semantic_key": [arow["graph_id"], arow["target_member_id"]],
                "g2a_role_member_id": role_member,
                "g2b_exact_row_sha256": brow["row_sha256"],
                "g2b_priority_row_sha256": priority_sha,
                "current_assigned_terminal": current[pair]["assigned_terminal"] if pair in current else None,
                "included_in_scoped_candidate_union": included,
                "normalized_assigned_terminal": "POSITIVE_VOLUME_CARRIERS" if included else None,
                "formal_credit": 0,
            }))
        need(len(key_rows) == 18_800, "key comparison row census")

        ownership_rows: list[dict[str, Any]] = []
        normalized = {
            "SIGNED_BOUNDARY_FACES": "SIGNED_BOUNDARY_FACES",
            "COMPLETE_BOUNDARY_FACES": "COMPLETE_BOUNDARY_FACES",
            "POSITIVE_VOLUME_CARRIERS": "POSITIVE_VOLUME_CARRIERS",
        }
        for pair in sorted(candidate_keys):
            if pair in current:
                row = current[pair]
                terminal = normalized[row["assigned_terminal"]]
                positive_branch = (
                    "CURRENT_C19_PHYSICAL_SUPPORT"
                    if row["assigned_terminal"] == "POSITIVE_VOLUME_CARRIERS" else None
                )
                components = row["current_C15_components"]
                ownership_rows.append(closed({
                    "schema": "cm2.c27-independent.primitive-three-terminal-unique-ownership.row.v1",
                    "pair_key": list(pair),
                    "assigned_terminal": terminal,
                    "positive_support_branch": positive_branch,
                    "source_authority": "CURRENT_SUPPORT_V4B_SEED1_PRIORITY_LEDGER",
                    "source_row_sha256": row["row_sha256"],
                    "current_source_terminal": row["assigned_terminal"],
                    "C24A_G2B_exact_row_sha256": None,
                    "G2A_diagnostic_alias_row_sha256": None,
                    "unordered_current_C15_components": sorted(components),
                    "same_current_C15_component": components[0] == components[1],
                    "pair_assignment_rule": "FIRST_MATCH_SIGNED_THEN_COMPLETE_THEN_POSITIVE_VOLUME_CARRIERS",
                    "formal_credit": 0,
                }))
            else:
                exact = g2b_positive[pair]
                priority = g2b_priority[pair]
                alias = g2a_positive[pair]
                components = exact["current_C15_components"]
                ownership_rows.append(closed({
                    "schema": "cm2.c27-independent.primitive-three-terminal-unique-ownership.row.v1",
                    "pair_key": list(pair),
                    "assigned_terminal": "POSITIVE_VOLUME_CARRIERS",
                    "positive_support_branch": "C24A_G2B_EXACT_FACTOR_SIGN_POSITIVE_WITH_G2A_RELATIVE_BOUNDARY_DIAGNOSTIC",
                    "source_authority": "C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER",
                    "source_row_sha256": priority["row_sha256"],
                    "current_source_terminal": None,
                    "C24A_G2B_exact_row_sha256": exact["row_sha256"],
                    "G2A_diagnostic_alias_row_sha256": alias["row_sha256"],
                    "unordered_current_C15_components": sorted(components),
                    "same_current_C15_component": components[0] == components[1],
                    "pair_assignment_rule": "FIRST_MATCH_SIGNED_THEN_COMPLETE_THEN_POSITIVE_VOLUME_CARRIERS",
                    "formal_credit": 0,
                }))
        need(len(ownership_rows) == 101_080, "unique ownership ledger census")

        edge_rows: list[dict[str, Any]] = []
        for edge in sorted(candidate_edges):
            terminal_rows = edge_terminal_rows.get(edge, Counter())
            edge_rows.append(closed({
                "schema": "cm2.c27-independent.primitive-three-terminal-cross-c15-edge-union.row.v1",
                "unordered_component_pair": list(edge),
                "present_in_current_support_primitive": edge in current_edges,
                "current_cross_pair_row_census_by_terminal": dict(sorted(terminal_rows.items())),
                "present_in_G2A_scoped_authority": edge in g2a_edges,
                "present_in_G2B_terminal_authority": edge in g2b_edges,
                "G2A_G2B_same_edge_authority": (edge in g2a_edges) == (edge in g2b_edges),
                "novel_against_current_support": edge in (g2b_edges - current_edges),
                "incremental_rank_contribution_after_current_support": edge in contributing,
                "present_in_strict_volume_validation_only_set": edge in strict_edges,
                "strict_volume_used_as_candidate_source": False,
                "formal_credit": 0,
            }))
        need(len(edge_rows) == 14_724, "candidate edge ledger census")

        output.mkdir(parents=True, exist_ok=False)
        ledgers = {
            "C24A_key_comparison": write_rows(
                output / "C24A_18800_G2A_G2B_key_comparison.jsonl.gz", key_rows
            ),
            "unique_ownership": write_rows(
                output / "primitive_three_terminal_101080_unique_ownership.jsonl.gz",
                ownership_rows,
            ),
            "cross_C15_edge_union": write_rows(
                output / "primitive_three_terminal_14724_cross_C15_edge_union.jsonl.gz",
                edge_rows,
            ),
        }

        current_pairwise = {
            "SIGNED_intersection_COMPLETE_only": len(
                current_by_terminal["SIGNED_BOUNDARY_FACES"]
                & current_by_terminal["COMPLETE_BOUNDARY_FACES"]
            ),
            "SIGNED_intersection_POSITIVE": len(
                current_by_terminal["SIGNED_BOUNDARY_FACES"]
                & current_by_terminal["POSITIVE_VOLUME_CARRIERS"]
            ),
            "COMPLETE_only_intersection_POSITIVE": len(
                current_by_terminal["COMPLETE_BOUNDARY_FACES"]
                & current_by_terminal["POSITIVE_VOLUME_CARRIERS"]
            ),
        }
        body = {
            "schema": "cm2.c27-independent.c24a-current-primitive-three-terminal-union-comparator.v1",
            "status": (
                "PASS_SCOPED_PRIMITIVE_KEY_COMPARATOR_AND_101080_UNIQUE_UNION__"
                "GLOBAL_TOTALITY_FAIL_CLOSED__ZERO_CREDIT"
            ),
            "invocation_seed": args.seed,
            "C24A_G2A_G2B_key_by_key": {
                "G2A_authority_level": (
                    "SOURCE_EXEC_BOUND_SCOPED_ZERO_CREDIT_THEOREM__GLOBAL_POSITIVE_C19_OPEN"
                ),
                "canonical_positive_bijection": (
                    "G2A_(graph_id,target_member_id)_MAPS_BIJECTIVELY_VIA_"
                    "(positive_side_member_id,target_member_id)_TO_G2B_AUTHORITY_PAIR"
                ),
                "G2A_positive_contact_keys": 9_408,
                "G2B_exact_positive_keys": 9_408,
                "positive_key_intersection": 9_408,
                "positive_G2A_only": 0,
                "positive_G2B_only": 0,
                "G2A_reverse_empty_keys": 9_392,
                "G2B_exact_empty_keys": 9_392,
                "empty_key_intersection": 9_392,
                "empty_G2A_only": 0,
                "empty_G2B_only": 0,
                "G2B_exact_positive_equals_G2B_priority": True,
                "G2A_G2B_positive_empty_cross_intersections": 0,
                "G2A_semantic_contact_keys": g2a_meta["semantic_contact_key_count"],
                "G2A_reverse_semantic_keys": g2a_meta["reverse_semantic_key_count"],
                "G2A_single_side_no_reverse": g2a_meta["single_side_no_reverse_count"],
            },
            "pair_intersections_with_current_by_terminal": {
                "G2A_graph_target_alias_pairs": terminal_intersections(
                    graph_endpoint_pairs, current_by_terminal
                ),
                "G2A_positive_side_equals_G2B_positive": terminal_intersections(
                    positive_keys, current_by_terminal
                ),
                "G2A_reverse_side_equals_G2B_empty": terminal_intersections(
                    empty_keys, current_by_terminal
                ),
                "current_terminal_pairwise": current_pairwise,
            },
            "scoped_candidate_union": {
                "current_support_pair_count": 91_672,
                "C24A_G2B_positive_pair_count": 9_408,
                "C24A_G2B_empty_excluded_count": 9_392,
                "current_intersection_C24A_positive": 0,
                "current_intersection_C24A_empty": 0,
                "union_pair_count": 101_080,
                "unique_ownership_row_count": 101_080,
                "normalized_terminal_census": {
                    "SIGNED_BOUNDARY_FACES": 25_452,
                    "COMPLETE_BOUNDARY_FACES": 10_688,
                    "POSITIVE_VOLUME_CARRIERS": 64_940,
                },
                "positive_support_branch_census": {
                    "CURRENT_C19_PHYSICAL_SUPPORT": 55_532,
                    "C24A_G2B_EXACT_FACTOR_SIGN_POSITIVE_WITH_G2A_RELATIVE_BOUNDARY_DIAGNOSTIC": 9_408,
                },
                "G2A_graph_alias_counted_as_independent_candidate": False,
                "scoped_unique_assignment_closed": True,
            },
            "cross_C15_edge_overlap_and_rank": {
                "current_cross_pair_rows_by_terminal": dict(sorted(cross_rows.items())),
                "current_unique_edges": 14_620,
                "G2A_unique_edges": 144,
                "G2B_unique_edges": 144,
                "G2A_intersection_G2B": len(g2a_edges & g2b_edges),
                "C24A_intersection_current": len(g2b_edges & current_edges),
                "C24A_novel_against_current": len(g2b_edges - current_edges),
                "candidate_edge_union": len(candidate_edges),
                "incremental_rank_reduction_after_current": increment,
                "current_graph": current_rank,
                "C24A_graph": c24_rank,
                "candidate_union_graph": candidate_rank,
                "strict_volume_validation": {
                    "edge_count": len(strict_edges),
                    "current_intersection": len(current_edges & strict_edges),
                    "current_difference": len(current_edges - strict_edges),
                    "C24A_intersection": len(g2b_edges & strict_edges),
                    "C24A_difference": len(g2b_edges - strict_edges),
                    "candidate_union_intersection": len(candidate_edges & strict_edges),
                    "candidate_union_difference": len(candidate_edges - strict_edges),
                    "strict_edges_not_in_candidate_union": len(strict_edges - candidate_edges),
                    "incremental_C24A_rank_after_strict_volume": increment_after_strict,
                    "graph": strict_rank,
                    "used_as_candidate_universe": False,
                },
            },
            "candidate_governance": {
                "candidate_sources": [
                    "CURRENT_SUPPORT_V4B_SEED1_PRIORITY_PRIMITIVE_LEDGER",
                    "C24A_G2B_TERMINAL_AUTHORIZED_POSITIVE_PRIORITY_LEDGER",
                ],
                "G2A_scoped_authority_role": "DIAGNOSTIC_ALIAS_AND_KEY_CROSSWALK_ONLY",
                "G2B_exact_18800_role": "POSITIVE_EMPTY_AUTHORITY_PARTITION",
                "strict_volume_edge_role": "POST_CONSTRUCTION_VALIDATION_ONLY",
                "C19C_endpoint_v3_receipt_role": "HALF_OPEN_BOUNDARY_AUTHORITY_ONLY",
                "C19C_endpoint_v3_used_as_candidate_source": False,
                "current_seed2_role": "BYTE_IDENTICAL_NORMALIZATION_VALIDATION_ONLY",
                "current_seed2_used_as_second_candidate_source": False,
                "historical_edge_ledger_used_as_candidate_universe": False,
                "C27_FAMILIES_imported_or_read": False,
                "old_transition_ledger_imported_or_read": False,
                "C28_imported_or_read": False,
                "C29_imported_or_read": False,
                "producer_module_imported": False,
            },
            "ledgers": ledgers,
            "global_claim_gate": {
                "primitive_support_atom_denominator": 483_232,
                "primitive_support_atom_families": [
                    "C19A", "C19B", "C19C", "C20A", "C22A", "C23A"
                ],
                "atom_to_pair_incidence_ledger_materialized_here": False,
                "atom_without_pair_complement_census_materialized_here": False,
                "current_only_atom_incidence_count": 62_240,
                "current_only_atom_complement_count": 420_992,
                "current_only_complement_accepted_as_global_complement": False,
                "C24A_G2B_positive_C22_target_atom_incidence_joined": False,
                "C24A_G2B_positive_pair_count_requiring_atom_join": 9_408,
                "C24A_atom_terminal_normalization": (
                    "G2B_POSITIVE_VOLUME_CARRIERS__G2A_ALIAS_NO_SECOND_ASSIGNMENT"
                ),
                "C24A_same_chart_positive_double_count_forbidden": True,
                "full_union_atom_join_required": True,
                "primitive_row_bound_terminal_selection_exhaustive": False,
                "primitive_row_bound_terminal_selection_mutually_exclusive": False,
                "pair_routing_total_on_483232_atom_denominator": False,
                "C19C_endpoint_v3_half_open_authority_consumed": True,
                "global_candidate_totality_proved": False,
                "global_unique_assignment_proved": False,
                "current_support_seed2_normalized_authority_consumed": True,
                "current_support_seed1_seed2_priority_byte_identical": True,
                "G2A_source_exec_bound_scoped_authority_consumed": True,
                "G2A_global_positive_C19_extension_required": True,
                "C27_C28_C29_full_rebuild_required": True,
                "decision": "FAIL_CLOSED_NO_PROMOTION",
            },
            "formal_credit": 0,
            "manifest_authorized": False,
            "strict_nonpromotion": {
                "C27_transition_totality": 0,
                "C28_pair_routing": 0,
                "C29_physical_maximality": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {
                    label: capture.attestation()
                    for label, capture in sorted(captures.items())
                },
            },
        }
        result = dict(body)
        result["semantic_projection_sha256"] = digest({
            key: value for key, value in body.items()
            if key not in {"invocation_seed", "root_input_capture"}
        })
        result["result_sha256"] = digest(result)
        (output / "result.json").write_bytes(canonical(result) + b"\n")
        return result
    finally:
        for capture in captures.values():
            capture.close()


def add_input(parser: argparse.ArgumentParser, name: str) -> None:
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
    ):
        add_input(parser, name)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    try:
        result = run(args)
    except (Failure, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({
        "status": result["status"],
        "semantic_projection_sha256": result["semantic_projection_sha256"],
        "result_sha256": result["result_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
