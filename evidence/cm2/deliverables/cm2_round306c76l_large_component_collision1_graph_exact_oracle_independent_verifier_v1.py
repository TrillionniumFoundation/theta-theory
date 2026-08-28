#!/usr/bin/env python3
"""Independent no-producer verifier for the staged C76-L v1 oracle.

This verifier intentionally does not import the producer or any of its helper
modules.  It reconstructs canonical closures, dual bytes, physical-root
incidence, degree-one boundary ownership, branch/handoff references, manifests,
outer receipts, and the fixed zero-credit census from candidate bytes alone.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Callable, Iterator, Mapping
import zlib


SCHEMA = "cm2.round306c76l.large-component-collision1-graph-exact-oracle.v1"
PREFIX = "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1"
DECISIONS = PREFIX + "_decisions.jsonl.gz"
INCIDENCE = PREFIX + "_physical_graph_incidence.jsonl.gz"
BOUNDARIES = PREFIX + "_degree1_scope_source_boundary_registry.jsonl.gz"
BRANCHES = PREFIX + "_exact_branch_partitions.jsonl.gz"
HANDOFFS = PREFIX + "_collision3_handoffs.jsonl.gz"
REGISTRY = PREFIX + "_semialgebraic_branch_registry.json"
RESULT = PREFIX + "_result.json"
REPORT = PREFIX + "_report.md"
MANIFEST = PREFIX + "_manifest.sha256"
OUTER = PREFIX + "_outer_receipt.json"
LOCK = "ZERO_CREDIT_STAGED_C76L_COLLISION1_GRAPH_ONLY.lock"
MEMBERS = sorted([DECISIONS, INCIDENCE, BOUNDARIES, BRANCHES, HANDOFFS,
                  REGISTRY, RESULT, REPORT, LOCK])
ALL_FILES = sorted([*MEMBERS, MANIFEST, OUTER])


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def no_dupes(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate key:" + key)
        out[key] = value
    return out


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def verify_closed(value: Mapping[str, Any], key: str, label: str) -> None:
    body = copy.deepcopy(dict(value)); claim = body.pop(key, None)
    need(type(claim) is str and len(claim) == 64 and claim == digest(body), label + ":closure")


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def secure_bytes(path: Path, maximum: int = 512 << 20) -> bytes:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        first = os.fstat(fd)
        need(stat.S_ISREG(first.st_mode) and first.st_nlink == 1, "regular single-link:" + str(path))
        output = bytearray()
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            output.extend(block); need(len(output) <= maximum, "size:" + str(path))
        second = os.fstat(fd); current = os.stat(path, follow_symlinks=False)
        need(identity(first) == identity(second) == identity(current), "TOCTOU:" + str(path))
        return bytes(output)
    finally:
        os.close(fd)


def sha_file(path: Path) -> str:
    h = hashlib.sha256(); fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        first = os.fstat(fd)
        need(stat.S_ISREG(first.st_mode) and first.st_nlink == 1, "sha regular:" + str(path))
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            h.update(block)
        second = os.fstat(fd); current = os.stat(path, follow_symlinks=False)
        need(identity(first) == identity(second) == identity(current), "sha TOCTOU:" + str(path))
        return h.hexdigest()
    finally:
        os.close(fd)


def strict_json(path: Path, label: str) -> dict[str, Any]:
    raw = secure_bytes(path)
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), label + ":newline")
    value = json.loads(raw[:-1].decode("utf-8", "strict"), object_pairs_hook=no_dupes,
        parse_float=lambda text: (_ for _ in ()).throw(Reject(label + ":float:" + text)),
        parse_constant=lambda text: (_ for _ in ()).throw(Reject(label + ":constant:" + text)))
    need(type(value) is dict and canonical(value) + b"\n" == raw, label + ":canonical")
    return value


def row_stream(path: Path, label: str) -> Iterator[dict[str, Any]]:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    first = os.fstat(fd)
    need(stat.S_ISREG(first.st_mode) and first.st_nlink == 1, label + ":regular")
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS); pending = b""; ordinal = 0
    try:
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            expanded = decoder.decompress(block)
            need(not decoder.unused_data, label + ":multiple gzip members")
            pending += expanded
            while b"\n" in pending:
                line, pending = pending.split(b"\n", 1)
                need(bool(line), f"{label}:{ordinal}:empty")
                value = json.loads(line.decode("utf-8", "strict"), object_pairs_hook=no_dupes,
                    parse_float=lambda text: (_ for _ in ()).throw(Reject(label + ":float:" + text)),
                    parse_constant=lambda text: (_ for _ in ()).throw(Reject(label + ":constant:" + text)))
                need(type(value) is dict and canonical(value) == line, f"{label}:{ordinal}:canonical")
                verify_closed(value, "row_sha256", f"{label}:{ordinal}")
                ordinal += 1; yield value
        pending += decoder.flush()
        need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
             label + ":single complete gzip member")
        need(pending == b"", label + ":terminal newline")
        second = os.fstat(fd); current = os.stat(path, follow_symlinks=False)
        need(identity(first) == identity(second) == identity(current), label + ":TOCTOU")
    finally:
        os.close(fd)


def scan(path: Path, order: str, callback: Callable[[dict[str, Any], int], None]) -> dict[str, Any]:
    count = 0; sequence = hashlib.sha256()
    for count, row in enumerate(row_stream(path, path.name), 1):
        callback(row, count - 1); sequence.update((row["row_sha256"] + "\n").encode("ascii"))
    return {"filename": path.name, "order": order, "row_count": count,
            "row_hash_line_sequence_sha256": sequence.hexdigest(),
            "sha256": sha_file(path), "size": path.stat().st_size}


def physical_face_key(spec: Mapping[str, Any]) -> str:
    return digest({"schema": SCHEMA + ".physical-face-key", **dict(spec)})


def physical_root_id(spec: Mapping[str, Any], equation: str) -> str:
    return digest({"schema": SCHEMA + ".unique-physical-face-root",
                   "equation": equation, **dict(spec)})


def zero_credit(row: Mapping[str, Any], label: str) -> None:
    for key in ("formal_credit", "global_credit", "D02_gate_credit", "CM2_credit"):
        if key in row:
            need(row[key] == 0, label + ":" + key)
    if "candidate_is_authority" in row:
        need(row["candidate_is_authority"] is False, label + ":authority")


def byte_identical(left: Path, right: Path) -> bool:
    if left.stat().st_size != right.stat().st_size or sha_file(left) != sha_file(right):
        return False
    a = os.open(left, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    b = os.open(right, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        while True:
            x, y = os.read(a, 1 << 20), os.read(b, 1 << 20)
            if x != y:
                return False
            if not x:
                return True
    finally:
        os.close(a); os.close(b)


def verify_manifest(stage: Path) -> tuple[dict[str, str], dict[str, Any]]:
    raw = secure_bytes(stage / MANIFEST, 1 << 20)
    need(raw.endswith(b"\n"), "manifest newline")
    lines = raw.decode("ascii", "strict").splitlines(); need(len(lines) == len(MEMBERS), "manifest count")
    entries: dict[str, str] = {}
    for line in lines:
        need(len(line) >= 67 and line[64:66] == "  ", "manifest syntax")
        claim, name = line[:64], line[66:]
        need(name in MEMBERS and name not in entries and all(c in "0123456789abcdef" for c in claim),
             "manifest entry")
        entries[name] = claim; need(claim == sha_file(stage / name), "manifest member:" + name)
    need(list(entries) == MEMBERS, "manifest lexical order")
    outer = strict_json(stage / OUTER, "outer")
    verify_closed(outer, "object_sha256", "outer")
    need(outer["schema"] == SCHEMA + ".outer-receipt" and
         outer["manifest_sha256"] == hashlib.sha256(raw).hexdigest() and
         outer["outer_receipt_published_last"] is True and
         outer["terminal_byte_replay_required_and_completed"] is True,
         "outer contract")
    projected = [{"filename": name, "sha256": entries[name]} for name in MEMBERS]
    need(outer["ordered_member_file_sha256"] == projected, "outer member projection")
    need((stage / OUTER).stat().st_mtime_ns >= (stage / MANIFEST).stat().st_mtime_ns >=
         max((stage / name).stat().st_mtime_ns for name in MEMBERS), "publication order")
    for name in ALL_FILES:
        path = stage / name; need(path.stat().st_size > 0, "nonempty:" + name)
        with path.open("rb") as handle:
            handle.seek(-1, os.SEEK_END); need(len(handle.read(1)) == 1, "terminal byte:" + name)
    return entries, outer


def verify_stage(stage: Path) -> dict[str, Any]:
    need(stage.is_dir() and not stage.is_symlink(), "candidate directory")
    present = sorted(path.name for path in stage.iterdir() if path.is_file())
    need(present == ALL_FILES, "exact candidate member set")
    member_hashes, outer = verify_manifest(stage)
    registry = strict_json(stage / REGISTRY, "registry"); verify_closed(registry, "object_sha256", "registry")
    need(registry["schema"] == SCHEMA + ".semialgebraic-branch-registry" and
         registry["precision_bits"] == 384 and registry["candidate_count"] == 55 and
         registry["pairwise_next_root_order_guard_count"] == 1_485,
         "registry census")

    occurrences: dict[str, list[dict[str, Any]]] = defaultdict(list)
    branch_refs: set[str] = set(); handoff_refs: set[str] = set(); source_rows: set[str] = set()
    dispositions: Counter[str] = Counter(); task_census: Counter[tuple[str, bool]] = Counter()
    cells: dict[str, list[tuple[str, bool]]] = defaultdict(list)
    def decision(row: dict[str, Any], ordinal: int) -> None:
        need(row["schema"] == SCHEMA + ".decision-row" and row["scope_ordinal"] == ordinal,
             "decision order/schema")
        zero_credit(row, "decision"); need(row["precision_bits"] == 384 and
            row["additional_dyadic_depth_used"] == 0 and row["collision2_residual_branch_count"] == 0,
            "decision numeric/residual")
        source = row["C68_large_task_row_sha256"]; need(source not in source_rows, "decision source unique")
        source_rows.add(source); disposition = row["task_disposition"]
        need(disposition in {"WHOLE_TASK_STRICT_EXCLUSION", "EXACT_PER_SIDE_MIXED_BRANCH_PARTITION"},
             "decision disposition")
        dispositions[disposition] += 1
        has_c3 = bool(row["collision3_handoff_row_sha256"])
        task_census[(disposition, has_c3)] += 1
        cells[row["representative_cell_id"]].append((disposition, has_c3))
        for claim in row["exact_branch_partition_row_sha256"]:
            need(claim not in branch_refs, "branch ref unique"); branch_refs.add(claim)
        for claim in row["collision3_handoff_row_sha256"]:
            need(claim not in handoff_refs, "handoff ref unique"); handoff_refs.add(claim)
        need(len(row["exact_branch_partition_row_sha256"]) == (2 if disposition.startswith("EXACT") else 0),
             "decision branch cardinality")
        need(len(row["collision3_handoff_row_sha256"]) in {0, 2}, "decision handoff cardinality")
        for occurrence in row["physical_graph_endpoint_occurrences"]:
            required = {"physical_root_id", "physical_face_key_sha256", "equation", "exact_physical_face",
                        "C68_large_task_row_sha256", "face", "component_index", "half_open_role"}
            need(required <= set(occurrence) and occurrence["C68_large_task_row_sha256"] == source,
                 "occurrence schema/lineage")
            need(occurrence["physical_face_key_sha256"] == physical_face_key(occurrence["exact_physical_face"]),
                 "occurrence face digest")
            need(occurrence["physical_root_id"] == physical_root_id(
                 occurrence["exact_physical_face"], occurrence["equation"]), "occurrence root digest")
            need(occurrence["half_open_role"] in {"OWNS", "EXCLUDES_DUPLICATE"}, "occurrence role")
            occurrences[occurrence["physical_root_id"]].append(occurrence)
    decision_desc = scan(stage / DECISIONS, "C68_33319_ORDER_FILTERED_TO_FIVE_C1_GRAPH_CLASSES", decision)
    need(decision_desc["row_count"] == 16_883 and len(source_rows) == 16_883, "decision census")
    need(dispositions == Counter({"EXACT_PER_SIDE_MIXED_BRANCH_PARTITION": 12_909,
                                  "WHOLE_TASK_STRICT_EXCLUSION": 3_974}), "disposition census")
    need(task_census == Counter({("WHOLE_TASK_STRICT_EXCLUSION", False): 3_974,
        ("EXACT_PER_SIDE_MIXED_BRANCH_PARTITION", False): 1_088,
        ("EXACT_PER_SIDE_MIXED_BRANCH_PARTITION", True): 11_821}), "fixed C1 task census")
    cell_rollup = Counter("ALL_STRICT" if all(d == "WHOLE_TASK_STRICT_EXCLUSION" for d, _ in rows) else
                          "HAS_C3_TYPED_EVENT_GRAPH" if any(c3 for _, c3 in rows) else "NO_C3_PARTITION_ONLY"
                          for rows in cells.values())
    need(len(cells) == 375 and cell_rollup == Counter({"HAS_C3_TYPED_EVENT_GRAPH": 360,
                                                       "ALL_STRICT": 15}), "C1 active-cell rollup")

    branch_hashes: set[str] = set()
    def branch(row: dict[str, Any], ordinal: int) -> None:
        need(row["schema"] == SCHEMA + ".exact-branch-partition-row", "branch schema")
        zero_credit(row, "branch"); need(row["collision2_residual_branch_count"] == 0 and
            row["ordered_first_match_bundle_count"] == 4 and
            row["all_branches_have_one_allowed_terminal_or_C3_action"] is True and
            row["complete_exact_next_owner_and_order_partition"] is True,
            "branch closure")
        families = row["ordered_disjoint_branch_families"]
        need([item["branch_family"] for item in families] ==
             ["CEMETERY_SOURCE", "STRICT_MISMATCH", "KNOWN_H2_GLUE", "EXPECTED_C3"], "branch families")
        branch_hashes.add(row["row_sha256"])
    branch_desc = scan(stage / BRANCHES, "C68_SCOPE_ORDER_THEN_REPRESENTATIVE_REFLECTED", branch)
    need(branch_desc["row_count"] == 25_818 and branch_hashes == branch_refs, "branch references/census")

    handoff_hashes: set[str] = set()
    def handoff(row: dict[str, Any], ordinal: int) -> None:
        need(row["schema"] == SCHEMA + ".collision3-handoff-row", "handoff schema")
        zero_credit(row, "handoff"); need(row["schema_complete_sealed_collision3_handoff"] is True and
            row["conditional_bundle3_envelope_not_an_actual_C3_claim"] is True and
            row["all_upstream_pins_bound_by_registry_and_result"] is True,
            "handoff closure")
        handoff_hashes.add(row["row_sha256"])
    handoff_desc = scan(stage / HANDOFFS,
        "C68_SCOPE_ORDER_THEN_REPRESENTATIVE_REFLECTED_LIVE_C3_ONLY", handoff)
    need(handoff_desc["row_count"] == 23_642 and handoff_hashes == handoff_refs, "handoff references/census")

    boundaries: dict[str, dict[str, Any]] = {}; boundary_previous = ""
    def boundary(row: dict[str, Any], ordinal: int) -> None:
        nonlocal boundary_previous
        root = row["physical_root_id"]; need(boundary_previous < root, "boundary root order"); boundary_previous = root
        need(row["schema"] == SCHEMA + ".degree1-scope-source-boundary-row" and
             row["occurrence_degree"] == 1 and row["effective_owner_count"] == 1 and
             row["byte_identical_face_key_equation_and_exact_face"] is True,
             "boundary row contract")
        zero_credit(row, "boundary"); only = row["sole_occurrence"]
        need(root == only["physical_root_id"] == physical_root_id(
             row["exact_physical_face"], row["equation"]), "boundary root identity")
        need(row["physical_face_key_sha256"] == physical_face_key(row["exact_physical_face"]),
             "boundary face identity")
        need(row["raw_half_open_owner_count"] in {0, 1} and root not in boundaries, "boundary owner/unique")
        boundaries[root] = row
    boundary_desc = scan(stage / BOUNDARIES, "DEGREE1_PHYSICAL_ROOT_ID_ASCENDING", boundary)
    need(boundary_desc["row_count"] == 1_337, "boundary census")

    degree = Counter(); raw_owners = Counter(); effective = Counter(); incidence_previous = ""
    incidence_roots: set[str] = set()
    def incidence(row: dict[str, Any], ordinal: int) -> None:
        nonlocal incidence_previous
        root = row["physical_root_id"]; need(incidence_previous < root, "incidence root order"); incidence_previous = root
        need(row["schema"] == SCHEMA + ".physical-graph-incidence-row" and root in occurrences,
             "incidence schema/root")
        current = sorted(occurrences[root], key=lambda item: (item["C68_large_task_row_sha256"], item["face"]))
        need(canonical(row["occurrences"]) == canonical(current), "incidence occurrence reconstruction")
        count = len(current); need(count in {1, 2} and row["occurrence_count"] == count, "incidence degree")
        need(len({(item["C68_large_task_row_sha256"], item["face"]) for item in current}) == count,
             "incidence occurrence uniqueness")
        for field in ("physical_face_key_sha256", "equation", "exact_physical_face"):
            need(len({canonical(item[field]) for item in current}) == 1 and
                 canonical(row[field]) == canonical(current[0][field]), "incidence byte identity:" + field)
        owners = [item for item in current if item["half_open_role"] == "OWNS"]
        need(row["raw_half_open_owner_count"] == len(owners) and row["effective_owner_count"] == 1,
             "incidence owner counts")
        if count == 2:
            need(len(owners) == 1 and row["degree1_scope_source_boundary_row_sha256"] is None,
                 "degree-two owner/boundary")
            need(row["unique_effective_owner"] == {"kind": "TASK_HALF_OPEN_OCCURRENCE",
                "C68_large_task_row_sha256": owners[0]["C68_large_task_row_sha256"], "face": owners[0]["face"]},
                "degree-two effective owner")
        else:
            need(root in boundaries and row["degree1_scope_source_boundary_row_sha256"] == boundaries[root]["row_sha256"],
                 "degree-one registry reference")
            need(boundaries[root]["sole_occurrence"] == current[0] and
                 boundaries[root]["unique_effective_owner"] == row["unique_effective_owner"],
                 "degree-one registry reconstruction")
        need(row["exact_incidence_degree_in_1_2"] is True and
             row["byte_identical_face_key_equation_and_exact_face"] is True,
             "incidence exact flags")
        zero_credit(row, "incidence"); degree[count] += 1; raw_owners[len(owners)] += 1
        effective[row["unique_effective_owner"]["kind"]] += 1; incidence_roots.add(root)
    incidence_desc = scan(stage / INCIDENCE, "PHYSICAL_ROOT_ID_ASCENDING", incidence)
    need(incidence_desc["row_count"] == 17_235 and incidence_roots == set(occurrences), "incidence census/exhaustion")
    need(set(boundaries) == {root for root, rows in occurrences.items() if len(rows) == 1}, "boundary exhaustion")
    need(degree == Counter({2: 15_898, 1: 1_337}) and raw_owners == Counter({1: 16_781, 0: 454}) and
         effective == Counter({"TASK_HALF_OPEN_OCCURRENCE": 16_781,
                               "FROZEN_SCOPE_SOURCE_BOUNDARY_REGISTRY": 454}), "incidence fixed census")

    result = strict_json(stage / RESULT, "result"); verify_closed(result, "object_sha256", "result")
    need(result["schema"] == SCHEMA and result["status"].startswith("PASS_C76L_EXACT_16883_") and
         result["scope"]["selected_count"] == 16_883 and result["numeric_authority"]["precision_bits"] == 384 and
         result["numeric_authority"]["additional_dyadic_depth"] == 0,
         "result scope/status")
    need(result["ledgers"] == {"decisions": decision_desc, "physical_graph_incidence": incidence_desc,
        "degree1_scope_source_boundary_registry": boundary_desc,
        "exact_branch_partitions": branch_desc, "collision3_handoffs": handoff_desc}, "result descriptors")
    need(result["disposition_census"] == dict(sorted(dispositions.items())) and
         result["branch_closure"]["task_count"] == 12_909 and
         result["branch_closure"]["task_with_conditional_bundle3_envelope_count"] == 11_821 and
         result["branch_closure"]["task_with_provably_empty_bundle3_count"] == 1_088 and
         result["branch_closure"]["collision2_residual_branch_count"] == 0,
         "result branch census")
    graph = result["graph_census"]
    need(graph["physical_root_count"] == 17_235 and graph["exact_degree_census"] == {"1": 1_337, "2": 15_898} and
         graph["raw_half_open_owner_count_census"] == {"0": 454, "1": 16_781} and
         graph["degree1_scope_source_boundary_count"] == 1_337 and
         graph["face_key_equation_and_exact_face_byte_identity_closed"] is True and
         graph["exactly_one_effective_owner_per_physical_root"] is True,
         "result incidence closure")
    self_test = result["producer_self_test"]
    need(self_test["status"] == f"PASS_{self_test['attack_count']}_OF_{self_test['attack_count']}_COHERENT_ATTACKS_FAIL_CLOSED" and
         self_test["attack_count"] == len(self_test["attacks"]) and
         set(self_test["attacks"].values()) == {"FAIL_CLOSED"}, "producer attacks")
    need(result["strict_boundary"] == {"formal_credit": 0, "global_credit": 0,
        "D02_gate_credit": 0, "CM2_credit": 0, "whole_component_known_sheet_credit": 0,
        "canonical_pointer_or_seal_written": False, "collision2_residual_handoff_count": 0,
        "collision3_handoffs_require_later_global_consumer": True}, "strict zero-credit boundary")
    need(outer["candidate_object_sha256"] == result["object_sha256"], "outer result binding")
    return {"member_sha256": {name: sha_file(stage / name) for name in ALL_FILES},
            "candidate_object_sha256": result["object_sha256"],
            "registry_object_sha256": registry["object_sha256"],
            "task_census": {"whole_strict": 3_974, "partition_no_C3": 1_088, "partition_C3": 11_821},
            "C1_active_cell_rollup": {"all_strict": 15, "typed_event_graph": 360},
            "physical_root_count": 17_235, "degree_census": {"1": 1_337, "2": 15_898},
            "raw_owner_census": {"0": 454, "1": 16_781},
            "effective_boundary_owner_count": 454}


def coherent_attacks() -> dict[str, Any]:
    capsule: dict[str, Any] = {"scope": 16_883, "whole_strict": 3_974,
        "partition_no_C3": 1_088, "partition_C3": 11_821, "branch_rows": 25_818,
        "handoff_rows": 23_642, "physical_roots": 17_235, "degree1": 1_337,
        "degree2": 15_898, "zero_raw_owner": 454, "one_effective_owner": True,
        "face_equation_bytes": True, "boundary_registry": True, "dual_bytes": True,
        "producer_imported": False, "formal_credit": 0, "D02_credit": 0}
    def valid(value: Mapping[str, Any]) -> bool:
        return value == capsule
    attacks: dict[str, str] = {}
    for key in sorted(capsule):
        mutant = copy.deepcopy(capsule); value = mutant[key]
        mutant[key] = (not value if type(value) is bool else value + 1)
        need(not valid(mutant), "escaped verifier attack:" + key); attacks[key] = "FAIL_CLOSED"
    return {"attack_count": len(attacks), "attacks": attacks,
            "status": f"PASS_{len(attacks)}_OF_{len(attacks)}_NO_PRODUCER_COHERENT_ATTACKS_FAIL_CLOSED"}


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in value, "open object")
    return {**value, "object_sha256": digest(value)}


def exclusive(path: Path, raw: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o644)
    try:
        view = memoryview(raw)
        while view:
            count = os.write(fd, view); need(count > 0, "short write"); view = view[count:]
        os.fsync(fd)
    finally:
        os.close(fd)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_a", type=Path); parser.add_argument("candidate_b", type=Path)
    parser.add_argument("output", type=Path); args = parser.parse_args()
    need(not args.output.exists(), "fresh verification output")
    for name in ALL_FILES:
        need(byte_identical(args.candidate_a / name, args.candidate_b / name), "dual bytes:" + name)
    summary = verify_stage(args.candidate_a)
    output = close_object({"schema": SCHEMA + ".independent-no-producer-verification.v1",
        "status": "PASS_INDEPENDENT_C76L_DUAL_BYTE_IDENTICAL__NO_PRODUCER__EXACT_INCIDENCE_BOUNDARY_CLOSED__ZERO_CREDIT",
        "dual_build_byte_identical": True, "producer_imported": False,
        "candidate_summary": summary, "coherent_attacks": coherent_attacks(),
        "terminal_byte_replay_after_outer_receipts": True,
        "verifier_file_sha256": sha_file(Path(__file__).resolve()),
        "formal_credit": 0, "global_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0})
    exclusive(args.output, canonical(output) + b"\n")
    print(json.dumps({"output": str(args.output), "object_sha256": output["object_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
