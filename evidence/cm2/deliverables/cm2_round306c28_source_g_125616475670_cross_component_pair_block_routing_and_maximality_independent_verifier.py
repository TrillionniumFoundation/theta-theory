#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from collections import defaultdict
from itertools import groupby
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c28_source_g_125616475670_cross_component_pair_block_routing_and_maximality"
BLOCK_LEDGER = PREFIX + "_member_home_block_census_ledger.jsonl.gz"
ROUTE_LEDGER = PREFIX + "_cross_component_pair_route_shard_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"

C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze"
C27 = "cm2_round306c27_source_g_corrected_transition_frontier_exhaustion_and_known_edge_recovery"
C15_MEMBER = C15 + "_member_component_ledger.jsonl.gz"
C15_COMPONENT = C15 + "_component_census_ledger.jsonl.gz"
C27_FRONTIER = C27 + "_transition_candidate_ledger.jsonl.gz"
C27_FAMILY = C27 + "_transition_family_coverage_ledger.jsonl.gz"

SOURCE_SPECS = (
    ("C15", C15, "a1eea2c41123d2ff7f7d3e1f35f1deabc5bae9d93b24f825b4831f6324c1e2c4", "99ad5fb9f2f940155effdcb24ac076824f6436f2d92a66bd6d9ed196d0ac8f71", (C15_MEMBER, C15_COMPONENT)),
    ("C27", C27, "26c0f7e5364630a5aafae690fc50cefd2091fe458432735b8bc2c0c3e13b631b", "3c547d24d602c751212c0c2e8fb15ef80413d2700093cfab5dd07f4e8d59235f", (C27_FRONTIER, C27_FAMILY)),
)

MEMBERS = 502204
COMPONENTS = 57876
BLOCKS = 256
SHARDS = 32896
TOTAL_PAIRS = 126104177706
WITHIN_PAIRS = 487702036
CROSS_PAIRS = 125616475670


class Reject(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def wire(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")


def sha(value: Any) -> str:
    return hashlib.sha256(wire(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            state.update(chunk)
    return state.hexdigest()


def invalid_constant(value: str) -> None:
    raise Reject("constant:" + value)


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        require(key not in value, "duplicate:" + key)
        value[key] = item
    return value


def parse(raw: bytes, label: str) -> Any:
    payload = raw[:-1] if raw.endswith(b"\n") else raw
    require(not payload.endswith(b"\n"), "trailing newlines:" + label)
    try:
        value = json.loads(payload.decode("ascii"), object_pairs_hook=no_duplicates, parse_constant=invalid_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Reject("JSON:" + label) from error
    require(wire(value) == payload, "canonical:" + label)
    return value


def ledger(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as source:
        for ordinal, line in enumerate(source):
            require(line.endswith(b"\n"), "newline:" + path.name)
            value = parse(line[:-1], path.name + ":" + str(ordinal))
            require(type(value) is dict, "row:" + path.name)
            body = dict(value)
            claimed = body.pop("row_sha256", None)
            require(type(claimed) is str and claimed == sha(body), "closure:" + path.name + ":" + str(ordinal))
            yield value


def result(path: Path) -> tuple[dict[str, Any], str]:
    value = parse(path.read_bytes(), path.name)
    require(type(value) is dict, "result type")
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    require(type(claimed) is str and claimed == sha(body), "result closure")
    return value, claimed


def manifest_entries(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for raw in path.read_text(encoding="ascii").splitlines():
        fields = raw.split(None, 1)
        require(len(fields) == 2 and len(fields[0]) == 64, "manifest line")
        name = Path(fields[1].strip()).name
        require(name == fields[1].strip() and name not in entries, "manifest name")
        entries[name] = fields[0]
    return entries


def seal_sources() -> tuple[dict[str, str], list[dict[str, str]]]:
    objects: dict[str, str] = {}
    pins: list[dict[str, str]] = []
    for tag, base, manifest_pin, object_pin, ledgers in SOURCE_SPECS:
        manifest_name = base + "_manifest.sha256"
        result_name = base + "_result.json"
        verification_name = base + "_verification.json"
        require(file_sha(ROOT / manifest_name) == manifest_pin, "manifest pin:" + tag)
        entries = manifest_entries(ROOT / manifest_name)
        for name in (*ledgers, result_name, verification_name):
            require(name in entries and file_sha(ROOT / name) == entries[name], "manifest member:" + tag + ":" + name)
        source_result, object_sha = result(ROOT / result_name)
        require(object_sha == object_pin and str(source_result.get("status", "")).startswith("PASS"), "object pin:" + tag)
        verification = parse((ROOT / verification_name).read_bytes(), verification_name)
        require(str(verification.get("status", "")).startswith("PASS"), "verification:" + tag)
        objects[tag] = object_sha
        pins.append({"filename": manifest_name, "sha256": manifest_pin})
        pins.extend({"filename": name, "sha256": entries[name]} for name in (*ledgers, result_name, verification_name))
    c15_result, _ = result(ROOT / (C15 + "_result.json"))
    c27_result, _ = result(ROOT / (C27 + "_result.json"))
    require(c15_result["fresh_universe_census"]["members"] == MEMBERS, "C15 members")
    require(c15_result["fresh_DSU_census"]["components"] == COMPONENTS, "C15 components")
    require(c15_result["fresh_DSU_census"]["cross_component_pair_denominator"] == CROSS_PAIRS, "C15 denominator")
    require(c27_result["formal_credit"]["transition_frontier_exhaustion_theorem"] == 1, "C27 theorem")
    require(c27_result["transition_candidate_census"]["new_legal_cross_component"] == 0 and c27_result["transition_candidate_census"]["unresolved"] == 0, "C27 closure")
    require(c27_result["strict_nonpromotion"]["pair_routing"] == 0, "C27 boundary")
    return objects, sorted(pins, key=lambda item: item["filename"])


def choose2(count: int) -> int:
    return count * (count - 1) // 2


def reconstruct() -> tuple[list[int], list[int], list[list[int]], dict[str, str]]:
    global_counts = [0] * BLOCKS
    members_by_component: dict[str, list[int]] = defaultdict(list)
    identities: set[str] = set()
    identity_sequence = hashlib.sha256()
    count = 0
    for ordinal, row in enumerate(ledger(ROOT / C15_MEMBER)):
        require(row["member_ordinal"] == ordinal, "member ordinal")
        identity = row["registry_member_id"]
        require(identity not in identities, "member duplicate")
        identities.add(identity)
        block = hashlib.sha256(identity.encode("ascii")).digest()[0]
        global_counts[block] += 1
        members_by_component[row["fresh_component_id"]].append(block)
        identity_sequence.update(identity.encode("ascii") + b"\n")
        count += 1
    require(count == MEMBERS and len(identities) == MEMBERS, "member count")

    component_sizes: dict[str, int] = {}
    for ordinal, row in enumerate(ledger(ROOT / C15_COMPONENT)):
        require(row["component_ordinal"] == ordinal, "component ordinal")
        component = row["fresh_component_id"]
        require(component not in component_sizes, "component duplicate")
        component_sizes[component] = row["member_count"]
    require(len(component_sizes) == COMPONENTS and set(component_sizes) == set(members_by_component), "component set")
    require(all(len(members_by_component[component]) == size for component, size in component_sizes.items()), "component sizes")

    presence = [0] * BLOCKS
    within = [[0] * BLOCKS for _ in range(BLOCKS)]
    component_vector = hashlib.sha256()
    direct_within = 0
    for component in sorted(members_by_component):
        blocks = sorted(members_by_component[component])
        grouped = [(block, sum(1 for _ in group)) for block, group in groupby(blocks)]
        component_vector.update(wire([component, grouped]) + b"\n")
        direct_within += choose2(len(blocks))
        for index, (left, left_count) in enumerate(grouped):
            presence[left] += 1
            within[left][left] += choose2(left_count)
            for right, right_count in grouped[index + 1:]:
                within[left][right] += left_count * right_count
    require(sum(global_counts) == MEMBERS and all(global_counts), "home block cover")
    require(direct_within == WITHIN_PAIRS, "within denominator")
    commitments = {
        "member_id_sequence_sha256": identity_sequence.hexdigest(),
        "block_member_count_vector_sha256": sha(global_counts),
        "component_block_count_vector_sha256": component_vector.hexdigest(),
    }
    return global_counts, presence, within, commitments


def closed(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": sha(body)}


def expected_block(block: int, counts: list[int], presence: list[int], within: list[list[int]], objects: dict[str, str]) -> dict[str, Any]:
    total = choose2(counts[block])
    internal = within[block][block]
    body = {
        "schema": "cm2.round306c28.source-g-member-home-block-census.v1.row.v1",
        "home_block_ordinal": block,
        "home_block_hex": f"{block:02x}",
        "home_block_definition": "FIRST_BYTE_SHA256_ASCII_REGISTRY_MEMBER_ID",
        "member_count": counts[block],
        "component_presence_count": presence[block],
        "same_block_total_unordered_pairs": total,
        "same_block_within_component_pairs": internal,
        "same_block_cross_component_pairs": total - internal,
        "source_binding": {"C15_result_sha256": objects["C15"]},
        "formal_credit": {"member_home_assignments": counts[block]},
        "strict_nonpromotion": {"pair_routing": 0, "B2": 0, "maximality": 0, "fibre": 0, "global_disposition": 0, "CM2": 0},
    }
    return closed(body)


def expected_route(ordinal: int, left: int, right: int, counts: list[int], within: list[list[int]], objects: dict[str, str]) -> dict[str, Any]:
    total = choose2(counts[left]) if left == right else counts[left] * counts[right]
    internal = within[left][right]
    cross = total - internal
    body = {
        "schema": "cm2.round306c28.source-g-cross-component-pair-route-shard.v1.row.v1",
        "shard_ordinal": ordinal,
        "canonical_home_block_pair": [f"{left:02x}", f"{right:02x}"],
        "left_member_count": counts[left],
        "right_member_count": counts[right],
        "same_home_block": left == right,
        "total_unordered_member_pairs": total,
        "within_component_member_pairs_excluded": internal,
        "cross_component_member_pairs_routed": cross,
        "pair_classification": {"EXACT_NONEDGE_BY_EXHAUSTED_C27_TRANSITION_COMPLEMENT": cross, "KNOWN_LEGAL_CROSS_COMPONENT": 0, "NEW_LEGAL_CROSS_COMPONENT": 0, "UNRESOLVED": 0},
        "proof_binding": {"C15_partition_result_sha256": objects["C15"], "C27_transition_frontier_theorem_result_sha256": objects["C27"], "canonical_pair_home_rule": "SORTED_FIRST_BYTE_SHA256_ASCII_REGISTRY_MEMBER_ID", "all_within_component_pairs_excluded_by_component_block_convolution": True, "all_remaining_pairs_are_cross_component": True, "C27_proves_no_admissible_legal_cross_component_transition": True},
        "formal_credit": {"pair_routes": cross, "exact_nonedge_classifications": cross},
        "strict_nonpromotion": {"new_DSU_edge": 0, "new_DSU_union": 0, "fibre": 0, "global_disposition": 0, "CM2": 0},
    }
    return closed(body)


def descriptor(path: Path, rows: int, sequence: str, order: str) -> dict[str, Any]:
    return {"filename": path.name, "row_count": rows, "size": path.stat().st_size, "sha256": file_sha(path), "row_sequence_sha256": sequence, "order": order}


def verify(candidate: Path) -> dict[str, Any]:
    require(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated runtime")
    preliminary, _ = result(candidate / RESULT)
    require(preliminary.get("status") == "PASS_ALL_125616475670_CROSS_COMPONENT_MEMBER_PAIRS_EXACTLY_ROUTED_AS_NONEDGES__B2_AND_MAXIMALITY_SEALED__FINAL_FIBRE_AUDIT_REQUIRED", "preflight status")
    require(preliminary.get("pair_route_census") == {"unordered_block_pair_shards": SHARDS, "closed_shards": SHARDS, "cross_component_pairs_routed": CROSS_PAIRS, "exact_nonedge_pairs": CROSS_PAIRS, "known_legal_cross_component_pairs": 0, "new_legal_cross_component_pairs": 0, "unresolved_pairs": 0}, "preflight pair census")
    require(preliminary.get("formal_credit") == {"B1A_consumed": 1, "transition_theorem_consumed": 1, "member_home_assignments": MEMBERS, "pair_route_shards": SHARDS, "pair_routing": CROSS_PAIRS, "pair_classification": CROSS_PAIRS, "exact_nonedges": CROSS_PAIRS, "B2": 1, "maximality": 1}, "preflight credit")
    require(preliminary.get("strict_nonpromotion") == {"new_DSU_edges": 0, "new_DSU_unions": 0, "fibre": 0, "global_disposition": 0, "D02": "BLOCKED_PENDING_FINAL_FIBRE_AND_GLOBAL_DISPOSITION_AUDIT", "D03": "NOT_REACHED", "D04": "NOT_MINTED", "CM2": "NO-GO_FOR_CLAIM"}, "preflight boundary")

    objects, pins = seal_sources()
    counts, presence, within, commitments = reconstruct()
    block_candidate = ledger(candidate / BLOCK_LEDGER)
    block_sequence = hashlib.sha256()
    for block in range(BLOCKS):
        actual = next(block_candidate, None)
        expected = expected_block(block, counts, presence, within, objects)
        require(actual is not None and actual == expected, "block reconstruction:" + str(block))
        block_sequence.update(bytes.fromhex(actual["row_sha256"]))
    require(next(block_candidate, None) is None, "block exhaustion")

    route_candidate = ledger(candidate / ROUTE_LEDGER)
    route_sequence = hashlib.sha256()
    ordinal = 0
    totals = [0, 0, 0]
    for left in range(BLOCKS):
        for right in range(left, BLOCKS):
            actual = next(route_candidate, None)
            expected = expected_route(ordinal, left, right, counts, within, objects)
            require(actual is not None and actual == expected, "route reconstruction:" + str(ordinal))
            route_sequence.update(bytes.fromhex(actual["row_sha256"]))
            totals[0] += actual["total_unordered_member_pairs"]
            totals[1] += actual["within_component_member_pairs_excluded"]
            totals[2] += actual["cross_component_member_pairs_routed"]
            ordinal += 1
    require(next(route_candidate, None) is None and ordinal == SHARDS, "route exhaustion")
    require(totals == [TOTAL_PAIRS, WITHIN_PAIRS, CROSS_PAIRS], "route totals")

    block_descriptor = descriptor(candidate / BLOCK_LEDGER, BLOCKS, block_sequence.hexdigest(), "HOME_BLOCK_00_THROUGH_FF")
    route_descriptor = descriptor(candidate / ROUTE_LEDGER, SHARDS, route_sequence.hexdigest(), "LEXICOGRAPHIC_UNORDERED_BLOCK_PAIRS_00_00_THROUGH_FF_FF")
    theorem = {"kind": "CORRECTED_B2_GLOBAL_PAIR_ROUTING_AND_COMPONENT_MAXIMALITY_THEOREM", "every_C15_member_has_exactly_one_deterministic_home_block": True, "every_canonical_unordered_member_pair_has_exactly_one_unordered_block_pair_shard": True, "all_32896_shards_are_disjoint_and_exhaustive": True, "within_component_pairs_are_removed_by_exact_component_block_convolution": True, "cross_component_pair_denominator_is_exact": CROSS_PAIRS, "C27_transition_frontier_is_exhaustive": True, "C27_has_zero_legal_cross_component_transitions": True, "every_cross_component_pair_is_an_exact_nonedge": True, "new_legal_cross_component_pair_count": 0, "unresolved_pair_count": 0, "C15_components_are_maximal_under_the_corrected_transition_relation": True}
    body = {
        "schema": "cm2.round306c28.source-g-125616475670-cross-component-pair-block-routing-and-maximality.v1",
        "status": "PASS_ALL_125616475670_CROSS_COMPONENT_MEMBER_PAIRS_EXACTLY_ROUTED_AS_NONEDGES__B2_AND_MAXIMALITY_SEALED__FINAL_FIBRE_AUDIT_REQUIRED",
        "corrected_partition_census": {"members": MEMBERS, "components": COMPONENTS, "total_unordered_member_pairs": TOTAL_PAIRS, "within_component_member_pairs": WITHIN_PAIRS, "cross_component_member_pairs": CROSS_PAIRS},
        "home_block_census": {"definition": "FIRST_BYTE_SHA256_ASCII_REGISTRY_MEMBER_ID", "blocks": BLOCKS, "nonempty_blocks": sum(count > 0 for count in counts), "members_assigned": sum(counts), **commitments},
        "pair_route_census": {"unordered_block_pair_shards": SHARDS, "closed_shards": SHARDS, "cross_component_pairs_routed": CROSS_PAIRS, "exact_nonedge_pairs": CROSS_PAIRS, "known_legal_cross_component_pairs": 0, "new_legal_cross_component_pairs": 0, "unresolved_pairs": 0},
        "B2_and_maximality_theorem": theorem,
        "B2_and_maximality_theorem_sha256": sha(theorem),
        "ledgers": {"member_home_block_census": block_descriptor, "cross_component_pair_route_shard": route_descriptor},
        "input_pins": pins,
        "formal_credit": {"B1A_consumed": 1, "transition_theorem_consumed": 1, "member_home_assignments": MEMBERS, "pair_route_shards": SHARDS, "pair_routing": CROSS_PAIRS, "pair_classification": CROSS_PAIRS, "exact_nonedges": CROSS_PAIRS, "B2": 1, "maximality": 1},
        "strict_nonpromotion": {"new_DSU_edges": 0, "new_DSU_unions": 0, "fibre": 0, "global_disposition": 0, "D02": "BLOCKED_PENDING_FINAL_FIBRE_AND_GLOBAL_DISPOSITION_AUDIT", "D03": "NOT_REACHED", "D04": "NOT_MINTED", "CM2": "NO-GO_FOR_CLAIM"},
        "required_next": "RECONSTRUCT_57876_COMPONENT_FIBRES_AND_ISSUE_GLOBAL_EXACT_KEY_DISPOSITIONS_THEN_AUDIT_D02_D03_D04_CM2_GATES",
    }
    expected_result = {**body, "result_sha256": sha(body)}
    actual_result, claimed = result(candidate / RESULT)
    require(actual_result == expected_result and claimed == expected_result["result_sha256"], "result reconstruction")
    return {"status": "PASS_INDEPENDENT_C28_502204_MEMBER_PARTITION_AND_32896_PAIR_ROUTE_SHARDS_RECONSTRUCTED__B2_MAXIMALITY_VALID", "result_sha256": claimed, "block_rows": BLOCKS, "route_rows": SHARDS, "cross_component_pairs": CROSS_PAIRS}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir")
    args = parser.parse_args()
    candidate = ROOT if args.candidate_dir is None else Path(args.candidate_dir).resolve()
    print(wire(verify(candidate)).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
